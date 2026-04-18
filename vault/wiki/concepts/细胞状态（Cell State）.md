---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模"]
aliases: ["Cell State", "细胞状态", "记忆细胞"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: part_of
    confidence: 0.95
  - target: "[[遗忘门（Forget Gate）]]"
    type: relates_to
    confidence: 0.95
  - target: "[[输入门（Input Gate）]]"
    type: relates_to
    confidence: 0.95
supersedes: null
---

# 细胞状态（Cell State）

## 概述 (50-200字符)
LSTM 的核心创新，一条贯穿整个序列的"信息高速公路"，通过加法更新（Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ）保证梯度无损传递，从根本上解决[[梯度消失]]问题。

## 关键内容 (≥300字符, 用[[双链]])
1. **设计原理**：细胞状态 Cₜ 是 LSTM 中区别于隐藏状态 hₜ 的另一条信息流，它贯穿整个序列，像一本可以精确"写入"、"擦除"、"读取"的日记本。对比标准 RNN 像用粉笔写黑板（每次更新覆盖之前内容），细胞状态允许信息长期保留。
2. **更新机制**：Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ，其中 [[遗忘门（Forget Gate）]] fₜ 决定从旧状态中保留多少（f=0 完全遗忘，f=1 完全保留），[[输入门（Input Gate）]] iₜ 控制新候选值 C̃ₜ = tanh(Wc·[hₜ₋₁, xₜ] + bc) 的写入量。
3. **梯度传播**：细胞状态的梯度 ∂Cₜ/∂Cₜ₋₁ = fₜ，当[[遗忘门（Forget Gate）|遗忘门]]接近 1 时，梯度通过加法直接传递而不衰减。这是 LSTM 解决 [[梯度消失]] 的数学本质——对比 RNN 需要乘以 Wₕᵀ · diag(tanh'(·))（小于 1 的数连乘导致指数衰减）。
4. **输出控制**：细胞状态不直接输出，而是通过 [[输出门（Output Gate）]] 过滤：hₜ = oₜ ⊙ tanh(Cₜ)，决定当前时刻暴露什么信息给外部。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter & Schmidhuber (1997) 提出细胞状态概念
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — 细胞状态的数学推导与直觉解释

## 相关
- [[LSTM（长短期记忆网络）]] — part_of（LSTM 的核心组件）
- [[遗忘门（Forget Gate）]] — relates_to（控制细胞状态的遗忘）
- [[输入门（Input Gate）]] — relates_to（控制细胞状态的更新）
- [[输出门（Output Gate）]] — relates_to（控制细胞状态的输出）
- [[梯度消失]] — relates_to（细胞状态解决的核心问题）
