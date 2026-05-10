---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [neural networks, associative memory, energy-based models]
aliases: ["Hopfield Network", "霍普菲尔德网络", "Hopfield 网络"]
relates_to:
  - target: "[[McCulloch-Pitts 神经元模型]]"
    type: builds_on
  - target: "[[Associative Memory]]"
    type: implements
  - target: "[[Energy-based Models]]"
    type: related_to
  - target: "[[Recurrent Neural Networks]]"
    type: part_of
supersedes: null
---

# Hopfield Network

## 概述
[[John Hopfield|Hopfield]] 网络是一种递归神经网络，由 [[John Hopfield]] 在 1982 年提出，用于模拟联想记忆功能。

## 关键内容

1. **基本原理**：[[John Hopfield|Hopfield]] 网络是一种单层全连接的反馈网络，每个神经元都与其他所有神经元相连，具有对称权重（Wij = Wji）。

2. **能量函数**：网络的状态变化遵循能量函数下降的原则，确保网络最终收敛到局部最小值，这些最小值对应于存储的记忆模式。

3. **联想记忆**：给定部分或有噪声的输入模式，网络能够恢复完整的存储模式，表现出强大的联想记忆能力。

## 来源
- [[ai_papers_timeline.md]] — 神经网络发展历史
- [[Neural Networks and Learning Machines]] — 3rd Edition

## 相关
- [[McCulloch-Pitts 神经元模型]] — builds_on
- [[Associative Memory]] — implements
- [[Energy-based Models]] — related_to
- [[Recurrent Neural Networks]] — part_of