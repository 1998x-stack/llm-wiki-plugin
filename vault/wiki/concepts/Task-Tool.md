---
type: concept
status: active
confidence: 0.92
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI, 工具, 方法论, AI工程]
aliases:
  - "Task Tool"
  - "任务工具"
  - "Agent 任务协调"
relates_to:
  - target: "[[Claude-Code]]"
    type: implemented_by
    confidence: 0.95
  - target: "[[TodoWrite-Tool]]"
    type: supersedes
    confidence: 0.95
  - target: "[[渐进式披露 -Progressive-Disclosure]]"
    type: uses
    confidence: 0.9
  - target: "[[Agent-Skills]]"
    type: related_to
    confidence: 0.85
  - target: "[[AskUserQuestion-Tool]]"
    type: related_to
    confidence: 0.8
  - target: "[[脑手分离架构]]"
    type: related_to
    confidence: 0.75
supersedes:
  - target: "[[TodoWrite-Tool]]"
    type: supersedes
    confidence: 0.95
---

# Task Tool

## 概述

Claude Code 推出的任务协调工具，用于替代 [[TodoWrite-Tool]]。与 TodoWrite 专注于"保持模型轨道"不同，Task Tool 聚焦于帮助 Agent 之间进行沟通，支持任务依赖、跨子代理共享更新、可修改和删除。是"像智能体一样观察"设计哲学的典型应用，反映了模型能力提升后工具演进的必然性。

## 关键内容

### 设计动机

**TodoWrite 的局限性**：
- 僵化的清单思维：Claude 认为必须严格遵守清单，无法灵活调整
- 子代理协作困难：不支持多个子代理在共享清单上协作
- 能力错配：随着模型能力提升，旧工具从"帮助"变成"约束"

**新需求**：
- Opus 4.5 等更强模型的子代理使用能力提升
- 需要支持多 Agent 协调的机制
- 需要更灵活的任务管理方式

### 核心特性

**Agent 间沟通**：
- 核心目标：帮助 Agent 之间进行沟通，而非单纯跟踪进度
- 任务作为沟通载体，而非约束清单
- 支持自然的任务演进和调整

**依赖关系管理**：
- 支持任务间的依赖关系声明
- 自动识别前置任务和后续任务
- 优化任务执行顺序

**跨子代理共享**：
- 多个子代理可以访问和更新共享任务池
- 支持任务状态同步
- 避免信息孤岛

**灵活修改**：
- 模型可以修改任务内容
- 支持删除不再相关的任务
- 适应动态变化的需求

### vs TodoWrite

| 维度 | TodoWrite | Task Tool |
|------|-----------|-----------|
| **核心目标** | 保持模型轨道 | Agent 间协调 |
| **设计理念** | 约束模型行为 | 赋能 Agent 协作 |
| **结构** | 单一清单列表 | 任务网络图 |
| **依赖关系** | ❌ 不支持 | ✅ 原生支持 |
| **跨 Agent** | ❌ 困难 | ✅ 原生支持 |
| **可修改性** | ⚠️ 有限 | ✅ 可修改和删除 |
| **适用模型** | 早期模型（需提醒） | 现代模型（Opus 4.5+） |

### 演进历程

**替代 TodoWrite**：
- 识别到 TodoWrite 的局限性后，没有选择修补，而是重新设计
- Task Tool 从零开始设计，专注于 Agent 协调需求
- 反映了"不断重新审视假设"的设计哲学

**与 AskUserQuestion 的协同**：
- AskUserQuestion：在计划阶段收集用户需求
- Task Tool：在执行阶段协调 Agent 工作
- 两者可能在同一工作流中协同使用

### 设计哲学启示

**工具演进原则**：
1. **能力匹配**：工具设计需要契合模型当前能力水平
2. **持续审视**：随着模型能力提升，需要重新审视旧工具
3. **勇于替代**：当旧工具变成约束时，应该设计新工具替代而非修补

**"像智能体一样观察"**：
- 站在模型角度思考：需要什么样的任务管理工具？
- 实验频繁、阅读输出、尝试新方法
- 最重要的：试着像智能体一样思考

**小模型集合策略**：
- 坚持使用少数几个能力特征相似的模型
- 避免工具需要适配过多不同的能力水平
- 降低工具设计的复杂度

### 使用场景

**多 Agent 协作**：
- 主代理分解任务 → 创建子任务
- 子代理执行任务 → 更新状态
- 主代理汇总结果 → 标记完成

**复杂项目管理**：
- 声明任务依赖 → 自动排序
- 动态调整计划 → 修改任务
- 识别关键路径 → 优化执行

**长时任务跟踪**：
- 跨会话持久化
- 支持暂停和恢复
- 上下文传递

### 在 Claude Code 生态中的位置

**工具集合**：
- Claude Code 目前拥有约 20 个工具
- Task Tool 是核心协调工具之一
- 与 [[AskUserQuestion-Tool]]、[[ExitPlanTool]] 等协同工作

**与 [[Agent Skills]] 的关系**：
- Task Tool 是内置工具
- [[Agent-Skills]] 可以扩展和自定义 Task Tool 的使用方式
- 渐进式披露机制允许 [[Agent Skills|Skills]] 引入 Task 相关的最佳实践

## 来源

- [[raw/articles/ai-engineering/claude-blog/Seeing like an agent_ how we design tools in Claude Code.md]] — Task Tool 设计动机、与 TodoWrite 对比、演进原因

## 相关

- [[TodoWrite-Tool]] — 被此工具取代（supersedes）
- [[Claude-Code]] — 所属项目
- [[AskUserQuestion-Tool]] — 同时期设计的提问工具
- [[渐进式披露-Progressive-Disclosure]] — 设计方法论
- [[Agent-Skills]] — 可扩展 Task Tool 使用方式
- [[脑手分离架构]] — Task Tool 可能用于协调 Brain/Hands 角色
