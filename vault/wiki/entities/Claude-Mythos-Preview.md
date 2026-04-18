---
type: entity
entity_type: project
title: Claude Mythos Preview
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 2
tags: [AI, 工具, LLM能力]
aliases:
- claude-mythos-preview
- Claude Mythos
relates_to:
- target: '[[上下文压缩]]'
  type: implements
  confidence: 0.95
- target: '[[上下文窗口]]'
  type: implements
  confidence: 0.95
- target: '[[交错式思考]]'
  type: implements
  confidence: 0.9
supersedes: null
---

# Claude Mythos Preview

## 概述

Claude Mythos Preview 是 [[Anthropic]] 发布的预览版 Claude 模型，是支持 [[上下文压缩]] 功能的模型之一。该模型通过 [[Anthropic]] 官方 glasswing 页面发布。

## 关键内容

### 基本信息

- **模型 ID**：`claude-mythos-preview`
- **状态**：Preview（预览版）
- **[[上下文窗口]]**：1M tokens
- **发布方**：[[Anthropic]]
- **发布页面**：https://anthropic.com/glasswing

### 支持的功能

- [[上下文压缩]]（[[上下文压缩|Server-side Compaction]]）
- [[上下文感知]]（[[上下文感知|Context Awareness]]）
- [[交错式思考]]（[[交错式思考|Interleaved Thinking]]）
- 符合 [[零数据保留]] (ZDR) 条件

### 模型系列定位

Mythos 作为预览版模型，通常用于测试 [[Anthropic]] 的最新功能和 API 特性。与 [[Claude-Opus-4-6]] 和 [[Claude-Sonnet-4-6]] 同为支持压缩功能的模型家族成员。

## 来源

- [[raw/articles/ai-engineering/anthropic-developer/Compaction.md]] — Anthropic 官方文档
- [[raw/articles/ai-engineering/anthropic-developer/Context windows.md]] — 上下文窗口文档

## 相关

- [[上下文压缩]] — implements（支持压缩功能）
- [[上下文窗口]] — implements（1M tokens 上下文窗口）
- [[交错式思考]] — implements（支持交错式思考）
- [[Claude-Opus-4-6]] — compares_to（同代支持压缩的模型）
- [[Claude-Sonnet-4-6]] — compares_to（同代支持压缩的模型）
