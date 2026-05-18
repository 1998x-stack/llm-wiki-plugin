---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agents, multi-agent-systems, coordination, AI工程]
aliases: ["协调器模式", "Orchestrator Agent"]
relates_to: 
  - target: "[[Agent Swarms]]"
    type: part_of
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[KAIROS]]"
    type: compares_to
supersedes: null
---

# Coordinator Mode

## 概述
Coordinator Mode是[[Claude Code]]中的[[Multi-Agent-Coordination-Patterns|多智能体协调模式]]，采用[[Orchestrator Agent]]指挥多个[[Worker Agent]]的架构，解决单个AI Agent在处理大型复杂任务时的局限性。

## 关键内容

1. **角色分离机制**：
   - [[Orchestrator Agent]]负责理解高层目标、[[任务分解]]、分配子任务、监控进度和[[质量保障|质量控制]]
   - [[Worker Agent]]s具有有限工具集、独立上下文和Token配额，专注于特定子任务

2. **核心设计特点**：
   - 使用System Prompt作为协调"[[算法]]"，而非传统代码逻辑
   - 遵循最小[[Permissions|权限]]原则，为每个[[Worker Agent|Worker]]分配特定工具集
   - 实现Token预算管理和任务依赖分析

3. **工作纪律指令**：
   - "Do not rubber-stamp weak work"（不要草率认可质量差的工作）
   - "理解结论前不得指导后续工作"
   - "遇到矛盾结果需先调查再接受"

## 来源
- [[Claude Code 源码泄露深度解析（四）：多智能体协调器——Coordinator Mode 与 Agent Swarms]] — 原文第1-42行

## 相关
- [[Agent Swarms]] — part_of
- [[Claude Code]] — relates_to
- [[Orchestrator Agent]] — extends