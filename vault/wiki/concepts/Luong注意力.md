---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "注意力机制", "NLP", "机器翻译", "机器学习"]
aliases: ["Luong Attention", "Dot-product Attention", "点积注意力", "乘性注意力", "General Attention"]
relates_to:
  - target: "[[注意力机制（Attention Mechanism）]]"
    type: implements
    confidence: 0.9
  - target: "[[Bahdanau注意力]]"
    type: compares_to
    confidence: 0.9
  - target: "[[缩放点积注意力]]"
    type: extends
    confidence: 0.85
supersedes: null
---

# Luong注意力

## 概述

Luong 点积/乘性[[注意力机制|注意力]]以 $s^\top W h$ 替代 Bahdanau 的加性函数，参数更少、速度更快，是 [[缩放点积注意力]] 的直接前身。

## 关键内容

### 三种变体

| 类型 | 对齐函数 | 特点 |
|------|---------|------|
| **Dot（点积）** | $s^\top h$ | 无额外参数，最快 |
| **General（乘性）** | $s^\top W h$ | 折中方案，一个[[矩阵]] |
| **Concat（拼接）** | $v^\top \tanh(W[s; h])$ | 与 Bahdanau 类似 |

### 与 Bahdanau 的核心差异

1. **[[计算]]时机**：Bahdanau 在 Decoder 输入前[[计算]][[注意力机制|注意力]]；Luong 在 Decoder 状态更新后[[计算]]
2. **维度约束**：Luong 要求编码器与解码器隐藏维度相同；Bahdanau 无此限制
3. **效率**：Luong 点积变体无需额外前馈网络，速度显著快于 Bahdanau

### 演化意义

Luong [[注意力机制|注意力]]是 [[缩放点积注意力]] 的直接前身。Vaswani 等人在 [[Transformer 架构|Transformer]] 中采用的 $QK^\top / \sqrt{d}$ 正是 Luong 点积[[注意力机制|注意力]]的缩放版本，去除了 $W$ [[矩阵]]并加入维度归一化以防止高维点积过大。

## 来源

- [[Neural Machine Translation by Jointly Learning to Align and Translate (2015 论文)]] — 源文件中对比了 Luong 与 Bahdanau 注意力变体

## 相关

- [[注意力机制（Attention Mechanism）]] — implements（注意力机制的点积变体）
- [[Bahdanau注意力]] — compares_to（同年提出的加性变体，参数更多但略优）
- [[缩放点积注意力]] — extends（Luong 点积注意力的缩放改进版）
