---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "模型评估", "集成学习"]
aliases: ["OOB Error", "Out-of-Bag Error", "袋外误差估计", "OOB 误差"]
relates_to: ["Bagging（自举聚合）", "随机森林（Random Forests）", "交叉验证"]
supersedes: null
---

# 袋外误差（Out-of-Bag Error）

## 概述 (50-200字符)
[[Bagging（自举聚合）|Bagging]] 的内置模型评估方法，利用未被某棵树训练过的样本（约 36.8%）进行验证，无需额外划分验证集即可估计泛化误差。

## 关键内容 (≥300字符, 用[[双链]])
1. **原理**：在 [[Bagging（自举聚合）]] 中，每棵树训练时约 36.8% 的样本未被使用（袋外样本）。对每个训练样本 xᵢ，仅用"没有用 xᵢ 训练"的决策树（约 T/e 棵）对其进行预测并投票。
2. **计算方法**：OOB 误差 = 所有样本的 OOB 预测误差均值。该估计≈交叉验证误差，但无需额外划分验证集，节省了数据和计算资源。
3. **在随机森林中的应用**：[[随机森林（Random Forests）]] 将 OOB 误差作为内置的模型性能指标。训练完成后直接输出 OOB 准确率，用户无需手动划分 train/test split 或执行 k-fold 交叉验证。
4. **特征重要性计算基础**：[[排列重要性（Permutation Importance）]]方法依赖 OOB 样本——先计算原始 OOB 误差 E，再随机打乱某特征值后计算 OOB 误差 E'，重要性 = E' - E。误差增量越大，特征越重要。

## 来源
- [Breiman, L. (2001). Random forests. Machine learning, 45(1), 5–32.] — 提出 OOB 误差作为随机森林的内置评估方法

## 相关
- [[Bagging（自举聚合）]] — depends_on
- [[随机森林（Random Forests）]] — uses
- [[排列重要性（Permutation Importance）]] — enables
- [[交叉验证]] — compares_to
