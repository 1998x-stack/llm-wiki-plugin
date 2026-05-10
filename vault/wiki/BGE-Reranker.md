---
type: concept
status: active
confidence: 0.5
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [技术]
aliases: [BGE Reranker, BGE重排模型]
relates_to:
  - RFF融合
  - BGE-M3
  - 检索重排序
  - Cross-encoder与Bi-encoder
supersedes: null
---

# BGE-Reranker

## 概述
BGE-Reranker 是智源研究院（BAAI）开源的跨编码器重排模型系列，采用 Cross-Encoder 架构，将查询和文档拼接后通过双向自注意力机制逐词分析语义匹配关系，输出 0-1 相关性分数，是中文场景下性价比最高的 RAG 重排利器。

## 关键内容
1. **Cross-Encoder 架构**：不同于 Bi-encoder 分别编码再比距离，Cross-Encoder 将查询和文档拼成完整序列输入，通过双向自注意力实现细粒度语义匹配
2. **工业级落地流程**：RFF 融合得到 Top20 候选集 → 批量送入 BGE-Reranker 重新打分排序 → 按最终分数筛选送入大模型
3. **效果提升显著**：加入 BGE 重排后，RAG 系统 MRR@10 提升 37.2%，单点问题回答准确率从 80% 提升至 95% 以上
4. **解决噪音问题**：专门过滤语义接近但逻辑无关的"噪音文档"，是 RAG 准确率的最后一公里
5. **中文场景优势**：在中文多语种环境下表现优异，是当前中文 RAG 落地的首选重排模型

## 来源
- [[raw/articles/essays/thinking-series/008-算法面试]] — 全文

## 相关
- [[RFF融合]] — relates_to（RFF 融合后接 BGE 重排）
- [[BGE-M3]] — relates_to（同属 BGE 系列）
- [[检索重排序]] — extends
- [[Cross-encoder与Bi-encoder]] — implements
