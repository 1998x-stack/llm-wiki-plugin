---
type: concept
title: "LLM Wire Protocol 统一模式"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
  - AI
  - 技术
  - 架构
aliases:
  - LLM Wire Protocol
  - 四协议统一模式
  - Unified LLM API
relates_to:
  - target: "[[Pi-Agent]]"
    type: implements
    confidence: 0.95
  - target: "[[Context-Engineering]]"
    type: extends
    confidence: 0.7
supersedes: null
---

# LLM Wire Protocol 统一模式

## 概述

[[Mario-Zechner]] 在构建 [[Pi-Agent]] 的 pi-ai 层时发现：市面上 300+ LLM 模型归根结底只实现了四种 Wire Protocol（OpenAI Completions、OpenAI Responses、Anthropic Messages、Google Gen AI）。只需四个适配器即可统一覆盖所有 Provider。

## 关键内容

### 1. 四种协议全景

| 协议 | 代表 Provider |
|------|--------------|
| OpenAI Completions API | OpenAI、Groq、Mistral、Cerebras、xAI、Ollama、vLLM、LM Studio、llama.cpp |
| OpenAI Responses API | OpenAI（新版） |
| Anthropic Messages API | Anthropic、AWS Bedrock |
| Google Generative AI | Google Gemini 全系列 |

### 2. Provider 差异的实际痛点

即使号称"OpenAI 兼容"的端点也各有怪癖：Cerebras/xAI 不接受 `store` 字段、Mistral 用 `max_tokens` 而非 `max_completion_tokens`、各家推理模型的 reasoning 内容字段名各不相同（`reasoning_content` / `reasoning` / `thinking`）。

### 3. 适配器路由机制

pi-ai 的 Model 对象包含 `api` 字段决定路由到哪个适配器，与 `provider` 字段无关。这意味着任何 OpenAI 兼容端点只需声明 `api: 'openai-completions'` + `baseUrl` 即可接入，无需编写新的适配代码。

### 4. 统一事件流

所有 Provider 的流式输出标准化为五种事件：`text_delta`、`thinking_delta`、`toolcall_delta`、`done`、`error`。切换 Provider 只需改 `getModel()` 的一个参数，流式处理代码完全不变。

## 来源

- [[raw/articles/ai-tools/pi-agent/02-pi-ai.md]]

## 相关

- [[Pi-Agent]] — 实现者
- [[Context-Engineering]] — 上下文工程设计哲学
