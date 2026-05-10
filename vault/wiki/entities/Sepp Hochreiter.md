---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 4
tags: ["机器学习", "深度学习", "LSTM"]
aliases: ["Sepp Hochreiter", "约瑟夫·霍赫赖特"]
relates_to:
  - target: "[[LSTM]]"
    type: created
    confidence: 0.95
  - target: "[[Jurgen Schmidhuber]]"
    type: collaborated_with
    confidence: 0.95
  - target: "[[梯度消失]]"
    type: analyzed
    confidence: 0.95
  - target: "[[Long Short-Term Memory]]"
    type: authored
    confidence: 0.95
  - target: "[[常误差流（Constant Error Carousel）]]"
    type: invented
    confidence: 0.95
  - target: "[[门控机制]]"
    type: pioneered
    confidence: 0.95
entity_type: person
supersedes: null
---

# Sepp Hochreiter

## 概述
奥地利计算机科学家，LSTM共同发明人。1991年本科论文首次系统分析RNN梯度消失问题，1997年与导师Schmidhuber共同提出LSTM架构，解决序列建模中的长期依赖难题。其开创性工作为现代深度学习序列建模奠定了基础。

## 关键内容
1. **学术贡献**：
   - LSTM（长短期记忆）网络的主要发明者（1997年与Schmidhuber共同发表）
   - 早在1991年的本科毕业论文中就系统分析了RNN的梯度消失问题
   - 在1991年的硕士论文中首次从数学上证明了标准循环神经网络（RNN）在时间反向传播（BPTT）时，梯度会因连乘权重矩阵而指数级衰减
   - 提出了常误差流（CEC）机制，从根本上解决梯度消失问题
   - 开创了门控机制的范式，影响了后续所有序列建模架构

2. **学术生涯**：
   - 现任奥地利林茨约翰开普勒大学（Johannes Kepler University Linz）教授
   - ELLIS（欧洲学习与智能系统卓越实验室）单元主任

3. **研究领域**：
   - 深度学习理论
   - 生物信息学
   - 药物发现

4. **历史地位**：
   - 与Schmidhuber的合作被称为深度学习史上最具有影响力的师生组合之一
   - 他的研究为解决循环神经网络的长期依赖问题奠定了基础
   - LSTM成为1997-2017年间序列建模的标准架构，在语音识别、机器翻译、时间序列预测等领域统治了20年
   - 1997年发表的LSTM论文被引用超过98,000次，是计算机科学领域被引用最多的论文之一

5. **创新影响**：
   - LSTM中的门控设计思想深刻影响了后续所有序列建模架构，包括GRU和Transformer
   - 常误差流（CEC）机制为解决梯度问题提供了全新思路
   - 其工作推动了深度学习的复兴，在2000年代深度学习低谷期持续产生实际成果

## 来源
- [[12-hochreiter-1997-lstm.md]] — 论文介绍和作者信息
- [[Long Short-Term Memory (1997 论文)]] — Hochreiter, S., & Schmidhuber, J. (1997). Neural Computation, 9(8), 1735–1780
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — LSTM 核心原理与代码实现
- [[常误差流（Constant Error Carousel）]] — CEC机制详细介绍

## 相关
- [[Jurgen Schmidhuber]] — collaborated_with（导师与合作者）
- [[LSTM]] — created（共同发明）
- [[梯度消失]] — analyzed（首次系统分析）
- [[Long Short-Term Memory]] — authored（共同作者）
- [[常误差流（Constant Error Carousel）]] — invented（CEC机制发明）
- [[门控机制]] — pioneered（门控范式开创）
