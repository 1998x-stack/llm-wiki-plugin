---
type: entity
entity_type: project
title: Claude Opus 4.6
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 3
tags: [AI, 工具, LLM能力]
aliases:
- claude-opus-4-6
- Claude Opus 4.6
relates_to:
- target: '[[上下文压缩]]'
  type: implements
  confidence: 0.95
- target: '[[Context-Engineering]]'
  type: related_to
  confidence: 0.85
- target: '[[上下文窗口]]'
  type: implements
  confidence: 0.95
- target: '[[交错式思考]]'
  type: implements
  confidence: 0.9
- target: '[[Programmatic-Tool-Calling-PTC]]'
  type: implements
  confidence: 0.95
supersedes: null
---

# Claude Opus 4.6

## 概述

Claude Opus 4.6 是 Anthropic 发布的 Claude Opus 系列模型，是 Anthropic 能力最强的模型之一，支持 [[上下文压缩]] 等高级上下文管理功能。

## 关键内容

### 基本信息

- **模型 ID**：`claude-opus-4-6`
- **系列**：Claude Opus
- **版本**：4.6
- **[[上下文窗口]]**：1M tokens
- **发布方**：Anthropic

### 支持的功能

- [[上下文压缩]]（[[上下文压缩|Server-side Compaction]]，beta 阶段）
- [[上下文感知]]（[[上下文感知|Context Awareness]]）
- [[交错式思考]]（[[交错式思考|Interleaved Thinking]]）
- [[Programmatic-Tool-Calling-PTC|程序化工具调用 (PTC)]] — 动态构造工具调用
- 符合 [[零数据保留]] ([[零数据保留|ZDR]]) 条件
- [[提示词缓存]]（[[提示词缓存|Prompt Caching]]）

### 在知识库中的引用

[[Context-Engineering]] 和 [[Agent Harness模式]] 中多次提及 Opus 4.5 和 Opus 4.6 的能力对比：
- Opus 4.5 时代：需要 Sprint 分解 + [[上下文重置]] 才能完成长时任务
- Opus 4.6 时代：模型能力提升，边界外移——部分 Harness 组件可被移除

这体现了 [[生成器-评估器架构]] 中的核心观点：评估器的价值是条件性的，取决于任务相对于模型当前能力的位置。

### 压缩功能中的角色

在 [[上下文压缩]] 中，Opus 4.6 既是被压缩对话的执行模型，也是生成压缩摘要的模型（当前限制：无法使用更便宜的模型生成摘要）。

## 来源

- [[raw/articles/ai-engineering/anthropic-developer/Compaction.md]] — Anthropic 官方文档
- [[raw/articles/ai-engineering/anthropic-developer/Context windows.md]] — 上下文窗口文档
- [[Context-Engineering]] — 模型能力对比
- [[Agent Harness模式]] — Harness 复杂度与模型能力关系

## 相关

- [[上下文压缩]] — implements（支持压缩功能）
- [[上下文窗口]] — implements（1M tokens 上下文窗口）
- [[交错式思考]] — implements（支持交错式思考）
- [[Programmatic-Tool-Calling-PTC]] — implements（支持程序化工具调用）
- [[Context-Engineering]] — related_to（模型能力影响上下文管理策略）
- [[Agent Harness 模式]] — related_to（模型能力提升驱动 Harness 简化）
- [[Claude-Sonnet-4-6]] — compares_to（同代模型）
- [[Claude-Mythos-Preview]] — compares_to（同代支持压缩的模型）
- [[Lance-Martin]] — 技术分析者（related_to）
- [[Lance-Martin]] — 技术分析者（related_to）
