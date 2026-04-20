---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [RAG, 图数据库, 知识图谱]
aliases: [LightRAG]
relates_to:
  - "[[上下文检索]] — compares_to"
  - "[[GraphRAG]] — compares_to"
  - "[[检索增强生成]] — extends"
supersedes: null
---

# LightRAG

## 概述
LightRAG 是一种基于图结构的 RAG 扩展方法，在图结构层面建模文档关系，支持多跳推理任务，与上下文检索方法互补。

## 关键内容

1. **核心思想**：将文档/文本块组织为图结构，节点表示文本块或实体，边表示它们之间的关系，支持通过图遍历进行多跳推理。

2. **与上下文检索对比**：
   - Contextual Retrieval 在块级别添加上下文，更轻量、易实施
   - LightRAG 在图结构层面建模，适合复杂查询场景
   - 两种方法不互斥，可叠加使用

3. **适用场景**：需要多跳推理、实体关系查询、知识图谱问答等场景。

## 来源
- [[02_contextual_retrieval.md]] — 与 LightRAG/GraphRAG 对比章节

## 相关
- [[上下文检索]] — compares_to
- [[GraphRAG]] — compares_to
- [[检索增强生成]] — extends
