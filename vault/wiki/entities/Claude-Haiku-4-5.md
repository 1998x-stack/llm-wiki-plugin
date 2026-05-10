---
type: entity
entity_type: project
title: Claude Haiku 4.5
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 工具, LLM能力]
aliases:
- claude-haiku-4-5
- Claude Haiku 4.5
relates_to:
- target: '[[上下文窗口]]'
  type: implements
  confidence: 0.95
- target: '[[上下文感知]]'
  type: implements
  confidence: 0.9
supersedes: null
---

# Claude Haiku 4.5

## 概述

[[Claude_Code|Claude]] Haiku 4.5 是 [[Anthropic]] 发布的 [[Claude_Code|Claude]] Haiku 系列模型，[[上下文窗口]]为 200k tokens，支持 [[上下文感知]] 功能。

## 关键内容

### 基本信息

- **模型 ID**：`claude-haiku-4-5`
- **系列**：[[Claude_Code|Claude]] Haiku
- **版本**：4.5
- **[[上下文窗口]]**：200k tokens
- **发布方**：[[Anthropic]]

### 支持的功能

- [[上下文感知]]（[[上下文感知|Context Awareness]]）
- 符合 [[零数据保留]] (ZDR) 条件

### 定位

Haiku 系列是 [[Anthropic]] 的成本优化型模型，在保持[[上下文感知]]等高级功能的同时，提供比 Sonnet 和 Opus 更低的推理成本。

## 来源

- [[raw/articles/ai-engineering/anthropic-developer/Context windows.md]] — Anthropic 官方文档

## 相关

- [[上下文窗口]] — implements（200k 上下文窗口）
- [[上下文感知]] — implements（支持上下文感知）
