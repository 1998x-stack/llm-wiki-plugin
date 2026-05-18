---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agents, multi-agent-systems, parallel-processing, AI工程]
aliases: ["Agent 群", "Worker Agent"]
relates_to: 
  - target: "[[Coordinator Mode]]"
    type: part_of
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[Orchestrator Agent]]"
    type: works_with
supersedes: null
---

# Agent Swarms

## 概述
Agent Swarms是[[Claude Code]]中的一种并行Agent处理架构，通过并行执行多个[[Worker Agent]]来提高大型复杂任务的处理效率。

## 关键内容

1. **实现机制**：
   - 使用Node.js [[Worker Agent|Worker]] Threads或独立进程实现真正并行运行
   - [[Worker Agent|Worker]]间内存隔离，避免状态污染
   - 通过IPC（进程间通信）与Coordinator通信

2. **结果汇聚机制**：
   - 冲突检测：处理不同[[Worker Agent|Worker]]的矛盾结论
   - 结果去重：避免相同发现重复记录
   - 优先级排序：根据重要性对发现进行排序
   - 质量验证：确保接收结果的质量

3. **容错处理**：
   - 单个[[Worker Agent|Worker]]失败不影响整个Swarm
   - 支持重试机制（最多N次）
   - 支持降级处理（跳过失败[[Worker Agent|Worker]]，接受部分结果）

## 来源
- [[Claude Code 源码泄露深度解析（四）：多智能体协调器——Coordinator Mode 与 Agent Swarms]] — 原文第135-174行

## 相关
- [[Coordinator Mode]] — part_of
- [[Claude Code]] — relates_to
- [[Worker Agent]] — extends