#!/usr/bin/env python3
"""BM25 index manager for wiki/ pages.

Usage:
    python3 scripts/bm25_index.py build                 # Full rebuild
    python3 scripts/bm25_index.py update <file.md>       # Incremental update
    python3 scripts/bm25_index.py query "搜索词" -n 10   # Search
    python3 scripts/bm25_index.py remove <file.md>       # Remove from index
"""

import argparse
import json
import os
import pickle
import re
import sys
from pathlib import Path

import jieba
from rank_bm25 import BM25Okapi

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPT_DIR.parent
WIKI_DIR = VAULT_DIR / "wiki"
INDEX_DIR = VAULT_DIR / "index" / "BM25"

CORPUS_PATH = INDEX_DIR / "corpus.pkl"
INDEX_PATH = INDEX_DIR / "index.pkl"
DOCMAP_PATH = INDEX_DIR / "docmap.json"

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


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].strip()
    return text


def tokenize(text: str) -> list[str]:
    text = strip_frontmatter(text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"[#*`>|_\-=]", " ", text)
    tokens = list(jieba.cut_for_search(text))
    return [t.strip().lower() for t in tokens if t.strip() and t.strip().lower() not in STOP_WORDS and len(t.strip()) > 1]


def extract_title(text: str) -> str:
    for line in text.split("\n"):
        if line.startswith("title:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_type(text: str) -> str:
    for line in text.split("\n"):
        if line.startswith("type:"):
            return line.split(":", 1)[1].strip()
        if line.strip() == "---" and not text.startswith("---"):
            break
    return "unknown"


def load_state() -> tuple[list[dict], dict]:
    corpus = []
    docmap = {}
    if CORPUS_PATH.exists():
        with open(CORPUS_PATH, "rb") as f:
            corpus = pickle.load(f)
    if DOCMAP_PATH.exists():
        with open(DOCMAP_PATH, "r", encoding="utf-8") as f:
            docmap = json.load(f)
    return corpus, docmap


def save_state(corpus: list[dict], docmap: dict, tokenized_corpus: list[list[str]]):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with open(CORPUS_PATH, "wb") as f:
        pickle.dump(corpus, f)
    with open(DOCMAP_PATH, "w", encoding="utf-8") as f:
        json.dump(docmap, f, ensure_ascii=False, indent=2)
    if tokenized_corpus:
        bm25 = BM25Okapi(tokenized_corpus)
        with open(INDEX_PATH, "wb") as f:
            pickle.dump(bm25, f)
    elif INDEX_PATH.exists():
        INDEX_PATH.unlink()


def cmd_build():
    corpus = []
    docmap = {}
    tokenized = []
    if not WIKI_DIR.exists():
        print(json.dumps({"error": "wiki/ directory not found"}))
        sys.exit(2)
    md_files = sorted(WIKI_DIR.rglob("*.md"))
    for i, fp in enumerate(md_files):
        text = fp.read_text(encoding="utf-8")
        tokens = tokenize(text)
        rel_path = str(fp.relative_to(VAULT_DIR))
        doc_id = str(i)
        corpus.append({"id": doc_id, "tokens": tokens, "path": rel_path})
        docmap[doc_id] = {
            "path": rel_path,
            "title": extract_title(text),
            "type": extract_type(text),
            "updated": fp.stat().st_mtime,
        }
        tokenized.append(tokens)
    save_state(corpus, docmap, tokenized)
    print(json.dumps({"status": "ok", "indexed": len(corpus)}))


def cmd_update(file_path: str):
    fp = Path(file_path)
    if not fp.is_absolute():
        fp = VAULT_DIR / fp
    if not fp.exists():
        print(json.dumps({"error": f"file not found: {file_path}"}))
        sys.exit(2)
    rel_path = str(fp.relative_to(VAULT_DIR))
    text = fp.read_text(encoding="utf-8")
    tokens = tokenize(text)
    corpus, docmap = load_state()
    old_id = None
    for did, info in docmap.items():
        if info["path"] == rel_path:
            old_id = did
            break
    if old_id is not None:
        corpus = [c for c in corpus if c["id"] != old_id]
        del docmap[old_id]
    new_id = str(max((int(k) for k in docmap), default=-1) + 1)
    corpus.append({"id": new_id, "tokens": tokens, "path": rel_path})
    docmap[new_id] = {
        "path": rel_path,
        "title": extract_title(text),
        "type": extract_type(text),
        "updated": fp.stat().st_mtime,
    }
    tokenized = [c["tokens"] for c in corpus]
    save_state(corpus, docmap, tokenized)
    print(json.dumps({"status": "ok", "path": rel_path}))


def cmd_remove(file_path: str):
    fp = Path(file_path)
    if not fp.is_absolute():
        fp = VAULT_DIR / fp
    rel_path = str(fp.relative_to(VAULT_DIR))
    corpus, docmap = load_state()
    old_id = None
    for did, info in docmap.items():
        if info["path"] == rel_path:
            old_id = did
            break
    if old_id is None:
        print(json.dumps({"error": f"not in index: {rel_path}"}))
        sys.exit(1)
    corpus = [c for c in corpus if c["id"] != old_id]
    del docmap[old_id]
    tokenized = [c["tokens"] for c in corpus]
    save_state(corpus, docmap, tokenized)
    print(json.dumps({"status": "ok", "removed": rel_path}))


def cmd_query(query_str: str, top_n: int = 10):
    if not INDEX_PATH.exists():
        print(json.dumps({"error": "index not built. Run: python3 scripts/bm25_index.py build"}))
        sys.exit(1)
    with open(INDEX_PATH, "rb") as f:
        bm25 = pickle.load(f)
    corpus, docmap = load_state()
    query_tokens = tokenize(query_str)
    if not query_tokens:
        print(json.dumps([]))
        return
    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    results = []
    for idx in top_indices:
        if scores[idx] <= 0:
            continue
        doc = corpus[idx]
        info = docmap.get(doc["id"], {})
        results.append({
            "path": info.get("path", doc["path"]),
            "score": round(float(scores[idx]), 4),
            "title": info.get("title", ""),
            "type": info.get("type", "unknown"),
        })
    print(json.dumps(results, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="BM25 index manager for wiki/")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build", help="Full rebuild of BM25 index")
    p_update = sub.add_parser("update", help="Incremental update for one file")
    p_update.add_argument("file", help="Path to wiki file")
    p_remove = sub.add_parser("remove", help="Remove a file from index")
    p_remove.add_argument("file", help="Path to wiki file")
    p_query = sub.add_parser("query", help="Search the index")
    p_query.add_argument("query", help="Search query string")
    p_query.add_argument("-n", type=int, default=10, help="Number of results")
    args = parser.parse_args()
    if args.command == "build":
        cmd_build()
    elif args.command == "update":
        cmd_update(args.file)
    elif args.command == "remove":
        cmd_remove(args.file)
    elif args.command == "query":
        cmd_query(args.query, args.n)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
