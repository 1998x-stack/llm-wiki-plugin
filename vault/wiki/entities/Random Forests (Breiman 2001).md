---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "集成学习", "经典论文"]
aliases: ["Random Forests 2001", "Breiman 2001 Random Forests"]
relates_to: ["随机森林（Random Forests）", "Bagging（自举聚合）", "Leo Breiman", "决策树（Decision Tree）"]
supersedes: null
---

# Random Forests (Breiman 2001)

## 概述 (50-200字符)
[[Leo Breiman]] 于 2001 年发表在 Machine Learning 期刊的论文，正式提出随机森林算法，引用量逾 10 万次，是机器学习领域被引最高的论文之一。

## 关键内容 (≥300字符, 用[[双链]])
1. **发表信息**：Breiman, L. (2001). Random forests. Machine learning, 45(1), 5–32. 作者 [[Leo Breiman]]，期刊 Machine Learning，年份 2001。
2. **核心贡献**：论文提出随机森林 = [[Bagging（自举聚合）]]（Breiman 1996）+ 随机特征子集（新贡献）。每次分裂节点时仅随机选取 m 个特征（分类 m = ⌊√p⌋，回归 m = ⌊p/3⌋），降低树间相关性，使集成方差进一步减小。
3. **理论分析**：论文给出了[[偏差-方差分解]]视角下的集成方差公式：集成方差 = ρ·σ² + (1-ρ)/T · σ²，证明当 T → ∞ 时方差下限由树间相关性 ρ 决定。同时提出袋外误差（[[袋外误差（Out-of-Bag Error）|OOB Error]]）作为内置验证方法，以及两种特征重要性量化方法。
4. **历史地位**：该论文是[[模型融合|集成学习]]领域的里程碑，直接催生了 [[XGBoost]]、[[LightGBM]] 等后续算法。至今在表格数据任务中，随机森林仍是首选算法之一。

## 来源
- [Breiman, L. (2001). Random forests. Machine learning, 45(1), 5–32.] — 原始论文

## 相关
- [[Leo Breiman]] — author
- [[随机森林（Random Forests）]] — describes
- [[Bagging（自举聚合）]] — builds_on
- [[偏差-方差分解]] — uses
