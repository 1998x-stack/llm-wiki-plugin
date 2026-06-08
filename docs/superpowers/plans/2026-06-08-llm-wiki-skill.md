# LLM Wiki Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract the llm-wiki knowledge management system into a portable, installable Claude Code skill (`llm-wiki`).

**Architecture:** All logic lives in the skill directory. Scripts discover the user's wiki root via `.wiki-root` marker file or `LLM_WIKI_ROOT` env var. Skill defaults (schemas, templates) are overrideable by user. PostToolUse hooks maintain BM25 index and graph.json on each wiki edit.

**Tech Stack:** Python 3.10+ (jieba, rank_bm25, pyyaml, markitdown), Bash (hooks + wrapper), Claude Code skill framework.

**Source:** Extracts and adapts files from `vault/scripts/`, `vault/_schema/`, `vault/templates/`.

**Output:** `llm-wiki-skill/` directory at repo root, ready for install via skill-creator.

---

## File Map

| File | Responsibility | Source |
|------|---------------|--------|
| `SKILL.md` | Entry point: core rules, path discovery, command index | New (derived from `_schema/CLAUDE.md`) |
| `commands/init.md` | One-time wiki initialization workflow | New |
| `commands/ingest.md` | Knowledge extraction with format auto-routing | New (merged from ingest + convert-to-markdown + qa-import) |
| `commands/ingest-loop.md` | Batch ingest via ingest_loop.py | Adapted from `.claude/commands/wiki/ingest-loop.md` |
| `commands/query.md` | Unified search + answer workflow | Adapted from `.claude/commands/wiki/query.md` |
| `commands/journal.md` | Daily/reflection/judgment with !insight | Adapted from `.claude/commands/wiki/journal.md` |
| `commands/review.md` | Health check + review + crystallize + consolidate | Merged from review + crystallize + consolidate |
| `commands/maintain.md` | check + lint + reindex + keywords + graph pipeline | Adapted from `.claude/commands/wiki/maintain.md` |
| `scripts/wiki_utils.py` | Shared: path discovery, frontmatter, tokenize, constants | Modified from `vault/scripts/wiki_utils.py` |
| `scripts/wiki.sh` | Wrapper: CWD + PYTHONPATH resolution | Modified from `vault/scripts/wiki.sh` |
| `scripts/bm25_index.py` | BM25 search index manager | Modified (new path imports) |
| `scripts/search_wiki.py` | Unified search: BM25 + maps + graph + RRF | Modified (new path imports) |
| `scripts/build_graph.py` | Knowledge graph JSON builder (no --full) | Modified (new path imports, remove --full) |
| `scripts/build_maps.py` | Per-topic map generator with cold-start guard | Modified (new path imports, 20-page threshold) |
| `scripts/build_keywords.py` | Jieba custom dictionary builder | Modified (new path imports) |
| `scripts/build_ingest_context.py` | Compact context for ingest subagents (layered schema) | Modified (new path imports, layered override) |
| `scripts/lint_wiki.py` | 9-item wiki quality checker | Modified (new path imports, WIKI_SUBDIRS=3) |
| `scripts/snapshot_index.py` | Index integrity: check/update/snapshot/slim | Modified (new path imports, no qa-insight type) |
| `scripts/relink.py` | Auto-link unlinked term mentions | Modified (new path imports, WIKI_SUBDIRS=3) |
| `scripts/qwen_ingest.py` | Qwen API wiki extraction | Modified (discover_wiki_root, no __file__ path) |
| `scripts/ingest_loop.py` | Batch ingest: hash tracking + resume + auto-relink | **New** |
| `scripts/hooks/bm25.sh` | PostToolUse: BM25 incremental index update | **New** |
| `scripts/hooks/graph.sh` | PostToolUse: graph rebuild with 30s debounce | **New** |
| `scripts/requirements.txt` | Python dependencies (no markdown/networkx/scipy) | Modified from root `requirements.txt` |
| `schemas/entity-types.md` | Entity type definitions | Copy from `vault/_schema/entity-types.md` |
| `schemas/relationship-types.md` | Relationship type definitions | Copy from `vault/_schema/relationship-types.md` |
| `schemas/quality-rules.md` | Quality rules + lint format | Copy from `vault/_schema/quality-rules.md` |
| `templates/wiki-page.md` | Wiki page template (with decay_rate field) | Modified from `vault/templates/wiki-page.md` |
| `templates/daily.md` | Daily journal template (bilingual) | Modified from `vault/templates/daily.md` |
| `templates/reflection.md` | Reflection template (bilingual) | Modified from `vault/templates/reflection.md` |
| `templates/judgment.md` | Judgment template (bilingual) | Modified from `vault/templates/judgment.md` |
| `templates/weekly-review.md` | Weekly review template (bilingual) | Modified from `vault/templates/weekly-review.md` |
| `resources/init-kit/` | Scaffold for /llm-wiki:init | New (skeleton dirs + empty marker files) |

---

### Task 1: Create skill directory skeleton

**Files:**
- Create: `llm-wiki-skill/SKILL.md` (empty placeholder)
- Create: `llm-wiki-skill/scripts/requirements.txt`
- Create: `llm-wiki-skill/resources/init-kit/.wiki-root` (empty)
- Create: `llm-wiki-skill/resources/init-kit/index.md` (initial skeleton)
- Create: `llm-wiki-skill/resources/init-kit/log.md` (empty)

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p llm-wiki-skill/{commands,scripts/hooks,schemas,templates,resources/init-kit}
mkdir -p llm-wiki-skill/resources/init-kit/{raw/qa,wiki/{entities,concepts,syntheses},journal/{daily,reflections,judgments,growth},maps}
```

- [ ] **Step 2: Create .wiki-root marker**

```bash
touch llm-wiki-skill/resources/init-kit/.wiki-root
```

- [ ] **Step 3: Create initial index.md skeleton**

Write `llm-wiki-skill/resources/init-kit/index.md`:
```markdown
---
type: index
updated: {{date}}
---

# 知识库目录

> 本文件由 LLM 自动维护。详细清单见各 `maps/*.md`。

## 统计

| 主题 | 概念 | 实体 | 合计 | map |
|------|------|------|------|-----|

总计: 0 页

## 全部页面

（暂无页面）
```

- [ ] **Step 4: Create empty log.md**

```bash
touch llm-wiki-skill/resources/init-kit/log.md
```

- [ ] **Step 5: Create requirements.txt**

Write `llm-wiki-skill/scripts/requirements.txt`:
```
jieba>=0.42
rank_bm25>=0.2.2
pyyaml>=6.0
openai>=1.0.0
markitdown>=0.1
```

(Removed: `markdown`, `networkx`, `scipy` — no static site/statistics.)

- [ ] **Step 6: Create empty SKILL.md placeholder**

```bash
touch llm-wiki-skill/SKILL.md
```

---

### Task 2: Copy and adapt wiki_utils.py

**Files:**
- Copy: `vault/scripts/wiki_utils.py` → `llm-wiki-skill/scripts/wiki_utils.py`
- Modify: path constants section

- [ ] **Step 1: Copy the file**

```bash
cp vault/scripts/wiki_utils.py llm-wiki-skill/scripts/wiki_utils.py
```

- [ ] **Step 2: Replace path constants section (lines 20-34)**

Replace:
```python
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPT_DIR.parent
WIKI_DIR = VAULT_DIR / "wiki"
INDEX_DIR = VAULT_DIR / "index" / "BM25"
MAPS_DIR = VAULT_DIR / "maps"
GRAPH_PATH = VAULT_DIR / "graph.json"
INDEX_FILE = VAULT_DIR / "index.md"

WIKI_SUBDIRS = ["concepts", "entities", "syntheses", "qa-insights"]

KEYWORDS_PATH = WIKI_DIR / "keywords.txt"
```

With:
```python
SKILL_DIR = Path(__file__).resolve().parent.parent  # <skill>/


def discover_wiki_root() -> Path:
    """Find the user's wiki root directory.

    1. LLM_WIKI_ROOT env var (highest priority)
    2. Walk up from CWD looking for .wiki-root marker
    3. Raise if not found
    """
    if env_root := os.environ.get("LLM_WIKI_ROOT"):
        root = Path(env_root)
        if root.is_dir():
            return root
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".wiki-root").exists():
            return parent
    raise RuntimeError(
        "Wiki root not found. Set LLM_WIKI_ROOT or run /llm-wiki:init"
    )


VAULT_DIR = discover_wiki_root()
WIKI_DIR = VAULT_DIR / "wiki"
INDEX_DIR = VAULT_DIR / "index" / "BM25"
MAPS_DIR = VAULT_DIR / "maps"
GRAPH_PATH = VAULT_DIR / "graph.json"
INDEX_FILE = VAULT_DIR / "index.md"

WIKI_SUBDIRS = ["concepts", "entities", "syntheses"]

KEYWORDS_PATH = WIKI_DIR / "keywords.txt"
```

- [ ] **Step 3: Add `os` import at top if missing**

Check if `import os` exists; if not, add after `from pathlib import Path`:
```python
import os
```

- [ ] **Step 4: Verify the file is valid Python**

```bash
cd llm-wiki-skill && python3 -c "import sys; sys.path.insert(0, 'scripts'); import ast; ast.parse(open('scripts/wiki_utils.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

---

### Task 3: Copy and adapt wiki.sh

**Files:**
- Copy: `vault/scripts/wiki.sh` → `llm-wiki-skill/scripts/wiki.sh`
- Modify: VAULT_DIR discovery, SCRIPT_DIR derivation

- [ ] **Step 1: Copy the file**

```bash
cp vault/scripts/wiki.sh llm-wiki-skill/scripts/wiki.sh
```

- [ ] **Step 2: Rewrite wiki.sh**

Replace entire content with:
```bash
#!/usr/bin/env bash
# wiki.sh — Wrapper for all wiki Python scripts.
#
# Resolves CWD to the user's wiki root (via .wiki-root marker) and
# PYTHONPATH to the skill's scripts/ directory.
#
# Usage: bash scripts/wiki.sh <script_name> [args...]

set -euo pipefail

# Resolve symlinks to find the real script location (skill's scripts/)
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
    DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
    SOURCE="$(readlink "$SOURCE")"
    [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Discover user's wiki root by walking up from CWD
find_wiki_root() {
    local dir="$PWD"
    while true; do
        if [ -f "$dir/.wiki-root" ]; then
            echo "$dir"
            return 0
        fi
        if [ "$dir" = "/" ]; then
            break
        fi
        dir="$(dirname "$dir")"
    done
    # Fallback: env var
    if [ -n "${LLM_WIKI_ROOT:-}" ] && [ -d "$LLM_WIKI_ROOT" ]; then
        echo "$LLM_WIKI_ROOT"
        return 0
    fi
    echo "ERROR: Wiki root not found. Set LLM_WIKI_ROOT or run /llm-wiki:init" >&2
    return 1
}

VAULT_DIR="$(find_wiki_root)"

if [ $# -lt 1 ]; then
    echo "Usage: bash scripts/wiki.sh <script_name> [args...]"
    echo ""
    echo "Available scripts:"
    for f in "$SCRIPT_DIR"/*.py; do
        name=$(basename "$f" .py)
        [ "$name" = "wiki_utils" ] && continue
        [ "$name" = "__init__" ] && continue
        echo "  $name"
    done
    exit 1
fi

SCRIPT_NAME="$1"
shift

TARGET="$SCRIPT_DIR/${SCRIPT_NAME}.py"

if [ ! -f "$TARGET" ]; then
    echo "Error: script not found: $TARGET" >&2
    exit 1
fi

cd "$VAULT_DIR"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH:-}"
exec python3 "$TARGET" "$@"
```

- [ ] **Step 3: Make executable and verify**

```bash
chmod +x llm-wiki-skill/scripts/wiki.sh
bash llm-wiki-skill/scripts/wiki.sh 2>&1 | head -5
```

Expected: "Error: script not found" or usage output (since no script name provided).

---

### Task 4: Copy and adapt remaining Python scripts (path import changes)

**Files:** Modify 10 scripts in `llm-wiki-skill/scripts/`

- [ ] **Step 1: Copy all remaining scripts from vault/scripts/**

```bash
for f in bm25_index.py search_wiki.py build_graph.py build_maps.py build_keywords.py build_ingest_context.py lint_wiki.py snapshot_index.py relink.py qwen_ingest.py; do
    cp vault/scripts/"$f" llm-wiki-skill/scripts/"$f"
done
```

- [ ] **Step 2: Fix qwen_ingest.py — replace __file__-based wiki path discovery**

In `scan_existing_pages()` (function around line 240-264), replace:
```python
    script_dir = Path(__file__).resolve().parent
    wiki_dir = script_dir.parent / "wiki"
```
With:
```python
    wiki_dir = WIKI_DIR  # imported from wiki_utils
```

Also add `WIKI_DIR` to the import line at top. Change:
```python
from wiki_utils import parse_frontmatter
```
To:
```python
from wiki_utils import WIKI_DIR, parse_frontmatter
```

And update the `rel` path computation from:
```python
        rel = str(fp.relative_to(script_dir.parent))
```
To:
```python
        rel = str(fp.relative_to(VAULT_DIR))
```

Add `VAULT_DIR` to imports.

- [ ] **Step 3: Fix lint_wiki.py — reduce WIKI_SUBDIRS to 3**

The `WIKI_SUBDIRS` in wiki_utils already handles this, so lint_wiki just needs to import it. Verify the existing import already uses `from wiki_utils import ... WIKI_DIR ...` — it does (line 12). No change needed since wiki_utils already defines `WIKI_SUBDIRS = ["concepts", "entities", "syntheses"]`.

- [ ] **Step 4: Fix relink.py — reduce WIKI_SUBDIRS to 3**

Same as above — relink imports `WIKI_SUBDIRS` from wiki_utils. No change needed.

- [ ] **Step 5: Fix snapshot_index.py — remove qa-insight from TYPE_SECTIONS**

In `snapshot_index.py`, change `TYPE_SECTIONS` dict (around line 22-27). Replace:
```python
TYPE_SECTIONS = {
    "entity": "实体 (wiki/entities/)",
    "concept": "概念 (wiki/concepts/)",
    "synthesis": "综合分析 (wiki/syntheses/)",
    "qa-insight": "QA 洞见 (wiki/qa-insights/)",
}
```
With:
```python
TYPE_SECTIONS = {
    "entity": "实体 (wiki/entities/)",
    "concept": "概念 (wiki/concepts/)",
    "synthesis": "综合分析 (wiki/syntheses/)",
}
```

- [ ] **Step 6: Fix build_graph.py — remove --full mode**

Find and remove the `--full` argument handling in `main()` (around line 178-234). Keep only the core graph build logic:

Remove `--full` from argument parser:
```python
# Delete these lines:
    parser.add_argument(
        "--full",
        action="store_true",
        help="Also build statistics JSON and wiki HTML pages",
    )
```

Remove the entire `if args.full:` block at the end of `main()` (the subprocess calls to build_statistics.py and build_wiki_pages.py).

- [ ] **Step 7: Fix build_maps.py — add 20-page cold-start threshold**

In the `build()` function, add a guard before generating maps. After loading `topic_map`, add:

```python
    # Count total wiki pages — skip topic clustering if too few
    wiki_page_count = sum(1 for _ in WIKI_DIR.rglob("*.md"))
    if wiki_page_count < 20:
        msg = f"Insufficient pages for topic clustering ({wiki_page_count} < 20). Skipping."
        if as_json:
            print(json.dumps({"status": "skipped", "reason": "insufficient_pages",
                              "page_count": wiki_page_count, "threshold": 20}))
        else:
            print(f"SKIPPED: {msg}")
        return
```

- [ ] **Step 8: Fix build_ingest_context.py — layered schema/template override**

In `build_compact_schema()` (around line 47-72), change from reading from `SCHEMA_DIR` only to layered override:

Replace the function with:
```python
def read_layered(filename: str, user_dir: Path, skill_dir: Path) -> str | None:
    """Read file with user override priority: user_dir > skill_dir."""
    user_path = user_dir / filename
    if user_path.exists():
        return user_path.read_text(encoding="utf-8")
    skill_path = skill_dir / "schemas" / filename
    if skill_path.exists():
        return skill_path.read_text(encoding="utf-8")
    return None


def build_compact_schema() -> str:
    """Merge entity-types, relationship-types, quality-rules — layered override."""
    user_schema = VAULT_DIR / "_schema"
    skill_schema = SKILL_DIR / "schemas"

    parts = []
    for filename, label in [
        ("entity-types.md", "Entity Types"),
        ("relationship-types.md", "Relationship Types"),
        ("quality-rules.md", "Quality Rules"),
    ]:
        text = read_layered(filename, user_schema, skill_schema)
        if text:
            _, body = parse_frontmatter(text)
            parts.append(f"### {label}\n" + body.strip())

    return "\n\n".join(parts)
```

And in `build_template()`:
```python
def build_template() -> str:
    """Read wiki-page template — layered override."""
    user_tpl = VAULT_DIR / "templates" / "wiki-page.md"
    if user_tpl.exists():
        return user_tpl.read_text(encoding="utf-8")
    skill_tpl = SKILL_DIR / "templates" / "wiki-page.md"
    if skill_tpl.exists():
        return skill_tpl.read_text(encoding="utf-8")
    return ""
```

Add `SKILL_DIR` to imports at top:
```python
from wiki_utils import VAULT_DIR, WIKI_DIR, WIKI_SUBDIRS, SKILL_DIR, parse_frontmatter
```

Also update the module-level constants at top (lines 21-22). Replace:
```python
SCHEMA_DIR = VAULT_DIR / "_schema"
TEMPLATE_PATH = VAULT_DIR / "templates" / "wiki-page.md"
```
(These are now handled inside the functions — remove them.)

- [ ] **Step 9: Verify all scripts parse as valid Python**

```bash
cd llm-wiki-skill/scripts
for f in *.py; do
    echo -n "$f: "
    python3 -c "import ast; ast.parse(open('$f').read()); print('OK')"
done
```

---

### Task 5: Create ingest_loop.py (new script)

**Files:**
- Create: `llm-wiki-skill/scripts/ingest_loop.py`

- [ ] **Step 1: Write ingest_loop.py**

```python
#!/usr/bin/env python3
"""Batch ingest scanner with hash-based tracking and breakpoint resume.

Scans raw/ for files not yet ingested (by content hash), processes each
via the ingest command, and runs relink on completion.

Usage:
    python3 scripts/ingest_loop.py                # Claude engine (default)
    python3 scripts/ingest_loop.py --engine=qwen   # Qwen API engine
    python3 scripts/ingest_loop.py --reset         # Clear state and restart
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from wiki_utils import VAULT_DIR

STATE_FILE = VAULT_DIR / "raw" / ".ingest-state.json"
RAW_DIR = VAULT_DIR / "raw"

SUPPORTED_EXTS = {".md", ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".epub", ".csv", ".jsonl"}


def file_hash(path: Path) -> str:
    """SHA256 first 16 hex chars of file content."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def load_state() -> dict:
    """Load ingest state, return {} if absent or corrupt."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def scan_files() -> list[Path]:
    """Find all supported files under raw/ (excluding qa/ subfolder state)."""
    files = []
    for fp in sorted(RAW_DIR.rglob("*")):
        if fp.is_file() and fp.suffix.lower() in SUPPORTED_EXTS:
            # Skip state file and hidden files
            if fp.name.startswith("."):
                continue
            files.append(fp)
    return files


def main():
    engine = "claude"
    reset = False
    args = sys.argv[1:]
    for a in args:
        if a == "--engine=qwen":
            engine = "qwen"
        elif a == "--reset":
            reset = True

    if reset and STATE_FILE.exists():
        STATE_FILE.unlink()

    state = load_state()
    all_files = scan_files()

    # Discover new/changed files (hash-based)
    pending = []
    for fp in all_files:
        rel = str(fp.relative_to(VAULT_DIR))
        current_hash = file_hash(fp)
        entry = state.get(rel)
        if entry is None:
            pending.append(fp)
        elif entry.get("hash") != current_hash and entry.get("status") != "failed":
            pending.append(fp)
        # failed entries retry once; skip done entries with matching hash

    if not pending:
        print(json.dumps({"status": "up_to_date", "files_checked": len(all_files)}))
        return

    print(json.dumps({"status": "processing", "pending": len(pending), "total": len(all_files)},
                     ensure_ascii=False))

    processed = 0
    failed = 0
    for fp in pending:
        rel = str(fp.relative_to(VAULT_DIR))
        current_hash = file_hash(fp)
        existing = state.get(rel, {})

        # Skip if previously failed (already retried once)
        if existing.get("status") == "failed":
            print(f"  SKIP (previously failed): {rel}")
            continue

        print(f"  [{processed + 1}/{len(pending)}] Ingesting: {rel}")

        # Call ingest via Claude Code or Qwen
        if engine == "qwen":
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "qwen_ingest.py"),
                 "--raw", str(fp)],
                capture_output=True, text=True, cwd=str(VAULT_DIR),
                env={**__import__("os").environ, "PYTHONPATH": str(Path(__file__).parent)},
            )
        else:
            # Claude-driven ingest — user invokes /llm-wiki:ingest manually or via ralph-loop
            # For script-driven, we just track that the file needs processing
            print(f"  NOTE: Use /llm-wiki:ingest {rel} to process this file")
            state[rel] = {"hash": current_hash, "status": "pending", "engine": engine}
            processed += 1
            continue

        if result.returncode == 0:
            state[rel] = {"hash": current_hash, "status": "done", "engine": engine}
            processed += 1
        else:
            prev_status = existing.get("status")
            if prev_status == "retry":
                # Already retried once — mark failed
                state[rel] = {"hash": current_hash, "status": "failed", "engine": engine,
                              "error": result.stderr[:200]}
                failed += 1
                print(f"  FAILED (after retry): {rel}")
            else:
                # First failure — retry once
                print(f"  RETRY: {rel}")
                result2 = subprocess.run(
                    [sys.executable, str(Path(__file__).parent / "qwen_ingest.py"),
                     "--raw", str(fp)],
                    capture_output=True, text=True, cwd=str(VAULT_DIR),
                    env={**__import__("os").environ, "PYTHONPATH": str(Path(__file__).parent)},
                )
                if result2.returncode == 0:
                    state[rel] = {"hash": current_hash, "status": "done", "engine": engine}
                    processed += 1
                else:
                    state[rel] = {"hash": current_hash, "status": "failed", "engine": engine,
                                  "error": result2.stderr[:200]}
                    failed += 1
                    print(f"  FAILED: {rel}")

        save_state(state)

    # Clean stale entries (files that no longer exist)
    current_rels = {str(fp.relative_to(VAULT_DIR)) for fp in all_files}
    stale = [r for r in state if r not in current_rels]
    for r in stale:
        del state[r]
    if stale:
        save_state(state)

    # Auto-relink after batch ingest
    print("--- Running relink ---")
    subprocess.run(
        [sys.executable, str(Path(__file__).parent / "relink.py")],
        cwd=str(VAULT_DIR),
        env={**__import__("os").environ, "PYTHONPATH": str(Path(__file__).parent)},
    )

    print(json.dumps({"status": "complete", "processed": processed, "failed": failed,
                      "stale_cleaned": len(stale)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify syntax**

```bash
python3 -c "import ast; ast.parse(open('llm-wiki-skill/scripts/ingest_loop.py').read()); print('Syntax OK')"
```

---

### Task 6: Create hook scripts

**Files:**
- Create: `llm-wiki-skill/scripts/hooks/bm25.sh`
- Create: `llm-wiki-skill/scripts/hooks/graph.sh`

- [ ] **Step 1: Write bm25.sh**

```bash
#!/bin/bash
# PostToolUse hook: update BM25 index after wiki file write
# Reads tool_input.file_path from stdin JSON (Claude Code hooks protocol)
set -euo pipefail

FILE=$(cat | python3 -c 'import sys,json; print(json.load(sys.stdin)["tool_input"]["file_path"])' 2>/dev/null || echo "")

if [ -z "$FILE" ]; then
    exit 0
fi

# Resolve SKILL_DIR from this script's location
SKILL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# Discover wiki root from FILE path
WIKI_ROOT="$FILE"
while [ ! -f "$WIKI_ROOT/.wiki-root" ] && [ "$WIKI_ROOT" != "/" ] && [ "$WIKI_ROOT" != "." ]; do
    WIKI_ROOT="$(dirname "$WIKI_ROOT")"
done

if [ ! -f "$WIKI_ROOT/.wiki-root" ]; then
    exit 0
fi

cd "$WIKI_ROOT" && bash "$SKILL_DIR/scripts/wiki.sh" bm25_index update "$FILE"
```

- [ ] **Step 2: Write graph.sh**

```bash
#!/bin/bash
# PostToolUse hook: rebuild graph.json after wiki file write (30s debounce)
set -euo pipefail

FILE=$(cat | python3 -c 'import sys,json; print(json.load(sys.stdin)["tool_input"]["file_path"])' 2>/dev/null || echo "")

if [ -z "$FILE" ]; then
    exit 0
fi

SKILL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

WIKI_ROOT="$FILE"
while [ ! -f "$WIKI_ROOT/.wiki-root" ] && [ "$WIKI_ROOT" != "/" ] && [ "$WIKI_ROOT" != "." ]; do
    WIKI_ROOT="$(dirname "$WIKI_ROOT")"
done

if [ ! -f "$WIKI_ROOT/.wiki-root" ]; then
    exit 0
fi

GRAPH="$WIKI_ROOT/graph.json"
if [ -f "$GRAPH" ]; then
    AGE=$(( $(date +%s) - $(stat -f %m "$GRAPH" 2>/dev/null || stat -c %Y "$GRAPH" 2>/dev/null || echo 0) ))
    if [ "$AGE" -lt 30 ] 2>/dev/null; then
        exit 0
    fi
fi

cd "$WIKI_ROOT" && bash "$SKILL_DIR/scripts/wiki.sh" build_graph
```

- [ ] **Step 3: Make hooks executable**

```bash
chmod +x llm-wiki-skill/scripts/hooks/bm25.sh llm-wiki-skill/scripts/hooks/graph.sh
```

---

### Task 7: Copy and adapt schema files

**Files:**
- Copy: `vault/_schema/entity-types.md` → `llm-wiki-skill/schemas/entity-types.md`
- Copy: `vault/_schema/relationship-types.md` → `llm-wiki-skill/schemas/relationship-types.md`
- Copy: `vault/_schema/quality-rules.md` → `llm-wiki-skill/schemas/quality-rules.md`

- [ ] **Step 1: Copy schema files**

```bash
cp vault/_schema/entity-types.md llm-wiki-skill/schemas/
cp vault/_schema/relationship-types.md llm-wiki-skill/schemas/
cp vault/_schema/quality-rules.md llm-wiki-skill/schemas/
```

No modifications needed — entity types, relationship types, and quality rules are the same in the skill.

---

### Task 8: Copy and adapt template files

**Files:**
- Modify: `llm-wiki-skill/templates/wiki-page.md` (add decay_rate field)
- Modify: `llm-wiki-skill/templates/daily.md` (bilingual)
- Modify: `llm-wiki-skill/templates/reflection.md` (bilingual)
- Modify: `llm-wiki-skill/templates/judgment.md` (bilingual)
- Modify: `llm-wiki-skill/templates/weekly-review.md` (bilingual)

- [ ] **Step 1: Copy all templates**

```bash
cp vault/templates/wiki-page.md llm-wiki-skill/templates/
cp vault/templates/daily.md llm-wiki-skill/templates/
cp vault/templates/reflection.md llm-wiki-skill/templates/
cp vault/templates/judgment.md llm-wiki-skill/templates/
cp vault/templates/weekly-review.md llm-wiki-skill/templates/
```

- [ ] **Step 2: Update wiki-page.md frontmatter — add decay_rate field**

In `llm-wiki-skill/templates/wiki-page.md`, add `decay_rate` field after `confidence`:

```yaml
---
type:                    # entity | concept | synthesis (必填)
status: active           # draft | active | stale | archived (必填)
confidence:              # 0.0-1.0，基于来源数量估算 (必填)
decay_rate: medium       # slow | medium | fast (默认 medium)
created: {{date}}        # 创建日期 (必填)
updated: {{date}}        # 最后更新日期
last_accessed: {{date}}  # 最后被引用日期
source_count:            # 信息来源数量 (必填，≥1)
tags: []                 # 主题标签，如 [数值分析, 迭代法]
aliases: []              # 别名列表，含中英文变体
relates_to: []           # 关系列表
supersedes: null         # 如果此页面取代旧页面，填入旧页面名
---
```

- [ ] **Step 3: Bilingualize templates — add English annotations**

For each template (daily.md, reflection.md, judgment.md, weekly-review.md), add English translations as HTML comments beside each Chinese label. Example for daily.md:

```markdown
---
type: daily
date: {{date}}
---

# {{date}}

## 上午 <!-- Morning -->
<!-- Record morning work and thoughts -->

## 下午 <!-- Afternoon -->
<!-- Record afternoon work and thoughts -->

## 晚上 <!-- Evening -->
<!-- Record evening study and thoughts -->
```

(Apply similar pattern to reflection.md, judgment.md, weekly-review.md — Chinese labels with English HTML comments.)

---

### Task 9: Write SKILL.md entry point

**Files:**
- Write: `llm-wiki-skill/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: llm-wiki
description: AI-powered personal knowledge management system. Ingest source materials into structured wiki pages, query with unified search (BM25 + graph), maintain knowledge quality, and review/crystallize insights. Use when the user wants to build or manage a personal knowledge base.
---

# LLM Wiki

You are a knowledge base maintainer. Your role is to compile source materials into structured wiki pages, maintain connections and consistency between knowledge, manage page lifecycles, discover patterns, flag contradictions, and fill gaps.

## Architecture

```
<wiki-root>/
├── .wiki-root      # Marker file (empty)
├── raw/            # Immutable source materials (read-only)
│   └── qa/         # Chat exports for Q&A import
├── wiki/           # LLM-generated knowledge pages
│   ├── entities/   # People, companies, projects, tools
│   ├── concepts/   # Theories, methods, algorithms
│   └── syntheses/  # Cross-topic analyses, QA insights
├── journal/        # User-owned diary/reflections/judgments
├── maps/           # Auto-generated topic maps
├── _schema/        # User schema overrides (optional)
├── templates/      # User template overrides (optional)
├── index.md        # Auto-maintained directory
└── log.md          # Operation log
```

## Core Principles

1. **raw/ is read-only** — never modify source files
2. **wiki/ is LLM-owned** — all wiki pages created and maintained by you
3. **journal/ is user-owned** — personal thoughts written by user, you assist with linking and analysis
4. **Links over folders** — use [[wikilinks]] to organize relationships
5. **Bottom-up** — structure emerges naturally, no preset taxonomy
6. **Log everything** — all operations append to log.md

## Path Discovery

Scripts find the user's wiki root via:
1. `LLM_WIKI_ROOT` environment variable
2. Walking up from CWD to find `.wiki-root` marker
3. Error if not found — prompt user to run `/llm-wiki:init`

## Frontmatter Specification

All wiki/ pages must have:

```yaml
---
type: entity | concept | synthesis
status: draft | active | stale | archived
confidence: 0.0-1.0
decay_rate: slow | medium | fast
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_accessed: YYYY-MM-DD
source_count: N
tags: []
aliases: []
relates_to:
  - target: "[[PageName]]"
    type: uses | depends_on | contradicts | caused | extends | implements | supersedes | part_of | compares_to
    confidence: 0.0-1.0
---
```

## Wiki Page Lifecycle

```
draft ──(confidence >= 0.5)──→ active
active ──(confidence < 0.3)──→ stale
stale ──(30 days no update)──→ archived
```

Ebbinghaus decay rates:
- slow (180d half-life): architecture decisions, core concepts
- medium (60d half-life, default): general facts
- fast (14d half-life): temporary observations

## Schema / Template Override

Commands read from two layers (user overrides take priority):
1. `<wiki-root>/_schema/xxx.md`, `<wiki-root>/templates/xxx.md`
2. `<skill>/schemas/xxx.md`, `<skill>/templates/xxx.md` (defaults)

## Commands

| Command | File |
|---------|------|
| `/llm-wiki:init` | `commands/init.md` |
| `/llm-wiki:ingest` | `commands/ingest.md` |
| `/llm-wiki:ingest-loop` | `commands/ingest-loop.md` |
| `/llm-wiki:query` | `commands/query.md` |
| `/llm-wiki:journal` | `commands/journal.md` |
| `/llm-wiki:review` | `commands/review.md` |
| `/llm-wiki:maintain` | `commands/maintain.md` |

When a command is invoked, read the corresponding file in `commands/` for detailed steps.

## Scripts

All Python scripts are invoked through the wiki.sh wrapper:

```bash
bash <skill>/scripts/wiki.sh <script_name> [args...]
```

Available: bm25_index, search_wiki, build_graph, build_maps, build_keywords, build_ingest_context, lint_wiki, snapshot_index, relink, qwen_ingest, ingest_loop

## Hooks

PostToolUse hooks fire on every Write/Edit to `wiki/**/*.md`:
- BM25 index update (immediate)
- Graph rebuild (30s debounce)

## Dependencies

Install: `pip install -r <skill>/scripts/requirements.txt`
Required: jieba, rank_bm25, pyyaml, markitdown
Optional (Qwen engine): openai (requires DASHSCOPE_API_KEY)
```

---

### Task 10: Write command files

**Files:** Create 7 command files in `llm-wiki-skill/commands/`

- [ ] **Step 1: Write init.md**

```markdown
# /llm-wiki:init — Initialize a new knowledge base

Initialize the current directory as an llm-wiki knowledge base.

## Detection

1. Check current directory
   - No `.obsidian/` → full initialization (copy all init-kit contents)
   - Has `.obsidian/` → Obsidian injection mode (merge directories, don't overwrite existing files)

## Steps

1. Copy directory structure from `<skill>/resources/init-kit/` to current directory:
   - `.wiki-root` (marker file)
   - `raw/`, `raw/qa/`
   - `wiki/entities/`, `wiki/concepts/`, `wiki/syntheses/`
   - `journal/daily/`, `journal/reflections/`, `journal/judgments/`, `journal/growth/`
   - `maps/`
   - `index.md` (initial skeleton), `log.md` (empty)
   - `_schema/` (empty, for user overrides)
   - `templates/` (empty, for user overrides)

2. Write `.wiki-root` marker file (empty file)

3. Run `pip install -r <skill>/scripts/requirements.txt`

4. Write `.claude/settings.local.json` with PostToolUse hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash <absolute-path-to-skill>/scripts/hooks/bm25.sh"
          },
          {
            "type": "command",
            "command": "bash <absolute-path-to-skill>/scripts/hooks/graph.sh"
          }
        ]
      }
    ]
  }
}
```

Replace `<absolute-path-to-skill>` with the actual skill installation path.

5. Output completion message:

```
LLM Wiki initialized in <directory>.

Next steps:
1. Put source materials in raw/ (markdown, PDF, DOCX, etc.)
2. Run /llm-wiki:ingest <file> to extract knowledge
3. Run /llm-wiki:query <question> to search your knowledge base
```
```

- [ ] **Step 2: Write ingest.md**

```markdown
# /llm-wiki:ingest — Extract knowledge from source materials

Read a source file from raw/ and compile it into structured wiki pages.

## Usage

```
/llm-wiki:ingest <path>          # Process a specific file (relative to raw/)
/llm-wiki:ingest all              # Process all unprocessed files
/llm-wiki:ingest !insight <text>  # Direct insight entry
```

## Format Auto-Routing

1. **!insight mode**: Direct text → create/update wiki page immediately
2. **Non-markdown** (.pdf/.docx/.pptx/.xlsx/.html/.epub/.csv):
   a. Run `bash <skill>/scripts/wiki.sh qwen_ingest --raw <file>` or use markitdown
   b. Convert to .md first
   c. Then process as markdown
3. **Markdown in raw/qa/**: Q&A clustering mode
   - Parse Q&A pairs from JSONL/markdown
   - Cluster by topic
   - Extract cross-conversation insights
   - Output to `wiki/syntheses/`
4. **Markdown in raw/ (other)**: Entity/concept extraction
   - Identify entities (people, companies, projects, tools) and concepts (theories, methods, algorithms)
   - Create pages in `wiki/entities/` and `wiki/concepts/`
   - Establish relationships via `relates_to`
   - Update `index.md` and `log.md`

## Quality Requirements

Each new page must have:
- Complete frontmatter (all required fields)
- Overview 50-200 chars
- At least 1 source citation
- At least 1 relates_to relationship
- At least 3 [[wikilinks]] in body
```

- [ ] **Step 3: Write ingest-loop.md**

```markdown
# /llm-wiki:ingest-loop — Batch ingest all files in raw/

Scan raw/ for unprocessed files and process them in sequence.

## Usage

```
/llm-wiki:ingest-loop                # Default (Claude engine, interactive)
/llm-wiki:ingest-loop --engine=qwen  # Qwen API engine (non-interactive)
/llm-wiki:ingest-loop --reset        # Clear state and restart
```

## Steps

1. Run `bash <skill>/scripts/wiki.sh ingest_loop [--engine=qwen] [--reset]`
2. The script:
   - Scans `raw/` for supported files (.md/.pdf/.docx/.pptx/.xlsx/.html/.epub/.csv/.jsonl)
   - Computes SHA256 hash (first 16 chars) for each file
   - Compares against `raw/.ingest-state.json` to find new/changed files
   - Processes each file via ingest (Claude engine) or qwen_ingest.py (Qwen engine)
   - Retries once on failure, then marks as failed
   - Auto-completes: skips deleted files, cleans stale state entries
3. After all files processed: runs `relink.py` automatically to add [[wikilinks]]
4. Output: JSON summary with processed/failed/skipped counts

## State File

`raw/.ingest-state.json` tracks each file:
```json
{
  "raw/articles/example.md": {
    "hash": "abc123def4567890",
    "status": "done",
    "engine": "claude"
  }
}
```

Status values: `done`, `pending`, `failed`, `retry`
```

- [ ] **Step 4: Write query.md**

```markdown
# /llm-wiki:query — Search and answer questions

Answer questions using the knowledge base with unified search.

## Usage

```
/llm-wiki:query <question>
```

## Steps

1. **Query rewrite**: Optimize the user's question into search keywords
2. **Unified search**: Run `bash <skill>/scripts/wiki.sh search_wiki "<keywords>" --top 15 --json`
   - BM25 full-text search (jieba-tokenized)
   - Maps topic expansion (best-match topic → all pages in that topic)
   - Graph 1-hop BFS traversal (seed from BM25 top-5)
   - RRF (Reciprocal Rank Fusion, k=60) to merge results
3. **Read relevant pages**: Read full content of top-N results; note low-confidence pages
4. **Synthesize answer**: Answer in the user's language, cite sources as `来源：[[PageName]]`
5. **Crystallize if valuable**: If answer synthesizes 3+ pages and forms new insight, auto-create `wiki/syntheses/` page
6. **Update last_accessed**: Update `last_accessed` on all cited pages
```

- [ ] **Step 5: Write journal.md**

```markdown
# /llm-wiki:journal — Create journal entries

Create daily notes, reflections, or judgments with automatic wiki linking.

## Usage

```
/llm-wiki:journal daily                    # Today's daily note
/llm-wiki:journal reflection <topic>       # Deep reflection on a topic
/llm-wiki:journal judgment <topic>         # Record a decision/judgment
```

## Steps

### daily
1. Check if `journal/daily/YYYY-MM-DD.md` exists; if so, read it
2. If not, create from `<skill>/templates/daily.md` (or user override in `templates/daily.md`)
3. Search wiki for recently ingested topics → suggest links in "Related" section

### reflection
1. Create `journal/reflections/<topic>.md` from template
2. Search wiki for related pages → populate "Related" section with [[links]]

### judgment
1. Create `journal/judgments/<topic>.md` from template
2. Search wiki for related pages → populate "Related Knowledge" section

## !insight Support

When writing journal content, the user can mark paragraphs with `!insight`:

```
今天意识到：条件数描述了问题本身的属性，而算法稳定性
描述了求解过程的属性。两者正交。 !insight
```

This marks the content for automatic wiki page creation during the next `/llm-wiki:review`.
```

- [ ] **Step 6: Write review.md**

```markdown
# /llm-wiki:review — Periodic review, crystallization, and memory consolidation

Review knowledge base health and patterns, crystallize insights, manage page decay.

## Usage

```
/llm-wiki:review              # Weekly review (default)
/llm-wiki:review monthly      # Monthly review
/llm-wiki:review quarterly    # Quarterly review
```

## Steps

### 0. System Health Check
- Read `log.md` for last `maintain` timestamp → if > 7 days, remind user
- Compare current wiki page count vs last snapshot → if > 20 pages difference, suggest maintain

### 1. Gather Materials
- Scan past 7/30/90 days of journal entries (daily notes, reflections, judgments)

### 2. Pattern Discovery
- Identify concepts mentioned 3+ days
- Discover new cross-domain connections
- Flag topics with growing mention frequency

### 3. Crystallization
- If session connected 3+ concepts forming a new insight → create `wiki/syntheses/` page
- Update `index.md` and `log.md`

### 4. Journal → Wiki Link Scan
- Scan recent journal entries for [[wiki page links]]
- If a page is referenced 3+ days AND confidence < 0.5 → suggest promoting confidence or adding content

### 5. !insight Processing
- Scan journal entries for `!insight` markers
- For each unprocessed !insight: create or update a wiki page
- Content is extracted from the marked paragraph

### 6. Memory Decay (Ebbinghaus)
- Scan all wiki pages with `status: active`
- Apply decay formula: `new_confidence = confidence * 0.5^(days/half_life)`
  - slow (180d half-life): architecture decisions, core concepts
  - medium (60d half-life): general facts
  - fast (14d half-life): temporary observations
- Pages with confidence < 0.3 → mark `status: stale`
- stale pages with 30+ days no update → mark `status: archived`

### 7. Adaptive Automation
- Analyze operation frequency from log.md
- If same operation at similar time for 3+ consecutive days → propose cron task
- If X days since last maintain → remind user
- User confirms → write cron config to `.claude/settings.local.json`

## Output Format

```
Review Complete (YYYY-MM-DD)

Health:
  Last maintain: N days ago — OK / Reminder
  Pages: N (Δ+N since last snapshot)

Patterns:
  - [[Topic]] mentioned 5 times this week

Crystallized:
  - Created wiki/syntheses/New Insight.md

!insight Processed:
  - Created wiki/concepts/Condition Number vs Stability.md

Decay Applied:
  - N pages decayed, M marked stale, K archived

Automation Proposed:
  - Daily journal at 22:57? Confirm to set cron.
```
```

- [ ] **Step 7: Write maintain.md**

```markdown
# /llm-wiki:maintain — Full knowledge base health check and repair

Run the complete maintenance pipeline: check → lint → reindex → build.

## Usage

```
/llm-wiki:maintain
```

## Steps

### 1. Check — Read-only diagnostics
Run: `bash <skill>/scripts/wiki.sh lint_wiki --json`

9 checks performed:
- F1: Missing required frontmatter fields (error)
- F2: Unparseable YAML frontmatter (error)
- F3: Overview > 200 chars (warning)
- F4: Empty sections (warning)
- B1: Broken [[links]] (warning)
- B2: Page not in BM25 docmap (warning)
- I1: Page not in index.md (warning)
- I2: Stale index entries (warning)
- O1: Orphan pages — no inbound links (warning)

Exit code 2 if errors exist. Record findings.

### 2. Lint — Auto-repair
For each fixable issue from Step 1:
- Missing frontmatter fields → fill defaults (confidence based on source_count)
- Broken [[links]] → correct if similar page exists, otherwise flag
- Page not in index.md → auto-add
- Orphan pages → try to find related pages and add links

Run: `bash <skill>/scripts/wiki.sh snapshot_index --slim`

### 3. Reindex
Run: `bash <skill>/scripts/wiki.sh snapshot_index --slim`
Run: `bash <skill>/scripts/wiki.sh build_maps --json`

Cold-start guard: if wiki pages < 20, skip topic clustering and maps generation.

### 4. Build
Run: `bash <skill>/scripts/wiki.sh build_keywords`
Run: `bash <skill>/scripts/wiki.sh build_graph`

(These are also maintained by hooks — this is a full rebuild for insurance.)

## Output

```
Maintenance Complete

[1/4] Check — 0 errors, 3 warnings
[2/4] Lint — 2 fixed, 1 pending
[3/4] Reindex — OK (N pages, M topics) | SKIPPED (< 20 pages)
[4/4] Build — keywords (N entries), graph (N nodes, M edges)
```

## Post-Maintenance

Append to log.md:
```
## [YYYY-MM-DD] maintain
- Check: N errors, M warnings
- Lint: K fixed
- Reindex: OK / SKIPPED
- Build: OK
```
```

---

### Task 11: Integration verification

**Verify:** All skill files present and valid

- [ ] **Step 1: Verify file count and structure**

```bash
echo "=== Skill Structure ==="
find llm-wiki-skill -type f | sort

echo ""
echo "=== Expected file count ==="
echo "SKILL.md: 1"
echo "commands/: 7"
echo "scripts/*.py: 13 (11 retained + 1 new + wiki_utils)"
echo "scripts/*.sh: 3 (wiki.sh + 2 hooks)"
echo "schemas/: 3"
echo "templates/: 5"
echo "resources/init-kit/: directories + 2 files"
```

- [ ] **Step 2: Verify all Python scripts parse**

```bash
cd llm-wiki-skill
for f in scripts/*.py; do
    echo -n "$(basename $f): "
    python3 -c "import ast; ast.parse(open('$f').read()); print('OK')"
done
```

Expected: All files print "OK"

- [ ] **Step 3: Verify shell scripts are executable**

```bash
ls -la llm-wiki-skill/scripts/*.sh llm-wiki-skill/scripts/hooks/*.sh
```

All `.sh` files should have `x` permission.

- [ ] **Step 4: Test wiki.sh discovery with a temp wiki root**

```bash
# Create temp test directory
TEST_DIR=$(mktemp -d)
cp llm-wiki-skill/resources/init-kit/.wiki-root "$TEST_DIR/"

# Test wiki.sh discovery
cd "$TEST_DIR" && bash "$(pwd -P)/../llm-wiki-skill/scripts/wiki.sh" 2>&1 | head -3

# Cleanup
rm -rf "$TEST_DIR"
```

Expected: Usage output (list of available scripts).

- [ ] **Step 5: Test that wiki_utils paths resolve correctly**

```bash
TEST_DIR=$(mktemp -d)
cp llm-wiki-skill/resources/init-kit/.wiki-root "$TEST_DIR/"
cd "$TEST_DIR" && PYTHONPATH="$(pwd -P)/../llm-wiki-skill/scripts" python3 -c "
from wiki_utils import VAULT_DIR, WIKI_DIR, WIKI_SUBDIRS
print(f'VAULT_DIR: {VAULT_DIR}')
print(f'WIKI_DIR: {WIKI_DIR}')
print(f'WIKI_SUBDIRS: {WIKI_SUBDIRS}')
assert WIKI_SUBDIRS == ['concepts', 'entities', 'syntheses'], f'Expected 3 subdirs, got {WIKI_SUBDIRS}'
print('All checks passed')
"
rm -rf "$TEST_DIR"
```

Expected: All checks passed, WIKI_SUBDIRS has 3 entries.

---

### Task 12: Final commit

- [ ] **Step 1: Review all changes**

```bash
git status
git diff --stat
```

- [ ] **Step 2: Commit**

```bash
git add llm-wiki-skill/ docs/superpowers/specs/2026-06-08-llm-wiki-skill-design.md docs/superpowers/plans/2026-06-08-llm-wiki-skill.md
git commit -m "feat: extract llm-wiki skill from vault system

- 12 Python scripts adapted (path discovery, 3 wiki subdirs, no --full)
- 2 hook scripts (BM25 + graph with 30s debounce)
- 5 commands + init (ingest, ingest-loop, query, journal, review, maintain)
- Schema + templates with layered override (user > skill defaults)
- ingest_loop.py: hash-based tracking, breakpoint resume, auto-relink
- No _memory/ directory (lifecycle embedded in wiki page frontmatter)
- No static site generation

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```
```

---

## Self-Review Checklist

1. **Spec coverage**: All spec sections have corresponding tasks.
   - §3 Skill structure → Task 1 (skeleton)
   - §4 Path discovery → Task 2 (wiki_utils), Task 3 (wiki.sh)
   - §5 Commands → Task 10 (command files)
   - §6 Init → Task 10 Step 1 (init.md)
   - §7 Scripts → Tasks 2-6 (all script changes)
   - §8 Page lifecycle → Task 9 (SKILL.md), Task 10 (review.md)
   - §9 Journal → Task 10 Step 5 (journal.md)
   - §10 Naming → Tasks 4, 8
   - §11 Template/schema override → Tasks 2, 8
   - §12 Feedback loops → Task 10 Step 6 (review.md)

2. **Placeholder scan**: No TBD/TODO. All code steps have concrete content. All commands have complete step-by-step instructions.

3. **Type consistency**:
   - `WIKI_SUBDIRS = ["concepts", "entities", "syntheses"]` — consistent across wiki_utils.py, lint_wiki.py, relink.py
   - `SKILL_DIR` — defined in wiki_utils.py, used in build_ingest_context.py
   - `discover_wiki_root()` — defined in wiki_utils.py, called at module level
   - `decay_rate` field — added to wiki-page.md template, referenced in SKILL.md and review.md
