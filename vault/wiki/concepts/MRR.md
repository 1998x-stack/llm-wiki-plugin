---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 评估指标, 排名, 倒数排名]
aliases: [MRR, Mean Reciprocal Rank, 平均倒数排名]
relates_to:
  - {target: Recall@K, type: compares_to}
  - {target: NDCG, type: compares_to}
  - {target: 序列推荐, type: part_of}
supersedes: null
---

# MRR

## 概述
平均倒数排名指标，衡量正确物品在推荐列表中排名的倒数的均值，对排序位置敏感，是推荐系统评估中与 [[Recall@K]] 互补的核心指标。

## 关键内容

1. **定义**：MRR@K = $\frac{1}{|U|} \sum_{u \in U} \frac{1}{\text{rank}_u}$，其中 $\text{rank}_u$ 是用户 $u$ 的真实交互物品在推荐列表中的排名（若未在前 K 内则记为 0）。取值范围 [0, 1]，越高越好。

2. **与 [[Recall@K]] 的区别**：[[Recall@K]] 只关心"是否在前 K 内"，MRR 关心"排在第几位"。若正确物品排在第 1 位，MRR 贡献为 1.0；排在第 10 位，贡献仅 0.1。MRR 对排序位置更敏感。

3. **与 NDCG 的区别**：NDCG 通过折扣因子对多个相关物品的位置进行加权，适合多标签场景；MRR 通常假设每个测试样本只有一个正确物品，计算更简单。两者在单标签场景下趋势一致。

4. **在[[序列推荐]]中的应用**：[[GRU4Rec]] 使用 MRR@20 作为辅助评估指标，在 RSC15 数据集上达到 0.2164。后续研究通常报告 MRR@5、MRR@10、MRR@20 多个 K 值。

5. **直观理解**：MRR = 0.2 意味着平均而言正确物品排在第 5 位左右；MRR = 0.5 意味着平均排在第 2 位。MRR 对头部排名非常敏感，适合评估"首屏推荐"质量。

## 来源
- [GRU4Rec 原始论文 (arXiv)](https://arxiv.org/abs/1511.06939)

## 相关
- [[Recall@K]] — 互补的召回指标
- NDCG — 更细粒度的排序指标
- [[序列推荐]] — 主要应用场景
