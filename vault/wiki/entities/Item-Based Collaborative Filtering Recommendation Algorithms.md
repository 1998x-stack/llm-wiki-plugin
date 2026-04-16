---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 协同过滤, 学术论文]
aliases: ["Item-Based CF Paper", "Sarwar 2001"]
relates_to:
  - target: "[[基于物品的协同过滤]]"
    type: caused
  - target: "[[GroupLens]]"
    type: part_of
  - target: "[[MovieLens]]"
    type: uses
  - target: "[[基于用户的协同过滤]]"
    type: compares_to
supersedes: null
entity_type: paper
---

# Item-Based Collaborative Filtering Recommendation Algorithms

## 概述
推荐系统领域引用量最高的论文之一（[[Google]] Scholar 超 10,000 次），首次系统性分析和评估了[[基于物品的协同过滤]]方法，确立了"离线预计算 + 在线查表"的工业级推荐系统架构范式。

## 关键内容

1. **基本信息**：由明尼苏达大学 [[GroupLens|GroupLens 研究组]]的 [[Badrul Sarwar]]、George Karypis、[[Joseph Konstan]]、[[John Riedl]] 于 2001 年发表在 WWW '01 会议（第 10 届国际万维网大会，香港）。DOI: 10.1145/371920.372071。

2. **核心贡献**：提出将相似度计算从用户维度转换到物品维度，通过离线预计算物品相似度表，将推荐系统的在线计算复杂度从 O(M)（用户总数）降低到 O(K)（邻居数量），实现数量级的性能提升。

3. **调整后余弦相似度**：论文最重要的方法创新，通过减去每个用户的平均评分来消除用户评分尺度差异，实验证明在三种相似度方法中表现最优。

4. **实验验证**：使用 [[MovieLens]] 100K 数据集（943 用户、1,682 部电影、100,000 条评分），以[[平均绝对误差 MAE|平均绝对误差]]（[[平均绝对误差 MAE|MAE]]）为评估指标，证明 [[基于物品的协同过滤|Item-Based CF]] 在推荐质量和性能上均优于 [[基于用户的协同过滤|User-Based CF]]。

5. **与 [[Amazon]] 的关系**：[[Amazon]] 在 1998 年已独立开发了类似的 Item-to-Item [[协同过滤]]算法并申请专利（US Patent 6,266,649），但直到 2003 年才发表学术论文。本文是学术界首次系统性分析，两项工作被频繁共同引用。

6. **历史影响**：开创了 [[基于物品的协同过滤|Item-Based CF]] 研究方向，后续衍生出 Slope One（2005）、[[SVD++]]（2008）、FISM（2013）等重要工作。2017 年 IEEE Internet Computing 将 [[Amazon]] 相关论文评为最经受住"时间考验"的论文。

## 来源
- [论文原文](https://doi.org/10.1145/371920.372071)
- [GroupLens 论文 PDF](https://files.grouplens.org/papers/www10_sarwar.pdf)

## 相关
- [[基于物品的协同过滤]] — caused
- [[GroupLens]] — part_of
- [[MovieLens]] — uses
- [[基于用户的协同过滤]] — compares_to
- [[Adjusted Cosine Similarity]] — caused
