---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, machine-learning, ensemble, 机器学习]
aliases: [Breiman 2001]
relates_to:
  - target: Leo Breiman
    relation: authored_by
  - target: 随机森林
    relation: introduced
  - target: Bagging（自举聚合）
    relation: extends
supersedes: null
---

# Random Forests (2001 论文)

## 概述
提出[[随机森林]][[算法]]的论文，通过集成多个随机化[[决策树]]实现强大的分类和回归性能。

## 关键内容

1. **[[算法]]设计**：在 [[Bagging（自举聚合）]] 基础上，每次分裂时随机选择特征子集，进一步降低树之间的相关性。
2. **优势**：[[随机森林]]对[[过拟合（Overfitting）|过拟合]]鲁棒、无需调参、可以处理高维数据，并提供特征重要性评估。
3. **与深度学习对比**：在表格数据领域，[[随机森林]]至今仍与 [[深度学习]] 方法竞争，两者形成互补。

## 来源
- [[ai_papers_timeline.md]] — 2001 年时间线条目

## 相关
- [[Leo Breiman]] — authored_by
- [[随机森林]] — introduced
- [[Bagging（自举聚合）]] — extends
