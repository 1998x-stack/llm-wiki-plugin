# Page Templates

> Copy-paste these when creating new pages. 
> Delete sections marked "(optional)" if not applicable.
> Replace all `[FILL]` markers with content.
> Never leave `[FILL]` in a published page — use `stub` status instead.

---

## Template: Entity Page

**Filename convention**: `wiki/entities/[entity-name-kebab-case].md`

```markdown
---
title: "[Entity Name]"
type: entity
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: N
status: stub
entity_type: person | company | product | place | event | dataset | paper
---

# [Entity Name]

**Type:** Person | Company | Product | Place | Event
**Also known as:** [aliases, abbreviations — or delete line]

## Summary
[2-3 sentences. What is this? Why does it matter in the context of this wiki's topic?
Write for someone who has never heard of it.]

## Key Facts

| Attribute | Value |
|-----------|-------|
| [key] | [value] |

(For people: Founded/Born, Role, Affiliation, Active period)
(For companies: Founded, HQ, Size, Domain)
(For products: Released, Creator, Type, Status)

## Role in [Wiki Topic]
[What does this entity do, make, or represent in our specific research domain?
This is the most important section — make it specific, not generic.]

## Claims & Positions (optional)
[If this entity makes claims relevant to our topic, list them with sources.]
- Claims that [X] because [Y] — [[source-a]]
- Argues against [Z] — [[source-b]]

## Timeline (optional)
[For entities with important historical arcs]
- `YYYY-MM-DD` — [event]
- `YYYY-MM-DD` — [event]

## Connections
[Link to related pages. Every link must have a one-line annotation.]
- Related to [[entity-b]] — [how they are related]
- Exemplifies [[concept-x]] — [how this entity instantiates the concept]
- Contrasts with [[entity-c]] — [key difference]

## Sources
[Every source that contributed information to this page]
- [[source-a]] — [what this source says about this entity, 1 sentence]
- [[source-b]] — [what this source says, 1 sentence]

## Open Questions
[What do we not know about this entity that matters for the wiki's topic?]
- ❓ [Question]
```

---

## Template: Concept Page

**Filename convention**: `wiki/concepts/[concept-name-kebab-case].md`

```markdown
---
title: "[Concept Name]"
type: concept
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: N
status: stub
---

# [Concept Name]

## Definition
[1-2 sentences. Precise. If this is a term of art, define it as it is used in this wiki.
Note if our usage differs from common usage.]

## Why It Matters (in this wiki's context)
[Not a generic textbook explanation. Why does THIS wiki, on THIS topic, care about this concept?
What explanatory work does it do?]

## Mechanism / How It Works
[The actual explanation. Use Mermaid diagrams, tables, or step-by-step breakdowns if helpful.]

\`\`\`mermaid
graph LR
  A --> B --> C
\`\`\`

## Variants & Subtypes (optional)
[If the concept has named variants or subtypes that appear in sources, list them here.]
- **[Variant A]** — [how it differs from the base concept]
- **[Variant B]** — [how it differs]

## Instantiations
[Which entities in this wiki exemplify or implement this concept?]
- [[entity-a]] — [how it instantiates this concept]
- [[entity-b]] — [how it instantiates this concept]

## Tensions
[Where does this concept conflict with other concepts in the wiki?
Where do sources disagree about this concept?]
- ⚡ Tension with [[concept-y]]: [description of conflict]

## Historical Context (optional)
[When did this concept emerge? Who coined it? How has it evolved?]

## Sources
[Sources that define, use, or discuss this concept]
- [[source-a]] — [how this source uses or discusses the concept]
- [[source-b]] — [how]
```

---

## Template: Source Page

**Filename convention**: `wiki/sources/[author-keyword-year].md` or `[title-slug].md`

```markdown
---
title: "[Full Source Title]"
type: source
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: 1
status: active
raw_file: raw/[filename]
author: "[Author Name(s)]"
published: YYYY-MM-DD
domain: "[domain.com or 'book' or 'podcast']"
word_count_approx: N
---

# [Full Source Title]

**Author:** [name] | **Published:** YYYY-MM-DD | **Domain:** [domain]
**Ingested:** YYYY-MM-DD | **Raw file:** `raw/[filename]`

---

## TL;DR
[1 paragraph. What is this source? What is its single most important claim or contribution?
Who is the intended audience? What is the author's apparent agenda or perspective?]

## Key Claims
[Bulleted list of factual assertions. Each is a claim, not a topic heading.
Be specific: "X is Y" not "discusses X". Include confidence signals from the author.]
- [Claim 1]
- [Claim 2]
- [Claim 3]

## Evidence & Data
[Tables, statistics, named studies, quoted evidence. Keep direct quotes < 15 words.]

| Finding | Value | Context |
|---------|-------|---------|
| [metric] | [value] | [where/when] |

## Methodology (optional — for academic/research sources)
[How was this data collected? What are the limitations?]

## Author's Perspective & Potential Bias
[What is the author's background? Any institutional affiliation, financial interest,
or ideological lens that might color the claims?]

## Tensions & Contradictions
[Does this source contradict anything in the wiki?]
- ⚡ Contradicts [[page]] on [specific claim] — [brief explanation]
- Consistent with [[page]] on [claim] ✓

## Wiki Impact
[Which existing pages were updated because of this source?]
- Updated [[entity-a]]: [what was added/changed]
- Informed [[concept-b]]: [what was added]
- Created [[entity-c]]: [why a new page was needed]

## Raw Excerpts
[2-5 verbatim excerpts too important to paraphrase. Max 50 words each. Quote sparingly.]

> "[Excerpt 1]" (p. N / para. N)

> "[Excerpt 2]"

## Open Questions Raised
[Questions this source raises but does not answer]
- ❓ [Question 1]
- ❓ [Question 2]
```

---

## Template: Analysis Page

**Filename convention**: `wiki/analyses/[question-slug]-[YYYY-MM-DD].md`

```markdown
---
title: "Analysis: [Short question or theme]"
type: analysis
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_count: N
status: active
question: "[Full verbatim question that prompted this analysis]"
---

# Analysis: [Title]

**Question:** [Full verbatim question]
**Date:** YYYY-MM-DD
**Prompted by:** [what triggered this — user question, lint finding, etc.]
**Sources consulted:** [[s1]], [[s2]], [[s3]]
**Confidence:** high | medium | low

---

## Answer

[Direct answer to the question in 1-3 paragraphs. Lead with the conclusion.
Cite wiki pages throughout.]

## Supporting Evidence

[Structured argument from wiki content.]

### Evidence For
- [Point 1] — [[source-a]]
- [Point 2] — [[source-b]]

### Evidence Against / Caveats
- [Counterpoint 1] — [[source-c]]
- [Caveat] — [[concept-x]]

## Comparison Table (optional — for "A vs B" questions)

| Dimension | [[entity-a]] | [[entity-b]] |
|-----------|-------------|-------------|
| [dim 1]   | [value]     | [value]     |
| [dim 2]   | [value]     | [value]     |

## Implications for the Wiki

[What does this analysis mean for the overall thesis? Does it update overview.md?
Does it resolve any contradiction in the registry?]

## Follow-up Questions

[What should be investigated next?]
- ❓ [Follow-up 1]
- ❓ [Follow-up 2]
```
