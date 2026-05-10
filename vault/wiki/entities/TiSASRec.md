---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 序列推荐, 时间间隔, Self-Attention, WSDM]
aliases: [TiSASRec, Time-Interval Aware SASRec, Time-Interval Aware Self-Attentive Sequential Recommendation]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 自注意力机制, type: uses}
  - {target: 位置编码, type: extends}
  - {target: 时间间隔建模, type: implements}
  - {target: 序列推荐, type: implements}
  - {target: 自注意力机制, type: uses}
supersedes: null
---

# TiSASRec

## 概述
Time-Interval Aware [[SASRec]]，2020 年提出的 [[SASRec]] 后续工作，在[[Self-Attention机制|自注意力]]中引入实际时间间隔建模，弥补了 [[SASRec]] 仅使用[[位置编码]]而忽略交互时间语义的不足。

## 关键内容

1. **论文信息**：Ti[[SASRec]]（Time-Interval Aware [[SASRec|Self-Attentive Sequential Recommendation]]），2020 年发表。

2. **核心改进**：[[SASRec]] 使用[[位置编码]]表示物品在序列中的相对顺序，但没有考虑交互之间的实际时间间隔。Ti[[SASRec]] 在[[Self-Attention机制|自注意力]][[计算]]中引入了时间间隔信息——用户一小时内连续浏览的物品和间隔数月的两次购买具有完全不同的语义关联。

3. **方法**：在 [[SASRec]] 的[[嵌入表示|嵌入层]]中增加时间间隔嵌入（Time-Interval [[Embedding]]），与物品嵌入和[[位置编码|位置嵌入]]一起输入[[Self-Attention机制|自注意力]]层。注意力权重同时考虑内容相关性和时间接近度。

4. **核心创新**：
   - **时间间隔嵌入**：为每个交互的时间间隔分配嵌入向量，编码时间距离信息
   - **时间感知位置编码**：结合相对位置信息和时间间隔信息，构建更丰富的序列表示
   - **时间衰减机制**：根据时间间隔长短对注意力权重进行衰减，长时间间隔的物品关注度更低
   - **双重位置编码**：不仅考虑序列中的相对位置，还考虑交互之间的实际时间戳
   - **时间间隔编码**：将连续交互间的时间间隔离散化，映射为可学习的时间嵌入
   - **增强的自注意力**：在计算Q/K/V时融入时间间隔信息，使模型能够区分不同时间尺度的依赖关系

5. **解决的问题**：[[SASRec]] 的局限性之一——缺少时间间隔建模。在现实场景中，时间间隔是用户意图的重要信号：短时间内的密集交互通常反映明确的购买意图，而长时间跨度的交互可能反映周期性需求。SASRec使用位置编码来表示物品在序列中的相对顺序，但没有考虑交互之间的实际时间间隔，而TiSASRec在SASRec的基础上加入了时间间隔感知能力。

6. **技术实现**：
   - **双重位置编码**：不仅考虑序列中的相对位置，还考虑交互之间的实际时间戳
   - **时间间隔编码**：将连续交互间的时间间隔离散化，映射为可学习的时间嵌入
   - **增强的自注意力**：在计算Q/K/V时融入时间间隔信息，使模型能够区分不同时间尺度的依赖关系

7. **与SASRec的关系**：TiSASRec直接扩展了SASRec的架构，在其基础上加入了时间间隔感知能力，保持了原有的自注意力机制和因果掩码设计。

8. **实验效果**：在多个带有时间戳信息的数据集上验证了有效性，特别是在用户行为时间分布不均匀的场景下表现优异。

## 来源
- [TiSASRec 原始论文 (WSDM 2020)](https://dl.acm.org/doi/10.1145/3336191.3371785)

## 相关
- [[SASRec]] — TiSASRec 的基础模型
- [[序列推荐]] — TiSASRec 解决的核心场景
- [[自注意力机制]] — TiSASRec 的核心计算机制
- [[位置编码]] — TiSASRec 在此基础上增加时间间隔嵌入
- [[时间间隔建模]] — TiSASRec关注的核心问题
