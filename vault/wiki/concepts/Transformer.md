---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [transformer, attention, nlp, architecture, deep-learning]
aliases: ["Transformer Architecture", "Transformer Model"]
relates_to:
  - target: "[[Attention Is All You Need]]"
    type: described_in
    confidence: 0.9
  - target: "[[Self-Attention]]"
    type: utilizes
    confidence: 0.9
  - target: "[[Multi-Head Attention]]"
    type: utilizes
    confidence: 0.9
  - target: "[[Positional Encoding]]"
    type: utilizes
    confidence: 0.9
  - target: "[[Feed Forward Network]]"
    type: utilizes
    confidence: 0.8
  - target: "[[Layer Normalization]]"
    type: utilizes
    confidence: 0.8
  - target: "[[Residual Connection]]"
    type: utilizes
    confidence: 0.8
  - target: "[[BERT]]"
    type: predecessor
    confidence: 0.9
  - target: "[[GPT]]"
    type: predecessor
    confidence: 0.9
  - target: "[[RNN]]"
    type: supersedes
    confidence: 0.8
supersedes: null
---

# Transformer

## 概述
Transformer是一种完全基于[[注意力机制（Attention Mechanism）|注意力机制]]的深度学习架构，由[[Google Brain]]于2017年在论文《[[Transformer 论文|Attention Is All You Need]]》中提出。该架构抛弃了传统的循环和卷积结构，实现了完全并行化处理，成为现代AI模型的基础架构。

## 关键内容

1. **整体架构**：
   - [[编码器-解码器架构（Seq2Seq）|编码器-解码器]]结构，各含N个相同的层（原论文中N=6）
   - 编码器负责将输入序列转换为连续表示
   - 解码器逐步生成输出序列

2. **编码器组件**：
   - [[多头注意力|多头自注意力]]机制：捕获输入序列内部的依赖关系
   - [[多层感知机（MLP）|前馈神经网络]]：对每个位置独立进行相同变换
   - [[残差连接]]与[[Layer Normalization|层归一化]]：提升训练稳定性

3. **解码器组件**：
   - 掩蔽[[多头注意力|多头自注意力]]：防止关注未来信息
   - [[多头注意力]]层：关注编码器输出
   - [[多层感知机（MLP）|前馈神经网络]]：逐位置变换
   - 线性层与[[Softmax]]：输出概率分布

4. **关键技术**：
   - [[位置编码]]解决序列顺序问题
   - [[注意力机制（Attention Mechanism）|注意力机制]]实现长距离依赖
   - 并行化训练大幅提升效率

## 来源
- [[Attention Is All You Need]] — 原始论文
- [[paper_06_transformer.md]] — 论文精读笔记
- [[raw/articles/ai-papers/foundations/paper_06_transformer.md]] — 原始资料

## 相关
- [[Attention Is All You Need]] — described_in
- [[Self-Attention]] — utilizes
- [[Multi-Head Attention]] — utilizes
- [[Positional Encoding]] — utilizes
- [[Feed Forward Network]] — utilizes
- [[Layer Normalization]] — utilizes
- [[Residual Connection]] — utilizes
- [[Google Brain]] — developed_by
- [[BERT]] — predecessor
- [[GPT]] — predecessor
- [[RNN]] — supersedes