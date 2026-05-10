---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [transformer, time-series, forecasting, attention-mechanism, long-sequence]
aliases: ["Informer", "Informer论文", "Beyond Efficient Transformer for Long Sequence Time-Series Forecasting"]
relates_to: []
supersedes: null
entity_type: paper
---

# Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting

## 概述
AAAI 2021最佳论文，提出了解决Transformer在长序列时间序列预测中复杂度问题的Informer模型，开创了"Transformer for Time Series"研究新方向。

## 关键内容

1. **背景与问题**：
   - 2017年Transformer提出后在NLP和CV领域取得巨大成功，但在时间序列预测领域进展缓慢
   - 标准Transformer在长序列时间序列预测(LSTF)面临三大瓶颈：O(L^2)的注意力复杂度、编码器堆叠的内存瓶颈、自回归解码的速度瓶颈

2. **核心创新**：
   - **ProbSparse自注意力**：通过KL散度识别有价值查询，只保留注意力分布集中、信息量大的query，计算复杂度降至O(L*ln L)
   - **自注意力蒸馏**：通过一维卷积和最大池化将序列长度逐层减半，大幅降低内存占用
   - **生成式解码器**：一步并行生成所有未来预测值，避免自回归模式下的误差累积

3. **影响力与意义**：
   - 在ETTh1、ETTh2、ETTm1、ECL等多个数据集上显著优于基线模型
   - 获得AAAI 2021最佳论文奖
   - 开启了"Transformer for Time Series"研究浪潮，后续涌现Autoformer、FEDformer、Pyraformer等众多相关工作

## 来源
- [[15-informer-2021-transformer-time-series]] — Informer: 当 Transformer 叩开时间门
- [[]] —

## 相关
- [[Transformer]] — extends
- [[时间序列预测]] — relates_to
- [[自注意力机制]] — uses
- [[ProbSparse自注意力]] — implements
- [[Long Sequence Time-Series Forecasting]] — relates_to
- [[PatchTST：一段时间序列值 64 个词 —— Transformer 的绝地反击]] — relates_to