---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "论文"]
aliases: ["Long Short-Term Memory", "Long short-term memory", "LSTM 1997 论文"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: extends
    confidence: 0.95
  - target: "[[Sepp Hochreiter]]"
    type: relates_to
    confidence: 0.95
  - target: "[[Jürgen Schmidhuber]]"
    type: relates_to
    confidence: 0.95
supersedes: null
---

# Long Short-Term Memory (1997 论文)

## 概述 (50-200字符)
Hochreiter & Schmidhuber 于 1997 年在 Neural Computation 发表的划时代论文，提出 LSTM 架构，通过[[细胞状态（Cell State）|细胞状态]]和[[门控机制（Gating Mechanism）|门控]]机制解决 RNN [[梯度消失]]问题，被引用超过 98,000 次。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题定义**：论文系统分析了标准 [[循环神经网络（RNN）]] 在 BPTT 训练时的[[梯度消失]]问题——梯度从 t=T 传回 t=1 需要连乘权重[[矩阵]]和 tanh'（∈(0,1)），导致指数级衰减，网络无法记住 10 步以前的信息。
2. **核心方案**：提出**[[细胞状态（Cell State）|细胞状态]] Cₜ**作为贯穿序列的"信息高速公路"，配合三个[[门控机制（Gating Mechanism）|门控]]机制：[[遗忘门（Forget Gate）]]（fₜ = σ(Wf·[hₜ₋₁, xₜ] + bf)，决定丢弃什么）、[[输入门（Input Gate）]]（iₜ 控制更新量，C̃ₜ 为候选值）、[[输出门（Output Gate）]]（oₜ 决定输出什么）。[[细胞状态（Cell State）|细胞状态]]更新公式：Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ。
3. **梯度分析**：论文证明了 ∂Cₜ/∂Cₜ₋₁ = fₜ，当[[遗忘门（Forget Gate）|遗忘门]]接近 1 时，梯度通过加法直接传递而不衰减，从根本上解决了 [[梯度消失]] 问题。这一数学分析是 LSTM 设计的理论基础。
4. **历史地位**：该论文成为序列建模领域的里程碑，LSTM 在 1997-2017 年间统治语音识别、机器翻译、[[Time Series Analysis|时间序列]]预测等领域，直到 [[Transformer架构]] 出现才被替代。

## 来源
- Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8), 1735–1780.

## 相关
- [[LSTM（长短期记忆网络）]] — extends（提出架构）
- [[Sepp Hochreiter]] — relates_to（第一作者）
- [[Jürgen Schmidhuber]] — relates_to（第二作者）
- [[梯度消失]] — relates_to（解决的核心问题）
- [[循环神经网络（RNN）]] — compares_to（对比分析）
