---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [深度学习, Transformer, 注意力机制, NLP, LLM能力]
aliases: ["Self-Attention", "自注意力", "自注意力机制", "Scaled Dot-Product Attention"]
relates_to:
  - target: "[[多头注意力]]"
    type: part_of
    confidence: 0.95
  - target: "[[Transformer架构]]"
    type: part_of
    confidence: 0.95
  - target: "[[注意力预算]]"
    type: relates_to
    confidence: 0.85
supersedes: null
---

# Self-Attention机制

## 概述

[[Self-Attention]]（自[[注意力机制|注意力]]）是 [[Transformer架构|Transformer]] 的核心机制，让序列中每个位置根据内容动态关注其他所有位置，从而获得全局上下文表示，时间复杂度为 O(n²d)。

## 关键内容

### 基本计算过程

输入[[矩阵]] $X \in \mathbb{R}^{n \times d}$（序列长度 n，维度 d）经三组线性变换映射为：

$$Q = XW_Q,\quad K = XW_K,\quad V = XW_V$$

其中 $Q, K, V \in \mathbb{R}^{n \times d_k}$。核心公式：

$$\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

**四步流程：**

1. **[[计算]][[注意力机制|注意力]]分数**：$QK^T$，结果为 $n \times n$ [[矩阵]]，表示每个位置对所有位置的相似度
2. **缩放**：除以 $\sqrt{d_k}$，防止点积值过大导致 softmax [[梯度消失]]
3. **[[Softmax]] 归一化**：对每行归一化，使权重之和为 1
4. **加权求和**：用[[注意力机制|注意力]]权重对 V 加权聚合，得到输出表示

### 直觉理解

- **Q（Query）**：我想找什么信息
- **K（Key）**：我这里有什么信息可供匹配
- **V（Value）**：真正要取出的内容

每个 token 以自身 Q 与所有 token 的 K 比较，决定从哪些位置取多少信息，再对对应 V 加权汇总。

### 计算复杂度

| 操作 | 复杂度 |
|------|--------|
| [[计算]] $QK^T$：$(n \times d)(d \times n)$ | $O(n^2 d)$ |
| [[注意力机制|注意力]]权重乘 $V$：$(n \times n)(n \times d)$ | $O(n^2 d)$ |
| **总时间复杂度** | $O(n^2 d)$，简写 $O(n^2)$ |
| **空间复杂度**（存储[[注意力机制|注意力]][[矩阵]]） | $O(n^2)$ |

$O(n^2)$ 是 [[Transformer架构|Transformer]] 处理长序列的主要瓶颈，[[注意力预算]]随序列增长而被稀释。

### 与 RNN/CNN 的对比

| 维度 | RNN | CNN | [[Self-Attention]] |
|------|-----|-----|----------------|
| 并行化 | 串行（时间步依赖） | 并行 | 全并行 |
| [[感受野]] | 全局（需多步传播） | 局部 | 天然全局 |
| 长距依赖 | 困难（[[梯度消失]]） | 困难 | 直接 |
| 复杂度（序列长度） | $O(n)$ | $O(n)$ | $O(n^2)$ |

[[Self-Attention]] 的优势：能直接建模长距离依赖，无需按顺序传播，每个位置可直接看到全局上下文。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-Self-Attention机制解析/01-解释Transformer架构中的Self-Attention机制，并说明其计算复杂度.md]] — 完整推导与复杂度分析

## 相关

- [[多头注意力]] — extends（Multi-Head Attention 是 Self-Attention 的多子空间扩展）
- [[Transformer架构]] — part_of（Self-Attention 是 Transformer 的核心模块）
- [[注意力预算]] — relates_to（n² 复杂度是注意力预算有限的架构根因）
