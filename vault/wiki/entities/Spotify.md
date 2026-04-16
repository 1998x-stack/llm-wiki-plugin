---
type: entity
entity_type: company
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 音乐流媒体]
aliases: [Spotify, 声破天]
relates_to:
  - {target: 矩阵分解, type: uses}
  - {target: 混合推荐系统, type: uses}
supersedes: null
---

# Spotify

## 概述
全球音乐流媒体平台，工业界采用[[矩阵分解]]方法作为推荐系统核心策略的代表性公司之一。

## 关键内容

1. **[[矩阵分解]]的工业采用**：Koren 等人 2009 年论文中描述的[[矩阵分解]]方法（特别是带 Bias 项的 SGD 优化）被 Spotify 等大量工业推荐系统采用或作为重要的[[候选生成]]策略之一。
2. **推荐场景**：Spotify 的推荐场景包括音乐推荐、播放列表生成、Discover Weekly 等，[[矩阵分解]]为其提供了用户-物品匹配的基础建模能力。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[矩阵分解]] — 采用的核心推荐技术
- [[Amazon]] — 同样采用 MF 的工业平台
- [[YouTube]] — 同样采用 MF 的工业平台
