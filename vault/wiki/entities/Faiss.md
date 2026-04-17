---
type: entity
entity_type: tool
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [向量检索, ANN, Facebook, 推荐系统基础设施, 推荐系统]
aliases: [FAISS, Facebook AI Similarity Search]
relates_to:
  - {target: 近似最近邻检索, type: implements}
  - {target: 双塔模型, type: uses}
  - {target: Deep Neural Networks for YouTube Recommendations, type: extends}
  - {target: Embedding, type: uses}
supersedes: null
---

# Faiss

## 概述
[[Meta|Facebook]] 开源的[[近似最近邻检索|向量检索]]库，提供高效的[[近似最近邻检索|近似最近邻]]搜索算法，是推荐系统[[候选生成]]阶段的核心检索基础设施。

## 关键内容

1. **与 [[Deep Neural Networks for YouTube Recommendations|YouTube DNN]] 的关系**：[[Deep Neural Networks for YouTube Recommendations]] 中"训练时用 softmax，服务时用 ANN 检索"的思路，直接推动了[[近似最近邻检索|向量检索]]技术在推荐系统中的广泛应用。[[Faiss]]（[[Meta|Facebook]]）、[[ScaNN]]（[[Google]]）、Milvus、Pinecone 等向量数据库和检索库的兴起，都与这一范式的流行密切相关。

2. **核心能力**：支持多种 ANN 算法（IVF-PQ、HNSW、Flat 等），可在 CPU 和 GPU 上运行，支持数十亿级别的[[近似最近邻检索|向量检索]]。提供了从精确搜索到各种近似搜索的完整方案谱系。

3. **在推荐系统中的角色**：在 [[双塔模型]] 产生用户和物品 embedding 后，Faiss 用于在物品 embedding 空间中快速找到与用户 embedding 最近的 Top-N 个物品，是 [[候选生成]] 阶段的核心检索组件。

4. **性能**：相比传统的精确最近邻搜索（O(V)），Faiss 的 ANN 算法能在亚线性时间内完成检索，同时保持较高的召回率。

## 来源
- [[07-youtube-dnn.md]] — Deep Neural Networks for YouTube Recommendations 深度解读

## 相关
- [[Deep Neural Networks for YouTube Recommendations]] — 推动 Faiss 等向量检索库兴起的范式
- [[近似最近邻检索]] — Faiss 实现的核心技术
- [[双塔模型]] — 产生 embedding 的模型架构
- [[ScaNN]] — Google 的同类竞品
- [[Embedding]] — Faiss 检索的输入
