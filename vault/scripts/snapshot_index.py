#!/usr/bin/env python3
"""Index integrity checker: ensures no wiki page is missing from index.md.

Usage:
    python3 scripts/snapshot_index.py              # check mode (default)
    python3 scripts/snapshot_index.py --update     # add missing entries to index.md
    python3 scripts/snapshot_index.py --snapshot    # save snapshot to .claude/reindex.snapshot.json
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPT_DIR.parent
WIKI_DIR = VAULT_DIR / "wiki"
INDEX_PATH = VAULT_DIR / "index.md"
SNAPSHOT_PATH = VAULT_DIR / ".claude" / "reindex.snapshot.json"

TYPE_SECTIONS = {
    "entity": "\u5b9e\u4f53 (wiki/entities/)",
    "concept": "\u6982\u5ff5 (wiki/concepts/)",
    "synthesis": "\u7efc\u5408\u5206\u6790 (wiki/syntheses/)",
    "qa-insight": "QA \u6d1e\u89c1 (wiki/qa-insights/)",
}


def parse_frontmatter(text):
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


def extract_overview(text):
    m = re.search(r"## \u6982\u8ff0\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if m:
        t = m.group(1).strip().split("\n")[0]
        return t[:80] + "..." if len(t) > 80 else t
    in_fm = False
    for line in text.split("\n"):
        if line.strip() == "---":
            in_fm = not in_fm
            continue
        if in_fm:
            continue
        if line.startswith("# "):
            continue
        if line.strip():
            t = line.strip()
            return t[:80] + "..." if len(t) > 80 else t
    return ""


def scan_wiki():
    """Scan all wiki pages, return {stem: {type, confidence, overview, path}}."""
    pages = {}
    for fp in sorted(WIKI_DIR.rglob("*.md")):
        text = fp.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            continue
        pages[fp.stem] = {
            "type": fm.get("type", "unknown"),
            "confidence": fm.get("confidence"),
            "overview": extract_overview(text),
            "path": str(fp.relative_to(VAULT_DIR)),
        }
    return pages


def parse_index():
    """Extract all [[page]] names from index.md."""
    if not INDEX_PATH.exists():
        return set()
    text = INDEX_PATH.read_text(encoding="utf-8")
    return set(re.findall(r"\[\[(.+?)\]\]", text)) - {"\u9875\u9762\u540d"}


def check(pages, indexed):
    """Compare wiki pages vs index entries."""
    wiki_names = set(pages.keys())
    missing = wiki_names - indexed
    orphaned = indexed - wiki_names
    return {
        "total_wiki": len(wiki_names),
        "total_indexed": len(indexed),
        "missing": sorted(missing),
        "orphaned": sorted(orphaned),
        "ok": len(missing) == 0 and len(orphaned) == 0,
    }


def update_index(pages, indexed):
    """Add missing entries to index.md in the correct sections."""
    missing = set(pages.keys()) - indexed
    if not missing:
        print(json.dumps({"status": "ok", "message": "index.md is up to date"}))
        return

    text = INDEX_PATH.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Group missing pages by type
    by_type = {}
    for name in missing:
        p = pages[name]
        by_type.setdefault(p["type"], []).append(name)

    for page_type, names in by_type.items():
        section_header = TYPE_SECTIONS.get(page_type, TYPE_SECTIONS["concept"])

        # Find the section
        section_idx = None
        for i, line in enumerate(lines):
            if section_header in line:
                section_idx = i
                break

        if section_idx is None:
            continue

        # Find last entry in section (last line starting with "- [[")
        insert_idx = section_idx + 1
        for i in range(section_idx + 1, len(lines)):
            if lines[i].startswith("- [["):
                insert_idx = i + 1
            elif lines[i].startswith("##") or (lines[i].strip() == "" and i > insert_idx):
                break

        # Insert new entries
        new_entries = []
        for name in sorted(names):
            p = pages[name]
            conf = f" (confidence: {p['confidence']})" if p["confidence"] else ""
            new_entries.append(f"- [[{name}]] \u2014 {p['overview']}{conf}")

        for j, entry in enumerate(new_entries):
            lines.insert(insert_idx + j, entry)

    # Update stats
    entity_count = sum(1 for p in pages.values() if p["type"] == "entity")
    concept_count = sum(1 for p in pages.values() if p["type"] == "concept")
    synthesis_count = sum(1 for p in pages.values() if p["type"] == "synthesis")
    total = len(pages)
    today = datetime.now().strftime("%Y-%m-%d")

    for i, line in enumerate(lines):
        if line.startswith("updated:"):
            lines[i] = f"updated: {today}"
        elif line.startswith("- \u603b\u9875\u9762\u6570\uff1a"):
            lines[i] = f"- \u603b\u9875\u9762\u6570\uff1a{total}"
        elif line.startswith("- \u5b9e\u4f53\uff1a"):
            lines[i] = f"- \u5b9e\u4f53\uff1a{entity_count}"
        elif line.startswith("- \u6982\u5ff5\uff1a"):
            lines[i] = f"- \u6982\u5ff5\uff1a{concept_count}"
        elif "\u7efc\u5408\u5206\u6790" in line and line.startswith("- "):
            lines[i] = f"- \u7efc\u5408\u5206\u6790\uff1a{synthesis_count}"
        elif line.startswith("- \u6700\u540e\u66f4\u65b0\uff1a"):
            lines[i] = f"- \u6700\u540e\u66f4\u65b0\uff1a{today}"

    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "status": "updated",
        "added": len(missing),
        "entries": sorted(missing),
    }, ensure_ascii=False, indent=2))


def save_snapshot(pages):
    """Save snapshot for integrity tracking."""
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "total": len(pages),
        "pages": {
            name: {"type": p["type"], "confidence": p["confidence"], "path": p["path"]}
            for name, p in sorted(pages.items())
        },
    }
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(json.dumps({"status": "ok", "snapshot": str(SNAPSHOT_PATH), "pages": len(pages)}))


def main():
    parser = argparse.ArgumentParser(description="Index integrity checker")
    parser.add_argument("--update", action="store_true", help="Add missing entries to index.md")
    parser.add_argument("--snapshot", action="store_true", help="Save snapshot JSON")
    args = parser.parse_args()

    pages = scan_wiki()
    indexed = parse_index()

    if args.snapshot:
        save_snapshot(pages)
        return

    if args.update:
        update_index(pages, indexed)
        return

    # Default: check mode
    result = check(pages, indexed)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
