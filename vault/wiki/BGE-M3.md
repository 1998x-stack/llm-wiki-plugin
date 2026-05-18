---
type: tool
status: active
confidence: 0.5
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [技术, AI工程]
aliases: [BGE M3, bge-m3]
relates_to:
  - BGE-Reranker
  - RFF融合
  - Embedding
  - 近似最近邻检索
supersedes: null
entity_type: tool
---

# BGE-M3

## 概述
BGE-M3 是智源研究院（BAAI）开源的多语种、多粒度嵌入模型，支持多语言、多粒度文本的向量表示，是目前中文场景下最主流的嵌入模型之一，广泛用于 RAG 系统的向量检索环节。

## 关键内容
1. **多语种支持**：支持超过 100 种语言的文本嵌入，适用于多语言 RAG 场景
2. **多粒度处理**：支持文档级、段落级、句子级等不同粒度的嵌入表示
3. **相似度阈值实践**：行业通用分级标准为 >0.85 极度相似、0.6-0.85 语义相关、<0.6 基本不相关，高精度场景下 0.78 是平衡召回率和精确率的最优值
4. **阈值确定方法**：构建正例（同义句）和负例（无关句）测试集，人工标注后构建相似度直方图，找到正负例分界点
5. **局限性**：余弦相似度本身不具备绝对语义意义，分布受文本长度、领域、语言复杂度影响，固定阈值无法适配所有场景

## 来源
- [[raw/articles/essays/thinking-series/008-算法面试]] — 全文

## 相关
- [[BGE-Reranker]] — relates_to（同属 BGE 系列，检索链路上下游）
- [[RFF融合]] — relates_to
- [[Embedding]] — part_of
- [[近似最近邻检索]] — uses
