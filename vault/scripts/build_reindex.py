#!/usr/bin/env python3
"""Topic-clustered reindex: split index.md into maps/*.md files.

Usage:
    python3 scripts/build_reindex.py
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPT_DIR.parent
WIKI_DIR = VAULT_DIR / "wiki"
MAPS_DIR = VAULT_DIR / "maps"
INDEX_PATH = VAULT_DIR / "index.md"
SNAPSHOT_PATH = MAPS_DIR / "tmp.snapshot.json"

MIN_CLUSTER_SIZE = 2  # minimum pages to form a cluster


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("---", 3)
    if end == -1:
        return None, text
    try:
        fm = yaml.safe_load(text[3:end])
        return (fm, text[end + 3:].strip()) if isinstance(fm, dict) else (None, text)
    except yaml.YAMLError:
        return None, text


def extract_overview(body: str) -> str:
    m = re.search(r"## 概述\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
    if m:
        text = m.group(1).strip()
        return text[:80] + "..." if len(text) > 80 else text
    # fallback: first heading
    for line in body.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def cluster_pages(pages: list[dict]) -> dict[str, list[dict]]:
    """Cluster pages by shared tags using frequency analysis."""
    # Count global tag frequency
    tag_counter = Counter()
    for p in pages:
        for t in p["tags"]:
            tag_counter[t] += 1

    # For each page, pick the most frequent tag as its primary cluster
    clusters: dict[str, list[dict]] = defaultdict(list)
    for p in pages:
        if not p["tags"]:
            clusters["其他"].append(p)
            continue
        # Pick the tag with highest global frequency (= biggest cluster)
        best_tag = max(p["tags"], key=lambda t: tag_counter[t])
        clusters[best_tag].append(p)

    # Merge tiny clusters into 其他
    final: dict[str, list[dict]] = {}
    for name, members in clusters.items():
        if len(members) < MIN_CLUSTER_SIZE and name != "其他":
            final.setdefault("其他", []).extend(members)
        else:
            final[name] = members

    return final


def write_map_file(topic: str, pages: list[dict]):
    """Write a single maps/<topic>.md file."""
    entities = [p for p in pages if p["type"] == "entity"]
    concepts = [p for p in pages if p["type"] == "concept"]
    syntheses = [p for p in pages if p["type"] == "synthesis"]
    others = [p for p in pages if p["type"] not in ("entity", "concept", "synthesis")]

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "---",
        "type: map",
        f'topic: "{topic}"',
        f"page_count: {len(pages)}",
        f"updated: {today}",
        "---",
        "",
        f"# {topic}",
        "",
    ]

    def add_section(title: str, items: list[dict]):
        if not items:
            return
        lines.append(f"## {title}")
        for p in sorted(items, key=lambda x: x["title"]):
            conf = f" (confidence: {p['confidence']})" if p["confidence"] else ""
            overview = p["overview"]
            lines.append(f"- [[{p['title']}]] — {overview}{conf}")
        lines.append("")

    add_section("概念", concepts)
    add_section("实体", entities)
    add_section("综合分析", syntheses)
    add_section("其他", others)

    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    fp = MAPS_DIR / f"{topic}.md"
    fp.write_text("\n".join(lines), encoding="utf-8")
    return fp


def write_hub_index(clusters: dict[str, list[dict]], total: int):
    """Rewrite index.md as a lightweight hub."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "---",
        "type: index",
        f"updated: {today}",
        "---",
        "",
        "# 知识库目录",
        "",
        "> 本文件由 LLM 自动维护。详细索引见 maps/ 目录下的分类文件。",
        "",
        "## 主题索引",
        "",
    ]

    for topic in sorted(clusters.keys()):
        count = len(clusters[topic])
        lines.append(f"- [[maps/{topic}]] — {count} 个页面")

    lines.extend([
        "",
        "## 统计",
        "",
        f"- 总页面数: {total}",
        f"- 主题分类: {len(clusters)}",
        f"- 最后更新: {today}",
        "",
    ])

    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_snapshot(pages: list[dict], clusters: dict[str, list[dict]]):
    """Write maps/tmp.snapshot.json for integrity checking."""
    # Build reverse map: page path -> cluster name
    page_cluster = {}
    for cluster_name, members in clusters.items():
        for p in members:
            page_cluster[p["path"]] = cluster_name

    snapshot = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": len(pages),
        "pages": {
            p["path"]: {"title": p["title"], "cluster": page_cluster.get(p["path"], "其他")}
            for p in pages
        },
    }

    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Topic-clustered reindex")
    parser.parse_args()

    if not WIKI_DIR.exists():
        print(json.dumps({"error": "wiki/ directory not found"}))
        return

    # Scan all wiki pages
    pages = []
    for fp in sorted(WIKI_DIR.rglob("*.md")):
        text = fp.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm is None:
            continue
        rel_path = str(fp.relative_to(VAULT_DIR))
        pages.append({
            "path": rel_path,
            "title": fp.stem,
            "type": fm.get("type", "unknown"),
            "tags": fm.get("tags", []) or [],
            "confidence": fm.get("confidence"),
            "overview": extract_overview(body),
        })

    # Cluster
    clusters = cluster_pages(pages)

    # Clean old maps
    if MAPS_DIR.exists():
        for old in MAPS_DIR.glob("*.md"):
            old.unlink()

    # Write map files
    for topic, members in clusters.items():
        write_map_file(topic, members)

    # Write hub index
    write_hub_index(clusters, len(pages))

    # Write snapshot
    write_snapshot(pages, clusters)

    # Report
    report = {
        "status": "ok",
        "total_pages": len(pages),
        "clusters": {name: len(members) for name, members in sorted(clusters.items())},
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
