---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模"]
aliases: ["Forget Gate", "遗忘门"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: part_of
    confidence: 0.95
  - target: "[[细胞状态（Cell State）]]"
    type: relates_to
    confidence: 0.95
supersedes: null
---

# 遗忘门（Forget Gate）

## 概述 (50-200字符)
LSTM 三个门之一，决定从[[细胞状态（Cell State）|细胞状态]]中丢弃什么信息。输出 fₜ ∈ [0, 1]，f=0 完全遗忘，f=1 完全保留。是 LSTM 解决[[梯度消失]]的关键——当 fₜ ≈ 1 时梯度无损传递。

## 关键内容 (≥300字符, 用[[双链]])
1. **数学公式**：fₜ = σ(Wf · [hₜ₋₁, xₜ] + bf)，其中 σ 为 [[Sigmoid激活函数]]，输出范围 [0, 1]。输入为上一时刻隐藏状态 hₜ₋₁ 和当前输入 xₜ 的拼接。
2. **功能直觉**：遗忘[[门控机制（Gating Mechanism）|门控]]制 [[细胞状态（Cell State）]] 中旧信息的保留比例。f=0 时完全清空[[细胞状态（Cell State）|细胞状态]]（擦除），f=1 时原封不动传递（保留）。在[[Language-Model|语言模型]]中，遇到句号时[[遗忘门]]可能清除上一句的主语信息。
3. **梯度意义**：[[细胞状态（Cell State）|细胞状态]]的梯度传播 ∂Cₜ/∂Cₜ₋₁ = fₜ。当[[遗忘门]]接近 1 时，梯度通过加法直接传递而不衰减，这是 LSTM 解决 [[梯度消失]] 的核心机制。对比标准 RNN 需要连乘小于 1 的数导致指数衰减。
4. **与[[输入门（Input Gate）|输入门]]协作**：[[遗忘门]]和 [[输入门（Input Gate）]] 共同决定[[细胞状态（Cell State）|细胞状态]]的更新：Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ，一个控制"遗忘旧信息"，一个控制"加入新信息"。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter & Schmidhuber (1997) 提出遗忘门概念
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — 遗忘门的数学公式与语言学直觉

## 相关
- [[LSTM（长短期记忆网络）]] — part_of（LSTM 的核心组件）
- [[细胞状态（Cell State）]] — relates_to（控制细胞状态的遗忘）
- [[输入门（Input Gate）]] — relates_to（协作更新细胞状态）
- [[Sigmoid激活函数]] — uses（遗忘门的激活函数）
- [[梯度消失]] — relates_to（遗忘门解决的核心问题）
