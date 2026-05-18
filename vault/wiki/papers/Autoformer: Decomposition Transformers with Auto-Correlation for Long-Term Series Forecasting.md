---
type: entity
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [transformer, time-series, forecasting, research-paper, 时间序列]
aliases: ["Autoformer", "Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting"]
relates_to: []
supersedes: null
entity_type: paper
---

# Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting

## 概述
2021年NeurIPS发表的论文，引入序列分解和自相关机制的Transformer模型，用于长期时间序列预测，是Informer之后的重要后续工作。

## 关键内容

1. **核心创新**：
   - 将序列分解机制融入Transformer架构
   - 用自相关机制替代传统的点对点注意力
   - 通过自相关函数捕获序列中的周期性和趋势信息

2. **技术特点**：
   - 采用多尺度分解处理不同频率成分
   - 利用自相关性识别时间序列的内在周期
   - 在多个时间尺度上进行预测并融合结果

3. **应用场景**：
   - 适用于具有明显周期性和趋势特征的时间序列
   - 在电力负荷、气象数据、交通流量等预测任务中表现优异
   - 特别适合长期预测场景

## 来源
- [[15-informer-2021-transformer-time-series]] — Informer: 当 Transformer 叩开时间序列预测的大门
- [[]] —

## 相关
- [[Informer]] — compares_to
- [[时间序列预测]] — relates_to
- [[Transformer]] — extends
- [[自相关机制]] — uses
- [[PatchTST：一段时间序列值 64 个词 —— Transformer 的绝地反击]] — relates_to