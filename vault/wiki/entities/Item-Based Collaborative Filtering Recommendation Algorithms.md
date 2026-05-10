---
type: entity
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 协同过滤, 论文]
aliases: ["Item-Based CF", "基于物品的协同过滤推荐算法", "Item-Based Collaborative Filtering Recommendation Algorithms", "Sarwar 2001"]
entity_type: paper
relates_to:
  - target: "[[Badrul Sarwar]]"
    type: authored
    confidence: 0.9
  - target: "[[George Karypis]]"
    type: authored
    confidence: 0.9
  - target: "[[Joseph Konstan]]"
    type: authored
    confidence: 0.9
  - target: "[[John Riedl]]"
    type: authored
    confidence: 0.9
  - target: "[[协同过滤]]"
    type: extends
    confidence: 0.9
  - target: "[[User-Based 协同过滤]]"
    type: improves_upon
    confidence: 0.9
  - target: "[[Adjusted Cosine Similarity]]"
    type: introduces
    confidence: 0.9
  - target: "[[MovieLens]]"
    type: evaluated_on
    confidence: 0.8
  - target: "[[平均绝对误差 MAE]]"
    type: uses_metric
    confidence: 0.9
  - target: "[[GroupLens Research Group]]"
    type: affiliated_with
    confidence: 0.9
  - target: "[[University of Minnesota]]"
    type: affiliated_with
    confidence: 0.9
  - target: "[[Pearson 相关系数]]"
    type: compares_to
    confidence: 0.8
  - target: "[[基于物品的协同过滤]]"
    type: proposes
    confidence: 0.9
supersedes: null
---

# Item-Based Collaborative Filtering Recommendation Algorithms

## 概述
一篇2001年发表的经典推荐系统论文，提出[[基于物品的协同过滤|基于物品的协同过滤算法]]，通过预[[计算]]物品相似度表将推荐系统性能提升数量级。

## 关键内容
1. **核心贡献**：
   - 提出了[[基于物品的协同过滤|Item-Based CF]][[算法]]，通过[[计算]]物品间相似度而非用户间相似度来生成推荐
   - 解决了[[基于用户的协同过滤|User-Based CF]]在大规模系统中的可扩展性瓶颈问题
   - 实现了离线预[[计算]]物品相似度表，在线实时生成推荐的架构

2. **方法创新**：
   - 系统性研究了三种物品相似度[[计算]]方法：余弦相似度、调整后余弦相似度、皮尔逊相关系数
   - 提出了"调整后余弦相似度"([[Adjusted Cosine Similarity]])，有效消除用户评分尺度差异
   - 实验证明调整后余弦相似度表现最优

3. **架构优势**：
   - 物品间相似度关系比用户间相似度关系更稳定，可离线预[[计算]]
   - 实现了"离线模型构建+在线查表预测"的架构[[规范化理论|范式]]
   - 时间复杂度从O(M)降低到O(K)，M为用户总数，K为邻居数量

4. **实验验证**：
   - 使用[[MovieLens]] 100K数据集进行评估，包含943个用户、1,682部电影、100,000条评分
   - 采用[[平均绝对误差 MAE|平均绝对误差]](MAE)作为主要评估指标
   - 证明[[基于物品的协同过滤|Item-Based CF]]在保持与[[基于用户的协同过滤|User-Based CF]]相当甚至更优推荐质量的同时，实现了显著的性能提升

5. **历史地位**：
   - 推荐系统领域引用量最高的论文之一（[[Google]] Scholar超10,000次引用）
   - 与[[Amazon]]的Item-to-Item CF[[算法]]共同奠定了[[基于物品的协同过滤|Item-Based CF]]作为工业级推荐系统核心技术的地位
   - 确立了"离线预[[计算]]+在线查表"的架构[[规范化理论|范式]]，影响至今

## 来源
- [[从"找相似用户"到"找相似物品"：Item-Based CF 如何重塑推荐系统]] — raw/books/推荐系统/03-item-based-collaborative-filtering.md
- [论文原文](https://doi.org/10.1145/371920.372071)

## 相关
- [[协同过滤]] — extends
- [[User-Based 协同过滤]] — improves_upon
- [[Adjusted Cosine Similarity]] — introduces_method
- [[Badrul Sarwar]] — authored
- [[Joseph Konstan]] — authored
- [[MovieLens]] — evaluated_on
- [[平均绝对误差 MAE]] — uses_metric
