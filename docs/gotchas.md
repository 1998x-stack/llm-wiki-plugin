# Gotchas & Known Issues — Index

> Last updated: 2026-04-15

Issues are split into topical files under `docs/gotchas/`.

## Files

| File | Topics | Issues |
|------|--------|--------|
| [ingest-issues.md](gotchas/ingest-issues.md) | Index errors, broken links, ingest-loop state | #1-4 |
| [qwen-api.md](gotchas/qwen-api.md) | Model names, frontmatter failures, session summary | Qwen-specific |
| [infrastructure.md](gotchas/infrastructure.md) | Source format, BM25, graph rebuild, hooks | #5-8 |
| [knowledge-graph.md](gotchas/knowledge-graph.md) | Cross-domain connections, fix checklist | #9 |
| [code-review-bugs.md](gotchas/code-review-bugs.md) | V2.1-V2.3 code review (12 bugs fixed) | #10 |
| [integration-testing.md](gotchas/integration-testing.md) | claude -p max_turns, lint F4, allowedTools | #11-14 |
| [script-fixes.md](gotchas/script-fixes.md) | Lint regex, relates_to crash, KaTeX math | #15-17 |

## Quick Status

| Status | Count | Description |
|--------|-------|-------------|
| Fixed | 14 | Code bugs, script issues, deployment blockers |
| Documented | 2 | claude -p allowedTools, cross-domain connections |
| Open | 3 | Remaining ingest files 14-16, broken links, source format |

## Fix Checklist (remaining)

| Priority | Task |
|----------|------|
| HIGH | Complete ingest files 14-16 (Kolmogorov/Doob/Ito) |
| MEDIUM | Fix broken link `[[马尔可夫]]` → `[[安德烈·马尔可夫]]` |
| MEDIUM | Fix broken link `[[切比雪夫不等式]]` link mismatch |
| LOW | Create `[[离散傅里叶变换]]` concept page |
| LOW | Standardize source section format (bare string → `[[raw/...]]`) |
