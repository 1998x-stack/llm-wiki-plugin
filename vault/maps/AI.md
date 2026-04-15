---
type: map
topic: "AI"
page_count: 8
updated: 2026-04-15
---

# AI

## 概念
- [[ACP协议]] — **Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和... (confidence: 0.85)
- [[Agent Harness模式]] — **Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 La... (confidence: 0.9)
- [[DeepAgents中间件体系]] — DeepAgents 中间件（`libs/deepagents/deepagents/middleware/`）是 [[Agent Harness模式]] 的核... (confidence: 0.9)
- [[DeepAgents后端协议]] — DeepAgents 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtocol` 定... (confidence: 0.9)
- [[DeepAgents评估体系]] — DeepAgents 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹"（tra... (confidence: 0.9)
- [[LLM-as-Judge]] — 使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义**准则**打分，代替人工评估。适用于难以用规则/子串匹配表达的**语义正确性、风格、完... (confidence: 0.9)

## 实体
- [[DeepAgents]] — LangChain 官方开源的 **生产级 Agent Harness**（`langchain-ai/deepagents`），基于 [[LangGraph]... (confidence: 0.95)

## 综合分析
- [[DeepAgents评估设计哲学]] — DeepAgents 评估设计哲学：三重分离原则 (confidence: 0.9)
