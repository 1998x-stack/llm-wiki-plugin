---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [统计学, 推荐系统, 相似度度量, 相关分析]
aliases: ["Pearson Correlation Coefficient", "Pearson's r", "皮尔逊积矩相关系数"]
relates_to:
  - target: "[[GroupLens]]"
    type: uses
  - target: "[[User-Based 协同过滤]]"
    type: uses
  - target: "[[协同过滤]]"
    type: uses
  - target: "[[余弦相似度]]"
    type: compares_to
supersedes: null
---

# Pearson 相关系数

## 概述
Pearson 相关系数（Pearson Correlation Coefficient）是衡量两个变量之间线性相关程度的统计量，取值范围 [-1, 1]，在推荐系统中被 [[GroupLens]] 系统首次用于[[计算]]用户间评分模式的相似度，成为 [[User-Based 协同过滤]]的默认相似度度量。

## 关键内容

1. **数学定义**：给定两个用户 $a$ 和 $i$，他们之间的 Pearson 相关系数定义为：
   $$w(a, i) = \frac{\sum_{j \in J_{ai}} (v_{a,j} - \bar{v}_a)(v_{i,j} - \bar{v}_i)}{\sqrt{\sum_{j \in J_{ai}} (v_{a,j} - \bar{v}_a)^2 \cdot \sum_{j \in J_{ai}} (v_{i,j} - \bar{v}_i)^2}}$$
   其中 $J_{ai}$ 是两用户都评过分的物品集合，$v_{a,j}$ 是用户 $a$ 对物品 $j$ 的评分，$\bar{v}_a$ 是用户 $a$ 的平均评分。

2. **取值含义**：
   - $w = 1$：完全正相关（品味一致）
   - $w = -1$：完全负相关（品味完全相反）
   - $w = 0$：无关联

3. **在推荐系统中的优势**：
   - **均值中心化**：衡量评分偏离个人均值的模式，而非绝对评分值。因此，即使两个用户使用评分量表的方式不同（如"手紧型"习惯打 3-5 分，"手松型"习惯打 1-3 分），只要相对偏好一致，相关系数仍然可以很高
   - **方向鲁棒性**：若两用户品味完全相反，Pearson 系数产生负相关，系统可将对方的高分"翻译"为低分预测

4. **在 [[GroupLens]] 中的应用**：[[GroupLens]] 论文（1994）首次将 Pearson 相关系数引入[[协同过滤]]，用于[[计算]] [[Usenet]] [[Usenet|新闻组]]用户间的相似度。此后十余年间，Pearson 相关系数一直是 [[User-Based 协同过滤]] 的默认相似度度量。

5. **局限性**：
   - 需要至少两篇共同评分的物品才能[[计算]]，实际中需要远多于此才能获得稳定估计
   - 只捕捉线性相关，无法检测非线性关系
   - 对异常值敏感
   - 现代推荐系统中已较少直接使用，被[[矩阵分解]]、深度学习等方法取代

6. **与其他相似度度量的比较**：
   - **余弦相似度**：不考虑均值中心化，对评分尺度敏感
   - **Jaccard 相似度**：只考虑是否交互，不考虑评分值
   - **Spearman 秩相关**：基于排序而非原始值，对异常值更鲁棒

## 来源
- [[raw/books/推荐系统/02-grouplens-collaborative-filtering.md]] — 用户相似度计算章节

## 相关
- [[GroupLens]] — 首次将 Pearson 相关系数引入协同过滤
- [[User-Based 协同过滤]] — Pearson 相关系数是 User-Based CF 的默认相似度度量
- [[协同过滤]] — Pearson 相关系数是协同过滤的核心技术组件
- [[余弦相似度]] — 与 Pearson 相关系数可比较的另一种相似度度量
