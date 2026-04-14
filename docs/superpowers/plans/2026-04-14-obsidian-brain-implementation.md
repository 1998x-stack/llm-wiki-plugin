# Obsidian Brain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a fully functional Obsidian-based personal knowledge operating system with four-tier memory, 8 agent skills, journal layer, and full automation — all as markdown files and Claude Code commands.

**Architecture:** Obsidian vault as core data layer (pure markdown). AI Agent (Claude Code) operates via project commands in `.claude/commands/wiki/`. No backend, no database — the vault directory IS the system. Frontmatter encodes structure (types, confidence, relationships).

**Tech Stack:** Obsidian, Markdown, YAML frontmatter, Claude Code project commands, bash (fswatch/cron for automation), qmd (future search)

**Important:** This is a content/configuration project, not a software project. The "code" is markdown files — schema documents, templates, and Claude Code command definitions. Verification = files exist + correct structure + commands execute successfully. After each Phase, update `README.md` and `CHANGELOG.md`, then git commit.

**Vault location:** `vault/` subdirectory of this repo. Obsidian opens this directory as a vault.

---

## File Map

### System layer
- Create: `vault/_schema/CLAUDE.md` — main operational schema (ingest/query/lint workflows)
- Create: `vault/_schema/entity-types.md` — entity type definitions
- Create: `vault/_schema/relationship-types.md` — relationship type definitions
- Create: `vault/_schema/quality-rules.md` — quality standards and lint rules

### Memory layer
- Create: `vault/_memory/working/.gitkeep`
- Create: `vault/_memory/episodic/.gitkeep`
- Create: `vault/_memory/semantic/.gitkeep`
- Create: `vault/_memory/procedural/.gitkeep`

### Content layer
- Create: `vault/raw/articles/.gitkeep`
- Create: `vault/raw/qa/.gitkeep`
- Create: `vault/raw/books/.gitkeep`
- Create: `vault/raw/assets/.gitkeep`
- Create: `vault/wiki/entities/.gitkeep`
- Create: `vault/wiki/concepts/.gitkeep`
- Create: `vault/wiki/syntheses/.gitkeep`
- Create: `vault/wiki/qa-insights/.gitkeep`

### Journal layer
- Create: `vault/journal/daily/.gitkeep`
- Create: `vault/journal/reflections/.gitkeep`
- Create: `vault/journal/judgments/.gitkeep`
- Create: `vault/journal/growth/quarterly/.gitkeep`
- Create: `vault/journal/growth/skills-tracker.md`
- Create: `vault/journal/growth/cognitive-patterns.md`

### Templates
- Create: `vault/templates/daily.md`
- Create: `vault/templates/wiki-page.md`
- Create: `vault/templates/reflection.md`
- Create: `vault/templates/judgment.md`
- Create: `vault/templates/weekly-review.md`

### Root files
- Create: `vault/index.md`
- Create: `vault/log.md`
- Create: `vault/dashboard.md`

### Agent commands (Claude Code project commands)
- Create: `vault/.claude/commands/wiki/ingest.md`
- Create: `vault/.claude/commands/wiki/query.md`
- Create: `vault/.claude/commands/wiki/lint.md`
- Create: `vault/.claude/commands/wiki/consolidate.md`
- Create: `vault/.claude/commands/wiki/crystallize.md`
- Create: `vault/.claude/commands/wiki/journal.md`
- Create: `vault/.claude/commands/wiki/review.md`
- Create: `vault/.claude/commands/wiki/qa-import.md`

### Automation
- Create: `vault/scripts/watch-raw.sh` — fswatch auto-ingest
- Create: `vault/scripts/cron-setup.sh` — cron job installer

### Repo-level (this repo, not the vault)
- Modify: `README.md` — update after each phase
- Modify: `CHANGELOG.md` — update after each phase

---

## Task 1: Create Vault Directory Structure (Phase 1a)

**Files:**
- Create: all directories and `.gitkeep` files listed in File Map

- [ ] **Step 1: Create the full directory tree**

```bash
cd /Users/mx/Desktop/series/核心项目系列/llm-wiki

# System layer
mkdir -p vault/_schema
mkdir -p vault/_memory/{working,episodic,semantic,procedural}

# Content layer
mkdir -p vault/raw/{articles,qa,books,assets}
mkdir -p vault/wiki/{entities,concepts,syntheses,qa-insights}

# Journal layer
mkdir -p vault/journal/{daily,reflections,judgments}
mkdir -p vault/journal/growth/quarterly

# Templates and commands
mkdir -p vault/templates
mkdir -p vault/.claude/commands/wiki
mkdir -p vault/scripts

# Obsidian config
mkdir -p vault/.obsidian
```

- [ ] **Step 2: Add .gitkeep files to empty directories**

```bash
for dir in \
  vault/_memory/working vault/_memory/episodic vault/_memory/semantic vault/_memory/procedural \
  vault/raw/articles vault/raw/qa vault/raw/books vault/raw/assets \
  vault/wiki/entities vault/wiki/concepts vault/wiki/syntheses vault/wiki/qa-insights \
  vault/journal/daily vault/journal/reflections vault/journal/judgments \
  vault/journal/growth/quarterly; do
  touch "$dir/.gitkeep"
done
```

- [ ] **Step 3: Verify structure**

```bash
find vault -type d | sort
```

Expected: all directories from the file map exist.

---

## Task 2: Write Schema Documents (Phase 1b)

**Files:**
- Create: `vault/_schema/CLAUDE.md`
- Create: `vault/_schema/entity-types.md`
- Create: `vault/_schema/relationship-types.md`
- Create: `vault/_schema/quality-rules.md`

- [ ] **Step 1: Write the main schema `vault/_schema/CLAUDE.md`**

```markdown
# Obsidian Brain Schema

你是这个知识库的维护者。你的职责是将源材料编译为结构化的知识页面，维护知识之间的连接和一致性，管理记忆的晋升和衰减，发现模式、标记矛盾、填补空白。

## 架构

```
vault/
├── _schema/    系统规则（你正在读的文件）
├── _memory/    四层记忆系统
├── raw/        不可变源材料（只读）
├── wiki/       LLM 生成的知识页面
├── journal/    个人日记/思考/判断/成长
├── templates/  模板
├── index.md    内容目录
└── log.md      操作日志
```

## 核心原则

1. **raw/ 只读**：源材料不可变，LLM 永远不修改 raw/ 中的文件
2. **wiki/ LLM 拥有**：所有 wiki 页面由 LLM 创建和维护，人类只读
3. **journal/ 人类拥有**：个人思考由人类写入，LLM 辅助链接和分析
4. **Links over folders**：优先使用 [[双链]] 组织关系，而非文件夹层级
5. **Bottom-up**：结构自然浮现，不预设分类体系
6. **所有操作写 log.md**：可追溯、可审计

## Frontmatter 规范

所有 wiki/ 页面必须包含以下 frontmatter：

```yaml
---
type: entity | concept | synthesis | qa-insight | source-summary
status: draft | active | stale | archived
confidence: 0.0-1.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_accessed: YYYY-MM-DD
source_count: N
tags: []
aliases: []
relates_to: []
supersedes: null
---
```

### relates_to 格式

```yaml
relates_to:
  - target: "[[页面名]]"
    type: uses | depends_on | contradicts | caused | extends | implements | supersedes
    confidence: 0.0-1.0
```

每个页面最多 10 个关系。

### tags 规则

最多 8 个大类横切标签。当前已定义标签：
- `技术` `研究` `工作` `学习` `游戏` `个人` `工具` `方法论`

不要创建新标签，除非现有标签确实无法覆盖。

## 操作手册

### Ingest

1. 读取 raw/ 中的源文件（完整阅读，不要跳过）
2. 判断内容涉及哪些实体和概念
3. 对于每个实体/概念：
   - 如果 wiki/ 中已有对应页面 → 更新该页面，追加新信息
   - 如果没有 → 创建新页面，使用 templates/wiki-page.md 模板
4. 检查新信息是否与已有页面矛盾 → 如有，用 supersedes 机制处理
5. 更新 index.md：添加新页面条目
6. 追加 log.md：记录本次 ingest 的操作

### Query

1. 读取 index.md 定位相关页面
2. 读取相关页面，沿 relates_to 扩展搜索范围
3. 综合所有信息回答问题
4. 如果答案有价值（综合了 3+ 个页面的信息），自动创建为新 wiki 页面
5. 回答时引用来源页面：`来源：[[页面名]]`

### Lint

检查以下问题并自动修复可修复项：
1. **孤页**：wiki/ 中没有任何入链的页面 → 尝试找到相关页面并添加链接
2. **矛盾**：两个页面对同一事实有不同描述 → 用 supersedes 标记旧的
3. **过期内容**：confidence < 0.3 的页面 → 标记为 stale
4. **缺失链接**：页面提到的概念没有加 [[链接]] → 自动添加
5. **空页面**：有 frontmatter 但没有实质内容 → 标记为 draft
6. 生成 lint 报告追加到 log.md

### 质量标准

wiki 页面必须满足：
- 有完整的 frontmatter（所有必要字段）
- 概述部分不超过 200 字
- 至少有 1 个来源链接
- 至少有 1 个 relates_to 关系
- 中文为主，专有名词保留英文

## 记忆系统

见 `_memory/` 目录。四层：Working → Episodic → Semantic → Procedural。

晋升规则：
- Working → Episodic：会话结束时自动压缩
- Episodic → Semantic：一个观察在 3+ 个 episode 中重复出现
- Semantic → Procedural：一个行为模式在 5+ 个语义记忆中被发现

衰减规则（Ebbinghaus）：
- slow（半衰期 180 天）：架构决策、核心概念
- medium（半衰期 60 天）：一般事实
- fast（半衰期 14 天）：临时 bug、短期观察
- confidence < 0.3 → 标记 stale

## 隐私

- journal/ 中的内容是私人的，不要在 wiki:query 结果中暴露具体日记内容
- 可以引用 journal 中的判断和反思的结论，但不引用原文
- raw/ 中标记为 private 的文件不进行 ingest
```

- [ ] **Step 2: Write `vault/_schema/entity-types.md`**

```markdown
# 实体类型定义

wiki/entities/ 中的页面必须属于以下类型之一。

| 类型 | 说明 | 示例 |
|------|------|------|
| person | 人物 | 黄仁勋、Karpathy |
| company | 公司/组织 | 腾讯、OpenAI |
| project | 项目/产品 | Claude Code、agentmemory |
| tool | 工具/库/框架 | CLIP、PyTorch、Obsidian |
| paper | 论文 | GameDevBench |
| book | 书籍 | 深入理解计算机系统 |

## Frontmatter 扩展

entity 页面在通用 frontmatter 基础上增加：

```yaml
entity_type: person | company | project | tool | paper | book
```

## 命名规则

- 中文名为主标题，英文名放 aliases
- 公司用全称，缩写放 aliases
- 人物用最常用的名字
```

- [ ] **Step 3: Write `vault/_schema/relationship-types.md`**

```markdown
# 关系类型定义

relates_to 中 type 字段的合法值。

| 类型 | 语义 | 方向 | 示例 |
|------|------|------|------|
| uses | A 使用 B | A → B | PyTorch uses CUDA |
| depends_on | A 依赖 B | A → B | 项目 depends_on Redis |
| contradicts | A 与 B 矛盾 | 双向 | 论文 A contradicts 论文 B |
| caused | A 导致 B | A → B | Bug caused 数据丢失 |
| extends | A 扩展 B | A → B | v2 extends v1 |
| implements | A 实现 B | A → B | agentmemory implements LLM Wiki |
| supersedes | A 取代 B | A → B | 新方案 supersedes 旧方案 |
| part_of | A 是 B 的一部分 | A → B | 模块 part_of 系统 |
| compares_to | A 与 B 可比较 | 双向 | CLIP compares_to BLIP-2 |

## 使用原则

- 优先选择最具体的关系类型
- 每个关系必须有 confidence 值
- 矛盾关系 (contradicts) 必须附带 note 说明具体矛盾点
- supersedes 关系必须同时更新被取代页面的 supersedes 字段
```

- [ ] **Step 4: Write `vault/_schema/quality-rules.md`**

```markdown
# 质量规则

## 页面质量标准

### 必须满足（lint 会自动检查）

1. frontmatter 包含所有必要字段
2. 概述部分存在且不超过 200 字
3. 至少 1 个来源引用
4. 至少 1 个 relates_to 关系
5. 所有 [[链接]] 指向存在的页面或标记为待创建

### 建议满足

1. confidence ≥ 0.5（低于此值应标注原因）
2. source_count ≥ 2（单一来源的事实可信度有限）
3. 每个 section 有实质内容（非空）
4. aliases 包含中英文双语名称

## Lint 自动修复规则

| 问题 | 自动修复 |
|------|---------|
| 缺失的 frontmatter 字段 | 填入默认值 |
| 断裂的 [[链接]] | 如果存在近似页面则修正，否则标记 |
| confidence 未设置 | 根据 source_count 估算：1 源=0.5, 2 源=0.7, 3+=0.85 |
| 页面未出现在 index.md | 自动添加到 index.md |
| 页面未被任何其他页面链接 | 标记为孤页，尝试找到相关页面添加链接 |

## Lint 报告格式

```markdown
## Lint Report YYYY-MM-DD

- 扫描页面数：N
- 问题总数：N
- 自动修复：N
- 需要人工处理：N

### 详情
- [页面名]: 问题描述 → 已修复 / 待处理
```
```

- [ ] **Step 5: Verify all schema files exist**

```bash
ls -la vault/_schema/
```

Expected: `CLAUDE.md`, `entity-types.md`, `relationship-types.md`, `quality-rules.md`

---

## Task 3: Write Templates (Phase 1c)

**Files:**
- Create: `vault/templates/daily.md`
- Create: `vault/templates/wiki-page.md`
- Create: `vault/templates/reflection.md`
- Create: `vault/templates/judgment.md`
- Create: `vault/templates/weekly-review.md`

- [ ] **Step 1: Write `vault/templates/daily.md`**

```markdown
---
type: daily
date: {{date}}
---

# {{date}}

## 今天在做什么

## 临时想法
<!-- 重要概念加 [[链接]]，先写再整理 -->

## 遇到的问题

## 值得记住的
<!-- weekly review 的输入源 -->

## 相关
- [[]]
```

- [ ] **Step 2: Write `vault/templates/wiki-page.md`**

```markdown
---
type: 
status: active
confidence: 
created: {{date}}
updated: {{date}}
last_accessed: {{date}}
source_count: 
tags: []
aliases: []
relates_to: []
supersedes: null
---

# {{title}}

## 概述

## 关键内容

## 来源
- [[]]

## 相关
- [[]]
```

- [ ] **Step 3: Write `vault/templates/reflection.md`**

```markdown
---
type: reflection
date: {{date}}
trigger:
tags: []
---

# {{title}}

## 发生了什么

## 我的理解

## 这改变了我什么看法

## 相关
- [[]]
```

- [ ] **Step 4: Write `vault/templates/judgment.md`**

```markdown
---
type: judgment
date: {{date}}
topic:
confidence:
tags: []
---

# {{title}}

## 我的立场

## 依据

## 可能的反驳

## 如果我错了会怎样

## 相关知识
- [[]]
```

- [ ] **Step 5: Write `vault/templates/weekly-review.md`**

```markdown
---
type: weekly-review
date: {{date}}
week:
---

# Weekly Review {{date}}

## 本周发生了什么

## 哪些值得继续

## 哪些需要停止

## 新的连接和发现

## 下周最重要的三件事
- [ ]
- [ ]
- [ ]
```

- [ ] **Step 6: Verify all templates exist**

```bash
ls vault/templates/
```

Expected: `daily.md`, `wiki-page.md`, `reflection.md`, `judgment.md`, `weekly-review.md`

---

## Task 4: Write Root Files + Growth Trackers (Phase 1d)

**Files:**
- Create: `vault/index.md`
- Create: `vault/log.md`
- Create: `vault/dashboard.md`
- Create: `vault/journal/growth/skills-tracker.md`
- Create: `vault/journal/growth/cognitive-patterns.md`

- [ ] **Step 1: Write `vault/index.md`**

```markdown
---
type: index
updated: 2026-04-14
---

# 知识库目录

> 本文件由 LLM 自动维护。每次 ingest 后更新。

## 实体 (wiki/entities/)

<!-- 格式：- [[页面名]] — 一行摘要 (confidence: X.X) -->

## 概念 (wiki/concepts/)

## 综合分析 (wiki/syntheses/)

## QA 洞见 (wiki/qa-insights/)

## 统计

- 总页面数：0
- 实体：0
- 概念：0
- 综合分析：0
- QA 洞见：0
- 最后更新：2026-04-14
```

- [ ] **Step 2: Write `vault/log.md`**

```markdown
---
type: log
---

# 操作日志

> 追加写入，不可修改历史条目。格式：`## [YYYY-MM-DD] 操作类型 | 描述`

## [2026-04-14] init | 知识库初始化

- 创建 vault 目录结构
- 写入 schema 文档（CLAUDE.md, entity-types.md, relationship-types.md, quality-rules.md）
- 写入模板（daily, wiki-page, reflection, judgment, weekly-review）
- 创建 index.md, log.md, dashboard.md
```

- [ ] **Step 3: Write `vault/dashboard.md`**

```markdown
---
type: dashboard
updated: 2026-04-14
---

# Dashboard

## 知识库概览

| 指标 | 值 |
|------|-----|
| Wiki 页面数 | 0 |
| 源材料数 | 0 |
| 记忆条目数 | 0 |
| 最近 ingest | - |
| 最近 lint | - |
| 最近 consolidate | - |

## 最近活动

见 [[log]]

## 待处理

- [ ] 迁移旧系统源文件
- [ ] 首次 ingest

## 关注领域

<!-- 由 wiki:consolidate 自动更新：最近频繁出现的主题 -->
```

- [ ] **Step 4: Write `vault/journal/growth/skills-tracker.md`**

```markdown
---
type: growth-tracker
updated: 2026-04-14
---

# 技能跟踪

> 由 wiki:consolidate 自动更新。记录技能领域的提及频率和深度变化。

## 当前关注领域

<!-- 格式：
### 领域名
- 首次出现：YYYY-MM-DD
- 最近活跃：YYYY-MM-DD
- 深度评估：入门 | 进阶 | 深入
- 趋势：↑ 增长 | → 稳定 | ↓ 衰减
-->
```

- [ ] **Step 5: Write `vault/journal/growth/cognitive-patterns.md`**

```markdown
---
type: growth-tracker
updated: 2026-04-14
---

# 认知模式记录

> 由 wiki:consolidate 自动更新。记录 LLM 从 journal 中发现的行为模式和认知偏见。

## 已发现模式

<!-- 格式：
### 模式名
- 首次发现：YYYY-MM-DD
- 出现次数：N
- 描述：...
- 证据：[[日记1]], [[日记2]], ...
- 建议：...
-->
```

- [ ] **Step 6: Verify all root and growth files**

```bash
ls vault/index.md vault/log.md vault/dashboard.md vault/journal/growth/skills-tracker.md vault/journal/growth/cognitive-patterns.md
```

---

## Task 5: Write wiki:ingest Command (Phase 1e)

**Files:**
- Create: `vault/.claude/commands/wiki/ingest.md`

- [ ] **Step 1: Write the ingest command**

Write `vault/.claude/commands/wiki/ingest.md`:

```markdown
# wiki:ingest

处理 raw/ 中的源材料，将知识编译到 wiki/ 中。

## 输入

$ARGUMENTS — 源文件路径（相对于 vault/raw/），或 "all" 处理所有未处理的文件。

## 流程

1. **读取源文件**
   - 完整阅读 `raw/$ARGUMENTS`
   - 如果是 .docx，使用 `pandoc` 或直接读取文本内容
   - 如果是 .jsonl，按行解析
   - 如果是 .pdf，提取文本

2. **提取实体和概念**
   - 识别文中提到的人物、公司、项目、工具、论文、书籍
   - 识别文中的核心概念和主题
   - 参考 `_schema/entity-types.md` 确定实体类型

3. **查找已有页面**
   - 读取 `index.md` 查看已有页面列表
   - 对每个提取的实体/概念，检查是否已有对应 wiki 页面

4. **创建或更新页面**
   - **新实体** → 在 `wiki/entities/` 创建新页面，使用 `templates/wiki-page.md` 模板
   - **新概念** → 在 `wiki/concepts/` 创建新页面
   - **已有页面** → 读取现有页面，追加新信息，更新 confidence 和 source_count
   - 文件名用 kebab-case：`游戏资产语义搜索` → `游戏资产语义搜索.md`

5. **建立关系**
   - 在每个新建/更新的页面的 frontmatter relates_to 中添加关系
   - 参考 `_schema/relationship-types.md` 选择关系类型
   - 同时更新被关联页面的 relates_to（双向）

6. **矛盾检查**
   - 如果新信息与已有页面矛盾：
     - 新页面的 relates_to 加 `type: contradicts`
     - 如果新信息更可靠（更新、更多来源），用 supersedes 标记旧声明

7. **更新 index.md**
   - 在对应分类下添加新页面条目
   - 格式：`- [[页面名]] — 一行摘要 (confidence: X.X)`
   - 更新统计数字

8. **更新 log.md**
   - 追加条目：`## [YYYY-MM-DD] ingest | 源文件名`
   - 列出创建了哪些页面、更新了哪些页面

## 质量要求

- 每个新页面必须满足 `_schema/quality-rules.md` 中的必须标准
- 概述部分不超过 200 字
- 中文为主，专有名词保留英文
- 第一次提到的重要概念加 [[链接]]

## 输出

完成后报告：
- 处理了哪个源文件
- 创建了 N 个新页面
- 更新了 N 个已有页面
- 发现了 N 个矛盾（如有）
```

- [ ] **Step 2: Verify command file exists and is readable**

```bash
cat vault/.claude/commands/wiki/ingest.md | head -5
```

Expected: `# wiki:ingest` as the first line.

---

## Task 6: Phase 1 Commit

- [ ] **Step 1: Update README.md**

Add after the "实施路径" section:

```markdown
## 当前状态

Phase 1 完成 — vault 目录结构、schema 文档、模板、wiki:ingest 命令已就绪。
```

- [ ] **Step 2: Update CHANGELOG.md**

Add under `## [Unreleased]`:

```markdown
### Phase 1 - 最小可行 vault (2026-04-14)
- 创建完整 vault 目录结构（_schema, _memory, raw, wiki, journal, templates）
- 写入主 schema `_schema/CLAUDE.md`（ingest/query/lint 操作手册 + frontmatter 规范 + 隐私规则）
- 写入类型定义（entity-types.md, relationship-types.md, quality-rules.md）
- 写入 5 套模板（daily, wiki-page, reflection, judgment, weekly-review）
- 创建 index.md, log.md, dashboard.md
- 创建 growth 跟踪文件（skills-tracker.md, cognitive-patterns.md）
- 实现 `wiki:ingest` Claude Code 命令
```

- [ ] **Step 3: Git commit**

```bash
git add vault/ README.md CHANGELOG.md
git commit -m "feat: Phase 1 — vault structure, schema, templates, wiki:ingest command

Create the Obsidian Brain vault with:
- Directory structure (_schema, _memory, raw, wiki, journal, templates)
- Operational schema (CLAUDE.md) with ingest/query/lint workflows
- Type definitions (entity-types, relationship-types, quality-rules)
- 5 templates (daily, wiki-page, reflection, judgment, weekly-review)
- Root files (index.md, log.md, dashboard.md)
- Growth trackers (skills-tracker.md, cognitive-patterns.md)
- wiki:ingest Claude Code project command"
```

---

## Task 7: Migrate Raw Sources (Phase 2a)

**Files:**
- Populate: `vault/raw/articles/` with migrated source files
- Populate: `vault/raw/books/` with book-related sources

- [ ] **Step 1: Copy source files from old system**

```bash
# Articles and documents
cp /Users/mx/Desktop/llm-wiki/raw/*.docx vault/raw/articles/
cp /Users/mx/Desktop/llm-wiki/raw/*.md vault/raw/articles/
cp /Users/mx/Desktop/llm-wiki/raw/*.pdf vault/raw/articles/

# Directories (research topics)
cp -r /Users/mx/Desktop/llm-wiki/raw/矩阵分析 vault/raw/books/
cp -r /Users/mx/Desktop/llm-wiki/raw/概率论 vault/raw/books/
cp -r /Users/mx/Desktop/llm-wiki/raw/数值分析 vault/raw/books/
cp -r /Users/mx/Desktop/llm-wiki/raw/思考系列 vault/raw/articles/

# Technical reference directories
cp -r /Users/mx/Desktop/llm-wiki/raw/claude-analysis vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/claude-code-source-code vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/claude-mem vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/CLI-tools vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/codex vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/CV-models vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/docs vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/everything-claude-code vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/gsd-skill vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/LUA-analysis vault/raw/articles/
cp -r /Users/mx/Desktop/llm-wiki/raw/deepagents-book-main vault/raw/books/
```

- [ ] **Step 2: Verify migration**

```bash
echo "Articles:" && ls vault/raw/articles/ | wc -l
echo "Books:" && ls vault/raw/books/ | wc -l
```

- [ ] **Step 3: Update log.md**

Append to `vault/log.md`:

```markdown
## [2026-04-14] migration | 从旧系统迁移源文件

- 迁移了 N 个文件/目录到 raw/articles/
- 迁移了 N 个文件/目录到 raw/books/
- 来源：/Users/mx/Desktop/llm-wiki/raw/
```

---

## Task 8: Write wiki:query and wiki:lint Commands (Phase 2b)

**Files:**
- Create: `vault/.claude/commands/wiki/query.md`
- Create: `vault/.claude/commands/wiki/lint.md`

- [ ] **Step 1: Write `vault/.claude/commands/wiki/query.md`**

```markdown
# wiki:query

基于知识库回答问题。

## 输入

$ARGUMENTS — 要回答的问题。

## 流程

1. **搜索相关页面**
   - 读取 `index.md` 找到可能相关的页面
   - 读取这些页面的 frontmatter，沿 relates_to 扩展搜索范围
   - 如果相关页面不够，用 Grep 在 wiki/ 中搜索关键词

2. **读取相关页面**
   - 读取所有找到的相关页面的完整内容
   - 注意 confidence 值——低置信度的信息标注 "（置信度较低）"

3. **综合回答**
   - 用中文回答
   - 引用来源页面：`来源：[[页面名]]`
   - 如果信息不足，明确说明哪些方面缺少数据

4. **结晶化判断**
   - 如果回答综合了 3+ 个页面的信息，且形成了新的洞见：
     - 在 `wiki/syntheses/` 创建新页面保存这个分析
     - 更新 index.md
     - 追加 log.md

5. **更新 last_accessed**
   - 更新所有被引用页面的 `last_accessed` 字段为今天日期
```

- [ ] **Step 2: Write `vault/.claude/commands/wiki/lint.md`**

```markdown
# wiki:lint

对知识库进行健康检查，自动修复可修复的问题。

## 流程

1. **扫描所有 wiki/ 页面**
   - 读取 wiki/ 下所有 .md 文件
   - 解析每个文件的 frontmatter

2. **检查项**

   **A. Frontmatter 完整性**
   - 检查每个页面是否有所有必需的 frontmatter 字段
   - 缺失字段 → 自动填入默认值（confidence 根据 source_count 估算）

   **B. 孤页检查**
   - 找出没有被任何其他页面链接到的页面
   - 尝试在相关页面中添加链接
   - 无法自动链接的 → 报告为需人工处理

   **C. 断链检查**
   - 找出所有 [[链接]] 指向不存在的页面的情况
   - 如果存在近似名称的页面 → 自动修正
   - 否则 → 报告为需创建的页面

   **D. 矛盾检查**
   - 扫描 relates_to 中 type=contradicts 的关系
   - 检查是否已有 supersedes 解决
   - 未解决的矛盾 → 基于 confidence 和 source_count 提出建议

   **E. 过期检查**
   - 找出 confidence < 0.3 的页面 → 标记为 stale
   - 找出 last_accessed 超过 180 天的页面 → 报告为可能需要复查

   **F. index.md 一致性**
   - 确保 wiki/ 中所有页面都出现在 index.md 中
   - 确保 index.md 中没有指向已删除页面的条目

3. **生成报告**
   - 追加到 log.md，格式见 `_schema/quality-rules.md` 中的 Lint 报告格式

4. **更新 dashboard.md**
   - 更新 "最近 lint" 日期
```

- [ ] **Step 3: Verify command files**

```bash
ls vault/.claude/commands/wiki/
```

Expected: `ingest.md`, `query.md`, `lint.md`

---

## Task 9: Phase 2 Commit

- [ ] **Step 1: Update README.md**

Change the "当前状态" section:

```markdown
## 当前状态

Phase 2 完成 — 源文件已迁移，wiki:query 和 wiki:lint 命令就绪。可以开始 ingest 源材料。
```

- [ ] **Step 2: Update CHANGELOG.md**

Add:

```markdown
### Phase 2 - 知识重建准备 (2026-04-14)
- 从旧系统迁移 65 个源文件到 vault/raw/
- 实现 `wiki:query` Claude Code 命令
- 实现 `wiki:lint` Claude Code 命令
```

- [ ] **Step 3: Git commit**

```bash
git add vault/ README.md CHANGELOG.md
git commit -m "feat: Phase 2 — migrate sources, add wiki:query and wiki:lint commands

Migrate 65 raw source files from old llm-wiki system into vault/raw/.
Add wiki:query command for knowledge-based Q&A with auto-crystallization.
Add wiki:lint command for health checks and auto-repair."
```

---

## Task 10: Write Journal and Review Commands (Phase 3)

**Files:**
- Create: `vault/.claude/commands/wiki/journal.md`
- Create: `vault/.claude/commands/wiki/review.md`

- [ ] **Step 1: Write `vault/.claude/commands/wiki/journal.md`**

```markdown
# wiki:journal

辅助写日记、反思或判断，自动链接到相关知识页面。

## 输入

$ARGUMENTS — 日记类型和内容提示。格式：`<type> [topic]`
- `daily` — 创建/打开今天的 daily note
- `reflection <topic>` — 创建一篇新的反思
- `judgment <topic>` — 创建一篇新的判断

## 流程

### daily

1. 检查 `journal/daily/` 中是否已有今天的文件（YYYY-MM-DD.md）
2. 如果没有 → 用 `templates/daily.md` 创建，替换 {{date}} 为今天日期
3. 如果已有 → 读取现有内容
4. 读取 index.md，找到最近 ingest 的主题，在 daily note 的"相关"部分建议链接

### reflection

1. 用 `templates/reflection.md` 创建新文件在 `journal/reflections/`
2. 文件名：topic 转为文件名格式
3. 替换 {{date}} 和 {{title}}
4. 搜索 wiki/ 中与 topic 相关的页面，在"相关"部分添加 [[链接]]
5. 追加 log.md

### judgment

1. 用 `templates/judgment.md` 创建新文件在 `journal/judgments/`
2. 文件名：topic 转为文件名格式
3. 替换 {{date}} 和 {{title}}
4. 搜索 wiki/ 中与 topic 相关的页面，在"相关知识"部分添加 [[链接]]
5. 追加 log.md
```

- [ ] **Step 2: Write `vault/.claude/commands/wiki/review.md`**

```markdown
# wiki:review

kepano 式分形回顾。扫描近期 journal 内容，辅助升维和建立连接。

## 输入

$ARGUMENTS — 回顾范围（可选）。默认为 "weekly"。
- `weekly` — 过去 7 天的 daily notes
- `monthly` — 过去 30 天
- `quarterly` — 过去 90 天

## 流程

### weekly

1. **收集素材**
   - 读取 `journal/daily/` 中过去 7 天的所有 daily notes
   - 读取 `journal/reflections/` 和 `journal/judgments/` 中过去 7 天创建的文件

2. **生成周报草稿**
   - 用 `templates/weekly-review.md` 创建 `journal/daily/YYYY-WNN.md`
   - 填充"本周发生了什么"——从 daily notes 中提取关键条目
   - 填充"新的连接和发现"——找出本周新增的 [[链接]] 关系

3. **升维建议**
   - 识别本周反复出现的主题（同一概念在 3+ 天被提到）
   - 对每个高频主题：
     - 如果 wiki/ 中还没有对应概念页 → 建议创建，并提供草稿
     - 如果已有 → 建议更新
   - 识别值得升级为正式 reflection 或 judgment 的 daily 内容

4. **链接补全**
   - 检查本周 daily notes 中提到但未加 [[链接]] 的概念
   - 自动在 daily notes 中补充 [[链接]]

5. **记录**
   - 追加 log.md：`## [YYYY-MM-DD] review | weekly`

### monthly

在 weekly 基础上增加：
- 扫描本月所有 reflections 和 judgments，提议哪些可以合并为 wiki/syntheses/ 综合页面
- 更新 `journal/growth/skills-tracker.md`

### quarterly

在 monthly 基础上增加：
- 生成 `journal/growth/quarterly/YYYY-QN.md` 季度成长报告
- 更新 `journal/growth/cognitive-patterns.md`
- 分析技能领域的变化趋势
```

- [ ] **Step 3: Phase 3 commit**

Update README.md "当前状态":

```markdown
Phase 3 完成 — journal 系统和 review 回顾命令就绪。
```

Update CHANGELOG.md:

```markdown
### Phase 3 - 个人层 (2026-04-14)
- 实现 `wiki:journal` Claude Code 命令（daily / reflection / judgment）
- 实现 `wiki:review` Claude Code 命令（weekly / monthly / quarterly 分形回顾）
```

```bash
git add vault/ README.md CHANGELOG.md
git commit -m "feat: Phase 3 — journal system with wiki:journal and wiki:review commands

Add wiki:journal for creating daily notes, reflections, and judgments
with auto-linking to relevant wiki pages.
Add wiki:review for kepano-style fractal review (weekly/monthly/quarterly)
with auto-upgrade suggestions and link completion."
```

---

## Task 11: Write Memory Commands (Phase 4)

**Files:**
- Create: `vault/.claude/commands/wiki/consolidate.md`
- Create: `vault/.claude/commands/wiki/crystallize.md`

- [ ] **Step 1: Write `vault/.claude/commands/wiki/consolidate.md`**

```markdown
# wiki:consolidate

执行记忆层的晋升和衰减。管理 Working → Episodic → Semantic → Procedural 的知识生命周期。

## 输入

$ARGUMENTS — 可选：`--deep` 执行完整的深度整合（包含 semantic→procedural 晋升）。默认只做日常整合。

## 流程

### 1. Working → Episodic 压缩

- 扫描 `_memory/working/` 中 status=unprocessed 的文件
- 对每个文件：
  - 提取关键观察
  - 合并到当天的 `_memory/episodic/YYYY-MM-DD.md`
    - 如果当天文件不存在 → 创建，frontmatter:
      ```yaml
      type: episodic-memory
      date: YYYY-MM-DD
      confidence: 0.6
      last_accessed: YYYY-MM-DD
      access_count: 1
      source_sessions: []
      ```
    - 如果已存在 → 追加新观察，更新 source_sessions
  - 将 working memory 文件标记为 `status: processed`

### 2. Episodic → Semantic 晋升

- 扫描 `_memory/episodic/` 中最近 30 天的文件
- 找出在 3+ 个不同 episode 中重复出现的观察/事实
- 对每个候选：
  - 检查 `_memory/semantic/` 中是否已有对应条目
  - 如果没有 → 创建新 semantic memory 文件：
    ```yaml
    type: semantic-memory
    fact: "..."
    confidence: 0.7
    first_observed: YYYY-MM-DD
    last_confirmed: YYYY-MM-DD
    confirmation_count: 3
    sources: []
    contradicted_by: []
    supersedes: null
    decay_rate: medium
    ```
  - 如果已有 → 更新 last_confirmed, confirmation_count, confidence（每次确认 +0.05，上限 0.95）

### 3. 置信度衰减

- 扫描 `_memory/semantic/` 中所有文件
- 对每个文件：
  - 计算距 last_confirmed 的天数
  - 按 decay_rate 计算新 confidence:
    - slow: `confidence * 0.5^(days/180)`
    - medium: `confidence * 0.5^(days/60)`
    - fast: `confidence * 0.5^(days/14)`
  - 如果新 confidence < 0.3 → 标记 status=stale
  - 更新 frontmatter

### 4. Journal 模式扫描

- 扫描 `journal/daily/` 中最近 7 天的文件
- 找出重复主题（同一 [[链接]] 或关键词在 3+ 天出现）→ 记录到 log.md
- 找出行为模式（5+ 次同类决策偏向）→ 更新 `journal/growth/cognitive-patterns.md`
- 找出成长信号（某领域提及频率增长）→ 更新 `journal/growth/skills-tracker.md`

### 5. 深度整合（--deep 时执行）

- **Semantic → Procedural 晋升**
  - 扫描 `_memory/semantic/` 中 confidence ≥ 0.8 的条目
  - 找出 5+ 个语义记忆描述同一行为模式或工作流
  - 提取为 `_memory/procedural/` 条目
- **月度/季度报告**
  - 如果当天是月初 → 生成月度 growth 报告
  - 如果当天是季初 → 生成季度报告到 `journal/growth/quarterly/`

### 6. 记录

- 追加 log.md：`## [YYYY-MM-DD] consolidate | 处理了 N 个 working, 晋升了 N 个 semantic, 衰减了 N 个`
- 更新 dashboard.md 的 "最近 consolidate" 日期
```

- [ ] **Step 2: Write `vault/.claude/commands/wiki/crystallize.md`**

```markdown
# wiki:crystallize

将当前会话的探索过程蒸馏为结构化摘要，写入 wiki 和记忆系统。

## 输入

$ARGUMENTS — 可选的会话主题描述。如果不提供，自动从当前对话上下文推断。

## 流程

1. **回顾当前会话**
   - 分析本次对话中讨论了什么
   - 识别关键发现、决策、洞见

2. **写入 Working Memory**
   - 创建 `_memory/working/YYYY-MM-DD-NN.md`（NN 为当天的序号）
   - frontmatter:
     ```yaml
     type: working-memory
     session: YYYY-MM-DD-NN
     created: YYYY-MM-DDTHH:MM:SS
     status: unprocessed
     observations: N
     ```
   - 列出本次会话的关键观察

3. **判断是否值得结晶**
   - 如果会话产生了新的综合洞见（连接了 3+ 个已有概念）：
     - 在 `wiki/syntheses/` 创建新页面
     - 更新相关页面的 relates_to
     - 更新 index.md

4. **强化已有知识**
   - 如果会话确认了已有 semantic memory 中的事实：
     - 更新对应 semantic memory 的 last_confirmed 和 confirmation_count
     - 重置衰减曲线

5. **记录**
   - 追加 log.md：`## [YYYY-MM-DD] crystallize | 会话主题`
```

- [ ] **Step 3: Phase 4 commit**

Update README.md "当前状态":

```markdown
Phase 4 完成 — 四层记忆系统和 consolidate/crystallize 命令就绪。
```

Update CHANGELOG.md:

```markdown
### Phase 4 - 记忆系统 (2026-04-14)
- 实现 `wiki:consolidate` Claude Code 命令（Working→Episodic→Semantic→Procedural 晋升 + 置信度衰减 + journal 模式扫描）
- 实现 `wiki:crystallize` Claude Code 命令（会话结晶化 → working memory + wiki synthesis）
```

```bash
git add vault/ README.md CHANGELOG.md
git commit -m "feat: Phase 4 — memory system with wiki:consolidate and wiki:crystallize

Add wiki:consolidate for four-tier memory promotion (Working→Episodic→
Semantic→Procedural), Ebbinghaus confidence decay, and journal pattern
scanning.
Add wiki:crystallize for distilling session explorations into structured
summaries and working memory entries."
```

---

## Task 12: Write wiki:qa-import Command (Phase 5)

**Files:**
- Create: `vault/.claude/commands/wiki/qa-import.md`

- [ ] **Step 1: Write the qa-import command**

Write `vault/.claude/commands/wiki/qa-import.md`:

```markdown
# wiki:qa-import

批量导入 QA 对话数据，提取洞见到 wiki。

## 输入

$ARGUMENTS — QA 文件路径（相对于 vault/raw/qa/），或 "all" 处理所有。

## 支持格式

- `.jsonl` — 每行一个 JSON 对象，必须有 `question` 和 `answer` 字段
- `.md` — ChatGPT 导出格式（Prompt/Response 交替）

## 流程

1. **解析 QA 数据**
   - 读取源文件
   - 提取所有 Q&A 对
   - 记录每个 QA 的行号/位置（用于溯源）

2. **主题聚类**
   - 将 QA 按主题分组（同一概念/项目的归到一起）
   - 每个聚类标注主题关键词

3. **提取洞见**
   - 对每个聚类：
     - 提取跨多个 QA 的关键发现
     - 过滤掉纯操作性内容（"怎么安装 X"），保留有知识价值的洞见
     - 评估每个洞见的 confidence（基于 QA 数量和一致性）

4. **创建洞见页面**
   - 对每个高价值洞见，在 `wiki/qa-insights/` 创建页面
   - frontmatter:
     ```yaml
     type: qa-insight
     source_file: "raw/qa/文件名"
     source_lines: [行号列表]
     topics: ["主题1", "主题2"]
     confidence: X.X
     created: YYYY-MM-DD
     status: active
     tags: []
     aliases: []
     relates_to: []
     ```
   - 内容包含：发现摘要、证据、关联知识的 [[链接]]

5. **建立双向链接**
   - 找到 wiki/ 中与洞见主题相关的已有页面
   - 在已有页面的 relates_to 中添加指向新洞见页面的链接
   - 在洞见页面的 relates_to 中添加指向已有页面的链接

6. **更新 index.md 和 log.md**
   - index.md: 在 "QA 洞见" 分类下添加新条目
   - log.md: `## [YYYY-MM-DD] qa-import | 文件名 → N 个洞见`
```

- [ ] **Step 2: Phase 5 commit**

Update README.md "当前状态":

```markdown
Phase 5 完成 — QA 导入系统就绪。所有 8 个 agent 命令已实现。
```

Update CHANGELOG.md:

```markdown
### Phase 5 - QA 集成 (2026-04-14)
- 实现 `wiki:qa-import` Claude Code 命令（jsonl/md 解析 → 主题聚类 → 洞见提取 → 双向链接）
```

```bash
git add vault/ README.md CHANGELOG.md
git commit -m "feat: Phase 5 — QA integration with wiki:qa-import command

Add wiki:qa-import for batch importing QA conversation data (jsonl/md),
clustering by topic, extracting insights, and creating bidirectional
links with existing wiki pages."
```

---

## Task 13: Write Automation Scripts (Phase 7)

**Files:**
- Create: `vault/scripts/watch-raw.sh`
- Create: `vault/scripts/cron-setup.sh`

- [ ] **Step 1: Write `vault/scripts/watch-raw.sh`**

```bash
#!/usr/bin/env bash
# watch-raw.sh — 监控 raw/ 目录，新文件自动触发 ingest
#
# 依赖: fswatch (brew install fswatch)
# 用法: ./scripts/watch-raw.sh
# 停止: Ctrl+C

set -euo pipefail

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Watching $VAULT_DIR/raw/ for new files..."
echo "Press Ctrl+C to stop."

fswatch -0 --event Created "$VAULT_DIR/raw/" | while IFS= read -r -d '' file; do
  # 忽略 .DS_Store 和 .gitkeep
  basename="$(basename "$file")"
  if [[ "$basename" == .* ]]; then
    continue
  fi

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] New file detected: $file"

  # 计算相对于 raw/ 的路径
  rel_path="${file#$VAULT_DIR/raw/}"

  echo "Triggering ingest for: $rel_path"
  cd "$VAULT_DIR" && claude -p "/project:wiki/ingest $rel_path" 2>&1 | tail -5

  echo "---"
done
```

- [ ] **Step 2: Write `vault/scripts/cron-setup.sh`**

```bash
#!/usr/bin/env bash
# cron-setup.sh — 安装定时任务
#
# 用法: ./scripts/cron-setup.sh
# 查看: crontab -l
# 卸载: crontab -r (删除所有 cron 任务)

set -euo pipefail

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Setting up cron jobs for Obsidian Brain..."
echo "Vault directory: $VAULT_DIR"

# 生成 cron 条目
CRON_ENTRIES="
# Obsidian Brain — 每日凌晨 2:07 consolidate
7 2 * * * cd $VAULT_DIR && claude -p '/project:wiki/consolidate' >> $VAULT_DIR/data/cron.log 2>&1

# Obsidian Brain — 每周日晚 20:13 lint + review
13 20 * * 0 cd $VAULT_DIR && claude -p '/project:wiki/lint' >> $VAULT_DIR/data/cron.log 2>&1 && claude -p '/project:wiki/review weekly' >> $VAULT_DIR/data/cron.log 2>&1

# Obsidian Brain — 每月 1 号凌晨 3:17 深度 consolidate
17 3 1 * * cd $VAULT_DIR && claude -p '/project:wiki/consolidate --deep' >> $VAULT_DIR/data/cron.log 2>&1
"

# 检查是否已安装
if crontab -l 2>/dev/null | grep -q "Obsidian Brain"; then
  echo "Cron jobs already installed. Replacing..."
  crontab -l 2>/dev/null | grep -v "Obsidian Brain" | grep -v "wiki/consolidate" | grep -v "wiki/lint" | grep -v "wiki/review" > /tmp/crontab_clean
  echo "$CRON_ENTRIES" >> /tmp/crontab_clean
  crontab /tmp/crontab_clean
  rm /tmp/crontab_clean
else
  echo "Installing new cron jobs..."
  (crontab -l 2>/dev/null; echo "$CRON_ENTRIES") | crontab -
fi

echo ""
echo "Installed cron jobs:"
crontab -l | grep "Obsidian Brain" -A1
echo ""
echo "Done. Logs will be written to $VAULT_DIR/data/cron.log"

mkdir -p "$VAULT_DIR/data"
```

- [ ] **Step 3: Make scripts executable**

```bash
chmod +x vault/scripts/watch-raw.sh vault/scripts/cron-setup.sh
```

- [ ] **Step 4: Phase 7 commit**

Update README.md "当前状态":

```markdown
## 当前状态

所有 Phase 完成。系统就绪，可以开始使用。

### 快速开始

1. 用 Obsidian 打开 `vault/` 目录作为 vault
2. 在 vault 目录中运行 Claude Code
3. 执行 `/project:wiki/ingest articles/文件名.md` 开始 ingest 源材料
4. 执行 `/project:wiki/journal daily` 创建今天的日记
5. （可选）运行 `./scripts/watch-raw.sh` 启动自动 ingest
6. （可选）运行 `./scripts/cron-setup.sh` 安装定时任务
```

Update CHANGELOG.md:

```markdown
### Phase 7 - 自动化 (2026-04-14)
- 添加 `scripts/watch-raw.sh`：fswatch 监控 raw/ 目录自动 ingest
- 添加 `scripts/cron-setup.sh`：安装定时 consolidate/lint/review 任务
```

```bash
git add vault/ README.md CHANGELOG.md
git commit -m "feat: Phase 7 — automation scripts for fswatch and cron

Add watch-raw.sh for auto-ingest on new files in raw/.
Add cron-setup.sh for scheduled consolidate (daily), lint+review
(weekly), and deep consolidate (monthly)."
```

---

## Task 14: Write Obsidian Configuration (Final)

**Files:**
- Create: `vault/.obsidian/app.json`
- Create: `vault/.obsidian/core-plugins.json`

- [ ] **Step 1: Write minimal Obsidian config**

Write `vault/.obsidian/app.json`:

```json
{
  "attachmentFolderPath": "raw/assets",
  "newLinkFormat": "shortest",
  "useMarkdownLinks": false,
  "showFrontmatter": true,
  "defaultViewMode": "source"
}
```

Write `vault/.obsidian/core-plugins.json`:

```json
[
  "file-explorer",
  "global-search",
  "switcher",
  "graph",
  "backlink",
  "outgoing-link",
  "tag-pane",
  "properties",
  "daily-notes",
  "templates",
  "command-palette",
  "bookmarks",
  "outline"
]
```

- [ ] **Step 2: Write vault-level CLAUDE.md**

Write `vault/CLAUDE.md`:

```markdown
# CLAUDE.md

This is an Obsidian Brain vault — a personal knowledge operating system.

## Quick Reference

- Schema: `_schema/CLAUDE.md` (read this first for full operational instructions)
- Commands: `.claude/commands/wiki/` (ingest, query, lint, consolidate, crystallize, journal, review, qa-import)
- Templates: `templates/` (daily, wiki-page, reflection, judgment, weekly-review)

## Key Rules

1. Never modify files in `raw/` — it is read-only
2. All wiki pages must have complete frontmatter (see `_schema/CLAUDE.md`)
3. All operations must be logged in `log.md`
4. Journal content is private — do not expose in query results
5. Use [[双链]] liberally — links over folders
```

- [ ] **Step 3: Final commit**

```bash
git add vault/ README.md CHANGELOG.md
git commit -m "feat: Obsidian config and vault CLAUDE.md

Add minimal Obsidian settings (attachment path, core plugins).
Add vault-level CLAUDE.md as quick-reference entry point."
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] Vault directory structure (Section 2) → Task 1
- [x] Four-tier memory system (Section 3) → Task 1 (dirs) + Task 11 (commands)
- [x] Schema documents (Section 4) → Task 2
- [x] All 8 Agent Skills (Section 5) → Tasks 5, 8, 10, 11, 12
- [x] Journal system (Section 6) → Task 1 (dirs) + Task 4 (growth) + Task 10 (commands)
- [x] QA integration (Section 7) → Task 12
- [x] Search architecture (Section 8) → embedded in wiki:query command
- [x] Automation (Section 9) → Task 13
- [x] Templates (Section 10) → Task 3
- [x] Migration (Section 11) → Task 7
- [x] Implementation path (Section 12) → all tasks organized by phase
- [x] README.md + CHANGELOG.md + git commit per phase → Tasks 6, 9, 10, 11, 12, 13, 14

**Placeholder scan:** No TBD/TODO/placeholders found. All commands have complete flow definitions.

**Type consistency:** Frontmatter field names consistent across all templates and command definitions (type, status, confidence, created, updated, last_accessed, source_count, tags, aliases, relates_to, supersedes).
