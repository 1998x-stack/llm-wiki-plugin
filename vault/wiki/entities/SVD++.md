---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 3
tags: [推荐系统, 矩阵分解, 隐式反馈]
aliases: [SVD++, Factorization Meets the Neighborhood]
relates_to:
  - {target: Yehuda Koren, type: implements}
  - {target: 矩阵分解, type: extends}
  - {target: 隐式反馈, type: uses}
  - {target: Factorization Machines, type: extends}
  - {target: Netflix Prize, type: part_of}
supersedes: null
---

# SVD++

## 概述
[[Yehuda Koren]] 于 KDD 2008 提出的[[矩阵分解]]扩展模型，在 [[矩阵分解|MF]] 基础上引入用户[[隐式反馈]]历史，在 [[Netflix Prize]] 竞赛中表现卓越，后被证明可被 [[Factorization Machines]] 框架等价表示。

## 关键内容

1. **核心思想**：在传统[[矩阵分解]]（用户[[嵌入表示|隐向量]] × 物品[[嵌入表示|隐向量]]）基础上，额外引入用户的[[隐式反馈]]信息——用户曾经评过哪些物品、浏览过哪些物品等，将这些行为编码为归一化的物品指示变量，与显式评分共同建模。
2. **模型结构**：[[奇异值分解|SVD]]++ 的预测公式包含四部分：全局偏置、用户偏置、物品偏置、用户-物品[[嵌入表示|隐向量]]内积，以及[[隐式反馈]]项（用户历史行为物品的[[嵌入表示|隐向量]]加权求和）。这使得模型不仅利用显式评分，还利用了用户的[[隐式反馈|行为信号]]。
3. **[[Netflix Prize]] 表现**：[[奇异值分解|SVD]]++ 是 [[BellKor]] 团队赢得 [[Netflix Prize]]（2009年，100万美元大奖）的核心技术之一，在 [[Netflix]] 数据集上取得了显著的精度提升。
4. **与 [[Factorization Machines|FM]] 的等价关系**：在 [[Factorization Machines]] 框架下，只需在特征向量中额外拼接一组归一化的物品指示变量（表示用户历史评过的物品），[[Factorization Machines|FM]] 的交互项就会自动包含 [[奇异值分解|SVD]]++ 中的[[隐式反馈]]交互，无需重新设计模型方程和优化算法。
5. **后续影响**：[[奇异值分解|SVD]]++ 的[[隐式反馈]]融合思想被后续大量推荐系统工作继承，包括 [[timeSVD++]]（加入时间动态建模）等变体。[[Factorization Machines|FM]] 的统一框架进一步证明了这种"特征编码决定建模能力"而非"模型结构决定一切"的范式。

## 来源
- [Factorization Meets the Neighborhood (Koren 2008)](https://dl.acm.org/doi/10.1145/1401890.1401944)
- [Factorization Machines (Rendle 2010)](https://arxiv.org/abs/1209.3994)
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[Yehuda Koren]] — 第一作者
- [[矩阵分解]] — 基础模型
- [[隐式反馈]] — 核心创新点
- [[Factorization Machines]] — 可等价表示 SVD++ 的统一框架
- [[Netflix Prize]] — 应用场景
