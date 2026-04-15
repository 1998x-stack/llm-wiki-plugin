#!/usr/bin/env python3
"""Reclassify raw/ files according to raw/re-map.json (folder-level mapping).

This script has NO hardcoded category rules. Claude generates raw/re-map.json
with the new folder structure; this script only executes the moves and updates.

Steps:
1. Read raw/re-map.json (folder-level: {"old_folder": "new_folder"})
2. Snapshot all raw files (pre-count)
3. Expand folder map to per-file moves
4. Move files + resolve conflicts
5. Snapshot again (post-count) and verify no files lost
6. Build raw/raw-wiki-map.json (raw → wiki page mapping)
7. Update wiki markdown source references
8. Clean up empty directories
9. Output JSON summary

Usage:
  python reclassify_raw.py [--dry-run]

Input:
  raw/re-map.json — folder-level mapping, e.g.:
  {
    "raw/articles/claude-mem": "raw/ai-tools/claude-mem",
    "raw/books/数值分析": "raw/books/math/numerical-analysis"
  }

Output:
  raw/raw-wiki-map.json — updated raw → wiki page mapping
  stdout — JSON summary with status, counts, etc.
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
RAW_DIR = VAULT / "raw"
REMAP_PATH = RAW_DIR / "re-map.json"
WIKI_MAP_PATH = RAW_DIR / "raw-wiki-map.json"


def snapshot_raw_files() -> set[str]:
    """Collect all non-ignored file paths under raw/ (relative to vault/)."""
    files = set()
    for root, dirs, fnames in os.walk(RAW_DIR):
        dirs[:] = [d for d in dirs if d not in ('.obsidian', '.git')]
        for fn in fnames:
            if fn in ('.DS_Store', '.gitkeep'):
                continue
            rel = os.path.relpath(os.path.join(root, fn), VAULT)
            files.add(rel)
    return files


def load_folder_map() -> dict[str, str]:
    """Load raw/re-map.json. Returns folder-level mapping {old: new}."""
    if not REMAP_PATH.exists():
        return {}
    with open(REMAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def expand_folder_map(folder_map: dict[str, str]) -> dict[str, str]:
    """Expand folder-level mapping to per-file mapping.

    Given {"raw/articles/claude-mem": "raw/ai-tools/claude-mem"},
    maps each file under the old folder to the corresponding new path.
    Skips folders that no longer exist or are already at target.
    """
    file_map: dict[str, str] = {}
    for old_folder, new_folder in folder_map.items():
        old_dir = VAULT / old_folder
        if not old_dir.exists():
            continue
        # Skip if old == new (case-insensitive for macOS)
        if old_folder.lower() == new_folder.lower():
            continue
        # Skip if old is a prefix of new (already a reorganized parent)
        if new_folder.lower().startswith(old_folder.lower() + "/"):
            continue
        for root, dirs, files in os.walk(old_dir):
            dirs[:] = [d for d in dirs if d not in ('.obsidian', '.git')]
            for fn in files:
                if fn in ('.DS_Store', '.gitkeep'):
                    continue
                old_abs = Path(root) / fn
                rel_within = old_abs.relative_to(old_dir)
                old_rel = str(Path(old_folder) / rel_within)
                new_rel = str(Path(new_folder) / rel_within)
                if old_rel != new_rel:
                    file_map[old_rel] = new_rel
    return file_map


def check_conflicts(file_map: dict[str, str]) -> dict[str, list[str]]:
    """Return dest paths that have multiple sources."""
    dest_to_src: dict[str, list[str]] = {}
    for old, new in file_map.items():
        dest_to_src.setdefault(new, []).append(old)
    return {d: s for d, s in dest_to_src.items() if len(s) > 1}


def resolve_conflicts(file_map: dict[str, str]) -> dict[str, str]:
    """Resolve conflicts by prefixing filename with source folder name."""
    conflicts = check_conflicts(file_map)
    conflict_dests = set(conflicts.keys())
    resolved = {}
    for old, new in file_map.items():
        if new in conflict_dests:
            # Use the immediate parent folder name of old as prefix
            old_parts = Path(old).parts
            # Find the folder name that differs from the new path
            prefix = old_parts[-2] if len(old_parts) > 1 else "unknown"
            new_path = Path(new)
            resolved[old] = str(new_path.parent / f"{prefix}--{new_path.name}")
        else:
            resolved[old] = new
    return resolved


def execute_moves(file_map: dict[str, str], dry_run: bool = False) -> int:
    """Move files. Returns count."""
    moved = 0
    for old_rel, new_rel in sorted(file_map.items()):
        old_abs = VAULT / old_rel
        new_abs = VAULT / new_rel
        if not old_abs.exists():
            continue
        if not dry_run:
            new_abs.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_abs), str(new_abs))
        moved += 1
    return moved


def build_raw_wiki_map() -> int:
    """Build raw/raw-wiki-map.json by scanning wiki pages. Returns entry count."""
    wiki_dir = VAULT / "wiki"
    raw_to_wiki: dict[str, list[str]] = {}

    for wf in wiki_dir.rglob("*.md"):
        text = wf.read_text(encoding="utf-8")
        rel_wiki = str(wf.relative_to(VAULT))

        # Find ## 来源 section
        m = re.search(r'^## 来源\s*\n(.*?)(?=^## |\Z)', text, re.MULTILINE | re.DOTALL)
        if not m:
            continue
        section = m.group(1)
        links = re.findall(r'\[\[(raw/[^\]|]+?)(?:\|[^\]]*?)?\]\]', section)
        for link in links:
            link = link.strip()
            if not link.endswith('.md') and not link.endswith('.html') and '.' not in link.split('/')[-1]:
                link += '.md'
            raw_to_wiki.setdefault(link, []).append(rel_wiki)

    sorted_map = {k: sorted(set(v)) for k, v in sorted(raw_to_wiki.items())}
    with open(WIKI_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, ensure_ascii=False, indent=2)
    return len(sorted_map)


def update_wiki_sources(file_map: dict[str, str]) -> tuple[int, int]:
    """Update [[raw/...]] references in wiki markdown files. Returns (files, refs)."""
    wiki_dir = VAULT / "wiki"
    # Build lookup including both .md and without-extension variants
    lookup = {}
    for old, new in file_map.items():
        lookup[old] = new
        if old.endswith('.md'):
            lookup[old[:-3]] = new[:-3] if new.endswith('.md') else new

    updated_files = 0
    updated_refs = 0
    for wiki_file in wiki_dir.rglob("*.md"):
        content = wiki_file.read_text(encoding="utf-8")
        new_content = content
        changed = False
        for old_path, new_path in lookup.items():
            if old_path in new_content:
                new_content = new_content.replace(old_path, new_path)
                changed = True
        if changed:
            wiki_file.write_text(new_content, encoding="utf-8")
            updated_refs += sum(1 for old in lookup if old in content)
            updated_files += 1
    return updated_files, updated_refs


def cleanup_empty_dirs() -> int:
    """Remove empty dirs (including those with only .DS_Store)."""
    removed = 0
    for root, dirs, files in os.walk(RAW_DIR, topdown=False):
        for d in dirs:
            dirpath = Path(root) / d
            if not dirpath.is_dir():
                continue
            contents = list(dirpath.iterdir())
            real = [c for c in contents if c.name not in ('.DS_Store', '.gitkeep')]
            if not real:
                for c in contents:
                    c.unlink()
                dirpath.rmdir()
                removed += 1
    return removed


def main():
    dry_run = "--dry-run" in sys.argv

    # 1. Load folder map
    folder_map = load_folder_map()
    if not folder_map:
        print(json.dumps({"status": "error", "reason": "raw/re-map.json not found or empty"}))
        sys.exit(1)

    # 2. Pre-snapshot
    pre_files = snapshot_raw_files()
    pre_count = len(pre_files)

    # 3. Expand to per-file map
    file_map = expand_folder_map(folder_map)
    if not file_map:
        # Rebuild raw-wiki-map anyway (might have new wiki pages)
        map_entries = build_raw_wiki_map()
        print(json.dumps({"status": "noop", "reason": "all folders already at target",
                          "pre_count": pre_count, "map_entries": map_entries}))
        return

    # 4. Resolve conflicts
    conflicts = check_conflicts(file_map)
    if conflicts:
        file_map = resolve_conflicts(file_map)
        remaining = check_conflicts(file_map)
        if remaining:
            print(json.dumps({"status": "error", "reason": "unresolvable conflicts",
                              "conflicts": remaining}, ensure_ascii=False))
            sys.exit(1)

    if dry_run:
        move_count = execute_moves(file_map, dry_run=True)
        print(json.dumps({
            "status": "dry_run",
            "pre_count": pre_count,
            "file_moves": len(file_map),
            "conflicts_resolved": len(conflicts),
            "would_move": move_count,
        }))
        return

    # 5. Execute moves
    move_count = execute_moves(file_map)

    # 6. Post-snapshot + integrity check
    post_files = snapshot_raw_files()
    post_count = len(post_files)

    missing = []
    for pf in pre_files:
        if pf in file_map:
            expected = file_map[pf]
            if expected not in post_files:
                missing.append({"old": pf, "expected_new": expected})
        elif pf not in post_files:
            missing.append({"old": pf, "expected_new": pf})

    if missing:
        print(json.dumps({
            "status": "error", "reason": "files lost during reorganization",
            "pre_count": pre_count, "post_count": post_count, "missing": missing,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 7. Build raw-wiki-map.json
    map_entries = build_raw_wiki_map()

    # 8. Update wiki references
    wiki_files_updated, wiki_refs_updated = update_wiki_sources(file_map)

    # 9. Cleanup
    dirs_removed = cleanup_empty_dirs()

    # 10. Output
    print(json.dumps({
        "status": "ok",
        "pre_count": pre_count,
        "post_count": post_count,
        "moved": move_count,
        "conflicts_resolved": len(conflicts),
        "map_entries": map_entries,
        "wiki_files_updated": wiki_files_updated,
        "wiki_refs_updated": wiki_refs_updated,
        "dirs_removed": dirs_removed,
    }))


if __name__ == "__main__":
    main()
