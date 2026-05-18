---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [注意力机制, 深度学习, 多头机制, AI工程]
aliases: ["Multi-Head Attention Mechanism"]
relates_to: []
supersedes: null
---

# Multi-Head Attention

## 概述
一种扩展的[[注意力机制]]，将查询、键和值分别投影到多个不同的子空间中，在每个子空间独立执行[[注意力机制|注意力]][[计算]]，最后将结果拼接起来，增强了模型的表达能力。

## 关键内容

1. **[[计算]]过程**：
   - 将 Q、K、V 分别投影到 h 个不同的低维子空间
   - 在每个子空间独立执行[[注意力机制|注意力]][[计算]]：head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)
   - 拼接多头输出：Concat(head_1, ..., head_h) W^O

2. **技术参数**：
   - 论文中使用 h = 8 个[[注意力机制|注意力]]头
   - 每个头的维度为 d_k = d_v = d_model / h = 64
   - 保持总体[[计算]]成本与单头相近

3. **优势特点**：
   - 能够在多个表示子空间中学习不同的[[注意力机制|注意力]]模式
   - 不同的头可以关注不同类型的关系（语法、语义、位置等）
   - 显著增强了模型的表达能力

## 来源
- [[Transformer]] — 核心组件
- [[20-vaswani-transformer.md]] — raw/books/计算机科学/20-vaswani-transformer.md

## 相关
- [[Transformer]] — core_component
- [[Attention Is All You Need]] — introduced_in
- [[Self-Attention]] — variant
- [[Scaled Dot-Product Attention]] — component