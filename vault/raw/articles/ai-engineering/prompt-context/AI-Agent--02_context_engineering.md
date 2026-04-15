# 第二阶段：Context Engineering（上下文工程）

> **定义**：系统性地设计、构建、管理和优化输入到 LLM 上下文窗口中的所有信息——包括其内容、结构、来源、时序和动态组装逻辑——以稳定、可扩展地实现复杂 AI 应用目标的工程学科。

---

## 一、诞生条件（Birth Conditions）

### 技术触发因素

| 触发点 | 时间 | 内容 |
|--------|------|------|
| 长上下文窗口出现 | 2023 | Claude 100K、GPT-4-turbo 128K，窗口从"稀缺资源"变为"待管理空间" |
| RAG 范式成熟 | 2023 | LlamaIndex / LangChain 标准化检索增强生成工作流 |
| Agent 框架崛起 | 2023–2024 | AutoGPT、LangGraph、CrewAI 使多轮工具调用成为标准 |
| 工具调用（Function Calling）标准化 | 2023 | OpenAI Function Calling API，工具结果需要结构化注入上下文 |
| 模型能力上移 | 2024 | 推理质量提升，"上下文组装质量"成为主要瓶颈 |

### 认知转折

```
旧认知（Prompt Engineering 时代）：
"如何让模型理解我的指令？"

新认知（Context Engineering 时代）：
"如何让模型在正确的时间，拥有完成任务所需的全部、且仅有必要的信息？"
```

关键推手：Andrej Karpathy 2024 年提出"Context Engineering > Prompt Engineering"，
将这一概念正式推向主流视野。

---

## 二、5W2H 分析

### What — 是什么

Context Engineering 管理的不再只是"提示词"，而是整个上下文窗口的**信息架构**：

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

### Why — 为什么

**定理**：上下文质量 = 模型输出质量的上界。

```
即使是最强的模型：
  - 给错信息 → 输出错误答案（垃圾进，垃圾出）
  - 信息缺失 → 幻觉填充
  - 信息冗余 → 注意力稀释（Lost in the Middle 问题）
  - 信息无序 → 推理链断裂

Context Engineering 的核心价值：
  确保模型每次生成时，
  面对的是"恰好够用、高质量、结构清晰"的信息
```

### Who — 谁在用

| 角色 | 工作内容 |
|------|------|
| AI 应用工程师 | 设计 RAG 管道、记忆系统、上下文压缩策略 |
| LLM 平台团队 | 构建多租户上下文管理基础设施 |
| Agent 系统开发者 | 设计 Agent 的状态管理和信息流架构 |
| ML 工程师 | 评估上下文策略对模型性能的影响 |

### When — 什么时候

- **2023 Q1–Q2**：LangChain/LlamaIndex 推动 RAG 成为标配
- **2023 Q3**：Claude 100K 上下文，出现"如何利用长窗口"的工程问题
- **2024 Q1**：Karpathy 提出 Context Engineering，概念正式命名
- **2024 全年**：MCP（Model Context Protocol）标准化上下文注入协议
- **2025**：Context Engineering 成为 AI 应用工程师核心技能

### Where — 应用场景

- **企业知识库问答**：RAG + 动态检索 + 重排序
- **多轮对话助手**：对话历史管理 + 记忆压缩
- **代码助手**：代码库上下文动态注入（如 Claude Code 的 @ 引用）
- **Agent 系统**：工具调用链的状态传递
- **文档处理**：长文档分块策略 + 滑动窗口

### How — 怎么做

#### 核心技术体系

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

### How Much — 规模/代价

| 维度 | 数据 |
|------|------|
| 典型上下文窗口 | 128K–1M tokens（2024–2025） |
| RAG 检索延迟 | 50–200ms（向量检索） |
| 记忆系统存储 | 用户级 KB 到 GB 不等 |
| 工程复杂度 | 中高（需要维护检索管道 + 记忆系统 + 压缩策略） |
| Token 成本 | 上下文越长，成本线性增长 |

---

## 三、核心技术机理

### 注意力稀释原理

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

### RAG 的检索-生成耦合

```
检索质量 → 上下文质量 → 生成质量

关键洞察：
- 检索召回的"假相关"文档 → 幻觉注入
- 检索遗漏的"关键信息" → 知识缺失幻觉
- 最优策略：
  precision@k 和 recall@k 需要同时优化
  不是"检索越多越好"
```

### 记忆的神经科学类比

```
人类记忆系统          LLM 记忆系统
─────────────────     ──────────────────
工作记忆（7±2项）  →   Context Window（有限）
海马体编码           →   Embedding + 向量存储
长期记忆             →   外部知识库
遗忘曲线             →   摘要压缩策略
```

---

## 四、代表性工程框架

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

---

## 五、局限性与失效边界

| 局限 | 表现 | 根因 |
|------|------|------|
| 检索错误级联 | 错误检索 → 错误生成，且难以溯源 | RAG 管道中间态不透明 |
| 上下文窗口仍有上限 | 超长文档仍需截断或压缩 | Transformer O(n²) 复杂度 |
| 多智能体协调困难 | 多个 Agent 共享上下文时状态冲突 | 无统一状态管理原语 |
| 工程复杂度高 | 检索+压缩+注入+评估，维护成本高 | 无标准化"上下文操作系统" |
| 实时知识延迟 | 数据入库 → 可检索存在时间差 | 向量数据库更新延迟 |

---

## 六、历史地位

Context Engineering 是 LLM 工程的**第一个真正的系统性工程学科**：

- 将"AI 应用质量"问题从"模型问题"转移到"工程问题"
- 确立了"信息架构 + 检索系统 + 记忆管理"的三角支柱
- 为 Agent 系统提供了状态管理的理论基础
- 但仍以**人类为中心**：人类设计流程，Agent 执行单步

> **核心隐喻**：Context Engineer = 图书馆员。不管理书的内容（模型），而是管理"哪些书、以什么顺序、放在读者面前"。让读者（LLM）在最短时间内找到并理解正确信息。
