---
type: entity
entity_type: paper
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 对比学习, Self-Attention, WSDM]
aliases: [DuoRec, Contrastive Learning for Sequential Recommendation]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 对比学习, type: uses}
  - {target: 自注意力机制, type: uses}
supersedes: null
---

# DuoRec

## 概述
DuoRec，2022 年提出的[[对比学习]]增强的[[序列推荐]]模型，在 [[SASRec]] 架构上引入模型级和数据级的[[对比学习]]，提升表示质量和泛化能力。

## 关键内容

1. **论文信息**：DuoRec（[[对比学习|Contrastive Learning]] for [[序列推荐|Sequential Recommendation]] with Augmented Data），发表于 WSDM 2022。

2. **核心创新**：在 [[SASRec]] 的基础上引入双重[[对比学习]]——（1）模型级对比：对同一序列的不同 dropout 掩码视图进行对比；（2）数据级对比：通过采样增强生成正样本对。

3. **方法**：结合 [[InfoNCE]] 损失与[[二元交叉熵|二元交叉熵损失]]，使模型学习到更鲁棒的序列表示。[[对比学习]]帮助模型区分相似和不相似的序列模式。

4. **效果**：在多个数据集上显著超越 [[SASRec]] 基线，证明[[对比学习]]在[[序列推荐]]中的有效性。

## 来源
- [DuoRec 原始论文 (WSDM 2022)](https://dl.acm.org/doi/10.1145/3488560.3498443)

## 相关
- [[SASRec]] — DuoRec 的基础模型
- [[对比学习]] — DuoRec 的核心学习方法
- [[InfoNCE]] — DuoRec 使用的对比损失
- [[序列推荐]] — DuoRec 解决的核心场景
