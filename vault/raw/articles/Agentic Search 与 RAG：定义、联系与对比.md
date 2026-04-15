**Agentic Search 与 RAG：定义、联系与对比**

|  |
| --- |
| **适用场景**：LLM 应用研发、AI 架构设计、技术选型 **更新时间**：2025–2026 |

|  |
| --- |
| [**1. RAG 是什么**](#heading_0)  [**定义**](#heading_1)  [**传统 RAG 的工作流程**](#heading_2)  [**RAG 的关键组件**](#heading_3)  [**RAG 的主要变体**](#heading_4)  [**RAG 的优势与局限**](#heading_5)  [**2. Agentic Search 是什么**](#heading_6)  [**定义**](#heading_7)  [**Agentic Search 的工作流程**](#heading_8)  [**Agentic Search 的核心能力**](#heading_9)  [**Agentic Search 的主流实现模式**](#heading_10)  [**3. 两者的联系**](#heading_11)  [**演进关系**](#heading_12)  [**本质关系**](#heading_13)  [**互补关系图**](#heading_14)  [**4. 核心对比**](#heading_15)  [**全维度对比表**](#heading_16)  [**能力雷达图（定性）**](#heading_17)  [**5. 架构图对比**](#heading_18)  [**传统 RAG 架构**](#heading_19)  [**Agentic Search 架构**](#heading_20)  [**6. 技术栈对比**](#heading_21)  [**RAG 技术栈**](#heading_22)  [**Agentic Search 技术栈**](#heading_23)  [**7. 选型指南**](#heading_24)  [**决策树**](#heading_25)  [**快速对照**](#heading_26) |

1. **RAG 是什么**

**定义**

**RAG（Retrieval-Augmented Generation，检索增强生成）** 是一种将外部知识库检索与 LLM 生成能力结合的架构模式。其核心思路是：

|  |
| --- |
| LLM 不依赖"记忆"（训练参数），而是在生成答案前先从可信知识库中"查阅"相关文档片段，用检索到的证据来辅助生成。 |

类比：**开卷考试**——模型带着参考资料作答，而非纯靠记忆。

**传统 RAG 的工作流程**

|  |
| --- |
| Plain Text 用户提问  │  ▼ [查询向量化] ──► 嵌入模型（Embedding Model）  │  ▼ [向量检索] ──► 向量数据库（Milvus / Faiss / Qdrant）  │  ▼ [上下文注入] ──► Top-K 文档片段 → 拼入 Prompt  │  ▼ [LLM 生成] ──► 基于检索结果生成答案  │  ▼ 最终回答 |

**RAG 的关键组件**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**RAG 的主要变体**

|  |
| --- |
| Plain Text 传统 RAG（Naive RAG）  └─ 单次固定检索 → 生成  高级 RAG（Advanced RAG）  ├─ HyDE（假设文档嵌入）  ├─ RAPTOR（层级摘要树）  ├─ Self-RAG（自反思检索）  └─ CRAG（修正型 RAG）  GraphRAG  └─ 知识图谱 + 实体关系检索（适合全局摘要型问题）  Agentic RAG ──► 见第2节 |

**RAG 的优势与局限**

**✅ 优势**

* 知识可实时更新，无需重训练模型
* 答案可溯源、可引用，减少幻觉
* 固定检索路径，延迟低且可预测
* 适合知识密集型 QA 场景

**❌ 局限**

* 单次 top-k 检索，无法处理多步推理
* Chunking 破坏文档结构，语境可能丢失
* 复杂问题（跨文档、多跳）表现差
* 检索质量高度依赖 Embedding 模型

2. **Agentic Search 是什么**

**定义**

**Agentic Search（智能体搜索）** 是将搜索/检索行为嵌入 AI Agent 决策循环中的架构模式。与 RAG 的"一次检索 → 生成"不同，Agentic Search 让 LLM **主动决定**：

* **何时**需要搜索
* **搜什么**（动态构造查询）
* **搜多少次**（迭代直到满足需求）
* **如何整合**多次搜索结果

类比：**研究助理**——不只是取书，而是读书、找相关材料、验证结论、写报告的完整过程。

**Agentic Search 的工作流程**

|  |
| --- |
| Plain Text 用户任务  │  ▼ [LLM 规划] ──► 任务分解、子问题生成  │  ▼ [工具调用] ──► 选择：向量搜索 | 关键词搜索 | 文件读取 | API 调用 | 代码执行  │  ▼ [结果观察] ──► 评估检索结果是否满足需求  │  ▼ [迭代判断] ──► 需要更多信息？→ 重新搜索（修改查询）  │ 满足要求？→ 进入生成  ▼ [LLM 生成] ──► 综合多轮搜索结果生成答案  │  ▼ 最终回答（含推理过程） |

**Agentic Search 的核心能力**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**Agentic Search 的主流实现模式**

|  |
| --- |
| Plain Text ReAct 模式  └─ Reasoning → Action → Observation → 循环  RAISE 模式  └─ ReAct + 短期记忆 + 长期记忆  Corrective RAG（CRAG）  └─ 检索后自动评估质量，质量差则重新搜索  Self-RAG  └─ 模型本身输出"是否需要检索"的判断令牌  Deep Research 模式  └─ 多轮搜索 + 规划 + 报告生成（Perplexity / Gemini） |

3. **两者的联系**

**演进关系**

|  |
| --- |
| Plain Text 传统 LLM（纯生成）  │  ▼ Naive RAG（单次检索增强）  │  ▼ Advanced RAG（HyDE / RAPTOR / Hybrid Retrieval）  │  ▼ Agentic RAG（检索融入 Agent 循环）  │  ▼ Agentic Search（搜索作为 Agent 核心能力） |

**本质关系**

* **RAG 是 Agentic Search 的底层工具之一**：Agent 在执行 Agentic Search 时，可以将向量检索（RAG）作为其众多工具之一来调用
* **Agentic Search 是 RAG 的"超集"**：传统 RAG 是静态管道，Agentic Search 是动态决策循环
* **Agentic RAG = RAG + Agent 控制层**：是两者的融合形态

**互补关系图**

|  |
| --- |
| Plain Text ┌─────────────────────────────────────────────────────┐ │ Agentic Search │ │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────────────┐ │ │ │ 向量RAG │ │ BM25搜索 │ │ grep/ls/read │ │ │ │ (工具1) │ │ (工具2) │ │ (工具3) │ │ │ └─────────┘ └─────────┘ └─────────────────┘ │ │ │ │ ┌─────────┐ ┌─────────┐ ┌─────────────────┐ │ │ │ API调用 │ │ 代码执行 │ │ 知识图谱查询 │ │ │ │ (工具4) │ │ (工具5) │ │ (工具6) │ │ │ └─────────┘ └─────────┘ └─────────────────┘ │ └─────────────────────────────────────────────────────┘ |

4. **核心对比**

**全维度对比表**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**能力雷达图（定性）**

|  |
| --- |
| Plain Text  复杂推理  10  │  ┌──────┼──────┐  多源整合 8 ────│Agentic├──── 8 准确性  │ │Search│ │  │ │ │ │  可控性 6 ────┤ ├──── 6 可解释  │ ╔══╪══╗ │ │  │ ║ RAG ║ │ │  延迟低 10 ╢ ╟── 4 多源整合  └──╚══╪══╝───┘  │  4  token效率 |

5. **架构图对比**

**传统 RAG 架构**

|  |
| --- |
| Plain Text 离线索引阶段： 文档 → Chunking → Embedding → 向量库  在线查询阶段： 用户问题 ──► Embedding ──► 向量检索 ──► Top-K Chunks  │  ▼  [Prompt 组装]  │  ▼  LLM  │  ▼  答案 |

**Agentic Search 架构**

|  |
| --- |
| Plain Text 用户任务  │  ▼ ┌───────────────────────────────┐ │ Agent 核心 │ │ │ │ ┌─────────────────────────┐ │ │ │ Planning / ReAct │ │ │ └────────────┬────────────┘ │ │ │ │ │ ┌──────────▼──────────┐ │ │ │ Tool Dispatcher │ │ │ └──┬───────┬──────┬───┘ │ │ │ │ │ │ └───────┼───────┼──────┼────────┘  │ │ │  ▼ ▼ ▼  向量RAG grep/ls API调用  │ │ │  └───────┴──────┘  │  ┌───────▼───────┐  │ 观察 & 评估 │  └───────┬───────┘  │ 不满足需求  ▼  继续搜索（迭代）  │ 满足需求  ▼  最终生成 |

6. **技术栈对比**

**RAG 技术栈**

|  |
| --- |
| Plain Text 数据层： PDF / MD / 代码 / 数据库 处理层： LangChain / LlamaIndex / RAGFlow 嵌入层： OpenAI Embeddings / BGE / Qwen-Embed 存储层： Milvus / Qdrant / Faiss / pgvector 检索层： Hybrid Search (BM25 + Dense) + Reranker 生成层： GPT-4 / Claude / Qwen |

**Agentic Search 技术栈**

|  |
| --- |
| Plain Text 编排层： LangGraph / AutoGen / CrewAI / Agno 工具层： MCP (Model Context Protocol) 工具集 检索工具： 向量库 + grep + LSP + 文件系统 记忆层： 短期（上下文窗口）+ 长期（外部存储） 评估层： LLM-as-Judge / 自反思机制 生成层： GPT-4o / Claude Sonnet / Qwen 观测层： LangSmith / Langfuse / OpenTelemetry |

7. **选型指南**

**决策树**

|  |
| --- |
| Plain Text 你的场景是什么？ │ ├─► 知识库 QA / 文档问答（FAQ类） │ │ │ └─► ✅ 传统 RAG 即可 │ ├─► 多跳推理 / 跨文档综合分析 │ │ │ └─► ✅ Agentic Search 或 GraphRAG │ ├─► 代码仓库探索 / Bug 修复 │ │ │ ├─► 小型项目 → ✅ Agentic Search（grep + 文件读取） │ └─► 大型单一概念搜索 → ✅ RAG 辅助 Agentic Search │ ├─► 实时数据 / 动态信息 │ │ │ └─► ✅ Agentic Search（工具调用实时API） │ └─► 对延迟要求严格（< 2s）  │  └─► ✅ 传统 RAG（固定管道，可预测） |

**快速对照**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

|  |
| --- |
| **结论**：传统 RAG 是稳定、高效、可预测的"精准武器"；Agentic Search 是灵活、强大、高成本的"全能解法"。最佳实践往往是**以 Agentic Search 为骨架，以 RAG 为其工具之一**的混合架构。 |