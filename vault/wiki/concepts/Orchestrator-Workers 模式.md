---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["agent-pattern", "workflow", "dynamic-decomposition"]
aliases: ["编排器-工作者模式", "Master-Worker", "动态任务分解"]
relates_to:
  - "[[AI Agent 架构模式]] — part_of"
  - "[[Agent vs Workflow]] — relates_to"
supersedes: null
---

# Orchestrator-Workers 模式

## 概述
中央 LLM（Orchestrator）动态分解任务、委派给工作 LLM，并综合结果，子任务由编排器根据具体输入动态确定而非预先定义。

## 关键内容
1. **工作流程**：Input → [Orchestrator] → [Worker-A] + [Worker-B] + [Worker-C] → [Synthesizer] → Output。编排器先分析任务，再动态决定需要多少工作者。
2. **与并行化的关键区别**：子任务是由 Orchestrator 根据具体输入**动态确定**的，而非预先定义。这是工作流模式中最接近 Agent 自主性的模式。
3. **适用场景**：无法预判所需子任务数量的复杂任务，如修改多个文件的代码任务、需要动态分析的研究任务。
4. **工程价值**：在任务复杂度不确定时，让模型自行决定分解策略，避免人工预设的僵化结构。
5. **与软件工程的对应**：Orchestrator-Workers 对应 Master-Worker 模式和 Actor Model，中央协调器动态分配任务给工作节点。

## 来源
- [[01_building_effective_agents.md]] — 第三章 3.5 节，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[AI Agent 架构模式]] — part_of (五种核心模式之一)
- [[Parallelization 模式]] — compares_to (都涉及并行，但任务分配方式不同)
- [[Agent vs Workflow]] — relates_to (属于工作流范式，但最接近自主 Agent)
