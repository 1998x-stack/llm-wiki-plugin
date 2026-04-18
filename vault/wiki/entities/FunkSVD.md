---
type: entity
entity_type: tool
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 矩阵分解, SGD]
aliases: [FunkSVD]
relates_to:
  - {target: Simon Funk, type: implements}
  - {target: Netflix Prize, type: part_of}
  - {target: 矩阵分解, type: implements}
  - {target: SVD++, type: supersedes}
supersedes: null
---

# FunkSVD

## 概述
[[Simon Funk]] 2006 年提出的基于 SGD 的[[矩阵分解]]方法，放弃了完整[[矩阵]]精确 SVD 分解的传统思路，仅在已知评分上进行梯度优化。

## 关键内容

1. **核心创新**：传统 SVD（如 LSA/LSI）需要对完整[[矩阵]]进行分解（$A = U \Sigma V^T$），但推荐系统中评分[[矩阵]]高度不完整。FunkSVD 仅在已知评分上进行梯度优化，避免了缺失值处理的难题。
2. **性能表现**：在 [[Netflix Prize]] 数据集上，FunkSVD 迅速将 RMSE 从基线 0.9514 降至约 0.896（约 5.9% 的提升），一举跃居排行榜第三位。
3. **优化方法**：使用[[随机梯度下降（SGD）]]进行优化，实现简单、收敛速度快、内存占用小。
4. **历史地位**：FunkSVD 点燃了推荐系统领域的方法论革命，是后续 [[SVD++]]、[[timeSVD++]] 等进阶模型的基础。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[Simon Funk]] — 提出者
- [[Netflix Prize]] — 应用竞赛
- [[矩阵分解]] — 方法论类别
- [[SVD++]] — 后续演进
