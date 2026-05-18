---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [nlp, "sequence modeling", encoder-decoder, 计算理论]
aliases: ["Sequence to Sequence", "Seq2Seq", "序列到序列模型"]
relates_to:
  - target: "[[Sequence to Sequence Learning with Neural Networks (2014 论文)]]"
    type: described_in
  - target: "[[Ilya Sutskever]]"
    type: created_by
  - target: "[[Encoder-Decoder Architecture]]"
    type: implements
  - target: "[[Machine Translation]]"
    type: applied_to
  - target: "[[Neural Machine Translation]]"
    type: pioneered
  - target: "[[RNN]]"
    type: uses
supersedes: null
---

# Seq2Seq

## 概述
Seq2Seq（Sequence to Sequence）是一种端到端的神经网络架构，用于处理输入序列到输出序列的映射问题。

## 关键内容

1. **[[编码器-解码器架构（Seq2Seq）|编码器-解码器]]架构**：Seq2Seq模型由两个主要组件组成：编码器将输入序列转换为固定长度的上下文向量（通常称为"thought vector"），解码器从这个向量生成输出序列。

2. **循环神经网络**：最初使用RNN（通常是LSTM或GRU）来处理变长序列，编码器逐步处理输入序列并将其信息压缩到上下文向量中。

3. **应用领域**：Seq2Seq模型首次在机器翻译任务中取得重大突破，随后被广泛应用于文本摘要、对话系统、语法纠错等多种NLP任务。

## 来源
- [[ai_papers_timeline.md]] — 2014年Seq2Seq提出
- [[Sequence to Sequence Learning with Neural Networks (2014 论文)]] — Ilya Sutskever等人的开创性工作

## 相关
- [[Sequence to Sequence Learning with Neural Networks (2014 论文)]] — described_in
- [[Ilya Sutskever]] — created_by
- [[Encoder-Decoder Architecture]] — implements
- [[Machine Translation]] — applied_to
- [[Neural Machine Translation]] — pioneered
- [[RNN]] — uses