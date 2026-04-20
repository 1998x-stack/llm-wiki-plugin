---
type: concept
status: active
confidence: 0.95
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: ["agent-architecture", "engineering-patterns", "anthropic"]
aliases: ["AI Agent 模式", "Agent 构建模式", "Agent Building Patterns"]
relates_to:
  - "[[Anthropic]] — source"
  - "[[Prompt Chaining]] — part_of"
  - "[[Routing 模式]] — part_of"
  - "[[Parallelization 模式]] — part_of"
  - "[[Orchestrator-Workers 模式]] — part_of"
  - "[[Evaluator-Optimizer 模式]] — part_of"
  - "[[Agent vs Workflow]] — relates_to"
supersedes: null
---

# AI Agent 架构模式

## 概述
Anthropic 提出的五种核心 AI Agent 构建模式，从简单的 Prompt Chaining 到完全自主的 Agent，构成了一套可组合的模式分类学框架。后续深化至长时运行场景，衍生出 [[Harness 设计]] 框架。

## 关键内容
1. **设计哲学**：最成功的 Agent 实现并非依赖复杂框架，而是使用简单的可组合模式（simple, composable patterns）。Anthropic 建议开发者直接使用 LLM API，许多模式仅需几行代码即可实现。
2. **五种核心模式**：[[Prompt Chaining]]（提示链）、[[Routing 模式]]（路由）、[[Parallelization 模式]]（并行化）、[[Orchestrator-Workers 模式]]（编排器-工作者）、[[Evaluator-Optimizer 模式]]（评估器-优化器）。这五种模式与软件工程经典设计模式存在深刻对应关系。
3. **模式与软件工程的对应**：Prompt Chaining ↔ Chain of Responsibility/Pipeline；Routing ↔ Strategy Pattern；Parallelization ↔ Fork-Join/MapReduce；Orchestrator-Workers ↔ Master-Worker/Actor Model；Evaluator-Optimizer ↔ Feedback Control Loop。
4. **工作流 vs Agent 的选择**：[[Agent vs Workflow]] 是关键架构区分。工作流提供确定性和一致性，Agent 提供灵活性和模型驱动决策。除非任务天然开放且步骤无法预判，否则工作流通常优于自主 Agent。
5. **ACI 设计原则**：[[ACI (Agent-Computer Interface)]] 需要与 HCI 同等重视，工具定义应包含示例用法、边缘情况、输入格式要求，参数名称要让意图显而易见。
6. **长时运行深化**：针对应用开发场景，Anthropic 提出 [[Harness 设计]] 框架，包含 [[特性追踪器]]、[[上下文传递协议]]、[[智能检查点触发]]、[[三级自主权模型]]、[[持续验证循环]] 和 [[技术债务追踪]] 六大核心组件，本质上是"为 AI Agent 定制的 CI/CD 系统"。

## 来源
- [[01_building_effective_agents.md]] — 全文，Anthropic Engineering Blog "Building effective agents"
- [[14_harness_design_long_running.md]] — 长时运行应用开发场景的 Harness 设计深化

## 相关
- [[Anthropic]] — source (提出方)
- [[Prompt Chaining]] — part_of (五种模式之一)
- [[Routing 模式]] — part_of (五种模式之一)
- [[Parallelization 模式]] — part_of (五种模式之一)
- [[Orchestrator-Workers 模式]] — part_of (五种模式之一)
- [[Evaluator-Optimizer 模式]] — part_of (五种模式之一)
- [[Agent vs Workflow]] — relates_to (架构选择原则)
- [[ACI (Agent-Computer Interface)]] — relates_to (接口设计原则)
- [[Harness 设计]] — extends (长时运行场景的深化框架)
