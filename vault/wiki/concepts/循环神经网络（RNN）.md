---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模"]
aliases: ["Recurrent Neural Network", "RNN", "循环网络"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: extends
    confidence: 0.95
  - target: "[[梯度消失]]"
    type: caused
    confidence: 0.9
  - target: "[[反向传播]]"
    type: uses
    confidence: 0.9
supersedes: null
---

# 循环神经网络（RNN）

## 概述 (50-200字符)
一类处理序列数据的神经网络架构，通过隐藏状态的递归传递实现对时间依赖的建模。标准 RNN 存在[[梯度消失]]问题，无法学习长期依赖，后被 LSTM 和 [[Transformer 架构|Transformer]] 逐步替代。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心递推公式**：标准 RNN 的隐藏状态更新为 hₜ = tanh(Wₕ · hₜ₋₁ + Wₓ · xₜ + b)，每个时间步共享权重[[矩阵]] Wₕ 和 Wₓ，理论上可以处理任意长度的序列。
2. **[[梯度消失]]根源**：训练时使用 BPTT（通过时间的[[反向传播]]），梯度从 t=T 传回 t=1 需要连乘：∂L/∂h₁ = ∂L/∂hₜ · ∏ₜ'₌₂ᵀ (Wₕᵀ · diag(tanh'(·)))。由于 tanh'(x) ∈ (0, 1)，连乘 T 次后梯度指数级衰减至 ≈ 0，导致网络无法学习超过 10 步的长期依赖。
3. **实际后果**：标准 RNN 几乎无法记住"10 步以前发生的事"，序列建模能力严重受限。这一问题由 [[Sepp Hochreiter]] 在 1991 年硕士论文中首次系统分析。
4. **演进路径**：RNN → [[LSTM（长短期记忆网络）]]（1997，[[门控机制（Gating Mechanism）|门控]]解决[[梯度消失]]）→ [[双向 LSTM（Bi-LSTM）]]（2005）→ Encoder-Decoder + Attention（2014-2015）→ [[Transformer架构]]（2017，彻底替代 RNN）。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter & Schmidhuber (1997) 对 RNN 梯度问题的系统分析
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — RNN 梯度消失的数学推导

## 相关
- [[LSTM（长短期记忆网络）]] — extends（解决 RNN 梯度消失）
- [[梯度消失]] — caused（RNN 的固有缺陷）
- [[反向传播]] — uses（BPTT 训练算法）
- [[Transformer架构]] — supersedes（最终替代 RNN）
