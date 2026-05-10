---
type: concept
title: MCP 层工程亮点
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["MCP", "工程设计", "无状态", "工具设计", "MemPalace", "工具与框架"]
aliases: ["MCP Server Engineering", "MCP 设计原则"]
relates_to:
  - target: "[[MCP]]"
    type: implements
  - target: "[[MemPalace]]"
    type: part_of
  - target: "[[MCP 工具集成]]"
    type: extends
  - target: "[[HTTP 传输协议]]"
    type: uses
    confidence: 0.7
  - target: "[[Stdio 传输协议]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# MCP 层工程亮点

## 概述
[[MemPalace]] [[MCP Prompts|MCP Server]] 的三个核心工程设计原则：无状态架构、小粒度工具拆分、错误友好性，共同构成高可靠 Agent 工具层。

## 关键内容
- **无状态 Server**：[[MCP Prompts|MCP Server]] 本身不维护任何会话状态，所有状态存储在 [[ChromaDB]] 和 KG 文件中。Server 可随时重启而不丢失数据，符合云原生无状态[[服务]]最佳实践
- **工具粒度设计**：19 个工具被刻意设计成小粒度，而非一个"do everything"工具。小粒度让 AI Agent 能精确表达意图，同时使 token 消耗可预测
- **错误友好性**：所有工具返回结构化错误信息，包含建议的下一步操作（如"该 Wing 不存在，可用 Wing 列表：..."），降低 Agent 的重试成本和循环失败概率
- **跨模型兼容**：[[MCP Prompts|MCP Server]] 遵循标准协议，支持 [[Claude_Code|Claude]]（原生）、GPT-4o、[[Gemini CLI|Gemini]]、Llama（via [[Ollama]]）、Mistral 等多种模型
- **AAAK 跨模型可读**：AAAK 本质上是结构化英语缩写，任何能读英文的模型都能理解 Closet 内容，无需针对特定模型做适配
- **[[Claude Code]] Auto-save**：为 [[Claude Code]] 提供特殊自动保存功能，会话结束时自动保存关键决策和代码变更摘要

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_06_mcp_tools.md]] — MemPalace 深度解析第六篇：MCP 工具集成

## 相关
- [[MCP]] — implements
- [[MemPalace]] — part_of
- [[MCP 工具集成]] — extends
- [[ChromaDB]] — uses
