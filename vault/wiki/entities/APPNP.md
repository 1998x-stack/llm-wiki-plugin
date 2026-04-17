---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [图神经网络, Personalized PageRank, ICLR 2019, 节点分类, 推荐系统]
aliases: [APPNP, Approximate Personalized Propagation of Neural Predictions]
relates_to:
  - {target: LightGCN, type: compares_to}
  - {target: SGC, type: compares_to}
  - {target: Embedding, type: uses}
supersedes: null
---

# APPNP

## 概述
Klicpera 等人于 ICLR 2019 发表的论文，基于 Personalized PageRank 思想，在每层传播中混入初始特征（teleport）以缓解过平滑，与 [[LightGCN]] 共享抗过平滑机制。

## 关键内容

1. **核心思想**：APPNP 将神经网络与图传播解耦——先用 MLP 学习节点初始表示，再通过 Personalized PageRank 风格的传播在图上传播这些表示。每层传播中混入一定比例的初始特征（teleport），防止深层传播导致的过度平滑。

2. **传播公式**：`H^(k+1) = (1-α) D^(-1/2) A D^(-1/2) H^(k) + α H^(0)`，其中 α 是 teleport 概率，控制初始特征的保留比例。

3. **与 [[LightGCN]] 的联系**：[[LightGCN]] 的层组合策略可以被视为 APPNP 思想的一种体现——通过将第0层嵌入纳入最终表示，同样实现了"在长距离传播的同时保持局部性"的平衡。两者共享类似的抗过平滑机制，但 [[LightGCN]] 的均匀加权方案更为简洁，避免了额外超参数 α 的引入。

4. **谱图理论视角**：APPNP 对应 PageRank 多项式，与 SGC 的单项式滤波器和 [[LightGCN]] 的均匀加权多项式共同构成了多项式图滤波器的统一框架。

## 来源
- [[15-lightgcn.md]] — LightGCN 论文中与 APPNP 的理论对比分析

## 相关
- [[LightGCN]] — 共享抗过平滑机制，但层组合策略不同
- SGC — 同为简化 GNN 的代表工作
- [[Embedding]] — APPNP 使用的核心技术
