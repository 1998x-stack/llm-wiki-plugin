# Obsidian Brain：个人第二大脑系统设计

> 融合 LLM Wiki v1（Karpathy）、LLM Wiki v2（agentmemory 生产经验）、kepano-Obsidian 方法论三套体系，构建一个以 Obsidian vault 为核心、AI Agent 为深度处理引擎的个人知识操作系统。

---

## 1. 系统定位

**核心定位**：个人"第二大脑"——全面覆盖思考、学习、工作、成长的知识操作系统。

**设计哲学融合**：

| 来源 | 核心贡献 |
|------|---------|
| **LLM Wiki v1** | 三层架构（raw/wiki/schema）、三个操作（ingest/query/lint）、index.md + log.md |
| **LLM Wiki v2** | 四层记忆、知识图谱、置信度与衰减、结晶化、自动化 hooks、质量控制 |
| **kepano-Obsidian** | File-over-app、links-over-folders、低摩擦输入、分形回顾、bottom-up 结构生长 |

**架构方案**：A + C 混合——Obsidian vault 为核心数据层（方案 A 的简洁性），AI Agent 为深度处理引擎（方案 C 的自动化），不引入独立后端（避免同步复杂度）。

**交互入口**：
- **Obsidian**：日常快速记录、浏览、链接（主要输入端）
- **AI Agent CLI**（Claude Code / Codex / OpenCode）：深度处理——ingest、query、lint、consolidate
- **Web App**（可选）：只读视图层，后期按需搭建

---

## 2. Vault 目录结构

```
obsidian-brain/                     # vault 根目录
│
├── _schema/                        # 系统规则层（v1/v2 的 schema）
│   ├── CLAUDE.md                   # 主 schema：ingest/query/lint 工作流
│   ├── entity-types.md             # 实体类型定义（人/项目/概念/工具/...）
│   ├── relationship-types.md       # 关系类型定义（uses/contradicts/extends/...）
│   └── quality-rules.md            # 质量标准与 lint 规则
│
├── _memory/                        # 四层记忆系统（v2 核心）
│   ├── working/                    # 工作记忆：当前会话的原始观察
│   ├── episodic/                   # 情节记忆：会话摘要（按日期）
│   ├── semantic/                   # 语义记忆：跨会话沉淀的事实
│   └── procedural/                 # 程序性记忆：工作流与模式
│
├── raw/                            # 不可变源材料（v1 的 raw sources）
│   ├── articles/                   # 网页/文章/论文
│   ├── qa/                         # QA jsonl 原始数据
│   ├── books/                      # 书籍摘录
│   ├── assets/                     # 图片/附件
│   └── ...                         # 按领域按需扩展
│
├── wiki/                           # LLM 生成的知识页面（v1 的 wiki 层）
│   ├── entities/                   # 实体页面（人/公司/工具/项目）
│   ├── concepts/                   # 概念页面
│   ├── syntheses/                  # 综合分析、比较、专题
│   └── qa-insights/                # 从 QA 提取的洞见页面
│
├── journal/                        # 个人层（私人思考，kepano 式）
│   ├── daily/                      # 每日 note（时间锚点）
│   ├── reflections/                # 深度反思/复盘
│   ├── judgments/                   # 对特定话题的个人判断
│   └── growth/                     # 成长记录/目标跟踪
│       ├── skills-tracker.md       # 技能变化记录
│       ├── cognitive-patterns.md   # 认知模式记录（LLM 自动发现）
│       └── quarterly/              # 季度回顾
│
├── templates/                      # 模板（kepano 式）
│
├── index.md                        # 内容目录（v1）
├── log.md                          # 操作日志（v1）
└── dashboard.md                    # 个人仪表板
```

**设计决策**：
1. `_` 前缀标记系统级目录——Obsidian 中排在最前面，视觉上与内容区分
2. `journal/` 与 `wiki/` 物理分离——个人思考和知识内容有清晰边界，但可以自由互链
3. `raw/` 保持不可变——LLM 只读不写（v1 核心原则）
4. `wiki/` 下用少量子目录（≤5），符合 kepano "少分类"原则
5. QA 双重存在：`raw/qa/` 存原始 jsonl，`wiki/qa-insights/` 存提取洞见

---

## 3. 四层记忆系统

### 3.1 层级定义

| 层级 | 目录 | 压缩程度 | 置信度 | 生命周期 | 内容类型 |
|------|------|---------|-------|---------|---------|
| Working | `_memory/working/` | 原始 | 低 | 会话内，3 天内处理 | 当前观察 |
| Episodic | `_memory/episodic/` | 中 | 中 | 数天至数周 | 会话摘要 |
| Semantic | `_memory/semantic/` | 高 | 高 | 数月至永久 | 跨会话事实 |
| Procedural | `_memory/procedural/` | 极高 | 极高 | 永久 | 工作流与模式 |

### 3.2 Working Memory

每次会话一个文件。

```yaml
---
type: working-memory
session: 2026-04-14-01
created: 2026-04-14T23:30:00
status: unprocessed    # unprocessed → processed → archived
observations: 5
---

## 观察记录
1. 发现 [[CLIP]] 在游戏资产搜索中的 recall 比 BLIP-2 高 12%
2. ...
```

### 3.3 Episodic Memory

按日/周聚合的会话摘要。

```yaml
---
type: episodic-memory
date: 2026-04-14
confidence: 0.7
last_accessed: 2026-04-14
access_count: 1
source_sessions: [2026-04-14-01, 2026-04-14-02]
---

## 今日要点
- 游戏资产搜索：CLIP 在 recall 上显著优于 BLIP-2

## 值得深入的
- [[CLIP：跨模态语义对齐]] 需要更新

## 待晋升候选
- "CLIP recall > BLIP-2"（已出现 3 次）
```

### 3.4 Semantic Memory

跨多个 session 验证过的稳定事实。每个事实一个文件。

```yaml
---
type: semantic-memory
fact: "CLIP 在游戏资产语义搜索中的 recall 显著优于 BLIP-2"
confidence: 0.85
first_observed: 2026-03-20
last_confirmed: 2026-04-14
confirmation_count: 5
sources:
  - "[[游戏资产语义搜索系统]]"
  - "[[CLIP：跨模态语义对齐]]"
contradicted_by: []
supersedes: null
decay_rate: slow    # slow/medium/fast
---

## 证据链
- 2026-03-20: 初次在论文研究中发现
- 2026-04-14: 对比实验再次确认

## 关联
- supports: [[混合搜索优于单一方法]]
- used_in: [[游戏资产语义搜索系统]]
```

### 3.5 Procedural Memory

从反复出现的模式中提取的最佳实践。

```yaml
---
type: procedural-memory
pattern: "技术选型研究流程"
confidence: 0.9
extracted_from: 12
last_updated: 2026-04-14
---

## 流程
1. 先搜集 3+ 个竞品/方案
2. 对每个方案写一页对比分析（不超过 300 字）
3. 做小规模实验验证核心指标
4. 写最终判断，记录选择理由

## 常见陷阱
- 倾向于选择最复杂的方案（个人偏见）

## 来源
- 从 [[2026-W12]] 到 [[2026-W16]] 的 5 次技术选型中归纳
```

### 3.6 晋升与衰减规则

```
Working → Episodic: 每次会话结束时自动压缩
Episodic → Semantic: 当一个观察在 3+ 个 episode 中重复出现
Semantic → Procedural: 当一个行为模式在 5+ 个语义记忆中被发现
```

**置信度衰减**：基于 Ebbinghaus 遗忘曲线
- 每次被访问/确认/引用：重置衰减曲线
- 未被触及的记忆：按 `decay_rate` 指数衰减
  - slow: 半衰期 180 天（架构决策、核心概念）
  - medium: 半衰期 60 天（一般事实）
  - fast: 半衰期 14 天（临时 bug、短期观察）
- confidence < 0.3 时标记为 `stale`，不再主动使用但保留

---

## 4. Schema 文档

### 4.1 CLAUDE.md 核心结构

`_schema/CLAUDE.md` 是 LLM 操作知识库的主要指令文件。编码：

- 实体类型和关系类型定义
- 各类源材料的 ingest 工作流
- 何时创建新页面 vs 更新现有页面的判断标准
- 质量标准（结构完整性、来源引用、一致性）
- 矛盾处理策略（新覆盖旧，保留历史）
- 记忆 consolidation 调度
- 隐私规则（私人层内容不进入公开搜索）

### 4.2 Frontmatter 规范

所有页面统一核心属性：

```yaml
---
type: entity | concept | synthesis | qa-insight | source-summary | ...
status: draft | active | stale | archived
confidence: 0.0-1.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_accessed: YYYY-MM-DD
source_count: N
tags: []              # ≤8 个大类横切标签（kepano 原则）
aliases: []           # 同义词/中英文别名（kepano 原则）
relates_to: []        # 类型化关系
supersedes: null      # 超越关系（v2）
---
```

### 4.3 类型化关系

不引入独立 graph.json。关系直接写在 frontmatter 的 `relates_to` 中：

```yaml
relates_to:
  - target: "[[CLIP]]"
    type: uses
    confidence: 0.9
  - target: "[[BLIP-2]]"
    type: contradicts
    confidence: 0.85
    note: "在 recall 指标上 CLIP 显著优于 BLIP-2"
```

Obsidian graph view 仍能看到链接关系，agent 通过解析 frontmatter 做图遍历。

---

## 5. Agent Skills

| Skill | 触发方式 | 功能 |
|-------|---------|------|
| `wiki:ingest` | 手动 / on-new-file 自动 | 读取源材料 → 写/更新 wiki 页面 → 更新 index.md → 更新 log.md → 提取实体和关系 |
| `wiki:query` | 手动 | 搜索相关页面 → 综合答案 → 高质量答案自动归档为新 wiki 页面 |
| `wiki:lint` | 手动 / 每周自动 | 检查孤页、矛盾、过期内容、缺失链接 → 自动修复可修复项 → 生成 lint 报告 |
| `wiki:consolidate` | 每日自动 | Working→Episodic→Semantic→Procedural 晋升 + 置信度衰减 |
| `wiki:crystallize` | 会话结束自动 | 将探索过程蒸馏为结构化摘要 → 写入 wiki + 强化相关 semantic memory |
| `wiki:journal` | 手动 | 辅助写日记/反思/判断，自动链接到相关知识页面 |
| `wiki:review` | 每周手动 + 辅助 | kepano 式分形回顾：过去一周 → 升维 → 补链接 → 补判断 |
| `wiki:qa-import` | 手动 / on-new-file 自动 | 批量导入 QA jsonl → 按主题聚类 → 提取洞见到 wiki → 双向链接 |

---

## 6. 个人层（Journal 系统）

### 6.1 设计原则

- kepano 式低摩擦：Daily note 是入口不是负担
- 个人判断与客观知识物理分离但互链
- LLM 自动发现个人行为模式和成长信号

### 6.2 目录与内容类型

| 目录 | 内容类型 | 示例 |
|------|---------|------|
| `journal/daily/` | 每日 note | `2026-04-14.md` |
| `journal/reflections/` | 深度反思 | `技术选型中的复杂度偏见.md` |
| `journal/judgments/` | 个人判断 | `为什么我不再用-RAG-做知识库.md` |
| `journal/growth/` | 成长记录 | `skills-tracker.md`, `cognitive-patterns.md` |
| `journal/growth/quarterly/` | 季度回顾 | `2026-Q1.md` |

### 6.3 Daily Note 模板

```yaml
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

### 6.4 分形回顾机制

```
日级：捕捉 → Daily note，零摩擦记录
  ↓
周级：筛选 → wiki:review skill 辅助
  看这周 daily → 挑出有价值的 → 升级为正式 note
  补链接、补 frontmatter、写一句判断
  ↓
月级：归纳 → LLM 扫描 reflections + judgments，提议合并为综合页面
  ↓
季级：抽象 → 自动生成季度成长报告
  技能变化、认知升级、行为模式分析
```

### 6.5 LLM 自动模式发现

Agent 在 `wiki:consolidate` 时扫描 journal 层：
- **重复主题**：连续 3+ 天提到同一概念 → 建议创建 wiki 概念页
- **行为模式**：连续 5+ 次同类决策偏向 → 写入 `cognitive-patterns.md`
- **成长信号**：某技能领域提及频率和深度在增长 → 更新 `skills-tracker.md`
- **情绪模式**：情绪标记与事件类型的关联（如有）

发现默认自动写入（记入 log.md 供审计），无需手动确认。如发现有误，可通过 lint 修正。

---

## 7. QA 数据集成

### 7.1 数据流

```
raw/qa/*.jsonl            # 原始 QA 对话数据
    ↓  wiki:qa-import
wiki/qa-insights/*.md     # 提取的洞见页面
    ↔  双向链接
wiki/concepts/*.md        # 相关知识页面
wiki/entities/*.md
```

### 7.2 QA Import 流程

1. 读取 jsonl 文件中的对话
2. 按主题聚类（同一概念/项目的 QA 归到一起）
3. 从每个聚类中提取关键洞见
4. 为每个高价值洞见创建 `wiki/qa-insights/` 页面
5. 在页面 frontmatter 中标记源 QA 文件和行号（可追溯）
6. 与 wiki 中已有的相关页面建立双向链接

### 7.3 QA Insight 页面格式

```yaml
---
type: qa-insight
source_file: "raw/qa/claude-sessions.jsonl"
source_lines: [142, 143, 144]
topics: ["CLIP", "游戏资产搜索"]
confidence: 0.8
created: 2026-04-14
---

# CLIP 在游戏资产搜索中的适用性

## 发现
从与 Claude 的对话中发现...

## 关联知识
- [[CLIP：跨模态语义对齐]]
- [[游戏资产语义搜索系统]]
```

---

## 8. 搜索架构

### 8.1 分层搜索策略

1. **Agent 内部搜索**：读 index.md → 定位相关页面 → 读取详情
2. **结构化查找**：通过 frontmatter `relates_to` 做图遍历
3. **全文搜索**：qmd hybrid search（BM25 + vector）——wiki 超过 200 页后启用
4. **回退**：grep 全 vault

### 8.2 Agent 查询流程

```
1. 读 index.md 找相关页面
2. 读这些页面的 frontmatter，沿 relates_to 扩展发现范围
3. 如果 1+2 不够，调用 qmd 做全文搜索
4. 综合所有找到的信息回答
5. 如果答案质量 > 阈值，自动归档为新 wiki 页面（结晶化）
```

---

## 9. 自动化与 Hooks

### 9.1 核心原则

**人做策略，agent 做一切战术操作。**

### 9.2 自动化事件表

| 事件 | 自动触发 | 人工参与度 |
|------|---------|-----------|
| 新文件出现在 `raw/` | 自动 ingest → 写/更新 wiki 页面 → 更新 index → 记 log | **零** |
| 新 QA jsonl 文件出现 | 自动 qa-import → 提取洞见 → 链接到 wiki | **零** |
| Daily note 写完（日结束） | 扫描 daily → 提取观察到 working memory → 标记升维候选 | **零** |
| Agent 会话结束 | 自动 crystallize → 写入 episodic memory | **零** |
| 每日凌晨 | consolidate: episodic 整合 + 置信度衰减 + 晋升检查 | **零** |
| 每周日 | lint + review 辅助：生成周报草稿 + 自动修复 lint 项 | **低**（看一眼确认） |
| 每月 1 号 | 深度 consolidate → semantic→procedural 晋升 → 月度 growth 报告 | **低** |
| wiki 页面被修改 | 自动矛盾检查 → 新覆盖旧，保留历史 | **零** |
| 每季度 | 生成季度成长报告 + 认知模式分析 | **零** |

### 9.3 实现机制

**文件系统监控**（推荐用于 raw/ 目录自动 ingest）：
```bash
fswatch -0 raw/ | xargs -0 -I {} claude -p "wiki:ingest {}"
```

**定时任务**：
```bash
# 每日凌晨 2 点 consolidate
0 2 * * * cd /path/to/vault && claude -p "wiki:consolidate"
# 每周日晚 8 点 lint + review
0 20 * * 0 cd /path/to/vault && claude -p "wiki:lint && wiki:review"
```

**Claude Code Hooks**：
在 `.claude/settings.json` 中配置 PostToolUse hooks，监测对 `raw/` 目录的写入操作。

### 9.4 安全网

1. **所有自动操作写入 log.md**——可追溯、可审计
2. **矛盾解析保留历史**——旧版本标记 stale 但不删除
3. **每周 lint 报告发送摘要**——快速确认一周自动操作是否正常
4. **confidence < 0.3 的自动决策需要人工确认**——低置信度场景回退

---

## 10. 模板清单

### 10.1 Daily Note 模板

（见 Section 6.3）

### 10.2 Wiki 页面模板

```yaml
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
---

# {{title}}

## 概述

## 关键内容

## 来源
- [[]]

## 相关
- [[]]
```

### 10.3 反思模板

```yaml
---
type: reflection
date: {{date}}
trigger:  # 是什么触发了这个反思
tags: []
---

# {{title}}

## 发生了什么

## 我的理解

## 这改变了我什么看法

## 相关
- [[]]
```

### 10.4 判断模板

```yaml
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

### 10.5 周回顾模板

```yaml
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

---

## 11. 迁移策略

**只迁移源文件**，wiki 页面全部由新系统重新生成。

### 11.1 迁移步骤

1. 将 `/Users/mx/Desktop/llm-wiki/raw/` 中的 65 个源文件复制到新 vault 的 `raw/` 目录
2. 按类型分入 `raw/articles/`、`raw/books/` 等子目录
3. 逐步对源文件执行 `wiki:ingest`（建议分批，每次 5-10 个）
4. 现有的 QA 数据（如有 jsonl 文件）放入 `raw/qa/`
5. 旧系统 `/Users/mx/Desktop/llm-wiki/` 归档不删除

---

## 12. 实施路径

### Phase 1 - 最小可行（1-2 天）
- 创建 vault 目录结构
- 写 `_schema/CLAUDE.md` 主 schema
- 写核心模板（daily, wiki page, reflection, judgment）
- 迁移 raw 源文件到新 vault
- 实现 `wiki:ingest` skill

### Phase 2 - 知识重建（3-5 天）
- 对 65 个源文件逐步重新 ingest
- 实现 `wiki:query` 和 `wiki:lint` skills
- 建立 index.md

### Phase 3 - 个人层（1-2 天）
- 开始使用 daily notes
- 实现 `wiki:journal` 和 `wiki:review` skills
- 写 judgment/reflection 模板

### Phase 4 - 记忆系统（2-3 天）
- 实现四层记忆目录和 frontmatter 规范
- 实现 `wiki:consolidate` 和 `wiki:crystallize` skills
- 设置定时任务

### Phase 5 - QA 集成（1-2 天）
- 实现 `wiki:qa-import` skill
- 导入现有 QA 数据

### Phase 6 - 搜索增强（按需）
- Wiki 超过 200 页后，接入 qmd 作为 MCP server

### Phase 7 - 自动化完善（按需）
- 配置 fswatch 文件系统监控
- 配置 cron 定时任务
- 优化 Claude Code hooks

---

## 13. 关键约束与权衡

### 13.1 有意不做的

- **不引入独立后端数据库**——避免 markdown ↔ 结构化数据的同步问题
- **不引入 graph.json**——关系在 frontmatter 中表达，降低维护成本
- **不做团队协作**——纯个人系统，不需要 mesh sync
- **不做实时搜索索引**——按需使用 qmd，不常驻

### 13.2 已知风险

| 风险 | 缓解措施 |
|------|---------|
| 置信度数字由 LLM 生成，可能不准确 | 置信度作为参考而非绝对值；人工可覆盖 |
| 自动化可能传播 LLM 错误 | log.md 全量审计；低置信度决策回退到人工 |
| Frontmatter 中的 relates_to 结构可能变复杂 | 限制每个页面最多 10 个关系 |
| 四层记忆增加系统复杂度 | 先建目录结构，consolidate skill 渐进实现 |

---

## 14. 成功标准

系统成功的标志：

1. **日常记录零摩擦**：打开 Obsidian → Daily note → 写 → 关掉。不超过 30 秒启动
2. **找得到**：任何之前看过/想过的东西，能在 60 秒内找到
3. **知识在增长**：wiki 页面数量稳定增长，且质量可控（lint 通过率 > 90%）
4. **个人洞见在沉淀**：季度报告能看到认知变化和成长轨迹
5. **旧内容不腐烂**：过期信息被自动标记，矛盾被自动解析
6. **自动化在工作**：90%+ 的 ingest/consolidate/lint 无需手动触发
