---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI, 工具, 方法论, AI工程]
aliases:
  - "TodoWrite"
  - "TodoWrite Tool"
  - "待办事项工具"
  - "待办清单"
relates_to:
  - target: "[[Claude-Code]]"
    type: implemented_by
    confidence: 0.9
  - target: "[[Task-Tool]]"
    type: supersedes
    confidence: 0.95
  - target: "[[渐进式披露 -Progressive-Disclosure]]"
    type: uses
    confidence: 0.8
  - target: "[[Agent-Skills]]"
    type: related_to
    confidence: 0.8
  - target: "[[AskUserQuestion-Tool]]"
    type: compares_to
    confidence: 0.75
supersedes: null
---

# TodoWrite Tool

## 概述

[[Claude Code]] 早期推出的任务跟踪工具，用于让模型在会话开始时写下待办清单并在工作过程中逐一勾选。随着模型能力提升，发现其局限性：使 Claude 认为必须严格遵守清单而无法灵活调整，最终被 [[Task-Tool]] 取代。是理解 Agent 工具演进的重要案例。

## 关键内容

### 设计初衷

**保持模型轨道（Keep Model on Track）**：
- [[Claude Code]] 发布初期，发现模型经常忘记需要完成的任务
- TodoWrite 允许在会话开始时写下待办清单
- 工作过程中可以勾选已完成的项目
- 通过 UI 向用户展示当前进度

### 工作机制

**基本流程**：
1. 会话开始 → Claude 写下待办清单
2. 执行任务 → 逐一勾选完成的项目
3. 用户可见 → 清单显示在 UI 中
4. 系统提醒 → 每 5 轮插入提醒，让 Claude 记住目标

### 发现的问题

**局限性 1：僵化的清单思维**
- 当收到待办清单提醒时，Claude 认为自己必须严格遵守清单
- 无法在意识到需要调整方向时修改清单
- 限制了模型的灵活性和适应性

**局限性 2：子代理协作困难**
- 随着 Opus 4.5 等更强模型的推出，子代理（subagents）使用能力提升
- 但子代理之间如何在共享待办清单上协作成为问题
- TodoWrite 的单一清单模型不支持多 Agent 协调

**局限性 3：能力错配**
- 随着模型能力提升，旧工具的约束变得明显
- TodoWrite 设计时的假设（模型需要外部提醒）不再适用
- 工具从"帮助"变成了"约束"

### 演进：被 Task Tool 取代

**替代方案**：[[Task-Tool]]

**改进点**：
| 维度 | TodoWrite | [[Task-Tool|Task Tool]] |
|------|-----------|-----------|
| **核心目标** | 保持模型轨道 | Agent 间协调 |
| **结构** | 单一清单 | 任务网络 |
| **依赖关系** | 不支持 | 支持任务依赖 |
| **跨 Agent** | 困难 | 原生支持 |
| **可修改性** | 有限 | 可修改和删除 |

**设计哲学转变**：
- TodoWrite：聚焦于"让模型不忘记"
- [[Task-Tool|Task Tool]]：聚焦于"Agent 间沟通"
- 从"约束模型"到"赋能协作"

### 设计启示

**工具演进的必要性**：
- 随着模型能力提升，旧工具可能变成约束
- 需要不断重新审视关于"需要什么工具"的假设
- 坚持使用能力特征相似的模型组合有助于工具稳定性

**能力错配检测**：
- 当工具使用频率下降或效果变差时，可能是模型能力已超越工具
- 评估框架（如 [[Agent-Skills]] 的 Evals）可帮助判断是否需要调整工具

**从简单到复杂**：
- TodoWrite：简单的清单模型
- [[Task-Tool|Task Tool]]：复杂的任务网络和依赖管理
- 演进反映了模型处理复杂性的能力提升

### 在工具历史中的位置

**时间线**：
1. [[Claude Code]] 发布 → TodoWrite 作为核心工具
2. 发现局限性 → 添加系统提醒（每 5 轮）
3. 模型能力提升 → Opus 4.5 子代理使用增加
4. 认识到局限 → 开发 [[Task-Tool|Task Tool]]
5. 最终取代 → TodoWrite 被 [[Task-Tool|Task Tool]] 替代

**相关工具**：
- [[AskUserQuestion-Tool]]：同时期的提问工具优化
- [[ExitPlanTool]]：计划生成工具，可能与 TodoWrite 协同
- [[Task-Tool]]：直接替代者

## 来源

- [[raw/articles/ai-engineering/claude-blog/Seeing like an agent_ how we design tools in Claude Code.md]] — TodoWrite 局限性和被 Task Tool 取代的详细分析

## 相关

- [[Task-Tool]] — 直接替代者（supersedes）
- [[Claude-Code]] — 所属项目
- [[渐进式披露-Progressive-Disclosure]] — 工具设计方法论
- [[Agent-Skills]] — 工具能力评估框架
- [[TodoWrite-Tool]] — 与 AskUserQuestion 同时期工具
