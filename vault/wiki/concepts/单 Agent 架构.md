---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Agent架构, 单Agent, 简单性, Anthropic, AI工程]
aliases:
- 单 Agent 架构
- Single Agent Architecture
- 单 Agent 模式
relates_to:
- target: '[[Agent 架构与设计原则]]'
  type: part_of
  confidence: 0.95
- target: '[[多 Agent 系统]]'
  type: compares_to
  confidence: 0.9
- target: '[[Claude 3.5 Sonnet]]'
  type: implements
  confidence: 0.85
supersedes: null
---

# 单 Agent 架构

## 概述
单 [[Agent 架构与设计原则|Agent 架构]]是一种 AI Agent 设计模式，使用单一 Agent 实例配合精心设计的工具集完成复杂任务，而非依赖多 Agent 编排，体现了"简单优于复杂"的工程哲学。

## 关键内容

1. **[[SWE-bench]] 验证**：[[Claude 3.5 Sonnet]] 的 [[SWE-bench]] Agent 采用相对简单的单 [[Agent 架构与设计原则|Agent 架构]]——[[Claude 3.5 Sonnet]] 作为核心推理引擎，一套精心设计的工具集（文件读写、命令执行、搜索等），无复杂的多 Agent 编排。

2. **SOTA 成绩证明**：单 Agent 配合优质工具就能达到 [[SWE-bench]] SOTA（49%），这个设计选择体现了 [[Anthropic]] 一贯的"简单优于复杂"哲学——复杂的多 [[Agent 架构与设计原则|Agent 架构]]并未带来额外收益。

3. **与[[多 Agent 系统]]的对比**：
   - 单 Agent：简单、低延迟、上下文一致、调试容易
   - 多 Agent：复杂、高延迟、需要协调机制、调试困难
   - 关键结论：在 [[SWE-bench]] 这类任务上，单 Agent + 优质工具 > 复杂多 Agent 编排

4. **适用场景**：
   - 任务可在单个 Agent 的[[上下文窗口]]内完成
   - 工具集设计良好，能覆盖任务所需的所有操作
   - 延迟敏感，需要快速响应

5. **设计要点**：
   - 核心推理引擎选择强模型（如 [[Claude 3.5 Sonnet]]）
   - 工具集深度优化（Poka-Yoke 设计）
   - 引入 [[Think 工具]] 增强中间推理能力

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — Agent 架构工程决策分析

## 相关

- [[Agent 架构与设计原则]] — part_of（单 Agent 是 Agent 架构的一种模式）
- [[多 Agent 系统]] — compares_to（单 Agent vs 多 Agent 的架构选择）
- [[Claude 3.5 Sonnet]] — implements（Claude 3.5 Sonnet 的 SWE-bench Agent 采用单 Agent 架构）
