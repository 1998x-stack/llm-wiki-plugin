---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["分布式系统", "架构模式", "长事务", "Agent工程"]
aliases: ["Saga Pattern", "Saga 事务模式", "长事务分解"]
relates_to:
  - target: '[[Agent Harness 运行框架]]'
    type: compares_to
  - target: '[[检查点策略]]'
    type: relates_to
  - target: '[[AI Agent 架构模式]]'
    type: relates_to
supersedes: null
---

# Saga 模式

## 概述
Saga 模式是分布式系统中处理长事务的设计模式，将长事务分解为一系列可补偿的短步骤，每步成功后记录进度，失败时从最近检查点回滚或继续，与 Agent Harness 设计高度相似。

## 关键内容

1. **核心思想**：
   - 将长事务分解为多个可独立执行的短步骤
   - 每个步骤完成后记录进度（检查点）
   - 失败时从最近的检查点回滚或继续执行
   - 每个步骤都有对应的补偿操作

2. **与 Agent Harness 的类比**：
   - Agent Harness 设计与 Saga 模式高度相似
   - 长时 Agent 任务 ≈ 分布式长事务
   - Agent 的每个执行步骤 ≈ Saga 中的本地事务
   - 检查点 ≈ Saga 的补偿点
   - 错误恢复 ≈ Saga 的补偿执行

3. **设计启示**：
   - 这种类比为 Harness 工程师提供了丰富的已知解决方案库
   - 可以从分布式系统领域借鉴成熟的错误处理和恢复策略
   - Saga 模式的补偿机制可应用于 Agent 任务的回滚设计

4. **在 Agent 工程中的应用**：
   - 将长时任务分解为可验证的短步骤
   - 每步成功后更新进度文件（如 claude-progress.txt）
   - 失败时从最近检查点恢复，而非从头开始
   - 设计补偿操作来撤销已完成的步骤

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/09_effective_harnesses.md]] — Effective harnesses for long-running agents

## 相关
- [[Agent Harness 运行框架]] — compares_to（Harness 设计与 Saga 模式高度相似）
- [[检查点策略]] — relates_to（Saga 使用检查点进行状态恢复）
- [[AI Agent 架构模式]] — relates_to（Saga 模式可应用于 Agent 架构设计）
