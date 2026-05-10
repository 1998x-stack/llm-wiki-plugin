---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [信息检索, RAG, 排序算法]
aliases: [Reranking, 检索重排序, 重排序]
relates_to:
  - "[[上下文检索]] — uses"
  - "[[BM25]] — relates_to"
  - "[[语义嵌入]] — relates_to"
supersedes: null
---

# Reranking

## 概述
Reranking（检索重排序）是在初始检索后对候选文档块进行精细打分排序的技术，通过相关性模型对 Top 候选块重新评分，进一步提升检索准确性。

## 关键内容

1. **工作流程**：初始检索取 Top 150 候选块 → 重排序模型对每块评分（查询相关性 + 重要性）→ 取 Top 20 块传给生成模型。

2. **性能提升**：在 [[上下文检索]] 中，结合语境嵌入和语境 BM25 后，再加 Reranking 可将检索失败率从 2.9% 降至 1.9%，相对基准降低 **67%**。

3. **成本-性能权衡**：重排序增加了推理延迟，需要在性能提升和延迟增加之间找到平衡点。

4. **与混合检索的关系**：Reranking 是在语义嵌入 + BM25 混合检索之后的第三层增强，形成三层检索增强架构。

## 来源
- [[02_contextual_retrieval.md]] — 重排序作用与性能实验章节

## 相关
- [[上下文检索]] — uses
- [[BM25]] — relates_to
- [[语义嵌入]] — relates_to
- [[检索增强生成]] — uses
