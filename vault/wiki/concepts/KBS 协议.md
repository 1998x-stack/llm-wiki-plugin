---
type: concept
title: KBS 协议
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [AI, Agent, 协议, 记忆检索, MemPalace, AI工程]
aliases: ["Know Before Speaking", "KBS Protocol", "先查后答协议"]
relates_to:
  - target: "[[MemPalace]]"
    type: part_of
  - target: "[[MCP]]"
    type: implements
  - target: "[[检索增强生成]]"
    type: extends
supersedes: null
---

# KBS 协议

## 概述
"[[Know Before Speaking 协议|Know Before Speaking]]"（先查后答）协议，强制 AI Agent 在回答关于用户历史的问题时，优先检索记忆系统而非依赖训练数据。

## 关键内容
- **触发机制**：每次调用 `mempalace_status` 时，响应体末尾自动附加协议指令
- **协议内容**：`BEFORE RESPONDING about any person, project, or past event: call mempalace_kg_query or mempalace_search FIRST. Do not rely on training data for questions about this user's history.`
- **软约束设计**：不是硬锁，而是 System Prompt 级别的指令，LLM 遵从率高
- **工程目的**：确保 [[MemPalace]] 不是"有了就用"的可选工具，而是 Agent 工作流中的强制检查点
- **与 RAG 的关系**：本质上是[[检索增强生成]]的行为约束层，确保检索优先于生成
- **实际效果**：Agent 给出带完整推理链的答案，从保存的原始对话中检索，而非凭模型训练数据猜测

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_06_mcp_tools.md]] — MemPalace 深度解析第六篇：MCP 工具集成

## 相关
- [[MemPalace]] — part_of
- [[MCP]] — implements
- [[检索增强生成]] — extends
