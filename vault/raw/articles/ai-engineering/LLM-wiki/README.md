# Raw Sources — Contribution Guide

> **This directory is read-only for the LLM.**
> The LLM reads sources here; it never writes, renames, or modifies them.
> Only the human (you) adds or removes files from this directory.

---

## What Goes Here

Any source material you want the LLM to ingest into the wiki:
- Articles (clipped as markdown via Obsidian Web Clipper)
- PDFs (research papers, reports)
- Images (screenshots, diagrams, charts)
- Transcript text (podcast transcripts, interview transcripts)
- Data files (CSV, JSON — for the LLM to read and summarize)
- Your own notes (meeting notes, highlights, margin notes)

## What Doesn't Go Here

- Pages you've already ingested and don't need to revisit
- Bookmarks or links without content (fetch the content first)
- Duplicate sources (check `wiki/sources/` first)

---

## File Naming Convention

```
[author-lastname]-[keyword]-[YYYY].md          # articles / papers
[publication]-[topic]-[YYYY-MM-DD].md          # news articles
[title-slug].pdf                               # PDFs
transcript-[source]-[YYYY-MM-DD].md            # transcripts
notes-[topic]-[YYYY-MM-DD].md                 # your own notes
data-[dataset-name]-[YYYY].csv                # data files
```

Examples:
```
silver-reinforcement-learning-overview-2017.md
nytimes-openai-valuation-2025-03-15.md
transcript-lex-fridman-hinton-2024-11-01.md
notes-reading-group-attention-2024-09-10.md
data-model-benchmark-leaderboard-2025-03.csv
```

---

## Adding a Source

### Step 1: Get the content as a file

**For web articles**: Use [Obsidian Web Clipper](https://obsidian.md/clipper) 
to convert to markdown. Then optionally download images locally:
`Settings → Hotkeys → "Download attachments for current file"`.

**For PDFs**: Drop the PDF directly into `raw/`. 
The LLM can read text-based PDFs natively. For scanned PDFs, 
run OCR first (e.g. `ocrmypdf input.pdf output.pdf`).

**For podcasts/videos**: Get a transcript first.
Free options: `yt-dlp + whisper` for YouTube; Descript; Otter.ai.

### Step 2: Tell the LLM to ingest it

```
"Please ingest raw/[filename]"
```

The LLM will follow the ingest workflow in CLAUDE.md §5.1.

---

## Source Quality Guidelines

Before adding a source, ask yourself:
1. **Is this primary?** Prefer original sources over summaries of summaries.
2. **Is this dated?** Always know when something was written.
3. **Is this already in the wiki?** Check `wiki/index.md → Sources` first.
4. **Does this add something new?** Redundant confirmation has value, but flag it.

---

## Current Source Inventory

*(The LLM maintains this table automatically — do not edit manually)*

| Filename | Type | Added | Ingested |
|----------|------|-------|----------|
| *(empty)* | | | |

---

## Assets

`raw/assets/` stores locally downloaded images referenced by source files.

Image naming: `[source-slug]-fig-[N].[ext]`
Example: `silver-2017-fig-1.png`
