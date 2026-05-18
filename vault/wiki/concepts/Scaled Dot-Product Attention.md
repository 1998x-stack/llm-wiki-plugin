---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [注意力机制, 深度学习, 缩放机制, 机器学习]
aliases: ["Scaled Dot-Product Attention Mechanism"]
relates_to: []
supersedes: null
---

# Scaled Dot-Product Attention

## 概述
一种具体的[[注意力机制|注意力]][[计算]]方法，通过点积[[计算]]查询和键的相似度，并除以键向量维度的平方根进行缩放，是 [[Transformer]] 中使用的基础[[注意力机制]]。

## 关键内容

1. **[[计算]]公式**：
   - Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
   - 包括四个步骤：[[计算]]相似度、缩放、归一化、加权求和

2. **缩放目的**：
   - 当 d_k 较大时，点积结果可能变得很大
   - 导致 softmax 函数进入梯度极小的饱和区域
   - 除以 sqrt(d_k) 稳定点积方差，确保梯度有效传播

3. **应用场景**：
   - 作为 [[Multi-Head Attention]] 的基础组件
   - 在编码器[[Self-Attention机制|自注意力]]、解码器掩码[[Self-Attention机制|自注意力]]、[[编码器-解码器架构（Seq2Seq）|编码器-解码器]]交叉[[注意力机制|注意力]]中使用
   - 是 [[Transformer 架构]]的核心[[计算]]单元

## 来源
- [[Transformer]] — 核心组件
- [[20-vaswani-transformer.md]] — raw/books/计算机科学/20-vaswani-transformer.md

## 相关
- [[Transformer]] — core_component
- [[Attention Is All You Need]] — introduced_in
- [[Multi-Head Attention]] — component
- [[Self-Attention]] — variant