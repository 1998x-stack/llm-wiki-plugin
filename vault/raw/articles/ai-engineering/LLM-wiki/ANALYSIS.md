# LLM Wiki — 组件深度分析

> 本文件是 LLM Wiki 模式的完整技术拆解。
> 每个组件独立分析：设计动机、核心机制、实现细节、常见陷阱。

---

## 组件总览

```
LLM Wiki
├── [C1] Schema (CLAUDE.md)          ← 大脑：约束LLM行为的操作契约
├── [C2] Index (index.md)            ← 导航：内容目录 + 快速查找
├── [C3] Log (log.md)                ← 记忆：跨session的时间线
├── [C4] Overview (overview.md)      ← 综合：当前知识状态的论文摘要
├── [C5] Entity Pages                ← 命名实体的知识节点
├── [C6] Concept Pages               ← 抽象概念的解释节点
├── [C7] Source Pages                ← 原始资料的编译摘要
├── [C8] Analysis Pages              ← 查询结果的永久保存
├── [C9] Raw Sources                 ← 不可变的原始数据层
└── [C10] Workflows                  ← 标准操作程序
```

---

## C1: Schema (CLAUDE.md) — 操作契约

### 设计动机

LLM 没有跨 session 的记忆。每次新对话都是一张白纸。
Schema 文件解决的问题是：**如何让无状态的 LLM 在每次 session 开始时立即恢复一致的行为？**

没有 Schema，LLM 每次面对同一个问题会给出不同结构、不同深度、不同格式的回答。
Wiki 会随时间变得不一致，最终失去可用性。

Schema 的本质：**把人类编辑规范变成 LLM 可执行的程序**。

### 核心机制

Schema 文件包含三类指令：

| 类型 | 作用 | 例子 |
|------|------|------|
| **结构规范** | 告诉 LLM 文件在哪里、叫什么 | 目录布局、文件命名规则 |
| **格式标准** | 告诉 LLM 每页面长什么样 | Frontmatter schema、各类型页面模板 |
| **工作流程序** | 告诉 LLM 接到指令时执行什么步骤 | Ingest workflow、Query workflow |

### 关键设计决策

**1. Session 开始仪式**
Schema 必须包含"session 开始时做什么"：
- 读 Schema 本身
- 读 log.md 最近10条（恢复近期上下文）
- 读 overview.md（恢复当前论点）
- 给用户一个状态摘要

没有这个仪式，每次 session 开始用户都要重新解释上下文。

**2. 工作流的顺序是强制的**
Ingest workflow 必须是有序步骤，不是建议。
LLM 天然倾向于跳过"讨论"直接写文件 —— Schema 必须明确禁止这个。

**3. Schema 本身是演进的**
Schema 不是一次性写好的。它和 wiki 一起演进。
每次发现 LLM 的行为不对（比如总是漏掉某个步骤），就修改 Schema 并记录在 log 里。

### 常见陷阱

- **太长**: Schema 超过 2000 字后 LLM 会遗漏细节。保持精简；细节放模板文件里。
- **太模糊**: "更新相关页面" 不够。要指定：先读 index，识别候选页，逐一打开读，逐一更新。
- **没有 session 协议**: 没有开始仪式，wiki 很快退化成孤立的文件堆。

---

## C2: Index (index.md) — 导航层

### 设计动机

随着 wiki 增长（50-200页），LLM 不可能知道哪些页面存在。
Index 是解决这个问题的最简单方案：**一个 LLM 每次查询前必须读的目录**。

这是在 RAG 基础设施不可用时的"穷人版语义搜索"。
一个结构良好的 index 条目（链接 + 一句话摘要 + 元数据）足以让 LLM 判断是否需要读完整页面。

### 核心机制

Index 分为几个独立功能的部分：

**内容目录**（按类型分区）
每个条目：`[[slug]] — 一句话摘要 · status · updated · sources: N`

**开放问题注册表**
跨越多个 session 的问题清单。避免问题在 log 里被淹没。

**矛盾注册表**
活跃的 source 之间的矛盾。直到 lint pass 解决后才从注册表删除。

**统计面板**
页面数量、stub 比例等。让人类一眼看到 wiki 健康状况。

### 更新时机

```
触发 index 更新的事件：
- ingest 后（新增 source page + 更新现有页面）
- 新建任何 wiki 页面后
- 主要页面修订后（摘要可能过期）
- lint pass 后（孤立页、缺失页）
```

### 关键设计决策

**条目格式要机器友好**
LLM 扫描 index 时要快速判断相关性。
条目要包含：是什么（摘要）+ 多新（日期）+ 多成熟（status）+ 有多少来源（source_count）。

**用 status 区分页面成熟度**
`stub → active → mature → superseded`
LLM 看到 `stub` 知道这个页面可能不完整，需要谨慎引用。

### 常见陷阱

- **更新延迟**: 每次 ingest 忘记更新 index，index 就开始失真。Schema 里必须强制。
- **条目太详细**: Index 条目如果超过两行，读 index 本身就会耗尽 context window。

---

## C3: Log (log.md) — 时间线记忆

### 设计动机

LLM 没有对话历史记忆，但 wiki 是随时间演进的产物。
Log 解决的是：**如何让 LLM 在新 session 里知道"上次我们做了什么"？**

没有 log：
- 用户必须每次重新解释"我们上周处理过这个问题了"
- LLM 可能重复已经回答过的问题
- 无法追踪 wiki 的演化轨迹

### 核心机制

**grep 友好的格式**
每个条目的第一行格式固定：`## [YYYY-MM-DD] type | title`

这使得用 unix 工具分析 log 变得简单：
```bash
grep "^## \[" log.md | tail -10      # 最近10条
grep "ingest" log.md | wc -l         # 总 ingest 次数
grep "Contradiction" log.md          # 所有发现的矛盾
```

**类型化的条目结构**
不同操作类型（ingest/query/lint/schema）有不同的字段模板。
一致的结构让 LLM 扫描 log 时知道在哪里找什么信息。

**append-only 不可变性**
过去的条目永远不修改。这是记录，不是草稿。
如果发现之前的判断错了，新建一条条目记录修正，不要回头改。

### Session 恢复模式

Session 开始时 LLM 读 log 的最近 10 条，提取：
1. 上次 ingest 了什么（知道 wiki 最新状态）
2. 有什么 open question 还没解决
3. 有什么矛盾还在 pending

这是跨 session 连续性的核心机制。

### 常见陷阱

- **条目太长**: Log 条目不是报告，是摘要。超过 20 行就太长了。
- **格式不一致**: 如果 LLM 自由发挥格式，grep 就失效。Schema 里的模板要强制执行。
- **忘记记录 query**: 大多数人只记录 ingest，忘记记录 query。但 query 历史同样有价值。

---

## C4: Overview (overview.md) — 知识综合

### 设计动机

Index 是目录，Overview 是**论文摘要**。

它回答的问题是："基于目前所有的 sources，我们对这个话题知道什么？"

Overview 强迫 wiki 保持一个**核心论点**，而不是变成无数孤立事实的堆砌。
它还是矛盾和不确定性的诚实反映 —— 好的研究不假装一切都已知。

### 更新时机

不需要每次 ingest 都更新。触发条件：
- 每 5 次 ingest 后（定期综合）
- 某个 source 根本性地改变了现有论点
- Lint pass 解决了重大矛盾
- 人类明确要求"重新综合"

### 版本历史

Overview 维护版本历史（见 Revision History 表）。
过时的段落不删除，用 `~~strikethrough~~` + 日期标记。
这让 wiki 本身成为知识演化的记录。

### 关键设计决策

**"Tensions" 部分是最重要的**
最没用的知识库是那些声称一切都清楚的知识库。
Overview 的 Tensions 部分是 wiki 智识诚实性的指标。
Sources 之间的矛盾、未解答的问题、竞争性解释 —— 都要在这里反映。

**Central Thesis 应该是一个可证伪的陈述**
"这个话题很复杂" 不是论点。
"X 机制是 Y 现象的主要驱动力，但在 Z 条件下被 W 所取代" 才是论点。

---

## C5: Entity Pages — 命名实体节点

### 设计动机

每个重要的命名实体（人、机构、产品、论文）需要**一个聚合点**，
把来自多个 sources 的信息集中在一起，并保持更新。

没有 Entity Pages：
- 关于某个实体的信息散落在多个 Source Pages 里
- 矛盾难以发现（source A 说 X，source B 说 ¬X）
- 问"关于实体 E 我们知道什么"需要扫描所有 sources

### 核心机制

Entity Page 是**一个 source 视角的聚合器**：

```
Entity Page = 多个 Source Pages 中关于该实体信息的 JOIN
```

每次 ingest 一个新 source，如果它提到了现有 Entity，就要更新该 Entity Page。
这是 wiki 的"写入放大"——一个 source 可能触发 10-15 个页面的更新。

### Source Count 的意义

Frontmatter 里的 `source_count` 表示有多少 sources 提到了这个实体。
- `source_count: 1` → 这个实体只被一个 source 提及，可能是边缘实体
- `source_count: 5+` → 核心实体，值得深入维护

Lint pass 会找出 `source_count: 1` 且内容单薄的页面，建议合并到 source page 里。

### 常见陷阱

- **过早创建**: 每个人名都建页面会让 wiki 膨胀。只为"重要"实体建页面（出现在 ≥2 sources）。
- **更新遗漏**: 新 source 提到了已有实体但没有更新 entity page，会导致 entity page 过期。

---

## C6: Concept Pages — 抽象概念节点

### 设计动机

概念页面解决的问题：**术语歧义和跨 source 的概念统一**。

不同 sources 可能用不同的名字称呼同一个概念，或者用同一个名字称呼不同的概念。
Concept Page 是这个 wiki 里的**术语表** + **解释器**。

它还提供了"Why It Matters (in this wiki's context)"部分 —— 
这是一般术语表没有的，它把概念锚定到当前研究语境中。

### 与 Entity Pages 的区别

| Entity Page | Concept Page |
|-------------|--------------|
| "什么是 X？" | "X 如何工作？" |
| 命名的特定事物 | 可实例化的抽象思想 |
| 有唯一的历史和时间线 | 跨不同实体可重用 |
| 例：OpenAI、GPT-4 | 例：attention mechanism、RLHF |

### Instantiations 部分的重要性

Concept Page 的 Instantiations 部分列出了哪些实体"实现"了这个概念。
这是 wiki 里的**双向链接**：从 entity 链到 concept，从 concept 链回 entity。
双向链接让图视图（Obsidian Graph View）变得有意义。

---

## C7: Source Pages — 编译的知识单元

### 设计动机

Source Page 是**原始 source 的编译结果**。

原始文章里有很多无关信息、重复、冗余。
Source Page 提取出：核心主张、证据、矛盾、与 wiki 其他内容的连接。

关键设计：**Source Page 写完之后，你几乎不需要再回去读原始文章。**
所有有价值的信息已经被提取并结构化了。

### 和 RAG 的本质区别

| RAG | LLM Wiki |
|-----|----------|
| 每次查询重新检索原始文档片段 | Source Page 是预编译的摘要 |
| LLM 每次从头推断 | 矛盾和连接已经预先标注 |
| 适合"在一堆文档里找答案" | 适合"基于积累知识回答问题" |
| 无状态 | 有状态、可积累 |

### Wiki Impact 部分的价值

每个 Source Page 都有一个 "Wiki Impact" 部分，记录这个 source 影响了哪些其他页面。
这使得 source 与 wiki 的关系变得**可审计**：如果一个 source 被发现有误，
可以立即找到所有受影响的页面并修正。

---

## C8: Analysis Pages — 永久化的查询结果

### 设计动机

这是 LLM Wiki 里最被低估的组件。

大多数人问 LLM 问题，得到答案，然后答案消失在对话历史里。
如果答案很有价值（一个比较分析、一个综合、一个发现的连接），
为什么不把它存进 wiki？

Analysis Pages 让**探索本身也成为积累**。

### 触发条件

不是每个问题都值得存为 Analysis Page。存的条件：
- 回答需要综合多个 sources（超过 3 个）
- 回答产生了新的 insight，不只是检索已知事实
- 回答会被多次参考（比较、评估框架）
- 回答解决了一个在 Open Questions 注册表里的问题

### 和 Overview 的区别

Overview 是关于整个 wiki 话题的综合论点。
Analysis 是关于特定问题的深入回答。
一个成熟的 Analysis 可能最终被合并进 Overview。

---

## C9: Raw Sources — 不可变的真相层

### 设计动机

分离"原始材料"和"编译知识"是整个架构的核心原则。

原始 sources 永远不修改，原因：
1. 如果 wiki 里的某个主张出错，可以溯源到原始文档核查
2. 随着分析能力提升，可以"重新 ingest"同一 source，得到更深的洞察
3. 清晰的责任边界：LLM 只写 wiki，不"修改历史"

### Source 质量决定 Wiki 质量

Wiki 的质量上限 = 输入 sources 的质量。

好的 source 选择原则：
- **Primary over secondary**: 原始论文 > 新闻报道 > 博客摘要
- **Dated**: 知道信息的时间背景
- **Specific**: 有具体数据和主张，不只是泛泛而谈
- **Diverse**: 不同视角、可能相互矛盾的 sources 比单方面 sources 更有价值

---

## C10: Workflows — 标准操作程序

### 为什么 Workflow 比 "告诉 LLM 怎么做" 更重要

如果 Schema 只说"处理 source 时更新相关页面"，LLM 会自由发挥，
每次的行为都不同，wiki 的一致性很快崩溃。

Workflow 是**算法**，不是建议：
- 明确的步骤顺序
- 明确的每步产出
- 明确的触发条件和结束条件

### Ingest Workflow 的关键步骤：讨论先于写作

最重要的一步是：**读完 source 后先和用户讨论，再开始写任何文件**。

原因：
- 用户可能知道 LLM 不知道的上下文（"这篇文章的作者有利益冲突"）
- 用户可以指导强调什么、忽略什么
- 防止 LLM 把用户不认为重要的东西标记为"关键主张"

这个步骤很容易被 LLM 跳过（它很想直接开始写）。Schema 必须明确说"禁止跳过"。

### Lint Workflow：必须等待人类确认再执行

Lint pass 的职责是**发现问题，不是自动修复问题**。

Lint 产出的是问题清单（"建议合并 X 和 Y"），
然后等待人类确认，再执行修改。

自动执行 lint 修改很危险：
LLM 可能误判两个页面是重复的，把一个重要的区分给合并掉。

---

## 整体数据流图

```
原始 Source 文件
      │
      ▼ (读取，不写入)
 [Ingest Workflow]
      │
      ├──→ wiki/sources/[slug].md         (新建)
      │
      ├──→ wiki/entities/[entity].md      (更新 or 新建)
      │
      ├──→ wiki/concepts/[concept].md     (更新 or 新建)
      │
      ├──→ wiki/overview.md              (可能更新，每5次强制)
      │
      ├──→ wiki/index.md                 (必须更新)
      │
      └──→ wiki/log.md                   (必须追加)

用户查询
      │
      ▼
 [Query Workflow]
      │
      ├──→ 读 index.md → 读相关页面 → 综合回答
      │
      └──→ (可选) wiki/analyses/[slug].md  (新建)
                  │
                  └──→ wiki/index.md        (更新)
                  └──→ wiki/log.md          (追加)

定期 Lint
      │
      ▼
 [Lint Workflow]
      │
      ├──→ 产出问题清单
      │
      ├──→ (等待人类确认)
      │
      ├──→ 执行修复
      │
      └──→ wiki/log.md                   (追加 lint 记录)
```

---

## 扩展选项

### 当 wiki 超过 ~100 页时

Index 扫描开始变慢。考虑引入本地搜索：
- [qmd](https://github.com/tobi/qmd): BM25 + 向量混合搜索，有 MCP server 接口
- 自建简单 BM25 搜索脚本（LLM 可以帮你写）
- Obsidian 的 Quick Switcher + Search 插件（用于人工浏览）

### Obsidian 插件推荐

| 插件 | 用途 |
|------|------|
| Dataview | 查询 frontmatter 生成动态表格 |
| Graph View | 可视化页面之间的连接 |
| Templater | 快速插入页面模板 |
| Marp | 从 wiki 内容生成 slides |
| Web Clipper | 把网页文章剪辑为 markdown |

### 多人协作

Wiki 是 git repo。自然支持：
- `git blame` 追踪谁修改了什么
- Pull request review 让人类审核 LLM 的更新
- Branch 用于"实验性 ingest"（不确定 source 是否可信）

---

## 快速上手检查清单

```
[ ] 1. 复制这个目录结构
[ ] 2. 填写 CLAUDE.md 里的 [TOPIC] 占位符
[ ] 3. 根据你的领域调整 Entity Page 的 Key Facts 表格字段
[ ] 4. 决定 source 文件命名规则
[ ] 5. 添加第一个 source 到 raw/
[ ] 6. 对 LLM 说："Read CLAUDE.md, then ingest raw/[filename]"
[ ] 7. 观察 LLM 的第一次 ingest，给 schema 打补丁
[ ] 8. 每完成 5 次 ingest，运行一次 lint
[ ] 9. 每完成 10 次 ingest，检查 overview 是否需要更新论点
```
