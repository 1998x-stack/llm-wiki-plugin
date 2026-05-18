---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模"]
aliases: ["Gating Mechanism", "门控", "门控设计"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: implements
    confidence: 0.95
  - target: "[[遗忘门（Forget Gate）]]"
    type: part_of
    confidence: 0.95
  - target: "[[输入门（Input Gate）]]"
    type: part_of
    confidence: 0.95
  - target: "[[输出门（Output Gate）]]"
    type: part_of
    confidence: 0.95
supersedes: null
---

# 门控机制（Gating Mechanism）

## 概述 (50-200字符)
通过 sigmoid 门控信号（∈[0,1]）精确控制信息流动的神经网络设计模式。LSTM 首次系统应用，包含[[遗忘门（Forget Gate）|遗忘门]]、[[输入门（Input Gate）|输入门]]、[[输出门（Output Gate）|输出门]]，解决 RNN [[梯度消失]]问题，成为序列建模标准[[规范化理论|范式]]。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心思想**：[[门控机制]]使用 [[Sigmoid激活函数]] 产生 [0, 1] 范围的控制信号，通过逐元素乘法（⊙）调节信息流的通过比例。0 表示完全阻断，1 表示完全通过，实现精确的"软开关"控制。
2. **LSTM 三門体系**：[[遗忘门（Forget Gate）]]（fₜ = σ(Wf·[hₜ₋₁, xₜ] + bf)）决定丢弃什么；[[输入门（Input Gate）]]（iₜ 控制更新量，C̃ₜ 为候选值）决定写入什么；[[输出门（Output Gate）]]（oₜ = σ(Wo·[hₜ₋₁, xₜ] + bo)）决定输出什么。三者共同调控 [[细胞状态（Cell State）]]。
3. **解决[[梯度消失]]**：[[门控机制]]使 LSTM 的[[细胞状态（Cell State）|细胞状态]]梯度 ∂Cₜ/∂Cₜ₋₁ = fₜ，当[[遗忘门（Forget Gate）|遗忘门]]接近 1 时梯度无损传递。对比标准 [[循环神经网络（RNN）]] 需要连乘小于 1 的数导致指数衰减，门控设计从根本上解决了 [[梯度消失]] 问题。
4. **历史影响**：门控设计成为序列建模的标准[[规范化理论|范式]]，后续 GRU（[[GRU|门控循环单元]]）、Attention 机制等都受到门控思想的影响。Hochreiter & Schmidhuber (1997) 的门控设计被评为 ⭐⭐⭐⭐⭐ 的历史贡献。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter & Schmidhuber (1997) 首次系统应用门控机制
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — 门控机制的数学公式与直觉解释

## 相关
- [[LSTM（长短期记忆网络）]] — implements（LSTM 的核心设计）
- [[遗忘门（Forget Gate）]] — part_of（门控组件之一）
- [[输入门（Input Gate）]] — part_of（门控组件之一）
- [[输出门（Output Gate）]] — part_of（门控组件之一）
- [[细胞状态（Cell State）]] — relates_to（门控调控的对象）
- [[Sigmoid激活函数]] — uses（门控信号的生成函数）
- [[梯度消失]] — relates_to（门控解决的核心问题）
