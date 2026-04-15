# LLM Wiki — Agent Schema (CLAUDE.md)

> **This file is the operating contract between you (the LLM agent) and this knowledge base.**
> Read it fully at the start of every session before touching any file.
> When in doubt, refer back here.

---

## 0. What This Wiki Is

This is a **persistent, compounding knowledge base** on the topic: `[TOPIC — fill in]`.

You (the LLM) are the sole writer and maintainer of the `wiki/` directory.
I (the human) am the curator of sources and the director of analysis.

The wiki is not a cache of raw documents. It is a **compiled synthesis** — structured pages
that get richer with every source ingested and every question asked.
Cross-references are pre-built. Contradictions are pre-flagged. Nothing is re-derived from scratch.

---

## 1. Directory Layout

```
llm-wiki/
├── CLAUDE.md              ← THIS FILE. The schema. Read first, every session.
├── wiki/
│   ├── index.md           ← Master catalog. Update after every ingest or new page.
│   ├── log.md             ← Append-only activity timeline. Never edit past entries.
│   ├── overview.md        ← Top-level synthesis. The "executive summary" of the wiki.
│   ├── entities/          ← Named things: people, companies, products, places, events
│   ├── concepts/          ← Abstract ideas, frameworks, mechanisms, terminology
│   ├── sources/           ← One summary page per ingested raw source
│   └── analyses/          ← Query answers, comparisons, syntheses worth preserving
└── raw/
    ├── README.md          ← How to add sources
    ├── assets/            ← Locally downloaded images
    └── [source files]     ← Immutable. Never modify. LLM reads, never writes here.
```

### Rules
- You **never** write to `raw/`. That directory is read-only for you.
- You **own** everything in `wiki/`. Create, update, reorganize freely.
- File names use `kebab-case.md`. Spaces become hyphens. All lowercase.
- Every wiki file must have a YAML frontmatter block (see §3).

---

## 2. Page Types & When to Create Each

| Type | Directory | Create When |
|------|-----------|-------------|
| **Entity** | `wiki/entities/` | A named thing appears in ≥2 sources or is central to 1 source |
| **Concept** | `wiki/concepts/` | An abstract idea, term, or framework deserves its own explanation |
| **Source** | `wiki/sources/` | Every time a raw source is ingested |
| **Analysis** | `wiki/analyses/` | A query answer is worth preserving (comparison, synthesis, deep-dive) |
| **Overview** | `wiki/overview.md` | Exists as a single file; update it, never recreate it |

**When unsure**: create the page. Orphan pages are cheaper than missing ones.
The lint pass will clean up orphans.

---

## 3. Page Format Standard

Every wiki page must begin with YAML frontmatter, followed by structured content.

### 3.1 Frontmatter Schema

```yaml
---
title: "Page Title"
type: entity | concept | source | analysis | overview
tags: [tag1, tag2]          # lowercase, hyphenated
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: N             # entities/concepts: how many sources reference this page
status: stub | active | mature | superseded
---
```

**Status definitions:**
- `stub` — page exists but has minimal content (< 3 sections filled)
- `active` — being actively updated as new sources arrive
- `mature` — comprehensive; only needs updates when contradicted
- `superseded` — older info, replaced by a newer page (add a `supersedes:` field)

### 3.2 Source Page Format

```markdown
---
title: "Source Title"
type: source
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: 1
status: active
raw_file: raw/filename.md
author: ""
published: YYYY-MM-DD
domain: ""             # e.g. "arxiv.org", "nytimes.com"
---

# Source Title

**Author:** | **Published:** | **Domain:** | **Ingested:**

## TL;DR
One paragraph. What is this source? What's the single most important claim?

## Key Claims
Bulleted list. Each claim is a factual assertion, not a heading.
- Claim 1
- Claim 2

## Evidence & Data
Tables, numbers, quotes (< 15 words), statistics worth preserving.

## Tensions & Contradictions
Does this source contradict anything already in the wiki?
List explicitly: "Contradicts [[entity-page]] on X"

## Connections
Which wiki pages does this source inform or update?
- Updates [[entity-name]]: reason
- Informs [[concept-name]]: reason

## Raw Excerpts
Paste 2-5 verbatim excerpts (< 50 words each) that are too important to paraphrase.
```

### 3.3 Entity Page Format

```markdown
---
title: "Entity Name"
type: entity
...
---

# Entity Name

**Type:** Person | Company | Product | Place | Event
**Also known as:** aliases, abbreviations

## Summary
2-3 sentence factual summary. What is this? Why does it matter in this wiki's context?

## Key Facts
| Attribute | Value |
|-----------|-------|
| Founded   | ...   |
| ...       | ...   |

## Role in [Wiki Topic]
What does this entity do in the context of our specific research domain?

## Claims Made / Positions Taken
If the entity makes claims relevant to our topic, list them here with source citations.

## Connections
- Related to [[entity-b]]: description of relationship
- Exemplifies [[concept-x]]: how

## Sources
- [[source-a]] — what this source says about this entity
- [[source-b]] — what this source says about this entity

## Open Questions
What do we not yet know about this entity that matters?
```

### 3.4 Concept Page Format

```markdown
---
title: "Concept Name"
type: concept
...
---

# Concept Name

## Definition
1-2 sentences. Precise. Avoid jargon unless defined here.

## Why It Matters (in this wiki's context)
Not a generic explanation — why does THIS wiki care about this concept?

## Mechanism / How It Works
The actual explanation. Use diagrams (Mermaid) or tables if helpful.

## Variants & Subtypes
If the concept has sub-forms, list them here.

## Instantiations
Which entities in this wiki exemplify this concept?
- [[entity-a]] — how
- [[entity-b]] — how

## Tensions
Where does this concept conflict with other concepts in the wiki?

## Sources
- [[source-a]]: how this source discusses the concept
```

### 3.5 Analysis Page Format

```markdown
---
title: "Analysis: [Question or Theme]"
type: analysis
...
---

# Analysis: [Title]

**Question:** The original question this analysis answers.
**Date:** YYYY-MM-DD
**Sources consulted:** [[s1]], [[s2]], ...

## Answer / Finding
Direct answer in 1-3 paragraphs.

## Supporting Evidence
Structured evidence from wiki pages.

## Counterarguments / Caveats
What challenges this finding?

## Implications
What does this mean for the broader wiki thesis?

## Follow-up Questions
What should be investigated next?
```

---

## 4. Cross-Reference Conventions

- Use `[[page-name]]` Obsidian-style wikilinks. The linked name = the filename without `.md`.
- **Backlinks are mandatory**: if page A links to page B, check if page B should link back to A.
- Never leave a cross-reference without a brief annotation: `[[entity]] — why it's linked`.
- Contradictions get a special marker: `⚡ Contradicts [[page]] on [claim]`
- Unresolved questions get: `❓ Open: [what we don't know]`
- High-confidence claims get: `✓ Confirmed across [[s1]], [[s2]], [[s3]]`

---

## 5. Workflows

### 5.1 Ingest Workflow

When I say "ingest [source]", execute these steps **in order**:

```
1. READ the raw source completely.
2. DISCUSS: surface 3-5 key takeaways with me before writing anything.
   Ask: "Does this contradict anything you already know in this wiki?"
3. WRITE source page → wiki/sources/[slug].md
4. IDENTIFY which existing pages need updating:
   - Read wiki/index.md to find candidate pages
   - Open and read each candidate page
5. UPDATE entity and concept pages (add new facts, note contradictions, update source_count)
6. UPDATE wiki/overview.md if the source shifts the overall thesis
7. UPDATE wiki/index.md (add new source page; update modified pages' summaries if changed)
8. APPEND to wiki/log.md:
   ## [YYYY-MM-DD] ingest | [Source Title]
   - Pages created: [list]
   - Pages updated: [list]
   - Key contradictions found: [list or "none"]
   - Open questions raised: [list]
```

**Do not skip step 2.** The discussion is where I direct the analysis.

### 5.2 Query Workflow

When I ask a question:

```
1. READ wiki/index.md to identify relevant pages.
2. READ the relevant pages (entities + concepts + sources).
3. SYNTHESIZE an answer with citations to wiki pages.
4. ASK: "Should I save this analysis as a wiki page?"
5. If yes → WRITE to wiki/analyses/[slug].md
6. APPEND to wiki/log.md:
   ## [YYYY-MM-DD] query | [Question Summary]
   - Pages consulted: [list]
   - Filed as analysis: yes/no → [[analysis-page]] or "no"
```

### 5.3 Lint Workflow

When I say "lint the wiki":

```
1. READ wiki/index.md completely.
2. For each page, check:
   a. Stub pages that haven't been updated in > 2 ingests
   b. Cross-references pointing to non-existent pages
   c. Pages with source_count=1 that might be mergeable
   d. Concepts mentioned in multiple pages but lacking their own page
   e. Contradictions flagged with ⚡ that haven't been resolved
3. PRODUCE a lint report:
   - Orphan pages (no inbound links)
   - Missing pages (referenced but don't exist)
   - Stale stubs
   - Unresolved contradictions
   - Suggested new pages
   - Suggested merges
4. WAIT for my instructions before making changes.
5. APPEND to wiki/log.md:
   ## [YYYY-MM-DD] lint | Lint Pass
   - Issues found: [count]
   - [summary of key issues]
```

---

## 6. The Overview Page

`wiki/overview.md` is the wiki's thesis statement. It should:
- Summarize the current state of knowledge on the topic in 3-5 paragraphs
- Link to the most important entity and concept pages
- State the **main open questions** we haven't resolved
- Note major **tensions** between sources or between ideas

Update overview.md:
- After every 5th ingest
- When a source fundamentally shifts the thesis
- When a lint pass resolves major contradictions

The overview is a living document. Treat it like a paper abstract that gets rewritten as the research matures.

---

## 7. Session Protocol

At the start of every new session:

```
1. READ CLAUDE.md (this file) — re-orient to the schema.
2. READ wiki/log.md (last 10 entries) — what was done recently?
3. READ wiki/overview.md — what is the current thesis?
4. GREET the user with:
   - A 2-sentence summary of where the wiki stands
   - The 2-3 most recent activities from the log
   - Any unresolved open questions flagged in the overview
   - "What would you like to do? [ingest / query / lint / explore]"
```

This ensures continuity across sessions without requiring me to re-explain context.

---

## 8. Quality Standards

### Do
- Be precise. Vague claims ("important", "significant") without evidence get flagged ❓.
- Preserve nuance. If a source is uncertain about something, the wiki page must reflect that.
- Date everything. Facts decay; knowing when something was written matters.
- Show your sources. Every factual claim on an entity/concept page should cite a `[[source]]`.

### Don't
- Don't synthesize beyond what the sources support. Flag it as ❓ speculation.
- Don't delete content when updating — add `~~strikethrough~~` and note why it's superseded.
- Don't create duplicate pages. Search the index before creating new pages.
- Don't let the overview drift into cheerleading. It must reflect tensions honestly.

---

## 9. Schema Evolution

This schema will change as the wiki matures. When we agree to change a convention:
1. Update this file.
2. Append to the log: `## [YYYY-MM-DD] schema | [What changed and why]`
3. Backfill the change across existing pages if feasible.

The schema is not sacred. It serves the wiki, not the other way around.
