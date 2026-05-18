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
由Sun等人于2019年提出的[[序列推荐]]模型，将BERT的[[BERT|双向编码器表示]]引入推荐系统，通过[[Cloze任务]]进行训练，是[[SASRec]]之后[[序列推荐]]领域的另一个重要里程碑。

## 关键内容

1. **论文信息**：标题"[[BERT4Rec]]: [[BERT4Rec|Sequential Recommendation with Bidirectional Encoder Representations from Transformer]]"，作者Fajie Sun等，发表于CIKM 2019，arXiv: 1904.06690。作为[[SASRec]]的直接后续工作，[[BERT4Rec]]采用了双向[[注意力机制]]，与[[SASRec]]的单向因果[[注意力机制|注意力]]形成对比。

2. **核心创新**：与[[SASRec]]的单向[[因果掩码]]不同，[[BERT4Rec]]使用双向[[Transformer]] Encoder，通过[[Cloze任务]]（随机掩盖序列中的某些物品，预测被掩盖的物品）进行训练。这种方法允许模型在训练时同时看到目标物品的前后上下文，理论上能捕获更丰富的序列信息。

3. **架构特点**：
   - **双向[[注意力机制|注意力]]**：与[[SASRec]]的[[因果掩码]]不同，[[BERT4Rec]]允许序列中每个位置看到所有其他位置（除了被掩盖的物品）
   - **[[Cloze任务]]**：随机掩盖序列中的部分物品，训练模型预测被掩盖的物品
   - **[[位置编码]]**：保持[[Transformer]]的位置感知能力
   - **[[AR 模型（自回归模型）|自回归]]推理**：在推理阶段采用[[AR 模型（自回归模型）|自回归]]方式，逐步预测下一个物品

4. **与[[SASRec]]的对比**：[[SASRec]] vs. [[BERT4Rec]]的争论是[[序列推荐]]领域持续时间最长的学术辩论之一。2023年的研究（"Turning Dross Into Gold Loss"）发现，[[BERT4Rec]]的优势主要来自其损失函数（全物品softmax[[交叉熵]]），而非双向[[注意力机制|注意力]]本身。当两者使用相同损失函数时，[[SASRec]]在大多数数据集上实际表现更好。

5. **实验效果**：在多个公开数据集上取得了当时的最优性能，但由于其复杂的训练策略和[[计算]]开销，实际应用中需要权衡效果与效率。

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