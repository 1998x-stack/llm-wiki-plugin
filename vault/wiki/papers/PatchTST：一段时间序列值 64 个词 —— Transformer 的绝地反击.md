---
type: paper
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [时间序列预测, Transformer, PatchTST, 机器学习]
aliases: ["A Time Series is Worth 64 Words", "PatchTST", "时间序列分块", "通道独立"]
relates_to: []
supersedes: null
---

# PatchTST：一段时间序列值 64 个词 —— Transformer 的绝地反击

## 概述
PatchTST 是 2023 年 ICLR 发表的重要论文，提出了一种革新性的时间序列预测方法，通过分块（Patching）和通道独立策略，解决了 Transformer 在时序建模中的效率和性能问题。

## 关键内容

1. **时代背景与核心挑战**：
   - 2022年出现的 DLinear 模型用简单线性层超越了复杂的 Transformer 变体，引发学界对 Transformer 在时序预测中有效性质疑
   - PatchTST 通过"分块输入"而非"逐点输入"的方式，重新定义了时序建模

2. **核心技术创新**：
   - **Patching（分块）**：将时间序列按固定长度切分为子序列片段（patches），每个 patch 包含多个时间步，类似于 ViT 中的图像分块
   - **通道独立（Channel Independence）**：忽略变量间关系，将每个变量视为独立序列分别处理，但共享 Transformer 权重

3. **方法优势**：
   - 保留局部语义信息：16个时间步的 patch 编码了局部趋势和短期波动
   - 大幅降低计算复杂度：自注意力计算量下降约 64 倍（$(336/42)^2 \approx 64$）
   - 扩大有效感受野：可接收更长输入序列，捕捉长周期规律

## 来源
- [[raw/books/时间序列分析/17-patchtst-2023-time-series-worth-64-words.md]] — 完整论文解读

## 相关
- [[Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting]] — extends
- [[Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting]] — relates_to
- [[DLinear: Are Transformers Effective for Time Series Forecasting]] — contradicts
- [[ViT]] — compares_to