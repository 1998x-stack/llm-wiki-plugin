---
type: map
topic: "AI工程"
page_count: 24
updated: 2026-04-16
---

# AI工程

## 概述

AI工程 相关概念与实体的集群。核心主题：Claude-Code-Hook-System、Context-Engineering、DeepAgents中间件体系、DeepAgents后端协议。

## 概念

- [[Claude-Code-Hook-System]] — Claude Code Hook System 是 Claude Code 编程助手提供的一种扩展机制，允许开发者通过编写脚本拦截和响应 AI 会话的生命周期事 (confidence: 0.9)
- [[Context-Engineering]] — Context Engineering（上下文工程）是指对 LLM 的有限[[上下文窗口]]进行策展与管理的系统化方法。Anthropic 将其定义为：在固定  (confidence: 0.92)
- [[DeepAgents中间件体系]] — [[DeepAgents]] [[ROS (Robot Operating System)|中间件]]（`libs/deepagents/deepagents/ (confidence: 0.9)
- [[DeepAgents后端协议]] — [[DeepAgents]] 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtoco (confidence: 0.9)
- [[DeepAgents评估体系]] — [[DeepAgents]] 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹" (confidence: 0.9)
- [[ExecPolicy]] — [[Codex CLI]] 的命令审批引擎，位于 [[Codex沙箱系统]] 之前。将"哪些命令允许、哪些需要审批、哪些禁止"从硬编码逻辑中解放出来，变成**可 (confidence: 0.9)
- [[LLM-Statelessness]] — LLM Statelessness（大型语言模型无状态性）是指主流大语言模型在设计上不具备跨会话记忆能力的固有特性。每一次 API 调用或新会话的开启，模型都从 (confidence: 0.95)
- [[LLM-Wire-Protocol统一模式]] — [[Mario-Zechner]] 在构建 [[Pi-Agent]] 的 pi-ai 层时发现：市面上 300+ LLM 模型归根结底只实现了四种 Wire P (confidence: 0.9)
- [[LLM-as-Judge]] — 使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义**准则**打分，代替人工评估。适用于难以用规则/子串匹配表达的**语义正确性、风格、完 (confidence: 0.9)
- [[MCP协议层]] — [[Codex CLI]] 的工具连接协议层。MCP（Model Context Protocol）是 Anthropic 提出的开放协议，让工具与 Agent (confidence: 0.9)
- [[Sprint合约制]] — Sprint 合约制是[[生成器-评估器架构]]三 Agent 系统中的一个机制：在每个 Sprint 开始前，**生成器（Generator）和评估器（Eva (confidence: 0.88)
- [[Think工具]] — Think 工具是一个无副作用的特殊工具：模型调用它时，输入文本被追加到日志中作为"思考"，不获取新信息，不修改任何状态。它为模型在复杂工具链中提供一个**结构 (confidence: 0.9)
- [[上下文焦虑]] — 上下文焦虑（Context Anxiety）是 LLM 在长时任务中的一种失败模式：模型感知到自身接近[[上下文窗口]]限制时，会**过早包装工作、草率结束任务 (confidence: 0.9)
- [[上下文腐烂]] — 上下文腐烂（Context Rot）是指随着 LLM [[上下文窗口]]中 token 数量增加，模型从上下文中**准确召回和推理信息的能力非均匀下降**的现象 (confidence: 0.95)
- [[上下文重置]] — 上下文重置（Context Reset）是长时 Agent 任务中的一种会话管理策略：**彻底清空[[上下文窗口]]，启动全新 Agent**，通过精心设计的* (confidence: 0.9)
- [[分层记忆架构]] — 分层记忆架构（Hierarchical Memory Architecture）是 [[Context-Engineering]] 的核心实现模式。将 LLM  (confidence: 0.9)
- [[即时上下文检索]] — 即时上下文检索（Just-in-Time Context Retrieval）是一种 Agent 信息管理策略：Agent **不在运行前预加载所有可能相关的数 (confidence: 0.9)
- [[情境化检索]] — 情境化检索（Contextual Retrieval）是 Anthropic 提出的 [[检索增强生成|RAG]] 增强方案：在将文档 Chunk 建立[[Em (confidence: 0.95)
- [[检索增强生成]] — 检索增强生成（Retrieval-Augmented Generation, RAG）是一种通过检索外部知识库中的相关信息并注入提示，来弥补 LLM 静态训练知 (confidence: 0.95)
- [[检索重排序]] — 检索重排序（Retrieval Reranking）是 [[检索增强生成|RAG]] 流水线中的精排步骤：在初始召回（粗排）获得大量候选 Chunk 后，用专门 (confidence: 0.9)
- [[注意力预算]] — 注意力预算（Attention Budget）是对 [[Transformer架构|Transformer]] 模型处理上下文时有限注意力资源的比喻性描述：每个 (confidence: 0.9)
- [[跨Provider上下文迁移]] — Context Handoff 是 [[Pi-Agent]] pi-ai 层最独特的能力：一个会话可以在 Anthropic → OpenAI → [[Goog (confidence: 0.85)

## 综合分析

- [[Claude-Code-TOOL-设计七维分析]] — 本分析综合了 8 个知识库页面，从七个维度系统拆解 Claude Code 的 TOOL 设计为何被视为业界标杆。核心洞见：**Claude Code 不是把工 (confidence: 0.95)
- [[DeepAgents评估设计哲学]] — ## 洞见 (confidence: 0.9)
