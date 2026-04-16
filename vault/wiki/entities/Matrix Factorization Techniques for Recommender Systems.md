---
type: entity
entity_type: paper
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 矩阵分解, 综述]
aliases: [Matrix Factorization Techniques for Recommender Systems, MF 综述论文]
relates_to:
  - {target: Yehuda Koren, type: implements}
  - {target: Robert Bell, type: implements}
  - {target: Chris Volinsky, type: implements}
  - {target: Netflix Prize, type: part_of}
  - {target: 矩阵分解, type: implements}
  - {target: 隐因子模型, type: implements}
supersedes: null
---

# Matrix Factorization Techniques for Recommender Systems

## 概述
Koren、Bell、Volinsky 2009 年发表于 IEEE Computer 的综述论文，系统化了 [[Netflix Prize]] 竞赛中的[[矩阵分解]]方法论，成为推荐系统领域引用最多的文献之一。

## 关键内容

1. **论文信息**：发表于 IEEE Computer, Volume 42, Issue 8, pp. 30-37，DOI: 10.1109/MC.2009.263。截至 2026 年，[[Google]] Scholar 引用 15,000+，ACM Digital Library 引用 4,100+。
2. **核心贡献**：提出了由简到繁、层层递进的[[矩阵分解]]建模框架：
   - 基本 [[矩阵分解|MF]] 模型：$R \approx P \times Q^T$，用内积预测评分
   - [[Bias 建模]]：$\hat{r}_{ui} = \mu + b_u + b_i + q_i^T p_u$，分离系统性偏差
   - [[SVD++]]：融合[[隐式反馈]]信号
   - [[timeSVD++]]：引入时间动态建模
3. **优化方法**：详细讨论了随机梯度下降（SGD）和[[交替最小二乘法 ALS|交替最小二乘法]]（[[交替最小二乘法 ALS|ALS]]）两种优化策略的优劣与适用场景。
4. **历史地位**：将 [[Netflix Prize]] 竞赛中的实战经验升华为可复用的学术知识，确立了[[隐因子模型]]作为推荐系统第一范式的地位。此后十年中，几乎所有推荐系统研究都以[[矩阵分解]]为基线或出发点。
5. **现代视角**：[[矩阵分解]]中的隐因子向量本质上是现代深度学习中的 [[Embedding]]，该论文的思想直接影响了 [[Neural Collaborative Filtering]]、[[Wide & Deep]]、[[DeepFM]] 等后续深度学习推荐方法。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[Yehuda Koren]] — 第一作者
- [[Robert Bell]] — 共同作者
- [[Chris Volinsky]] — 共同作者
- [[Netflix Prize]] — 论文背景
- [[矩阵分解]] — 核心技术
- [[Neural Collaborative Filtering]] — 后续深度学习演进
