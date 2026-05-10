---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: ["机器学习", "深度学习", "人物"]
aliases: ["Jürgen Schmidhuber", "于尔根·施密德胡贝尔", "Jurgen Schmidhuber"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: created
    confidence: 0.95
  - target: "[[Sepp Hochreiter]]"
    type: supervised
    confidence: 0.95
  - target: "[[常误差流（Constant Error Carousel）]]"
    type: co-invented
    confidence: 0.95
  - target: "[[梯度消失]]"
    type: addressed
    confidence: 0.95
  - target: "[[IDSIA]]"
    type: affiliated_with
    confidence: 0.9
  - target: "[[NNAISENSE]]"
    type: founder
    confidence: 0.9
supersedes: null
---

# Jürgen Schmidhuber

## 概述 (50-200字符)
德国计算机科学家，AI研究者，LSTM共同发明人。作为[[Sepp Hochreiter]]的博士导师，与Hochreiter于1997年共同提出LSTM架构，通过门控机制解决RNN梯度消失问题，对深度学习序列建模产生深远影响。被誉为"现代AI之父"之一。

## 关键内容 (≥300字符, 用[[双链]])
1. **LSTM共同发明**：1997年，Schmidhuber与学生[[Sepp Hochreiter]]在*Neural Computation*发表《[[LSTM（长短期记忆网络）|Long Short-Term Memory]]》，引入**[[细胞状态（Cell State）]]**和三个门（[[遗忘门（Forget Gate）]]、[[输入门（Input Gate）]]、[[输出门（Output Gate）]]），使神经网络首次能够学习跨越数百时间步的长期依赖。共同开发了[[常误差流（Constant Error Carousel）|常误差流]]（CEC）机制，从根本上解决梯度问题。

2. **技术贡献**：LSTM的核心思想是让梯度通过加法路径直接传递而不衰减（∂Cₜ/∂Cₜ₋₁ = fₜ），当[[遗忘门（Forget Gate）|遗忘门]]接近1时，梯度可以无损流过整个序列。这一设计从根本上解决了[[梯度消失]]问题。他还积极推动神经网络压缩、元学习、强化学习等领域发展。

3. **学术影响**：LSTM论文被引用超过98,000次，成为语音识别（[[Google]] Voice 2015）、机器翻译（[[Google]]翻译2016）、[[Time Series Analysis|时间序列]]预测等领域的标准架构，统治序列学习领域近20年。

4. **学术生涯**：长期担任瑞士IDSIA（Dalle Molle人工智能研究所）科学主任，现创办AI公司NNAISENSE。以积极为自己和学生的历史贡献争取认可而闻名。

5. **师生合作**：与[[Sepp Hochreiter]]的合作被称为深度学习史上最具有影响力的师生组合之一。他们的协作模式展示了深度学习研究中理论分析与实践创新的完美结合。

## 来源
- [[12-hochreiter-1997-lstm.md]] — 作者信息和贡献介绍
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter, S., & Schmidhuber, J. (1997). Neural Computation, 9(8), 1735–1780
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — LSTM 核心原理与代码实现

## 相关
- [[Sepp Hochreiter]] — supervised（博士导师与合作者）
- [[LSTM（长短期记忆网络）]] — created（共同发明）
- [[常误差流（Constant Error Carousel）]] — co-invented（共同发明）
- [[Long Short-Term Memory (1997 论文)]] — authored（共同作者）
- [[IDSIA]] — affiliated_with（任职机构）
- [[NNAISENSE]] — founder（创办公司）
- [[梯度消失]] — addressed（解决的核心问题）
