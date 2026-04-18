---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "Transformer", "归一化"]
aliases: ["Pre-LN", "Pre-Normalization", "预归一化"]
relates_to:
  - target: "[[Transformer 架构]]"
    type: part_of
    confidence: 0.95
  - target: "[[Layer Normalization]]"
    type: uses
    confidence: 0.95
  - target: "[[残差连接]]"
    type: uses
    confidence: 0.9
supersedes: null
---

# Pre-LN架构

## 概述

Pre-LN（Pre-[[规范化理论|Normalization]]）是 [[Transformer 架构]] 的一种变体，将 [[Layer Normalization|LayerNorm]] 置于子层（[[Self-Attention机制|Self-Attention]]、FFN）之前而非之后，相比原版 Post-LN 训练更稳定、梯度流动更顺畅，已成为现代 [[Transformer 架构|Transformer]] 实现的标准做法。

## 关键内容

1. **Post-LN（原版 [[Transformer 架构|Transformer]]）**：`x = LayerNorm(x + Sublayer(x))`。残差相加后再归一化，深层网络中梯度需穿过 [[Layer Normalization|LayerNorm]] [[反向传播]]，易导致训练初期不稳定，需要 warmup 策略。

2. **Pre-LN（现代变体）**：`x = x + Sublayer(LayerNorm(x))`。先归一化再送入子层，残差直接绕过子层形成恒等映射通路，梯度可无损回传，训练更稳定，通常无需 warmup。

3. **代码实现**：
```python
# Pre-LN Self-Attention
normed = self.norm1(x)
attn_out, _ = self.self_attn(normed, normed, normed, mask)
x = x + dropout(attn_out)

# Pre-LN FFN
x = x + dropout(self.ffn(self.norm2(x)))
```

4. **对比**：Post-LN 最终输出质量略高但训练困难；Pre-LN 收敛更快、对超参数更鲁棒，是 [[BERT]]、[[GPT]] 等后续模型的实际选择。

## 来源

- [[raw/articles/ai-papers/machine-learning/14_transformer_2017.md]] — Transformer Encoder/Decoder 代码实现（Pre-LN 变体）

## 相关

- [[Transformer 架构]] — Pre-LN 是其现代实现的标准变体
- [[Layer Normalization]] — Pre-LN 的核心组件
- [[残差连接]] — Pre-LN 依赖残差通路保证梯度流动
