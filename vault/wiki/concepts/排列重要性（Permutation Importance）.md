---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "特征工程", "可解释性"]
aliases: ["Permutation Importance", "排列特征重要性", "置换重要性"]
relates_to: ["随机森林（Random Forests）", "袋外误差（Out-of-Bag Error）", "基尼重要性（Mean Decrease Impurity）"]
supersedes: null
---

# 排列重要性（Permutation Importance）

## 概述 (50-200字符)
一种可靠的特征重要性量化方法，通过随机打乱某特征值后测量模型误差增量来评估该特征对预测的贡献程度。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[算法]]流程**：对每个特征 j，(1) [[计算]]原始 [[袋外误差（Out-of-Bag Error）|OOB 误差]] E；(2) 随机打乱特征 j 的值以破坏其信息；(3) [[计算]]打乱后的 [[袋外误差（Out-of-Bag Error）|OOB 误差]] E'；(4) 重要性(j) = E' - E。误差增量越大，说明该特征越重要。
2. **与基尼重要性的对比**：[[随机森林]]提供两种特征重要性方法。基尼重要性（Mean Decrease Impurity）累计所有树中以该特征为分裂点时降低的基尼不纯度之和——[[计算]]快速但对高基数特征有偏。排列重要性更可靠，因为它直接测量特征对预测性能的实际影响。
3. **直观解释**：如果打乱某特征后模型误差显著增加，说明模型高度依赖该特征进行预测；如果误差几乎不变，说明该特征对预测贡献微弱。这种方法不依赖模型内部结构，可推广到任意黑盒模型。
4. **应用价值**：支持特征选择、模型可解释性分析和业务洞察。在表格数据任务中，特征重要性是 [[随机森林（Random Forests）]] 相比深度学习模型的主要优势之一。

## 来源
- [Breiman, L. (2001). Random forests. Machine learning, 45(1), 5–32.] — 提出排列重要性作为随机森林的特征评估方法

## 相关
- [[随机森林（Random Forests）]] — uses
- [[袋外误差（Out-of-Bag Error）]] — depends_on
- [[基尼重要性（Mean Decrease Impurity）]] — compares_to
