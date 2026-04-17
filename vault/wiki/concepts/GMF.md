---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 协同过滤, 矩阵分解, NCF]
aliases: [Generalized Matrix Factorization, GMF]
relates_to:
  - {target: Neural Collaborative Filtering, type: part_of}
  - {target: 矩阵分解, type: extends}
  - {target: Embedding, type: uses}
  - {target: NeuMF, type: compares_to}
supersedes: null
---

# GMF

## 概述
广义[[矩阵分解]]，NCF 框架的第一个实例化模型，用可学习的逐元素乘积和权重向量替代传统[[矩阵分解]]的固定内积操作。

## 关键内容

1. **公式定义**：$\hat{y}_{ui} = a_{out}(\mathbf{h}^T (\mathbf{p}_u \odot \mathbf{q}_i))$，其中 $\odot$ 为逐元素乘积（Hadamard product），$\mathbf{h}$ 是可学习的权重向量，$a_{out}$ 是输出激活函数（[[Neural Collaborative Filtering]] 论文中使用 sigmoid）。
2. **与[[矩阵分解]]的关系**：当 $a_{out}$ 为恒等函数、$\mathbf{h}$ 为全1向量时，GMF 恰好退化为标准 MF。这证明了**MF 是 NCF 的一个特例**。GMF 的"广义"体现在：(1) 权重向量 $\mathbf{h}$ 允许不同潜在维度有不同的重要性；(2) 非线性激活函数引入表达能力提升。
3. **在 NCF 中的角色**：GMF 负责捕捉潜在因子之间的线性交互模式（传统 MF 擅长的部分），与 MLP 的非线性建模能力形成互补。
4. **独立嵌入空间**：在最终的 [[NeuMF]] 融合模型中，GMF 使用自己独立的用户/物品嵌入 $\mathbf{p}_u^G, \mathbf{q}_i^G$，不与 MLP 共享，赋予子模型更大的灵活性。
5. **实验表现**：在大多数设置下，GMF 的性能不如 MLP，验证了非线性交互函数优于线性交互函数的假设。但 GMF + MLP 的融合（[[NeuMF]]）持续优于单一模型。

## 来源
- [[10-ncf.md]] — Neural Collaborative Filtering 论文详细解读

## 相关
- [[Neural Collaborative Filtering]] — GMF 所属的通用框架
- [[矩阵分解]] — GMF 扩展的传统方法
- [[NeuMF]] — GMF 与 MLP 的融合模型
- [[Embedding]] — GMF 使用的用户和物品表示
