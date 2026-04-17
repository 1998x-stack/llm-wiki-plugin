---
type: entity
entity_type: project
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 数据集, 评论, Yelp]
aliases: [Yelp Review, Yelp Review Dataset]
relates_to:
  - {target: P5 论文, type: uses}
  - {target: 序列推荐, type: uses}
  - {target: 评分预测, type: uses}
supersedes: null
---

# Yelp Review

## 概述
Yelp 商户评论数据集，[[P5 论文]]用于实验验证的四个数据集之一。

## 关键内容

1. **数据集描述**：Yelp Review 是 Yelp 平台的商户评论数据集，包含用户评分、评论文本、商户信息等。

2. **在 P5 中的使用**：[[P5 论文]] 使用 Yelp Review 数据集评估五大推荐任务（评分预测、[[序列推荐]]、解释生成、评论摘要、直接推荐），与 [[Amazon US Reviews]] 的三个子集共同构成实验验证基础。

3. **与 [[Amazon]] 数据集的对比**：Yelp Review 侧重于本地商户和餐饮服务评论，与 [[Amazon]] 的产品评论在领域和内容风格上有显著差异，为 P5 的跨领域泛化能力提供了额外验证。

4. **实验结果**：P5 在 Yelp Review 上展示了与 [[Amazon]] 数据集一致的实验趋势——评分预测 MAE 优于传统[[矩阵分解]]，直接推荐显著优于 BPR-MF 基线。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)

## 相关
- [[P5 论文]] — 使用 Yelp Review 进行实验
- [[Amazon US Reviews]] — P5 使用的另一数据集
- [[序列推荐]] — Yelp Review 支持的任务之一
- [[评分预测]] — Yelp Review 支持的任务之一
- [[矩阵分解]] — Yelp Review 上的传统基线
- BPR — Yelp Review 上的传统基线
