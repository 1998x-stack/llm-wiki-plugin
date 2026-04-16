# Wiki Guidelines 虚拟分区 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `guidelines/` directory with per-topic guideline files derived from `topic-to-wiki.json`, slim down `index.md` to a summary table + global name list, and update commands/scripts to load context per-topic instead of globally.

**Architecture:** `topic-to-wiki.json` remains source of truth. A new `build_guidelines.py` script generates `guidelines/*.md` from it. `snapshot_index.py` gains a `--slim` mode for the compact index. Commands (`ingest`, `ingest-loop`, `query`) are updated to read guidelines instead of full index. `wiki:reindex` and `wiki:maintain` are updated to include guideline generation.

**Tech Stack:** Python 3.10+, pyyaml, existing wiki_utils.py infrastructure

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `scripts/wiki_utils.py` | Modify | Add `GUIDELINES_DIR` constant |
| `scripts/build_guidelines.py` | Create | Generate `guidelines/*.md` from `topic-to-wiki.json` + wiki pages |
| `scripts/snapshot_index.py` | Modify | Add `--slim` mode to output compact index.md |
| `scripts/build_ingest_context.py` | Modify | Add `--topic` filter for per-topic existing_pages |
| `.claude/commands/wiki/reindex.md` | Modify | Add guideline generation step after maps |
| `.claude/commands/wiki/ingest.md` | Modify | Use guidelines for dedup instead of full index |
| `.claude/commands/wiki/ingest-loop.md` | Modify | Pass `--topic` to build_ingest_context |
| `.claude/commands/wiki/query.md` | Modify | Load guidelines instead of full index |
| `.claude/commands/wiki/check.md` | Modify | Add guideline consistency check |
| `.claude/commands/wiki/maintain.md` | Modify | Include guideline generation in reindex step |
| `CLAUDE.md` (vault) | Modify | Document `guidelines/` directory |
| `_schema/CLAUDE.md` | Modify | Document guideline format and generation |

---

### Task 1: Add GUIDELINES_DIR constant to wiki_utils.py

**Files:**
- Modify: `scripts/wiki_utils.py:28-32`

- [ ] **Step 1: Add the constant**

In `scripts/wiki_utils.py`, after line 28 (`MAPS_DIR = VAULT_DIR / "maps"`), add:

```python
GUIDELINES_DIR = VAULT_DIR / "guidelines"
```

- [ ] **Step 2: Verify import works**

Run:
```bash
cd /Users/mx/Desktop/series/核心项目系列/llm-wiki/vault && python3 -c "from scripts.wiki_utils import GUIDELINES_DIR; print(GUIDELINES_DIR)"
```

Expected: prints the path ending in `/vault/guidelines`

- [ ] **Step 3: Commit**

```bash
git add scripts/wiki_utils.py
git commit -m "feat: add GUIDELINES_DIR constant to wiki_utils"
```

---

### Task 2: Create build_guidelines.py

**Files:**
- Create: `scripts/build_guidelines.py`

This script reads `topic-to-wiki.json` (or `maps/tmp.snapshot.json` as fallback) and wiki page frontmatter to generate `guidelines/*.md` files.

- [ ] **Step 1: Write build_guidelines.py**

```python
#!/usr/bin/env python3
"""Generate per-topic guideline files from topic-to-wiki.json.

Each guideline contains a topic overview + page list, optimized for
LLM prompt consumption (compact, low token count).

Usage:
    python3 scripts/build_guidelines.py              # generate all guidelines
    python3 scripts/build_guidelines.py --topic AI   # generate one topic
    python3 scripts/build_guidelines.py --json        # output stats as JSON
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from wiki_utils import VAULT_DIR, WIKI_DIR, GUIDELINES_DIR, parse_frontmatter

TOPIC_MAP_PATH = VAULT_DIR / ".claude" / "topic-to-wiki.json"
SNAPSHOT_PATH = VAULT_DIR / "maps" / "tmp.snapshot.json"


def load_topic_mapping() -> dict[str, list[str]]:
    """Load topic -> [page_names] from topic-to-wiki.json or snapshot fallback."""
    if TOPIC_MAP_PATH.exists():
        data = json.loads(TOPIC_MAP_PATH.read_text(encoding="utf-8"))
        return data.get("topics", {})

    # Fallback: build from tmp.snapshot.json
    if SNAPSHOT_PATH.exists():
        data = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        topics: dict[str, list[str]] = {}
        for page_path, info in data.get("pages", {}).items():
            cluster = info.get("cluster", "其他")
            title = info.get("title", Path(page_path).stem)
            topics.setdefault(cluster, []).append(title)
        return topics

    return {}


def read_page_info(name: str) -> dict | None:
    """Read frontmatter + overview for a wiki page by stem name."""
    for subdir in ["concepts", "entities", "syntheses", "qa-insights"]:
        fp = WIKI_DIR / subdir / f"{name}.md"
        if fp.exists():
            text = fp.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            if fm is None:
                continue
            # Extract overview (first meaningful line after frontmatter)
            overview = ""
            m = re.search(r"## 概述\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
            if m:
                overview = m.group(1).strip().split("\n")[0][:80]
            elif body.strip():
                for line in body.split("\n"):
                    if line.startswith("# "):
                        continue
                    if line.strip():
                        overview = line.strip()[:80]
                        break
            return {
                "name": name,
                "type": fm.get("type", "unknown"),
                "confidence": fm.get("confidence"),
                "overview": overview,
                "subdir": subdir,
            }
    return None


def generate_guideline(topic: str, page_names: list[str]) -> str:
    """Generate guideline markdown for one topic."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Collect page info
    pages = []
    for name in sorted(page_names):
        info = read_page_info(name)
        if info:
            pages.append(info)

    concepts = [p for p in pages if p["type"] == "concept"]
    entities = [p for p in pages if p["type"] == "entity"]
    syntheses = [p for p in pages if p["type"] == "synthesis"]
    qa_insights = [p for p in pages if p["type"] == "qa-insight"]

    total = len(pages)

    # Build overview from top concepts (first 4 concept names)
    top_names = [p["name"] for p in concepts[:4]]
    overview_hint = "、".join(top_names) if top_names else topic

    lines = [
        "---",
        "type: guideline",
        f'topic: "{topic}"',
        f"page_count: {total}",
        f"updated: {today}",
        "---",
        "",
        f"## 概述",
        "",
        f"{topic} 相关概念与实体的集群。核心主题：{overview_hint}。",
        "",
    ]

    def add_section(title: str, items: list[dict]):
        if not items:
            return
        lines.append(f"## {title} ({len(items)})")
        lines.append("")
        for p in items:
            conf = f" ({p['confidence']})" if p["confidence"] else ""
            ov = f" — {p['overview']}" if p["overview"] else ""
            lines.append(f"- [[{p['name']}]]{ov}{conf}")
        lines.append("")

    add_section("概念", concepts)
    add_section("实体", entities)
    add_section("综合分析", syntheses)
    add_section("QA 洞见", qa_insights)

    return "\n".join(lines)


def build(topics_filter: list[str] | None = None, as_json: bool = False):
    """Generate guideline files."""
    topic_map = load_topic_mapping()
    if not topic_map:
        msg = "No topic mapping found (need .claude/topic-to-wiki.json or maps/tmp.snapshot.json)"
        if as_json:
            print(json.dumps({"status": "error", "message": msg}))
        else:
            print(f"ERROR: {msg}")
        return

    # Filter topics if requested
    if topics_filter:
        topic_map = {k: v for k, v in topic_map.items() if k in topics_filter}

    # Ensure guidelines dir exists
    GUIDELINES_DIR.mkdir(parents=True, exist_ok=True)

    # If no filter, clean out old guidelines first
    if not topics_filter:
        for old in GUIDELINES_DIR.glob("*.md"):
            old.unlink()

    generated = {}
    for topic, page_names in sorted(topic_map.items()):
        content = generate_guideline(topic, page_names)
        out_path = GUIDELINES_DIR / f"{topic}.md"
        out_path.write_text(content, encoding="utf-8")
        generated[topic] = len(page_names)

    if as_json:
        print(json.dumps({
            "status": "ok",
            "guidelines_dir": str(GUIDELINES_DIR),
            "topics": generated,
            "total_topics": len(generated),
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Generated {len(generated)} guidelines in {GUIDELINES_DIR}/")
        for topic, count in sorted(generated.items()):
            print(f"  {topic}: {count} pages")


def main():
    parser = argparse.ArgumentParser(description="Generate per-topic guideline files")
    parser.add_argument("--topic", type=str, help="Generate only for specific topic(s), comma-separated")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    topics_filter = args.topic.split(",") if args.topic else None
    build(topics_filter=topics_filter, as_json=args.json)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test the script**

Run:
```bash
cd /Users/mx/Desktop/series/核心项目系列/llm-wiki/vault && python3 scripts/build_guidelines.py --json
```

Expected: JSON output with `status: "ok"`, lists of topics with page counts. `guidelines/` directory created with per-topic `.md` files.

- [ ] **Step 3: Verify a generated guideline looks correct**

Run:
```bash
head -20 guidelines/AI.md
```

Expected: frontmatter with `type: guideline`, `topic: "AI"`, page_count, followed by `## 概述` and `## 概念 (N)` sections.

- [ ] **Step 4: Register in wiki.sh**

Check if `wiki.sh` auto-discovers scripts or needs explicit registration. If needed, the script is already in `scripts/` and follows the naming convention, so `bash scripts/wiki.sh build_guidelines` should work (wiki.sh uses the script name as the subcommand).

Run:
```bash
bash scripts/wiki.sh build_guidelines --json
```

Expected: same output as step 2.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_guidelines.py guidelines/
git commit -m "feat: add build_guidelines.py — per-topic guideline generation"
```

---

### Task 3: Add --slim mode to snapshot_index.py

**Files:**
- Modify: `scripts/snapshot_index.py`

Add a `--slim` flag that rewrites `index.md` as a compact summary table + global name list instead of the full 450-line listing.

- [ ] **Step 1: Add the slim_index function**

Add this function after `save_snapshot()` (before `main()`):

```python
def slim_index(pages):
    """Rewrite index.md as compact summary table + global name list."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Load topic mapping for stats
    topic_map_path = VAULT_DIR / ".claude" / "topic-to-wiki.json"
    snapshot_path = VAULT_DIR / "maps" / "tmp.snapshot.json"

    # Build page→topic mapping
    page_topic = {}
    if topic_map_path.exists():
        data = json.loads(topic_map_path.read_text(encoding="utf-8"))
        for topic, names in data.get("topics", {}).items():
            for name in names:
                page_topic[name] = topic
    elif snapshot_path.exists():
        data = json.loads(snapshot_path.read_text(encoding="utf-8"))
        for path_str, info in data.get("pages", {}).items():
            page_topic[Path(path_str).stem] = info.get("cluster", "其他")

    # Count by topic and type
    topic_stats = {}  # topic -> {concept: N, entity: N, ...}
    for name, info in pages.items():
        topic = page_topic.get(name, "其他")
        if topic not in topic_stats:
            topic_stats[topic] = {"concept": 0, "entity": 0, "other": 0}
        t = info["type"]
        if t in ("concept", "entity"):
            topic_stats[topic][t] += 1
        else:
            topic_stats[topic]["other"] += 1

    # Global counts
    entity_count = sum(1 for p in pages.values() if p["type"] == "entity")
    concept_count = sum(1 for p in pages.values() if p["type"] == "concept")
    synthesis_count = sum(1 for p in pages.values() if p["type"] == "synthesis")
    qa_count = sum(1 for p in pages.values() if p["type"] == "qa-insight")
    total = len(pages)

    # Build table rows (sorted by total desc, 其他 last)
    rows = []
    for topic, stats in sorted(topic_stats.items(), key=lambda x: (x[0] == "其他", -sum(x[1].values()))):
        t_total = sum(stats.values())
        rows.append(f"| {topic} | {stats['concept']} | {stats['entity']} | {t_total} | [[guidelines/{topic}]] |")

    # Build global name list (comma-separated, sorted)
    all_names = ", ".join(sorted(pages.keys()))

    lines = [
        "---",
        "type: index",
        f"updated: {today}",
        "---",
        "",
        "# 知识库目录",
        "",
        "> 本文件由 LLM 自动维护。详细清单见各 `guidelines/*.md`。",
        "",
        "## 统计",
        "",
        "| 主题 | 概念 | 实体 | 合计 | guideline |",
        "|------|------|------|------|-----------|",
    ]
    lines.extend(rows)
    lines.extend([
        "",
        f"总计: {total} 页 ({concept_count} 概念, {entity_count} 实体, {synthesis_count} 综合, {qa_count} QA)",
        "",
        "## 全部页面",
        "",
        all_names,
        "",
    ])

    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "status": "slim",
        "total": total,
        "topics": len(topic_stats),
        "index_lines": len(lines),
    }, ensure_ascii=False, indent=2))
```

- [ ] **Step 2: Add --slim to argparse in main()**

Update the `main()` function to add the flag and call it:

```python
def main():
    parser = argparse.ArgumentParser(description="Index integrity checker")
    parser.add_argument("--update", action="store_true", help="Add missing entries to index.md")
    parser.add_argument("--snapshot", action="store_true", help="Save snapshot JSON")
    parser.add_argument("--slim", action="store_true", help="Rewrite index.md as compact summary")
    args = parser.parse_args()

    pages = scan_wiki()
    indexed = parse_index()

    if args.slim:
        slim_index(pages)
        return

    if args.snapshot:
        save_snapshot(pages)
        return

    if args.update:
        update_index(pages, indexed)
        return

    # Default: check mode
    result = check(pages, indexed)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

- [ ] **Step 3: Test --slim**

Run:
```bash
cd /Users/mx/Desktop/series/核心项目系列/llm-wiki/vault && python3 scripts/snapshot_index.py --slim
```

Expected: JSON output with `status: "slim"`, index_lines ~20. Check the actual file:

```bash
wc -l index.md
```

Expected: ~20-30 lines instead of ~450.

**Important:** After testing, restore the original index.md before committing (the slim mode will be used only when explicitly called during reindex):

```bash
git checkout -- index.md
```

- [ ] **Step 4: Commit**

```bash
git add scripts/snapshot_index.py
git commit -m "feat: add --slim mode to snapshot_index.py for compact index"
```

---

### Task 4: Add --topic filter to build_ingest_context.py

**Files:**
- Modify: `scripts/build_ingest_context.py`

Add `--topic` argument that filters `existing_pages` to only pages in the specified topic(s).

- [ ] **Step 1: Add topic filtering logic**

Replace the `build()` function and add `main()` with argparse:

```python
def load_topic_pages(topics: list[str]) -> set[str]:
    """Load page names for given topics from topic-to-wiki.json or snapshot."""
    topic_map_path = VAULT_DIR / ".claude" / "topic-to-wiki.json"
    snapshot_path = VAULT_DIR / "maps" / "tmp.snapshot.json"

    if topic_map_path.exists():
        data = json.loads(topic_map_path.read_text(encoding="utf-8"))
        result = set()
        for topic in topics:
            result.update(data.get("topics", {}).get(topic, []))
        return result

    if snapshot_path.exists():
        data = json.loads(snapshot_path.read_text(encoding="utf-8"))
        result = set()
        for path_str, info in data.get("pages", {}).items():
            if info.get("cluster") in topics:
                result.add(info.get("title", Path(path_str).stem))
        return result

    return set()


def build(topic_filter: list[str] | None = None):
    if not WIKI_DIR.exists():
        print(json.dumps({"error": "wiki/ directory not found"}))
        sys.exit(2)

    pages = scan_existing_pages()
    schema = build_compact_schema()
    template = build_template()

    # Apply topic filter
    if topic_filter:
        allowed = load_topic_pages(topic_filter)
        pages = [p for p in pages if p["name"] in allowed]

    # Stats
    entities = sum(1 for p in pages if p["type"] == "entity")
    concepts = sum(1 for p in pages if p["type"] == "concept")

    # Build page list string (compact: one line per page, no aliases to save tokens)
    page_lines = []
    for p in pages:
        page_lines.append(f"- {p['name']} [{p['type']}]")
    existing_pages_text = "\n".join(page_lines)

    output = {
        "status": "ok",
        "stats": {
            "total_pages": len(pages),
            "entities": entities,
            "concepts": concepts,
        },
        "existing_pages": existing_pages_text,
        "schema_compact": schema,
        "template": template,
    }

    if topic_filter:
        output["topic_filter"] = topic_filter

    print(json.dumps(output, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Build ingest context package")
    parser.add_argument("--topic", type=str, help="Filter to topic(s), comma-separated (e.g. 'AI,方法论')")
    args = parser.parse_args()

    topic_filter = args.topic.split(",") if args.topic else None
    build(topic_filter=topic_filter)


if __name__ == "__main__":
    main()
```

Note: the existing `build()` call at the bottom (`build()`) must be replaced by the `main()` entry point.

- [ ] **Step 2: Test without filter (backwards compatible)**

Run:
```bash
cd /Users/mx/Desktop/series/核心项目系列/llm-wiki/vault && python3 scripts/build_ingest_context.py | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['stats'])"
```

Expected: `total_pages` should be ~452 (all pages).

- [ ] **Step 3: Test with topic filter**

Run:
```bash
python3 scripts/build_ingest_context.py --topic AI | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['stats']); print('filter:', d.get('topic_filter'))"
```

Expected: `total_pages` ~72 (only AI pages), `filter: ['AI']`.

- [ ] **Step 4: Test wiki.sh wrapper**

Run:
```bash
bash scripts/wiki.sh build_ingest_context --topic AI | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['stats'])"
```

Expected: same as step 3.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_ingest_context.py
git commit -m "feat: add --topic filter to build_ingest_context.py"
```

---

### Task 5: Update wiki:reindex command to generate guidelines

**Files:**
- Modify: `.claude/commands/wiki/reindex.md`

Add a new step after step 5 (Generate maps) to generate guidelines, and add a final step to slim index.md.

- [ ] **Step 1: Add guideline generation step**

After the existing "### 5. 生成 maps/*.md" section, add a new section:

```markdown
### 6. 生成 guidelines/*.md

从 `.claude/topic-to-wiki.json` 生成面向 LLM prompt 的分主题 guideline 文件：

```bash
bash scripts/wiki.sh build_guidelines --json
```

解析 JSON 输出，记录生成的 topic 数量和各 topic 页面数。

guideline 文件格式：
- frontmatter: `type: guideline`, `topic`, `page_count`, `updated`
- 概述段 ≤100 字
- 按类型分 section（概念、实体、综合分析）
- 每条含 `[[双链]]`、概述、confidence

### 7. 精简 index.md

```bash
bash scripts/wiki.sh snapshot_index --slim
```

将 index.md 从完整清单重写为：
- 统计表（每个 topic 一行，含概念/实体/合计数和指向 guideline 的链接）
- 全局页面名称列表（逗号分隔，用于快速去重）
```

- [ ] **Step 2: Renumber subsequent sections**

The existing sections 6 ("同步 _schema/CLAUDE.md") and 7 ("清理 + 日志") become 8 and 9 respectively.

- [ ] **Step 3: Update the log format in the cleanup section**

Update the log entry template to include guideline info:

```markdown
## [YYYY-MM-DD HH:MM] reindex
- 完整性: OK (N 页面, 0 缺失, 0 孤条目)
- 主题分类 (subagent): T 个 topics → topic1(N1), topic2(N2), ... → .claude/topic-to-wiki.json
- Tags 修复: M 个页面补充了 tags
- Guidelines: G 个 guideline 文件生成 → guidelines/
- Index: 精简为 L 行（统计表 + 名称列表）
- Schema 同步: _schema/CLAUDE.md Topics 已更新（如有变化）
```

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/wiki/reindex.md
git commit -m "feat: add guideline generation + index slim to wiki:reindex"
```

---

### Task 6: Update wiki:ingest command to use guidelines

**Files:**
- Modify: `.claude/commands/wiki/ingest.md`

- [ ] **Step 1: Update step 3 (查找已有页面)**

Replace the current step 3 content:

```markdown
3. **查找已有页面**
   - 读取 `index.md` 的「全部页面」段落，快速检查提取的实体/概念是否已有对应 wiki 页面
   - 如需更多上下文（概述、confidence），读取对应主题的 `guidelines/*.md`
   - 如果 `guidelines/` 不存在或为空，回退到读取完整 `index.md`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/wiki/ingest.md
git commit -m "feat: wiki:ingest uses guidelines for dedup context"
```

---

### Task 7: Update wiki:ingest-loop command to use --topic

**Files:**
- Modify: `.claude/commands/wiki/ingest-loop.md`

- [ ] **Step 1: Update step 3 (构建上下文包) for claude engine**

Replace the claude engine section of step 3:

```markdown
3. **构建上下文包**

   - **claude 引擎**：构建一次性上下文包供所有子代理使用。
   
     首先判断源材料的主题（从文件夹路径或文件内容推断），然后按主题构建上下文包：
     ```
     Bash: bash scripts/wiki.sh build_ingest_context --topic <推断的主题>
     ```
     如果无法确定主题，不传 `--topic`（回退到全量模式）。
     
     解析 JSON 输出，提取：
     - `existing_pages` — 该主题的已有页面列表（用于去重）
     - `schema_compact` — 合并后的 schema 规则
     - `template` — wiki-page 模板
     - `stats` — 当前页面统计
     - `topic_filter` — 实际使用的主题过滤（如有）
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/wiki/ingest-loop.md
git commit -m "feat: wiki:ingest-loop uses --topic for context reduction"
```

---

### Task 8: Update wiki:query command to use guidelines

**Files:**
- Modify: `.claude/commands/wiki/query.md`

- [ ] **Step 1: Update step 2 (主题扩展)**

After the existing topic matching logic, add guideline loading:

```markdown
   - 若找到匹配 topic → 读取 `guidelines/{MATCHED_TOPIC}.md` 获取该主题的页面清单和概述，作为后续搜索的优先上下文
   - 若 `guidelines/` 不存在，回退到 `.claude/topic-to-wiki.json`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/wiki/query.md
git commit -m "feat: wiki:query loads guidelines for topic context"
```

---

### Task 9: Update wiki:check to verify guideline consistency

**Files:**
- Modify: `.claude/commands/wiki/check.md`

- [ ] **Step 1: Add check item J**

After check item I (模板合规性), add:

```markdown
   **J. Guideline 一致性**
   - 如果 `guidelines/` 目录存在：
     - 检查每个 guideline 的 `page_count` 是否与实际 wiki 页面数匹配
     - 检查 guideline 中列出的页面是否都存在于 wiki/ 中
     - 检查是否有 wiki 页面不属于任何 guideline（可能是 topic-to-wiki.json 缺失）
   - 如果 `guidelines/` 不存在 → 报告为 INFO（建议运行 wiki:reindex 生成）
   - 不一致 → 报告为 WARNING
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/wiki/check.md
git commit -m "feat: wiki:check adds guideline consistency check"
```

---

### Task 10: Update wiki:maintain to include guidelines in output

**Files:**
- Modify: `.claude/commands/wiki/maintain.md`

- [ ] **Step 1: Update step 2 (Reindex) description**

In the Reindex section, add guideline generation to the bullet list:

```markdown
- 生成 `guidelines/*.md` 分主题 guideline 文件
- 精简 `index.md` 为统计表 + 全局名称列表
```

- [ ] **Step 2: Update the summary report template**

In the summary template (step 6), update the Reindex section:

```markdown
[2/5] Reindex
  - 完整性: OK (N 页面)
  - 主题分类: K 个 cluster
  - Tags 修复: M 个页面
  - Guidelines: G 个 guideline 生成
  - Index: 精简为 L 行
  - Schema 同步: _schema/CLAUDE.md Topics 已更新 / 无变化
```

- [ ] **Step 3: Update the log.md template**

In step 7, update the log entry:

```markdown
- Reindex: OK (N 页面, K clusters, G guidelines) | Index: L 行 | Schema 同步: 已更新/无变化
```

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/wiki/maintain.md
git commit -m "feat: wiki:maintain includes guidelines in reindex step"
```

---

### Task 11: Update documentation (CLAUDE.md files)

**Files:**
- Modify: `CLAUDE.md` (vault)
- Modify: `_schema/CLAUDE.md`

- [ ] **Step 1: Update vault/CLAUDE.md directory table**

Add `guidelines/` to the Directory Purpose table:

```markdown
| `guidelines/` | 按主题的 LLM prompt 上下文分片（由 `build_guidelines.py` 从 `topic-to-wiki.json` 生成） |
```

- [ ] **Step 2: Update vault/CLAUDE.md Key Commands**

Add to the Key Commands section:

```markdown
- `wiki:reindex` — validate index.md integrity + generate topic maps + generate guidelines + slim index
```

- [ ] **Step 3: Update _schema/CLAUDE.md**

Add a "Guidelines 系统" section after the existing "Maps 系统" section:

```markdown
### Guidelines 系统

Guidelines 是面向 LLM prompt 的分主题上下文包，从 `topic-to-wiki.json` 派生：

- **位置**: `guidelines/*.md`（每个 topic 一个文件）
- **格式**: frontmatter (`type: guideline`) + 概述 + 分类型页面清单
- **消费者**: `wiki:ingest`（去重）、`wiki:query`（主题上下文）、`build_ingest_context.py`（子代理上下文）
- **生成**: `wiki:reindex` 步骤 6 自动生成，不手动编辑
- **与 maps 的区别**: maps 面向脚本（结构化、完整 confidence），guidelines 面向 LLM（紧凑、优化 token）
```

- [ ] **Step 4: Update root CLAUDE.md scripts table**

Add `build_guidelines.py` to the scripts table in the root `CLAUDE.md`:

```markdown
| `build_guidelines.py` | Per-topic guideline generator from topic-to-wiki.json | wiki_utils |
```

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md _schema/CLAUDE.md ../CLAUDE.md
git commit -m "docs: document guidelines system in CLAUDE.md and schema"
```

---

### Task 12: Integration test — run wiki:reindex and verify

This is the end-to-end verification task. Run the full reindex pipeline and verify all outputs.

- [ ] **Step 1: Run build_guidelines.py standalone**

```bash
cd /Users/mx/Desktop/series/核心项目系列/llm-wiki/vault && python3 scripts/build_guidelines.py --json
```

Expected: JSON with status "ok", topics listed with page counts.

- [ ] **Step 2: Verify guideline content**

```bash
ls guidelines/ && head -15 guidelines/AI.md
```

Expected: `guidelines/` contains one .md per topic. AI.md has correct frontmatter and page listings.

- [ ] **Step 3: Run snapshot_index --slim**

```bash
python3 scripts/snapshot_index.py --slim && wc -l index.md && head -25 index.md
```

Expected: ~20-30 lines. Contains stats table and comma-separated name list.

- [ ] **Step 4: Run build_ingest_context with --topic**

```bash
python3 scripts/build_ingest_context.py --topic AI | python3 -c "import sys,json; d=json.load(sys.stdin); print('pages:', d['stats']['total_pages'], 'filter:', d.get('topic_filter'))"
```

Expected: ~72 pages (not 452), filter shows `['AI']`.

- [ ] **Step 5: Run build_ingest_context without --topic (backwards compat)**

```bash
python3 scripts/build_ingest_context.py | python3 -c "import sys,json; d=json.load(sys.stdin); print('pages:', d['stats']['total_pages'])"
```

Expected: ~452 pages (full set, no filter).

- [ ] **Step 6: Restore index.md to full format**

```bash
git checkout -- index.md
```

The slim format will only be applied during actual `wiki:reindex` runs.

- [ ] **Step 7: Commit any remaining test artifacts**

```bash
git add guidelines/
git commit -m "chore: add generated guideline files from integration test"
```
