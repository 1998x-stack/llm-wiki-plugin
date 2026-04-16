---
type: entity
entity_type: project
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 数据集, 评论, Amazon]
aliases: [Amazon US Reviews, Amazon Reviews Dataset]
relates_to:
  - {target: P5 论文, type: uses}
  - {target: 序列推荐, type: uses}
  - {target: 评分预测, type: uses}
supersedes: null
---

# Amazon US Reviews

## 概述
[[Amazon]] 产品评论数据集，[[P5 论文]]使用其三个子集（Sports/Beauty/Toys）进行实验验证。

## 关键内容

1. **数据集描述**：[[Amazon]] US Reviews 是 [[Amazon]] 电商平台的产品评论数据集，包含用户评分、评论文本、交互历史等信息。

2. **在 [[P5 论文|P5]] 中的使用**：[[P5 论文]] 使用了三个子集进行实验：
   - **Sports and Outdoors**：运动和户外用品评论
   - **Beauty**：美容产品评论
   - **Toys and Games**：玩具和游戏产品评论

3. **实验设置**：[[P5 论文|P5]] 在这三个数据集上评估了评分预测（[[RMSE]]/[[平均绝对误差 MAE|MAE]]）、[[序列推荐]]（HR@k/[[NDCG]]@k）、解释生成（BLEU/ROUGE）、评论摘要和直接推荐等五大任务。

4. **跨域迁移实验**：[[P5 论文|P5]] 展示了跨域推荐能力——在一个领域（如 Beauty）上预训练的模型，可以迁移到其他领域（如 Sports 或 Toys）的推荐任务上。

5. **局限性**：[[P5 论文|P5]] 的实验主要在 [[Amazon]] Reviews 的较小子集上进行，用户和物品规模相对有限。对于大规模工业场景（上亿用户和物品），[[P5 论文|P5]] 方案的可行性尚未得到充分验证。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)

## 相关
- [[P5 论文]] — 使用 Amazon US Reviews 进行实验
- [[序列推荐]] — Amazon US Reviews 支持的任务之一
- [[评分预测]] — Amazon US Reviews 支持的任务之一
