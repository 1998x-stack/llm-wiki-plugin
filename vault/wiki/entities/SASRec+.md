---
type: entity
entity_type: paper
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 损失函数, Self-Attention, RecSys]
aliases: [SASRec+, SASRec with improved loss]
relates_to:
  - {target: SASRec, type: extends}
  - {target: BERT4Rec, type: compares_to}
  - {target: 序列推荐, type: implements}
  - {target: 二元交叉熵, type: compares_to}
supersedes: null
---

# SASRec+

## 概述
[[SASRec]]+，2023 年提出的改进版 [[SASRec]]，通过替换损失函数为全物品 softmax [[交叉熵]]，在公平比较条件下反超 [[BERT4Rec]]，揭示了损失函数而非架构是性能差异的关键。

## 关键内容

1. **论文信息**：来源于 "Turning Dross Into Gold Loss: is [[BERT4Rec]] really better than [[SASRec]]?"（Petrov & Macdonald, RecSys 2023）。

2. **核心发现**：[[BERT4Rec]] 相比 [[SASRec]] 的优势主要来自其损失函数（全物品 softmax [[交叉熵]]），而非双向注意力本身。当 [[SASRec]] 使用相同的全物品 softmax 损失（称为 [[SASRec]]+）时，在大多数数据集上实际表现优于 [[BERT4Rec]]，且训练速度更快。

3. **方法**：将 [[SASRec]] 原始的"一正一负"[[二元交叉熵]]损失替换为全物品 softmax [[二元交叉熵|交叉熵损失]]，利用更多负样本信息进行更充分的优化。

4. **意义**：这一发现深化了对模型设计中各组件贡献的理解，提醒研究者在比较不同模型时需要控制变量（尤其是损失函数），避免将损失函数的贡献错误归因于架构差异。

## 来源
- [Turning Dross Into Gold Loss (RecSys 2023)](https://dl.acm.org/doi/10.1145/3604915.3608876)

## 相关
- [[SASRec]] — SASRec+ 的基础模型
- [[BERT4Rec]] — SASRec+ 在公平条件下反超的对手
- [[二元交叉熵]] — SASRec 原始损失，SASRec+ 替换为全物品 softmax
- [[序列推荐]] — SASRec+ 解决的核心场景
