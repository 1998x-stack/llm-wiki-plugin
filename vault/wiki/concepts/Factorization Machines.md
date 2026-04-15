---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 特征工程, 因子分解机]
aliases: [Factorization Machines, FM]
relates_to:
  - {target: 矩阵分解, type: extends}
  - {target: BPR, type: relates_to}
  - {target: 隐式反馈, type: relates_to}
supersedes: null
---

# Factorization Machines

## 概述
一种通过[[嵌入表示|隐向量]]内积建模特征间二阶交互的通用预测模型，由 [[Steffen Rendle]] 提出，可视为[[矩阵分解]]在更广泛特征空间上的推广。

## 关键内容

1. **提出背景**：[[Steffen Rendle]]（[[BPR]] 第一作者）在 [[BPR]] 之后的工作中提出了 Factorization Machines，将[[矩阵分解]]的思想推广到任意实值特征向量，而不仅限于用户-物品交互[[矩阵]]。

2. **模型公式**：F[[Solomonoff先验|M(x)]] = w₀ + Σ_i w_i x_i + Σ_i Σ_j>i ⟨v_i, v_j⟩ x_i x_j，其中 w₀ 为全局偏置，w_i 为一阶权重，v_i 为特征 i 的[[嵌入表示|隐向量]]，通过[[嵌入表示|隐向量]]内积 ⟨v_i, v_j⟩ 建模特征对的交互。

3. **与[[矩阵分解]]的关系**：当输入特征仅为用户 one-hot 和物品 one-hot 时，FM 退化为标准的[[矩阵分解]]模型。FM 可处理额外的上下文特征（如时间、地点、物品属性等）。

4. **计算效率**：FM 的二阶交互项可通过代数变换从 O(n²) 优化到 O(nk) 计算复杂度，其中 n 为特征数量，k 为[[嵌入表示|隐向量]]维度，使得 FM 在高维稀疏特征空间上高效运行。

5. **后续发展**：[[DeepFM]] 等深度推荐模型将 FM 与深度神经网络结合，FM 部分负责低阶[[特征交叉|特征交互]]，DNN 部分负责高阶[[特征交叉|特征交互]]，两者共享输入[[嵌入表示|嵌入层]]。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, Steffen Rendle 后续工作提及

## 相关
- [[矩阵分解]] — extends
- [[BPR]] — relates_to
- [[隐式反馈]] — relates_to
