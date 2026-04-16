---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags:
  - AI
  - 架构
  - 方法论
aliases:
  - "Wide Research"
  - "广泛研究"
  - "Manus Wide Research"
relates_to: []
supersedes: null
---

# Wide Research（广泛研究）

## 概述

Wide Research（广泛研究）是 [[Manus]] 推出的架构范式，通过并行启动多个专用子代理来解决[[上下文窗口]]限制导致的"编造阈值"问题。每个子代理都是功能齐全的 [[Manus]] 实例，独立处理研究子任务，最后汇总为综合结论。（[[Manus]] 于 2026 年被 [[Meta]] 收购）

## 关键内容

### 设计动机

**[[上下文窗口]]限制**：
- 当 AI 助手研究一长串项目时，会开始编造结果
- 这一常见困扰被称为"编造阈值"（fabrication threshold）
- 由 AI [[上下文窗口]]的固有局限性造成
- 即使是最大的[[上下文窗口]]也无法解决此问题

### 工作原理

**并行子代理架构**：
- 对于每个子任务，系统启动一个专用的子代理
- 关键特性：这些不是轻量级进程，而是功能齐全的 [[Manus]] 实例
- 每个子代理具有完整的[[上下文窗口]]和研究能力
- 子代理独立工作，最后汇总结果

### 核心优势

**解决编造阈值**：
- 每个子代理专注于有限范围的研究
- 避免单个[[上下文窗口]]承载过多信息
- 保持高召回精度，减少幻觉

**并行执行**：
- 多个子代理同时工作
- 缩短总体研究时间
- 提升吞吐量

**专业化**：
- 每个子代理可针对特定领域优化
- 积累领域特定上下文
- 提升研究质量

### 与 Subagents 的对比

| 维度 | Wide Research | Claude Code [[Subagents-in-Claude-Code|Subagents]] |
|------|--------------|---------------------|
| **目标** | 解决上下文限制 | 并行处理独立任务 |
| **范围** | 研究密集型任务 | 通用任务（研究/实施/验证） |
| **上下文** | 每个子代理完整上下文 | 独立[[上下文窗口]] |
| **汇总** | 综合研究结论 | 蒸馏后的发现 |

### 应用场景

**适合使用 Wide Research 的场景**：
- 大规模文献综述
- 竞争情报调研
- 技术栈评估
- 市场研究
- 需要阅读数十个来源的综合分析

**不适合的场景**：
- 单一来源的深度分析
- 需要跨来源实时协作的研究
- 顺序依赖的研究任务

### 在 Manus 生态系统中的位置

**[[Manus]] [[Context-Engineering|上下文工程]]六原则**之一：
- Wide Research 是核心架构范式
- 与 [[KV 缓存命中率]]优化协同
- 支持长时研究任务

## 来源

- [[raw/articles/ai-engineering/claude-blog/Wide Research：超越上下文窗口.md]] — Manus 官方博客

## 相关

- [[Manus]] — 提出者（part_of）
- [[Subagents-in-Claude-Code]] — 相关技术（compares_to）
- [[Context-Engineering]] — 上下文工程范式（part_of）
- [[上下文窗口]] — 解决的问题（caused）
- [[Agent-Teams-Pattern]] — 协调模式（implements）
