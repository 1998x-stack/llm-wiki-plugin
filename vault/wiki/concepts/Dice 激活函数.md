---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 深度学习, 激活函数, 训练技巧, DIN]
aliases: [Dice, Data Adaptive Activation Function]
relates_to:
  - {target: DIN, type: part_of}
  - {target: PReLU, type: extends}
  - {target: Batch Normalization, type: depends_on}
supersedes: null
---

# Dice 激活函数

## 概述
DIN 论文提出的数据自适应激活函数，通过引入输入统计量将分界点从固定的零移动到数据分布中心，可视为 PReLU 的泛化。

## 关键内容

1. **核心公式** — $\text{Dice}(s) = p(s) \cdot s + (1 - p(s)) \cdot \alpha \cdot s$，其中 $p(s) = \frac{1}{1 + e^{-\frac{s - E(s)}{\sqrt{\text{Var}(s) + \epsilon}}}}$ 是 Sigmoid 控制函数。
2. **数据自适应分界点** — 传统 ReLU/PReLU 的分界点固定在零，Dice 通过引入输入均值 $E(s)$ 和方差 $\text{Var}(s)$，使分界点自适应到数据分布中心，适应每一层不同的输入分布。
3. **平滑过渡** — 用 Sigmoid 函数替代 ReLU 的阶跃函数，在分界点附近实现平滑过渡，避免梯度突变。
4. **BN 的隐式作用** — 公式中的标准化项 $(s - E(s)) / \sqrt{\text{Var}(s) + \epsilon}$ 本质上就是 [[Batch Normalization]] 操作，使 Dice 天然具有缓解 Internal Covariate Shift 的能力。
5. **与 PReLU 的退化关系** — 当 $E(s) = 0$ 且 $\text{Var}(s) = 0$ 时，Dice 退化为 PReLU，因此 Dice 是 PReLU 的泛化形式。
6. **训练与推理** — 训练阶段使用当前 mini-batch 的统计量计算 $E(s)$ 和 $\text{Var}(s)$；推理阶段使用训练过程中的指数移动平均值，与 BN 的处理方式一致。
7. **实验效果** — 在阿里巴巴工业数据集上，Dice 相比 PReLU 带来 +0.0015 的绝对 AUC 提升。

## 来源
- [raw/books/推荐系统/11-din.md](raw/books/推荐系统/11-din.md)

## 相关
- DIN — Dice 激活函数的提出者
- [[PReLU]] — Dice 的特例形式
- [[Batch Normalization]] — Dice 隐式包含的标准化操作
- [[Mini-batch Aware Regularization]] — DIN 论文提出的另一项训练技巧
