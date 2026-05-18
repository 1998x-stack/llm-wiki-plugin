---
type: concept
status: active
confidence: 0.75
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [Agent系统, 架构模式, 多Agent]
aliases: ["Agent Composability", "Agent 可组合性", "Composable Agent Pattern"]
relates_to:
  - target: "[[MCP协议层]]"
    type: implements
  - target: "[[MCP]]"
    type: uses
  - target: "[[Multi-Agent-Coordination-Patterns]]"
    type: part_of
  - target: "[[Orchestrator-Subagent-Pattern]]"
    type: extends
supersedes: null
---

# Agent可组合性

## 概述
通过标准化协议（如 MCP）使 Agent 实例既能调用其他工具，又能将自身暴露为工具，从而在更大系统中作为可插拔节点被组合和编排的架构属性。

## 关键内容

1. **核心机制**：Agent 同时具备双重身份——作为 Client 消费外部工具，作为 Server 暴露自身能力。这种双向性使 Agent 可以像乐高积木一样被任意组合。

2. **实现路径**：
   ```
   父级 Orchestrator Agent
       ├── 调用 codex_exec("写测试")    → Codex 子 Agent
       ├── 调用 codex_exec("生成文档")   → Codex 子 Agent
       └── 调用 codex_review("检查PR")  → Codex 子 Agent
   ```
   父 Agent 负责协调和[[任务分解]]，[[Codex CLI|Codex]] 作为执行节点被动态调用。

3. **协议依赖**：依赖 [[MCP]] 等标准化协议实现解耦。任何支持 MCP 的 Agent 都可以被任何支持 MCP 的 [[Orchestrator Agent|Orchestrator]] 发现和调用，无需定制集成代码。

4. **与 [[Orchestrator-Subagent-Pattern]] 的关系**：可组合性是实现编排模式的底层能力。[[Orchestrator Agent|Orchestrator]] 模式是顶层架构设计，可组合性确保[[子 Agent & 多 Agent 系统|子 Agent]] 可以被不同父级复用。

5. **工程意义**：
   - **工具集成[[Configuration|配置]]化**：从"写集成代码"变成"写[[Configuration|配置]]文件"
   - **Agent 复用**：同一 [[Codex CLI|Codex]] 实例可被 [[Cursor]]、父级 Agent、CI 流水线等不同消费者调用
   - **生态效应**：类似 USB-C 标准，协议统一后工具和[[服务]]自动可插拔

## 来源
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — Codex MCP Layer 深度解析

## 相关
- [[MCP协议层]] — implements
- [[MCP]] — uses
- [[Multi-Agent-Coordination-Patterns]] — part_of
- [[Orchestrator-Subagent-Pattern]] — extends
