---
type: entity
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [transformer, time-series, forecasting, research-paper]
aliases: ["DLinear", "Are Transformers Effective for Time Series Forecasting"]
relates_to: []
supersedes: null
entity_type: paper
---

# DLinear: Are Transformers Effective for Time Series Forecasting?

## 概述
2023年AAAI发表的论文，提出了极其简单的线性模型DLinear，质疑了复杂Transformer模型在时间序列预测中的有效性，引发了学界对模型复杂性的深刻反思。

## 关键内容

1. **核心质疑**：
   - Transformer的自注意力机制具有"置换不变性"(permutation-invariant)，与时间序列的顺序本质可能矛盾
   - 位置编码是否真正有效利用时间序列中的时序信息存疑
   - 模型的复杂性不等于有效性

2. **模型设计**：
   - 仅由一层线性层组成，没有任何注意力机制
   - 模型结构极其简单，参数量极少
   - 先做趋势-季节性分解，然后分别用一个单层线性网络预测，最后把结果加起来
   - 性能与复杂Transformer模型相当

3. **研究发现**：
   - DLinear在多个基准数据集上表现与Informer、Autoformer等模型不相上下
   - 甚至在某些场景下优于复杂模型
   - 对"Transformer是否真适合时间序列预测"提出质疑
   - Transformer的优势可能并非来自自注意力机制本身，而是来自它使用的DMS(直接多步预测)策略

4. **学术影响**：
   - 促使研究者重新审视复杂架构改进的必要性
   - 引发对注意力机制在时间序列任务中有效性的讨论
   - 强调了简单基线模型的重要性
   - 后续出现了如PatchTST等新的时间序列预测方法

## 来源
- [[15-informer-2021-transformer-time-series]] — Informer: 当 Transformer 叩开时间序列预测的大门
- [[../raw/books/时间序列分析/16-dlinear-2023-are-transformers-effective.md]] — 详细内容来源

## 相关
- [[Informer]] — contradicts
- [[Autoformer]] — contradicts
- [[FEDformer]] — contradicts
- [[时间序列预测]] — relates_to
- [[线性模型]] — part_of
- [[PatchTST：一段时间序列值 64 个词 —— Transformer 的绝地反击]] — responds_to
- [[曾爱玲]] — author_of
- [[陈慕希]] — contributor_to
- [[香港中文大学]] — institution_of