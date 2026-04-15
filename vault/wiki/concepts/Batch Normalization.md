---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [深度学习, 归一化, CNN, 训练稳定性]
aliases: [批归一化, BatchNorm, BN]
relates_to: [Layer Normalization, 残差连接]
supersedes: null
---

# Batch Normalization

## 概述

在一个 batch 上对某一特征维度统计均值和方差并做归一化。在 CNN 中广泛使用，但不适合 [[Transformer架构|Transformer]] 的序列建模场景。

## 关键内容

1. **计算方式**：跨 batch 中所有样本，对同一特征位置统计均值和方差，再做标准化。训练时使用 batch 内统计量，推理时使用历史移动平均统计量，两者行为不一致

2. **适用场景**：在 batch size 较大、输入尺寸固定的 CNN 图像任务中效果好，能有效稳定激活值分布，加速收敛

3. **不适合 [[Transformer架构|Transformer]] 的原因**：序列长度可变导致 batch 统计不稳定；长序列致 batch size 小，统计噪声大；不同位置 token 语义差异大不宜混合统计；训练/推理行为不一致；自回归生成场景单样本推理时无法正常工作

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-Self-Attention机制解析]] — Self-Attention 机制解析系列 QA

## 相关

- [[Layer Normalization]] — compares_to（Transformer 选择 LayerNorm 而非 BatchNorm 的核心对比）
- [[残差连接]] — relates_to
