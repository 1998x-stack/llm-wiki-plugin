# CLAUDE.md

This is an Obsidian Brain vault — a personal knowledge operating system.

## Quick Reference

- Schema: `_schema/CLAUDE.md` (read this first for full operational instructions)
- Commands: `.claude/commands/wiki/` (ingest, ingest-loop, ingest-loop-qwen, query, lint, graph, consolidate, crystallize, journal, review, qa-import)
- Templates: `templates/` (daily, wiki-page, reflection, judgment, weekly-review)
- Scripts: `scripts/` (bm25_index.py, qwen_ingest.py, build_graph.py, lint_wiki.py, hooks)

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

## New Commands

- `wiki:ingest-loop <folder>` — batch ingest using ralph-loop, one file per iteration
- `wiki:ingest-loop-qwen <folder>` — batch ingest using Qwen 3-plus API
- `wiki:graph` — lint + build graph.json with stats report
