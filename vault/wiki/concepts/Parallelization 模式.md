---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["agent-pattern", "workflow", "parallel-processing"]
aliases: ["并行化模式", "Parallel Processing", "Fork-Join"]
relates_to:
  - "[[AI Agent 架构模式]] — part_of"
  - "[[Agent vs Workflow]] — relates_to"
supersedes: null
---

# Parallelization 模式

## 概述
LLM 同时处理多个独立子任务，输出以程序化方式聚合，包含分区（Sectioning）和投票（Voting）两个关键变体。

## 关键内容
1. **工作流程**：Input → [LLM-1] + [LLM-2] + [LLM-3] → [Aggregator] → Output。多个 LLM 并行处理，结果由聚合器整合。
2. **两个关键变体**：
   - **分区（Sectioning）**：将任务分解为并行独立子任务，各自处理不同部分
   - **投票（Voting）**：同一任务运行多次，获取多样输出以提高置信度
3. **适用场景**：子任务可并行加速，或需要多视角/多次尝试以获得高置信度结果。
4. **经典应用**：内容安全审查（主任务 + 安全检查并行）是一个经典应用，比让同一 LLM 同时处理两个关注点效果更好。
5. **与软件工程的对应**：Parallelization 对应 Fork-Join 模式和 MapReduce 模式，先分后合的并行计算范式。

## 来源
- [[01_building_effective_agents.md]] — 第三章 3.4 节，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[AI Agent 架构模式]] — part_of (五种核心模式之一)
- [[Orchestrator-Workers 模式]] — compares_to (都涉及并行处理)
- [[Agent vs Workflow]] — relates_to (属于工作流范式)
