---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [architecture-pattern, agent-system, context-management, AI工程]
aliases: ["Compressor wU2", "Context Compressor"]
relates_to:
  - target: "[[Claude Code]]"
    type: component_of
  - target: "[[Context Management]]"
    type: implements
  - target: "[[Context Window]]"
    type: manages
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Compressor wU2

## 概述
Compressor wU2 是 [[Claude Code]] 中的[[Context Management|上下文管理]]器，用于管理模型的[[上下文窗口]]，当上下文达到 92% 阈值时触发压缩操作。

## 关键内容
1. **触发机制**：当上下文使用率达到 92% 时自动触发压缩操作，确保模型有足够的上下文空间继续工作。

2. **功能目的**：防止[[上下文窗口]]溢出，保持重要信息的同时移除冗余或不太重要的信息，维持代理运行的连续性。

3. **在 [[Claude Code]] 中的作用**：作为[[Context Management|上下文管理]]器，在 [[TAOR Loop]] 中发挥作用，确保代理在长时间运行的任务中不会因上下文耗尽而中断。

4. **设计考虑**：平衡信息保存和上下文空间管理的需求，保留对当前任务最重要的上下文信息。

## 来源
- [[01_system_overview.md]] — Claude Code 系统总览

## 相关
- [[Claude Code]] — component_of
- [[Context Management]] — implements
- [[Context Window]] — manages

## 指令