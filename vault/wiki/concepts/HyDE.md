---
type: concept
status: active
confidence: 0.75
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [信息检索, RAG, 向量搜索, LLM能力]
aliases: [HyDE, Hypothetical Document Embeddings, 假设文档嵌入]
relates_to:
  - "[[上下文检索]] — compares_to"
  - "[[语义嵌入]] — uses"
supersedes: null
---

# HyDE

## 概述
HyDE（Hypothetical Document [[Embedding]]s，假设文档嵌入）是一种[[零样本学习|零样本]]稠密检索方法，通过生成假设文档来改善[[向量空间模型|向量检索]]效果，与[[上下文检索]]方向不同。

## 关键内容

1. **核心思想**：对用户查询，先生成一个假设的理想回答文档，然后对该假设文档进行嵌入检索，而非直接对查询嵌入。

2. **与[[上下文检索]]对比**：
   - HyDE 在查询侧生成假设文档来匹配真实文档
   - [[上下文检索|Contextual Retrieval]] 在文档侧为每个块添加语境前缀
   - 两者方向不同，未直接比较，但思路有相似之处（都用 LLM 生成额外文本改善检索）

3. **局限性**：生成的假设文档可能引入噪声或不准确信息，且增加查询延迟。

## 来源
- [[02_contextual_retrieval.md]] — 与其他方法比较章节
- [HyDE: Precise Zero-Shot Dense Retrieval](https://arxiv.org/abs/2212.10496) — 原始论文

## 相关
- [[上下文检索]] — compares_to
- [[语义嵌入]] — uses
- [[检索增强生成]] — relates_to
