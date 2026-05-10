---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 训练策略, RNN, GPU并行, 负采样]
aliases: [Session-Parallel Mini-Batch, 会话并行小批量, Session-Parallel Mini-Batches]
relates_to:
  - {target: GRU4Rec, type: part_of}
  - {target: 负采样, type: uses}
  - {target: 序列推荐, type: part_of}
supersedes: null
---

# Session-Parallel Mini-Batch

## 概述
[[GRU4Rec]] 提出的 RNN 训练策略，将多个会话并排放置逐步推进，充分利用 GPU 并行[[计算]]能力，避免长短不一会话带来的 padding 浪费，同时天然提供[[负采样]]机制。

## 关键内容

1. **核心机制**：将多个会话并排放置，每个 mini-batch 包含来自不同会话的同一"步骤"的事件；每步取各会话的当前事件作为输入、下一个事件作为目标；当某会话结束时，替换为新会话并重置对应位置的 GRU 隐藏状态；权重在每步都更新，而非等待整个会话完成。

2. **与传统 BPTT 的对比**：传统方式将一个会话作为一个样本，对会话内所有时间步做[[反向传播]]（BPTT）。但会话长度差异巨大（2 次到几十次点击不等），导致效率低下且实现复杂。Session-Parallel Mini-Batch 提供了一种优雅的折中方案。

3. **关键优势**：
   - **[[计算]]效率**：充分利用 GPU 并行[[计算]]能力，避免长短不一会话带来的 padding 浪费
   - **隐藏状态管理**：每个会话独立维护自己的 GRU 隐藏状态，会话结束后状态归零
   - **[[负采样]]便利**：mini-batch 中其他会话的目标物品天然作为当前会话的负样本，无需额外采样操作
   - **流行度采样**：热门物品更容易被采到作为负样本，与 popularity-based sampling 一致

4. **后续影响**：这一训练[[规范化理论|范式]]被广泛采用，成为[[序列推荐]]模型训练的标准方法之一。后续的 NARM、[[SASRec]]、[[BERT4Rec]] 等模型均采用了类似的批处理策略。

5. **工程意义**：体现了 [[GRU4Rec]] 论文务实的工程思维——将[[计算]]效率作为设计约束，而非仅追求理论优美。这种理论与实践并重的态度是论文被工业界广泛采纳的重要原因。

## 来源
- [GRU4Rec 原始论文 (arXiv)](https://arxiv.org/abs/1511.06939)

## 相关
- [[GRU4Rec]] — 提出者
- [[负采样]] — 天然提供的负采样机制
- [[序列推荐]] — 标准训练方法之一
