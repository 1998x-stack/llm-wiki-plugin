---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", "深度学习", 时间序列]
aliases: ["DLinear", "Simple Linear Model for Time Series", "线性时间序列模型"]
relates_to:
  - target: "[[Informer]]"
    type: contradicts
    confidence: 0.9
  - target: "[[Transformer架构]]"
    type: contradicts
    confidence: 0.85
  - target: "[[PatchTST]]"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# DLinear

## 概述
DLinear 由[[香港中文大学]][[曾爱玲]]等提出（AAAI 2023 Oral），用一个简单到令人尴尬的线性模型击败了几乎所有 [[Transformer架构|Transformer]] [[Time Series Analysis|时间序列]]变体，引发了对"[[Transformer架构|Transformer]] 是否真的适合[[Time Series Analysis|时间序列]]预测"的深刻反思。

## 关键内容

1. **历史背景**：2021-2022 年 [[Transformer架构|Transformer]] 在[[Time Series Analysis|时间序列]]预测领域掀起"军备竞赛"——[[Informer]]、Autoformer、FEDformer 等纷纷声称取得 SOTA。学术界达成共识：[[自注意力机制]]能捕捉长距离依赖，天然适合长期预测。

2. **核心质疑**：[[自注意力机制]]是"置换不变的"（permutation-invariant），而[[Time Series Analysis|时间序列]]的核心恰恰是顺序。[[位置编码]]这种"事后补救"是否真正有效？

3. **DLinear 设计**：仅包含单层线性层 + 趋势-季节分解。将输入序列分解为趋势分量和季节分量，分别用线性层映射到预测结果。结构简单到令人尴尬。

4. **实验结果**：在多个基准数据集上全面超越 [[Informer]]、Autoformer、FEDformer 等 [[Transformer架构|Transformer]] 变体，证明"简单模型 + 正确归纳偏置 > 复杂架构"。

5. **影响**：引发了[[Time Series Analysis|时间序列]]预测领域的"[[Occam剃刀|奥卡姆剃刀]]"运动，促使研究者重新审视模型复杂度与实际收益的关系。

## 来源
- [[16-dlinear-2023-are-transformers-effective]] — 皇帝的新衣？一个线性模型掀翻了整个 Transformer 时间序列帝国

## 相关
- [[Informer]] — contradicts
- [[Transformer架构]] — contradicts
- [[PatchTST]] — compares_to
