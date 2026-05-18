---
type: concept
title: 渐进式披露 (Progressive Disclosure)
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: '2026-04-16'
source_count: 1
tags: [方法论, 研究, AI, 计算理论]
aliases:
  - Progressive Disclosure
  - Gradual Information Release
relates_to:
  - target: '[[Context-Engineering]]'
    type: implements
    confidence: 0.95
  - target: '[[Claude-Mem 三层渐进式检索架构]]'
    type: implements
    confidence: 1.0
  - target: '[[提示词工程即架构 (Prompt Engineering as Architecture)]]'
    type: implements
    confidence: 0.9
supersedes: null
---

# 渐进式披露 (Progressive Disclosure)

## 概述
[[渐进式披露（Progressive Disclosure）]]是一种交互设计和信息管理策略，旨在通过分阶段、按需的方式向用户（或 AI 模型）展示信息，以避免认知过载和资源浪费。在 AI 系统设计中，该原则表现为优先提供高层摘要或元数据，仅在用户明确表达进一步兴趣时，才提供详细的底层数据。在 [[Claude-Mem]] 系统中，这一原则被具体化为“三层检索工作流”，有效解决了大[[Language-Model|语言模型]][[上下文窗口]]有限和[[注意力预算|注意力稀释]]的核心痛点。

## 关键内容

### 理论基础与起源
渐进式披露最初源于人机交互（HCI）领域，用于简化复杂软件的界面，避免新手用户被过多的选项和功能吓退。其核心思想是：**默认只显示最常用、最核心的信息，将高级或详细信息隐藏在次级界面中，待用户需要时再展开。**
在 LLM 时代，这一概念被赋予了新的内涵。由于 Token 成本高昂且[[上下文窗口]]有限，“用户”不仅是人类，更是消耗资源的 AI 模型。此时的渐进式披露不仅是为了易用性，更是为了**经济性**和**推理质量**。

### 在 AI 检索系统中的实施
在传统的 RAG（[[检索增强生成]]）系统中，系统往往会一次性将所有检索到的文档片段全部填入 Context，这是一种“全量披露”的反面教材。相比之下，基于渐进式披露的架构（如 [[Claude-Mem]]）采用以下策略：

#### 1. 分层信息结构
-   **第一层（索引层）**：仅披露元数据（标题、时间、类型、简短摘要）。这一层的信息密度极高，Token 消耗极低，足以让模型进行相关性判断和筛选。
-   **第二层（上下文层）**：披露局部关联信息（如时间线上的前后事件）。这一层提供了叙事连贯性，帮助模型理解孤立事件的背景，但仍保持较高的抽象度。
-   **第三层（详情层）**：仅对经过前两层筛选的高置信度目标，披露完整的原始内容。此时模型已经明确了关注点，全量信息的投入能产生最大的推理价值。

#### 2. 主动筛选机制
渐进式披露不仅仅是被动地隐藏信息，更强调**主动筛选**。系统通过工作流设计，强迫模型参与筛选过程。模型必须先在第一层“看目录”，然后在第二层“翻章节”，最后才能在第三层“读正文”。这种互动过程利用了模型的智能进行预过滤，确保了进入最终推理阶段的信息都是高[[信噪比]]的。

### 核心价值
-   **Token 经济性**：通过避免加载大量无关的详细信息，显著降低了 API 调用成本。在 [[Claude-Mem]] 的案例中，实现了约 10 倍的 Token 节省。
-   **[[注意力机制|注意力]]聚焦**：减少了上下文中的噪声，防止模型因[[信息过载]]而产生幻觉或忽略关键细节（[[注意力预算|注意力稀释]]效应）。
-   **推理深度**：模型可以将有限的[[上下文窗口]]容量集中在最相关的问题上，从而进行更深度的分析和推理，而不是浅尝辄止地处理大量碎片信息。
-   **可控性**：开发者可以通过控制披露的粒度和顺序，精确引导模型的思考路径，使系统行为更加可控和可预测。

### 与其他概念的关系
渐进式披露是**[[Context-Engineering|上下文工程]] ([[Context Engineering]])** 的核心支柱之一。它与**[[Prompt-Engineering|提示词工程]]即架构**紧密相连，后者提供了实现渐进式披露的技术手段（如工具参数约束）。同时，它也是**三层渐进式检索架构**的理论基础，解释了为什么要这样设计工作流。

### 应用场景扩展
除了记忆检索，渐进式披露还可应用于：
-   **长文档分析**：先总结章节大意，再按需读取具体段落。
-   **代码库导航**：先展示文件结构和函数签名，再读取具体实现代码。
-   **多轮对话管理**：根据对话进展，动态注入相关的背景知识，而非一开始就灌输所有设定。

### Claude Code 中的演进应用

**搜索能力演进**：

1. **RAG 阶段（早期）**
   - 向量数据库预索引整个代码库
   - 每次响应前检索相关片段并交给 [[Claude_Code|Claude]]
   - 缺陷：[[Claude_Code|Claude]] *被给予* 上下文，而非自行查找

2. **Grep 工具阶段**
   - 给 [[Claude_Code|Claude]] 一个 Grep 工具
   - [[Claude_Code|Claude]] 可以自行搜索文件并构建上下文
   - 进步：从"被动接受"到"主动查找"

3. **[[Agent Skills]] 阶段（当前）**
   - [[Claude_Code|Claude]] 可以读取 [[Skills|Skill]] 文件
   - [[Skills|Skill]] 文件可引用其他文件，支持递归读取
   - 一年演进：从"几乎无法自建上下文"到"跨多层嵌套搜索"

**[[Claude Code]] Guide 智能体案例**：

问题：用户对 [[Claude Code]] 本身提问（如"如何添加 MCP"）时，[[Claude_Code|Claude]] 无法回答。

- **尝试 1**：放入系统提示词 → 导致[[上下文腐烂]]，干扰主要工作
- **尝试 2**：提供文档链接 → [[Claude_Code|Claude]] 拉取大量文档，效率低
- **尝试 3（成功）**：创建[[Subagents-in-Claude-Code|子智能体]]，在自身上下文中搜索文档，只返回答案

关键优势：无需新增工具，为 [[Claude_Code|Claude]] 的行动空间添加能力，保持主上下文清洁。

### 在工具设计中的应用

渐进式披露是 [[Claude Code]] 添加新功能而不新增工具的常用技巧。核心是在需要时才加载详细信息，避免给模型增加额外的选项负担。

## 来源

- [[raw/articles/ai-tools/claude-mem/blog_05_search.md]] — Claude-Mem 三层检索架构
- [[raw/articles/ai-engineering/claude-blog/Seeing like an agent_ how we design tools in Claude Code.md]] — Claude Code Guide 案例、搜索能力演进

## 相关

- [[Context-Engineering]] — 核心支柱（implements）
- [[Claude-Mem 三层渐进式检索架构]] — 具体实现（implements）
- [[提示词工程即架构 (Prompt Engineering as Architecture)]] — 技术手段（implements）
- [[RAG (Retrieval-Augmented Generation)]] — 对比技术（compares_to）
- [[Agent-Skills]] — 核心机制（part_of）
- [[Claude-Code]] — 主要应用场景
- [[即时上下文检索]] — 相关技术（compares_to）
- [[上下文腐烂]] — 解决的问题（caused）
- [[注意力预算]] — 解决的问题（caused）