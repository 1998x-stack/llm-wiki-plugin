# LLM Wiki Plugin 用户指南

本指南详细介绍 LLM Wiki Plugin 的安装、配置和使用方法。系统以 Obsidian vault 为数据层，Claude Code CLI 为 AI 处理引擎，构建个人知识操作系统。

---

## 目录

1. [前置条件](#1-前置条件)
2. [安装步骤](#2-安装步骤)
3. [Vault 结构说明](#3-vault-结构说明)
4. [命令详解](#4-命令详解)
5. [工作流指南](#5-工作流指南)
6. [Hook 系统说明](#6-hook-系统说明)
7. [BM25 搜索系统](#7-bm25-搜索系统)
8. [模板定制指南](#8-模板定制指南)
9. [常见问题排查](#9-常见问题排查)
10. [高级配置](#10-高级配置)

---

## 1. 前置条件

### 必备

| 依赖 | 最低版本 | 用途 |
|------|---------|------|
| Python | 3.10+ | 运行 BM25 索引、知识图谱构建、lint 检查、Qwen ingest 脚本 |
| Obsidian | 1.5+ | 浏览和编辑 vault 中的 markdown 文件 |
| Claude Code CLI | latest | AI 处理引擎，执行所有 wiki 命令 |

### 可选

| 依赖 | 用途 |
|------|------|
| `DASHSCOPE_API_KEY` | 通义千问 API 密钥，用于 Qwen 批量 ingest |
| `fswatch` | macOS 文件监控，用于 `watch-raw.sh` 自动 ingest |
| Node.js | 安装 Claude Code CLI（`npm install -g @anthropic-ai/claude-code`） |

### Python 依赖

项目所需的 Python 包列在 `requirements.txt` 中：

```
jieba>=0.42          # 中文分词
rank_bm25>=0.2.2     # BM25 检索算法
pyyaml>=6.0          # YAML frontmatter 解析
openai>=1.0.0        # Qwen API（兼容 OpenAI 接口）
```

---

## 2. 安装步骤

### Step 1: 克隆仓库

```bash
git clone https://github.com/1998x-stack/llm-wiki-plugin.git
cd llm-wiki-plugin
```

### Step 2: 安装 Python 依赖

```bash
pip install -r requirements.txt
```

验证安装：

```bash
python3 -c "import jieba, rank_bm25, yaml, openai; print('All dependencies OK')"
```

### Step 3: 用 Obsidian 打开 vault

1. 打开 Obsidian
2. 选择 "Open folder as vault"
3. 选择项目中的 `vault/` 目录
4. Obsidian 会自动加载 `.obsidian/` 中的预配置设置

### Step 4: 启动 Claude Code

```bash
cd vault
claude
```

Claude Code 会自动读取 `vault/CLAUDE.md` 和 `vault/_schema/CLAUDE.md`，加载所有 wiki 命令。

### Step 5: 验证命令可用

在 Claude Code 中输入 `/wiki:` 然后按 Tab，应该看到所有命令：

```
ingest  query  check  lint  consolidate  crystallize  journal  review  qa-import  ingest-loop  build  reindex  maintain  convert-to-markdown
```

### Step 6: （可选）配置 Qwen API

如果需要使用 Qwen 批量 ingest：

```bash
export DASHSCOPE_API_KEY="your-api-key-here"
```

建议将此行添加到 `~/.zshrc` 或 `~/.bashrc` 中以持久化。

### Step 7: （可选）启动自动化

```bash
# 文件监控 — 新文件自动 ingest
bash vault/scripts/watch-raw.sh &

# 定时任务 — 定期 consolidate/lint/review
bash vault/scripts/cron-setup.sh
```

---

## 3. Vault 结构说明

### 顶层目录

```
vault/
├── .claude/commands/wiki/   # Claude Code 命令定义
├── .obsidian/               # Obsidian 应用配置
├── _schema/                 # 系统规则和类型定义
├── _memory/                 # 四层记忆系统
├── raw/                     # 不可变源材料（LLM 只读）
├── wiki/                    # LLM 生成的知识页面
├── journal/                 # 个人日记系统
├── qa/                      # QA 数据存放区
├── index/                   # 搜索索引
├── templates/               # 页面模板
├── scripts/                 # 自动化脚本
├── index.md                 # 全局内容目录
├── log.md                   # 操作日志
├── log.hook.md              # Hook 执行日志
├── graph.json               # 知识图谱数据
└── dashboard.md             # 系统仪表盘
```

### `_schema/` — 系统规则

系统的"宪法"，定义所有 AI 行为规则。

| 文件 | 内容 |
|------|------|
| `CLAUDE.md` | 主 schema — ingest/query/lint 操作手册、frontmatter 规范、隐私规则 |
| `entity-types.md` | 实体类型定义（人物、工具、项目、组织等） |
| `relationship-types.md` | 关系类型定义（implements、extends、contradicts 等） |
| `quality-rules.md` | 质量规则（链接完整性、内容新鲜度、一致性检查） |

### `_memory/` — 四层记忆

模拟人脑记忆机制的知识生命周期系统。

| 层级 | 目录 | 生命周期 | 说明 |
|------|------|---------|------|
| Working | `working/` | 当前会话 | 会话中的临时观察和笔记 |
| Episodic | `episodic/` | 天级 | 会话结束后的结构化摘要 |
| Semantic | `semantic/` | 周/月级 | 跨会话提炼的事实和规律 |
| Procedural | `procedural/` | 永久 | 已验证的工作流和模式 |

### `raw/` — 源材料

所有原始输入材料，LLM 只能读取，不可修改。

```
raw/
├── articles/         # 文章、论文、技术分析
│   ├── CLI-tools/
│   ├── CV-models/
│   ├── claude-analysis/
│   ├── claude-code-source-code/
│   └── 思考系列/
├── books/            # 书籍章节
│   ├── deepagents-book-main/
│   ├── 数值分析/
│   ├── 概率论/
│   └── 矩阵分析/
├── qa/               # QA 对话原始数据
└── assets/           # 图片等非文本资源
```

### `wiki/` — 知识页面

AI 生成和维护的结构化知识，每个页面有标准 frontmatter。

```
wiki/
├── entities/         # 实体页面：人物、工具、项目
├── concepts/         # 概念页面：理论、方法、模式
├── syntheses/        # 综合页面：跨领域比较和分析
└── qa-insights/      # QA 洞见：从对话中提取的知识
```

每个 wiki 页面的 frontmatter 示例：

```yaml
---
title: "切比雪夫多项式"
type: concept
tags: [数值分析, 逼近论, 多项式]
confidence: 0.9
sources: ["raw/books/数值分析/chapter5.md"]
relates_to: ["勒贝格常数", "Romberg积分"]
created: 2026-04-15
updated: 2026-04-15
---
```

### `journal/` — 个人日记

```
journal/
├── daily/            # 每日笔记（YYYY-MM-DD.md）
├── reflections/      # 反思记录
├── judgments/        # 判断和决策记录
└── growth/           # 成长追踪
    ├── skills-tracker.md
    ├── cognitive-patterns.md
    └── quarterly/
```

### `scripts/` — 自动化脚本

| 脚本 | 类型 | 说明 |
|------|------|------|
| `bm25_index.py` | Python | BM25 索引构建和查询 |
| `build_graph.py` | Python | 知识图谱 JSON 生成 |
| `lint_wiki.py` | Python | Wiki 质量检查 |
| `qwen_ingest.py` | Python | Qwen API 页面提取 |
| `hook_bm25.sh` | Shell | Hook: ingest 后重建 BM25 索引 |
| `hook_graph.sh` | Shell | Hook: ingest 后重建知识图谱 |
| `hook_lint.sh` | Shell | Hook: ingest 后运行 lint |
| `watch-raw.sh` | Shell | fswatch 文件监控 |
| `cron-setup.sh` | Shell | 定时任务安装 |
| `setup-ingest-loop.sh` | Shell | Ralph-loop 设置（Claude） |
| `setup-ingest-loop-qwen.sh` | Shell | Ralph-loop 设置（Qwen） |

### `templates/` — 页面模板

| 模板 | 用途 |
|------|------|
| `daily.md` | 每日笔记 |
| `wiki-page.md` | Wiki 知识页面 |
| `reflection.md` | 反思记录 |
| `judgment.md` | 判断记录 |
| `weekly-review.md` | 每周回顾 |

### 核心文件

| 文件 | 说明 |
|------|------|
| `index.md` | 全局内容目录，按类别列出所有 wiki 页面（由 `snapshot_index.py` 自动维护的计算产出，勿手动编辑） |
| `log.md` | 操作日志，记录每次 ingest/lint/consolidate 的结果 |
| `log.hook.md` | Hook 执行日志 |
| `graph.json` | 知识图谱的节点和边数据 |
| `dashboard.md` | 系统统计仪表盘 |

---

## 4. 命令详解

### 4.1 `wiki:ingest` — 源材料导入

**功能：** 读取 `raw/` 中的源文件，提取知识，生成 wiki 页面，更新 index.md 和 log.md。

**用法：**

```
/wiki:ingest raw/articles/your-article.md
```

**处理流程：**

1. 读取源文件内容
2. 识别实体（人物、工具、项目）和概念（理论、方法）
3. 为每个知识点生成独立的 wiki 页面（含标准 frontmatter）
4. 建立页面之间的 `[[wikilink]]` 交叉引用
5. 更新 `index.md` 目录
6. 在 `log.md` 中记录本次操作

**输出示例：**

```
Ingested: raw/articles/数值分析-插值.md
Created:
  - wiki/concepts/拉格朗日插值.md
  - wiki/concepts/牛顿插值.md
  - wiki/entities/拉格朗日.md
Updated: index.md, log.md
```

### 4.2 `wiki:query` — 知识查询

**功能：** 搜索知识库，综合多个页面的信息回答问题。高质量答案可选自动归档。

**用法：**

```
/wiki:query 切比雪夫多项式和勒贝格常数的关系是什么？
```

**处理流程：**

1. 在 index.md 和 wiki 页面中搜索相关内容
2. 读取匹配页面，提取关键信息
3. 综合多个来源给出结构化回答
4. 附带引用来源列表

### 4.3 `wiki:check` — 只读诊断

**功能：** 只读审计知识库，报告质量问题但不修改任何文件。

**用法：**

```
/wiki:check
```

**检查项目：** 与 `wiki:lint` 相同，但只报告，不修复。适合快速了解当前知识库状态。

### 4.4 `wiki:lint` — 知识库健康检查与修复

**功能：** 调用 `wiki:check` 进行诊断，然后自动修复可修复的问题。

**用法：**

```
/wiki:lint
```

**检查项目：**

- 孤页（没有任何入链的页面）
- 断链（`[[wikilink]]` 指向不存在的页面）
- 缺失 frontmatter 字段
- 过期内容（confidence 低于阈值）
- index.md 与实际页面不一致
- 矛盾信息（同一事实在不同页面有不同描述）

**输出示例：**

```
Lint Results:
  Orphan pages: 3
    - wiki/concepts/旧概念.md
  Broken links: 1
    - wiki/entities/张三.md → [[不存在的页面]]
  Missing frontmatter: 2
  Auto-fixed: 2 issues
  Manual review needed: 1 issue
```

### 4.5 `wiki:consolidate` — 记忆晋升

**功能：** 执行四层记忆系统的晋升和衰减操作。

**用法：**

```
/wiki:consolidate
```

**操作内容：**

1. **Working → Episodic 晋升：** 扫描 `_memory/working/`，将成熟的观察整理为会话摘要，移入 `_memory/episodic/`
2. **Episodic → Semantic 晋升：** 找出反复出现的模式，提炼为稳定事实
3. **Semantic → Procedural 晋升：** 将已验证的工作流固化为标准流程
4. **置信度衰减：** 降低长期未引用页面的 confidence 值
5. **Journal 模式扫描：** 分析日记中的反复主题

### 4.6 `wiki:crystallize` — 会话结晶

**功能：** 将当前会话中的探索过程蒸馏为结构化摘要。

**用法：**

```
/wiki:crystallize
```

**输出：**

- 在 `_memory/working/` 中创建会话摘要
- 如果发现新知识，在 `wiki/syntheses/` 中创建综合页面
- 更新相关页面的交叉引用

### 4.7 `wiki:journal` — 日记辅助

**功能：** 辅助写日记、反思或判断，自动链接到相关知识页面。

**用法：**

```
/wiki:journal daily          # 创建今天的每日笔记
/wiki:journal reflection     # 创建反思记录
/wiki:journal judgment       # 创建判断记录
```

**输出文件位置：**

- `daily` → `journal/daily/YYYY-MM-DD.md`
- `reflection` → `journal/reflections/YYYY-MM-DD-reflection.md`
- `judgment` → `journal/judgments/YYYY-MM-DD-judgment.md`

### 4.8 `wiki:review` — 分形回顾

**功能：** kepano 式分形回顾。扫描近期 journal 内容，辅助升维和建立连接。

**用法：**

```
/wiki:review weekly          # 每周回顾
/wiki:review monthly         # 每月回顾
/wiki:review quarterly       # 每季回顾
```

**处理流程：**

1. 扫描对应时间段内的所有 journal 条目
2. 识别反复出现的主题和模式
3. 建议新的知识页面或跨领域连接
4. 生成回顾摘要

### 4.9 `wiki:qa-import` — QA 数据导入

**功能：** 批量导入 QA 对话数据（jsonl 或 markdown 格式），提取洞见到 wiki。

**用法：**

```
/wiki:qa-import raw/qa/conversations.jsonl
/wiki:qa-import raw/qa/session-notes.md
```

**处理流程：**

1. 解析输入文件（支持 jsonl 和 markdown 格式）
2. 按主题聚类 QA 对话
3. 从每个主题中提取核心洞见
4. 在 `wiki/qa-insights/` 中创建洞见页面
5. 建立与已有 wiki 页面的双向链接

### 4.10 `wiki:ingest-loop` — 自动循环 Ingest

**功能：** 基于 Ralph-loop 机制，自动逐文件 ingest 整个目录。支持 `--engine=qwen` 切换到 Qwen API。

**用法：**

```
/wiki:ingest-loop raw/articles/数值分析/
/wiki:ingest-loop raw/books/概率论/ --engine=qwen
```

**工作原理：**

1. 扫描目标目录中所有待处理的 markdown 文件
2. 生成状态文件 `.claude/ingest-loop.local.md`
3. 启动 Ralph-loop，每次处理一个文件
4. 处理完成后自动标记，继续下一个
5. 全部完成后停止

**引擎选项：**

- 默认（无 flag）：使用 Claude Code 处理，质量最高，消耗 Claude 上下文
- `--engine=qwen`：使用通义千问 API，快速，不消耗 Claude 上下文，适合大批量场景。需要设置 `DASHSCOPE_API_KEY`

### 4.11 `wiki:build` — 构建所有静态产出

**功能：** 扫描所有 wiki 页面，构建知识图谱、统计数据和静态 HTML wiki 查看器。

**用法：**

```
/wiki:build
```

**输出：**

- `graph.json`：节点（页面）和边（wikilink + frontmatter 关系）的 JSON 数据
- `graph-statistics.json`：类型分布、置信度、标签频率等统计数据
- `static/wiki/*.html`：静态 HTML wiki 查看器页面

### 4.12 `wiki:maintain` — 一键维护

**功能：** 一键执行完整维护流水线：reorganize-raw → reindex → check → build。等价于依次运行四个命令，但在关键步骤失败时提前终止。

**用法：**

```
/wiki:maintain
```

**处理流程：**

1. **Reindex** — 验证 index.md 完整性，生成主题分类 maps
2. **Check** — 只读诊断，生成问题报告
3. **Lint** — 基于诊断结果自动修复可修复的问题
4. **Build** — 构建 graph.json + statistics + wiki HTML

**适用场景：** 批量 ingest 后的全面维护、每周例行维护、发布前检查。

---

## 5. 工作流指南

### 5.1 日常工作流

每日推荐工作流程：

```
早上：
1. /wiki:journal daily        — 创建今日笔记
2. 浏览 dashboard.md                   — 了解系统状态

工作中：
3. 将新源材料放入 raw/articles/        — 收集
4. /wiki:ingest <path>         — 导入新知识
5. /wiki:query <question>      — 查询已有知识

结束时：
6. /wiki:crystallize           — 结晶今日探索
7. /wiki:consolidate           — 记忆整理
```

### 5.2 每周回顾

```
每周日：
1. /wiki:review weekly         — 回顾本周
2. /wiki:maintain              — 一键维护（reorganize-raw→relink→reindex→check→lint→build）
3. 在 Obsidian 图谱视图中浏览连接       — 发现模式
```

### 5.3 批量 Ingest 流程

当需要导入大量源材料（例如一本书的所有章节）：

```
# 方式 1：Claude 逐文件处理（高质量，消耗上下文）
/wiki:ingest-loop raw/books/矩阵分析/

# 方式 2：Qwen API 批量处理（快速，不消耗 Claude 上下文）
# 需要先设置：export DASHSCOPE_API_KEY="your-key"
/wiki:ingest-loop raw/books/矩阵分析/ --engine=qwen
```

```bash
# 处理完成后，重建索引和图谱
python3 scripts/bm25_index.py build
python3 scripts/build_graph.py
```

### 5.4 知识图谱探索

```
# 1. 构建图谱
/wiki:build

# 2. 在浏览器中打开 graph.html 查看交互式图谱

# 3. 在 Obsidian 中使用内置 Graph View（Ctrl/Cmd+G）

# 4. 通过 GitHub Pages 在线查看
#    https://1998x-stack.github.io/llm-wiki-plugin/graph.html
```

---

## 6. Hook 系统说明

### 什么是 Hook

Hook 是在特定操作（如 ingest）完成后自动触发的脚本。系统提供三个 hook 脚本：

| Hook | 脚本 | 触发时机 | 功能 |
|------|------|---------|------|
| BM25 Hook | `scripts/hook_bm25.sh` | ingest 后 | 重建 BM25 搜索索引 |
| Graph Hook | `scripts/hook_graph.sh` | ingest 后 | 重建知识图谱 JSON |
| Lint Hook | `scripts/hook_lint.sh` | ingest 后 | 运行质量检查 |

### Hook 执行流程

```
wiki:ingest 完成
  ├── hook_bm25.sh  → python3 bm25_index.py build
  ├── hook_graph.sh → python3 build_graph.py
  └── hook_lint.sh  → python3 lint_wiki.py
```

### `log.hook.md` 日志格式

每次 hook 执行后会在 `log.hook.md` 中追加记录：

```markdown
## 2026-04-15 14:30:22

- **trigger**: ingest raw/articles/example.md
- **hook_bm25**: OK (rebuilt 127 documents, 0.8s)
- **hook_graph**: OK (89 nodes, 156 edges)
- **hook_lint**: WARN (2 orphan pages found)
```

### 手动触发 Hook

```bash
# 单独重建 BM25 索引
bash scripts/hook_bm25.sh

# 单独重建图谱
bash scripts/hook_graph.sh

# 单独运行 lint
bash scripts/hook_lint.sh
```

---

## 7. BM25 搜索系统

### 工作原理

BM25（Best Matching 25）是经典的全文检索算法。系统实现流程：

1. **分词：** 使用 jieba 对所有 wiki 页面进行中文分词
2. **建索引：** 使用 rank_bm25 库构建倒排索引
3. **存储：** 索引文件保存在 `index/BM25/` 目录
4. **查询：** 输入查询词，返回按相关性排序的页面列表

### 索引管理

```bash
# 完整重建索引（扫描所有 wiki 页面）
python3 scripts/bm25_index.py build

# 查询
python3 scripts/bm25_index.py query "切比雪夫逼近"

# 查看索引统计
python3 scripts/bm25_index.py stats
```

### 查询语法

BM25 查询支持自然语言输入。jieba 会自动分词：

```bash
# 简单查询
python3 scripts/bm25_index.py query "矩阵特征值"

# 多关键词查询（自动分词后取并集）
python3 scripts/bm25_index.py query "概率论 贝叶斯 条件概率"

# 长查询（jieba 提取关键词）
python3 scripts/bm25_index.py query "如何使用切比雪夫多项式进行函数逼近"
```

### 索引更新时机

索引在以下情况需要重建：

- 新 wiki 页面被创建（ingest 后 hook 自动触发）
- 页面内容被修改
- 页面被删除

如果启用了 hook 系统，索引会在每次 ingest 后自动重建。

---

## 8. 模板定制指南

### 模板位置

所有模板位于 `vault/templates/` 目录。

### 模板结构

每个模板包含：

1. **YAML frontmatter** — 定义元数据字段
2. **Markdown body** — 页面结构和提示文本

### `wiki-page.md` 模板

这是最核心的模板，用于生成所有 wiki 知识页面：

```yaml
---
title: "{{title}}"
type: {{type}}               # entity | concept | synthesis
tags: []
confidence: 0.8
sources: []
relates_to: []
created: {{date}}
updated: {{date}}
---

## 概述

{{概述内容}}

## 核心内容

{{详细内容}}

## 关联

- 相关概念：{{wikilinks}}
- 参见：{{外部链接}}
```

### 修改模板的注意事项

1. **保留必须字段：** `title`、`type`、`confidence`、`sources`、`created`、`updated` 是系统必须字段，lint 会检查它们
2. **保持 frontmatter 格式：** 必须是合法的 YAML
3. **使用占位符：** `{{placeholder}}` 格式便于 AI 理解需要填充的位置
4. **修改后更新 schema：** 如果添加了新的 frontmatter 字段，需要在 `_schema/CLAUDE.md` 中同步说明

### 添加新模板

1. 在 `templates/` 中创建新的 `.md` 文件
2. 定义 frontmatter 和 body 结构
3. 在 `_schema/CLAUDE.md` 中注册新模板
4. （可选）创建对应的 Claude Code 命令

---

## 9. 常见问题排查

### API 相关错误

**问题：** Qwen ingest 报错 `DASHSCOPE_API_KEY not set`

```bash
# 解决：设置环境变量
export DASHSCOPE_API_KEY="your-key"
# 持久化
echo 'export DASHSCOPE_API_KEY="your-key"' >> ~/.zshrc
```

**问题：** Qwen API 返回 rate limit 错误

```
解决：
1. 检查 API 配额是否用完
2. 在 qwen_ingest.py 中调大 retry 间隔
3. 减少并发请求数
```

**问题：** Claude Code 无法连接

```
解决：
1. 确认 Claude Code CLI 已安装：claude --version
2. 确认 API key 已配置：claude config
3. 检查网络连接
```

### 索引损坏

**问题：** BM25 查询返回空结果或报错

```bash
# 解决：完整重建索引
python3 scripts/bm25_index.py build

# 如果仍报错，删除索引文件后重建
rm -rf index/BM25/*
python3 scripts/bm25_index.py build
```

**问题：** `graph.json` 数据不完整

```bash
# 解决：重新构建图谱
python3 scripts/build_graph.py --output vault/graph.json
```

### 权限问题

**问题：** `watch-raw.sh` 报权限错误

```bash
# 解决：添加执行权限
chmod +x scripts/watch-raw.sh
chmod +x scripts/hook_bm25.sh
chmod +x scripts/hook_graph.sh
chmod +x scripts/hook_lint.sh
```

**问题：** cron 任务不执行

```bash
# 检查 cron 任务是否已安装
crontab -l

# 检查 cron 日志
grep CRON /var/log/syslog        # Linux
log show --predicate 'process == "cron"' --last 1h  # macOS
```

### 缺失依赖

**问题：** `ModuleNotFoundError: No module named 'jieba'`

```bash
# 解决：安装依赖
pip install -r requirements.txt

# 如果使用虚拟环境，确保激活了正确的环境
source venv/bin/activate
pip install -r requirements.txt
```

**问题：** `fswatch: command not found`

```bash
# macOS
brew install fswatch

# Linux (Ubuntu/Debian)
sudo apt-get install fswatch
```

### 页面质量问题

**问题：** ingest 生成的页面质量不高

```
解决：
1. 确保源文件内容完整、结构清晰
2. 检查 _schema/CLAUDE.md 中的 ingest 规则是否完善
3. 对重要源文件使用 Claude ingest（而非 Qwen），质量更高
4. ingest 后运行 /wiki:lint 检查并修复问题
```

**问题：** 页面之间链接混乱

```bash
# 运行 lint 检查和修复
/wiki:lint

# 手动检查
python3 scripts/lint_wiki.py
```

---

## 10. 高级配置

### 10.1 Cron 定时任务

`scripts/cron-setup.sh` 会安装以下定时任务：

```cron
# 每天凌晨 2 点 — 记忆整理
0 2 * * * cd /path/to/vault && claude -p "consolidate"

# 每周日凌晨 3 点 — 知识库 lint
0 3 * * 0 cd /path/to/vault && claude -p "lint"

# 每周日凌晨 4 点 — 每周回顾
0 4 * * 0 cd /path/to/vault && claude -p "review weekly"
```

修改任务频率：

```bash
# 编辑 cron 任务
crontab -e

# 或修改 scripts/cron-setup.sh 后重新运行
bash scripts/cron-setup.sh
```

### 10.2 自定义模板

如需为特定领域创建专用模板：

1. 复制 `templates/wiki-page.md` 为新模板
2. 添加领域特定的 frontmatter 字段
3. 调整 body 结构
4. 在 `_schema/entity-types.md` 中注册新类型

示例 — 创建"论文"类型模板：

```yaml
---
title: "{{title}}"
type: paper
tags: []
authors: []
venue: ""
year: null
confidence: 0.8
sources: []
relates_to: []
created: {{date}}
updated: {{date}}
---

## 摘要

## 方法

## 实验结果

## 局限性

## 与其他工作的关系
```

### 10.3 Qwen Prompt 调优

`scripts/qwen_ingest.py` 中的 system prompt 可以定制。关键参数：

```python
# 修改 qwen_ingest.py 中的 prompt
SYSTEM_PROMPT = """
你是一个知识提取助手。请从输入文本中提取：
1. 核心概念（含定义和例子）
2. 关键人物（含贡献描述）
3. 概念之间的关系
输出格式为 Obsidian markdown，包含标准 frontmatter。
"""
```

调优建议：

- 明确指定输出格式（frontmatter 字段和 body 结构）
- 限制每次提取的知识点数量，避免信息过载
- 添加领域特定的提取指令
- 要求生成 `[[wikilink]]` 交叉引用

### 10.4 GitHub Pages 部署

将知识图谱部署到 GitHub Pages：

1. 在仓库 Settings → Pages 中启用 GitHub Pages
2. 选择部署源（推荐 GitHub Actions）
3. 创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy Graph to Pages
on:
  push:
    branches: [main]
    paths: ['vault/graph.json', 'static/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Build graph HTML
        run: python3 vault/scripts/build_graph.py
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: static/
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

4. Push 代码后，访问 `https://<username>.github.io/llm-wiki-plugin/graph.html`

### 10.5 自定义关系类型

在 `_schema/relationship-types.md` 中添加新的关系类型：

```markdown
## 关系类型

| 关系 | 含义 | 示例 |
|------|------|------|
| implements | A 实现了 B | Jacobi迭代法 implements 线性方程组求解 |
| extends | A 扩展了 B | v2 extends v1 |
| contradicts | A 与 B 矛盾 | 理论A contradicts 理论B |
| requires | A 依赖 B | QR算法 requires 矩阵分解 |
| your_relation | 自定义含义 | ... |
```

### 10.6 多 Vault 管理

如果需要管理多个知识领域的 vault：

```bash
llm-wiki-plugin/
├── vault-math/          # 数学知识库
├── vault-cs/            # 计算机科学知识库
└── vault-personal/      # 个人笔记

# 在不同 vault 中启动 Claude Code
cd vault-math && claude
cd vault-cs && claude
```

每个 vault 共享同一套 scripts 和 requirements，但有独立的 _schema、_memory 和 wiki 目录。

---

## 附录：快速参考卡

### 常用命令

```
/wiki:ingest <path>                      导入源材料
/wiki:query <question>                   查询知识
/wiki:check                              只读诊断（不修改文件）
/wiki:lint                               健康检查 + 自动修复
/wiki:journal daily                      创建日记
/wiki:review weekly                      每周回顾
/wiki:consolidate                        记忆整理
/wiki:crystallize                        会话结晶
/wiki:qa-import <path>                   导入 QA 数据
/wiki:ingest-loop <dir> [--engine=qwen]  Ralph-loop 批量 ingest
/wiki:build                              构建 graph + statistics + wiki HTML
/wiki:relink                             自动链接未链接术语（最长匹配优先）
/wiki:reorganize-raw                     重分类 raw/ 到嵌套目录 + 更新 wiki 引用
/wiki:maintain                           一键维护: reorganize-raw→relink→reindex→check→lint→build
```

### 常用脚本

```bash
python3 scripts/bm25_index.py build              重建搜索索引
python3 scripts/bm25_index.py query "关键词"      搜索
python3 scripts/build_graph.py                    构建知识图谱
python3 scripts/lint_wiki.py                      运行 lint
bash scripts/watch-raw.sh                         文件监控
bash scripts/cron-setup.sh                        安装定时任务
```

### 关键路径

```
vault/_schema/CLAUDE.md          系统规则
vault/index.md                   内容目录
vault/log.md                     操作日志
vault/graph.json                 图谱数据
vault/index/BM25/                搜索索引
```
