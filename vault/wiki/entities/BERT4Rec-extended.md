---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 序列推荐, Transformer, Self-Attention]
aliases: [BERT4Rec, BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer]
relates_to:
  - {target: SASRec, type: compares_to}
  - {target: Transformer架构, type: uses}
  - {target: 序列推荐, type: implements}
  - {target: Cloze任务, type: uses}
  - {target: 自注意力机制, type: uses}
  - {target: 双向注意力, type: uses}
supersedes: null
---

# BERT4Rec

## 概述
由Sun等人于2019年提出的序列推荐模型，将BERT的双向编码器表示引入推荐系统，通过Cloze任务进行训练，是SASRec之后序列推荐领域的另一个重要里程碑。

## 关键内容

1. **论文信息**：标题"BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer"，作者Fajie Sun等，发表于CIKM 2019，arXiv: 1904.06690。作为SASRec的直接后续工作，BERT4Rec采用了双向注意力机制，与SASRec的单向因果注意力形成对比。

2. **核心创新**：与SASRec的单向因果掩码不同，BERT4Rec使用双向Transformer Encoder，通过Cloze任务（随机掩盖序列中的某些物品，预测被掩盖的物品）进行训练。这种方法允许模型在训练时同时看到目标物品的前后上下文，理论上能捕获更丰富的序列信息。

3. **架构特点**：
   - **双向注意力**：与SASRec的因果掩码不同，BERT4Rec允许序列中每个位置看到所有其他位置（除了被掩盖的物品）
   - **Cloze任务**：随机掩盖序列中的部分物品，训练模型预测被掩盖的物品
   - **位置编码**：保持Transformer的位置感知能力
   - **自回归推理**：在推理阶段采用自回归方式，逐步预测下一个物品

4. **与SASRec的对比**：SASRec vs. BERT4Rec的争论是序列推荐领域持续时间最长的学术辩论之一。2023年的研究（"Turning Dross Into Gold Loss"）发现，BERT4Rec的优势主要来自其损失函数（全物品softmax交叉熵），而非双向注意力本身。当两者使用相同损失函数时，SASRec在大多数数据集上实际表现更好。

5. **实验效果**：在多个公开数据集上取得了当时的最优性能，但由于其复杂的训练策略和计算开销，实际应用中需要权衡效果与效率。

## 来源
- [BERT4Rec原始论文 (CIKM 2019)](https://dl.acm.org/doi/10.1145/3357384.3357870)
- [arXiv: 1904.06690](https://arxiv.org/abs/1904.06690)

## 相关
- [[SASRec]] — BERT4Rec的直接对比模型，单向自注意力
- [[序列推荐]] — BERT4Rec解决的核心场景
- [[Cloze任务]] — BERT4Rec采用的训练任务
- [[Transformer架构]] — BERT4Rec的基础架构
- [[自注意力机制]] — BERT4Rec的核心计算机制
- [[双向注意力]] — BERT4Rec与SASRec的关键区别