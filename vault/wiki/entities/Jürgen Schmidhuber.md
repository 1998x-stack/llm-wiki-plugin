---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "人物"]
aliases: ["Jürgen Schmidhuber", "于尔根·施密德胡贝尔"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: extends
    confidence: 0.95
  - target: "[[Sepp Hochreiter]]"
    type: relates_to
    confidence: 0.95
supersedes: null
---

# Jürgen Schmidhuber

## 概述 (50-200字符)
德国计算机科学家，AI 研究者，LSTM 共同发明人。作为 [[Sepp Hochreiter]] 的博士导师，与 Hochreiter 于 1997 年共同提出 LSTM 架构，通过[[门控机制（Gating Mechanism）|门控]]机制解决 RNN [[梯度消失]]问题，对深度学习序列建模产生深远影响。

## 关键内容 (≥300字符, 用[[双链]])
1. **LSTM 共同发明**：1997 年，Schmidhuber 与学生 [[Sepp Hochreiter]] 在 *Neural Computation* 发表《[[LSTM（长短期记忆网络）|Long Short-Term Memory]]》，引入**[[细胞状态（Cell State）]]**和三个门（[[遗忘门（Forget Gate）]]、[[输入门（Input Gate）]]、[[输出门（Output Gate）]]），使神经网络首次能够学习跨越数百时间步的长期依赖。
2. **技术贡献**：LSTM 的核心思想是让梯度通过加法路径直接传递而不衰减（∂Cₜ/∂Cₜ₋₁ = fₜ），当[[遗忘门（Forget Gate）|遗忘门]]接近 1 时，梯度可以无损流过整个序列。这一设计从根本上解决了 [[梯度消失]] 问题。
3. **学术影响**：LSTM 论文被引用超过 98,000 次，成为语音识别（[[Google]] Voice 2015）、机器翻译（[[Google]] 翻译 2016）、时间序列预测等领域的标准架构，统治序列学习领域近 20 年。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter, S., & Schmidhuber, J. (1997). Neural Computation, 9(8), 1735–1780
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — LSTM 核心原理与代码实现

## 相关
- [[Sepp Hochreiter]] — relates_to（学生与合作者）
- [[LSTM（长短期记忆网络）]] — extends（共同发明）
- [[Long Short-Term Memory (1997 论文)]] — extends（共同作者）
