---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模"]
aliases: ["Input Gate", "输入门"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: part_of
    confidence: 0.95
  - target: "[[细胞状态（Cell State）]]"
    type: relates_to
    confidence: 0.95
supersedes: null
---

# 输入门（Input Gate）

## 概述 (50-200字符)
LSTM 三个门之一，决定将什么新信息写入[[细胞状态（Cell State）|细胞状态]]。由 iₜ（控制更新量，∈[0,1]）和 C̃ₜ（候选新信息，∈[-1,1]）组成，与[[遗忘门（Forget Gate）|遗忘门]]协作完成[[细胞状态（Cell State）|细胞状态]]的精确更新。

## 关键内容 (≥300字符, 用[[双链]])
1. **数学公式**：iₜ = σ(Wi · [hₜ₋₁, xₜ] + bi)，控制更新量 [0, 1]；C̃ₜ = tanh(Wc · [hₜ₋₁, xₜ] + bc)，候选新信息 [-1, 1]。两个子组件分别使用 [[Sigmoid激活函数]] 和 tanh 激活函数。
2. **功能直觉**：[[输入门]]决定哪些新信息应该被写入 [[细胞状态（Cell State）]]。在[[Language-Model|语言模型]]中，遇到"小明"时[[输入门]]会写入主语信息；遇到"他"时保留"他=小明"的关联。iₜ 接近 1 时大量写入新信息，接近 0 时阻止写入。
3. **[[细胞状态（Cell State）|细胞状态]]更新**：[[输入门]]与 [[遗忘门（Forget Gate）]] 协作：Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ。[[遗忘门（Forget Gate）|遗忘门]]控制"擦除旧信息"，输入[[门控机制（Gating Mechanism）|门控]]制"写入新信息"，两者共同实现[[细胞状态（Cell State）|细胞状态]]的精确调控。
4. **候选值 C̃ₜ**：使用 tanh 而非 sigmoid 生成候选值，输出范围 [-1, 1]，允许[[细胞状态（Cell State）|细胞状态]]存储正负两种方向的信息，增强了表达能力。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter & Schmidhuber (1997) 提出输入门概念
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — 输入门的数学公式与语言学直觉

## 相关
- [[LSTM（长短期记忆网络）]] — part_of（LSTM 的核心组件）
- [[细胞状态（Cell State）]] — relates_to（控制细胞状态的更新）
- [[遗忘门（Forget Gate）]] — relates_to（协作更新细胞状态）
- [[Sigmoid激活函数]] — uses（iₜ 的激活函数）
- [[输出门（Output Gate）]] — relates_to（LSTM 三門之一）
