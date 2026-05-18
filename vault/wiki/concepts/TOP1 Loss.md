---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 损失函数, 排序学习, pairwise]
aliases: [TOP1 Loss, TOP1]
relates_to:
  - {target: GRU4Rec, type: part_of}
  - {target: BPR 论文, type: compares_to}
  - {target: 负采样, type: uses}
  - {target: 序列推荐, type: part_of}
supersedes: null
---

# TOP1 Loss

## 概述
[[GRU4Rec]] 提出的 pairwise 排序损失函数，包含正负样本分数比较项和负样本分数正则化项，内置稳定性使其在更大隐藏层尺寸下表现优于 [[BPR Loss]]。

## 关键内容

1. **公式定义**：$L_{TOP1} = \frac{1}{N_S} \sum_{j=1}^{N_S} \sigma(\hat{r}_j - \hat{r}_i) + \sigma(\hat{r}_j^2)$，其中 $\hat{r}_i$ 是正样本分数，$\hat{r}_j$ 是负样本分数，$N_S$ 是负样本数量。

2. **两项组成**：
   - **第一项** $\sigma(\hat{r}_j - \hat{r}_i)$：衡量负样本分数超过正样本的程度，与 [[BPR 论文|BPR Loss]] 的第一项类似
   - **第二项** $\sigma(\hat{r}_j^2)$：对负样本分数的正则化，是 TOP1 的独特之处，确保负样本分数不会变得过大，提供内置稳定性

3. **与 [[BPR Loss]] 的对比**：
   - TOP1 使用 rmsprop 优化器时表现更好，BPR 使用 adagrad 时更稳定
   - TOP1 内置正则化使其在更大隐藏层尺寸下表现更好
   - 两者都显著优于[[二元交叉熵|交叉熵损失]]（[[交叉熵]]在100次随机实验中仅10次收敛）

4. **后续演进**：[[GRU4Rec]] v2（CIKM 2018）进一步提出 TOP1-max 和 BPR-max，将性能提升 35%。TOP1-max 在 TOP1 基础上引入 max 操作，进一步增强对 hardest negative 的关注。

5. **设计洞察**：推荐本质是排序问题而非分类问题，损失函数应优化正负样本的相对排序而非绝对分数。TOP1 的正则化项体现了在损失函数设计中融入领域知识的价值。

## 来源
- [GRU4Rec 原始论文 (arXiv)](https://arxiv.org/abs/1511.06939)
- [GRU4Rec v2 (CIKM 2018)](https://hidasi.eu/assets/pdf/gru4rec_v2_cikm18.pdf)

## 相关
- [[GRU4Rec]] — 提出者
- [[BPR 论文]] — 对比的 pairwise 损失
- [[负采样]] — 依赖负样本构建损失
- [[序列推荐]] — 主要应用场景
