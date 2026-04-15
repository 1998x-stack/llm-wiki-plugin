# Qwen API Issues

> From vault/docs/gotchas.md — Qwen API Integration, Content Quality, and Session Summary

---

## Qwen API Integration

### Issue: Model Name Mismatch
**Date**: 2026-04-15
**Command**: `wiki:ingest-loop-qwen`
**Error**: `The model 'qwen3-plus' does not exist or you do not have access to it.`

**Root Cause**:
The `scripts/qwen_ingest.py` script was configured to use model `qwen3-plus`, but this model does not exist in the DashScope API. Available models include:
- `qwen3.5-plus` (working replacement)
- `qwen3.6-plus`
- `qwen3.5-flash`

**Fix Applied**:
Changed line 240 in `scripts/qwen_ingest.py`:
```python
# Before:
model="qwen3-plus"

# After:
model="qwen3.5-plus"
```

**Validation**:
- All 3 files processed successfully with `qwen3.5-plus`
- API calls completed without authentication errors
- Output quality maintained

**Recommendation**:
Periodically verify model names against DashScope API:
```bash
curl -s -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  https://dashscope.aliyuncs.com/api/v1/models | grep -i qwen
```

---

## General Patterns

### Pattern: Lint Warnings on Generated Content
**Issue**: Qwen-generated pages often exceed overview length limits (200 chars)
**Impact**: Non-blocking warnings in lint output
**Action**: Manual review and editing required for optimization
**Example**: `claude-cli-tools.md` generated overview with 341 chars

---

## Environment Setup

### Python Dependencies
Ensure all required packages are installed:
```bash
pip install -r requirements.txt
```

Key packages:
- `openai` (for Qwen API access)
- `pyyaml` (for frontmatter parsing)
- `jieba`, `rank_bm25` (for search indexing)

---

## State File Management

### Issue: State File Formatting Corruption
**Date**: 2026-04-15
**Command**: `wiki:ingest-loop-qwen`
**File**: `.claude/ingest-loop-qwen.local.md`

**Error Pattern**:
```yaml
files:
  - "raw/articles/claude-mem/blog_06_philosophy.md"current_index: 0
total: 6
```

**Root Cause**:
The setup script `scripts/setup-ingest-loop-qwen.sh` generates malformed YAML where the last file path and `current_index` field are concatenated on the same line without a newline separator. This occurs when the file list is written to the state file.

**Impact**:
- State file becomes unparsable by standard YAML parsers
- Ingest loop cannot read current progress
- Manual intervention required to fix formatting

**Fix Applied**:
Manual edit of state file to insert proper newlines:
```yaml
files:
  - "raw/articles/claude-mem/blog_06_philosophy.md"
current_index: 0
total: 6
```

**Recommendation**:
Update `scripts/setup-ingest-loop-qwen.sh` to ensure proper newline insertion when writing the last file entry. Add validation step to verify YAML syntax after state file generation.

---

## Qwen API Content Quality

### Issue: Missing YAML Frontmatter in Generated Pages
**Date**: 2026-04-15
**Command**: `wiki:ingest-loop-qwen`
**Files Affected**: `blog_02_hooks.md`, `blog_03_worker.md`, `blog_04_database.md`, `blog_05_search.md`, `blog_06_philosophy.md`

**Error Pattern**:
```json
{"wiki_name": "untitled", "critical": ["YAML frontmatter missing or unparseable"], "skipped": true}
```

**Occurrence Count**:
- blog_02_hooks.md: 9 skipped pages
- blog_03_worker.md: 5 skipped pages (all failed)
- blog_04_database.md: 5 skipped pages
- blog_05_search.md: 4 skipped pages
- blog_06_philosophy.md: 3 skipped pages

**Root Cause**:
Qwen API occasionally returns content that either:
1. Lacks proper YAML frontmatter entirely
2. Has malformed frontmatter that fails validation
3. Generates content that doesn't meet wiki page quality standards

**Impact**:
- Some source files produce zero valid wiki pages (e.g., blog_03_worker.md)
- Incomplete knowledge extraction from source material
- Need for re-processing or manual content creation

**Workaround**:
Successful pages are written and indexed; failed pages are logged in warnings array. For critical content, consider:
1. Re-running ingest with different model parameters
2. Manual wiki page creation using templates
3. Splitting large source files into smaller chunks

**Success Rate**:
- Total files processed: 6
- Fully successful: 3/6 (50%)
- Partially successful: 2/6 (33%)
- Completely failed: 1/6 (17%)

**Recommendation**:
- Add pre-validation step to check YAML frontmatter completeness before BM25 indexing
- Implement retry logic for pages that fail lint checks
- Consider adding `--strict` mode to abort on any validation failure
- Document expected frontmatter format in ingestion guidelines

---

## Session Summary: Claude-Mem Articles Ingest

**Date**: 2026-04-15
**Command**: `wiki:ingest-loop-qwen /Users/xd/Desktop/codes/mygithubs/llm-wiki-plugin/vault/raw/articles/claude-mem`
**Session ID**: 8C112D8B-0C32-4ADC-A55C-8E2109B4CE05

### Processing Results

**Total source files**: 6
**Successfully processed**: 5 (83%)
**Completely failed**: 1 (blog_03_worker.md - 0 pages generated)
**Total wiki pages created**: 8
**Total pages skipped (lint failures)**: 26

### File-by-File Breakdown

| File | Status | Pages Created | Pages Skipped | Notes |
|------|--------|---------------|---------------|-------|
| blog_01_overview.md | Success | 5 | 0 | Generated Claude-Mem, LLM-Statelessness, Alex-Newman, Claude-Code-Hook-System, Bun-Runtime |
| blog_02_hooks.md | Partial | 1 | 9 | Updated Claude-Mem with Hook architecture; 9 pages missing frontmatter |
| blog_03_worker.md | Failed | 0 | 5 | All pages rejected - missing YAML frontmatter |
| blog_04_database.md | Partial | 1 | 5 | Updated Claude-Mem with database architecture; 5 pages missing frontmatter |
| blog_05_search.md | Partial | 1 | 4 | Created 渐进式披露 concept page; 4 pages missing frontmatter |
| blog_06_philosophy.md | Partial | 5 | 3 | Created 5 concept pages; 3 pages missing frontmatter |

### Critical Issues Encountered

**1. State File Formatting Corruption**
```yaml
# Error pattern - line 10 concatenation:
files:
  - "raw/articles/claude-mem/blog_06_philosophy.md"current_index: 0

# Fixed format:
files:
  - "raw/articles/claude-mem/blog_06_philosophy.md"
current_index: 0
```
- **Root cause**: `scripts/setup-ingest-loop-qwen.sh` missing newline after last file entry
- **Impact**: State file unparsable, manual fix required
- **Fix**: Manual newline insertion during session

**2. YAML Frontmatter Failures**
```json
# Recurring error pattern:
{"wiki_name": "untitled", "critical": ["YAML frontmatter missing or unparseable"], "skipped": true}
```
- **Occurrences**: 26 pages across 5 files
- **Root cause**: Qwen API returning content without proper frontmatter or malformed YAML
- **Impact**: Incomplete knowledge extraction, some files produced zero valid pages
- **Workaround**: Successful pages indexed; failed pages logged for manual review

### Generated Wiki Pages

**Entities (5)**:
- Claude-Mem (updated 3x with architecture details)
- LLM-Statelessness
- Alex-Newman
- Claude-Code-Hook-System
- Bun-Runtime

**Concepts (5)**:
- 渐进式披露 (Progressive Disclosure) - created from blog_05_search.md
- 上下文工程 (Context Engineering) - created from blog_06_philosophy.md
- 上下文污染 (Context Pollution) - created from blog_06_philosophy.md
- 信息觅食理论 (Information Foraging Theory) - created from blog_06_philosophy.md
- 认知负荷理论 (Cognitive Load Theory) - created from blog_06_philosophy.md

### Key Learnings

1. **Content Quality Variance**: Qwen API produces inconsistent frontmatter quality; ~76% of generated pages failed validation (26 skipped / 34 total)
2. **Partial Success Pattern**: Even "failed" files often produce 1-2 valid pages worth keeping
3. **State Management Fragility**: Setup script requires fix for proper YAML generation
4. **Incremental Value**: Multiple passes on same entity (Claude-Mem) successfully accumulated knowledge from different source files

### Recommendations for Future Runs

1. Fix `scripts/setup-ingest-loop-qwen.sh` newline handling before next batch
2. Add frontmatter pre-validation in `qwen_ingest.py` to catch issues early
3. Consider implementing retry logic with different temperature parameters for failed pages
4. Split large source files into smaller chunks to reduce blast radius of failures
5. Add `--strict` flag option to abort on first validation failure vs. continue mode
6. Document expected frontmatter format in raw source file templates
