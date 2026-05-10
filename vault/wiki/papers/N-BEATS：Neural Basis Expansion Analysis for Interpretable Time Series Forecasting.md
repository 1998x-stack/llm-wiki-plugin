---
type: paper
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [时间序列预测, 深度学习, 神经网络, 基函数展开]
aliases: ["N-BEATS", "N-BEATS: Neural Basis Expansion Analysis for Interpretable Time Series Forecasting", "Neural Basis Expansion Analysis"]
relates_to:
  - target: "[[Yoshua Bengio]]"
    type: authored
    confidence: 0.9
  - target: "[[时间序列预测]]"
    type: addresses
    confidence: 0.9
  - target: "[[全连接网络]]"
    type: utilizes
    confidence: 0.9
  - target: "[[残差学习]]"
    type: utilizes
    confidence: 0.9
  - target: "[[基函数展开]]"
    type: implements
    confidence: 0.9
  - target: "[[ES-RNN]]"
    type: supersedes
    confidence: 0.8
  - target: "[[M4竞赛]]"
    type: evaluated_on
    confidence: 0.9
  - target: "[[M3竞赛]]"
    type: evaluated_on
    confidence: 0.9
supersedes: null
---

# N-BEATS：Neural Basis Expansion Analysis for Interpretable Time Series Forecasting

## 概述
N-BEATS是2019年由Element AI和Yoshua Bengio实验室提出的一种用于时间序列预测的神经网络架构，通过使用全连接网络和基函数展开方法，在权威预测竞赛中击败了传统的统计方法。

## 关键内容

1. **背景与动机**：
   - 在2018年M4竞赛中，纯深度学习方法表现不佳，冠军方案ES-RNN是统计方法与RNN的混合方案
   - N-BEATS试图证明纯深度学习方法能否在时间序列预测上击败统计方法
   - 采用了最朴素的全连接层而非当时流行的RNN、LSTM、CNN或Transformer

2. **架构特点**：
   - 基本块（Basic Block）包含全连接层、ReLU激活函数和双路径输出（前向预测和后向回溯）
   - 双重残差连接：后向残差（减法传递输入）和前向聚合（加法聚合输出）
   - 每个块专注于信号中不同层次的模式，避免重复学习

3. **两种配置**：
   - 通用型（Generic）：前向和后向输出由全连接层直接生成，追求预测精度
   - 可解释型（Interpretable）：趋势栈使用低阶多项式基函数，季节性栈使用傅里叶级数基函数
   - 可解释配置通过基函数约束实现了神经网络的可解释性

## 来源
- [[14-nbeats-2019-neural-basis-expansion.md]] — 全文内容总结

## 相关
- [[Yoshua Bengio]] — authored
- [[时间序列预测]] — addresses the problem
- [[全连接网络]] — core component
- [[残差学习]] — key technique
- [[基函数展开]] — core method
- [[ES-RNN]] — supersedes
- [[M4竞赛]] — evaluation benchmark