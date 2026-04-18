---
type: concept
status: active
confidence: 0.92
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [深度学习, Transformer, 归一化, 训练稳定性, LLM能力]
aliases: [层归一化, LayerNorm, LN]
relates_to: [Batch Normalization, 残差连接, Self-Attention, Transformer架构]
supersedes: null
---

# Layer Normalization

## 概述

对单个样本内部的特征维度做标准化，稳定网络中的数值分布，使训练更稳定。是 [[Transformer架构|Transformer]] 的基础组件，不依赖 batch 统计量。

## 关键内容

1. **计算方式**：对每个样本自身隐藏维度求均值 $\mu$ 和方差 $\sigma^2$，标准化后乘以可学习参数 $\gamma$（缩放）和 $\beta$（平移）。公式：$y_i = \gamma \hat{x}_i + \beta$，其中 $\hat{x}_i = (x_i - \mu)/\sqrt{\sigma^2 + \epsilon}$

2. **两种放置方式**：Post-LN（原始 [[Transformer架构|Transformer]]）将 LayerNorm 放在子层输出之后：$\text{LN}(x + \text{Sublayer}(x))$；[[Pre-LN架构|Pre-LN]]（现代大模型更常用）放在子层输入之前：$x + \text{Sublayer}(\text{LN}(x))$，深层网络训练更稳定

3. **核心优势**：不依赖 batch size，训练与推理行为一致，适合可变长度序列，适合[[AR 模型（自回归模型）|自回归]]生成（每次只处理一个样本/位置）；相比 [[Batch Normalization]] 不会混合不同样本的统计量

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-Self-Attention机制解析]] — Self-Attention 机制解析系列 QA

## 相关

- [[Batch Normalization]] — compares_to（LayerNorm 在特征维度归一化；BatchNorm 在 batch 维度归一化）
- [[残差连接]] — relates_to（LayerNorm 与残差连接配合控制数值尺度）
- [[注意力预算]] — relates_to
