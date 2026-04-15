---
type: entity
entity_type: company
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 电商]
aliases: [Amazon, 亚马逊]
relates_to:
  - {target: 矩阵分解, type: uses}
  - {target: 基于物品的协同过滤, type: uses}
supersedes: null
---

# Amazon

## 概述
全球电商平台，工业界采用[[矩阵分解]]方法作为推荐系统核心策略的代表性公司之一，早期以[[基于物品的协同过滤]]闻名。

## 关键内容

1. **[[矩阵分解]]的工业采用**：Koren 等人 2009 年论文中描述的[[矩阵分解]]方法被 Amazon 等大量工业推荐系统采用或作为重要的候选生成策略之一。
2. **推荐演进**：Amazon 早期以[[基于物品的协同过滤]]（[[基于物品的协同过滤|Item-Based CF]]）闻名，后逐步引入[[矩阵分解]]等[[隐因子模型]]以提升推荐精度。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[矩阵分解]] — 采用的推荐技术
- [[基于物品的协同过滤]] — 早期采用的方法
- [[Spotify]] — 同样采用 MF 的工业平台
