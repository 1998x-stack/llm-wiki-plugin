# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **design pattern documentation project** — not runnable code. It describes a pattern for building LLM-maintained personal knowledge bases (called an "LLM Wiki"). There is no build system, no tests, and no executable code.

The repo contains two markdown documents that evolve the same core idea:

| File | Role |
|------|------|
| `llm-wiki-v1.md` | Foundational concept: three-layer architecture, core operations, use cases |
| `llm-wiki-v2.md` | Extended with production lessons: knowledge graph, lifecycle management, hybrid search, multi-agent patterns |

## Core Architecture (The Pattern Described)

The pattern uses three layers:

1. **Raw Sources** — immutable source documents (articles, papers, images). LLM reads only.
2. **Wiki** — LLM-owned directory of markdown files: entity pages, concept pages, comparisons, syntheses with cross-references.
3. **Schema** — a config document (e.g. CLAUDE.md) encoding conventions, workflows, and lint rules that make the LLM a disciplined knowledge worker.

Key operations: **ingest** (process new sources into wiki), **query** (answer questions from wiki), **lint** (audit wiki for staleness, gaps, orphans).

## How to Work With This Repo

- These documents are **templates/blueprints** meant to be adapted. When a user wants to instantiate the pattern, the output is a tailored schema document (CLAUDE.md) for their specific knowledge domain.
- v2 extends v1 — read both when understanding the full design space. v1 is cleaner for introductions; v2 addresses scale concerns.
- The central insight: the schema document is the real product. It encodes the conventions that make the wiki self-consistent over time.

## Key Concepts to Know

- **Crystallization** (v2): compounding knowledge from exploration into permanent wiki entries.
- **Memory lifecycle** (v2): confidence scoring, supersession, and forgetting stale knowledge.
- **Typed relationships** (v2): knowledge graph edges with labels (e.g., `implements`, `contradicts`, `extends`).
- **Index and log files**: `index.md` serves as a table of contents; `log.md` records ingest history and decisions.
