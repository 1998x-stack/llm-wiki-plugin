---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [protocol, tool-integration, anthropic, standard, AI工程]
aliases: ["MCP", "模型上下文协议", "Model Context Protocol"]
relates_to:
  - "[[Anthropic]] — created_by"
  - "[[ACI (Agent-Computer Interface)]] — implements"
  - "[[AI Agent 架构模式]] — relates_to"
supersedes: null
---

# Model Context Protocol

## 概述
[[Anthropic]] 提出的工具生态集成协议，用于标准化第三方工具与 LLM 的交互接口，是 [[ACI 设计原则]]的具体实现。

## 关键内容
1. **协议定位**：Model Context Protocol (MCP) 是 [[Anthropic]] 提出的开放标准，用于 AI Agent 与外部工具/数据源之间的通信。
2. **与增强型 LLM 的关系**：增强型 LLM 需要检索（Retrieval）、工具（[[Tool System|Tools]]）和记忆（Memory）三类增强能力，MCP 提供了集成第三方工具生态的标准化方式。
3. **ACI 实践**：MCP 是 [[ACI (Agent-Computer Interface)]] 设计原则的具体实践，通过标准化的工具定义和接口文档，降低 Agent 使用工具的复杂度。
4. **行业影响**：MCP 被称为"AI 的 USB 接口"，旨在统一不同 AI 工具生态之间的互操作性。

## 来源
- [[01_building_effective_agents.md]] — 第三章 3.1 节，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[Anthropic]] — created_by (开发方)
- [[ACI (Agent-Computer Interface)]] — implements (ACI 原则的具体实现)
- [[AI Agent 架构模式]] — relates_to (增强型 LLM 的工具集成方式)
