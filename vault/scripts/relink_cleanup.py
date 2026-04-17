#!/usr/bin/env python3
"""Remove wrong [[wikilinks]] inserted by relink for short ASCII terms.

A link is "wrong" when the display text is an ASCII-only term shorter than
MIN_EN_TERM_LEN (5).  Patterns removed:
  [[shortterm]]          → shortterm
  [[pagename|shortterm]] → shortterm

Usage:
  python relink_cleanup.py [--dry-run] [--json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from wiki_utils import VAULT_DIR, WIKI_DIR, WIKI_SUBDIRS

MIN_EN_TERM_LEN = 5  # must match relink.py


def _is_ascii_term(term: str) -> bool:
    return all(c.isascii() for c in term)


def _is_wrong_link_display(display: str) -> bool:
    """Return True if display text is a short ASCII term that should not be linked."""
    return _is_ascii_term(display) and len(display) < MIN_EN_TERM_LEN


# Matches [[target]] and [[target|display]]
_WIKILINK_RE = re.compile(r'\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]')


def clean_page(text: str) -> tuple[str, int]:
    """Remove wrong wikilinks from page text. Returns (new_text, removed_count)."""
    removed = 0

    def replace(m: re.Match) -> str:
        nonlocal removed
        target = m.group(1)
        display = m.group(2)  # None if no pipe

        if display is None:
            # [[target]] — display text = target
            if _is_wrong_link_display(target):
                removed += 1
                return target
        else:
            # [[target|display]] — display text = display
            if _is_wrong_link_display(display):
                removed += 1
                return display

        return m.group(0)  # keep as-is

    new_text = _WIKILINK_RE.sub(replace, text)
    return new_text, removed


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    as_json = "--json" in sys.argv

    total_removed = 0
    pages_cleaned = 0
    details: list[dict] = []

    for subdir in WIKI_SUBDIRS:
        d = WIKI_DIR / subdir
        if not d.exists():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix != ".md":
                continue
            text = f.read_text(encoding="utf-8")
            new_text, removed = clean_page(text)
            if removed:
                if not dry_run:
                    f.write_text(new_text, encoding="utf-8")
                total_removed += removed
                pages_cleaned += 1
                details.append({
                    "page": f"{subdir}/{f.stem}",
                    "removed": removed,
                })

    result = {
        "status": "ok",
        "dry_run": dry_run,
        "pages_cleaned": pages_cleaned,
        "links_removed": total_removed,
    }
    if details:
        result["details"] = details

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Cleaned {pages_cleaned} pages, removed {total_removed} wrong links")
        for d in details[:20]:
            print(f"  {d['page']}: -{d['removed']}")
        if len(details) > 20:
            print(f"  ... and {len(details) - 20} more")


if __name__ == "__main__":
    main()
