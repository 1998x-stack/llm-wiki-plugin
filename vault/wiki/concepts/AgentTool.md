---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI工具, 代码助手, 智能体系统, 多智能体, AI工程]
aliases: ["AgentTool"]
relates_to: 
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[Tool System]]"
    type: part_of
  - target: "[[Sub Agent]]"
    type: generates
supersedes: null
---

# AgentTool

## 概述
[[Claude Code]]最强大的工具之一，允许主Agent生成子Agent来并行处理子任务，实现递归Agent架构。

## 关键内容
1. **递归Agent架构**：主Agent（[[Orchestrator Agent|Orchestrator]]）通过AgentTool调用生成多个子Agent（如分析前端代码的子Agent A、分析后端API的子Agent B、查找相关测试的子Agent C），子Agent完成任务后将结果返回给主Agent进行整合。

2. **访问控制机制**：
   - [[allowedTools|工具白名单]]：子Agent只能使用主Agent授权的工具子集
   - 递归深度限制：防止无限嵌套
   - Token预算分配：每个子Agent有独立的token配额

3. **架构优势**：通过并行处理多个子任务，提高复杂任务的处理效率，同时保持各子任务的独立性和安全性。

## 来源
- [[Claude Code 源码泄露深度解析（二）：核心 Agent 引擎与 40+ 工具系统]] — 全文

## 相关
- [[Claude Code]] — part_of
- [[Tool System]] — part_of
- [[Sub Agent]] — generates
- [[CoordinatorTool]] — relates_to