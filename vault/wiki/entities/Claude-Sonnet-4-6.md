---
type: entity
entity_type: project
title: Claude Sonnet 4.6
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 3
tags: [AI, 工具, LLM能力]
aliases:
- claude-sonnet-4-6
- Claude Sonnet 4.6
relates_to:
- target: '[[上下文压缩]]'
  type: implements
  confidence: 0.95
- target: '[[Claude-Opus-4-6]]'
  type: compares_to
  confidence: 0.9
- target: '[[上下文窗口]]'
  type: implements
  confidence: 0.95
- target: '[[上下文感知]]'
  type: implements
  confidence: 0.9
- target: '[[交错式思考]]'
  type: implements
  confidence: 0.9
- target: '[[Programmatic-Tool-Calling-PTC]]'
  type: implements
  confidence: 0.95
supersedes: null
---

# Claude Sonnet 4.6

## 概述

[[Claude-Sonnet-4|Claude Sonnet 4]].6 是 [[Anthropic]] 发布的 [[Claude_Code|Claude]] Sonnet 系列模型，在性能与成本之间取得平衡，支持 [[上下文压缩]] 等高级[[Context Management|上下文管理]]功能。

## 关键内容

### 基本信息

- **模型 ID**：`claude-sonnet-4-6`
- **系列**：[[Claude_Code|Claude]] Sonnet
- **版本**：4.6
- **[[上下文窗口]]**：1M tokens
- **发布方**：[[Anthropic]]

### 支持的功能

- [[上下文压缩]]（[[上下文压缩|Server-side Compaction]]，beta 阶段）
- [[上下文感知]]（[[上下文感知|Context Awareness]]）
- [[交错式思考]]（[[交错式思考|Interleaved Thinking]]）
- 符合 [[零数据保留]] (ZDR) 条件
- [[提示词缓存]]（[[提示词缓存|Prompt Caching]]）

### 与 Opus 4.6 的对比

[[Claude-Sonnet-4|Sonnet 4]].6 与 [[Claude-Opus-4-6]] 同为 4.6 代模型，共享压缩功能支持。Sonnet 系列通常在推理成本上低于 Opus，适合对成本敏感但需要长时对话能力的场景。

### 压缩功能中的角色

与 [[Claude_Opus_4.6|Opus 4.6]] 相同，[[Claude-Sonnet-4|Sonnet 4]].6 在压缩中既是对话执行模型，也是摘要生成模型（当前限制：无法指定更便宜的模型生成摘要）。

## 来源

- [[raw/articles/ai-engineering/anthropic-developer/Compaction.md]] — Anthropic 官方文档
- [[raw/articles/ai-engineering/anthropic-developer/Context windows.md]] — 上下文窗口文档
- [[raw/articles/ai-engineering/claude-blog/Give Claude a computerGive Claude a computer 给 Claude 一台电脑.md]] — Programmatic Tool Calling 能力

## 相关

- [[上下文压缩]] — implements（支持压缩功能）
- [[上下文窗口]] — implements（1M tokens 上下文窗口）
- [[上下文感知]] — implements（支持上下文感知）
- [[交错式思考]] — implements（支持交错式思考）
- [[Programmatic-Tool-Calling-PTC]] — implements（支持程序化工具调用）
- [[Claude-Opus-4-6]] — compares_to（同代模型，性能更高）
- [[Claude-Mythos-Preview]] — compares_to（同代支持压缩的模型）
- [[Lance-Martin]] — 技术分析者（related_to）
