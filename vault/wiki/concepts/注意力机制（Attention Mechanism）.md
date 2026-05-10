---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "注意力机制", "NLP", "机器翻译", "LLM基础"]
aliases: ["Attention Mechanism", "注意力机制", "动态上下文向量"]
relates_to:
  - target: "[[Bahdanau注意力]]"
    type: implements
    confidence: 0.95
  - target: "[[Luong注意力]]"
    type: implements
    confidence: 0.9
  - target: "[[自注意力机制]]"
    type: extends
    confidence: 0.95
  - target: "[[编码器-解码器架构（Seq2Seq）]]"
    type: extends
    confidence: 0.95
  - target: "[[缩放点积注意力]]"
    type: extends
    confidence: 0.9
  - target: "[[多头注意力]]"
    type: extends
    confidence: 0.85
  - target: "[[Transformer架构]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# 注意力机制（Attention Mechanism）

## 概述

注意力机制使解码器在生成每个目标词时，能动态加权聚焦源序列的不同位置，彻底解决了 [[编码器-解码器架构（Seq2Seq）]] 的固定长度瓶颈问题，是现代 LLM 的核心之源。

## 关键内容

### 历史背景：固定长度瓶颈

2014 年 [[编码器-解码器架构（Seq2Seq）]] 将整个源句子压缩为**单一固定向量 c**，导致长句信息严重丢失。实验表明 BLEU 分数随源句长度增加急剧下降。[[Dzmitry Bahdanau]] 等人提出核心问题：翻译每个目标词时，Decoder 能否"回头看"原文的不同位置？

### 核心计算流程

设源编码 $h_1, h_2, ..., h_n$（双向 RNN 隐藏状态），Decoder 当前状态 $s_{t-1}$：

1. **对齐分数**：$e_{it} = a(s_{t-1}, h_i) = v^\top \tanh(W_a s_{t-1} + U_a h_i)$，学习源位置与当前解码的相关性
2. **[[Softmax]] 归一化**：$\alpha_{it} = \frac{\exp(e_{it})}{\sum_j \exp(e_{jt})}$，得到注意力权重 $\alpha_{it} \in [0,1]$，$\sum_i \alpha_{it} = 1$
3. **加权上下文向量**：$c_t = \sum_i \alpha_{it} h_i$，每个解码时刻专属的动态上下文
4. **Decoder 生成**：$s_t = f(s_{t-1}, y_{t-1}, c_t)$，融合注意力上下文生成目标词

### 可解释性突破：对齐矩阵

注意力权重 $\alpha$ 构成**对齐[[矩阵]]**，使机器翻译首次可视化。英法等语序相近语言呈现对角线模式，语序调换场景（如英语→法语"European Economic Area"）呈现反对角线模式。

### 三种主要变体

| 类型 | 对齐函数 | 特点 | 提出者 |
|------|---------|------|--------|
| **[[Bahdanau注意力|加性注意力]]** | $v^\top \tanh(W_a s + U_a h)$ | 参数灵活，效果好 | Bahdanau (2015) |
| **[[Luong注意力|点积注意力]]** | $s^\top h$ | 无额外参数，速度快 | Luong (2015) |
| **缩放点积** | $s^\top h / \sqrt{d}$ | 防止高维点积过大 | Vaswani (2017) |

### 演化路径

[[Bahdanau注意力]]（2015，加性，解决固定瓶颈）→ [[Luong注意力]]（2015，点积，更简洁）→ [[自注意力机制]]（2017，序列内部互相关，去掉 RNN）→ [[多头注意力]]（2017，并行多子空间）→ Cross-Attention（[[Transformer 架构|Transformer]] Decoder，Q 来自 Decoder，K/V 来自 Encoder）→ Flash Attention（2022，IO 感知加速 10 倍）。

## 来源

- [[Neural Machine Translation by Jointly Learning to Align and Translate (2015 论文)]] — 提出加性注意力机制，首次实现动态上下文向量

## 相关

- [[Bahdanau注意力]] — implements（加性注意力的具体实现）
- [[Luong注意力]] — implements（点积/乘性注意力的具体实现）
- [[自注意力机制]] — extends（序列内部位置相互关注，去除 RNN 依赖）
- [[编码器-解码器架构（Seq2Seq）]] — extends（在 seq2seq 基础上引入动态上下文）
- [[缩放点积注意力]] — extends（高维场景下的点积注意力改进）
- [[Transformer架构]] — extends（注意力机制的终极形态，完全基于注意力）
