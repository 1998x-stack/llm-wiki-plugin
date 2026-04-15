#!/usr/bin/env python3
"""Build compact context package for ingest subagents.

Scans wiki state and schema files, outputs a single JSON object
that gives an ingest subagent everything it needs without reading
multiple files.

Usage:
    python3 scripts/build_ingest_context.py
"""

import json
import sys
from pathlib import Path

from wiki_utils import VAULT_DIR, WIKI_DIR, WIKI_SUBDIRS, parse_frontmatter

SCHEMA_DIR = VAULT_DIR / "_schema"
TEMPLATE_PATH = VAULT_DIR / "templates" / "wiki-page.md"


def scan_existing_pages() -> list[dict]:
    """Scan wiki/ for all pages, return compact list."""
    pages = []
    for subdir in WIKI_SUBDIRS:
        dirpath = WIKI_DIR / subdir
        if not dirpath.exists():
            continue
        for fp in sorted(dirpath.glob("*.md")):
            text = fp.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(text)
            name = fp.stem
            page_type = fm.get("type", subdir.rstrip("s")) if fm else "unknown"
            aliases = fm.get("aliases", []) if fm else []
            pages.append({
                "name": name,
                "type": page_type,
                "path": str(fp.relative_to(VAULT_DIR)),
                "aliases": aliases if isinstance(aliases, list) else [],
            })
    return pages


def build_compact_schema() -> str:
    """Merge entity-types, relationship-types, quality-rules into one compact string."""
    parts = []

    # Entity types
    et = SCHEMA_DIR / "entity-types.md"
    if et.exists():
        text = et.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        parts.append("### Entity Types\n" + body.strip())

    # Relationship types
    rt = SCHEMA_DIR / "relationship-types.md"
    if rt.exists():
        text = rt.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        parts.append("### Relationship Types\n" + body.strip())

    # Quality rules
    qr = SCHEMA_DIR / "quality-rules.md"
    if qr.exists():
        text = qr.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        parts.append("### Quality Rules\n" + body.strip())

    return "\n\n".join(parts)


def build_template() -> str:
    """Read wiki-page template."""
    if TEMPLATE_PATH.exists():
        return TEMPLATE_PATH.read_text(encoding="utf-8")
    return ""


def build():
    if not WIKI_DIR.exists():
        print(json.dumps({"error": "wiki/ directory not found"}))
        sys.exit(2)

    pages = scan_existing_pages()
    schema = build_compact_schema()
    template = build_template()

    # Stats
    entities = sum(1 for p in pages if p["type"] == "entity")
    concepts = sum(1 for p in pages if p["type"] == "concept")

    # Build page list string (compact: one line per page, no aliases to save tokens)
    page_lines = []
    for p in pages:
        page_lines.append(f"- {p['name']} [{p['type']}]")
    existing_pages_text = "\n".join(page_lines)

    output = {
        "status": "ok",
        "stats": {
            "total_pages": len(pages),
            "entities": entities,
            "concepts": concepts,
        },
        "existing_pages": existing_pages_text,
        "schema_compact": schema,
        "template": template,
    }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    build()
