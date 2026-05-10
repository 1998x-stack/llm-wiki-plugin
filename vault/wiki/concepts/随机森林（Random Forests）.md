---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "集成学习", "表格数据"]
aliases: ["Random Forests", "随机森林分类器", "随机森林回归器"]
relates_to: ["Bagging（自举聚合）", "决策树（Decision Tree）", "偏差-方差分解", "袋外误差（Out-of-Bag Error）", "排列重要性（Permutation Importance）", "XGBoost", "LightGBM"]
supersedes: null
---

# 随机森林（Random Forests）

## 概述 (50-200字符)
一种基于[[模型融合|集成学习]]的机器学习[[算法]]，结合 [[Bagging（自举聚合）|Bagging]] 与随机特征子集，通过大量[[决策树]]投票实现高准确率、抗[[过拟合（Overfitting）|过拟合]]的预测模型。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心思想**：由 [[Leo Breiman]] 于 2001 年提出，公式为 `随机森林 = Bagging（1996）+ 随机特征子集`。单棵[[决策树]]高方差、不稳定，但通过训练 T 棵树并进行多数投票（分类）或平均（回归），错误相互抵消，集成效果显著优于个体。
2. **随机特征子集**：每次分裂节点时仅随机选取 m 个特征（分类推荐 m = ⌊√p⌋，回归推荐 m = ⌊p/3⌋），在该子集中寻找最优分裂点。这一创新降低了树间相关性 ρ，使集成方差下限 ρ·σ² 进一步减小。
3. **内置验证与可解释性**：[[Bagging（自举聚合）|Bagging]] 的有放回抽样使约 36.8% 样本成为袋外（OOB）样本，可直接用于误差估计，无需额外划分验证集。同时提供两种特征重要性量化方法：基尼重要性（快速但有偏）和排列重要性（更可靠）。
4. **历史地位**：深度学习崛起前是 Kaggle 竞赛的绝对主力；至今在表格数据上仍与 [[XGBoost]]、[[LightGBM]] 并列最强。默认参数通常已表现良好，无需复杂调参。

## 来源
- [Breiman, L. (2001). Random forests. Machine learning, 45(1), 5–32.] — 原始论文，提出随机森林算法、OOB 误差估计、特征重要性方法

## 相关
- [[Bagging（自举聚合）]] — part_of
- [[决策树（Decision Tree）]] — depends_on
- [[偏差-方差分解]] — implements
- [[袋外误差（Out-of-Bag Error）]] — uses
- [[排列重要性（Permutation Importance）]] — uses
- [[Leo Breiman]] — created_by
- [[Random Forests (Breiman 2001)]] — described_by
