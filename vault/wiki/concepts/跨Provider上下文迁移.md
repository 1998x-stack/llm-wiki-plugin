---
type: concept
title: "跨 Provider 上下文迁移"
status: active
confidence: 0.85
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 技术, 方法论, AI工程]
aliases:
  - Context Handoff
  - Cross-Provider Context Migration
  - 会话跨模型迁移
relates_to:
  - target: "[[Pi-Agent]]"
    type: implements
    confidence: 0.95
  - target: "[[LLM-Wire-Protocol统一模式]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Context-Engineering]]"
    type: extends
    confidence: 0.85
supersedes: null
---

# 跨 Provider 上下文迁移

## 概述

Context Handoff 是 [[Pi-Agent]] pi-ai 层最独特的能力：一个会话可以在 Anthropic → OpenAI → [[Google]] 等不同 Provider 之间无缝延续，历史对话、思维链、工具调用记录完整保留。这在其他统一 LLM API 中几乎没有对应实现。

## 关键内容

### 1. 核心机制

pi-ai 维护 Provider 无关的 `Context` 对象（消息数组），在切换 Provider 时自动执行转换管道：
- Anthropic thinking traces → `<thinking></thinking>` 标签文本
- OpenAI reasoning → 文本块
- Provider 特有的签名 blob → 重放或转换

### 2. 工程挑战

各 Provider 在流式事件中插入的**签名 blob**（如 Anthropic 的 cache 标记、OpenAI 的 reasoning 元数据）在切换模型时必须正确重放。pi-ai 采用"尽力而为"（best-effort）策略，不保证 100% 精确互操作，但对绝大多数场景足够。

### 3. 实际应用

[[OpenClaw]] 利用此能力实现跨渠道会话共享——WhatsApp 上发起的对话可以在 Telegram 上继续，背后可能使用不同的 LLM Provider。

### 4. 依赖 JSONL 会话格式

Context Handoff 的前提是 Pi 的 JSONL 会话持久化——每条消息独立序列化，可跨 Provider 反序列化并继续。这是 Pi "会话 JSONL 第一公民"哲学的直接产物。

## 来源

- [[raw/articles/ai-tools/pi-agent/02-pi-ai.md]]

## 相关

- [[Pi-Agent]] — 实现者
- [[LLM-Wire-Protocol统一模式]] — 依赖四协议统一层
- [[Context-Engineering]] — 上下文工程哲学延伸
- [[OpenClaw]] — 应用场景
