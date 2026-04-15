---
type: entity
entity_type: project
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 推荐引擎]
aliases: [Cinematch]
relates_to:
  - {target: Netflix, type: part_of}
  - {target: Netflix Prize, type: compares_to}
  - {target: 矩阵分解, type: supersedes}
supersedes: null
---

# Cinematch

## 概述
[[Netflix]] 原有推荐引擎，[[Netflix Prize]] 竞赛的基线系统，[[RMSE]] 0.9514，后被[[矩阵分解]]方法全面超越。

## 关键内容

1. **基线性能**：Cinematch 是 [[Netflix]] 在 2006 年发起 [[Netflix Prize]] 竞赛时使用的推荐引擎，其基线 [[RMSE]] 为 0.9514。竞赛目标是将其精度提升 10%（即 [[RMSE]] 降至 0.8563 以下）。
2. **技术局限**：Cinematch 主要基于传统近邻[[协同过滤]]方法，在面对 [[Netflix]] 数据集 98.8% 的极高稀疏度时，其能力触顶。
3. **被超越**：竞赛过程中，[[矩阵分解]]方法（从 [[FunkSVD]] 到 [[SVD++]] 到 [[timeSVD++]]）逐步将 [[RMSE]] 从 0.9514 降至 0.8567，Cinematch 最终被全面超越。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[Netflix]] — 所属公司
- [[Netflix Prize]] — 作为基线被挑战
- [[矩阵分解]] — 超越 Cinematch 的技术
