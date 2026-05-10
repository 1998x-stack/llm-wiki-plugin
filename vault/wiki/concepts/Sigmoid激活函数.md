---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["机器学习", "深度学习", "激活函数"]
aliases: ["Sigmoid Function", "Logistic Function", "S型函数", "Logistic函数"]
relates_to:
  - target: "[[反向传播（Backpropagation）]]"
    type: uses
    confidence: 0.95
  - target: "[[Learning Representations by Back-propagating Errors (1986 论文)]]"
    type: used_in
    confidence: 0.9
  - target: "[[梯度消失]]"
    type: causes
    confidence: 0.85
  - target: "[[ReLU激活函数]]"
    type: supersedes
    confidence: 0.8
  - target: "[[链式法则]]"
    type: uses
    confidence: 0.9
supersedes: null
---

# Sigmoid激活函数

## 概述 (50-200字符)
Sigmoid 函数 σ(x) = 1/(1+e⁻ˣ) 将任意实数映射到 (0,1) 区间，是神经网络中最经典的激活函数。其导数形式优雅 σ'(x) = σ(x)(1-σ(x))，但最大值仅 0.25，深层网络中多层相乘导致[[梯度消失]]。该函数是1986年[[Learning Representations by Back-propagating Errors (1986 论文)]]中推荐使用的激活函数。

## 关键内容 (≥300字符, 用[[双链]])
1. **数学定义与性质**：σ(x) = 1/(1+e⁻ˣ)，输出范围 (0,1)，单调递增，关于原点对称 σ(0)=0.5。导数 σ'(x) = σ(x)·(1-σ(x)) 可用函数自身表示，[[计算]]高效。这一优雅性质使其成为[[反向传播]]论文（Rumelhart et al., 1986）中的原始激活选择。

2. **在[[反向传播]]中的角色**：[[反向传播]]需要[[计算]]每层的局部梯度，Sigmoid 的导数可直接由前向传播的输出值[[计算]]（无需额外存储输入），节省了内存和[[计算]]。在两层网络演示中，隐藏层梯度 ∂L/∂z₁ = ∂L/∂h ⊙ σ'(z₁)。

3. **[[梯度消失]]问题**：σ'(x) 最大值仅为 0.25（在 x=0 处），当 |x| 增大时导数趋近于 0。在 n 层网络中，梯度连乘 0.25ⁿ → 0，导致深层网络训练极慢甚至无法训练。这是 Sigmoid 被淘汰的根本原因。

4. **被 ReLU 取代**：2012 年 [[AlexNet]] 使用[[ReLU激活函数]] f(x) = max(0, x)，正区间导数恒为 1，彻底解决了[[梯度消失]]问题。ReLU [[计算]]更简单（无需指数运算），收敛速度显著快于 Sigmoid，成为现代深度学习的默认激活函数。

5. **历史意义**：1986年[[Learning Representations by Back-propagating Errors (1986 论文)]]选择了Sigmoid作为推荐的激活函数，因为它具有处处可导的优点，适合梯度[[计算]]。虽然该选择为后续[[梯度消失]]问题埋下隐患，但在当时是合理的，因为解决了单层[[感知机]]无法处理非线性问题的局限性。

## 来源
- [Learning Representations by Back-propagating Errors] — Rumelhart, Hinton & Williams, Nature 1986
- [[raw/articles/ai-papers/foundations/paper_02_backpropagation.md]] — 源文件
- [[ai_papers_timeline.md]] — 1986年时间线条目

## 相关
- [[反向传播（Backpropagation）]] — uses
- [[Learning Representations by Back-propagating Errors (1986 论文)]] — used_in
- [[梯度消失]] — caused
- [[ReLU激活函数]] — supersedes
- [[链式法则]] — uses
