---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, ID表示, 嵌入]
aliases: [Whole-word Embedding, 全词嵌入]
relates_to:
  - {target: P5 论文, type: part_of}
  - {target: Embedding, type: extends}
  - {target: T5, type: uses}
  - {target: 语义 ID, type: compares_to}
supersedes: null
---

# Whole-word Embedding

## 概述
[[P5 论文]]中提出的 ID 表示策略，为同一完整 ID 的所有子词单元添加共享的全词[[Embedding|嵌入向量]]，显著优于独立 token 方案。

## 关键内容

1. **问题背景**：在语言模型中表示用户和物品 ID 是一个棘手问题。[[P5 论文]] 探索了两种策略：P5-I（Independent Tokens）和 P5-S（Sub-word + Whole-word [[Embedding]]）。

2. **P5-I 策略（失败方案）**：为每个用户和物品分配一个独立的新词元（token），加入 T5 词汇表。实验证明效果较差，因为大量新引入的词元和[[Embedding|嵌入向量]]无法像原始 T5 的子词单元那样被充分训练。

3. **P5-S 策略（成功方案）**：将用户/物品 ID 作为普通文本进行分词（如 "user_1532" 分词为多个子词单元），然后引入 Whole-word [[Embedding]] 机制，为同一个完整 ID 的所有子词单元添加一个共享的全词[[Embedding|嵌入向量]]。

4. **核心优势**：既保持了 T5 原有词汇表的完整性，又赋予了 ID 特定的语义信息。允许模型通过协同学习获得更好的推荐性能，同时保持 token 数量恒定。

5. **实验验证**：在[[序列推荐]]和直接推荐任务上，P5-S 显著优于 P5-I，验证了 Whole-word [[Embedding]] 的有效性。

6. **与[[语义 ID]]的关系**：Whole-word [[Embedding]] 仍依赖数字 ID 作为基础表示，后续研究指出这与预训练语言模型的语义空间存在天然鸿沟。[[LC-Rec]] 等工作用[[语义 ID|语义标识符]]替代数字 ID，进一步解决了这一问题。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)

## 相关
- [[P5 论文]] — 提出 Whole-word Embedding 的论文
- [[Embedding]] — 嵌入表示的一般概念
- T5 — 使用 Whole-word Embedding 的基础模型
- [[语义 ID]] — 后续替代数字 ID 的方案
