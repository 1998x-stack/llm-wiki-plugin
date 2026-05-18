---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [transformer, attention-mechanism, sparse-attention, time-series, 机器学习]
aliases: ["ProbSparse自注意力", "Probabilistic Sparse Attention", "ProbSparse Attention"]
relates_to: []
supersedes: null
---

# ProbSparse自注意力

## 概述
[[Informer]]模型提出的一种改进[[自注意力机制]]的方法，通过概率稀疏化减少[[计算]]复杂度，从O(L^2)降至O(L*ln L)。

## 关键内容

1. **核心原理**：
   - 标准[[Self-Attention机制|自注意力]]中多数query的[[注意力机制|注意力]]分布接近均匀分布，信息含量极低
   - 只有少数query真正"专注"于某些key，呈现出尖锐的[[注意力机制|注意力]]分布，这些才是有价值的query
   - 通过[[计算]]每个query的[[注意力机制|注意力]]分布与均匀分布间的[[KL散度]]衡量query稀疏性

2. **实现方法**：
   - 在所有query中只保留[[KL散度]]最高的Top-u个query（u = c * ln(L)，c为采样因子）
   - 对被淘汰的query，将其[[注意力机制|注意力]]输出设为所有value的均值
   - 最终只需[[计算]]O(L * ln L)次点积，而非O(L^2)

3. **优势与效果**：
   - 大幅提升[[计算]]效率，降低内存占用
   - 保持模型性能，专注于有价值的信息交互
   - 为处理[[长序列时间序列预测]]提供可行方案

## 来源
- [[15-informer-2021-transformer-time-series]] — Informer: 当 Transformer 叩开时间序列预测的大门
- [[]] —

## 相关
- [[Informer]] — part_of
- [[自注意力机制]] — extends
- [[时间序列预测]] — relates_to
- [[注意力机制]] — relates_to