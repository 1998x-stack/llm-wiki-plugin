---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 序列推荐, Transformer, BERT, CIKM]
aliases: [BERT4Rec, Sequential Recommendation with Bidirectional Encoder Representations from Transformer, BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer]
relates_to:
  - {target: 序列推荐, type: implements}
  - {target: SASRec, type: compares_to}
  - {target: GRU4Rec, type: supersedes}
  - {target: 自注意力机制, type: uses}
  - {target: 位置编码, type: uses}
  - {target: NDCG, type: uses}
  - {target: SASRec+, type: compares_to}
  - {target: Cloze任务, type: uses}
  - {target: 双向注意力, type: uses}
  - {target: Transformer架构, type: uses}
supersedes: null
---

# BERT4Rec

## 概述
Sun 等人于 CIKM 2019 发表的论文，将双向 [[Transformer架构|Transformer]]（BERT 风格）和 Cloze 任务引入[[序列推荐]]，与 [[SASRec]] 形成单向 vs 双向的长期学术辩论。

## 关键内容

1. **论文信息**：标题 "BERT4Rec: [[序列推荐|Sequential Recommendation]] with Bidirectional Encoder Representations from [[Transformer架构|Transformer]]"，作者 Fei Sun 等人，发表于 CIKM 2019，arXiv: 1904.06690。作为[[SASRec]]的直接后续工作，BERT4Rec采用了双向注意力机制，与[[SASRec]]的单向因果注意力形成对比。

2. **核心创新**：与 [[SASRec]] 的单向（[[因果掩码]]）架构不同，BERT4Rec 采用双向 [[Transformer架构|Transformer]] Encoder，通过 Cloze（完形填空）任务训练——随机掩码序列中的某些物品，让模型预测被掩码的物品。这使得序列中每个位置都能利用双向上下文信息。允许模型在训练时同时看到目标物品的前后上下文，理论上能捕获更丰富的序列信息。

3. **架构特点**：
   - **双向注意力**：与[[SASRec]]的[[因果掩码]]不同，BERT4Rec允许序列中每个位置看到所有其他位置（除了被掩盖的物品）
   - **Cloze任务**：随机掩盖序列中的部分物品，训练模型预测被掩盖的物品
   - **位置编码**：保持[[Transformer架构|Transformer]]的位置感知能力
   - **自回归推理**：在推理阶段采用自回归方式，逐步预测下一个物品

4. **与 [[SASRec]] 的竞争**：[[SASRec]]（单向）vs BERT4Rec（双向）是[[序列推荐]]领域持续时间最长的学术辩论之一。2023年的研究（"Turning Dross Into Gold Loss"）发现：BERT4Rec 的优势主要来自其损失函数（全物品 softmax [[交叉熵]]），而非双向注意力本身。当两者使用相同损失函数时，[[SASRec]] 在大多数数据集上实际表现更好，且训练速度更快。

5. **架构差异**：BERT4Rec 使用双向注意力 + Cloze 训练，[[SASRec]] 使用[[因果掩码]] + [[二元交叉熵]]。BERT4Rec 在训练阶段信息利用更充分，但推理时需要额外步骤。

6. **实验效果**：在多个公开数据集上取得了当时的最优性能，但由于其复杂的训练策略和计算开销，实际应用中需要权衡效果与效率。

7. **历史地位**：与 [[SASRec]] 共同奠定了 [[Transformer架构|Transformer]] 在[[序列推荐]]中的基础架构[[规范化理论|范式]]，后续工作多在此两者基础上改进。

## 来源
- [BERT4Rec 原始论文 (CIKM 2019)](https://arxiv.org/abs/1904.06690)
- [arXiv: 1904.06690](https://arxiv.org/abs/1904.06690)

## 相关
- [[SASRec]] — 单向 Transformer 基线，长期竞争对手
- [[SASRec+]] — 证明损失函数而非架构是 BERT4Rec 优势来源
- [[序列推荐]] — BERT4Rec 解决的核心场景
- [[Cloze任务]] — BERT4Rec采用的训练任务
- [[Transformer架构]] — BERT4Rec的基础架构
- [[自注意力机制]] — BERT4Rec的核心计算机制
- [[双向注意力]] — BERT4Rec与SASRec的关键区别
- [[GRU4Rec]] — BERT4Rec 超越的 RNN 基线
- [[位置编码]] — BERT4Rec 使用位置编码补充顺序信息
