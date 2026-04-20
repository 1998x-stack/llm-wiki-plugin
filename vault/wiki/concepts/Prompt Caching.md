---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [LLM工程, 成本优化, Anthropic]
aliases: [Prompt Caching, 提示词缓存, 提示缓存]
relates_to:
  - "[[上下文检索]] — uses"
  - "[[Claude 3 Haiku]] — uses"
  - "[[工具结果缓存]] — compares_to"
supersedes: null
---

# Prompt Caching

## 概述
Prompt Caching 是 Anthropic 提供的一项工程特性，通过将长文档加载到缓存中供后续请求重复使用，显著降低批量 LLM 调用的成本。

## 关键内容

1. **工作原理**：文档只需加载到缓存一次，后续请求可直接复用缓存中的文档表示，避免重复处理相同内容。

2. **在上下文检索中的应用**：生成语境前缀时，同一文档的多个文本块共享相同的文档上下文，利用 Prompt Caching 可将成本降至每百万文档 token 1.02 美元。

3. **成本估算**：假设 800 token 块、8K token 文档、50 token 指令、100 token 语境，一次性生成语境化块的成本极低。

4. **适用场景**：适合批量处理同一文档的多个片段，如语境生成、批量摘要等任务。

## 来源
- [[02_contextual_retrieval.md]] — 成本优化章节

## 相关
- [[上下文检索]] — uses
- [[Claude 3 Haiku]] — uses
- [[Anthropic]] — implements
- [[工具结果缓存]] — compares_to (缓存输入 vs 缓存输出)
