---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ai-engineering, retrieval, rag, knowledge-management]
aliases: [RAG, Retrieval Augmented Generation, 检索增强生成]
relates_to:
  - target: "[[上下文工程]]"
    type: extends
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[Contextual Retrieval]]"
    type: supersedes
supersedes: null
---

# RAG 系统

## 概述
RAG（检索增强生成）是结合信息检索与语言生成的 AI 架构模式，通过从外部知识库检索相关上下文来增强模型生成能力。

## 关键内容

1. **Contextual Retrieval 突破**：2024 年 9 月 Anthropic 提出的上下文检索方法，通过为文本块添加语境前缀，降低检索失败率 49-67%。这是 RAG 系统的重要演进方向。

2. **检索失败优化**：传统 RAG 系统的核心问题是检索上下文不足，Contextual Retrieval 通过增加语境信息显著改善这一问题。

3. **与上下文工程的关系**：RAG 是上下文工程的重要组成部分，提供外部知识检索能力，与压缩、记录、子 Agent 等技术共同构成完整的上下文管理框架。

4. **工程实践挑战**：RAG 系统的质量取决于检索准确性、上下文相关性和生成一致性，需要持续的评测和优化。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — 上下文工程与知识管理章节

## 相关
- [[上下文工程]] — extends
- [[Anthropic]] — part_of
- [[Contextual Retrieval]] — supersedes
- [[评测驱动开发]] — relates_to
