---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [图神经网络, 简化GCN, ICML 2019, 节点分类, 推荐系统]
aliases: [SGC, Simplified Graph Convolution]
relates_to:
  - {target: LightGCN, type: compares_to}
  - {target: APPNP, type: compares_to}
  - {target: Embedding, type: uses}
supersedes: null
---

# SGC

## 概述
Wu 等人于 ICML 2019 发表的简化图卷积论文，移除非线性激活并将多层权重[[矩阵]]压缩为一个，面向节点分类任务，与 [[LightGCN]] 共享简化思路但应用场景不同。

## 关键内容

1. **核心思想**：SGC 发现 GCN 中的非线性激活对节点分类任务的贡献有限，提出移除激活函数并将多层权重[[矩阵]]压缩为单个线性变换。公式：`H^(K) = (D^(-1/2) A D^(-1/2))^K X Θ`。

2. **与 [[LightGCN]] 的区别**：（a）SGC 面向节点分类，节点有丰富初始特征，简化的目的是提升可解释性和效率；[[LightGCN]] 面向[[协同过滤]]，节点只有 ID 嵌入，简化有更根本的理由。（b）SGC 使用最后一层嵌入做预测，[[LightGCN]] 使用所有层的加权组合。

3. **理论联系**：从谱图理论视角，SGC 对应单项式滤波器 `P_K(A) = A^K`，而 [[LightGCN]] 对应均匀加权多项式 `P(A) = (1/(K+1)) Σ_{k=0}^{K} A^k`。两者都是多项式图滤波器的特例。

4. **历史地位**：SGC 是 GNN 简化趋势的早期代表之一，为后续 [[LightGCN]] 等工作的简化思路提供了理论参考。

## 来源
- [[15-lightgcn.md]] — LightGCN 论文中与 SGC 的理论对比分析

## 相关
- [[LightGCN]] — 共享简化 GCN 思路，但面向协同过滤
- [[APPNP]] — 与 SGC 同为简化 GNN 的代表工作
- [[Embedding]] — SGC 使用的核心技术
