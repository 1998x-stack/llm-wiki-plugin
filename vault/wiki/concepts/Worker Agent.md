---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agents, multi-agent-systems, coordination, AI工程]
aliases: ["工作智能体", "Worker Agent", "Worker"]
relates_to:
  - target: "[[Coordinator Mode]]"
    type: part_of
    confidence: 0.85
  - target: "[[Claude Code]]"
    type: part_of
    confidence: 0.8
  - target: "[[Orchestrator Agent]]"
    type: reports_to
    confidence: 0.9
  - target: "[[Agent Swarms]]"
    type: member_of
    confidence: 0.85
supersedes: null
---

# Worker Agent

## 概述
Worker Agent是[[Claude Code]]多[[Agent Systems|智能体系统]]中的执行角色，拥有有限工具集、独立上下文和Token配额，负责执行[[Orchestrator Agent]]分配的具体子任务。

## 关键内容

1. **能力限制**：
   - 拥有有限的工具集
   - 独立的上下文空间
   - Token配额限制
   - 根据任务需求被分配特定[[Permissions|权限]]

2. **[[Permissions|权限]]管理**：
   - 遵循最小[[Permissions|权限]]原则，只获得完成任务必要的工具
   - 分析代码任务：仅授予FileReadTool、[[GrepTool]]
   - 运行测试任务：添加[[BashTool]]（可能受限）
   - 提交代码任务：添加GitCommitTool

3. **资源管理**：
   - 由[[Orchestrator Agent|Orchestrator]]分配Token预算
   - 当接近预算上限时生成部分结果摘要并返回
   - 防止单个Worker无限消耗资源

## 来源
- [[04_coordinator_mode.md]] — Claude Code 源码泄露解析

## 相关
- [[Orchestrator Agent]] — reports_to
- [[Coordinator Mode]] — part_of
- [[Agent Swarms]] — member_of
- [[Claude Code]] — part_of