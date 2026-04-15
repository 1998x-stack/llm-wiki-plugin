---
type: entity
entity_type: person
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 矩阵分解, 开源贡献]
aliases: [Simon Funk, 西蒙·芬克]
relates_to:
  - {target: Netflix Prize, type: part_of}
  - {target: FunkSVD, type: implements}
  - {target: 矩阵分解, type: uses}
supersedes: null
---

# Simon Funk

## 概述
独立开发者，2006 年博客文章提出基于 SGD 的[[矩阵分解]]方法（[[FunkSVD]]），点燃推荐系统[[隐因子模型]]革命的里程碑人物。

## 关键内容

1. **[[FunkSVD]] 的诞生**：2006 年 12 月，在 [[Netflix Prize]] 竞赛开始仅两个月后，Simon Funk 以个人博客形式发表了一篇里程碑式文章，描述了基于随机梯度下降（SGD）的[[矩阵分解]]方法。该方法放弃了对完整[[矩阵]]做精确 [[奇异值分解|SVD]] 分解的传统思路，转而仅在已知评分上进行梯度优化。
2. **影响力**：[[FunkSVD]] 迅速将 [[Netflix Prize]] 的 [[RMSE]] 从基线 0.9514 降至约 0.896（约 5.9% 的提升），一举跃居排行榜第三位。这篇博客文章点燃了推荐系统领域的方法论革命，证明了[[隐因子模型]]在近邻[[协同过滤]]之上的巨大优势。
3. **历史地位**：作为独立开发者，Simon Funk 的工作展示了开源社区和个人研究者对推荐系统发展的关键推动作用。[[FunkSVD]] 成为后续 [[SVD++]]、[[timeSVD++]] 等进阶模型的基础。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[FunkSVD]] — 提出的算法
- [[Netflix Prize]] — 竞赛背景
- [[矩阵分解]] — 方法论基础
