---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 深度学习, 用户行为建模, 时序建模]
aliases: [DIEN, Deep Interest Evolution Network]
relates_to:
  - {target: DIN, type: extends}
  - {target: CTR 预估, type: implements}
supersedes: null
---

# DIEN

## 概述
阿里巴巴于 2019 提出的 [[CTR 预估]]模型，在 DIN 基础上引入 GRU 和辅助损失，显式建模用户兴趣的时序演化过程。

## 关键内容

1. **解决 DIN 的时序缺陷** — DIN 将用户历史行为视为无序集合，忽略行为之间的时序关系和演化规律。DIEN 通过引入 GRU（Gated Recurrent Unit）结构显式捕获兴趣随时间的动态变化。
2. **兴趣抽取层（Interest Extractor Layer）** — 使用 GRU 对用户行为序列进行逐时刻编码，每个时间步输出一个兴趣状态向量，形成兴趣演化轨迹。
3. **兴趣演化层（Interest Evolving Layer）** — 引入 [[Target Attention]] 机制，让候选广告与 GRU 的每个隐藏状态进行注意力计算，动态选择与当前候选最相关的兴趣演化路径。
4. **辅助损失（Auxiliary Loss）** — 为缓解 GRU 训练中的[[梯度消失]]问题，DIEN 设计了辅助点击预测任务：在每个时间步预测用户下一个行为是否为正样本，提供额外的监督信号。
5. **与 DIN 的关系** — DIEN 保留了 DIN 的 [[Target Attention]] 机制，但在注意力计算之前先用 GRU 对行为序列进行时序编码，实现了"时序建模 + 注意力激活"的两阶段兴趣表示。
6. **后续影响** — 开启了推荐系统中序列建模的新方向，后续 DSIN、BST 等工作进一步探索了更强大的序列建模架构（如 [[Transformer架构|Transformer]]）。

## 来源
- [raw/books/推荐系统/11-din.md](raw/books/推荐系统/11-din.md)

## 相关
- DIN — DIEN 的前作，DIEN 解决了其不建模时序关系的缺陷
- [[CTR 预估]] — 应用场景
- [[Target Attention]] — DIEN 在兴趣演化层使用的注意力机制
- GRU — DIEN 使用的时序建模组件
