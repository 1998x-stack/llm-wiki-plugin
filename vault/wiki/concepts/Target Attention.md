---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 注意力机制, CTR预估, DIN]
aliases: [Target Attention, Target-aware Attention]
relates_to:
  - {target: DIN, type: part_of}
  - {target: 注意力机制, type: extends}
  - {target: Self-Attention, type: compares_to}
supersedes: null
---

# Target Attention

## 概述
以候选物品为 Query、用户历史行为为 Key 和 Value 的[[注意力机制（Attention Mechanism）|注意力机制]]，使同一用户面对不同候选时展现不同的兴趣侧面。

## 关键内容

1. **核心思想** — 在推荐场景中，用户兴趣不是固定不变的，而是随候选物品动态变化的。Target Attention 以候选物品的 [[Embedding]] 作为 Query，以用户历史行为的 [[Embedding]] 作为 Key 和 Value，[[计算]]每个历史行为与候选物品的相关性权重。
2. **与 NLP [[注意力机制|注意力]]的区别** — 在机器翻译中，[[注意力机制|注意力]]权重由解码器当前状态和编码器所有状态共同决定。而在 Target Attention 中，权重由候选广告和用户历史行为共同决定，是 target-aware 的设计。
3. **DIN 中的实现** — DIN 的[[局部激活单元]]即 Target Attention 的具体实现：$v_u(a) = \sum_{i=1}^{T} a(e_i, e_a) \cdot e_i$，其中 $a(e_i, e_a)$ 是[[注意力机制|注意力]]权重函数，$e_a$ 是候选广告 [[Embedding]]。
4. **放弃 [[Softmax]] 归一化** — DIN 刻意不在[[注意力机制|注意力]]权重上施加 [[Softmax]]，以保留兴趣强度信息。两个用户相比，浏览了 10 个相关商品的用户应该比只浏览了 1 个相关商品的用户表现出更强的兴趣。
5. **后续演进** — Target Attention 是最基础的[[注意力机制|注意力]]形式，后续工作引入了更复杂的变体：[[Self-Attention机制|Self-Attention]]（BST、[[SASRec]]）让行为序列内部元素相互关注；[[多头注意力|Multi-Head Attention]]（DSIN）通过多头机制并行捕获不同方面的兴趣；Cross-Attention 在多模态推荐中连接不同特征空间。
6. **工业影响** — Target Attention 因其简洁性和有效性，成为工业级推荐系统的默认选择。当不确定用什么方法建模用户行为时，先用 Target Attention 通常不会错。

## 来源
- [raw/books/推荐系统/11-din.md](raw/books/推荐系统/11-din.md)

## 相关
- DIN — Target Attention 的首创者
- [[注意力机制]] — Target Attention 的父类概念
- [[Self-Attention]] — 后续演进方向
- [[局部激活单元]] — Target Attention 在 DIN 中的具体实现
- BST — 用 Self-Attention 替代 Target Attention
