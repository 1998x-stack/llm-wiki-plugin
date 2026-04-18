---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "人物"]
aliases: ["Sepp Hochreiter", "约瑟夫·霍赫赖特"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: extends
    confidence: 0.95
  - target: "[[Jürgen Schmidhuber]]"
    type: relates_to
    confidence: 0.95
  - target: "[[梯度消失]]"
    type: relates_to
    confidence: 0.9
supersedes: null
---

# Sepp Hochreiter

## 概述 (50-200字符)
奥地利计算机科学家，LSTM 共同发明人。1991 年硕士论文首次系统分析 RNN [[梯度消失]]问题，1997 年与导师 [[Jürgen Schmidhuber]] 共同提出 LSTM 架构，彻底解决序列建模中的长期依赖难题。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[梯度消失]]的早期洞察**：Hochreiter 在 1991 年的硕士论文中首次从数学上证明了标准 [[循环神经网络（RNN）]] 在时间[[反向传播]]（[[反向传播|BPTT]]）时，梯度会因连乘权重[[矩阵]]而指数级衰减，导致网络无法学习超过 10 步的长期依赖。
2. **LSTM 的诞生**：1997 年，Hochreiter 与 [[Jürgen Schmidhuber]] 在 *Neural Computation* 期刊发表划时代论文《[[LSTM（长短期记忆网络）|Long Short-Term Memory]]》，提出通过**[[细胞状态（Cell State）|细胞状态]]**和**[[门控机制（Gating Mechanism）|门控]]机制**（[[遗忘门（Forget Gate）]]、[[输入门（Input Gate）]]、[[输出门（Output Gate）]]）从根本上解决[[梯度消失]]问题。
3. **历史影响**：LSTM 成为 1997-2017 年间序列建模的标准架构，在语音识别、机器翻译、时间序列预测等领域统治了 20 年，直到 [[Transformer架构]] 出现才逐步退场。Hochreiter 的贡献被引用超过 98,000 次。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter, S., & Schmidhuber, J. (1997). Neural Computation, 9(8), 1735–1780
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — LSTM 核心原理与代码实现

## 相关
- [[Jürgen Schmidhuber]] — relates_to（导师与合作者）
- [[LSTM（长短期记忆网络）]] — extends（共同发明）
- [[Long Short-Term Memory (1997 论文)]] — extends（共同作者）
- [[梯度消失]] — relates_to（首次系统分析）
