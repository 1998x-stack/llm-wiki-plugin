---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", "深度学习", 时间序列]
aliases: ["Backpropagation", "反向传播算法", "误差反向传播"]
relates_to:
  - target: "[[McCulloch-Pitts 神经元模型]]"
    type: extends
    confidence: 0.9
  - target: "[[LSTM（长短期记忆网络）]]"
    type: extends
    confidence: 0.85
  - target: "[[Transformer架构]]"
    type: extends
    confidence: 0.75
supersedes: null
---

# 反向传播（Backpropagation）

## 概述
Rumelhart、Hinton 和 Williams 于 1986 年在 *Nature* 发表论文，系统展示了反向传播算法如何通过链式法则将输出误差逆向传播到隐藏层，使多层神经网络能够自动学习有用的内部表示，解决了困扰 AI 领域十余年的"信用分配问题"。

## 关键内容

1. **历史背景**：1969 年 Minsky-Papert《感知器》证明单层感知器无法解决 XOR 问题，导致神经网络研究陷入"AI 寒冬"。出路是添加隐藏层，但如何训练隐藏层成为核心难题。

2. **信用分配问题**：当系统整体犯错时，如何将责任分配给每个组件？输出层误差可直接计算，但隐藏层没有"期望输出"可供参考。

3. **核心算法**：通过链式法则逐层计算复合函数导数，将误差从输出层逆向传播到每个隐藏层神经元，实现梯度下降优化。

4. **历史优先权**：Werbos（1974 博士论文）最早提出，Linnainmaa（1970）描述自动微分反向模式，Parker（1985）独立再发现。但 Rumelhart 等人的论文通过令人信服的实验展示了隐藏层自动学习有意义内部表示的能力。

5. **范式意义**：标志着连接主义对符号主义的强势回归，证明了多层网络的理论和实践可行性。

## 来源
- [[17-rumelhart-backpropagation]] — 反向传播学习表示

## 相关
- [[McCulloch-Pitts 神经元模型]] — extends
- [[LSTM（长短期记忆网络）]] — extends
- [[Transformer架构]] — extends
