---
type: map
topic: "LLM能力"
page_count: 16
updated: 2026-04-16
---

# LLM能力

## 概述

LLM能力 相关概念与实体的集群。核心主题：Batch Normalization、Beam Search 生成、Layer Normalization、Mixture-of-Experts。

## 概念

- [[Batch Normalization]] — 在一个 batch 上对某一特征维度统计均值和方差并做归一化。在 CNN 中广泛使用，但不适合 [[Transformer架构|Transformer]] 的序 (confidence: 0.88)
- [[Beam Search 生成]] — [[P5 论文]]使用的推理方法，通过 beam size=20 的束搜索自回归生成物品 ID 或文本，是 LLM 推荐的核心推理范式。 (confidence: 0.8)
- [[Layer Normalization]] — 对单个样本内部的特征维度做标准化，稳定网络中的数值分布，使训练更稳定。是 [[Transformer架构|Transformer]] 的基础组件，不依赖 bat (confidence: 0.92)
- [[Mixture-of-Experts]] — Mixture-of-Experts(MoE)是一种深度学习架构，训练多个小型专家网络处理输入空间不同区域，通过门控网络决定各专家意见的权重。 (confidence: 0.85)
- [[Self-Attention机制]] — Self-Attention（自注意力）是 [[Transformer架构|Transformer]] 的核心机制，让序列中每个位置根据内容动态关注其他所有位置 (confidence: 0.9)
- [[Transformer架构]] — Transformer 是 2017 年提出的序列到序列神经网络架构，以 [[Self-Attention机制]] 替代 RNN 的顺序传播，实现完全并行的全局 (confidence: 0.85)
- [[令牌计数（Token Counting）]] — Anthropic API 的 `/v1/messages/count_tokens` 端点，用于在发送消息给 Claude 前估算输入令牌数量，帮助主动管理速 (confidence: 0.85)
- [[位置编码]] — 位置编码（Positional Encoding）是 [[Transformer架构|Transformer]] 中补充序列顺序信息的机制。[[Self-Att (confidence: 0.92)
- [[因果掩码]] — 因果掩码（Causal Masking）是 [[Transformer架构|Transformer]] 中实现自回归预测的关键技术，通过下三角掩码[[矩阵]]确 (confidence: 0.9)
- [[多头注意力]] — 多头注意力（Multi-Head Attention）在 h 个独立子空间中并行执行 [[Self-Attention机制]]，再拼接并线性变换，使模型同时捕获 (confidence: 0.9)
- [[残差连接]] — 将子层输入直接加到子层输出上：$x + \text{Sublayer}(x)$，缓解深层网络梯度消失问题，是 [[Transformer架构|Transform (confidence: 0.85)
- [[相对位置编码]] — 相对[[位置编码]]关注两个 token 之间相隔多远，而非各自处于第几位。位置信息直接注入注意力分数计算，使模型在决定"该关注谁"时显式考虑相对距离 $i-j (confidence: 0.9)
- [[绝对位置编码]] — 绝对[[位置编码]]直接告知模型当前 token 处于第几个位置。分固定式（正弦/余弦公式）和可学习式两种，是原始 [[Transformer架构|Transf (confidence: 0.9)
- [[缩放点积注意力]] — 缩放点积注意力（Scaled Dot-Product Attention）是 [[Transformer架构|Transformer]] 的核心计算单元，通过  (confidence: 0.88)
- [[自注意力机制]] — [[Self-Attention机制|Self-Attention]]（[[Self-Attention机制|自注意力]]）是 [[Transformer架构| (confidence: 0.88)

## 实体

- [[T5]] — [[Google]] 提出的 Text-to-Text Transfer [[Transformer架构|Transformer]]，将所有 NLP 任务统一为 (confidence: 0.9)
