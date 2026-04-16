---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", "深度学习", 时间序列]
aliases: ["N-BEATS", "Neural Basis Expansion Analysis", "神经基函数展开分析"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Informer]]"
    type: compares_to
    confidence: 0.75
  - target: "[[指数平滑]]"
    type: compares_to
    confidence: 0.7
supersedes: null
---

# N-BEATS

## 概述
N-BEATS（Neural Basis Expansion Analysis for Interpretable Time Series Forecasting）由 Boris Oreshkin 等（Yoshua Bengio 团队）于 2019 年提出，用纯全连接网络在 M4 竞赛中击败了所有统计方法，证明深度学习可独立称霸时间序列预测。

## 关键内容

1. **历史背景**：2018 年 M4 竞赛冠军 ES-RNN 是[[指数平滑]]+RNN 的混合方法，纯深度学习方法甚至不如简单统计基线。学术界流传"时间序列预测天然属于统计方法"的观点。

2. **核心创新**：抛弃 RNN/LSTM/CNN/[[Transformer架构|Transformer]] 等所有花哨结构，回归最朴素的全连接层。通过堆叠多层感知机 + 双重[[残差连接]]（前向残差 + 后向残差），实现基函数展开。

3. **双重分支**：趋势分支（拟合多项式基函数）+ 季节分支（拟合傅里叶基函数），两种分支的预测结果相加得到最终预测。这种设计既保证预测精度，又提供可解释性。

4. **影响**：在 M4 竞赛数据集上纯深度学习方法首次超越所有统计方法，证明"结构越简单，有时反而越强大"。

## 来源
- [[14-nbeats-2019-neural-basis-expansion]] — N-BEATS：当"最笨"的神经网络击败了所有统计学大师

## 相关
- [[LSTM（长短期记忆网络）]] — compares_to
- [[Informer]] — compares_to
- [[指数平滑]] — compares_to
