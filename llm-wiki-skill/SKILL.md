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

1. **raw/ is read-only** -- never modify source files
2. **wiki/ is LLM-owned** -- all wiki pages created and maintained by you
3. **journal/ is user-owned** -- personal thoughts written by user, you assist with linking and analysis
4. **Links over folders** -- use [[wikilinks]] to organize relationships
5. **Bottom-up** -- structure emerges naturally, no preset taxonomy
6. **Log everything** -- all operations append to log.md

## Path Discovery

Scripts find the user's wiki root via:
1. `LLM_WIKI_ROOT` environment variable
2. Walking up from CWD to find `.wiki-root` marker
3. Error if not found -- prompt user to run `/llm-wiki:init`

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
draft --(confidence >= 0.5)-- active
active --(confidence < 0.3)-- stale
stale --(30 days no update)-- archived
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
