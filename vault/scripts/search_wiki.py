#!/usr/bin/env python3
"""Unified wiki search: BM25 + maps topic expansion + graph traversal with RRF fusion.

Usage:
    python3 scripts/search_wiki.py "query" [--top N] [--json]
"""

import argparse
import json
import pickle
import re
import sys
from pathlib import Path
from typing import Optional

import jieba
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPT_DIR.parent
WIKI_DIR = VAULT_DIR / "wiki"
INDEX_DIR = VAULT_DIR / "index" / "BM25"
MAPS_DIR = VAULT_DIR / "maps"
GRAPH_PATH = VAULT_DIR / "graph.json"

CORPUS_PATH = INDEX_DIR / "corpus.pkl"
INDEX_PATH = INDEX_DIR / "index.pkl"
DOCMAP_PATH = INDEX_DIR / "docmap.json"

WIKI_SUBDIRS = ["concepts", "entities", "syntheses", "qa-insights"]

STOP_WORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
    "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
    "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那", "些",
    "什么", "可以", "这个", "那个", "如果", "因为", "所以", "但是", "而且",
    "或者", "以及", "还是", "已经", "可能", "应该", "需要", "通过", "进行",
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "and", "or", "but", "if", "for", "of", "in", "on", "at", "to", "from",
    "by", "with", "as", "it", "its", "this", "that", "these", "those",
    "not", "no", "nor", "so", "than", "too", "very",
])


def tokenize(text: str) -> list[str]:
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"[#*`>|_\-=]", " ", text)
    tokens = list(jieba.cut_for_search(text))
    return [
        t.strip().lower()
        for t in tokens
        if t.strip() and t.strip().lower() not in STOP_WORDS and len(t.strip()) > 1
    ]


def read_frontmatter(path: Path) -> dict:
    """Read YAML frontmatter from a markdown file. Returns {} on failure."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def resolve_page_name(name: str) -> Optional[str]:
    """Try to find wiki/{subdir}/{name}.md. Return relative path from VAULT_DIR or None."""
    for subdir in WIKI_SUBDIRS:
        candidate = WIKI_DIR / subdir / f"{name}.md"
        if candidate.exists():
            return str(candidate.relative_to(VAULT_DIR))
    return None


# ---------------------------------------------------------------------------
# Retrieval strategies
# ---------------------------------------------------------------------------

def retrieve_bm25(query: str, top_n: int) -> list[tuple[str, float]]:
    """Return [(rel_path, bm25_score), ...] sorted descending."""
    if not INDEX_PATH.exists() or not CORPUS_PATH.exists() or not DOCMAP_PATH.exists():
        return []
    with open(INDEX_PATH, "rb") as f:
        bm25 = pickle.load(f)
    with open(CORPUS_PATH, "rb") as f:
        corpus = pickle.load(f)
    with open(DOCMAP_PATH, "r", encoding="utf-8") as f:
        docmap = json.load(f)

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    results = []
    for idx in top_indices:
        if scores[idx] <= 0:
            continue
        doc = corpus[idx]
        info = docmap.get(doc["id"], {})
        path = info.get("path", doc.get("path", ""))
        if path:
            results.append((path, float(scores[idx])))
    return results


def retrieve_maps(query: str) -> tuple:
    """Scan maps/*.md, find best topic match, return (rel_paths, topic_name)."""
    if not MAPS_DIR.exists():
        return [], None

    query_tokens = set(tokenize(query))
    if not query_tokens:
        return [], None

    best_topic = None
    best_overlap = 0
    best_map_path = None

    for map_file in MAPS_DIR.glob("*.md"):
        fm = read_frontmatter(map_file)
        topic = fm.get("topic", map_file.stem)
        topic_tokens = set(tokenize(topic))
        # Also tokenize the stem directly for short names like "AI"
        topic_tokens |= set(tokenize(map_file.stem))
        overlap = len(query_tokens & topic_tokens)
        # Fallback: substring match (e.g. query "牛顿法" → topic "数值分析")
        # Check if any query token appears in the topic string or vice versa
        if overlap == 0:
            for qt in query_tokens:
                if qt in topic or topic in qt:
                    overlap = 0.5
                    break
        if overlap > best_overlap:
            best_overlap = overlap
            best_topic = topic
            best_map_path = map_file

    if best_map_path is None or best_overlap == 0:
        return [], None

    # Extract [[PageName]] links from the map file
    text = best_map_path.read_text(encoding="utf-8")
    page_names = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", text)

    paths = []
    for name in page_names:
        rel = resolve_page_name(name.strip())
        if rel:
            paths.append(rel)

    return paths, best_topic


def retrieve_graph(seed_paths: list[str], graph_data: dict) -> list[str]:
    """1-hop BFS from seed_paths using graph edges. Return neighbor paths not in seeds."""
    if not graph_data:
        return []

    seed_set = set(seed_paths)
    # Build adjacency: node id → set of neighbor ids
    adjacency: dict[str, set[str]] = {}
    for edge in graph_data.get("edges", []):
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        if src and tgt:
            adjacency.setdefault(src, set()).add(tgt)
            adjacency.setdefault(tgt, set()).add(src)

    neighbors = []
    for seed in seed_paths:
        for neighbor in adjacency.get(seed, set()):
            if neighbor not in seed_set and neighbor not in neighbors:
                # Only include paths that exist on disk
                candidate = VAULT_DIR / neighbor
                if candidate.exists():
                    neighbors.append(neighbor)

    return neighbors


# ---------------------------------------------------------------------------
# RRF fusion
# ---------------------------------------------------------------------------

def rrf_fuse(
    bm25_results: list[tuple[str, float]],
    map_paths: list[str],
    graph_paths: list[str],
    topic_name: Optional[str],
    top_k: int,
) -> list:
    """Reciprocal Rank Fusion over three sources. Returns fused result dicts."""
    RRF_K = 60
    scores: dict[str, float] = {}
    sources: dict[str, list[str]] = {}

    def add_source(path: str, rank: int, source_label: str):
        rrf = 1.0 / (RRF_K + rank + 1)
        scores[path] = scores.get(path, 0.0) + rrf
        sources.setdefault(path, [])
        if source_label not in sources[path]:
            sources[path].append(source_label)

    for rank, (path, _) in enumerate(bm25_results):
        add_source(path, rank, "bm25")

    map_label = f"map:{topic_name}" if topic_name else "map"
    for rank, path in enumerate(map_paths):
        add_source(path, rank, map_label)

    for rank, path in enumerate(graph_paths):
        add_source(path, rank, "graph")

    # Sort by fused score descending
    ranked = sorted(scores.keys(), key=lambda p: scores[p], reverse=True)[:top_k]

    results = []
    for path in ranked:
        full_path = VAULT_DIR / path
        fm = read_frontmatter(full_path)
        title = fm.get("title", "") or Path(path).stem
        confidence = fm.get("confidence", None)
        results.append({
            "path": path,
            "score": round(scores[path], 6),
            "sources": sources[path],
            "confidence": confidence,
            "title": title,
        })
    return results


# ---------------------------------------------------------------------------
# Main search
# ---------------------------------------------------------------------------

def search(query: str, top_k: int = 15) -> dict:
    # BM25 — fetch top_k * 2 candidates
    bm25_results = retrieve_bm25(query, top_k * 2)

    # Maps topic expansion
    map_paths, topic_name = retrieve_maps(query)

    # Graph traversal — seed from BM25 top-5
    graph_data = {}
    if GRAPH_PATH.exists():
        with open(GRAPH_PATH, "r", encoding="utf-8") as f:
            graph_data = json.load(f)
    seed_paths = [p for p, _ in bm25_results[:5]]
    graph_paths = retrieve_graph(seed_paths, graph_data)

    # Count total unique candidates before trimming
    all_candidates = set()
    all_candidates.update(p for p, _ in bm25_results)
    all_candidates.update(map_paths)
    all_candidates.update(graph_paths)

    # RRF fusion
    fused = rrf_fuse(bm25_results, map_paths, graph_paths, topic_name, top_k)

    return {
        "query": query,
        "results": fused,
        "topic_context": topic_name,
        "total_candidates": len(all_candidates),
    }


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_human(output: dict) -> str:
    lines = []
    lines.append(f"Query: {output['query']}")
    if output["topic_context"]:
        lines.append(f"Topic: {output['topic_context']}")
    lines.append(f"Candidates: {output['total_candidates']}  Results: {len(output['results'])}")
    lines.append("")
    for i, r in enumerate(output["results"], 1):
        conf = f"  confidence={r['confidence']}" if r["confidence"] is not None else ""
        src = ", ".join(r["sources"])
        lines.append(f"{i:2}. [{r['score']:.4f}] {r['title']}")
        lines.append(f"    {r['path']}")
        lines.append(f"    sources={src}{conf}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Unified wiki search (BM25 + maps + graph + RRF)")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--top", type=int, default=15, help="Number of results (default: 15)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable text")
    args = parser.parse_args()

    result = search(args.query, args.top)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_human(result))


if __name__ == "__main__":
    main()
