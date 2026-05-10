---
type: entity
entity_type: company
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 流媒体, 数据集]
aliases: [Netflix, 网飞, 奈飞]
relates_to:
  - {target: Netflix Prize, type: part_of}
  - {target: Cinematch, type: uses}
  - {target: 矩阵分解, type: uses}
  - {target: BellKor, type: compares_to}
supersedes: null
---

# Netflix

## 概述
全球流媒体巨头，2006 年发起 [[Netflix Prize]] 竞赛推动推荐系统技术革命，其 [[Cinematch]] 推荐引擎和公开数据集奠定了[[矩阵分解]]方法的工业地位。

## 关键内容

1. **[[Netflix Prize]] 发起者**：2006 年 10 月，Netflix 向全球发出价值 100 万美元的挑战——谁能将其推荐[[算法]] [[Cinematch]] 的评分预测精度（RMSE）提升 10%，即可获奖。同时公开了包含 1 亿条评分、48 万用户、17,770 部电影的数据集，成为推荐系统研究史上最重要的公开数据集之一。
2. **[[Cinematch]] 基线**：竞赛前 Netflix 的推荐引擎 [[Cinematch]] 基线 RMSE 为 0.9514。这一基线成为了后续所有推荐[[算法]]比较的参考点。
3. **工业影响**：[[Netflix Prize]] 竞赛持续近三年（2006-2009），吸引来自 186 个国家超过 40,000 支队伍参赛。竞赛结果证明[[矩阵分解]]方法在精度上全面超越传统近邻[[协同过滤]]，推动了 [[Spotify]]、[[Amazon]]、[[YouTube]] 等大量工业推荐系统采用[[矩阵分解]]技术。
4. **数据稀疏度**：Netflix 数据集的稀疏度高达 98.8%，这一极端稀疏场景暴露了传统方法的天花板，催生了[[隐因子模型]]的崛起。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[Netflix Prize]] — 发起的竞赛
- [[Cinematch]] — 原有推荐引擎
- [[BellKor]] — 竞赛获胜团队
- [[矩阵分解]] — 竞赛中确立的主导技术
