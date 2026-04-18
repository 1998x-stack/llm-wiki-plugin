---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 正则化, 深度学习, 训练技巧, DIN]
aliases: [Mini-batch Aware Regularization, MBAR]
relates_to:
  - {target: DIN, type: part_of}
  - {target: L2 正则化, type: extends}
  - {target: Dropout, type: compares_to}
supersedes: null
---

# Mini-batch Aware Regularization

## 概述
DIN 提出的频次感知正则化方法，只对当前 mini-batch 中出现的特征计算正则项，低频特征获得更强约束。

## 关键内容

1. **问题背景** — [[CTR 预估]]模型中特征稀疏性导致[[过拟合（Overfitting）|过拟合]]。商品 ID 特征维度达数亿，大部分商品出现频次极低。标准 L2 正则化需在每次梯度更新时计算所有参数的正则项，计算量过于庞大。
2. **核心公式** — $L_{\text{reg}} = \sum_{j=1}^{K} \sum_{m=1}^{B} \frac{\alpha_{mj}}{n_j} \| w_j \|^2$，其中 $n_j$ 是特征 $j$ 在整个训练集中的出现频次。
3. **频次感知** — 出现频次低的特征获得更强的正则化约束（因为 $n_j$ 小），出现频次高的特征获得较弱的约束。直觉是：高频特征有充足训练样本学习可靠 [[Embedding]]，低频特征容易[[过拟合（Overfitting）|过拟合]]到少量样本上。
4. **计算效率** — 只对当前 mini-batch 中实际出现的特征计算正则项，避免了对未出现特征的无效计算，在数亿参数规模下显著降低计算开销。
5. **实验效果** — 不使用正则化的模型在第一个 epoch 后就严重[[过拟合（Overfitting）|过拟合]]。[[Dropout]] 能缓解[[过拟合（Overfitting）|过拟合]]但收敛较慢。Mini-batch Aware Regularization 在防止[[过拟合（Overfitting）|过拟合]]和加速收敛之间取得最佳平衡，带来 +0.0031 的绝对 AUC 提升。
6. **后续影响** — "只关注当前 batch 中出现的特征"的思路后来被广泛应用于各种大规模稀疏模型的训练中。

## 来源
- [raw/books/推荐系统/11-din.md](raw/books/推荐系统/11-din.md)

## 相关
- DIN — Mini-batch Aware Regularization 的提出者
- [[L2 正则化]] — MBAR 扩展的基础方法
- [[Dropout]] — MBAR 对比的替代方案
- [[Dice 激活函数]] — DIN 论文提出的另一项训练技巧
- [[CTR 预估]] — 应用场景
