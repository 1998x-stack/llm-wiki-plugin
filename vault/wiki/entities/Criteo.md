---
type: entity
entity_type: project
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [CTR预估, 数据集, 推荐系统]
aliases: [Criteo Dataset, Criteo Benchmark]
relates_to:
  - {target: DeepFM, type: uses}
  - {target: CTR 预估, type: part_of}
supersedes: null
---

# Criteo

## 概述
业界标准的 [[CTR 预估]] benchmark 数据集，包含 4500 万条用户点击记录，广泛用于推荐模型评估。

## 关键内容

1. **数据集规模**：包含 4500 万条用户点击记录，13 个连续特征和 26 个类别特征。训练集和测试集按 9:1 比例划分。
2. **行业标准**：几乎所有 [[CTR 预估]]研究论文都将 Criteo 作为必跑的 benchmark 数据集，是模型性能对比的基准线。
3. **[[DeepFM]] 实验结果**：在 Criteo 数据集上，[[DeepFM]] 取得 [[AUC]]=0.8016、LogLoss=0.44985 的最优性能，显著超越 LR、[[Factorization Machines|FM]]、[[FNN]]、[[Wide & Deep]] 等基线模型。
4. **现代 benchmark 参考**：多项独立 benchmark 研究（如 Zhu et al. 的 Open Benchmarking for [[CTR 预估|CTR Prediction]]）发现，在充分调参条件下，DNN、[[DeepFM]]、[[DCN]]、[[xDeepFM]] 在 Criteo 上 [[AUC]] 约为 0.814 左右，差异很小。

## 来源
- [DeepFM (IJCAI 2017)](https://arxiv.org/abs/1703.04247)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[DeepFM]] — 在该数据集上验证
- [[CTR 预估]] — 评估任务
- [[xDeepFM]] — 在该数据集上对比
- [[DCN]] — 在该数据集上对比
