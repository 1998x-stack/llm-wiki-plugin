---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "论文"]
aliases: ["The Perceptron Paper", "Rosenblatt 1958", "感知机论文"]
relates_to:
  - target: "[[Frank Rosenblatt]]"
    type: implements
    confidence: 1.0
  - target: "[[感知机（Perceptron）]]"
    type: implements
    confidence: 1.0
  - target: "[[Perceptrons (Minsky & Papert 1969)]]"
    type: contradicts
    confidence: 0.8
supersedes: null
---

# The Perceptron (1958 论文)

## 概述
Rosenblatt 于 1958 年在 *Psychological Review* 发表的奠基性论文，首次提出感知机作为信息存储和组织在大脑中的概率模型，开创了可学习机器的先河。

## 关键内容

1. **论文信息**：Rosenblatt, F. (1958). "The [[感知机（Perceptron）|Perceptron]]: A Probabilistic Model for Information Storage and Organization in the Brain." *Psychological Review*, 65(6), 386.

2. **核心贡献**：提出感知机数学模型 ŷ = sign(w · x + b)，将单个神经元做最简洁的数学抽象，在特征空间中寻找超平面将两类样本分开。

3. **[[感知机学习规则]]**：首次提出权重通过错误自动修正的算法：w ← w + η · yᵢ · xᵢ，这是机器学习史上第一个自动学习算法。

4. **收敛定理**：严格证明若训练数据线性可分，感知机在有限步内必然收敛，更新次数上界为 T ≤ (R/γ)²。

5. **历史地位**：被誉为第一个可学习的人工神经网络，是现代深度学习的直接起源。

## 来源
- [[01_perceptron_1958]] — 感知机原始论文解读

## 相关
- [[Frank Rosenblatt]] — implements
- [[感知机（Perceptron）]] — implements
- [[Perceptrons (Minsky & Papert 1969)]] — contradicts
