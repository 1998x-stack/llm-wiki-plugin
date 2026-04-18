---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "神经网络"]
aliases: ["Perceptron", "感知器", "Rosenblatt Perceptron"]
relates_to:
  - target: "[[Frank Rosenblatt]]"
    type: implements
    confidence: 1.0
  - target: "[[McCulloch-Pitts 神经元模型]]"
    type: extends
    confidence: 0.9
  - target: "[[感知机学习规则]]"
    type: implements
    confidence: 1.0
  - target: "[[感知机收敛定理]]"
    type: implements
    confidence: 1.0
  - target: "[[XOR 问题]]"
    type: contradicts
    confidence: 0.8
  - target: "[[多层感知机（MLP）]]"
    type: supersedes
    confidence: 0.85
  - target: "[[反向传播（Backpropagation）]]"
    type: extends
    confidence: 0.7
supersedes: null
---

# 感知机（Perceptron）

## 概述
[[Frank Rosenblatt]] 于 1958 年提出的人工神经网络基本单元，数学表达为 ŷ = sign(w · x + b)，在特征空间中寻找超平面将两类样本线性分开，是深度学习的直接起源。

## 关键内容

1. **核心结构**：感知机对单个神经元做最简洁的数学抽象——输入特征向量 x 与权重向量 w 做加权求和，加上偏置 b，再通过符号函数 sign(·) 输出二分类结果 ŷ ∈ {-1, +1}。几何上是在特征空间中寻找一个超平面（2D 中是直线）将两类样本分开。

2. **[[感知机学习规则]]**：权重通过错误自动修正——初始化 w=0, b=0，对每个样本 (xᵢ, yᵢ)，若预测 ŷ ≠ yᵢ 则更新 w ← w + η · yᵢ · xᵢ，b ← b + η · yᵢ。直觉类比：考试做错题老师纠正你——错了就改，对了维持不动。

3. **收敛定理**：Rosenblatt 严格证明若训练数据线性可分，感知机学习算法在有限步内必然收敛。收敛步数上界 T ≤ (R/γ)²，其中 R 为样本最大范数，γ 为最近点到决策边界的距离。数据越"容易分"（γ 越大），收敛越快。

4. **致命局限——[[XOR 问题]]**：1969 年 Minsky 和 Papert 在《[[Perceptrons (Minsky & Papert 1969)]]》中证明，单层感知机无法解决线性不可分问题，如 XOR（异或）。这直接导致神经网络研究进入长达十余年的[[AI 寒冬]]。

5. **演化路径**：感知机（1958）→ 加隐藏层+非线性激活 → [[多层感知机（MLP）]]（1980s）→ +[[反向传播（Backpropagation）]]+更深的层 → 深度神经网络（2000s+）→ 现代大模型（GPT、Claude、BERT）。现代神经网络每个神经元本质上都是感知机，只是用更平滑的非线性激活替代了 sign 函数。

## 来源
- [[01_perceptron_1958]] — 感知机原始论文解读

## 相关
- [[Frank Rosenblatt]] — implements
- [[McCulloch-Pitts 神经元模型]] — extends
- [[感知机学习规则]] — implements
- [[感知机收敛定理]] — implements
- [[XOR 问题]] — contradicts
- [[多层感知机（MLP）]] — supersedes
- [[反向传播（Backpropagation）]] — extends
