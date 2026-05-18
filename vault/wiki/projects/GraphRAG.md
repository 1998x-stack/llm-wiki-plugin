---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [RAG, 知识图谱, 微软, LLM能力]
aliases: [GraphRAG]
relates_to:
  - "[[上下文检索]] — compares_to"
  - "[[LightRAG]] — compares_to"
  - "[[检索增强生成]] — extends"
supersedes: null
---

# GraphRAG

## 概述
GraphRAG 是微软提出的基于知识图谱的 RAG 方法，通过构建文档实体关系图，支持复杂的多跳推理和全局理解任务。

## 关键内容

1. **核心思想**：从文档中提取实体和关系，构建知识图谱，利用图结构进行检索和推理，超越单纯的文本块匹配。

2. **与上下文检索对比**：
   - Contextual Retrieval 在块级别添加上下文，实现简单、成本低
   - GraphRAG 在图结构层面建模，适合多跳推理和复杂查询
   - 实际工程中可先采用 Contextual Retrieval，复杂场景再考虑图增强

3. **优势**：支持全局文档理解、实体关系推理、主题聚类等高级检索能力。

## 来源
- [[02_contextual_retrieval.md]] — 与 LightRAG/GraphRAG 对比章节

## 相关
- [[上下文检索]] — compares_to
- [[LightRAG]] — compares_to
- [[检索增强生成]] — extends
