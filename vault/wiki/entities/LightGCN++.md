---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 图神经网络, 协同过滤, RecSys 2024]
aliases: [LightGCN++, LightGCN Plus Plus]
relates_to:
  - {target: LightGCN, type: extends}
  - {target: 协同过滤, type: implements}
  - {target: NDCG, type: compares_to}
supersedes: null
---

# LightGCN++

## 概述
RecSys 2024 发表的 [[LightGCN]] 改进工作，在 [[LightGCN]] 基础上引入灵活的嵌入范数缩放和邻居加权策略，在 [[NDCG]]@20 上进一步提升了最高 17.81%。

## 关键内容

1. **核心改进**：[[LightGCN]] 使用均匀的层组合权重 `α_k = 1/(K+1)`，[[LightGCN]]++ 引入自适应的嵌入范数缩放（embedding norm scaling），让不同层的嵌入根据其对最终预测的贡献自动调整权重。

2. **邻居加权**：在邻域聚合中，不再使用简单的对称归一化 `1/√(|N_u|·|N_i|)`，而是引入可学习的邻居权重，使模型能区分不同邻居节点的重要性。

3. **实验结果**：在多个数据集上，[[LightGCN]]++ 相比 [[LightGCN]] 在 [[NDCG]]@20 上最高提升 17.81%，验证了均匀权重和简单邻居加权确实不是最优选择。

4. **与 [[LightGCN]] 的关系**：不是推翻 [[LightGCN]] 的设计，而是在其简洁框架上增加适度的灵活性。体现了"在正确的基础上做增量改进"的研究思路。

## 来源
- [[15-lightgcn.md]] — LightGCN 论文中提及的后续改进工作

## 相关
- [[LightGCN]] — LightGCN++ 的直接前身
- [[NDCG]] — LightGCN++ 的主要评估指标
- [[协同过滤]] — LightGCN++ 解决的核心任务
