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

---

## 2. Claude SDK Integration Tests (`claude -p`)

Tests use `claude -p "/project:wiki/<cmd>" --output-format json --max-turns N` to invoke actual wiki commands end-to-end.

### Results

| Command | Result | Turns | Duration | Cost | Detail |
|---------|--------|-------|----------|------|--------|
| `wiki:lint` | PASS | ~20 | 141s | $0.45 | 0 errors, 175 warnings, auto-fixed 10 BM25 entries |
| `wiki:reindex` | PASS | ~40 | 298s | $0.90 | Updated 107 page tags, generated 7 topic maps |
| `wiki:query` | PASS | 15 | 124s | $0.54 | Answered CFL/Neumann question, wrote QA log |
| `wiki:graph` | **FAIL** | 30 (max) | 176s | $0.90 | Hit max_turns — lint auto-fix too ambitious |
| `wiki:ingest` | PASS | 36 | 498s | $1.38 | Ingested Wiener chapter → 7 new pages |

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

**Failed** — hit `max_turns` (30). Root cause: the `wiki:graph` command includes a lint step that tries to auto-fix broken links. In non-interactive `claude -p` mode, permission denials for edits cause the agent to retry, burning through turns. The actual graph build (`build_graph.py --full`) completes fine as a script.

**Gotcha**: `wiki:graph` should either skip lint auto-fix in non-interactive mode, or the lint step should be read-only when called from graph.

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

### Bugs found during integration tests

| Bug | Severity | Detail | Status |
|-----|----------|--------|--------|
| wiki:graph hits max_turns in non-interactive mode | HIGH | Lint auto-fix burns turns on permission denials | Documented — needs command redesign |
| index.md has duplicate entity block after reindex+ingest | MEDIUM | Reindex inserted entities at wrong position; ingest appended more | Will self-correct on next `snapshot_index.py --update` |

---

## 3. Commands Not Tested

| Command | Reason |
|---------|--------|
| `wiki:ingest-loop` | Requires ralph-loop mechanism (interactive) |
| `wiki:ingest-loop-qwen` | Requires `DASHSCOPE_API_KEY` |
| `wiki:consolidate` | Memory system — needs accumulated knowledge |
| `wiki:crystallize` | Session-dependent — needs active conversation |
| `wiki:journal` | Personal layer — needs user input |
| `wiki:review` | Requires time-based data (weekly/monthly) |
| `wiki:qa-import` | Tested indirectly via wiki:query's QA write |
