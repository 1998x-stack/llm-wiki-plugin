---
type: concept
status: active
confidence: 0.90
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "探索", "神经网络", "DQN"]
aliases: ["NoisyNet", "噪声网络", "NoisyLinear", "参数化噪声探索"]
relates_to:
  - target: "DQN"
    type: extends
    confidence: 0.92
  - target: "[[强化学习]]"
    type: part_of
    confidence: 0.88
  - target: "[[Rainbow]]"
    type: part_of
    confidence: 0.95
supersedes: null
---

# NoisyNets

## 概述
NoisyNets（Fortunato et al., 2017）将探索机制内嵌进神经网络参数中，用可学习的参数化噪声替代 ε-greedy 探索。NoisyLinear 层在权重和偏置中引入均值 μ 和噪声尺度 σ（均为可学习参数），噪声尺度随训练自适应调整，实现状态相关的探索，是[[Rainbow]]的组件之一。

## 关键内容

1. **问题**：ε-greedy 探索噪声固定，与状态和训练进度无关，且需要人工设计 ε 衰减计划，无法自适应不同状态的探索需求。

2. **NoisyLinear 层**：标准层 `y = Wx + b` 替换为 `y = (μ_W + σ_W ⊙ ε_W)x + (μ_b + σ_b ⊙ ε_b)`，其中 μ、σ 均为可学习参数，ε 在每次前向传播时随机采样。

3. **因子化噪声（Factorised Noise）**：`ε_W(i,j) = f(ε_i)·f(ε_j)`，`f(x) = sgn(x)·√|x|`。对 p×q 权重[[矩阵]]只需采样 p+q 个噪声，大幅减少随机数开销。

4. **自适应探索**：σ 随训练自动收敛——探索有价值的状态时 σ 保持大，探索无用的状态时 σ 自动缩小，无需手动调 ε 衰减。

5. **实现**：完全替代 ε-greedy，在 [[Rainbow]] 中用于 FC 层（不替换卷积层），推断时噪声固定（使用均值）。

6. **消融结果**：在 [[Rainbow]] 消融中移除 NoisyNets 造成中等程度下降，重要性排第四，显示探索质量对整体性能的影响。

## 来源
- [[rl_03_rainbow]] — Rainbow: Combining Improvements in Deep Reinforcement Learning (arXiv:1710.02298, AAAI 2018)，含 NoisyNets 在 Rainbow 中集成的详细说明

## 相关
- DQN — extends
- [[强化学习]] — part_of
- [[Rainbow]] — part_of
