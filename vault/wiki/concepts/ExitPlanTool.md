---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI, 工具, 方法论, AI工程]
aliases:
  - "ExitPlanTool"
  - "Exit Plan Tool"
  - "退出计划工具"
relates_to:
  - target: "[[Claude-Code]]"
    type: implemented_by
    confidence: 0.9
  - target: "[[AskUserQuestion-Tool]]"
    type: extends
    confidence: 0.85
    note: "尝试扩展失败后独立设计"
  - target: "[[渐进式披露 -Progressive-Disclosure]]"
    type: uses
    confidence: 0.8
  - target: "[[提示词缓存]]"
    type: related_to
    confidence: 0.7
supersedes: null
---

# ExitPlanTool

## 概述

[[Claude Code]] 早期工具之一，用于生成执行计划。在 [[AskUserQuestion-Tool|AskUserQuestion Tool]] 的设计演进中曾被尝试扩展以支持提问功能，但因设计冲突而放弃。是理解 [[Claude Code]] 工具演进历史的重要案例。

## 关键内容

### 核心功能

**计划生成**：
- 输出任务执行的详细计划
- 可能包含步骤分解、依赖关系、资源需求等信息
- 作为 [[Claude Code]] 工作流的起点

### 设计演进中的角色

**尝试扩展：添加提问参数**

在开发 [[AskUserQuestion-Tool]] 时，曾尝试修改 ExitPlanTool：

**方案**：
- 添加参数：在计划旁边附带一组问题数组
- 优点：最容易实现的修复方式

**失败原因**：
1. **职责冲突**：同时要求生成计划和关于计划的问题，导致 Claude 困惑
2. **潜在矛盾**：用户的回答可能与计划内容相冲突
3. **多次调用需求**：可能需要调用 ExitPlanTool 两次（一次生成计划，一次根据回答调整）

**结论**：此路不通，需要重新设计独立的提问工具

### 设计启示

**单一职责原则**：
- 工具应该专注于单一功能
- 混合职责（计划 + 提问）会导致模型困惑
- 分离关注点是更好的设计选择

**工具设计难度**：
- 即使看似简单的扩展也可能失败
- 需要"像智能体一样观察"才能理解设计约束
- 实验和迭代是必要的

### 在工具演进中的位置

**时间线**：
1. ExitPlanTool 作为早期工具存在
2. 尝试扩展以支持提问 → 失败
3. 尝试更改输出格式 → 失败
4. 最终创建独立的 [[AskUserQuestion-Tool|AskUserQuestion Tool]]

**与后续工具的关系**：
- [[AskUserQuestion-Tool|AskUserQuestion Tool]]：独立的提问工具，解决了 ExitPlanTool 无法处理的需求
- [[TodoWrite-Tool|TodoWrite]]/Task：任务跟踪工具，可能与 ExitPlanTool 协同使用

### 相关设计文档

关于 ExitPlanTool 的更多设计原因，可参考 [[Anthropic]] 关于[[提示词缓存]]的文章（[[trq212/status/2024574133011673516]]）。

## 来源

- [[raw/articles/ai-engineering/claude-blog/Seeing like an agent_ how we design tools in Claude Code.md]] — 提及 ExitPlanTool 在 AskUserQuestion 演进中的尝试

## 相关

- [[AskUserQuestion-Tool]] — 演进后续（独立提问工具）
- [[Claude-Code]] — 所属项目
- [[渐进式披露-Progressive-Disclosure]] — 工具设计方法论
- [[提示词缓存]] — 相关设计文档来源
