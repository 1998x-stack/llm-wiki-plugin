# Wiki System V2 — Comprehensive Design Spec

**Date:** 2026-04-15
**Scope:** Scripts, commands, hooks, templates, documentation, CI/CD, visualization
**Phases:** 6 sequential phases

---

## Overview

Upgrade the LLM Wiki plugin from a basic ingest/query/lint system to a production-grade knowledge management platform with:

- BM25 full-text search (jieba tokenization)
- Qwen API-powered batch ingestion
- Ralph-loop powered batch processing
- Knowledge graph visualization (D3.js)
- Automated hooks for index maintenance
- GitHub Actions CI/CD with lint gates
- Professional documentation suite

---

## Phase 1: Python Scripts Foundation (`vault/scripts/`)

All scripts live in `vault/scripts/` alongside existing shell scripts. Python 3.10+.

### 1.1 `bm25_index.py` — BM25 Index Manager

**Purpose:** Build, update, and query a BM25 index over all wiki/ pages.

**CLI interface:**
```
python3 scripts/bm25_index.py build                    # Full rebuild
python3 scripts/bm25_index.py update <wiki_file.md>    # Incremental single-file update
python3 scripts/bm25_index.py query "搜索词" -n 10     # Search, return JSON array
python3 scripts/bm25_index.py remove <wiki_file.md>    # Remove file from index
```

**Storage:** `vault/index/BM25/`
```
vault/index/BM25/
├── corpus.pkl      # List of tokenized documents [{id, tokens, path}]
├── index.pkl       # BM25Okapi index object from rank_bm25
└── docmap.json     # {doc_id: {path, title, type, updated}} mapping
```

**Dependencies:** `jieba`, `rank_bm25`, stdlib (`json`, `pickle`, `pathlib`, `argparse`, `sys`)

**Tokenization strategy:**
- Strip YAML frontmatter before tokenizing
- Use `jieba.cut_for_search` for fine-grained Chinese segmentation
- Preserve English tokens as-is (lowercased)
- Remove stop words (Chinese + English common words)

**Query output format (stdout JSON):**
```json
[
  {"path": "wiki/concepts/牛顿法.md", "score": 12.34, "title": "牛顿法"},
  {"path": "wiki/entities/牛顿.md", "score": 8.76, "title": "艾萨克·牛顿"}
]
```

**Incremental update logic:**
1. Load existing corpus.pkl and docmap.json
2. If file exists in docmap → remove old entry
3. Tokenize new file content
4. Append to corpus
5. Rebuild BM25 index (rank_bm25 requires full rebuild from corpus)
6. Save all three files

### 1.2 `qwen_ingest.py` — Qwen-Powered Ingest Tool

**Purpose:** Use Qwen 3.6-plus API to extract structured wiki content from raw source files.

**CLI interface:**
```
python3 scripts/qwen_ingest.py --raw <raw_file_path> --wiki <wiki_file_path>
```

**Output (stdout JSON):**
```json
{"status": "SUCCESS", "path": "wiki/concepts/example.md"}
{"status": "ERROR", "message": "API call failed: 429 rate limit"}
{"status": "LINT_WARNING", "path": "wiki/concepts/example.md", "issues": ["missing aliases field", "overview exceeds 200 chars"]}
```

**Environment:**
- `$DASHSCOPE_API_KEY` — required
- Endpoint: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- Model: `qwen3-plus`

**API call configuration:**
```python
client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen3-plus",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": raw_content}
    ],
    extra_body={"enable_thinking": False}
)
```

**System prompt (embedded in script):**

The system prompt instructs Qwen to:
1. Read the raw source material
2. Extract entities (people, organizations, tools, papers) and concepts (theories, methods, algorithms)
3. Output valid markdown with YAML frontmatter matching the wiki-page template:
   ```yaml
   ---
   type: entity | concept
   title: "页面标题"
   aliases: ["别名1", "别名2"]
   tags: [tag1, tag2]
   confidence: 0.8
   source_count: 1
   created: YYYY-MM-DD
   last_confirmed: YYYY-MM-DD
   status: active
   relates_to:
     - target: "[[相关页面]]"
       type: extends | implements | contradicts | ...
   ---
   ```
4. Write 概述 (50-200 chars), 关键内容 (300+ chars), 来源, 相关 sections
5. Use Chinese as primary language, preserve English proper nouns
6. Use [[双链]] for cross-references

**Inline lint checks (post-API-call):**
- Frontmatter has all required fields (type, title, confidence, created, status)
- `概述` section exists and is 50-200 characters
- At least one `[[link]]` in body
- No empty sections
- Valid YAML frontmatter (parseable)

If lint issues found but content is usable → write file + return LINT_WARNING.
If content is unparseable or missing critical sections → return ERROR without writing.

**Dependencies:** `openai` (for OpenAI-compatible client), `pyyaml`, `re`, `argparse`

### 1.3 `build_graph.py` — Knowledge Graph JSON Builder

**Purpose:** Scan all wiki/ pages and build a graph.json for visualization.

**CLI interface:**
```
python3 scripts/build_graph.py [--output vault/graph.json]
```

**Output:** `vault/graph.json`
```json
{
  "metadata": {
    "generated": "2026-04-15T12:00:00",
    "total_nodes": 96,
    "total_edges": 234,
    "orphan_count": 3
  },
  "nodes": [
    {
      "id": "wiki/concepts/牛顿法.md",
      "label": "牛顿法",
      "type": "concept",
      "confidence": 0.9,
      "tags": ["数值分析", "迭代法"],
      "edge_count": 8
    }
  ],
  "edges": [
    {
      "source": "wiki/concepts/牛顿法.md",
      "target": "wiki/entities/牛顿.md",
      "relation": "named_after",
      "bidirectional": true
    }
  ],
  "orphans": ["wiki/concepts/some_orphan.md"],
  "components": [
    {"id": 0, "size": 90, "nodes": ["..."]},
    {"id": 1, "size": 3, "nodes": ["..."]}
  ]
}
```

**Graph construction logic:**
1. Glob all `wiki/**/*.md` files
2. For each file:
   - Parse YAML frontmatter → extract type, title, confidence, tags, relates_to
   - Scan body for `[[wikilink]]` patterns → add implicit edges
3. Deduplicate edges (frontmatter relates_to + body wikilinks)
4. Compute connected components (BFS/DFS)
5. Flag orphan nodes (degree == 0)
6. Write graph.json

**Dependencies:** `pyyaml`, `re`, `json`, `pathlib`, `collections`

### 1.4 `lint_wiki.py` — Standalone Lint Script

**Purpose:** Automated quality checks for CI/CD and hook usage.

**CLI interface:**
```
python3 scripts/lint_wiki.py                        # Full scan, report only
python3 scripts/lint_wiki.py --fix                  # Full scan + auto-fix
python3 scripts/lint_wiki.py --file <path>          # Single file check
python3 scripts/lint_wiki.py --json                 # Output JSON report
```

**Checks:**
| ID | Check | Severity | Auto-fixable |
|----|-------|----------|-------------|
| F1 | Missing required frontmatter fields | ERROR | Yes (defaults) |
| F2 | Invalid YAML frontmatter | ERROR | No |
| F3 | Overview > 200 chars | WARNING | No |
| F4 | Empty sections | WARNING | No |
| O1 | Orphan pages (no incoming links) | WARNING | No |
| B1 | Broken [[links]] to non-existent pages | ERROR | Yes (fuzzy match) |
| B2 | BM25 index missing entry | WARNING | Yes (rebuild) |
| I1 | Page not in index.md | ERROR | Yes (add entry) |
| I2 | Stale index entry (page deleted) | WARNING | Yes (remove) |

**Output (JSON mode):**
```json
{
  "total_files": 96,
  "errors": 2,
  "warnings": 5,
  "checks": [
    {"file": "wiki/concepts/foo.md", "check": "F1", "severity": "ERROR", "message": "missing 'confidence' field", "fixed": true}
  ]
}
```

**Exit codes:** 0 = clean, 1 = warnings only, 2 = errors found

**Dependencies:** `pyyaml`, `re`, `json`, `pathlib`, `argparse`

---

## Phase 2: Commands Overhaul (`.claude/commands/wiki/`)

### 2.1 `ingest.md` — Polish Existing

Changes from current version:
- Add explicit "file not found" and "unsupported format" error handling at step 1
- After each page create/update, add step: `Bash: python3 scripts/bm25_index.py update <wiki_file>`
- Tighten quality requirements language: replace "应该" with "必须"
- Add step 8: verify created pages pass `python3 scripts/lint_wiki.py --file <path>`
- No structural changes to the ingest logic itself

### 2.2 `ingest-loop.md` — Ralph-Loop Batch Ingest (NEW)

**Input:** `$ARGUMENTS` — folder path or file path relative to `vault/raw/`

**Mechanism:** Ralph-loop stop hook pattern.

**Setup phase (first run):**
1. If `$ARGUMENTS` is a single file → skip loop, execute wiki:ingest directly, done
2. If `$ARGUMENTS` is a folder:
   a. Discover all processable files (`.md`, `.pdf`, `.docx`, `.jsonl`)
   b. Check `log.md` to filter out already-processed files
   c. Create state file `.claude/ingest-loop.local.md`:
      ```yaml
      ---
      source_path: "raw/books/数值分析"
      files:
        - "raw/books/数值分析/01_newton.md"
        - "raw/books/数值分析/02_euler.md"
      current_index: 0
      total: 15
      completed: []
      failed: []
      started_at: "2026-04-15T12:00:00"
      completion_promise: "ALL_FILES_INGESTED"
      ---
      ```
   d. Run `bash scripts/setup-ingest-loop.sh "$ARGUMENTS"` to configure stop hook

**Each iteration:**
1. Read `.claude/ingest-loop.local.md` state file
2. Get file at `files[current_index]`
3. Execute full ingest workflow for that file (same logic as wiki:ingest)
4. Update state file: increment `current_index`, add to `completed[]` or `failed[]`
5. Report: `[current_index/total] ✓ Ingested: filename` or `✗ Failed: filename — reason`
6. If `current_index >= total`:
   - Run `wiki:lint` on all newly created pages
   - Output `<promise>ALL_FILES_INGESTED</promise>`
   - Clean up: remove state file and hook
7. If `current_index < total`: session ends normally, stop hook re-feeds prompt

**Setup script:** `scripts/setup-ingest-loop.sh`
```bash
#!/bin/bash
# Parses folder path, discovers files, creates state file
# Configures stop hook in settings.local.json
# Usage: bash scripts/setup-ingest-loop.sh "raw/books/数值分析"
```

**Stop hook behavior:**
- On Claude exit attempt: check if `.claude/ingest-loop.local.md` exists
- If exists and `current_index < total`: block exit, re-feed `/wiki:ingest-loop $ARGUMENTS`
- If complete or file missing: allow exit

### 2.3 `ingest-loop-qwen.md` — Ralph-Loop + Qwen Batch Ingest (NEW)

**Input:** `$ARGUMENTS` — folder path or file path relative to `vault/raw/`

**Same ralph-loop mechanism as ingest-loop, with differences:**

- State file: `.claude/ingest-loop-qwen.local.md`
- Setup script: `scripts/setup-ingest-loop-qwen.sh`
- Completion promise: `"ALL_FILES_INGESTED_QWEN"`

**Each iteration:**
1. Read state file
2. Get file at `files[current_index]`
3. Determine target wiki path:
   - Analyze filename/content to classify as entity or concept
   - Target: `wiki/entities/<name>.md` or `wiki/concepts/<name>.md`
4. Call: `python3 scripts/qwen_ingest.py --raw <raw_path> --wiki <target_path>`
5. Parse JSON result:
   - `SUCCESS` → update state, report success
   - `ERROR` → add to failed[], log error, continue
   - `LINT_WARNING` → add to completed[] with warnings, continue
6. Run BM25 update: `python3 scripts/bm25_index.py update <target_path>`
7. Update state file
8. Same completion/continuation logic as ingest-loop

### 2.4 `query.md` — Enhanced with BM25 + QA Write

**Input:** `$ARGUMENTS` — question string

**Enhanced flow:**
1. **BM25 search:** `python3 scripts/bm25_index.py query "$ARGUMENTS" -n 10`
2. **Parse results:** combine BM25 hits with existing `index.md` keyword search and `relates_to` graph traversal
3. **Read pages:** read full content of top relevant pages (union of all search methods), note confidence levels
4. **Answer:** compose answer in Chinese with inline citations `来源：[[page name]]`
5. **Synthesis check:** if answer synthesizes 3+ pages into a new insight, create page in `wiki/syntheses/`
6. **Write QA file:** append to `vault/qa/YYYY-MM-DD.md` in ChatGPT export format:
   ```markdown
   ---

   ## Prompt

   <original question>

   ## Response

   <full answer with citations>

   ---
   ```
   If file doesn't exist, create with header:
   ```markdown
   ---
   type: qa-log
   date: YYYY-MM-DD
   ---

   # QA Log — YYYY-MM-DD
   ```
7. **Auto-import:** call `wiki:qa-import` on the QA file to extract any insights
8. **Update access:** set `last_accessed: today` on all referenced wiki pages

### 2.5 `graph.md` — Knowledge Graph Builder (NEW)

**Input:** none

**Flow:**
1. Run `wiki:lint` with focus on:
   - **B. Orphan page check** — pages with no incoming links
   - **C. Broken link check** — `[[links]]` to non-existent pages
2. Auto-fix fixable lint issues (broken links with fuzzy matches, missing index entries)
3. Call: `python3 scripts/build_graph.py`
4. Read generated `vault/graph.json` and report stats:
   - Total nodes, total edges
   - Orphan count and list
   - Connected component count and sizes
   - Top-10 most connected nodes
5. Append to `log.md`:
   ```
   ## [YYYY-MM-DD HH:MM] graph
   - 构建知识图谱: N 节点, M 边, K 孤页, C 连通分量
   ```

### 2.6 `lint.md` — Enhanced

**Additions to existing checks:**

| New Check | Description |
|-----------|-------------|
| **G. BM25 index consistency** | Read `vault/index/BM25/docmap.json`, compare with actual wiki/ files. Flag missing entries. Auto-fix: run `bm25_index.py update` for missing files. |
| **H. Graph connectivity** | Run `build_graph.py`, check for isolated subgraphs with < 3 nodes. Report as WARNING. |
| **I. Template compliance** | Check that pages match their template structure (required sections present). |

**Enhanced reporting:**
- Severity levels: ERROR (must fix), WARNING (should fix), INFO (optional)
- Summary counts at end
- Call `python3 scripts/lint_wiki.py --json` for scripted checks first
- Then perform Claude-specific semantic checks:
  - Contradiction reasoning (do `contradicts` relations have resolution?)
  - Confidence appropriateness (is confidence score reasonable given source_count?)
  - Tag consistency (similar pages should have similar tags)

---

## Phase 3: Hooks & Automation

### 3.1 Hook Architecture

Three hooks triggered on Write/Edit to `wiki/**/*.md` files:

| Hook | Script | Purpose |
|------|--------|---------|
| Lint | `scripts/hook_lint.sh` | Validate modified wiki page |
| BM25 | `scripts/hook_bm25.sh` | Update BM25 index for modified page |
| Graph | `scripts/hook_graph.sh` | Rebuild graph.json |

### 3.2 `scripts/hook_lint.sh`

```bash
#!/bin/bash
# Called by PostToolUse hook after Write/Edit on wiki/ files
# Args: $1 = file path that was modified
FILE_PATH="$1"
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Only process wiki/ files
if [[ "$FILE_PATH" != *"wiki/"* ]]; then
    exit 0
fi

RESULT=$(cd "$VAULT_DIR" && python3 scripts/lint_wiki.py --file "$FILE_PATH" --json 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] LINT $FILE_PATH — OK" >> "$LOG"
elif [ $STATUS -eq 1 ]; then
    echo "[$TIMESTAMP] LINT $FILE_PATH — WARN: $(echo $RESULT | python3 -c 'import sys,json; r=json.load(sys.stdin); print(", ".join(c["message"] for c in r.get("checks",[])))' 2>/dev/null)" >> "$LOG"
else
    echo "[$TIMESTAMP] LINT $FILE_PATH — ERROR: $(echo $RESULT | head -c 200)" >> "$LOG"
fi
```

### 3.3 `scripts/hook_bm25.sh`

```bash
#!/bin/bash
# Called by PostToolUse hook after Write/Edit on wiki/ files
# Args: $1 = file path that was modified
FILE_PATH="$1"
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

if [[ "$FILE_PATH" != *"wiki/"* ]]; then
    exit 0
fi

RESULT=$(cd "$VAULT_DIR" && python3 scripts/bm25_index.py update "$FILE_PATH" 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] BM25 $FILE_PATH — indexed" >> "$LOG"
else
    echo "[$TIMESTAMP] BM25 $FILE_PATH — error: $(echo $RESULT | head -c 200)" >> "$LOG"
fi
```

### 3.4 `scripts/hook_graph.sh`

```bash
#!/bin/bash
# Called by PostToolUse hook after Write/Edit on wiki/ files
# Rebuilds graph.json after any wiki change
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
FILE_PATH="$1"

if [[ "$FILE_PATH" != *"wiki/"* ]]; then
    exit 0
fi

RESULT=$(cd "$VAULT_DIR" && python3 scripts/build_graph.py 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] GRAPH rebuild — OK" >> "$LOG"
else
    echo "[$TIMESTAMP] GRAPH rebuild — error: $(echo $RESULT | head -c 200)" >> "$LOG"
fi
```

### 3.5 Hook Registration (`vault/.claude/settings.local.json`)

```json
{
  "permissions": {
    "allow": ["Read(*)", "Write(*)", "Grep(*)", "Update(*)", "Bash(*)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Tool matches Write or Edit",
        "command": "bash vault/scripts/hook_lint.sh \"$CLAUDE_TOOL_ARG_file_path\"",
        "description": "Lint wiki pages after modification"
      },
      {
        "matcher": "Tool matches Write or Edit",
        "command": "bash vault/scripts/hook_bm25.sh \"$CLAUDE_TOOL_ARG_file_path\"",
        "description": "Update BM25 index after wiki modification"
      },
      {
        "matcher": "Tool matches Write or Edit",
        "command": "bash vault/scripts/hook_graph.sh \"$CLAUDE_TOOL_ARG_file_path\"",
        "description": "Rebuild graph after wiki modification"
      }
    ]
  }
}
```

### 3.6 `vault/log.hook.md`

Created by hook scripts. Append-only format:
```markdown
# Hook Log

[2026-04-15 12:00] LINT wiki/concepts/牛顿法.md — OK
[2026-04-15 12:00] BM25 wiki/concepts/牛顿法.md — indexed
[2026-04-15 12:00] GRAPH rebuild — OK
[2026-04-15 12:01] LINT wiki/entities/牛顿.md — WARN: overview exceeds 200 chars
[2026-04-15 12:01] BM25 wiki/entities/牛顿.md — indexed
[2026-04-15 12:01] GRAPH rebuild — OK
```

---

## Phase 4: Templates Enhancement

### 4.1 `templates/wiki-page.md` — Stricter constraints

Add to template:
- Frontmatter: list ALL required fields with example values
- `概述` section: "50-200 字符，一句话概括核心定义或身份"
- `关键内容` section: "至少 300 字符，分条目阐述" with numbered sub-sections
- `来源` section: "列出所有信息来源，格式：`[[source page]] — 具体章节或页码`"
- `相关` section: "至少 3 个 [[双链]]，标注关系类型"
- Add character count constraints as HTML comments
- Add example filled-in content

### 4.2 `templates/daily.md` — Time structure

Add:
- Morning/afternoon/evening time slots
- Minimum 3 items per section requirement (stated in template comments)
- Required: at least 2 `[[links]]` to wiki pages
- `值得记住的` section: add "confidence: high/medium/low" annotation requirement

### 4.3 `templates/reflection.md` — Depth requirements

Add:
- `我的理解` section: minimum 200 words target (stated in template)
- `这改变了我什么看法` section: require "before → after" format
- `相关` section: minimum 3 links with relation type annotations
- Add `confidence` and `revisit_date` to frontmatter

### 4.4 `templates/judgment.md` — Evidence structure

Add:
- `依据` section: numbered evidence items, each with source citation
- `confidence` field in frontmatter (required)
- `revisit_date` field in frontmatter (required, default +30 days)
- `可能的反驳` section: minimum 2 counterarguments
- `如果我错了会怎样` section: add "impact: high/medium/low" annotation

### 4.5 `templates/weekly-review.md` — Quantitative metrics

Add:
- Metrics section: pages created, pages updated, QA questions answered, ingest count
- Link to previous week: `[[YYYY-WNN-1]]`
- `新的连接和发现` section: require at least 2 cross-domain links
- `下周最重要的三件事` section: add priority (P1/P2/P3) annotations

---

## Phase 5: Documentation

### 5.1 `docs/wiki.md` — Wiki Command Reference

Complete reference documentation for all wiki commands:
- Table of all commands with one-line descriptions
- For each command: purpose, input format, output, examples, dependencies, error handling
- Cross-references between related commands
- Workflow diagrams showing command interactions

### 5.2 `README.md` — Professional GitHub Overhaul

Structure:
```markdown
# LLM Wiki Plugin

> AI-powered personal knowledge operating system for Obsidian

[badges: Python, Claude Code, Obsidian, License]

## Architecture

[mermaid diagram: Raw Sources → Ingest → Wiki ← Query ← User]
[graph.png screenshot from static/asset/]

## Features

- [feature list with icons]

## Quick Start

[6-step setup guide]

## Commands

[table of all commands]

## Documentation

- [USERGUIDE.md](USERGUIDE.md)
- [docs/wiki.md](docs/wiki.md)
- [docs/CHANGELOG.md](docs/CHANGELOG.md)

## Knowledge Graph

[link to GitHub Pages visualization]

## Contributing

[contribution guide]
```

### 5.3 `USERGUIDE.md` — Extreme Detailed Guide

Sections:
1. Prerequisites (Python 3.10+, Obsidian, Claude Code CLI, API keys)
2. Installation step-by-step
3. Vault structure explained (every directory and file)
4. Command reference with full examples
   - wiki:ingest — single file example
   - wiki:ingest-loop — batch folder example
   - wiki:ingest-loop-qwen — Qwen batch example
   - wiki:query — question/answer example
   - wiki:graph — graph building example
   - wiki:lint — health check example
   - All other commands
5. Workflow recipes
   - Daily routine (journal → query → crystallize)
   - Weekly review workflow
   - Batch ingestion workflow
   - Knowledge graph exploration
6. Hook system explained
7. BM25 search system explained
8. Template customization guide
9. Troubleshooting (common errors, API issues, index corruption)
10. Advanced configuration (cron setup, custom templates, Qwen prompt tuning)

### 5.4 `docs/CHANGELOG.md` — Update

Append new entry for this release covering all changes.

---

## Phase 6: Visualization & CI/CD

### 6.1 `static/graph.html` — D3.js Force-Directed Knowledge Graph

**Self-contained single HTML file** (no build step, all CSS/JS inline).

**Features:**
- Force-directed layout with D3.js v7
- Collision detection and link force
- Node colors by type:
  - Entity: `#4A90D9` (blue)
  - Concept: `#50C878` (green)
  - Synthesis: `#9B59B6` (purple)
  - QA-Insight: `#E67E22` (orange)
- Node size: proportional to edge count (min 6px, max 24px radius)
- Edge colors by relation category:
  - structural (extends, implements): `#888`
  - semantic (relates_to, named_after): `#aaa`
  - conflict (contradicts, supersedes): `#e74c3c`
- Edge labels: relation type on hover
- Interactive features:
  - Zoom and pan (mouse wheel + drag)
  - Node drag (reposition individual nodes)
  - Search bar (filter/highlight by name)
  - Click node → highlight neighbors, show details sidebar
  - Double-click → zoom to node
- Sidebar panel:
  - Node title, type, confidence, tags
  - List of connected nodes with relation types
  - Link to source file path
- Dark/light mode toggle
- Responsive layout (works on mobile)
- Statistics bar: total nodes, edges, orphans, components

**CSS design:**
- Clean, modern sans-serif typography
- Subtle grid background
- Smooth transitions on hover/click
- Glass-morphism sidebar panel
- Color-coded legend

**Data loading:**
- Reads `graph.json` from same directory (relative path)
- Fallback: embedded sample data for demo

### 6.2 `.github/workflows/deploy.yml` — GitHub Actions

```yaml
name: Build & Deploy Knowledge Graph

on:
  push:
    branches: [main]
    paths:
      - 'vault/wiki/**'
      - 'vault/scripts/**'
      - 'static/**'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  lint-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install jieba rank_bm25 pyyaml

      - name: Lint wiki pages
        run: python3 vault/scripts/lint_wiki.py --json
        continue-on-error: false

      - name: Build graph
        run: python3 vault/scripts/build_graph.py --output static/graph.json

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: static/

  deploy:
    needs: lint-and-build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## CLAUDE.md Improvements

### Root `CLAUDE.md`

Add:
- Script dependencies section (Python packages: jieba, rank_bm25, pyyaml, openai)
- Command reference summary table
- Hook system overview
- BM25 index location and management
- graph.json and visualization info

### `vault/CLAUDE.md`

Add:
- `vault/qa/` directory purpose (QA log files)
- `vault/index/BM25/` directory purpose (search index)
- `vault/graph.json` purpose (knowledge graph data)
- Hook behavior documentation (what triggers, what runs)
- `vault/log.hook.md` purpose (hook execution log)
- New commands reference (ingest-loop, ingest-loop-qwen, graph)

---

## File Inventory

**New files to create:**

| File | Phase |
|------|-------|
| `vault/scripts/bm25_index.py` | P1 |
| `vault/scripts/qwen_ingest.py` | P1 |
| `vault/scripts/build_graph.py` | P1 |
| `vault/scripts/lint_wiki.py` | P1 |
| `vault/.claude/commands/wiki/ingest-loop.md` | P2 |
| `vault/.claude/commands/wiki/ingest-loop-qwen.md` | P2 |
| `vault/.claude/commands/wiki/graph.md` | P2 |
| `vault/scripts/setup-ingest-loop.sh` | P2 |
| `vault/scripts/setup-ingest-loop-qwen.sh` | P2 |
| `vault/scripts/hook_lint.sh` | P3 |
| `vault/scripts/hook_bm25.sh` | P3 |
| `vault/scripts/hook_graph.sh` | P3 |
| `vault/log.hook.md` | P3 |
| `vault/qa/` (directory) | P2 |
| `vault/index/BM25/` (directory) | P1 |
| `docs/wiki.md` | P5 |
| `USERGUIDE.md` | P5 |
| `static/graph.html` | P6 |
| `.github/workflows/deploy.yml` | P6 |

**Files to modify:**

| File | Phase |
|------|-------|
| `vault/.claude/commands/wiki/ingest.md` | P2 |
| `vault/.claude/commands/wiki/query.md` | P2 |
| `vault/.claude/commands/wiki/lint.md` | P2 |
| `vault/.claude/settings.local.json` | P3 |
| `vault/templates/wiki-page.md` | P4 |
| `vault/templates/daily.md` | P4 |
| `vault/templates/reflection.md` | P4 |
| `vault/templates/judgment.md` | P4 |
| `vault/templates/weekly-review.md` | P4 |
| `README.md` | P5 |
| `CLAUDE.md` | P4 |
| `vault/CLAUDE.md` | P4 |
| `docs/CHANGELOG.md` | P5 |

---

## Dependencies

**Python packages (add to requirements.txt):**
```
jieba>=0.42
rank_bm25>=0.2.2
pyyaml>=6.0
openai>=1.0.0
```

**System requirements:**
- Python 3.10+
- `$DASHSCOPE_API_KEY` environment variable (for qwen_ingest.py only)
- Claude Code CLI (for commands and hooks)
- Obsidian (for vault usage)
