---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [api-mode, multi-provider, adapter]
aliases: [Three API Modes, API Adapter Pattern]
relates_to:
  - Hermes Agent
  - 模型无关设计
  - 同步编排引擎
supersedes: null
---

# 三种 API 模式

## 概述
[[Hermes Agent]] 不强迫所有供应商适配同一接口，而是为三种主流 API 格式分别实现适配器，通过 `hermes model` 命令运行时动态切换。

## 关键内容
- **chat_completions（最广泛）**：适用 [[OpenAI]]、Open[[网关与路由器|Router]]、Kimi、MiniMax、GLM、本地 [[Ollama]] 等 200+ 模型，[[OpenAI]] Chat Completions API 标准格式，兼容性最广
- **codex_responses（[[OpenAI]] 新格式）**：适用 [[OpenAI]] Responses API，支持 [[OpenAI]] 最新功能如 Reasoning tokens
- **anthropic_messages（[[Anthropic]] 原生）**：适用 Claude 系列直连，支持 [[提示词缓存|Prompt Caching]]、[[扩展思维|Extended Thinking]]、文档类型等 Claude 独有功能
- **切换方式**：`hermes model` 命令即可切换，无需更改任何应用代码，运行时动态解析 Provider
- **设计哲学**：不强迫统一接口，而是为三种主流格式分别实现适配器 — `anthropic_adapter.py` 专门处理 [[Anthropic]] Messages API 格式转换
- **与[[模型无关设计]]的关系**：三种 API 模式是[[模型无关设计]]的具体实现机制，保证 200+ 模型无缝切换

## 来源
- [02_hermes_architecture.md](/raw/articles/ai-tools/hermes/02_hermes_architecture.md) — Hermes Agent 深度解析系列第二篇，2026 年 4 月版本

## 相关
- [[Hermes Agent]] — implements
- [[模型无关设计]] — implements
- [[同步编排引擎]] — uses
- [[Prompt 缓存]] — extends
