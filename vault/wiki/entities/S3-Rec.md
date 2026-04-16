---
type: entity
entity_type: paper
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 自监督学习, 预训练, CIKM]
aliases: [S3-Rec, Self-Supervised Learning for Sequential Recommendation]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 对比学习, type: uses}
  - {target: 自注意力机制, type: uses}
supersedes: null
---

# S3-Rec

## 概述
S3-Rec（Self-Supervised [[序列推荐|Sequential Recommendation]]），2020 年提出的 [[SASRec]] 后续工作，引入自监督预训练增强[[序列推荐]]，通过辅助任务学习更好的物品表示。

## 关键内容

1. **论文信息**：S3-Rec（Self-Supervised Learning for [[序列推荐|Sequential Recommendation]] via Contrastive Estimation），发表于 CIKM 2020。

2. **核心创新**：在 [[SASRec]] 的基础上引入自监督预训练阶段，通过四个辅助任务（Attribute Prediction, Masked Item Prediction, Segment Prediction, Maximal Association Prediction）学习物品和序列的表示，然后在下游推荐任务上进行微调。

3. **方法**：利用序列数据本身的内在关联作为监督信号，无需额外标注数据。预训练阶段学习通用的序列表示，微调阶段针对具体推荐任务优化。

4. **效果**：在多个数据集上显著超越 [[SASRec]] 基线，证明了自监督学习在[[序列推荐]]中的有效性。

## 来源
- [S3-Rec 原始论文 (CIKM 2020)](https://dl.acm.org/doi/10.1145/3340531.3411954)

## 相关
- [[SASRec]] — S3-Rec 的基础模型
- [[对比学习]] — S3-Rec 使用的学习方法
- [[序列推荐]] — S3-Rec 解决的核心场景
- [[自注意力机制]] — S3-Rec 的核心编码机制
