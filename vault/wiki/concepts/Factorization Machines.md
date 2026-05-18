---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 特征工程, 因子分解机, CTR预估]
aliases: [Factorization Machines, FM, 因子分解机]
relates_to:
  - {target: 矩阵分解, type: extends}
  - {target: BPR, type: relates_to}
  - {target: 隐式反馈, type: relates_to}
  - {target: SVM, type: improves_over}
  - {target: SVD++, type: compares_to}
  - {target: PITF, type: compares_to}
  - {target: FPMC, type: compares_to}
  - {target: libFM, type: implementation}
  - {target: DeepFM, type: predecessor_to}
  - {target: FFM, type: predecessor_to}
supersedes: null
---

# Factorization Machines

## 概述
一种通过[[嵌入表示|隐向量]]内积建模特征间二阶交互的通用预测模型，由 [[Steffen Rendle]] 提出，可视为[[矩阵分解]]在更广泛特征空间上的推广。FM 解决了SVM在稀疏数据下失效、[[矩阵分解]]不够通用的两个痛点，通过一个统一公式兼容多种分解模型。

## 关键内容

1. **提出背景**：[[Steffen Rendle]]（BPR 第一作者）在 BPR 之后的工作中提出了 Factorization Machines，将[[矩阵分解]]的思想推广到任意实值特征向量，而不仅限于用户-物品交互[[矩阵]]。FM 旨在统一[[矩阵分解]]、[[SVD++]]、PITF 等专用分解模型的表达能力。

2. **模型公式**：FM(x) = w₀ + Σ_i w_i x_i + Σ_i Σ_j>i ⟨v_i, v_j⟩ x_i x_j，其中 w₀ 为全局偏置，w_i 为一阶权重，v_i 为特征 i 的[[嵌入表示|隐向量]]，通过[[嵌入表示|隐向量]]内积 ⟨v_i, v_j⟩ 建模特征对的交互。这种参数分解方式使模型在稀疏数据下也能有效学习[[特征交叉|特征交互]]。

3. **与[[矩阵分解]]的关系**：当输入特征仅为用户 one-hot 和物品 one-hot 时，FM 退化为标准的[[矩阵分解]]模型。FM 可处理额外的上下文特征（如时间、地点、物品属性等），比传统[[矩阵分解]]更具通用性。

4. **[[计算]]效率**：FM 的二阶交互项可通过代数变换从 O(n²) 优化到 O(nk) [[计算]]复杂度，其中 n 为特征数量，k 为[[嵌入表示|隐向量]]维度，使得 FM 在高维稀疏特征空间上高效运行。在稀疏场景下，实际复杂度为 O(kn̄)，n̄ 为非零特征数。

5. **稀疏数据友好**：FM 通过参数分解（将 w_ij 分解为 ⟨v_i, v_j⟩）引入参数间的依赖关系，使每个参数可以从全局数据中学习，而非仅依赖于直接相关的样本，解决了SVM在稀疏场景下的失败问题。

6. **统一框架**：FM 可通过不同特征编码方式等价表示[[矩阵分解]]、[[SVD++]]、PITF等多种专用分解模型，提供了一个通用预测框架，使用户无需理解各种分解模型的细节即可应用。

7. **后续发展**：[[DeepFM]] 等深度推荐模型将 FM 与深度神经网络结合，FM 部分负责低阶[[特征交叉|特征交互]]，DNN 部分负责高阶[[特征交叉|特征交互]]，两者共享输入[[嵌入表示|嵌入层]]。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, Steffen Rendle 后续工作提及
- [[推荐系统/06-factorization-machines.md]] — Factorization Machines 论文深度解读

## 相关
- [[矩阵分解]] — extends
- BPR — relates_to
- [[隐式反馈]] — relates_to
- [[SVM]] — improves_over
- [[SVD++]] — compares_to
- [[PITF]] — compares_to
- [[FPMC]] — compares_to
- [[libFM]] — implementation
- [[DeepFM]] — predecessor_to
- [[FFM]] — predecessor_to
