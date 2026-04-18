---
type: entity
entity_type: project
title: Claude Sonnet 3.7
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 工具, LLM能力]
aliases:
- claude-sonnet-3-7
- Claude Sonnet 3.7
relates_to:
- target: '[[上下文窗口]]'
  type: implements
  confidence: 0.95
- target: '[[交错式思考]]'
  type: contradicts
  confidence: 0.9
supersedes: null
---

# Claude Sonnet 3.7

## 概述

Claude Sonnet 3.7 是 [[Anthropic]] 发布的 Claude Sonnet 系列模型，[[上下文窗口]]为 200k tokens。是从该模型开始，Claude 在超出[[上下文窗口]]时返回验证错误而非静默截断。

## 关键内容

### 基本信息

- **模型 ID**：`claude-sonnet-3-7`
- **系列**：Claude Sonnet
- **版本**：3.7
- **[[上下文窗口]]**：200k tokens
- **发布方**：[[Anthropic]]

### 行为变更

从 Sonnet 3.7 开始，当提示词和输出令牌超出[[上下文窗口]]时，模型返回**验证错误**而非静默截断。这一变更带来了更可预测的行为，但要求对令牌进行更细致的管理。

### 不支持的功能

- **不支持 [[交错式思考]]**：在没有非工具结果用户轮次介入的情况下，[[扩展思维|扩展思考]]与工具调用不会交错进行

## 来源

- [[raw/articles/ai-engineering/anthropic-developer/Context windows.md]] — Anthropic 官方文档

## 相关

- [[上下文窗口]] — implements（200k 上下文窗口，验证错误行为起始模型）
- [[交错式思考]] — contradicts（不支持交错式思考）
