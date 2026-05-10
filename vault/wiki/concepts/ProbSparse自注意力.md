---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [transformer, attention-mechanism, sparse-attention, time-series]
aliases: ["ProbSparse自注意力", "Probabilistic Sparse Attention", "ProbSparse Attention"]
relates_to: []
supersedes: null
---

# ProbSparse自注意力

## 概述
Informer模型提出的一种改进自注意力机制的方法，通过概率稀疏化减少计算复杂度，从O(L^2)降至O(L*ln L)。

## 关键内容

1. **核心原理**：
   - 标准自注意力中多数query的注意力分布接近均匀分布，信息含量极低
   - 只有少数query真正"专注"于某些key，呈现出尖锐的注意力分布，这些才是有价值的query
   - 通过计算每个query的注意力分布与均匀分布间的KL散度衡量query稀疏性

2. **实现方法**：
   - 在所有query中只保留KL散度最高的Top-u个query（u = c * ln(L)，c为采样因子）
   - 对被淘汰的query，将其注意力输出设为所有value的均值
   - 最终只需计算O(L * ln L)次点积，而非O(L^2)

3. **优势与效果**：
   - 大幅提升计算效率，降低内存占用
   - 保持模型性能，专注于有价值的信息交互
   - 为处理长序列时间序列预测提供可行方案

## 来源
- [[15-informer-2021-transformer-time-series]] — Informer: 当 Transformer 叩开时间序列预测的大门
- [[]] —

## 相关
- [[Informer]] — part_of
- [[自注意力机制]] — extends
- [[时间序列预测]] — relates_to
- [[注意力机制]] — relates_to