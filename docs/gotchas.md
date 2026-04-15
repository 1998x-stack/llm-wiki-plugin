# Gotchas & Known Issues — Index

> Last updated: 2026-04-16

Issues are split into topical files under `docs/gotchas/`.

## Files

| File | Topics | Issues |
|------|--------|--------|
| [ingest-issues.md](gotchas/ingest-issues.md) | Index errors, broken links, ingest-loop state | #1-4 |
| [qwen-api.md](gotchas/qwen-api.md) | Model names, frontmatter failures, session summary | Qwen-specific |
| [infrastructure.md](gotchas/infrastructure.md) | Source format, BM25, graph rebuild, hooks, keywords pollution | #5-8, #36-37 |
| [knowledge-graph.md](gotchas/knowledge-graph.md) | Cross-domain connections, fix checklist | #9 |
| [code-review-bugs.md](gotchas/code-review-bugs.md) | V2.1-V2.3 code review (12 bugs fixed) | #10 |
| [integration-testing.md](gotchas/integration-testing.md) | claude -p max_turns, lint F4, allowedTools | #11-14 |
| [script-fixes.md](gotchas/script-fixes.md) | Lint regex, relates_to crash, KaTeX math, B1 false-positive in code blocks | #15-17, #35 |
| [v3.3-refactor.md](gotchas/v3.3-refactor.md) | wiki_utils, dedup, QA pipeline, XSS, debounce | #18-27 |
| [v3.4-relink-reorganize.md](gotchas/v3.4-relink-reorganize.md) | relink substring matching, bold markers, hooks, macOS case, re-map.json, lint removal | #28-34 |

## Quick Status

| Status | Count | Description |
|--------|-------|-------------|
| Fixed | 21 | Code bugs, script issues, XSS, edge directionality, macOS case-insensitive, B1 false-positive in code blocks, keywords.txt year-range pollution (28 entries), 来源 non-standard format (125 entries) |
| Documented | 12 | yaml fallback, pickle, debounce, qa/ deprecation, relink substring, bold markers, hooks, re-map.json, 来源 boundary, lint removal |
| Open | 3 | Remaining ingest files, broken links, dedup semantic matching |

## Fix Checklist (remaining)

| Priority | Task |
|----------|------|
| HIGH | Complete ingest files 14-16 (Kolmogorov/Doob/Ito) |
| MEDIUM | Fix broken link `[[马尔可夫]]` → `[[安德烈·马尔可夫]]` |
| MEDIUM | Fix broken link `[[切比雪夫不等式]]` link mismatch |
| LOW | Create `[[离散傅里叶变换]]` concept page |
| ~~LOW~~ | ~~Standardize source section format (bare string → `[[raw/...]]`)~~ — **FIXED 2026-04-16** |
