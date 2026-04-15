# CLAUDE.md

This is an Obsidian Brain vault — a personal knowledge operating system.

## Quick Reference

- Schema: `_schema/CLAUDE.md` (read this first for full operational instructions)
- Commands: `.claude/commands/wiki/` (ingest, ingest-loop, query, check, lint, build, graph, reindex, consolidate, crystallize, journal, review, qa-import, convert-to-markdown)
- Templates: `templates/` (daily, wiki-page, reflection, judgment, weekly-review)
- Scripts: `scripts/` (search_wiki.py, bm25_index.py, qwen_ingest.py, build_graph.py, build_statistics.py, build_wiki_pages.py, snapshot_index.py, lint_wiki.py, hooks)

## Key Rules

1. Never modify files in `raw/` — it is read-only
2. All wiki pages must have complete frontmatter (see `_schema/CLAUDE.md`)
3. All operations must be logged in `log.md`
4. Journal content is private — do not expose in query results
5. Use [[双链]] liberally — links over folders

## Directory Purpose

| Directory | Purpose |
|-----------|---------|
| `qa/` | QA log files — ChatGPT-format question/answer records |
| `index/BM25/` | BM25 search index files (corpus.pkl, index.pkl, docmap.json) |
| `graph.json` | Knowledge graph data for D3.js visualization |
| `log.hook.md` | Hook execution log (lint, BM25, graph hook results) |

## Hook Behavior

Three PostToolUse hooks fire on every Write/Edit to `wiki/**/*.md`:
1. `hook_lint.sh` — validates page quality, logs to log.hook.md
2. `hook_bm25.sh` — updates BM25 index for modified page
3. `hook_graph.sh` — rebuilds graph.json

## Key Commands

- `wiki:check` — read-only diagnostics (不修改文件)
- `wiki:build` — build all static assets: graph + statistics + wiki HTML
- `wiki:graph` — wiki:build 的别名
- `wiki:reindex` — validate index.md integrity + generate topic maps
- `wiki:ingest-loop <folder> [--engine=qwen]` — batch ingest, default Claude engine, --engine=qwen for Qwen API
- `wiki:convert-to-markdown` — markitdown 批量转换 raw/ 中的 PDF/DOCX 等文件
