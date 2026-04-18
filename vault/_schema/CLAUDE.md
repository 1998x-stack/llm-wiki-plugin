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

## Maps 系统

### 是什么

`maps/` 目录存放**按主题自动分类的知识地图文件**，每个文件是一个 topic cluster，汇集归属该主题的所有 wiki 页面。Maps 由 `build_maps.py` 脚本从 `topic-to-wiki.json` 自动生成，包含 `## 概述` 段落和分类型页面清单。**不要手动编辑**。

### 文件格式

```markdown
---
type: map
topic: "AI"
page_count: 62
updated: 2026-04-15
---

# AI

## 概念

- [[生成器-评估器架构]] — GAN 启发的多 Agent 生成/评估分离模式 (confidence: 0.95)
- [[上下文腐烂]] — 随 token 增加 LLM 召回精度下降的现象 (confidence: 0.95)

## 实体

- [[ChromaDB]] — 开源向量数据库，上下文腐烂研究来源机构 (confidence: 0.85)

## 综合分析

- [[矩阵谱理论的统一叙事]] — 三种证明范式的知识谱系 (confidence: 0.92)
```

**Frontmatter 字段：**
- `type: map` — 固定值，区别于 concept/entity/synthesis
- `topic` — cluster 的主题名称
- `page_count` — 该 cluster 包含的页面数
- `updated` — 最近生成日期

### 生成规则

Maps 由 `wiki:reindex` 步骤 3-5 生成，核心数据源是 **`.claude/topic-to-wiki.json`**：

1. **构建清单**：扫描所有 wiki 页面，生成紧凑清单（`type/name | tags | 概述首句`）
2. **语义聚类（Haiku subagent）**：将清单发给 Haiku 子代理，由 LLM 基于内容语义将每个页面分配到一个主题 topic（可新建 topic，topic 名 2-4 汉字，页面数 < 3 的合并为"其他"）
3. **保存权威映射**：结果写入 `.claude/topic-to-wiki.json`（`{"topics": {"推荐系统": ["矩阵分解", ...], ...}}`），这是唯一权威的 topic→pages 映射
4. **生成 maps**：从 `topic-to-wiki.json` 读取，每个 topic 生成 `maps/{topic}.md`，sections 内按字母序排列
5. **补全 tags**：对于被分配到 topic 但 tags 中缺少该 topic 的页面，追加该 topic 到 tags

> **关键变化**：不再用 tag 频率推导 cluster，而是用 LLM 理解页面内容后语义分配。这使得 maps 能跨越 tag 边界，更准确反映知识结构。

### 当前 Topics

实际 cluster 数量随内容动态变化，当前存在的 topics（从 `maps/` 目录读取）：
- `推荐系统` — 推荐算法、协同过滤、工业应用（216 页）
- `社会科学` — 社会学、社会理论与思想史（107 页）
- `AI工程` — AI 工程、搜索与检索技术（105 页）
- `游戏开发` — 游戏引擎、渲染、动画（78 页）
- `工具与框架` — 开发工具、框架与生态（66 页）
- `Agent系统` — Agent 架构、编排与技能系统（64 页）
- `数值分析` — 数值方法、优化与计算数学（62 页）
- `计算理论` — 计算理论、分布式系统、密码学（60 页）
- `机器人学` — 机器人学、运动规划、控制（56 页）
- `机器学习` — 传统与现代机器学习方法（56 页）
- `信息论` — 信息熵、编码理论与通信（51 页）
- `概率论` — 概率论、统计学、贝叶斯（46 页）
- `天文学` — 天体物理、宇宙学、科学史（42 页）
- `LLM能力` — LLM 上下文、提示工程与模型能力（36 页）
- `强化学习` — 强化学习、博弈论与决策（35 页）
- `文档处理` — 文档解析、OCR 与信息提取（35 页）
- `矩阵理论` — 线性代数、矩阵分析（32 页）
- `经济学` — 经济学、金融与市场（26 页）
- `Lua编程` — Lua 脚本语言与游戏脚本（25 页）
- `控制论` — 控制系统、反馈机制（15 页）
- `时间序列` — 时序分析、序列模型（15 页）
- `C++编程` — C++ 编程模式与系统（10 页）
- `AI设计` — AI 设计、前端 AI 应用（8 页）
- `深度学习` — 神经网络架构与训练（7 页）
- `脑科学` — 认知科学、神经科学（1 页）
- `其他` — 小型 cluster 合并（242 页）

### 使用场景

- **`wiki:query`**：搜索时通过 maps 做主题扩展，找到相关 cluster 下的所有页面
- **Obsidian 导航**：用户可在 maps/ 下按主题浏览知识库
- **`wiki:reindex`**：完整性验证 + 重新生成全部 maps

### 与 index.md 的区别

| | `index.md` | `maps/{topic}.md` |
|--|--|--|
| 内容 | 所有页面的平铺列表 | 按主题分类的子集 |
| 组织方式 | 按 type（实体/概念/综合） | 按 tag cluster |
| 维护方式 | `snapshot_index --update` | `wiki:reindex` Step 3-5（需 subagent） |
| 权威数据源 | — | `.claude/topic-to-wiki.json` |
| 用途 | ingest 时查重、完整性审计 | **query 主题扩展**（首要）、用户浏览、tags 补全 |

### index.md 精简

`wiki:reindex` 步骤 6 将 index.md 从完整页面清单（~600 行）重写为紧凑格式（~35 行）：
- **统计表**：每个 topic 一行，含概念/实体/合计数和指向 map 的链接
- **全局页面名称列表**：逗号分隔，用于快速去重
- 详细清单由各 `maps/*.md` 承载

## 操作手册

### Ingest

1. 读取 raw/ 中的源文件（完整阅读，不要跳过）
2. 判断内容涉及哪些实体和概念
3. 对于每个实体/概念：
   - 如果 wiki/ 中已有对应页面 → 更新该页面，追加新信息
   - 如果没有 → 创建新页面，使用 templates/wiki-page.md 模板
4. 检查新信息是否与已有页面矛盾 → 如有，用 supersedes 机制处理
5. 同步 index.md：执行 `python3 scripts/snapshot_index.py --update`（index.md 是计算产物）
6. 追加 log.md：记录本次 ingest 的操作

### Query

1. 将用户问题改写为优化的搜索关键词（query rewrite）
2. 读取 index.md 定位相关页面
3. 读取相关页面，沿 relates_to 扩展搜索范围
4. 综合所有信息回答问题
5. 如果答案有价值（综合了 3+ 个页面的信息），自动创建为新 wiki 页面
6. 回答时引用来源页面：`来源：[[页面名]]`

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

### 记忆 vs Wiki 边界规则

`_memory/semantic/` 和 `wiki/syntheses/` 服务不同目的，**严禁重复**：

| 层 | 存放位置 | 内容类型 | 示例 |
|----|---------|---------|------|
| **Semantic Memory** | `_memory/semantic/` | 单一事实性声明（不跨主题） | "Python 3.10+ 支持 match 语句" |
| **Syntheses** | `wiki/syntheses/` | 跨主题综合分析（连接 3+ 个概念） | "矩阵谱理论的统一叙事" |

- `wiki:crystallize` 只写入 `_memory/working/` 和可选的 `wiki/syntheses/`
- `wiki:consolidate` 负责 working → episodic → semantic 的晋升和衰减
- 如果一个洞见跨越 3+ 个已有概念 → 放 syntheses/
- 如果一个洞见是单一事实确认 → 放 semantic/
- **决不**将同一信息同时放入两个位置

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
