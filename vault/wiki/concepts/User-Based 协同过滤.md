---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 协同过滤, 用户相似度]
aliases: ["User-Based Collaborative Filtering", "User-Based CF", "基于用户的协同过滤"]
relates_to:
  - target: "[[协同过滤]]"
    type: part_of
  - target: "[[GroupLens]]"
    type: implements
  - target: "[[Pearson 相关系数]]"
    type: uses
  - target: "[[Item-Based 协同过滤]]"
    type: compares_to
  - target: "[[冷启动问题]]"
    type: caused
  - target: "[[数据稀疏性问题]]"
    type: caused
supersedes: null
---

# User-Based 协同过滤

## 概述
User-Based [[协同过滤]]（[[基于用户的协同过滤|User-Based Collaborative Filtering]]）是一种推荐算法[[规范化理论|范式]]，通过计算用户之间的相似度，找到与目标用户品味相似的邻居用户，然后基于邻居用户的评分来预测目标用户对未交互物品的评分。

## 关键内容

1. **核心思想**：如果两个用户在过去对某些物品的评价上达成一致，那么他们在未来对其他物品的评价也很可能一致。这一假设由 [[GroupLens]] 论文于 1994 年形式化，成为整个[[协同过滤]]领域的理论基石。

2. **用户相似度计算**：采用 [[Pearson 相关系数]] 衡量用户间评分模式的相似性：
   $$w(a, i) = \frac{\sum_{j \in J_{ai}} (v_{a,j} - \bar{v}_a)(v_{i,j} - \bar{v}_i)}{\sqrt{\sum_{j \in J_{ai}} (v_{a,j} - \bar{v}_a)^2 \cdot \sum_{j \in J_{ai}} (v_{i,j} - \bar{v}_i)^2}}$$
   取值范围 [-1, 1]，其中 1 表示完全正相关，-1 表示完全负相关，0 表示无关联。

3. **加权预测公式**：
   $$\hat{r}_{u,j} = \bar{r}_u + \frac{\sum_{k \in N(u)} w(u,k) \cdot (r_{k,j} - \bar{r}_k)}{\sum_{k \in N(u)} |w(u,k)|}$$
   直觉解释：从目标用户的平均分出发，按相似度加权叠加邻居用户的评分偏差。

4. **[[Pearson 相关系数]]的优势**：
   - **均值中心化**：衡量评分偏离个人均值的模式，兼容不同评分习惯的用户（如"手紧型"和"手松型"评分者）
   - **方向鲁棒性**：若两用户品味完全相反，产生负相关，系统可将对方的高分"翻译"为低分预测

5. **计算复杂度**：计算所有用户对之间的相关系数需要 $O(n^2)$ 的时间和空间，其中 $n$ 是用户数量。这是 [[基于用户的协同过滤|User-Based CF]] 的主要可扩展性瓶颈。

6. **局限性**：
   - [[冷启动问题]]：新用户无历史评分时无法计算相似度
   - [[数据稀疏性问题]]：用户-物品评分[[矩阵]]极其稀疏，共同评分少时 Pearson 系数不可靠
   - 可扩展性瓶颈：用户数量增长时计算复杂度平方级增长
   - 后来 [[Amazon]] 等公司转向 [[Item-Based 协同过滤]] 正是为了解决这一瓶颈

7. **历史地位**：[[GroupLens]] 的加权预测公式后来成为 [[基于用户的协同过滤|User-Based CF]] 的标准[[规范化理论|范式]]，在随后十余年间被无数论文引用、扩展和改进。[[Pearson 相关系数]]在此后十余年间一直是 [[基于用户的协同过滤|User-Based CF]] 的默认相似度度量。

## 来源
- [[raw/books/推荐系统/02-grouplens-collaborative-filtering.md]] — 核心方法详解章节

## 相关
- [[协同过滤]] — User-Based CF 是协同过滤的主要实现范式之一
- [[GroupLens]] — User-Based CF 的开创者
- [[Pearson 相关系数]] — User-Based CF 计算用户相似度的核心算法
- [[Item-Based 协同过滤]] — 为解决 User-Based CF 可扩展性瓶颈而发展出的替代范式
- [[冷启动问题]] — User-Based CF 面临的经典挑战
- [[数据稀疏性问题]] — User-Based CF 面临的核心难题
