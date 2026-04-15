#!/usr/bin/env python3
"""Build raw-wiki-map.json: map each raw file to the list of wiki pages that reference it."""

import json
import os
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT / "wiki"
RAW_DIR = VAULT / "raw"


def extract_source_links(wiki_file: Path) -> list[str]:
    """Extract [[raw/...]] links from the ## 来源 section of a wiki page."""
    text = wiki_file.read_text(encoding="utf-8")

    # Find ## 来源 section
    source_match = re.search(r'^## 来源\s*\n(.*?)(?=^## |\Z)', text, re.MULTILINE | re.DOTALL)
    if not source_match:
        return []

    section = source_match.group(1)
    # Extract [[raw/...]] links — may have suffixes like " — §note"
    links = re.findall(r'\[\[(raw/[^\]|]+?)(?:\|[^\]]*?)?\]\]', section)
    # Normalize: strip trailing whitespace, ensure .md extension if missing
    result = []
    for link in links:
        link = link.strip()
        if not link.endswith('.md') and not link.endswith('.html') and '.' not in link.split('/')[-1]:
            link += '.md'
        result.append(link)
    return result


def build_map():
    raw_to_wiki: dict[str, list[str]] = {}

    wiki_files = list(WIKI_DIR.rglob("*.md"))
    for wf in wiki_files:
        rel_wiki = str(wf.relative_to(VAULT))
        raw_links = extract_source_links(wf)
        for raw_link in raw_links:
            if raw_link not in raw_to_wiki:
                raw_to_wiki[raw_link] = []
            raw_to_wiki[raw_link].append(rel_wiki)

    # Sort keys and values
    sorted_map = {}
    for k in sorted(raw_to_wiki.keys()):
        sorted_map[k] = sorted(set(raw_to_wiki[k]))

    out_path = RAW_DIR / "raw-wiki-map.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, ensure_ascii=False, indent=2)

    print(f"Built raw-wiki-map.json: {len(sorted_map)} raw files mapped to wiki pages")
    print(f"Total wiki references: {sum(len(v) for v in sorted_map.values())}")

    # Also print raw files NOT referenced by any wiki page
    all_raw_files = set()
    for root, dirs, files in os.walk(RAW_DIR):
        dirs[:] = [d for d in dirs if d != '.obsidian']
        for fn in files:
            if fn == '.DS_Store' or fn.endswith('.snapshot.md') or fn == '.gitkeep':
                continue
            rel = os.path.relpath(os.path.join(root, fn), VAULT)
            all_raw_files.add(rel)

    mapped_raw = set(sorted_map.keys())
    unmapped = sorted(all_raw_files - mapped_raw)
    print(f"\nUnmapped raw files (not referenced by any wiki page): {len(unmapped)}")
    for f in unmapped:
        print(f"  {f}")


if __name__ == "__main__":
    build_map()
