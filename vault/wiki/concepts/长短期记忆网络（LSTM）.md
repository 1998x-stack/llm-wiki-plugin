---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [sequence-modeling, RNN, LSTM, 脑科学]
aliases: [LSTM, Long Short-Term Memory, 长短期记忆网络]
relates_to:
  - target: Sepp Hochreiter
    relation: relates_to
  - target: Jürgen Schmidhuber
    relation: relates_to
  - target: 梯度消失
    relation: addresses
  - target: 双向 LSTM（Bi-LSTM）
    relation: extends_to
supersedes: null
---

# 长短期记忆网络（LSTM）

## 概述
一种特殊的循环神经网络，通过[[门控机制（Gating Mechanism）|门控]]机制解决[[梯度消失]]问题，能够学习长期依赖关系。

## 关键内容

1. **[[门控机制（Gating Mechanism）|门控]]机制**：包含[[输入门（Input Gate）|输入门]]、[[遗忘门（Forget Gate）|遗忘门]]和[[输出门（Output Gate）|输出门]]，控制信息的流动和记忆更新。
2. **[[常误差流（Constant Error Carousel）|恒定误差轮播]]**：内部维护恒定误差路径，使梯度可以长时间流动而不衰减。
3. **应用场景**：在 [[Transformer]] 出现前是序列建模的主流方法，用于机器翻译、语音识别、文本生成等。

## 来源
- [[ai_papers_timeline.md]] — 1997 年时间线条目

## 相关
- [[Sepp Hochreiter]] — relates_to
- [[Jürgen Schmidhuber]] — relates_to
- [[梯度消失]] — addresses
- [[双向 LSTM（Bi-LSTM）]] — extends_to
- [[Bahdanau注意力]] — relates_to
