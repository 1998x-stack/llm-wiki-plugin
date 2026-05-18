---
type: tool
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [api, ai-models, anthropic, messaging, AI工程]
aliases: ["Anthropic Messages API", "Anthropic API"]
relates_to: 
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[Anthropic]]"
    type: provided_by
  - target: "[[Claude (模型)]]"
    type: supports
supersedes: null
---

# Anthropic Messages API

## 概述
Anthropic Messages API是由Anthropic公司提供的API服务，用于直接访问其AI模型能力，特别是Claude系列模型。

## 关键内容
1. **功能特性**：提供直接访问Anthropic模型能力的接口，支持多轮对话、工具调用等功能。

2. **在Claude Code中的应用**：Claude Code通过Anthropic Messages API直接接入模型能力，体现了其"直接暴露模型能力"的设计理念。

3. **技术优势**：相比其他封装较深的接口，Messages API提供更低级别的直接访问，符合Claude Code的极简设计哲学。

4. **模型支持**：支持多种Anthropic模型，包括Claude Sonnet、Claude Opus等不同性能等级的模型。

## 来源
- [[01_system_overview.md]] — Tech Stack部分提及

## 相关
- [[Claude Code]] — uses
- [[Anthropic]] — provided_by
- [[Claude (模型)]] — supports