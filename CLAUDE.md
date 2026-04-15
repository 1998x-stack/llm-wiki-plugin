# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is an **LLM Wiki Plugin** — an AI-powered personal knowledge operating system built on Obsidian. It combines three methodologies: LLM Wiki v1 (Karpathy), LLM Wiki v2 (agentmemory), and kepano-Obsidian.

The repo contains:

| Directory | Role |
|-----------|------|
| `vault/` | Obsidian vault — the live knowledge base |
| `vault/.claude/commands/wiki/` | Claude Code commands for knowledge operations |
| `vault/scripts/` | Python and shell automation scripts |
| `docs/` | Design specs, references, and changelog |
| `static/` | GitHub Pages assets (graph visualization) |

## Core Architecture

Three-layer pattern:
1. **Raw Sources** (`vault/raw/`) — immutable source documents. Read-only.
2. **Wiki** (`vault/wiki/`) — LLM-generated knowledge pages with cross-references.
3. **Schema** (`vault/_schema/`) — conventions, types, and quality rules.

## Commands

| Command | Purpose |
|---------|---------|
| `wiki:ingest` | Process raw source → wiki pages |
| `wiki:ingest-loop` | Batch ingest with ralph-loop (`--engine=qwen` for Qwen API) |
| `wiki:query` | Answer questions with unified search (BM25 + maps + graph) |
| `wiki:check` | Read-only diagnostics (no auto-repair) |
| `wiki:lint` | Health check + auto-repair (calls check first) |
| `wiki:build` | Build all static assets: graph + statistics + wiki HTML |
| `wiki:reindex` | Validate index integrity + generate topic maps |
| `wiki:maintain` | Full pipeline: reindex → check → lint → build |
| `wiki:consolidate` | Memory layer promotion + decay |
| `wiki:crystallize` | Session → structured summary |
| `wiki:journal` | Journal assistance |
| `wiki:review` | Fractal review (weekly/monthly/quarterly) |
| `wiki:qa-import` | Import QA data → wiki insights |
| `wiki:convert-to-markdown` | markitdown 批量转换非 markdown 文件 |

## Scripts

| Script | Purpose | Dependencies |
|--------|---------|-------------|
| `search_wiki.py` | Unified search (BM25 + maps + graph + RRF) | jieba, rank_bm25, pyyaml |
| `bm25_index.py` | BM25 search index (build/update/query) | jieba, rank_bm25 |
| `qwen_ingest.py` | Qwen API wiki extraction (multi-page: `--raw` only; legacy: `--raw --wiki`) | openai, pyyaml |
| `build_graph.py` | Knowledge graph JSON builder (outputs `graph.json`) | pyyaml |
| `build_statistics.py` | Statistics JSON from graph + frontmatter | pyyaml |
| `build_wiki_pages.py` | Wiki markdown → static HTML | pyyaml, markdown |
| `snapshot_index.py` | Index integrity checker (check/update/snapshot) | pyyaml |
| `lint_wiki.py` | Standalone lint checker | pyyaml |
| `hook_lint.sh` | PostToolUse hook: lint | — |
| `hook_bm25.sh` | PostToolUse hook: BM25 update | — |
| `hook_graph.sh` | PostToolUse hook: graph rebuild | — |
| `setup-ingest-loop.sh` | Setup ralph-loop for Claude ingest | — |
| `setup-ingest-loop-qwen.sh` | Setup ralph-loop for Qwen ingest | — |
| `watch-raw.sh` | fswatch monitor for auto-ingest | — |
| `cron-setup.sh` | Install cron jobs for consolidate/lint/review | — |

## Hooks

PostToolUse hooks fire on every Write/Edit to `wiki/**/*.md`:
1. **Lint** → validates page quality
2. **BM25** → updates search index
3. **Graph** → rebuilds graph.json

Hook logs: `vault/log.hook.md`

## Dependencies

Python 3.10+ packages: `jieba`, `rank_bm25`, `pyyaml`, `openai`, `markdown`, `networkx`, `markitdown`

Install: `pip install -r requirements.txt`

## Key Concepts

- **BM25 Index** (`vault/index/BM25/`): jieba-tokenized full-text search
- **Graph** (`vault/graph.json`): knowledge graph for visualization
- **QA Logs** (`vault/qa/`): ChatGPT-format Q&A records
- **Crystallization**: compounding knowledge into permanent entries
- **Memory lifecycle**: confidence scoring, supersession, decay
- **Typed relationships**: edges with labels (extends, contradicts, etc.)
