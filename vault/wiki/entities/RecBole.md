---
type: entity
entity_type: tool
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 框架, 开源, Baseline]
aliases: [RecBole 框架]
relates_to:
  - {target: BPR, type: implements}
  - {target: 矩阵分解, type: implements}
supersedes: null
---

# RecBole

## 概述
一个主流开源推荐系统框架，提供统一的基准测试平台和标准化实现，将 [[BPR]] 作为标准的 baseline 实现之一。

## 关键内容

1. **定位**：RecBole 是一个基于 PyTorch 的推荐系统统一基准测试框架，旨在提供公平、可复现的算法比较平台。涵盖传统[[协同过滤]]、深度学习推荐、图神经网络推荐等多种模型类别。

2. **[[BPR]] 实现**：RecBole 将 [[BPR]] 作为标准的 baseline 实现之一，提供 [[BPR]]-[[矩阵分解|MF]] 的标准化代码、默认超参数配置和评估流程，方便研究者在新工作中与 [[BPR]] 进行公平比较。

3. **支持的模型类别**：
   - 传统[[协同过滤]]（[[BPR]]、Neu[[矩阵分解|MF]]、Pop 等）
   - 基于内容的推荐
   - [[序列推荐]]（[[SASRec]]、[[BERT4Rec]]、[[GRU4Rec]] 等）
   - 图神经网络推荐（[[LightGCN]]、NG[[协同过滤|CF]]、SGL 等）
   - 知识图谱增强推荐

4. **评估体系**：提供统一的评估指标（[[AUC]]、[[NDCG]]、Hit Rate、[[MRR]] 等）和标准化的训练/验证/测试流程，确保不同模型之间的比较公平可信。

5. **工业价值**：RecBole 等标准化框架的出現降低了推荐系统研究的门槛，使研究者能更专注于算法创新而非工程实现。同时为工业界提供了可靠的 baseline 参考。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, 工业界广泛采用部分提及

## 相关
- [[BPR]] — implements
- [[矩阵分解]] — implements
