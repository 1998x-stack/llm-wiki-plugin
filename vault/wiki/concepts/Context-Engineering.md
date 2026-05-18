---
type: concept
title: Context Engineering
status: active
confidence: 0.92
created: 2026-04-15
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 6
tags:
- 技术
- 方法论
- AI
- AI工程
aliases:
- 上下文工程
- 有限注意力预算调度
- Context OS
relates_to:
- target: '[[分层记忆架构]]'
  type: uses
  confidence: 0.95
- target: '[[LLM-Statelessness]]'
  type: extends
  confidence: 0.88
- target: '[[检索增强生成]]'
  type: uses
  confidence: 0.9
- target: '[[Prompt缓存]]'
  type: uses
  confidence: 0.85
- target: '[[上下文腐烂]]'
  type: related_to
  confidence: 0.95
- target: '[[即时上下文检索]]'
  type: related_to
  confidence: 0.9
- target: '[[上下文压缩]]'
  type: implements
  confidence: 0.95
- target: '[[提示词缓存]]'
  type: uses
  confidence: 0.9
- target: '[[上下文策略]]'
  type: part_of
  confidence: 0.85
- target: '[[子 Agent 卸载]]'
  type: implements
  confidence: 0.8
- target: '[[上下文预算管理]]'
  type: implements
  confidence: 0.85
- target: '[[RAG]]'
  type: incorporates
  confidence: 0.9
- target: '[[Transformer架构]]'
  type: builds_on
  confidence: 0.8
- target: '[[MCP]]'
  type: uses
  confidence: 0.85
- target: '[[Andrej Karpathy]]'
  type: contributed_by
  confidence: 0.9
- target: '[[LlamaIndex]]'
  type: uses
  confidence: 0.75
- target: '[[RAGAs]]'
  type: uses
  confidence: 0.7
- target: '[[Context Design]]'
  type: implements
  confidence: 0.8
- target: '[[Claude Code Skills]]'
  type: uses
  confidence: 0.85
supersedes: null
---

# Context Engineering

## 概述

[[Context Engineering]]（[[Context Engineering|上下文工程]]）是指对 LLM 的有限[[上下文窗口]]进行策展与管理的系统化方法。[[Anthropic]] 将其定义为：在固定 token 预算下最大化有用信息密度，而非简单地将聊天历史拼接填满窗口。核心隐喻是把上下文当作**有限缓存**（Cache）和**工作集**（Working Set），而非日志记录器。

> **定义**：系统性地设计、构建、管理和优化输入到 LLM [[上下文窗口]]中的所有信息——包括其内容、结构、来源、时序和动态组装逻辑——以稳定、可扩展地实现复杂 AI 应用目标的工程学科。

## 诞生条件

### 技术触发因素

| 触发点 | 时间 | 内容 |
|--------|------|------|
| 长[[上下文窗口]]出现 | 2023 | [[Claude_Code|Claude]] 100K、GPT-4-turbo 128K，窗口从"稀缺资源"变为"待管理空间" |
| RAG [[规范化理论|范式]]成熟 | 2023 | LlamaIndex / [[LangChain]] 标准化[[检索增强生成]]工作流 |
| Agent 框架崛起 | 2023–2024 | AutoGPT、LangGraph、CrewAI 使多轮工具调用成为标准 |
| 工具调用（Function [[天职|Calling]]）标准化 | 2023 | [[OpenAI]] Function [[天职|Calling]] API，工具结果需要结构化注入上下文 |
| 模型能力上移 | 2024 | 推理质量提升，"上下文组装质量"成为主要瓶颈 |

### 认知转折

旧认知（[[Prompt Engineering]] 时代）：
"如何让模型理解我的指令？"

新认知（[[Context Engineering]] 时代）：
"如何让模型在正确的时间，拥有完成任务所需的全部、且仅有必要的信息？"

关键推手：[[Andrej Karpathy]] 2024 年提出"[[Context Engineering]] > [[Prompt Engineering]]"，
将这一概念正式推向主流视野。

## 关键内容

### 四条经验规律驱动的设计原则

| 规律                   | [[Context Engineering | 上下文工程]]含义                                       | 工程手段 |
| -------------------- | --------------------- | ----------------------------------------------- | ---- |
| **Zipf / Pareto**    | 绝大多数价值来自少数热点上下文       | 热/温/冷分层，优先权加权                                   |      |
| **Bradford / Lotka** | 少数核心来源覆盖大多数高价值信息      | source prior、每源上限（per-source cap）               |      |
| **Matthew Effect**   | 早进入上下文的材料放大后续推理偏向     | 强制多源检索、反证位（counter-evidence lane）               |      |
| **Benford 式思路**      | 用分布基线发现异常             | 监控 source share、stale fact rate、retrieval drift |      |

### Context 的信息架构

[[Context Engineering]] 管理的不再只是"提示词"，而是整个[[上下文窗口]]的**信息架构**：

```
┌─────────────────────────────────────────────┐
│              Context Window                  │
├──────────────┬──────────────────────────────┤
│ System       │ 角色定义、全局规则、工具声明    │
│ Prompt       │                              │
├──────────────┼──────────────────────────────┤
│ Memory       │ 短期记忆（当前对话）           │
│              │ 长期记忆（向量检索/KV存储）     │
├──────────────┼──────────────────────────────┤
│ Retrieved    │ RAG 检索内容                  │
│ Knowledge    │ 知识库/文档片段               │
├──────────────┼──────────────────────────────┤
│ Tool         │ 工具定义 + 工具调用结果        │
│ Results      │                              │
├──────────────┼──────────────────────────────┤
│ Conversation │ 历史对话（选择性保留）          │
│ History      │                              │
├──────────────┼──────────────────────────────┤
│ Task         │ 当前任务描述 + 状态            │
│ State        │                              │
└──────────────┴──────────────────────────────┘
```

### 核心技术体系

**1. RAG（检索增强生成）**

```python
# 基础 RAG 流程
query → Embedding → 向量检索 → Top-K 文档 → 注入上下文 → 生成

# 高级变体
- HyDE（假设文档嵌入）：先让 LLM 生成假设答案，再用假设答案检索
- RAG-Fusion：多查询 + 倒排融合重排序
- GraphRAG：知识图谱 + 向量检索双通道
- RAPTOR：递归摘要树，解决超长文档检索
```

**2. 记忆系统分层架构**

```
┌─────────────────────────────────────┐
│ L1: 工作记忆（Working Memory）       │
│     当前对话轮次，直接在上下文中      │
├─────────────────────────────────────┤
│ L2: 情节记忆（Episodic Memory）      │
│     历史对话摘要，按需检索注入        │
├─────────────────────────────────────┤
│ L3: 语义记忆（Semantic Memory）      │
│     向量化知识库，相关性检索          │
├─────────────────────────────────────┤
│ L4: 程序记忆（Procedural Memory）    │
│     系统 Prompt 中的规则和能力定义    │
└─────────────────────────────────────┘
```

**3. 上下文压缩与管理**

```python
策略一：滑动窗口（Sliding Window）
→ 只保留最近 N 轮对话

策略二：摘要压缩（Summarization）
→ 定期将历史对话压缩为摘要

策略三：选择性保留（Selective Retention）
→ 用 LLM 判断哪些信息"重要"需要保留

策略四：分层压缩（Hierarchical Compression）
→ 近期详细 + 中期摘要 + 远期关键事件
```

**4. 上下文窗口位置效应（Position Effects）**

```
Lost in the Middle 研究发现：
┌─────────────────────────────┐
│ 开头部分：注意力权重 ████████ │  ← 最高
│ 中间部分：注意力权重 ████░░░░ │  ← 最低（"lost in middle"）
│ 结尾部分：注意力权重 ███████░ │  ← 次高
└─────────────────────────────┘

工程策略：
- 关键信息放头部（System Prompt）或尾部（用户消息紧前）
- 大量背景材料放中间
- 重要规则在头尾重复
```

**5. 动态上下文组装（Dynamic Context Assembly）**

```python
class ContextAssembler:
    def build(self, query, session, tools) -> Context:
        return Context(
            system=self.load_system_prompt(session.persona),
            memories=self.retrieve_relevant_memories(query, k=5),
            knowledge=self.rag_retrieve(query, k=10),
            conversation=self.compress_history(session.history),
            tools=self.select_relevant_tools(query, tools),
            task=self.format_current_task(query)
        )
    
    def compress_history(self, history):
        # 保留最近 3 轮完整 + 更早的摘要
        recent = history[-3:]
        older = self.summarize(history[:-3])
        return older + recent
```

**6. MCP（Model Context Protocol）**

```
Anthropic 2024 年提出的上下文注入标准协议：
- 统一工具/资源/Prompt 注入接口
- 解决各框架上下文注入方式不统一的碎片化问题
- Server/Client 架构，服务可复用

MCP 将 Context Engineering 推向"基础设施"层面
```

**7. 上下文评估指标**

```python
评估维度：
- 相关性（Relevance）：检索内容与查询的语义相关度
- 忠实性（Faithfulness）：生成内容是否基于给定上下文
- 覆盖率（Coverage）：所需信息是否都被包含
- 噪声比（Noise Ratio）：无关信息占比
- 位置效率（Position Efficiency）：关键信息是否在高注意力区域

工具：RAGAs、TREC、TruLens
```

### 核心机理

**注意⼒稀释原理**：

```
Transformer 的 Softmax Attention：
attention(Q,K,V) = softmax(QK^T / √d) · V

当上下文长度 N 增大：
- Softmax 分母增大 → 每个 token 平均注意力权重下降
- 关键信息被"稀释"在大量噪声中
- 模型有效"关注"范围存在软上限

→ Context Engineering 的核心任务之一：
  最大化信噪比（Signal-to-Noise Ratio）
```

### 请求路由（Router-first）

第一层不是检索，而是**路由判断**：

```
if kb_size < 200k and low_churn and low_tooling:
    mode = "full_context_cached"
elif task_is_knowledge_intensive:
    mode = "retrieval_augmented"
elif session_is_long_running:
    mode = "hierarchical_memory"
else:
    mode = "hybrid_agent"
```

Anthropic 建议：知识库小于约 200k tokens 且相对稳定时，直接放入 prompt 往往是最简单方案。

### 代表性工程框架

```
检索框架：
├── LlamaIndex（最完整的 RAG 生态）
├── LangChain（最广泛的 Context 管道工具）
└── Haystack（企业级搜索+RAG）

向量数据库：
├── Chroma（本地开发首选）
├── Pinecone（云端生产）
├── Weaviate（混合检索）
├── Qdrant（Rust 高性能）
└── Milvus（分布式规模化）

记忆系统：
├── Mem0（智能记忆层）
├── Zep（对话记忆专项）
└── LangMem（LangGraph 官方记忆）

上下文协议：
└── MCP（Model Context Protocol）

评估：
├── RAGAs（RAG 专项评估）
└── TruLens（全链路追踪）
```

### 局限性与失效边界

| 局限 | 表现 | 根因 |
|------|------|------|
| 检索错误级联 | 错误检索 → 错误生成，且难以溯源 | RAG 管道中间态不透明 |
| 上下文窗口仍有上限 | 超长文档仍需截断或压缩 | Transformer O(n²) 复杂度 |
| 多智能体协调困难 | 多个 Agent 共享上下文时状态冲突 | 无统一状态管理原语 |
| 工程复杂度高 | 检索+压缩+注入+评估，维护成本高 | 无标准化"上下文操作系统" |
| 实时知识延迟 | 数据入库 → 可检索存在时间差 | 向量数据库更新延迟 |

### 历史地位

Context Engineering 是 LLM 工程的**第一个真正的系统性工程学科**：

- 将"AI 应用质量"问题从"模型问题"转移到"工程问题"
- 确立了"信息架构 + 检索系统 + 记忆管理"的三角支柱
- 为 Agent 系统提供了状态管理的理论基础
- 但仍以**人类为中心**：人类设计流程，Agent 执行单步

> **核心隐喻**：Context Engineer = 图书馆员。不管理书的内容（模型），而是管理"哪些书、以什么顺序、放在读者面前"。让读者（LLM）在最短时间内找到并理解正确信息。

### 检索链路：按需混合检索

**query understanding → need_retrieval? → hybrid retrieve → contextualize → rerank → diversify → compress → assemble**

关键环节：
1. **need_retrieval?** — 先判断能否靠 working memory 回答
2. **hybrid retrieve** — 同时跑 dense + BM25 + metadata filter + graph hop
3. **contextualize chunk** — 给每个 chunk 补最小必要上下文（标题、章节、时间）
4. **rerank + diversify** — 考虑 source quality / freshness / novelty / redundancy penalty / per-source cap
5. **counter-evidence lane** — 保留 1 个"反证/边界条件"槽位，防止 Matthew effect 锚定

### Prompt 位置编排

_Lost in the Middle_ 研究表明关键信息埋在中段时模型利用效果显著下降。推荐布局：

```
[Cached Prefix: system / policy / tool contract / output schema]
[Task contract: 这轮要解决什么]
[Working memory]
[Top evidence A]             ← 最关键证据放靠前
[Compressed session summary]
[Supporting evidence B/C]
[Counter evidence / freshness note]  ← 关键约束放靠尾
[Current user ask]
[Final answer rubric]
```

对真正不能丢的约束，**允许重复一次**比埋在中间更稳。

### 压缩目标：可复用状态，而非摘要

压缩应产出四种结构化对象，而非自由文本摘要：

- **durable facts** — 长期有效事实
- **decisions** — 已做选择和理由
- **open loops** — 未完成事项
- **source anchors** — 原文锚点，便于回源

压缩触发条件：任务阶段切换 / 关键决策 / 工具返回超长结果 / token 预算逼近阈值。

⚠️ 禁止压缩的内容：数字/合同/代码逻辑（会失真）、事实与推断混写（无法审计）。

### Memory Object 模型

上下文管理的对象不应是 message，而应是 **memory object**：

```json
{
  "id": "mem_xxx",
  "type": "fact|decision|preference|plan|episode",
  "text": "用户更关心 latency 而不是 peak accuracy",
  "source": "chat:turn_18",
  "freshness": "2026-04-14",
  "salience": 0.82,
  "reuse_count": 6,
  "confidence": 0.91,
  "anchors": ["turn18", "doc:spec#p4"]
}
```

### Token 预算分配（参考值）

| 层 | 比例 | 内容 |
|---|---|---|
| Cached Prefix | 10% | 系统指令、工具契约、output schema |
| Working Memory | 15% | 当前任务、约束、实体 |
| Recent Turns | 15% | 近期对话 |
| Retrieved Evidence | 35% | 检索结果 |
| Episodic Summaries | 15% | 阶段压缩摘要 |
| Output Contract | 10% | 输出要求、checklist |

Coding agent 场景：减少 Retrieved Evidence，增加 Working Memory + Tool Delta。
Enterprise QA 场景：Retrieved Evidence 提升至 ~45%。

### 候选 Memory 评分函数

$$
score = 0.35 \cdot relevance + 0.20 \cdot source\_quality + 0.15 \cdot freshness + 0.10 \cdot salience + 0.10 \cdot dependency + 0.10 \cdot novelty - redundancy
$$

按 token budget 做 knapsack 式选择，而非 top-k 直接截断。

### 评估指标（Pareto 风格）

- **Context utilization** — 注入 token 中真正被引用的比例
- **Answer quality @ fixed budget** — 固定预算下质量变化
- **Stale fact rate** — 过期信息混入比例
- **Source dominance** — 单一来源是否垄断前几条证据
- **Position robustness** — 换位置后答案是否明显劣化
- **Cache hit rate / latency / cost** — 前缀缓存效果

### 核心结论

> 大模型上下文管理不要围绕"聊天历史"设计，而要围绕"**价值密度**"设计；不要把上下文当日志，而要当**缓存、工作集、可审计记忆**。

设计公式：**分层记忆（hot/warm/cold） + 按需检索 + 混合检索与重排 + 结构化压缩 + 位置编排 + 工具状态外置 + 预算与评估闭环。**

### Anthropic 工程视角的补充（2026）

Anthropic Applied AI 团队对上下文工程的核心定位：**在任意时刻找到最小化的高[[信噪比]] token 集合，最大化目标行为的概率。**

**[[上下文腐烂]]（[[上下文腐烂|Context Rot]]）**：[[ChromaDB|Chroma]] Research 基准研究发现，随上下文 token 增加，模型从上下文中准确召回信息的能力持续下降。这不是硬性崖式截止，而是性能梯度——是上下文工程存在的核心动机。

**[[注意力预算]]（[[注意力预算|Attention Budget]]）**：[[Transformer架构|Transformer]] n² 注意力机制导致每个新 token 都消耗有限的[[注意力预算|注意力资源]]，上下文增长时每对 token 关系可获得的参数容量被稀释。

**长时任务的三种技术**（Anthropic 实践）：
1. **[[上下文压缩]]（Compaction）**：Anthropic 官方 API，当对话接近窗口限制时自动将旧内容压缩为摘要。触发阈值可配置（默认 150,000 tokens，最低 50,000），支持 `pause_after_compaction` 暂停注入额外内容，支持自定义摘要指令。与 [[提示词缓存]] 协同：系统提示末尾加 `[[提示词缓存|cache_control]]` 断点可保持系统[[提示词缓存|提示缓存]]有效。详见 [[上下文压缩]]。
2. **[[结构化笔记法]]**（[[结构化笔记法|Agentic Memory]]）：Agent 将关键状态写入上下文外的持久存储 → 适合有明确里程碑的迭代开发
3. **多 Agent 架构**：子 Agent 处理深度工作并返回精简摘要 → 适合需要并行探索的复杂研究

**[[即时上下文检索]]（[[即时上下文检索|Just-in-Time Context]]）**：Agent 不预加载所有数据，而是持有轻量标识符（文件路径、URL、查询），运行时工具按需动态加载。Claude Code 的 glob/grep/Bash 模式是典型实现。

**系统 Prompt 的"高度"（Altitude）校准**：Anthropic 提出系统 prompt 应处于 Goldilocks zone——在两个常见失败模式之间找到平衡：
- **过低（过度具体）**：硬编码复杂的 if-else 逻辑，试图精确控制 agent 行为 → 导致脆弱性和维护成本递增
- **过高（过度抽象）**：提供模糊的高层指导，无法给 LLM 具体信号或错误假设共享上下文 → 导致行为不可预测
- **最佳高度**：足够具体以有效引导行为，又足够灵活以给模型提供强启发式指导

推荐用 XML 标签或 Markdown header 将 prompt 分成独立段落（`<background_information>`、`<instructions>`、`## Tool guidance` 等），但随模型能力提升，精确格式的重要性在下降。

**工具设计的上下文工程含义**：
- 工具集应是最小可行集（minimal viable set），功能重叠会导致 agent 在工具选择上产生歧义
- 如果人类工程师都无法确定某场景该用哪个工具，就不能指望 agent 做得更好
- 工具返回的信息必须 token-efficient，避免把 agent 的有限注意力预算浪费在冗余数据上
- Few-shot examples 应精选 diverse、canonical 的样例，而非往 prompt 里塞一长串 edge case

**混合检索策略（Hybrid Strategy）**：
- 部分数据预加载（速度优先）+ 部分运行时自主探索（灵活性优先）
- Claude Code 是典型混合实现：`[[CLAUDE.md]]` 文件预先放入上下文，同时通过 glob/grep 按需导航环境检索文件
- 混合策略更适合内容变化不频繁的场景（如法律、金融工作）
- 随模型能力提升，agent 设计会趋向于让智能模型自主行动，人类策展逐步减少

### 来源作者

本文由 [[Anthropic]] Applied AI 团队撰写：[[Prithvi-Rajasekaran|Prithvi Rajasekaran]], Ethan Dixon, Carly Ryan, [[Jeremy Hadfield]]，贡献者包括 Rafi Ayub, Hannah Moran, Cal Rueb, Connor Jennings。

### Manus 的上下文工程六原则（2025）

[[Manus]] 团队通过四次框架重建总结出六条核心原则，是[[Context Engineering|上下文工程]]在生产环境的重要实践补充：

1. **围绕 [[KV 缓存命中率]] 进行设计**：KV-cache 命中率是生产阶段最重要的单一指标，Agent 的输入/输出 token 比约 100:1，缓存命中与未命中成本差 10 倍
2. **遮蔽，而非移除**：使用状态机 + logits 掩码管理工具可用性，避免动态增删工具导致 KV 缓存失效
3. **使用文件系统作为上下文**：文件系统是终极上下文——大小不受限、天然持久化、Agent 可直接操作；压缩策略始终设计为可恢复的
4. **通过复述操控[[注意力机制|注意力]]**：不断重写待办事项列表（如 todo.md），将全局计划推入模型近期[[注意力机制|注意力]]范围，避免"丢失在中间"
5. **保留错误的内容**：将失败尝试保留在上下文中，让模型隐式更新内部信念，降低重复同样错误的概率
6. **不要被[[少样本学习|少样本]]示例所困**：在行动和观察中引入结构化变化（不同序列化模板、替代性措辞、微小噪音），打破模式避免 Agent 陷入重复节奏

**核心哲学**：[[Context Engineering|上下文工程]]仍是一门新兴科学，但对于 Agent 系统已是必不可少。模型可能更强大、更快速、更经济，但再多的原始能力也无法替代对记忆、环境和反馈的需求。

## 来源

- [[raw/articles/ai-engineering/prompt-context/context-design.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Effective context engineering for AI agents.md]]
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic
- [Lost in the Middle (Liu et al. 2023)](https://arxiv.org/abs/2307.03172)
- [Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) — MemGPT
- [[raw/articles/ai-engineering/anthropic-developer/Compaction.md]] — Anthropic Compaction API 文档

## 相关

- [[分层记忆架构]]
- [[LLM-Statelessness]]
- [[检索增强生成]]
- [[Prompt缓存]]
- [[Agent Harness模式]]
- [[Claude-Code上下文工程全景]]
- [[上下文腐烂]] — 上下文工程的核心动机
- [[注意力预算]] — 核心约束条件
- [[即时上下文检索]] — 按需加载策略
- [[结构化笔记法]] — 长时任务持久记忆技术
- [[检索增强生成]] — 外部知识注入的主要技术路径
- [[情境化检索]] — 解决 RAG 上下文破坏的增强方案
- [[上下文压缩]] — 长时任务 Compaction 技术的官方 API 实现
- [[提示词缓存]] — 缓存优化与压缩协同工作
- [[工作台 vs 长期记忆]] — implements（上下文外部化的极端实践：工作台用完即扔，状态全存文件）
- [[Ralph Loop]] — implemented_by（工作台 vs 长期记忆模型的具体实现系统）
