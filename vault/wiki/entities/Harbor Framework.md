---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [框架, 评测, 容器化, Agent, AI工程]
aliases: ["Harbor Framework"]
relates_to:
  - target: "[[评测驱动开发]]"
    type: uses
supersedes: null
---

# Harbor Framework

## 概述
Harbor Framework 是容器化的 [[Agent 评测体系|Agent 评测框架]]，用于标准化和模块化 [[评测驱动开发|Agent 评测]]流程。

## 关键内容

1. **核心特性**：
   - 容器化设计：每个评测任务在隔离环境中运行
   - 模块化架构：支持灵活组合不同的[[评分器设计|评分器]]和评测组件
   - 标准化接口：统一的评测任务定义和执行框架

2. **在评测体系中的位置**：
   - 提供 [[Evaluation Harness]] 的开源实现
   - 解决评测环境隔离性问题（避免跨 Trial 共享状态）
   - 支持多类型 Agent 的评测需求

3. **工程价值**：
   - 降低[[Evaluation Harness|评测基础设施]]的搭建门槛
   - 提供可复用的评测组件库
   - 支持评测的持续集成和自动化

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 参考与扩展阅读

## 相关
- [[评测驱动开发]] — uses（Harbor Framework 是评测基础设施的开源实现）
