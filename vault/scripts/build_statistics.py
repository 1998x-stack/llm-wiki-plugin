#!/usr/bin/env python3
"""Generate statistics JSON from graph.json and wiki frontmatter.

Usage:
    python3 scripts/build_statistics.py [--output ../static/graph-statistics.json]

Requires: pyyaml, networkx
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from wiki_utils import VAULT_DIR, WIKI_DIR, GRAPH_PATH, parse_frontmatter

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False
    print("WARNING: networkx not installed — advanced graph metrics unavailable", file=sys.stderr)

DEFAULT_OUTPUT = VAULT_DIR.parent / "static" / "graph-statistics.json"


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
        fm, _ = parse_frontmatter(text)
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

    # --- NetworkX graph analysis ---
    nx_stats = {}
    if HAS_NX and nodes:
        G = nx.Graph()
        for n in nodes:
            G.add_node(n["id"], label=n["label"], type=n.get("type", "unknown"))
        for e in edges:
            G.add_edge(e["source"], e["target"], relation=e.get("relation", "unknown"))

        # Degree distribution
        degrees = [d for _, d in G.degree()]
        avg_degree = sum(degrees) / len(degrees) if degrees else 0
        degree_hist = Counter(degrees)

        # Betweenness centrality (top 15)
        bc = nx.betweenness_centrality(G)
        top_betweenness = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:15]
        top_betweenness_list = [
            {"id": nid, "label": G.nodes[nid].get("label", nid), "betweenness": round(v, 4)}
            for nid, v in top_betweenness
        ]

        # PageRank (top 15)
        pr = nx.pagerank(G)
        top_pagerank = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:15]
        top_pagerank_list = [
            {"id": nid, "label": G.nodes[nid].get("label", nid), "pagerank": round(v, 4)}
            for nid, v in top_pagerank
        ]

        # Clustering coefficient
        cc = nx.clustering(G)
        avg_clustering = round(nx.average_clustering(G), 4)
        top_clustering = sorted(cc.items(), key=lambda x: x[1], reverse=True)[:10]
        top_clustering_list = [
            {"id": nid, "label": G.nodes[nid].get("label", nid), "clustering": round(v, 4)}
            for nid, v in top_clustering if v > 0
        ]

        # Diameter and radius (on largest component)
        largest_cc = max(nx.connected_components(G), key=len)
        subG = G.subgraph(largest_cc)
        try:
            diameter = nx.diameter(subG)
            radius = nx.radius(subG)
            center_nodes = list(nx.center(subG))[:5]
            center_labels = [G.nodes[n].get("label", n) for n in center_nodes]
        except nx.NetworkXError:
            diameter = radius = 0
            center_labels = []

        # Density
        density = round(nx.density(G), 4)

        # Bridge edges (removing them disconnects the graph)
        bridges = list(nx.bridges(G))

        nx_stats = {
            "avg_degree": round(avg_degree, 2),
            "degree_distribution": {str(k): v for k, v in sorted(degree_hist.items())},
            "density": density,
            "diameter": diameter,
            "radius": radius,
            "center_nodes": center_labels,
            "avg_clustering": avg_clustering,
            "bridge_count": len(bridges),
            "top_betweenness": top_betweenness_list,
            "top_pagerank": top_pagerank_list,
            "top_clustering": top_clustering_list,
        }

    # Build output
    stats = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "total_nodes": metadata.get("total_nodes", len(nodes)),
            "total_edges": metadata.get("total_edges", len(edges)),
            "orphan_count": metadata.get("orphan_count", 0),
            "component_count": metadata.get("component_count", 1),
            "avg_degree": nx_stats.get("avg_degree", 0),
            "density": nx_stats.get("density", 0),
            "diameter": nx_stats.get("diameter", 0),
            "avg_clustering": nx_stats.get("avg_clustering", 0),
            "bridge_count": nx_stats.get("bridge_count", 0),
        },
        "type_distribution": dict(type_dist.most_common()),
        "confidence_distribution": conf_buckets,
        "top_connected": top_list,
        "top_betweenness": nx_stats.get("top_betweenness", []),
        "top_pagerank": nx_stats.get("top_pagerank", []),
        "top_clustering": nx_stats.get("top_clustering", []),
        "degree_distribution": nx_stats.get("degree_distribution", {}),
        "center_nodes": nx_stats.get("center_nodes", []),
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
