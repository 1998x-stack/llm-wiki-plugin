---
type: entity
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [推荐系统, 简化模型, 协同过滤]
aliases: [SimpleX]
relates_to: 
  - {target: "LightGCN", type: compares_to}
  - {target: "协同过滤", type: implements}
supersedes: null
---

# SimpleX

## 概述
SimpleX是2021年CIKM会议上提出的[[协同过滤]]推荐方法，探索了简单损失函数设计在[[协同过滤]]中的有效性，是"简化推荐模型"趋势的代表工作之一。

## 关键内容

1. **核心理念**：
   - 探索简单损失函数在[[协同过滤]]中的有效性
   - 与[[LightGCN]]一样，体现了推荐系统领域对模型复杂度的反思
   - 通过简化损失函数设计而非复杂架构来提升推荐效果

2. **技术特点**：
   - 专注于损失函数层面的简化创新
   - 相比复杂的图神经网络架构，SimpleX采用更直接的方法
   - 在保持推荐效果的同时降低模型复杂度

3. **历史地位**：
   - 与[[UltraGCN]]同期，共同代表了2021年"简化推荐模型"趋势的延续
   - 启发于[[LightGCN]]的成功，进一步探索简化模型的有效性
   - 为推荐系统领域提供了另一种简化路径的思考

## 来源
- [[15-lightgcn.md]] — LightGCN论文深度解读中提及

## 相关
- [[LightGCN]] — 启发SimpleX的工作，同属简化模型趋势
- [[协同过滤]] — SimpleX解决的核心任务
- [[UltraGCN]] — 同期简化推荐模型工作