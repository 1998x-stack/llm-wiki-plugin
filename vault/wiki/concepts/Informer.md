---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", "深度学习", 时间序列]
aliases: ["Informer", "Long Sequence Time-Series Forecasting", "长序列时间序列预测"]
relates_to:
  - target: "[[Transformer架构]]"
    type: depends_on
    confidence: 0.95
  - target: "[[LSTM（长短期记忆网络）]]"
    type: compares_to
    confidence: 0.8
  - target: "[[N-BEATS]]"
    type: compares_to
    confidence: 0.75
supersedes: null
---

# Informer

## 概述
Informer 由 Haoyi Zhou 等提出，获 AAAI 2021 最佳论文奖，首次将 [[Transformer架构|Transformer]] 成功应用于长序列时间序列预测（LS[[TensorFlow|TF]]），通过 ProbSparse [[Self-Attention机制|自注意力]]将复杂度从 O(L²) 降至 O(L log L)，引爆了"[[Transformer架构|Transformer]] for Time Series"研究浪潮。

## 关键内容

1. **历史背景**：[[Transformer架构|Transformer]] 在 NLP 和 CV 领域势如破竹，但在时间序列预测中迟迟未能主导。三大瓶颈：O(L²) 注意力复杂度、编码器堆叠内存瓶颈、解码器[[AR 模型（自回归模型）|自回归]]生成的误差累积。

2. **ProbSparse [[Self-Attention机制|自注意力]]**：观察到注意力分布具有稀疏性——少数 query 主导注意力权重，多数接近均匀分布。只计算"重要"的 query-key 对，将复杂度从 O(L²) 降至 O(L log L)。

3. **生成式解码器**：一次性输出整个预测序列，而非[[AR 模型（自回归模型）|自回归]]逐步生成，避免了误差累积问题。

4. **蒸馏操作**：在编码器层之间引入蒸馏，逐步压缩序列长度，进一步降低内存消耗。

5. **影响**：开启了 [[Transformer架构|Transformer]] 在时间序列预测领域的研究热潮，后续涌现 Autoformer、FEDformer、[[PatchTST]] 等一系列改进工作。

## 来源
- [[15-informer-2021-transformer-time-series]] — Informer：当 Transformer 叩开时间序列预测的大门

## 相关
- [[Transformer架构]] — depends_on
- [[LSTM（长短期记忆网络）]] — compares_to
- [[N-BEATS]] — compares_to
