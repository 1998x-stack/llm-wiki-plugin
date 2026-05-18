---
type: concept
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [deep-learning, architecture, efficiency, AI工程]
aliases: [MoE, Mixture of Experts, 混合专家模型]
relates_to:
  - target: DeepSeek
    relation: applied_by
  - target: Transformer
    relation: extends
supersedes: null
---

# MoE（混合专家）

## 概述
通过激活部分专家网络而非全部参数实现高效推理的模型架构。

## 关键内容

1. **[[稀疏激活]]**：每次推理只激活部分专家网络，大幅降低[[计算]]成本同时保持大参数规模。
2. **[[DeepSeek]] 应用**：[[DeepSeek]]-V2/V3 使用 MoE 架构，在保持高性能的同时显著降低推理成本。
3. **与稠密模型对比**：相比 [[Transformer]] 的稠密[[计算]]，MoE 在推理效率上有显著优势。

## 来源
- [[ai_papers_timeline.md]] — 2024 年时间线条目

## 相关
- [[DeepSeek]] — applied_by
- [[Transformer]] — extends
