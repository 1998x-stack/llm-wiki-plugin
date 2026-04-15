# Wiki 系统命令参考手册

> 本文档完整描述 Obsidian Brain 知识系统的所有命令、钩子、自动化脚本和 Python 工具。
> 所有命令通过 `/wiki:<命令名>` 调用（在 vault/ 目录下运行 Claude Code）。

---

## 目录

1. [命令一览](#命令一览)
2. [知识录入命令](#知识录入命令)
   - [wiki:ingest](#wikiingest)
   - [wiki:ingest-loop](#wikiingest-loop)
3. [知识查询命令](#知识查询命令)
   - [wiki:query](#wikiquery)
4. [知识维护命令](#知识维护命令)
   - [wiki:check](#wikicheck)
   - [wiki:lint](#wikilint)
   - [wiki:build](#wikibuild)
   - [wiki:maintain](#wikimaintain)
   - [wiki:consolidate](#wikiconsolidate)
5. [知识沉淀命令](#知识沉淀命令)
   - [wiki:crystallize](#wikicrystallize)
6. [日志与反思命令](#日志与反思命令)
   - [wiki:journal](#wikijournal)
   - [wiki:review](#wikireview)
7. [数据导入命令](#数据导入命令)
   - [wiki:qa-import](#wikiqa-import)
   - [wiki:convert-to-markdown](#wikiconvert-to-markdown)
8. [PostToolUse 钩子](#posttooluse-钩子)
9. [Cron 自动化](#cron-自动化)
10. [文件监控](#文件监控)
11. [Python 脚本参考](#python-脚本参考)

---

## 命令一览

| 命令 | 用途 | 输入 | 主要输出 |
|------|------|------|----------|
| `wiki:ingest` | 源材料 → wiki 页面 | 文件路径 / `all` | wiki 页面 + log.md |
| `wiki:ingest-loop` | ralph-loop 批量 ingest | `<path> [--engine=qwen]` | 批量 wiki 页面 |
| `wiki:query` | 统一搜索 (BM25+maps+graph) + 回答 | 问题文本 | 回答 + 可选 synthesis 页面 |
| `wiki:check` | 只读健康诊断 (A-I 项) | 无 | 检查报告（不修改文件） |
| `wiki:lint` | 健康检查 + 自动修复 | 无 | lint 报告 + 自动修复 |
| `wiki:build` | 构建所有静态产出 | 无 | graph.json + statistics + wiki HTML |
| `wiki:relink` | 自动链接未链接的术语提及（最长匹配优先） | 无 | 修改后的 wiki 页面 |
| `wiki:reorganize-raw` | 重分类 raw/ 到嵌套目录 + 更新 wiki 引用 | 无 | re-map.json + raw-wiki-map.json |
| `wiki:maintain` | 一键维护 (reorganize-raw→relink→reindex→check→lint→build) | 无 | 索引 + 诊断 + 静态产出 |
| `wiki:consolidate` | 记忆晋升 + 衰减 | `--deep`（可选） | 记忆层更新 |
| `wiki:crystallize` | 会话 → 结构化摘要 | 主题描述（可选） | working memory + 可选 synthesis |
| `wiki:journal` | 日记 / 反思 / 判断 | `daily` / `reflection` / `judgment` | journal 文件 |
| `wiki:review` | 分形回顾 | `weekly` / `monthly` / `quarterly` | 回顾报告 |
| `wiki:qa-import` | QA 数据 → 洞见 | QA 文件路径 / `all` | qa-insight 页面 |
| `wiki:convert-to-markdown` | markitdown 批量转换 | 子目录路径/无 | 转换后的 .md 文件 |

---

## 知识录入命令

### wiki:ingest

**用途**：读取 `raw/` 中的源材料，提取实体和概念，编译为结构化的 wiki 页面。这是知识录入的核心命令。

**输入格式**：

```
/wiki:ingest <文件路径>
```

- `<文件路径>`：相对于 `vault/raw/` 的路径，例如 `textbooks/chapter1.md`
- 传入 `all` 处理所有尚未被 ingest 的文件

**支持的文件格式**：`.md`、`.pdf`、`.docx`、`.jsonl`

**执行流程**：

1. **读取源文件** — 完整阅读 `raw/<文件路径>`，根据格式选择解析方式
2. **提取实体和概念** — 识别人物、公司、项目、工具、论文、书籍等实体，以及核心概念和主题。参考 `_schema/entity-types.md` 确定类型
3. **查找已有页面** — 读取 `index.md`，对每个提取项检查是否已有对应 wiki 页面
4. **创建或更新页面** — 新实体写入 `wiki/entities/`，新概念写入 `wiki/concepts/`，已有页面追加新信息并更新 confidence 和 source_count。文件名用自然中文
5. **建立关系** — 在 frontmatter `relates_to` 中添加关系（参考 `_schema/relationship-types.md`），同时更新被关联页面（双向）
6. **矛盾检查** — 新信息与已有页面矛盾时，添加 `type: contradicts` 关系；新信息更可靠时用 `supersedes` 标记旧声明
7. **更新 index.md** — 在对应分类下添加 `- [[页面名]] — 一行摘要 (confidence: X.X)`
8. **更新 log.md** — 追加 `## [YYYY-MM-DD] ingest | 源文件名`，列出创建和更新的页面

**示例**：

```
/wiki:ingest textbooks/数值分析/第三章.md
```

期望输出：

```
处理完成：textbooks/数值分析/第三章.md
- 创建了 3 个新页面：[[牛顿法]], [[割线法]], [[收敛阶]]
- 更新了 1 个已有页面：[[艾萨克·牛顿]]
- 发现了 0 个矛盾
```

```
/wiki:ingest all
```

期望输出：

```
批量处理完成：
- 源文件：5 个
- 创建了 12 个新页面
- 更新了 4 个已有页面
- 发现了 1 个矛盾：[[欧拉方法]] vs [[改进欧拉方法]] 关于稳定性边界
```

**质量要求**：每个新页面必须满足 `_schema/quality-rules.md` 中的标准——完整 frontmatter、概述不超 200 字、至少 1 个来源引用、至少 1 个 relates_to 关系。

---

### wiki:ingest-loop

**用途**：使用 ralph-loop 机制对一个文件夹中的所有文件逐个执行 `wiki:ingest`。自动管理进度状态，支持中断恢复。

**输入格式**：

```
/wiki:ingest-loop <文件夹路径>
```

- `<文件夹路径>`：相对于 vault 的路径，例如 `raw/textbooks/数值分析`

**前置条件**：需要 ralph-loop 插件支持。

**执行流程**：

1. **初始化** — 运行 `scripts/setup-ingest-loop.sh <路径>`，扫描目标文件夹内所有 `.md`、`.pdf`、`.docx`、`.jsonl` 文件
2. **创建状态文件** — 在 `.claude/ingest-loop.local.md` 写入 YAML 状态，包含文件列表、当前进度、session ID
3. **循环执行** — ralph-loop 逐个文件调用 `wiki:ingest`，每完成一个文件更新状态文件中的 `current_index` 和 `completed`
4. **完成承诺** — 所有文件处理完毕后输出 `<promise>ALL_FILES_INGESTED</promise>`

**状态文件格式**（`.claude/ingest-loop.local.md`）：

```yaml
---
active: true
source_path: "raw/textbooks/数值分析"
files:
  - "raw/textbooks/数值分析/第一章.md"
  - "raw/textbooks/数值分析/第二章.md"
current_index: 0
total: 2
completed: []
failed: []
started_at: "2026-04-15T10:00:00Z"
session_id: "uuid"
completion_promise: "ALL_FILES_INGESTED"
---
```

**示例**：

```
/wiki:ingest-loop raw/textbooks/数值分析
```

期望输出：

```
=== Ingest Loop Setup ===
Source: raw/textbooks/数值分析
Files to process: 8
State file: .claude/ingest-loop.local.md

[1/8] 处理 raw/textbooks/数值分析/第一章.md ... 完成
[2/8] 处理 raw/textbooks/数值分析/第二章.md ... 完成
...
[8/8] 处理 raw/textbooks/数值分析/第八章.md ... 完成

<promise>ALL_FILES_INGESTED</promise>
```

**中断恢复**：如果中途中断，再次执行同一命令会从 `current_index` 处继续。删除状态文件可取消循环。

---

### Qwen 引擎模式

使用 `--engine=qwen` 切换到 Qwen API 引擎：

```
/wiki:ingest-loop raw/papers --engine=qwen
```

**Qwen 模式前置条件**：环境变量 `DASHSCOPE_API_KEY` 已设置，已安装 `openai` + `pyyaml`。

**Qwen 模式差异**：使用 `qwen_ingest.py` 调用 Qwen3-Plus API 提取知识，不占用 Claude 上下文，适合大批量处理。

---

## 知识查询命令

### wiki:query

**用途**：基于知识库回答问题。通过 `search_wiki.py` 统一搜索（BM25 + maps/ 主题扩展 + graph.json 遍历 + RRF 融合），综合读取相关页面内容。如果回答形成了新洞见，自动结晶为 synthesis 页面。

**输入格式**：

```
/wiki:query <问题>
```

- `<问题>`：自然语言问题

**执行流程**：

1. **搜索相关页面**
   - 调用 `scripts/search_wiki.py "<问题>" --top 15` 执行统一搜索：
     - BM25 全文检索
     - maps/ 主题地图扩展
     - graph.json 图关系遍历
     - RRF（Reciprocal Rank Fusion）融合排序
   - 取返回的 top-N 页面作为候选

2. **读取相关页面** — 读取所有找到的页面完整内容，注意 confidence 值——低置信度信息标注"（置信度较低）"

3. **综合回答** — 中文回答，引用来源：`来源：[[页面名]]`。信息不足时明确说明

4. **结晶化判断** — 如果回答综合了 3+ 个页面且形成新洞见，自动在 `wiki/syntheses/` 创建新页面，更新 index.md 和 log.md

5. **更新 last_accessed** — 更新所有被引用页面的 `last_accessed` 字段

**示例**：

```
/wiki:query 龙格现象和切比雪夫逼近之间有什么联系？
```

期望输出：

```
龙格现象和切比雪夫逼近之间存在深刻联系：

龙格现象指的是在等距节点上进行高阶多项式插值时，插值函数在
区间端点附近出现剧烈振荡的现象。切比雪夫逼近理论正是解决这一
问题的关键方案——通过使用切比雪夫节点（余弦分布的非等距节点）
代替等距节点，可以将插值误差的上界最小化……

来源：[[龙格现象]], [[切比雪夫逼近理论]], [[切比雪夫多项式]], [[谱半径]]

---
已自动创建综合页面：wiki/syntheses/龙格现象与切比雪夫逼近的联系.md
```

```
/wiki:query 这个知识库里有哪些数值线性代数的人物？
```

期望输出：

```
知识库中涉及数值线性代数的人物包括：

1. [[阿尔斯顿·豪斯霍尔德]]（1904-1993）— Householder 变换提出者，数值线性代数学科建设先驱
2. [[吉恩·戈卢布]]（1932-2007）— Golub-Kahan SVD 算法，《Matrix Computations》作者
3. [[威廉·卡汉]]（1933-）— IEEE 754 浮点标准主要架构师，1989 年图灵奖

来源：[[阿尔斯顿·豪斯霍尔德]], [[吉恩·戈卢布]], [[威廉·卡汉]]
```

---

## 知识维护命令

### wiki:check

**用途**：对知识库进行只读健康诊断（不修改任何文件）。运行全部 A-I 检查项 + 语义检查，生成诊断报告。

**输入格式**：

```
/wiki:check
```

无需参数。输出 ERROR / WARNING / INFO 分类报告，但不执行任何修复。适合 CI 或审查场景。

---

### wiki:lint

**用途**：健康检查 + 自动修复。先调用 `wiki:check` 获取问题清单，然后对可修复项执行自动修复。

**输入格式**：

```
/wiki:lint
```

无需参数。

**检查项（A-I）**：

| 检查代码 | 名称 | 说明 | 严重度 |
|----------|------|------|--------|
| A / F1 | Frontmatter 完整性 | 检查所有必需字段是否存在 | error |
| B / F2 | Frontmatter 格式 | YAML 是否可解析 | error |
| C / F3 | 概述长度 | 概述是否超过 200 字 | warning |
| D / F4 | 空段落 | 是否存在无内容的 section | warning |
| E / B1 | 断链检查 | `[[链接]]` 指向不存在的页面 | warning |
| F / B2 | BM25 一致性 | 页面是否在 BM25 docmap 中 | warning |
| G / I1 | Index 缺失 | 页面是否出现在 index.md 中 | warning |
| H / I2 | Index 过期 | index.md 中是否有指向已删除页面的条目 | warning |
| I / O1 | 孤页检查 | 是否存在没有入链的页面 | warning |

**自动修复规则**：

| 问题 | 修复方式 |
|------|----------|
| 缺失的 frontmatter 字段 | 填入默认值（confidence 根据 source_count 估算） |
| 断裂的 `[[链接]]` | 存在近似页面则修正，否则标记为待创建 |
| confidence 未设置 | 1 源 = 0.5, 2 源 = 0.7, 3+ 源 = 0.85 |
| 页面未出现在 index.md | 自动添加到 index.md |
| 孤页 | 尝试找到相关页面添加链接 |

**执行流程**：

1. 扫描所有 `wiki/` 页面，解析 frontmatter
2. 逐项执行 A-I 检查（H / I2 孤页检查读取现有 `graph.json`，不重建图谱）
3. 自动修复可修复的问题
4. 生成 lint 报告追加到 `log.md`
5. 更新 `dashboard.md` 的"最近 lint"日期

**示例**：

```
/wiki:lint
```

期望输出：

```
Lint Report 2026-04-15

- 扫描页面数：42
- 问题总数：7
- 自动修复：4
- 需要人工处理：3

详情：
- [牛顿法]: 缺失 last_accessed 字段 → 已修复（填入今日日期）
- [割线法]: 未出现在 index.md → 已修复（已添加）
- [欧拉方法]: 概述 256 字超过 200 字限制 → 待处理
- [高斯消元]: 孤页，无入链 → 已在 [[数值线性代数]] 中添加链接
- [快速傅里叶变换]: 断链 [[蝴蝶运算]] 不存在 → 待创建
- [舍入误差]: confidence=0.2，标记为 stale → 已修复
- [样条插值]: 未在 BM25 docmap 中 → 待处理（需执行 BM25 rebuild）
```

---

### wiki:build

**用途**：构建所有静态产出：graph.json、graph-statistics.json、static/wiki/ HTML 页面。

**输入格式**：

```
/wiki:build
```

无需参数。

**执行流程**：

1. 先执行 lint 预检查（只读）确保数据健康
2. 调用 `scripts/build_graph.py` 构建图谱：
   - 第一遍扫描：从所有 wiki 页面的 frontmatter 构建节点（id、label、type、confidence、tags）
   - 第二遍扫描：从 frontmatter `relates_to` 提取带类型的边，从正文 `[[双链]]` 提取 wikilink 边
   - 边去重（无向键 + 关系类型）
   - BFS 计算连通分量
   - 识别孤页（edge_count = 0 的单节点分量）
3. 输出 `vault/graph.json`

**graph.json 结构**：

```json
{
  "metadata": {
    "generated": "2026-04-15T12:00:00+00:00",
    "total_nodes": 42,
    "total_edges": 87,
    "orphan_count": 3,
    "component_count": 5
  },
  "nodes": [
    {
      "id": "wiki/concepts/牛顿法.md",
      "label": "牛顿法",
      "type": "concept",
      "confidence": 0.85,
      "tags": ["技术", "方法论"],
      "edge_count": 6
    }
  ],
  "edges": [
    {
      "source": "wiki/concepts/牛顿法.md",
      "target": "wiki/entities/艾萨克·牛顿.md",
      "relation": "caused",
      "bidirectional": false
    }
  ],
  "orphans": ["wiki/concepts/某孤立概念.md"],
  "components": [
    {"id": 0, "size": 35, "nodes": ["..."]}
  ]
}
```

**示例**：

```
/wiki:build
```

期望输出：

```
Lint: 42 files, 2 warnings, 0 errors.

Graph build complete:
  nodes: 42
  edges: 87
  orphans: 3
  components: 5

Output: vault/graph.json
```

---

### wiki:maintain

**用途**：一键执行完整知识库维护流水线：reorganize-raw → reindex → check → build。等价于依次运行四个子命令，但在关键步骤失败时提前终止。

**输入格式**：

```
/wiki:maintain
```

无需参数。

**执行流程**：

1. **Reindex** — 验证 index.md 完整性，修复缺失/孤条目，保存快照，按 tags 构建主题分类，生成 `maps/*.md`
2. **Check** — 运行 `lint_wiki.py --json` + A-I 全部检查项 + 语义检查，生成诊断报告
3. **Lint** — 基于诊断结果自动修复（frontmatter、断链、index.md、BM25），生成 lint 报告
4. **Build** — 构建 graph.json + statistics + wiki HTML，同步到 `static/`

**终止条件**：步骤 1 脚本异常时终止。步骤 2-4 的 warnings 不阻断流程。

**适用场景**：
- 批量 ingest 后的全面维护
- 每周例行维护（替代手动 lint + build）
- 发布前检查

**示例**：

```
/wiki:maintain
```

期望输出：

```
=== wiki:maintain 完成 ===

[1/4] Reindex — OK (121 页面, 5 clusters)
[2/4] Check — 0 errors, 3 warnings, 2 info
[3/4] Lint — 2 修复, 1 待处理
[4/4] Build — 121 节点, 245 边 → static/ 已同步
```

---

### wiki:consolidate

**用途**：执行记忆层的晋升和衰减。管理 Working → Episodic → Semantic → Procedural 四层知识生命周期。

**输入格式**：

```
/wiki:consolidate [--deep]
```

- 无参数：执行日常整合（Working→Episodic、Episodic→Semantic、置信度衰减）
- `--deep`：增加 Semantic→Procedural 晋升和月度/季度报告

**四层记忆系统**：

| 层级 | 目录 | 内容 | 晋升条件 |
|------|------|------|----------|
| Working | `_memory/working/` | 会话级临时观察 | 会话结束自动压缩 |
| Episodic | `_memory/episodic/` | 按天聚合的观察 | — |
| Semantic | `_memory/semantic/` | 跨多天反复确认的事实 | 3+ 个 episode 重复 |
| Procedural | `_memory/procedural/` | 稳定的行为模式/工作流 | 5+ 个 semantic 描述同一模式 |

**执行流程**：

1. **Working → Episodic 压缩**
   - 扫描 `_memory/working/` 中 `status=unprocessed` 的文件
   - 提取关键观察，合并到当天的 `_memory/episodic/YYYY-MM-DD.md`
   - 标记 working memory 为 `status: processed`

2. **Episodic → Semantic 晋升**
   - 扫描最近 30 天的 episodic 文件
   - 找出 3+ 个不同 episode 中重复出现的事实
   - 创建或更新 `_memory/semantic/` 条目（每次确认 confidence +0.05，上限 0.95）

3. **置信度衰减**（Ebbinghaus 遗忘曲线）
   - 扫描所有 semantic memory
   - 按 decay_rate 计算新 confidence：
     - `slow`（半衰期 180 天）：`confidence * 0.5^(days/180)` — 用于架构决策、核心概念
     - `medium`（半衰期 60 天）：`confidence * 0.5^(days/60)` — 用于一般事实
     - `fast`（半衰期 14 天）：`confidence * 0.5^(days/14)` — 用于临时 bug、短期观察
   - confidence < 0.3 → 标记 `status=stale`

4. **Journal 模式扫描**
   - 扫描最近 7 天的 daily notes
   - 同一链接/关键词 3+ 天出现 → 记录到 log.md
   - 5+ 次同类决策偏向 → 更新 `journal/growth/cognitive-patterns.md`
   - 提及频率增长的领域 → 更新 `journal/growth/skills-tracker.md`

5. **深度整合**（仅 `--deep`）
   - Semantic → Procedural 晋升：confidence >= 0.8 且 5+ 个描述同一模式
   - 月初生成月度报告，季初生成季度报告到 `journal/growth/quarterly/`

**示例**：

```
/wiki:consolidate
```

期望输出：

```
Consolidate 完成（2026-04-15）：
- Working → Episodic：处理了 3 个 working memory
- Episodic → Semantic：晋升了 2 个新 semantic memory
- 置信度衰减：更新了 15 个 semantic memory，其中 1 个标记为 stale
- Journal 模式：发现 "数值稳定性" 在过去 7 天提及 4 次
```

```
/wiki:consolidate --deep
```

期望输出：

```
Deep Consolidate 完成（2026-04-15）：
- Working → Episodic：处理了 1 个 working memory
- Episodic → Semantic：晋升了 0 个（无新重复）
- 置信度衰减：更新了 15 个，0 个 stale
- Journal 模式：无新发现
- Semantic → Procedural：提取了 1 个新 procedural（"迭代法收敛判断流程"）
- 月度报告：已生成 journal/growth/2026-04.md
```

---

## 知识沉淀命令

### wiki:crystallize

**用途**：将当前对话会话中的探索过程蒸馏为结构化摘要，写入 working memory 和可选的 wiki synthesis 页面。用于在会话结束前保存有价值的发现。

**输入格式**：

```
/wiki:crystallize [主题描述]
```

- `主题描述`：可选。不提供时自动从当前对话上下文推断。

**执行流程**：

1. **回顾当前会话** — 分析本次对话讨论了什么，识别关键发现、决策、洞见
2. **写入 Working Memory** — 创建 `_memory/working/YYYY-MM-DD-NN.md`，记录会话的关键观察
3. **结晶化判断** — 如果会话连接了 3+ 个已有概念形成新洞见，在 `wiki/syntheses/` 创建新页面
4. **强化已有知识** — 如果会话确认了已有 semantic memory 中的事实，更新 `last_confirmed` 和 `confirmation_count`，重置衰减曲线
5. **记录** — 追加 log.md

**Working Memory 文件格式**：

```yaml
---
type: working-memory
session: 2026-04-15-01
created: 2026-04-15T14:30:00
status: unprocessed
observations: 5
---
```

**示例**：

```
/wiki:crystallize 数值稳定性与条件数的关系探索
```

期望输出：

```
Crystallize 完成：

Working Memory：
  写入 _memory/working/2026-04-15-01.md
  观察数：5
    1. 条件数决定了问题本身的敏感度，而稳定性描述算法的误差放大行为
    2. 良态问题 + 不稳定算法 → 仍可能得到错误结果
    3. 后向稳定性分析是现代数值分析的核心工具
    ...

结晶化：
  已创建 wiki/syntheses/数值稳定性与条件数的统一视角.md
  关联了 [[条件数]], [[后向误差分析]], [[浮点运算]], [[威廉·卡汉]]

已更新 semantic memory：
  - "浮点运算需要后向稳定性保证" — confirmation_count: 3 → 4
```

---

## 日志与反思命令

### wiki:journal

**用途**：辅助创建日记、反思或判断文档，自动链接到相关知识页面。

**输入格式**：

```
/wiki:journal <类型> [主题]
```

三种类型：

| 类型 | 说明 | 输出目录 | 模板 |
|------|------|----------|------|
| `daily` | 今日 daily note | `journal/daily/` | `templates/daily.md` |
| `reflection <主题>` | 针对某主题的深度反思 | `journal/reflections/` | `templates/reflection.md` |
| `judgment <主题>` | 针对某决策的判断记录 | `journal/judgments/` | `templates/judgment.md` |

**执行流程**：

**daily**：
1. 检查 `journal/daily/YYYY-MM-DD.md` 是否已存在
2. 不存在 → 用 `templates/daily.md` 创建，替换 `{{date}}`
3. 已存在 → 读取现有内容
4. 从 index.md 找到最近 ingest 的主题，在"相关"部分建议链接

**reflection**：
1. 用 `templates/reflection.md` 创建 `journal/reflections/<主题>.md`
2. 替换 `{{date}}` 和 `{{title}}`
3. 搜索 wiki 中与主题相关的页面，在"相关"部分添加 `[[链接]]`
4. 追加 log.md

**judgment**：
1. 用 `templates/judgment.md` 创建 `journal/judgments/<主题>.md`
2. 替换 `{{date}}` 和 `{{title}}`
3. 搜索 wiki 中与主题相关的页面，在"相关知识"部分添加 `[[链接]]`
4. 追加 log.md

**示例**：

```
/wiki:journal daily
```

期望输出：

```
已创建 journal/daily/2026-04-15.md

建议关联的近期主题：
- [[龙格现象]]（昨日 ingest）
- [[切比雪夫多项式]]（昨日 ingest）
- [[样条方法]]（3 天前 ingest）
```

```
/wiki:journal reflection 为什么我总是低估数学基础的重要性
```

期望输出：

```
已创建 journal/reflections/为什么我总是低估数学基础的重要性.md

已链接相关知识：
- [[数值稳定性]]
- [[条件数]]
- [[浮点运算]]
```

```
/wiki:journal judgment 选择 Jacobi 迭代还是 Gauss-Seidel
```

期望输出：

```
已创建 journal/judgments/选择Jacobi迭代还是Gauss-Seidel.md

已链接相关知识：
- [[Jacobi迭代法]]
- [[Gauss-Seidel方法]]
- [[谱半径]]
```

---

### wiki:review

**用途**：kepano 式分形回顾。扫描近期 journal 内容，辅助升维和建立连接。支持周/月/季三个层级。

**输入格式**：

```
/wiki:review [weekly|monthly|quarterly]
```

- 默认 `weekly`

**三个层级**：

| 层级 | 扫描范围 | 输出 | 额外功能 |
|------|----------|------|----------|
| weekly | 过去 7 天 | `journal/daily/YYYY-WNN.md` | 高频主题识别、链接补全 |
| monthly | 过去 30 天 | 周报基础上的月度总结 | 合并建议、skills-tracker 更新 |
| quarterly | 过去 90 天 | 季度成长报告 | cognitive-patterns 更新、趋势分析 |

**weekly 执行流程**：

1. **收集素材** — 读取过去 7 天的 daily notes + reflections + judgments
2. **生成周报草稿** — 用 `templates/weekly-review.md` 创建 `journal/daily/YYYY-WNN.md`，填充本周事件和新发现的连接
3. **升维建议**：
   - 同一概念 3+ 天被提到 → 如果 wiki 中没有对应概念页，建议创建并提供草稿
   - 识别值得升级为正式 reflection 或 judgment 的 daily 内容
4. **链接补全** — 检查 daily notes 中提到但未加 `[[链接]]` 的概念，自动补充
5. **记录** — 追加 log.md

**monthly 增加**：扫描本月所有 reflections 和 judgments，提议可合并为 `wiki/syntheses/` 的综合页面；更新 `journal/growth/skills-tracker.md`

**quarterly 增加**：生成 `journal/growth/quarterly/YYYY-QN.md` 季度成长报告；更新 `journal/growth/cognitive-patterns.md`；分析技能领域变化趋势

**示例**：

```
/wiki:review weekly
```

期望输出：

```
Weekly Review 2026-W16 (04-09 ~ 04-15)

本周发生了什么：
- 完成了数值分析教材第 3-5 章的 ingest（12 个新页面）
- 写了 2 篇 reflection
- 做了 1 个 judgment

新的连接和发现：
- [[龙格现象]] ↔ [[切比雪夫逼近理论]]：等距 vs 非等距节点的本质区别
- [[Jacobi迭代法]] ↔ [[Gauss-Seidel方法]]：收敛速度的关系

升维建议：
- "数值稳定性" 在 4 天被提及 → 建议创建 wiki/concepts/数值稳定性.md
- 04-12 的 daily note 中关于 "浮点误差累积" 的讨论值得升级为 reflection

链接补全：
- journal/daily/2026-04-11.md：补充了 [[样条方法]] 链接
- journal/daily/2026-04-13.md：补充了 [[谱半径]] 链接
```

```
/wiki:review quarterly
```

期望输出：

```
Quarterly Review 2026-Q1 (01-01 ~ 03-31)

已生成：journal/growth/quarterly/2026-Q1.md

技能领域变化：
- 数值分析：提及频率 +180%，从"学习"转入"应用"
- 知识图谱：提及频率 +50%，维持在"探索"阶段

认知模式更新：
- cognitive-patterns.md：新增 "倾向于先理解理论再看代码实现"
```

---

## 数据导入命令

### wiki:qa-import

**用途**：批量导入 QA 对话数据（如 ChatGPT 导出、自定义 JSONL），按主题聚类后提取有知识价值的洞见，写入 wiki。

**输入格式**：

```
/wiki:qa-import <文件路径>
```

- `<文件路径>`：相对于 `vault/raw/qa/` 的路径
- 传入 `all` 处理所有 QA 文件

**支持的格式**：

| 格式 | 说明 |
|------|------|
| `.jsonl` | 每行一个 JSON 对象，必须有 `question` 和 `answer` 字段 |
| `.md` | ChatGPT 导出格式（Prompt / Response 交替） |

**执行流程**：

1. **解析 QA 数据** — 读取源文件，提取所有 Q&A 对，记录行号/位置
2. **主题聚类** — 将 QA 按主题分组，标注主题关键词
3. **提取洞见** — 对每个聚类提取跨多个 QA 的关键发现，过滤纯操作性内容，评估 confidence
4. **创建洞见页面** — 在 `wiki/qa-insights/` 创建页面
5. **建立双向链接** — 找到 wiki 中已有的相关页面，双向添加 `relates_to`
6. **更新 index.md 和 log.md**

**QA Insight 页面 frontmatter**：

```yaml
---
type: qa-insight
source_file: "raw/qa/chatgpt-export.jsonl"
source_lines: [15, 23, 47]
topics: ["数值稳定性", "浮点运算"]
confidence: 0.7
created: 2026-04-15
status: active
tags: ["技术"]
aliases: []
relates_to:
  - target: "[[浮点运算]]"
    type: extends
    confidence: 0.7
---
```

**示例**：

```
/wiki:qa-import chatgpt-export.jsonl
```

期望输出：

```
QA Import 完成：chatgpt-export.jsonl

- 解析了 156 个 QA 对
- 聚类为 12 个主题
- 提取了 5 个高价值洞见：
  1. wiki/qa-insights/浮点运算中的灾难性消去.md (confidence: 0.8)
  2. wiki/qa-insights/迭代法收敛的充分条件.md (confidence: 0.7)
  3. wiki/qa-insights/稀疏矩阵存储格式选择策略.md (confidence: 0.75)
  4. wiki/qa-insights/条件数与误差放大的实践经验.md (confidence: 0.65)
  5. wiki/qa-insights/数值积分精度与效率的权衡.md (confidence: 0.7)
- 过滤了 7 个纯操作性聚类
- 建立了 12 个双向链接
```

---

### wiki:convert-to-markdown

**用途**：使用 markitdown 将 `raw/` 中的 PDF、DOCX 等非 Markdown 文件批量转换为 `.md` 文件，供后续 `wiki:ingest` 使用。

**输入格式**：

```
/wiki:convert-to-markdown [子目录路径]
```

- `子目录路径`：相对于 `vault/raw/` 的子目录，例如 `papers`。不提供则处理 `raw/` 下所有支持格式的文件。

**支持的格式**：`.pdf`、`.docx`、`.pptx`、`.xlsx`、`.html` 等 markitdown 支持的格式。

**执行流程**：

1. 扫描目标目录，找出所有非 `.md` 的可转换文件
2. 对每个文件调用 `markitdown <文件>` 输出同名 `.md` 文件（覆盖已有文件时给出提示）
3. 输出转换摘要

**示例**：

```
/wiki:convert-to-markdown papers
```

期望输出：

```
Convert to Markdown: raw/papers
转换完成：3 个文件
  - raw/papers/论文A.pdf → raw/papers/论文A.md
  - raw/papers/报告B.docx → raw/papers/报告B.md
  - raw/papers/slides.pptx → raw/papers/slides.md
跳过：0 个（已是 .md）
```

---

## PostToolUse 钩子

钩子定义在 `.claude/settings.local.json` 的 `hooks.PostToolUse` 中。每当 Claude 执行 `Write` 或 `Edit` 操作且文件路径包含 `wiki/` 时，三个钩子依次触发。

### 钩子配置

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "bash vault/scripts/hook_lint.sh \"$CLAUDE_TOOL_ARG_file_path\"",
        "description": "Lint wiki pages after modification"
      },
      {
        "matcher": "Write|Edit",
        "command": "bash vault/scripts/hook_bm25.sh \"$CLAUDE_TOOL_ARG_file_path\"",
        "description": "Update BM25 index after wiki modification"
      },
      {
        "matcher": "Write|Edit",
        "command": "bash vault/scripts/hook_graph.sh \"$CLAUDE_TOOL_ARG_file_path\"",
        "description": "Rebuild knowledge graph after wiki modification"
      }
    ]
  }
}
```

### hook_lint.sh

**触发条件**：Write/Edit 操作，且文件路径包含 `wiki/`

**行为**：调用 `lint_wiki.py --file <路径> --json`，对刚修改的单个 wiki 页面执行 lint 检查

**日志输出**（写入 `log.hook.md`）：
- 通过：`[2026-04-15 14:30] LINT wiki/concepts/牛顿法.md — OK`
- 警告：`[2026-04-15 14:30] LINT wiki/concepts/牛顿法.md — WARN: Missing frontmatter fields: last_accessed`
- 错误：`[2026-04-15 14:30] LINT wiki/concepts/牛顿法.md — ERROR: ...`

### hook_bm25.sh

**触发条件**：Write/Edit 操作，且文件路径包含 `wiki/`

**行为**：调用 `bm25_index.py update <路径>`，将修改后的页面增量更新到 BM25 索引

**日志输出**：
- 成功：`[2026-04-15 14:30] BM25 wiki/concepts/牛顿法.md — indexed`
- 失败：`[2026-04-15 14:30] BM25 wiki/concepts/牛顿法.md — error: ...`

### hook_graph.sh

**触发条件**：Write/Edit 操作，且文件路径包含 `wiki/`

**行为**：调用 `build_graph.py` 完整重建 `graph.json`

**日志输出**：
- 成功：`[2026-04-15 14:30] GRAPH rebuild — OK`
- 失败：`[2026-04-15 14:30] GRAPH rebuild — error: ...`

**注意**：三个钩子独立运行，任一个失败不会阻断其他钩子。所有日志统一写入 `vault/log.hook.md`。

---

## Cron 自动化

通过 `scripts/cron-setup.sh` 安装定时任务。

### 安装

```bash
cd vault
bash scripts/cron-setup.sh
```

### 已配置的定时任务

| 时间 | cron 表达式 | 命令 | 说明 |
|------|------------|------|------|
| 每日 02:07 | `7 2 * * *` | `/wiki:consolidate` | 日常记忆整合：Working→Episodic→Semantic 晋升 + 置信度衰减 |
| 每周日 20:13 | `13 20 * * 0` | `/wiki:lint` + `/wiki:review weekly` | 周末维护：lint 健康检查 + 周回顾 |
| 每月 1 号 03:17 | `17 3 1 * *` | `/wiki:consolidate --deep` | 月度深度整合：含 Semantic→Procedural 晋升和月度报告 |

### 管理

```bash
# 查看已安装的 cron
crontab -l

# 重新安装（幂等操作，会先清除旧的再安装）
bash scripts/cron-setup.sh

# 删除所有 cron
crontab -r
```

**日志位置**：`vault/data/cron.log`

---

## 文件监控

### watch-raw.sh

**用途**：监控 `raw/` 目录，新文件出现时自动触发 `wiki:ingest`。

**依赖**：`fswatch`（`brew install fswatch`）

**启动**：

```bash
cd vault
bash scripts/watch-raw.sh
```

**行为**：

1. 使用 `fswatch` 监听 `raw/` 目录的 `Created` 事件
2. 忽略隐藏文件（以 `.` 开头的文件名）
3. 新文件出现时，计算相对路径并调用 `claude -p "/wiki:ingest <相对路径>"`
4. 输出最近 5 行处理结果

**输出示例**：

```
Watching /Users/xd/.../vault/raw/ for new files...
Press Ctrl+C to stop.

[2026-04-15 15:30:12] New file detected: /Users/xd/.../vault/raw/papers/new-paper.md
Triggering ingest for: papers/new-paper.md
创建了 2 个新页面：[[注意力机制]], [[Transformer]]
更新了 1 个已有页面：[[深度学习]]
---
```

**停止**：`Ctrl+C`

---

## Python 脚本参考

所有脚本位于 `vault/scripts/`。依赖项定义在 `requirements.txt`。

### 依赖安装

```bash
pip install -r requirements.txt
```

依赖列表：

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| `jieba` | >= 0.42 | 中文分词（BM25 索引） |
| `rank_bm25` | >= 0.2.2 | BM25 算法实现 |
| `pyyaml` | >= 6.0 | YAML frontmatter 解析 |
| `openai` | >= 1.0.0 | Qwen API 调用（兼容 OpenAI 接口） |
| `markitdown` | >= 0.1 | PDF/DOCX 等文件转换为 Markdown |

### 脚本速查表

| 脚本 | 用途 | 命令行用法 |
|------|------|-----------|
| `search_wiki.py` | 统一搜索 (BM25+maps+graph+RRF) | 见下文 |
| `search_wiki.py` | 统一搜索 (BM25+maps+graph+RRF) | `python3 scripts/search_wiki.py "<查询>" --top 15 --json` |
| `bm25_index.py` | BM25 全文搜索索引 | 见下文 |
| `build_graph.py` | 知识图谱 JSON 构建 | 见下文 |
| `lint_wiki.py` | Wiki 页面质量检查 | 见下文 |
| `qwen_ingest.py` | Qwen API 知识提取 | 见下文 |
| `setup-ingest-loop.sh` | 批量 ingest 状态初始化 | `bash scripts/setup-ingest-loop.sh <路径>` |
| `setup-ingest-loop-qwen.sh` | Qwen 批量 ingest 状态初始化 | `bash scripts/setup-ingest-loop-qwen.sh <路径>` |
| `hook_lint.sh` | PostToolUse lint 钩子 | 由 hooks 自动调用 |
| `hook_bm25.sh` | PostToolUse BM25 钩子 | 由 hooks 自动调用 |
| `hook_graph.sh` | PostToolUse graph 钩子 | 由 hooks 自动调用 |
| `watch-raw.sh` | 文件监控自动 ingest | `bash scripts/watch-raw.sh` |
| `cron-setup.sh` | 安装定时任务 | `bash scripts/cron-setup.sh` |

### bm25_index.py

BM25 全文搜索索引管理器。使用 jieba 中文分词 + rank_bm25 算法。

**索引存储位置**：`vault/index/BM25/`

| 文件 | 格式 | 内容 |
|------|------|------|
| `corpus.pkl` | pickle | 分词后的文档语料 |
| `index.pkl` | pickle | BM25Okapi 索引对象 |
| `docmap.json` | JSON | 文档 ID → 路径/标题/类型的映射 |

**命令**：

```bash
# 全量重建索引
python3 scripts/bm25_index.py build

# 增量更新单个文件
python3 scripts/bm25_index.py update wiki/concepts/牛顿法.md

# 搜索
python3 scripts/bm25_index.py query "数值稳定性" -n 10

# 从索引中移除文件
python3 scripts/bm25_index.py remove wiki/concepts/已删除的页面.md
```

**搜索输出示例**：

```json
[
  {
    "path": "wiki/concepts/数值稳定性.md",
    "score": 12.3456,
    "title": "数值稳定性",
    "type": "concept"
  },
  {
    "path": "wiki/concepts/条件数.md",
    "score": 8.7654,
    "title": "条件数",
    "type": "concept"
  }
]
```

**分词处理**：去除 frontmatter → 展开 `[[双链]]` 为纯文本 → 清除 Markdown 标记 → jieba 搜索模式分词 → 过滤停用词（中英文）→ 过滤长度 <= 1 的 token。

### build_graph.py

知识图谱 JSON 构建器。扫描所有 wiki 页面，提取节点和边，输出包含连通分量分析的图结构。

**命令**：

```bash
# 构建图谱（默认输出 vault/graph.json）
python3 scripts/build_graph.py

# 指定输出路径
python3 scripts/build_graph.py --output /path/to/graph.json
```

**节点来源**：wiki 页面的 frontmatter（type、confidence、tags）

**边来源**：
- frontmatter `relates_to` 中的条目 → 带关系类型的边（uses、depends_on、contradicts 等）
- 正文中的 `[[双链]]` → `wikilink` 类型的边

**边去重**：以无向节点对 + 关系类型作为键，同一对节点的同一类型关系只保留一条。

**连通分量**：BFS 遍历，识别孤立节点（edge_count = 0 的单节点分量）。

**标准输出**：

```json
{
  "status": "ok",
  "nodes": 42,
  "edges": 87,
  "orphans": 3,
  "components": 5
}
```

### lint_wiki.py

Wiki 页面质量检查器。支持单文件检查（被钩子调用）和全量扫描。

**命令**：

```bash
# 全量扫描
python3 scripts/lint_wiki.py

# 单文件检查
python3 scripts/lint_wiki.py --file wiki/concepts/牛顿法.md

# JSON 输出（钩子模式）
python3 scripts/lint_wiki.py --file wiki/concepts/牛顿法.md --json

# 自动修复（预留，当前未实现）
python3 scripts/lint_wiki.py --fix
```

**检查项**：

| 代码 | 检查内容 | 严重度 |
|------|----------|--------|
| F1 | 缺失必需的 frontmatter 字段（type, status, confidence, created, tags, relates_to） | error |
| F2 | YAML frontmatter 无法解析 | error |
| F3 | 概述部分超过 200 字 | warning |
| F4 | 存在空的段落 | warning |
| B1 | `[[链接]]` 指向不存在的页面 | warning |
| B2 | 页面不在 BM25 docmap 中 | warning |
| I1 | 页面未出现在 index.md 中 | warning |
| I2 | index.md 中有指向已删除页面的条目（仅全量扫描） | warning |
| O1 | 孤页——没有入链（仅全量扫描） | warning |

**退出码**：
- `0`：无问题或仅有 warning
- `2`：有 error

**JSON 输出格式**：

```json
{
  "total_files": 42,
  "errors": 1,
  "warnings": 5,
  "checks": [
    {
      "file": "wiki/concepts/牛顿法.md",
      "check": "F1",
      "severity": "error",
      "message": "Missing frontmatter fields: last_accessed",
      "fixed": false
    }
  ]
}
```

### qwen_ingest.py

使用 Qwen3-Plus API 从源材料自动提取知识并生成结构化 wiki 页面。

**前置条件**：

- 环境变量 `DASHSCOPE_API_KEY`
- `pip install openai pyyaml`

**命令**：

```bash
python3 scripts/qwen_ingest.py --raw raw/papers/论文.md --wiki wiki/concepts/某概念.md
```

**处理流程**：

1. 读取源文件内容
2. 调用 Qwen3-Plus API（DashScope 端点），系统提示词包含完整的页面格式规范
3. 去除 API 返回中可能的代码块包裹（` ```markdown ... ``` `）
4. 对生成的页面执行内置 lint 检查
5. 通过关键检查 → 写入文件；严重错误 → 拒绝写入并报错

**内置 lint 检查**：

| 检查项 | 级别 | 说明 |
|--------|------|------|
| type / title / confidence 缺失 | critical | 阻止写入 |
| 其他 frontmatter 字段缺失 | warning | 允许写入 |
| type 值不合法 | warning | 必须是 entity/concept/synthesis/qa-insight/source-summary |
| confidence 超出 0-1 范围 | warning | — |
| 概述 < 20 字 | critical | 阻止写入 |
| 概述 20-50 字 | warning | — |
| 概述 > 300 字 | warning | — |
| 缺失 `## 概述` 或 `## 关键内容` | critical | 阻止写入 |
| 缺失 `## 来源` 或 `## 相关` | warning | — |
| 正文无 `[[双链]]` | warning | — |

**标准输出**（JSON）：

```json
// 成功
{"status": "SUCCESS", "wiki_path": "wiki/concepts/牛顿法.md"}

// 有警告但已写入
{"status": "LINT_WARNING", "wiki_path": "wiki/concepts/牛顿法.md", "warnings": ["Overview short: 45 chars"]}

// 失败，未写入
{"status": "ERROR", "error": "Lint critical errors", "critical": ["Missing ## 概述 section"], "warnings": [...]}
```

---

## 文件结构总览

```
vault/
├── .claude/
│   ├── commands/wiki/        # 命令定义
│   │   ├── ingest.md
│   │   ├── ingest-loop.md
│   │   ├── query.md
│   │   ├── check.md
│   │   ├── lint.md
│   │   ├── build.md
│   │   ├── reindex.md
│   │   ├── maintain.md
│   │   ├── consolidate.md
│   │   ├── crystallize.md
│   │   ├── journal.md
│   │   ├── review.md
│   │   ├── qa-import.md
│   │   └── convert-to-markdown.md
│   └── settings.local.json   # hooks 配置
├── _schema/
│   ├── CLAUDE.md              # 完整操作规范
│   ├── entity-types.md        # 实体类型定义
│   ├── relationship-types.md  # 关系类型定义
│   └── quality-rules.md       # 质量规则和 lint 报告格式
├── _memory/
│   ├── working/               # 会话级临时记忆
│   ├── episodic/              # 按天聚合的观察
│   ├── semantic/              # 跨天确认的稳定事实
│   └── procedural/            # 行为模式和工作流
├── raw/                       # 不可变源材料（只读）
├── wiki/
│   ├── entities/              # 实体页面
│   ├── concepts/              # 概念页面
│   ├── syntheses/             # 综合分析页面
│   └── qa-insights/           # QA 洞见页面
├── journal/
│   ├── daily/                 # 每日笔记
│   ├── reflections/           # 反思
│   ├── judgments/              # 判断
│   └── growth/                # 成长追踪
├── templates/                 # 模板文件
├── scripts/                   # Python 脚本和 Shell 脚本
├── index/BM25/                # BM25 搜索索引
├── index.md                   # 知识库目录
├── log.md                     # 操作日志
├── log.hook.md                # 钩子执行日志
├── graph.json                 # 知识图谱
└── dashboard.md               # 仪表盘
```
