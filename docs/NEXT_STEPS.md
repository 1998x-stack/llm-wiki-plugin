# Wiki System — Next Steps & Improvement Opportunities

> Generated from v3.0 enhancement brainstorming (2026-04-15)
> Based on: `docs/superpowers/specs/2026-04-15-wiki-v3-enhancement-design.md` section 7

---

## 1. Concrete Command Refactors

### 1.1 Split: wiki:lint → wiki:check + wiki:lint

**Problem:** `wiki:lint` does 9 checks (A-I) + semantic analysis + auto-repair in one command. Too many responsibilities.

**Proposed split:**
- `wiki:check` — **read-only** diagnostics. Runs all checks A-I plus semantic analysis, generates report. Never modifies files.
- `wiki:lint` — calls `wiki:check` first, then auto-repairs fixable issues.

**Why:** Separates "what's wrong?" from "fix it." Useful for CI (run check without side effects) and for reviewing before auto-repair.

**Effort:** Low. Extract check logic from lint.md into check.md, have lint.md call check first.

---

### 1.2 Rename: wiki:graph → wiki:build

**Problem:** `wiki:graph` doesn't just build the graph — it builds graph.json, statistics.json, and all wiki HTML pages. The name is misleading.

**Proposed:** Rename to `wiki:build` (builds all static assets).

**Why:** Accurate naming. Users currently don't know that running "graph" also regenerates HTML and statistics.

**Effort:** Low. Rename command file, update all references.

**Risk:** Breaking existing muscle memory. Consider keeping `wiki:graph` as an alias that calls `wiki:build`.

---

### 1.3 Merge: wiki:ingest-loop + wiki:ingest-loop-qwen → wiki:ingest-loop --engine=\<claude|qwen\>

**Problem:** Two commands share 90% of logic (setup script, state management, progress tracking). Only the extraction engine differs.

**Proposed:**
```
/wiki:ingest-loop <folder>                  # default: claude engine
/wiki:ingest-loop <folder> --engine=qwen    # qwen engine
```

**Why:** DRY. Reduces maintenance burden. New engines (e.g. local LLM) can be added via the same flag.

**Effort:** Medium. Merge the two command files, parameterize setup scripts.

---

## 2. Contradictions to Resolve

### 2.1 Memory vs Wiki duplication

**Issue:** `_memory/semantic/` and `wiki/syntheses/` both accumulate knowledge. Same insight can exist in both with different confidence scores.

**Resolution options:**
1. **Single source of truth**: syntheses/ pages ARE the semantic memory. Remove `_memory/semantic/` as a separate store.
2. **Clear boundary**: syntheses/ = published cross-topic analyses. semantic/ = private factual claims (not topic-spanning). Never duplicate.
3. **Merge on promotion**: when a semantic memory reaches confidence 0.9+, auto-create a syntheses/ page and mark the semantic memory as `published: true`.

**Recommended:** Option 2 with a clear rule in `_schema/CLAUDE.md`.

---

### 2.2 Hooks vs explicit commands — double work

**Issue:** PostToolUse hooks auto-rebuild graph/BM25 on every wiki file write. But `wiki:ingest` also calls `lint_wiki.py` and `bm25_index.py` explicitly at the end. This means double work during ingest.

**Resolution options:**
1. **Remove explicit calls from ingest**: let hooks handle everything. Simpler, but hooks must be reliable.
2. **Disable hooks during batch operations**: set an env var `WIKI_BATCH=1` that hooks check. If set, hooks skip. Ingest sets this var and does its own cleanup at the end.
3. **Accept the duplication**: hooks are idempotent. Double work is ~2 seconds. Not a real problem at current scale.

**Recommended:** Option 3 for now. Revisit at 500+ pages.

---

### 2.3 index.md as bottleneck

**Issue:** Every ingest appends to index.md. With concurrent ingest-loops, this causes merge conflicts.

**Resolution options:**
1. **Rebuild from scratch**: like maps/, regenerate index.md from wiki/ on each reindex. Remove append-only behavior.
2. **Lock file**: use a `.index.lock` file during writes.
3. **Atomic writes**: each ingest writes to `index.md.tmp`, then atomically replaces.

**Recommended:** Option 1. Makes index.md a computed artifact (like maps/), not a manually-maintained file. `wiki:reindex` already validates completeness.

---

## 3. Near-term Speculative Features

### 3.1 Vector Search (embedding-based)

**What:** Add semantic similarity search as a fourth retrieval stream in `search_wiki.py`.

**How:**
- Use `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (supports Chinese)
- Store embeddings in `index/vectors/` as `.npy` files
- Add `--embed` flag to `bm25_index.py` to build embeddings alongside BM25
- Hook into `search_wiki.py` as a fourth RRF source

**Effort:** Medium. ~200 lines of Python. Requires `sentence-transformers` + `numpy` (~500MB model download).

**Priority:** Low at current scale (~170 pages). BM25 + maps + graph covers most queries well. Revisit at 500+ pages or when Chinese semantic search fails on BM25.

---

### 3.2 MCP Server

**What:** Expose wiki operations as an MCP server so any LLM tool can use the knowledge base.

**Tools to expose:**
- `wiki_search(query, top_n)` — calls search_wiki.py
- `wiki_ingest(raw_path)` — triggers ingest
- `wiki_stats()` — returns graph statistics
- `wiki_page(page_name)` — reads a specific wiki page

**How:** Thin TypeScript/Python wrapper around existing scripts. MCP SDK handles protocol.

**Effort:** Medium. ~300 lines. Well-defined API (existing scripts do all the work).

**Priority:** Medium. Useful when working with multiple LLM tools (Codex, GPT-4, local models).

---

### 3.3 Enhanced fswatch → auto-ingest pipeline

**What:** Replace manual `wiki:ingest-loop` with a fully automated file watcher.

**Pipeline:**
```
New file in raw/ → detect format
  → if non-markdown: markitdown convert
  → qwen_ingest.py (batch, no Claude context)
  → bm25_index.py update
  → build_graph.py (debounced, every 5 min)
```

**How:** Enhance existing `watch-raw.sh` with format detection and markitdown pre-processing. Use debounced graph rebuilds to avoid thrashing.

**Effort:** Low-Medium. Mostly glue code.

**Priority:** Medium. Biggest UX improvement — drop a PDF and the wiki updates automatically.

---

### 3.4 wiki:diff — show what changed

**What:** New command showing knowledge base changes since last commit/snapshot.

**Output:**
- New pages (with titles and topics)
- Updated pages (confidence changes, new relationships)
- Deleted pages
- Relationship changes (new edges, removed edges)

**How:** `git diff --name-status` + frontmatter parsing. Compare current state against last snapshot.

**Effort:** Low. ~100 lines of Python.

**Priority:** Low. Nice for review workflows before committing.

---

### 3.5 wiki:export — portable knowledge export

**What:** Export the wiki (or a topic subset) to a portable format.

**Formats:**
- Markdown bundle (zip with all pages + assets)
- JSON-LD knowledge graph
- Obsidian Publish-compatible static site

**How:** New Python script that reads wiki/ + graph.json and packages output.

**Effort:** Medium.

**Priority:** Low. Useful for sharing, backup, or migrating to another system.

---

## 4. Priority Matrix

| Feature | Effort | Impact | Priority |
|---------|--------|--------|----------|
| lint/check split | Low | Medium | **P1** |
| graph→build rename | Low | Low | P2 |
| ingest-loop merge | Medium | Medium | P2 |
| Memory/wiki boundary rule | Low | High | **P1** |
| index.md rebuild-from-scratch | Medium | Medium | P2 |
| fswatch auto-pipeline | Medium | High | **P1** |
| MCP server | Medium | Medium | P2 |
| wiki:diff | Low | Low | P3 |
| Vector search | Medium | Low (at scale) | P3 |
| wiki:export | Medium | Low | P3 |

**Recommended next session:** P1 items (lint/check split, memory boundary rule, fswatch pipeline).
