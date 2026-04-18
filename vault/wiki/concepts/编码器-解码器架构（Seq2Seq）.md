---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "NLP", "机器翻译", "序列建模", "机器学习"]
aliases: ["Seq2Seq", "Encoder-Decoder Architecture", "编码器-解码器", "序列到序列模型"]
relates_to:
  - target: "[[注意力机制（Attention Mechanism）]]"
    type: extends
    confidence: 0.95
  - target: "[[循环神经网络（RNN）]]"
    type: uses
    confidence: 0.9
  - target: "[[LSTM（长短期记忆网络）]]"
    type: uses
    confidence: 0.85
  - target: "[[双向 LSTM（Bi-LSTM）]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# 编码器-解码器架构（Seq2Seq）

## 概述

Seq2Seq 将变长输入序列通过 Encoder 编码为固定向量，再由 Decoder 解码为变长输出序列，是机器翻译、文本摘要等任务的奠基性架构，但存在固定长度瓶颈。

## 关键内容

### 架构设计

```
源序列 "Je suis étudiant"
  ↓ Encoder（RNN/LSTM）逐词处理
  → 最终隐藏状态 c（固定长度向量，如 512 维）
  ↓ Decoder（RNN/LSTM）从 c 逐词生成
目标序列 "I am a student"
```

**Encoder**：使用双向 RNN/LSTM 逐词编码源序列，将全部上下文信息压缩至最终隐藏状态 $c = h_n$。

**Decoder**：以 $c$ 为初始状态，[[AR 模型（自回归模型）|自回归]]地生成目标序列 $P(y_t | y_1, ..., y_{t-1}, c)$，每个时刻依赖同一固定向量。

### 致命瓶颈：固定长度向量

整个源句子信息被压缩进**一个固定维度向量**，导致：

- 短句（5 词）→ c 尚能容纳
- 长句（50 词）→ 信息丢失严重
- 复杂句（100 词）→ 几乎无法翻译

实验验证：BLEU 分数随源句长度增加急剧下降。这一瓶颈直接催生了 [[注意力机制（Attention Mechanism）]]。

### 应用场景

- **机器翻译**：源语言→目标语言
- **文本摘要**：长文本→短摘要
- **对话生成**：用户输入→系统回复
- **语音识别**：音频序列→文本序列

### 改进方向

[[注意力机制（Attention Mechanism）]] 彻底解决了固定瓶颈：不再使用单一固定向量 $c$，而是在每个解码时刻动态计算专属上下文向量 $c_t = \sum_i \alpha_{it} h_i$，使 Decoder 能"回头看"源序列的不同位置。

## 来源

- [[Neural Machine Translation by Jointly Learning to Align and Translate (2015 论文)]] — 分析 seq2seq 固定瓶颈并引入注意力机制

## 相关

- [[注意力机制（Attention Mechanism）]] — extends（动态上下文替代固定向量）
- [[循环神经网络（RNN）]] — uses（Encoder/Decoder 的基础组件）
- [[LSTM（长短期记忆网络）]] — uses（常用 Encoder/Decoder 单元）
- [[双向 LSTM（Bi-LSTM）]] — uses（Encoder 常用双向编码）
