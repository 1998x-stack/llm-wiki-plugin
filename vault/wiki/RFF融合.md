---
type: concept
status: active
confidence: 0.5
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [技术, 方法论]
aliases: [Reciprocal Rank Fusion, RFF]
relates_to:
  - BGE-Reranker
  - BGE-M3
  - 检索重排序
  - 混合搜索
supersedes: null
---

# RFF融合

## 概述
RFF（Reciprocal Rank Fusion，倒数秩融合）是解决多路异构召回结果融合的无监督算法。它不看分数只看排名，将不同召回通道的结果统一到同一尺度，是目前 RAG 系统多路召回融合的标准方案。

## 关键内容
1. **核心公式**：`RRF_score(d) = ∑ 1 / (k + rank(d))`，其中 `rank(d)` 为文档在某路召回中的排名，`k` 为常量（行业默认值 60），用于降低低排名文档的影响
2. **无需训练调参**：完全无监督，天然适配向量检索、BM25、知识图谱等异构召回通道，无需分数归一化
3. **工业级效果**：混合召回+RFF 融合可将召回率从单路向量检索的 85% 提升至 92%，同时准确率不降反升
4. **主流引擎支持**：Elasticsearch 等主流搜索引擎已原生支持 RFF，接入成本极低
5. **工业流程**：多路并行召回 → 每路返回 Top50 → RFF 融合去重得到 Top20 → BGE-Reranker 重排 → 送入大模型上下文

## 来源
- [[raw/articles/essays/thinking-series/008-算法面试]] — 全文

## 相关
- [[BGE-Reranker]] — extends（RFF 融合后接 BGE 重排）
- [[BGE-M3]] — relates_to（同属检索链路组件）
- [[检索重排序]] — relates_to
- [[混合搜索]] — relates_to
