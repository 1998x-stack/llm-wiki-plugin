---
type: concept
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 计算理论
aliases:
- Transformer
- Transformer 架构
- 变换器架构
relates_to:
- target: "[[Transformer 论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文中首次提出
- target: "[[自注意力机制]]"
  type: implements
  confidence: 0.99
  note: 核心计算单元
- target: "[[函数式编程]]"
  type: compares_to
  confidence: 0.6
  note: 计算的组合性
- target: "[[MapReduce]]"
  type: compares_to
  confidence: 0.6
  note: 并行化计算
supersedes: null
---

# Transformer 架构

## 概述

Transformer 是一种完全基于注意力机制的序列转换架构，由 Vaswani 等人于2017年提出，彻底摆脱了对循环和卷积的依赖。

## 关键内容

### 整体架构

- **Encoder-Decoder 框架**：编码器6层，解码器6层
- **d_model = 512**：统一维度贯穿整个模型

### 核心组件

- **[[缩放点积注意力]]**：Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
- **[[多头注意力]]**：8个头，每个 d_k = d_v = 64
- **位置感知前馈网络**：FFN(x) = max(0, xW_1 + b_1)W_2 + b_2
- **[[位置编码]]**：正弦/余弦函数
- **[[残差连接]] + [[Layer Normalization|层归一化]]**：[[Layer Normalization|LayerNorm]](x + Sublayer(x))

### 三种注意力

1. **编码器[[Self-Attention机制|自注意力]]**：每个位置关注所有输入位置
2. **解码器掩码[[Self-Attention机制|自注意力]]**：每个位置只能关注之前的位置
3. **编码器-解码器交叉注意力**：解码器回看整个输入序列

### 历史影响

- BERT（2018）：Encoder-only 路线
- GPT 系列（2018-）：Decoder-only 路线
- ViT（2020）：视觉领域
- 成为当代 AI 的"[[操作系统]]"

## 来源

- [[raw/books/计算机科学/20-vaswani-transformer.md]]

## 相关

- [[Transformer 论文]] — 首次提出
- [[自注意力机制]] — 核心计算
- [[函数式编程]] — 计算的组合性
- [[MapReduce]] — 并行化计算
