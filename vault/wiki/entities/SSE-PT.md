---
type: entity
entity_type: paper
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 个性化嵌入, Transformer, RecSys]
aliases: [SSE-PT, Personalized Transformer for Sequential Recommendation]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 嵌入表示, type: uses}
supersedes: null
---

# SSE-PT

## 概述
SSE-PT（Personalized [[Transformer架构|Transformer]] for [[序列推荐|Sequential Recommendation]]），2020 年提出的 [[SASRec]] 后续工作，在 [[Transformer架构|Transformer]] 中引入个性化嵌入，增强用户特定行为模式的建模能力。

## 关键内容

1. **论文信息**：SSE-PT（[[序列推荐|Sequential Recommendation]] with Personalized [[Transformer架构|Transformer]]），发表于 RecSys 2020。

2. **核心创新**：在 [[SASRec]] 的 [[Transformer架构|Transformer]] 架构中引入个性化嵌入（Personalized [[Embedding]]），使模型能够捕获用户特定的行为模式，而非仅学习全局的物品转移关系。

3. **方法**：为每个用户学习一个个性化偏置向量，与物品嵌入和[[位置编码|位置嵌入]]结合后输入[[Self-Attention机制|自注意力]]层。这使得同一物品在不同用户的序列中具有不同的表示。

4. **效果**：在多个数据集上超越 [[SASRec]]，证明个性化建模在[[序列推荐]]中的重要性。

## 来源
- [SSE-PT 原始论文 (RecSys 2020)](https://dl.acm.org/doi/10.1145/3383313.3412240)

## 相关
- [[SASRec]] — SSE-PT 的基础模型
- [[嵌入表示]] — SSE-PT 引入个性化嵌入
- [[序列推荐]] — SSE-PT 解决的核心场景
