---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["prompt-caching", "anthropic", "cost-optimization", "LLM能力"]
aliases: [Prompt Cache, Anthropic Prompt Caching]
relates_to:
  - Hermes Agent
  - 冻结快照设计
  - 三种 API 模式
supersedes: null
---

# Prompt 缓存

## 概述
[[Hermes Agent]] 为 [[Anthropic]] API 模式实现的[[KV 缓存命中率|前缀缓存]]机制，标记 System Prompt 中的稳定前缀以命中缓存，大幅降低 Token 成本。

## 关键内容
- **实现位置**：`prompt_caching.py` 专为 `anthropic_messages` API 模式实现
- **缓存策略**：标记 System Prompt 中的稳定前缀（[[SOUL.md 人格系统|SOUL.md]] + [[语义记忆|MEMORY.md]] + USER.md），后续调用命中缓存
- **成本优化**：对于长期运行的 Agent，累积节省极为可观 — [[KV 缓存命中率|前缀缓存]] Token 的成本远低于常规 Token
- **与冻结快照协同**：[[冻结快照设计]]保证前缀稳定性，是 Prompt 缓存生效的前提条件
- **API 模式限制**：仅 [[Anthropic]] Messages API 支持此功能，chat_completions 和 codex_responses 模式无此优化

## 来源
- [02_hermes_architecture.md](/raw/articles/ai-tools/hermes/02_hermes_architecture.md) — Hermes Agent 深度解析系列第二篇，2026 年 4 月版本

## 相关
- [[Hermes Agent]] — implements
- [[冻结快照设计]] — extends
- [[三种 API 模式]] — part_of
