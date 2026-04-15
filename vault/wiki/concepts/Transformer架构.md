---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [深度学习, NLP, 大模型, 序列建模]
aliases: ["Transformer", "变换器架构", "Transformer model"]
relates_to:
  - target: "[[Self-Attention机制]]"
    type: depends_on
    confidence: 0.95
  - target: "[[多头注意力]]"
    type: depends_on
    confidence: 0.95
  - target: "[[注意力预算]]"
    type: relates_to
    confidence: 0.85
supersedes: null
---

# Transformer架构

## 概述

Transformer 是 2017 年提出的序列到序列神经网络架构，以 [[Self-Attention机制]] 替代 RNN 的顺序传播，实现完全并行的全局上下文建模，成为现代大语言模型的基础架构。

## 关键内容

### 核心设计思想

Transformer 的关键创新是用 [[Self-Attention机制]] 取代 RNN 的循环结构：

- **RNN**：时间步串行，难以并行；长距依赖靠梯度传播，易丢失
- **Transformer**：每层所有位置同时计算，直接建模全局上下文

核心模块：
1. **[[多头注意力]]（[[多头注意力|Multi-Head Attention]]）**：并行多子空间注意力
2. **前馈网络（FFN）**：逐位置的非线性变换
3. **[[Layer Normalization|层归一化]]（[[Layer Normalization|LayerNorm]]）**：稳定训练
4. **[[残差连接]]**：缓解梯度消失

### 计算瓶颈

[[Self-Attention机制|Self-Attention]] 的注意力[[矩阵]]大小为 $n \times n$（n 为序列长度），导致：

- 时间复杂度：$O(n^2 d)$
- 空间复杂度：$O(n^2)$

这是 Transformer 处理超长序列的主要障碍，也是 [[注意力预算]] 概念的架构根因。各类改进（Sparse Attention、Flash Attention、线性注意力）均以降低此复杂度为目标。

### 与 RNN/CNN 的比较

| | RNN | CNN | Transformer |
|--|-----|-----|-------------|
| 并行度 | 低（顺序） | 高（局部） | 高（全局） |
| 长距依赖 | 弱 | 弱 | 强 |
| 序列复杂度 | $O(n)$ | $O(n)$ | $O(n^2)$ |
| 适用场景 | 流式、短序列 | 局部模式 | 全局上下文建模 |

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-Self-Attention机制解析/01-解释Transformer架构中的Self-Attention机制，并说明其计算复杂度.md]] — 架构概述与复杂度对比

## 相关

- [[Self-Attention机制]] — depends_on（Self-Attention 是 Transformer 的核心）
- [[多头注意力]] — depends_on（MHA 是 Transformer 的标准注意力形式）
- [[注意力预算]] — relates_to（n² 复杂度是注意力预算有限的架构根因）
