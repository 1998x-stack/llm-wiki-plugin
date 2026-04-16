---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", "深度学习", 时间序列]
aliases: ["Patch Time Series Transformer", "分块时间序列 Transformer", "64 词时间序列"]
relates_to:
  - target: "[[Transformer架构]]"
    type: depends_on
    confidence: 0.95
  - target: "[[DLinear]]"
    type: compares_to
    confidence: 0.85
  - target: "[[Informer]]"
    type: extends
    confidence: 0.8
supersedes: null
---

# PatchTST

## 概述
PatchTST 由 IBM Research 于 2023 年提出（ICLR 2023），通过将时间序列分块（Patching）输入 [[Transformer架构|Transformer]]，解决了此前 [[Transformer架构|Transformer]] 处理时间序列时"语义贫乏"和"计算爆炸"两大痛点，是 [[Transformer架构|Transformer]] 在时间序列领域的绝地反击。

## 关键内容

1. **历史背景**：2022 年 [[DLinear]] 论文证明简单线性模型可击败所有 [[Transformer架构|Transformer]] 变体，[[Transformer架构|Transformer]] 阵营士气低迷。IBM Research 团队回到根本问题：是否一开始就把数据喂错了？

2. **核心洞察**：此前 [[Transformer架构|Transformer]] 将每个时间步视为一个 token（类似 NLP 中的词），但单个时间点信息量极其有限。PatchTST 将连续时间步打包为"块"（Patch），每个块包含多个时间步，信息量大幅提升。

3. **三大创新**：
   - **Patching**：将长度为 L 的序列分为 L/P 个块，每个块包含 P 个连续时间步，将 token 数量从 L 降至 L/P
   - **通道独立**：每个变量通道独立处理，不跨通道共享注意力，减少噪声干扰
   - **语义丰富**：每个 Patch 包含局部时序模式，类似 NLP 中一个词的语义

4. **效果**：在多个基准数据集上重新确立 [[Transformer架构|Transformer]] 的 SOTA 地位，证明"不是 [[Transformer架构|Transformer]] 不行，而是我们一直在用错误的方式喂数据"。

## 来源
- [[17-patchtst-2023-time-series-worth-64-words]] — PatchTST：一段时间序列值 64 个词

## 相关
- [[Transformer架构]] — depends_on
- [[DLinear]] — compares_to
- [[Informer]] — extends
