---
type: concept
status: active
confidence: 0.97
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 3
tags: [ai-engineering, agent-design, architecture]
aliases: [Agent Architecture, AI Agent Design Patterns, Agent 架构]
relates_to:
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[上下文工程]]"
    type: extends
  - target: "[[并行 Agent 开发]]"
    type: relates_to
  - target: "[[可扩展的受管理 Agent]]"
    type: extends
  - target: "[[并行工具调用]]"
    type: has
  - target: "[[工具选择控制]]"
    type: has
  - target: "[[工具错误处理]]"
    type: has
  - target: "[[工具组合模式]]"
    type: has
  - target: "[[工具结果缓存]]"
    type: has
supersedes: null
---

# Agent 架构与设计原则

## 概述
Agent 架构是 AI 系统设计的核心方法论，涵盖从简单可组合模式到多层受管理 Agent 的完整谱系，强调简单优于复杂的工程哲学。

## 关键内容

1. **五种核心 Agent 模式**：Anthropic 提出 Agent 分类学，最成功的使用场景采用简单可组合模式，而非过度复杂的架构设计。这一理念贯穿多篇文章，强调"do the simplest thing that works"。

2. **可扩展的受管理 Agent**：2026 年提出的多层 Agent 架构，解耦"大脑"与"双手"，实现成本优化和规模化部署。通过分层设计平衡智能水平与资源消耗。

3. **多 Agent 系统实践**：从原型到生产的工程路径，实现 90.2% 性能提升。提出 8 条 Prompt 工程原则，强调并行 Agent 编程中的接口规范挑战，如 C 编译器构建案例所示。

4. **简单优于复杂原则**：多篇文章反复验证的核心理念——最小高信噪比 token 集合、可组合模式优先、避免过度工程化。这是 Anthropic 工程哲学的基石。

5. **长时运行 Harness 设计**：针对应用开发场景，Anthropic 提出 [[Harness 设计]] 框架，包含 [[特性追踪器]]、[[上下文传递协议]]、[[智能检查点触发]]、[[三级自主权模型]]、[[持续验证循环]] 和 [[技术债务追踪]]。Harness 本质上是"为 AI Agent 定制的 CI/CD 系统"，管理即时/短期/长期三种状态形态。

6. **可扩展的受管理 Agent 架构**：2026 年提出的三层分层设计（战略层/战术层/执行层），将推理与执行解耦并独立扩展，通过不同规模模型匹配任务复杂度，实现成本降低 60-80% 的同时保持关键推理质量。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — Agent 架构与设计原则章节
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/13_building_c_compiler.md]] — 并行 Agent 架构案例
- [[14_harness_design_long_running.md]] — 长时运行应用开发场景的 Harness 设计

## 相关
- [[Anthropic]] — part_of
- [[Claude Code]] — uses
- [[上下文工程]] — extends
- [[多 Agent 系统]] — relates_to
- [[ACI 设计原则]] — relates_to
- [[并行 Agent 开发]] — relates_to
- [[Harness 设计]] — extends (长时运行场景的具体化)
- [[可扩展的受管理 Agent]] — extends (分层架构模式)
- [[并行工具调用]] — has (高级工具使用能力)
- [[工具选择控制]] — has (工具行为控制)
- [[工具错误处理]] — has (可靠性保障)
- [[工具组合模式]] — has (工具协同架构)
- [[工具结果缓存]] — has (性能优化)
