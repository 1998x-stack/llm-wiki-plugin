#!/usr/bin/env python3
"""Generate statistics JSON from graph.json and wiki frontmatter.

Usage:
    python3 scripts/build_statistics.py [--output ../static/graph-statistics.json]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPT_DIR.parent
WIKI_DIR = VAULT_DIR / "wiki"
GRAPH_PATH = VAULT_DIR / "graph.json"
DEFAULT_OUTPUT = VAULT_DIR.parent / "static" / "graph-statistics.json"


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(text[3:end])
        return fm if isinstance(fm, dict) else None
    except yaml.YAMLError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Build statistics JSON")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    output_path = Path(args.output)

    # Load graph.json
    if not GRAPH_PATH.exists():
        print(json.dumps({"error": "graph.json not found. Run build_graph.py first."}))
        return

    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    metadata = graph.get("metadata", {})

    # Type distribution
    type_dist = Counter(n.get("type", "unknown") for n in nodes)

    # Confidence distribution
    conf_buckets = {"0.0-0.3": 0, "0.3-0.5": 0, "0.5-0.7": 0, "0.7-0.9": 0, "0.9-1.0": 0}
    for n in nodes:
        c = n.get("confidence")
        if c is None:
            continue
        if c < 0.3:
            conf_buckets["0.0-0.3"] += 1
        elif c < 0.5:
            conf_buckets["0.3-0.5"] += 1
        elif c < 0.7:
            conf_buckets["0.5-0.7"] += 1
        elif c < 0.9:
            conf_buckets["0.7-0.9"] += 1
        else:
            conf_buckets["0.9-1.0"] += 1

    # Top connected nodes
    top_connected = sorted(nodes, key=lambda n: n.get("edge_count", 0), reverse=True)[:20]
    top_list = [{"label": n["label"], "type": n.get("type", "unknown"), "edge_count": n.get("edge_count", 0)} for n in top_connected]

    # Tag frequency from wiki pages
    tag_counter = Counter()
    growth_dates = Counter()

    for fp in sorted(WIKI_DIR.rglob("*.md")):
        text = fp.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            continue
        for t in (fm.get("tags") or []):
            tag_counter[t] += 1
        created = fm.get("created")
        if created:
            growth_dates[str(created)] += 1

    # Relationship type distribution
    rel_counter = Counter(e.get("relation", "unknown") for e in edges)

    # Growth timeline: cumulative
    growth_timeline = {}
    cumulative = 0
    for date_str in sorted(growth_dates.keys()):
        cumulative += growth_dates[date_str]
        growth_timeline[date_str] = cumulative

    # Build output
    stats = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "total_nodes": metadata.get("total_nodes", len(nodes)),
            "total_edges": metadata.get("total_edges", len(edges)),
            "orphan_count": metadata.get("orphan_count", 0),
            "component_count": metadata.get("component_count", 1),
        },
        "type_distribution": dict(type_dist.most_common()),
        "confidence_distribution": conf_buckets,
        "top_connected": top_list,
        "tag_frequency": dict(tag_counter.most_common(30)),
        "growth_timeline": growth_timeline,
        "relationship_types": dict(rel_counter.most_common()),
        "orphans": graph.get("orphans", []),
        "components": [
            {"id": c["id"], "size": c["size"]}
            for c in graph.get("components", [])
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps({"status": "ok", "output": str(output_path)}))


if __name__ == "__main__":
    main()
