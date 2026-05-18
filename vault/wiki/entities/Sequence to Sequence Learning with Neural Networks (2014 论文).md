---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, NLP, seq2seq, 信息论]
aliases: [Sutskever et al. 2014]
relates_to:
  - target: Ilya Sutskever
    relation: authored_by
  - target: 编码器-解码器架构（Seq2Seq）
    relation: introduced
  - target: 注意力机制（Attention Mechanism）
    relation: inspired
supersedes: null
---

# Sequence to Sequence Learning with Neural Networks (2014 论文)

## 概述
提出 [[Seq2Seq]] 架构的论文，使用[[编码器-解码器架构（Seq2Seq）|编码器-解码器]][[规范化理论|范式]]实现机器翻译等序列到序列任务。

## 关键内容

1. **[[编码器-解码器架构（Seq2Seq）|编码器-解码器]][[规范化理论|范式]]**：使用 LSTM 编码器将输入序列压缩为固定长度向量，解码器生成输出序列。
2. **机器翻译突破**：在英法翻译任务上取得优异结果，展示了神经网络可以学习复杂的序列映射。
3. **局限性**：固定长度瓶颈向量难以处理长序列，这一问题直接催生了 [[Bahdanau注意力]] 和 [[注意力机制（Attention Mechanism）]] 的研究。

## 来源
- [[ai_papers_timeline.md]] — 2014 年时间线条目

## 相关
- [[Ilya Sutskever]] — authored_by
- [[编码器-解码器架构（Seq2Seq）]] — introduced
- [[Bahdanau注意力]] — inspired
