---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", "深度学习", 时间序列]
aliases: ["Long Short-Term Memory", "长短期记忆网络", "LSTM 细胞"]
relates_to:
  - target: "[[Transformer架构]]"
    type: compares_to
    confidence: 0.85
  - target: "[[梯度消失问题]]"
    type: caused
    confidence: 0.9
  - target: "[[门控机制]]"
    type: implements
    confidence: 0.95
supersedes: null
---

# LSTM（长短期记忆网络）

## 概述
LSTM 由 Sepp Hochreiter 和 Jü[[ripgrep|rg]]en Schmidhuber 于 1997 年提出，通过门控机制解决传统 RNN 的梯度消失问题，使神经网络能够学习跨越数百个时间步的长期依赖关系，是深度学习序列建模的里程碑。

## 关键内容

1. **历史背景**：1990 年代 RNN 理论上拥有无限记忆能力，但实践中无法学习超过 10-20 个时间步的依赖。Hochreiter 1991 年本科论文首次系统分析此问题，1997 年与 Schmidhuber 发表划时代论文。

2. **梯度消失根源**：RNN 训练通过 BPTT（时间反向传播），梯度沿时间步连乘传递，每经过一步就被"打折"，导致远距离信息被稀释殆尽。

3. **核心创新**：引入细胞状态（cell state）和三个门控机制——遗忘门（决定丢弃什么信息）、输入门（决定存储什么新信息）、输出门（决定输出什么信息）。细胞状态像一条"信息高速公路"，梯度可以无损流过。

4. **影响**：98,000+ 次引用，成为语音识别、机器翻译、时间序列预测等领域的标准架构，直到 [[Transformer架构|Transformer]] 出现后才逐渐被取代。

## 来源
- [[12-hochreiter-1997-lstm]] — LSTM：一座让神经网络学会"记忆"的里程碑

## 相关
- [[Transformer架构]] — compares_to
- [[梯度消失问题]] — caused
- [[门控机制]] — implements
