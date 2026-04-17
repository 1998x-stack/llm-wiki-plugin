---
type: entity
entity_type: tool
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [向量检索, ANN, Google, 推荐系统基础设施, 推荐系统]
aliases: [SCaNN, Scalable Nearest Neighbors]
relates_to:
  - {target: 近似最近邻检索, type: implements}
  - {target: 双塔模型, type: uses}
  - {target: Deep Neural Networks for YouTube Recommendations, type: extends}
  - {target: Embedding, type: uses}
supersedes: null
---

# ScaNN

## 概述
[[Google]] 开发的[[近似最近邻检索]]库，专为大规模推荐系统设计，提供速度和精度最优平衡的向量搜索能力。

## 关键内容

1. **与 [[Deep Neural Networks for YouTube Recommendations|YouTube DNN]] 的关系**：[[Deep Neural Networks for YouTube Recommendations]] 中"训练时用 softmax，服务时用 ANN 检索"的思路，直接推动了[[近似最近邻检索|向量检索]]技术在推荐系统中的广泛应用。[[Faiss]]（[[Meta|Facebook]]）、ScaNN（[[Google]]）、Milvus、Pinecone 等向量数据库和检索库的兴起，都与这一[[规范化理论|范式]]的流行密切相关。

2. **核心能力**：ScaNN（Scalable Nearest Neighbors）是 [[Google]] 专门为大规模推荐系统优化的 ANN 库。相比通用 ANN 库，ScaNN 在大规模推荐场景下提供了更好的速度-精度权衡，支持 Anisotropic Vector Quantization 等高级算法。

3. **在推荐系统中的角色**：与 [[Faiss]] 类似，ScaNN 用于在 [[双塔模型]] 产生的物品 embedding 空间中快速找到与用户 embedding 最近的 Top-N 个物品，是 [[候选生成]] 阶段的核心检索组件。

4. **与现代检索技术的关系**：当前的 ANN 检索技术（如 HNSW、IVF-PQ、ScaNN）已经比2016年时的方案在速度和精度上提升了数个量级。

## 来源
- [[07-youtube-dnn.md]] — Deep Neural Networks for YouTube Recommendations 深度解读

## 相关
- [[Deep Neural Networks for YouTube Recommendations]] — 推动 ScaNN 等向量检索库兴起的范式
- [[近似最近邻检索]] — ScaNN 实现的核心技术
- [[双塔模型]] — 产生 embedding 的模型架构
- [[Faiss]] — Facebook 的同类竞品
- [[Embedding]] — ScaNN 检索的输入
