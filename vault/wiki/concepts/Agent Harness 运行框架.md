---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["Agent工程", "长时任务", "架构模式", "可靠性"]
aliases: ["Agent Harness", "Agent 运行框架", "Harness 设计", "Long-running Agent Harness"]
relates_to:
  - target: '[[AI Agent 架构模式]]'
    type: part_of
  - target: '[[Agent 架构与设计原则]]'
    type: relates_to
  - target: '[[外化工作记忆]]'
    type: implements
  - target: '[[错误复合]]'
    type: prevents
  - target: '[[上下文窗口]]'
    type: relates_to
supersedes: null
---

# Agent Harness 运行框架

## 概述
Agent Harness 运行框架是包裹 LLM Agent 的工程层，负责状态持久化、错误恢复、检查点管理和资源控制，使 Agent 能够跨多个上下文窗口连贯地执行长时任务。

## 关键内容

1. **核心职责**：
   - **状态持久化**：跨会话保存 Agent 进度，避免因上下文窗口限制导致早期决策被遗忘
   - **错误恢复**：在工具调用或 API 错误时优雅处理，而非直接失败
   - **检查点管理**：周期性保存可验证状态，支持从中间点恢复
   - **监控追踪**：记录 Agent 行为模式，便于调试和诊断
   - **资源管理**：控制 token 消耗和 API 调用频率

2. **与 Agent 能力的互补关系**：
   - 优秀的 Harness 不是弥补 Agent 能力不足，而是**释放** Agent 能力
   - Agent 不需要追踪自己的状态（Harness 负责）
   - Agent 可以专注于当前步骤的推理，而非全局管理
   - Agent 出错时 Harness 提供缓冲，而非直接失败

3. **长时任务的核心挑战**：
   - 任务执行时间往往超过单个上下文窗口所能承载的对话历史
   - 代码库迁移等任务可能持续数小时
   - 上下文窗口逼近限制后，Agent 可能重复已完成工作或忘记重要约束
   - 单步错误在多步迭代中积累放大，传统"重启"策略成本极高

4. **与分布式系统的类比**：
   - Harness 设计与 [[Saga 模式]] 高度相似
   - 将长事务分解为可补偿的短步骤
   - 每步成功后记录进度
   - 失败时从最近检查点回滚或继续

5. **设计原则**：
   - 采用 [[初始化-编码循环模式]] 分解长任务
   - 使用 [[外化进度追踪]] 作为外部记忆
   - 实施 [[检查点策略]] 基于可验证状态而非自我报告
   - 防止 Agent 过早声明完成

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/09_effective_harnesses.md]] — Effective harnesses for long-running agents

## 相关
- [[AI Agent 架构模式]] — part_of（Harness 是 Agent 架构模式的一种具体实现）
- [[Agent 架构与设计原则]] — relates_to（Harness 设计遵循的架构原则）
- [[外化工作记忆]] — implements（Harness 实现了外化工作记忆的机制）
- [[错误复合]] — prevents（Harness 防止错误在多步迭代中积累放大）
- [[上下文窗口]] — relates_to（Harness 解决上下文窗口边界问题）
