---
type: entity
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [transformer, time-series, forecasting, research-paper]
aliases: ["FEDformer", "Frequency Enhanced Decomposed Transformer"]
relates_to: []
supersedes: null
entity_type: paper
---

# FEDformer: Frequency Enhanced Decomposed Transformer

## 概述
2022年发表的Transformer改进模型，通过在频域中执行注意力计算，利用傅里叶变换捕捉全局模式，是时间序列预测领域的重要进展。

## 关键内容

1. **核心技术**：
   - 在频域中计算注意力机制，减少计算复杂度
   - 利用傅里叶变换捕获全局时间序列模式
   - 结合时域和频域信息进行预测

2. **创新点**：
   - 频域注意力：将时域信号转换到频域进行处理
   - 全局模式捕捉：利用频域特性更好地识别周期性
   - 高效计算：相比时域注意力计算效率更高

3. **应用价值**：
   - 在多时间尺度序列预测任务中表现优异
   - 适用于具有复杂周期性的时间序列
   - 为频域分析在时间序列预测中的应用开辟新方向

## 来源
- [[15-informer-2021-transformer-time-series]] — Informer: 当 Transformer 叩开时间序列预测的大门
- [[]] —

## 相关
- [[Informer]] — compares_to
- [[Autoformer]] — compares_to
- [[时间序列预测]] — relates_to
- [[傅里叶变换]] — uses