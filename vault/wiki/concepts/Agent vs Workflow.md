---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["agent-architecture", "design-principle", "workflow"]
aliases: ["Agent 与工作流", "智能体与工作流", "Agent vs Workflow Distinction"]
relates_to:
  - "[[AI Agent 架构模式]] — relates_to"
  - "[[Prompt Chaining]] — relates_to"
  - "[[Routing 模式]] — relates_to"
  - "[[Parallelization 模式]] — relates_to"
  - "[[Orchestrator-Workers 模式]] — relates_to"
  - "[[Evaluator-Optimizer 模式]] — relates_to"
supersedes: null
---

# Agent vs Workflow

## 概述
Anthropic 提出的关键架构区分：Workflow 通过预定义代码路径协调 LLM 和工具（确定性），Agent 由 LLM 动态指导自身过程和工具使用（灵活性）。

## 关键内容
1. **Workflow（工作流）定义**：LLM 和工具通过**预定义代码路径**进行协调。特征：确定性、可预测、适合结构化任务。提供一致性和可重复性。
2. **Agent（智能体）定义**：LLM **动态指导**自己的过程和工具使用。特征：灵活性、自主性、适合开放性任务。提供模型驱动的决策能力。
3. **选择错误的代价**：选择错误的范式会带来巨大的维护成本。工作流用于开放任务会僵化，Agent 用于结构化任务会不可预测。
4. **决策原则**：除非任务天然开放且步骤无法预判，否则工作流通常优于自主 Agent。先测试单次优化的 LLM 调用是否满足需求，再考虑引入架构。
5. **五种模式的归属**：Prompt Chaining、Routing、Parallelization、Orchestrator-Workers、Evaluator-Optimizer 都属于工作流范式，是确定性与灵活性的不同平衡点。

## 来源
- [[01_building_effective_agents.md]] — 第二章，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[AI Agent 架构模式]] — relates_to (架构选择的核心原则)
- [[Prompt Chaining]] — relates_to (属于工作流范式)
- [[Routing 模式]] — relates_to (属于工作流范式)
- [[Parallelization 模式]] — relates_to (属于工作流范式)
- [[Orchestrator-Workers 模式]] — relates_to (属于工作流范式，但最接近 Agent)
- [[Evaluator-Optimizer 模式]] — relates_to (属于工作流范式)
