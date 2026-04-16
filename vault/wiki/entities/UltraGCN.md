---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 图神经网络, 协同过滤, CIKM 2021]
aliases: [UltraGCN, UltraGCN 论文]
relates_to:
  - {target: LightGCN, type: extends}
  - {target: 协同过滤, type: implements}
  - {target: 邻域聚合, type: uses}
  - {target: BPR, type: uses}
supersedes: null
---

# UltraGCN

## 概述
CIKM 2021 发表的图推荐论文，在 [[LightGCN]] 基础上进一步简化，连显式邻域传播都省掉，通过直接逼近无限层传播的极限来做推荐。

## 关键内容

1. **核心思想**：[[LightGCN]] 虽然简化了 GCN，但仍需逐层进行邻域聚合的显式传播。UltraGCN 更进一步，直接逼近无限层图传播的极限，省掉了显式的多层传播过程。

2. **与 [[LightGCN]] 的关系**：UltraGCN 是 [[LightGCN]] "Less is More" 哲学的延续。如果 [[LightGCN]] 去掉了特征变换和非线性激活，UltraGCN 则去掉了显式传播本身。

3. **技术路径**：通过数学推导将无限层传播收敛到一个封闭解，避免了逐层[[矩阵]]乘法带来的计算开销。在保持甚至提升效果的同时，大幅降低了训练时间。

4. **历史地位**：与 [[SimpleX]]（CIKM 2021）同期，共同代表了"简化推荐模型"趋势在 2021 年的延续。

## 来源
- [[15-lightgcn.md]] — LightGCN 论文中提及的后续简化工作

## 相关
- [[LightGCN]] — UltraGCN 的直接前身
- [[SimpleX]] — 同期简化推荐模型工作
- [[协同过滤]] — UltraGCN 解决的核心任务
- [[BPR]] — UltraGCN 使用的损失函数
