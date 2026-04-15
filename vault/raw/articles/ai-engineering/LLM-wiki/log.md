# Wiki Activity Log

> **Append-only. Never edit past entries.**
> Every entry begins with `## [YYYY-MM-DD] type | title` for grep-friendliness.
>
> Useful shell commands:
> ```bash
> # Last 5 entries
> grep "^## \[" log.md | tail -5
>
> # All ingests
> grep "^## \[.*\] ingest" log.md
>
> # All contradictions found
> grep -A 10 "^## \[" log.md | grep "Contradiction"
>
> # Activity in a date range
> grep "^## \[2026-03" log.md
> ```
>
> Entry types: `ingest` | `query` | `lint` | `schema` | `init` | `explore`

---

## [YYYY-MM-DD] init | Wiki Initialized

- Schema version: 1.0
- Topic: [fill in]
- Directory structure created
- CLAUDE.md written
- index.md, log.md, overview.md initialized
- Pages created: overview, index, log
- Pages updated: none
- Notes: [any initial decisions about scope or conventions]

---

<!-- 
INGEST TEMPLATE:
## [YYYY-MM-DD] ingest | [Source Title]
- Source file: raw/[filename]
- Author: | Published:
- Pages created: [[source-slug]], [[entity-a]], [[concept-b]]
- Pages updated: [[entity-x]], [[overview]]
- Key findings: 
  1. [finding]
  2. [finding]
- Contradictions found: [[page-a]] vs [[page-b]] on [claim] / none
- Open questions raised:
  - ❓ [question]
- Notes: [anything unusual about this source or ingest]
-->

<!--
QUERY TEMPLATE:
## [YYYY-MM-DD] query | [Question summary]
- Full question: "[verbatim question]"
- Pages consulted: [[p1]], [[p2]], [[p3]]
- Answer confidence: high | medium | low
- Filed as analysis: yes → [[analysis-slug]] / no
- Follow-up questions:
  - ❓ [question]
- Notes:
-->

<!--
LINT TEMPLATE:
## [YYYY-MM-DD] lint | Lint Pass #N
- Total pages audited: N
- Orphan pages: [list or "none"]
- Missing pages (referenced but absent): [list or "none"]
- Stale stubs: [list or "none"]
- Unresolved contradictions: [count]
- Suggested new pages: [list or "none"]
- Suggested merges: [list or "none"]
- Actions taken: [list changes made or "none — awaiting instructions"]
-->

<!--
SCHEMA TEMPLATE:
## [YYYY-MM-DD] schema | [What changed]
- Change: [description]
- Reason: [why]
- Backfill needed: yes ([pages affected]) / no
-->
