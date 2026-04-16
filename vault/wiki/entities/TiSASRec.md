---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 时间间隔, Self-Attention, WSDM]
aliases: [TiSASRec, Time-Interval Aware SASRec]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 自注意力机制, type: uses}
supersedes: null
---

# TiSASRec

## 概述
Time-Interval Aware [[SASRec]]，2020 年提出的 [[SASRec]] 后续工作，在[[Self-Attention机制|自注意力]]中引入实际时间间隔建模，弥补了 [[SASRec]] 仅使用[[位置编码]]而忽略交互时间语义的不足。

## 关键内容

1. **论文信息**：Ti[[SASRec]]（Time-Interval Aware [[SASRec|Self-Attentive Sequential Recommendation]]），2020 年发表。

2. **核心改进**：[[SASRec]] 使用[[位置编码]]表示物品在序列中的相对顺序，但没有考虑交互之间的实际时间间隔。Ti[[SASRec]] 在[[Self-Attention机制|自注意力]]计算中引入了时间间隔信息——用户一小时内连续浏览的物品和间隔数月的两次购买具有完全不同的语义关联。

3. **方法**：在 [[SASRec]] 的[[嵌入表示|嵌入层]]中增加时间间隔嵌入（Time-Interval [[Embedding]]），与物品嵌入和[[位置编码|位置嵌入]]一起输入[[Self-Attention机制|自注意力]]层。注意力权重同时考虑内容相关性和时间接近度。

4. **解决的问题**：[[SASRec]] 的局限性之一——缺少时间间隔建模。在现实场景中，时间间隔是用户意图的重要信号：短时间内的密集交互通常反映明确的购买意图，而长时间跨度的交互可能反映周期性需求。

## 来源
- [TiSASRec 原始论文 (WSDM 2020)](https://dl.acm.org/doi/10.1145/3336191.3371785)

## 相关
- [[SASRec]] — TiSASRec 的基础模型
- [[序列推荐]] — TiSASRec 解决的核心场景
- [[自注意力机制]] — TiSASRec 的核心计算机制
- [[位置编码]] — TiSASRec 在此基础上增加时间间隔嵌入
