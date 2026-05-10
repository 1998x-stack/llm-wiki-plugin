---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agents, multi-agent-systems, coordination]
aliases: ["协调器智能体", "Orchestrator Agent", "Orchestrator"]
relates_to:
  - target: "[[Coordinator Mode]]"
    type: part_of
    confidence: 0.85
  - target: "[[Claude Code]]"
    type: part_of
    confidence: 0.8
  - target: "[[Worker Agent]]"
    type: manages
    confidence: 0.9
  - target: "[[Agent Swarms]]"
    type: coordinates
    confidence: 0.8
supersedes: null
---

# Orchestrator Agent

## 概述
Orchestrator Agent是[[Claude Code]]多[[Agent Systems|智能体系统]]中的协调器角色，负责理解用户高层目标、分解任务、分配子任务给[[Worker Agent]]s、监控执行进度、整合结果并执行[[质量保障|质量控制]]。

## 关键内容

1. **核心职责**：
   - 理解用户的高层目标
   - 将任务分解为独立子任务
   - 分配子任务给[[Worker Agent]]s
   - 监控执行进度
   - 整合所有结果
   - 执行[[质量保障|质量控制]]

2. **工作纪律指令**：
   - 不要草率认可质量差的工作("Do not rubber-stamp weak work")
   - 在指导后续工作前必须理解结论("Understand findings before directing follow-up work")
   - 遇到矛盾输出时先调查再接受

3. **核心[[算法]]设计**：
   - 使用自然语言System Prompt作为核心"[[算法]]"而非传统代码约束
   - 体现了用自然语言描述行为规范的创新哲学

## 来源
- [[04_coordinator_mode.md]] — Claude Code 源码泄露解析

## 相关
- [[Coordinator Mode]] — part_of
- [[Worker Agent]] — manages
- [[Agent Swarms]] — coordinates
- [[Claude Code]] — part_of