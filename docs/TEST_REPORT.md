# Wiki System Test Report

> Last updated: 2026-04-15

## 1. Script-Level Tests (run_all.sh)

Ran via `bash scripts/test/run_all.sh` — tests underlying Python scripts directly.

| Test | Script | Result | Detail |
|------|--------|--------|--------|
| wiki:lint | `lint_wiki.py --json` | PASS | 121 files, 0 errors, 175 warnings |
| wiki:graph | `build_graph.py --full` | PASS | 121 nodes, 781 edges, 3 orphans, 5 components |
| wiki:reindex | `snapshot_index.py` | PASS | 121/121 indexed, 0 missing, 0 orphaned |
| wiki:query | `bm25_index.py query` | PASS | BM25 returns relevant results for "贝叶斯定理" |

### Bugs found during script tests

| Bug | File | Fix |
|-----|------|-----|
| F4 check matched h1 page titles as "empty sections" | `lint_wiki.py:116` | Skip h1, skip h2 parents with h3 children |
| `--full` subprocess stdout mixed with main JSON | `build_graph.py:238` | `stdout=subprocess.DEVNULL` |
| `load_index_links` doesn't handle aliased wikilinks | `lint_wiki.py:62` | Use pipe-aware regex |
| No maps consistency check | `lint_wiki.py` | Added M1/M2 checks for maps/*.md |
| `relates_to` can be string not dict | `build_graph.py:110` | Skip non-dict entries |
| No math rendering in wiki HTML | `build_wiki_pages.py` | Added KaTeX CDN + auto-render |
| No graph analytics beyond edge count | `build_statistics.py` | Added networkx: PageRank, betweenness, clustering, diameter |

---

## 2. Claude SDK Integration Tests (`claude -p`)

Tests use `claude -p "/wiki:<cmd>" --output-format json --max-turns N` to invoke actual wiki commands end-to-end.

### Results

| Command | Result | Turns | Duration | Cost | Detail |
|---------|--------|-------|----------|------|--------|
| `wiki:lint` | PASS | ~20 | 141s | $0.45 | 0 errors, 175 warnings, auto-fixed 10 BM25 entries |
| `wiki:reindex` | PASS | ~40 | 298s | $0.90 | Updated 107 page tags, generated 7 topic maps |
| `wiki:query` | PASS | 15 | 124s | $0.54 | Answered CFL/Neumann question, wrote QA log |
| `wiki:graph` | PASS | 9 | 49s | $0.24 | 128 nodes, 828 edges (after lint read-only fix) |
| `wiki:ingest` | PASS | 36 | 498s | $1.38 | Ingested Wiener chapter → 7 new pages |
| `wiki:consolidate` | PASS | 34 | 265s | $0.96 | Merged working→episodic, skipped semantic (too few days) |
| `wiki:qa-import` | PASS | 20 | 83s | $0.54 | Processed QA log, created 数值PDE稳定收敛三角 insight |
| `wiki:crystallize` | PASS | 21 | 160s | $0.56 | Extracted 6 engineering insights to working memory |
| `wiki:journal` | PASS | 9 | 66s | $0.38 | Created daily note with related topics |
| `wiki:review` | PASS | 21 | 193s | $0.65 | Generated W16 weekly review with upgrade suggestions |
| **Total** | **10/10** | | **1877s** | **$6.00** | |

> Note: `wiki:ingest-loop` and `wiki:ingest-loop-qwen` are loop orchestrators that invoke `wiki:ingest` / `qwen_ingest.py` iteratively — not tested separately as they require interactive loop state.

### wiki:lint

Ran successfully. Key findings:
- **Auto-fixed**: 10 BM25 index missing entries
- **Pending**: 1 template comment in index.md flagged as broken link (I2)
- **Warnings**: B1 (85 broken links), F3 (71 overview too long), O1 (8 orphans)

Changes: `vault/index/BM25/` updated, `vault/log.md` appended

### wiki:reindex

Ran successfully. Full reindex workflow:
1. Integrity check: 121/121 OK
2. Snapshot saved
3. Tags audit: 107 pages had generic-only tags (`研究`/`技术`) → updated to domain-specific (`数值分析`, `矩阵理论`, `概率论`, `组合数学`)
4. Generated 7 topic maps: 数学(56), 数值分析(19), 概率论(15), 矩阵理论(15), AI(8), 组合数学(5), 工具(3)

Changes: 107 wiki page frontmatter, 7 `vault/maps/*.md` files

### wiki:graph

Initially **failed** (max_turns=30, lint auto-fix burned turns on permission denials). Fixed by changing lint step to read-only. Re-test: **PASS** in 9 turns / 49s / $0.24.

Changes: `vault/graph.json`, `static/graph.json`, `static/graph-statistics.json`, `static/wiki/` updated, `log.md` appended.

### wiki:query

Ran successfully. Tested with: `什么是CFL条件？它与冯·诺依曼稳定性分析有什么关系？`
- BM25 found relevant pages
- Read 3 pages, synthesized answer
- Wrote QA log to `vault/qa/2026-04-15.md`

### wiki:ingest

Ran successfully. Ingested `raw/books/概率论/13_wiener_brownian_motion.md`:
- Created 2 entities: 诺伯特·维纳, 路易·巴舍利耶
- Created 5 concepts: Wiener过程, Wiener测度, Wiener积分, Ito随机积分, 随机游走
- Updated index.md (128 pages)
- Updated BM25 index

### wiki:consolidate

PASS. Merged 5 observations from working memory session #3 into episodic memory. Skipped semantic promotion (needs 3+ days). Updated dashboard.md.

### wiki:qa-import

First attempt FAIL (max_turns=20 without --allowedTools). Re-test with tools: **PASS** in 20 turns / 83s. Found existing insight page `数值PDE稳定收敛三角`, confirmed links, logged.

### wiki:crystallize

PASS. Extracted 6 engineering insights from session context into working memory. Correctly decided not to create synthesis (single domain, needs 3+ cross-domain connections).

### wiki:journal

PASS. Created `journal/daily/2026-04-15.md` with recent ingest topics pre-filled. 9 turns, 66s.

### wiki:review

PASS. Generated `journal/daily/2026-W16.md` weekly review. Identified 4 cross-cutting cognitive patterns, suggested 3 priority items for next week. 21 turns, 193s.

### Bugs found during integration tests

| Bug | Severity | Detail | Status |
|-----|----------|--------|--------|
| wiki:graph lint auto-fix burns turns | HIGH | Fixed: lint step changed to read-only | Fixed |
| `claude -p` needs `--allowedTools` for write commands | HIGH | Without it, Edit/Write permissions denied, turns wasted | Documented |
| wiki:qa-import needs 40 turns for complex QA files | MEDIUM | 20 turns insufficient for full parse→cluster→extract pipeline | Use `--max-turns 40` |

### Key lesson: `claude -p` invocation pattern

```bash
# Read-only commands (lint, graph, query):
claude -p "/wiki:<cmd>" --output-format json --max-turns 20

# Write commands (ingest, consolidate, crystallize, journal, review, qa-import, reindex):
claude -p "/wiki:<cmd> <args>" --output-format json --max-turns 40 \
  --allowedTools 'Read,Write,Edit,Bash,Glob,Grep'
```

---

## 3. Commands Not Tested

| Command | Reason |
|---------|--------|
| `wiki:ingest-loop` | Requires ralph-loop mechanism (interactive state file) |
| `wiki:ingest-loop-qwen` | Requires `DASHSCOPE_API_KEY` environment variable |
