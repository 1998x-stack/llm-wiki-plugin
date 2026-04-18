---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["editor", "IDE", "integration", "ACP", "developer-tools", "Agent系统"]
aliases: [ACP, Agent Communication Protocol, 编辑器集成]
relates_to:
  - target: "[[Gateway 消息网关]]"
    type: compares_to
    confidence: 0.7
  - target: "[[Hermes Agent]]"
    type: part_of
    confidence: 0.8
  - target: "[[SKILL.md 格式规范]]"
    type: uses
    confidence: 0.6
supersedes: null
---

# ACP 编辑器集成

## 概述
Agent Communication Protocol，[[Hermes Agent|Hermes]] 与代码编辑器集成的标准协议，让 IDE 中的 Agent 携带项目上下文而非从零开始。

## 关键内容
- **支持的编辑器**：VS Code（通过扩展）、Zed（原生支持）、JetBrains IDE 系列（通过插件）
- **工作流程**：编辑器中选中代码片段 → 右键 "Ask [[Hermes Agent|Hermes]]" → ACP 将选中代码 + 用户问题发给本地 [[Hermes Agent]] → Agent 结合项目上下文（[[语义记忆|MEMORY.md]]、[[Agent Skills|Skills]]）回答 → 结果显示在编辑器 sidebar
- **与 IDE 内置 AI 的差异**：ACP 使用的是本地已配置好的 [[Hermes Agent]]，携带记忆、技能、项目上下文，比从零开始的 IDE 插件更了解项目
- **在架构中的位置**：与 [[网关与路由器|Gateway]]、CLI、[[Batch Runner]] 同属[[三层分离架构]]的入口层，最终都调用 `AIAgent.run_conversation()`
- **上下文注入**：ACP 请求会注入项目级 [[语义记忆|MEMORY.md]]（[[语义记忆]]）、相关 [[SKILL.md 格式规范|SKILL.md]] 文件、选中代码片段，形成完整的开发上下文
- **与 [[网关与路由器|Gateway]] 的对比**：[[网关与路由器|Gateway]] 面向消息平台（Telegram/Slack 等），ACP 面向开发者工具（IDE），两者覆盖不同的使用场景但共享相同的 AIAgent 核心

## 来源
- [05_hermes_gateway.md](/raw/articles/ai-tools/hermes/05_hermes_gateway.md) — Hermes Agent 深度解析第五篇：Gateway 消息网关，2026 年 4 月版本

## 相关
- [[Gateway 消息网关]] — compares_to
- [[Hermes Agent]] — part_of
- [[SKILL.md 格式规范]] — uses
