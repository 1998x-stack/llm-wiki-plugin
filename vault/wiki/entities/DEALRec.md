---
type: entity
entity_type: project
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 数据剪枝, 训练效率]
aliases: [DEALRec]
relates_to:
  - {target: P5 论文, type: extends}
  - {target: 生成式 LLM 推荐, type: part_of}
  - {target: 多任务学习, type: uses}
supersedes: null
---

# DEALRec

## 概述
通过数据剪枝方法提升 LLM 推荐的训练效率，减少冗余训练数据同时保持推荐性能。

## 关键内容

1. **核心问题**：LLM 推荐模型（如 [[P5 论文|P5]] 范式）需要大量训练数据，但并非所有数据对模型学习都有同等贡献。DEALRec 通过数据剪枝识别和保留最有价值的训练样本。

2. **技术方法**：通过数据剪枝（data pruning）方法筛选训练数据，去除冗余或低信息量的样本，提升 LLM 推荐的训练效率。

3. **在 LLM 推荐谱系中的位置**：属于[[生成式 LLM 推荐]]范式，关注训练效率优化，与 [[TALLRec]]、[[InstructRec]]、[[LC-Rec]] 等工作共同推动了 LLM 推荐的实用化。

4. **实际意义**：对于大规模工业场景，数据剪枝可以显著降低训练成本，使 LLM 推荐方案更具可行性。

## 来源
- DEALRec 论文 — Data Pruning for Efficient LLM-based Recommendation
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[P5 论文]] — DEALRec 的思想来源
- [[生成式 LLM 推荐]] — DEALRec 所属范式
- [[多任务学习]] — DEALRec 优化的训练策略
- [[TALLRec]] — 同期的 LLM 推荐工作
- [[InstructRec]] — 同期的 LLM 推荐工作
