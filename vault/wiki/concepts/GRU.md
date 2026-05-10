---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [神经网络, 深度学习, 序列建模]
aliases: ["Gated Recurrent Unit", "门控循环单元", "GRU"]
relates_to:
  - target: "[[LSTM]]"
    type: successor_to
    confidence: 0.9
  - target: "[[循环神经网络（RNN）]]"
    type: improves
    confidence: 0.9
  - target: "[[门控机制]]"
    type: implements
    confidence: 0.95
  - target: "[[Cho Kyunghyun]]"
    type: created_by
    confidence: 0.9
  - target: "[[2014年]]"
    type: developed_in
    confidence: 0.9
supersedes: null
---

# GRU

## 概述
门控循环单元（Gated Recurrent Unit，GRU）是由Cho Kyunghyun等人于2014年提出的循环神经网络变体，是LSTM的简化版本。

## 关键内容
1. **架构特点**：
   - 将LSTM的三个门简化为两个门：重置门（Reset Gate）和更新门（Update Gate）
   - 参数更少，训练更快
   - 在许多任务上表现与LSTM相当

2. **门控机制**：
   - 重置门：决定如何将过去的信息与当前输入结合起来
   - 更新门：决定保留多少过去的记忆
   - 与LSTM相比，GRU没有单独的输出门

3. **与LSTM的关系**：
   - 可以看作LSTM的"轻量版"
   - 在计算资源有限的情况下是很好的选择
   - 没有LSTM的记忆细胞和细胞状态概念

4. **发展历程**：
   - 2014年由Cho Kyunghyun等人提出
   - 是LSTM之后序列建模领域的重要进展
   - 代表了对门控机制的进一步简化和优化

## 来源
- [[12-hochreiter-1997-lstm.md]] — GRU发展历程

## 相关
- [[LSTM]] — successor_to
- [[循环神经网络（RNN）]] — improves
- [[门控机制]] — implements
- [[Cho Kyunghyun]] — created_by
- [[2014年]] — developed_in