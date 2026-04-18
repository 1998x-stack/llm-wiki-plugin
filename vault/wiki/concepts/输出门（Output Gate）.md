---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模"]
aliases: ["Output Gate", "输出门"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: part_of
    confidence: 0.95
  - target: "[[细胞状态（Cell State）]]"
    type: relates_to
    confidence: 0.95
supersedes: null
---

# 输出门（Output Gate）

## 概述 (50-200字符)
LSTM 三个门之一，决定从[[细胞状态（Cell State）|细胞状态]]输出什么信息作为隐藏状态。公式 oₜ = σ(Wo·[hₜ₋₁, xₜ] + bo)，hₜ = oₜ ⊙ tanh(Cₜ)，控制当前时刻对外暴露的信息。

## 关键内容 (≥300字符, 用[[双链]])
1. **数学公式**：oₜ = σ(Wo · [hₜ₋₁, xₜ] + bo)，使用 [[Sigmoid激活函数]] 输出 [0, 1]；hₜ = oₜ ⊙ tanh(Cₜ)，将[[细胞状态（Cell State）|细胞状态]]通过 tanh 压缩后再由输出门过滤。
2. **功能直觉**：输出门决定当前时刻的隐藏状态 hₜ 应该包含 [[细胞状态（Cell State）]] 中的哪些信息。在语言模型中，当需要预测下一个词时，输出门会输出与当前上下文相关的隐藏状态。oₜ 接近 1 时充分暴露[[细胞状态（Cell State）|细胞状态]]信息，接近 0 时隐藏信息。
3. **与[[细胞状态（Cell State）|细胞状态]]的关系**：输出门不修改[[细胞状态（Cell State）|细胞状态]]本身，而是控制[[细胞状态（Cell State）|细胞状态]]的"可见性"。[[细胞状态（Cell State）|细胞状态]] Cₜ 可以存储大量信息，但每个时刻只通过输出门暴露相关部分给外部（hₜ）和下一层网络。
4. **三門协作**：输出门与 [[遗忘门（Forget Gate）]]、[[输入门（Input Gate）]] 共同构成 LSTM 的[[门控机制（Gating Mechanism）|门控]]体系。[[遗忘门（Forget Gate）|遗忘门]]控制"记住什么"，[[输入门（Input Gate）|输入门]]控制"写入什么"，输出[[门控机制（Gating Mechanism）|门控]]制"输出什么"，三者协同实现精确的序列建模。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter & Schmidhuber (1997) 提出输出门概念
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — 输出门的数学公式与语言学直觉

## 相关
- [[LSTM（长短期记忆网络）]] — part_of（LSTM 的核心组件）
- [[细胞状态（Cell State）]] — relates_to（控制细胞状态的输出）
- [[遗忘门（Forget Gate）]] — relates_to（LSTM 三門之一）
- [[输入门（Input Gate）]] — relates_to（LSTM 三門之一）
- [[Sigmoid激活函数]] — uses（输出门的激活函数）
