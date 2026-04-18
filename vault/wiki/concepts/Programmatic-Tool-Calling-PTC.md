---
type: concept
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI, 工具, 方法论, AI工程]
aliases:
  - "Programmatic Tool Calling"
  - "PTC"
  - "程序化工具调用"
relates_to: []
supersedes: null
---

# Programmatic Tool Calling (PTC)

## 概述

Programmatic Tool [[天职|Calling]]（PTC，程序化工具调用）是 [[Claude-Opus-4-6|Claude Opus 4.6]] 和 [[Claude-Sonnet-4|Sonnet 4]].6 模型中引入的新能力。允许通过编程方式动态调用工具，而非仅依赖预定义的工具描述。这一能力使得工具调用更加灵活，支持运行时决策和动态参数构造。

## 关键内容

### 核心特性

**动态工具调用**：
- 不依赖静态工具描述
- 支持运行时根据上下文动态构造工具调用
- 允许条件性工具选择和参数生成

**与静态工具调用的对比**：

| 维度 | 静态工具调用 | 程序化工具调用 (PTC) |
|------|-------------|---------------------|
| **定义时机** | 系统提示中预定义 | 运行时动态构造 |
| **灵活性** | 固定工具和参数 | 可动态调整 |
| **适用场景** | 稳定、可预测的工作流 | 复杂、条件性任务 |
| **维护成本** | 需要手动更新工具定义 | 代码即定义 |

### 应用场景

**文件编辑的 stale 检查**：
- 文件编辑工具可以运行 staleness check
- 验证文件自模型最后读取后是否发生变化
- 避免基于过期上下文进行修改
- 提升编辑操作的可靠性和原子性

**动态工具选择**：
- 根据任务复杂度选择不同工具
- 条件性工具链编排
- 自适应工具参数构造

### 在 Claude 4.6 中的实现

**支持模型**：
- [[Claude-Opus-4-6]] — 完整支持 PTC
- [[Claude-Sonnet-4-6]] — 完整支持 PTC

**能力意义**：
- PTC 是 4.6 代模型的关键能力提升之一
- 与 [[上下文压缩]]、[[交错式思考]] 等能力协同
- 为复杂 Agent 工作流提供更灵活的工具调用机制

### 设计启示

**工具演进方向**：
- 从静态定义到动态编程
- 从预定义工具集到运行时工具构造
- 反映了模型处理复杂性的能力提升

**与渐进式披露的关系**：
- PTC 允许工具按需动态构造
- 符合"[[渐进式披露（Progressive Disclosure）|按需加载]]"的设计哲学
- 可能减少预定义工具数量，提升灵活性

### 在 AI 工程中的位置

**与 [[Agent Skills]] 的关系**：
- [[Agent Skills]]：通过 [[Agent Skills|SKILL.md]] 文件提供领域知识
- PTC：提供动态工具调用能力
- 可能协同：[[Agent Skills|Skills]] 可以包含 PTC 的最佳实践和模式

**与 [[Claude Code]] 的关系**：
- [[Claude Code]] 目前使用约 20 个预定义工具
- PTC 可能影响未来工具设计策略
- 需要持续实验验证 PTC 在实际工作流中的价值

## 来源

- [[raw/articles/ai-engineering/claude-blog/Give Claude a computerGive Claude a computer 给 Claude 一台电脑.md]] — Lance Martin 关于 PTC 的 X 文章

## 相关

- [[Claude-Opus-4-6]] — 支持模型（implements）
- [[Claude-Sonnet-4-6]] — 支持模型（implements）
- [[Agent-Skills]] — 相关能力扩展机制（compares_to）
- [[渐进式披露 -Progressive-Disclosure]] — 相关设计哲学（related_to）
- [[Claude-Code]] — 工具调用系统（part_of）
