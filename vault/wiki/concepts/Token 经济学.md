---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["token-optimization", "ai-memory", "context-engineering", "compression", "LLM能力"]
aliases: [Token Economics, Token Efficiency]
relates_to:
  - AAAK 方言
  - 上下文窗口
  - 语义压缩
  - 上下文压缩
supersedes: null
---

# Token 经济学

## 概述
Token 经济学研究在 LLM [[上下文窗口]]有限的约束下，如何最大化单位 token 的信息传递效率，是 AI 记忆系统和 RAG 架构的核心优化维度。

## 关键内容
- **核心问题**：普通英文的 token 效率低下，如约 20 tokens 仅传递 1 个事实（"The user decided to use [[PostgreSQL]] because the team had more experience with it than MySQL."）
- **优化目标**：通过压缩格式将同等事实压缩至约 5 tokens（如 `usr>psql[exp>mysql]`），实现约 4:1 的单条压缩比
- **规模效应**：在大规模重复实体场景下，压缩比可达到 30:1，这是 Token 经济学真正的收益区间
- **压缩格式对比**：
  - JSON：结构性 token（括号、引号、冒号）浪费大量空间
  - 二进制编码：AI 无法直接理解
  - 普通英文：信息密度不够高
  - [[AAAK 方言]]：保留语义可理解性，激进删除冗余，是第四条路
- **与[[上下文窗口]]的关系**：Token 经济学直接决定在有限[[上下文窗口]]内能加载多少历史信息，影响 AI Agent 的长期记忆能力
- **应用场景**：Closet 压缩摘要、System Prompt 优化、RAG 上下文装载、[[跨会话记忆]]持久化

## 来源
- [mempalace_03_aaak.md](/raw/articles/ai-tools/mempalace/mempalace_03_aaak.md) — MemPalace 深度解析第三篇：AAAK 方言

## 相关
- [[AAAK 方言]] — implements
- [[上下文窗口]] — depends_on
- [[语义压缩]] — compares_to
- [[上下文压缩]] — extends
