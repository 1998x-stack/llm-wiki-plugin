---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "优化", "优化器", "正则化"]
aliases: ["AdamW", "Adam with Weight Decay", "解耦权重衰减"]
relates_to: ["Adam（自适应矩估计）", "权重衰减", "L2 正则化", "Transformer 架构"]
supersedes: null
---

# AdamW

## 概述 (50-200字符)
AdamW 修正了 Adam 中[[权重衰减（Weight Decay）|权重衰减]]的实现方式，将[[权重衰减（Weight Decay）|权重衰减]]与梯度步骤解耦。[[Transformer 架构|Transformer]] 系列模型的标准优化器，配合 Warmup+Cosine 调度成为现代 LLM 训练标配。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题**：在原始[[Adam（自适应矩估计）]]中，[[权重衰减（Weight Decay）|权重衰减]]通过梯度添加 L2 正则项实现（grad += λ·w）。但这与自适应学习率耦合——大梯度参数的有效学习率小，[[权重衰减（Weight Decay）|权重衰减]]也被缩小，导致正则化效果不均匀。不同参数受到的正则化强度实际不同。
2. **解耦方案**：AdamW（Loshchilov & Hutter, 2019）将[[权重衰减（Weight Decay）|权重衰减]]直接作用于参数（w -= η·λ·w），与梯度步骤完全解耦。所有参数受到相同比例的[[权重衰减（Weight Decay）|权重衰减]]，不受自适应学习率影响。这使[[权重衰减（Weight Decay）|权重衰减]]回归其本意——直接缩小参数值。
3. **实践[[Settings|设置]]**：[[Transformer 架构|Transformer]]/NLP 任务推荐 lr=1e-4~3e-4, weight_decay=0.01，配合 Warmup（学习率线性增长到峰值）和 Cosine Annealing（余弦衰减到最小值）。梯度裁剪（clip_grad_norm）防止梯度爆炸，是 [[Transformer 架构|Transformer]] 训练的必备组件。
4. **效果**：AdamW 在[[Language-Model|语言模型]]、视觉 [[Transformer 架构|Transformer]]（ViT）、[[扩散模型]]等场景中显著优于原始 Adam。[[权重衰减（Weight Decay）|权重衰减]]的解耦实现提供了更稳定的正则化，配合学习率调度可达到更好的泛化性能。

## 来源
- [Loshchilov, I., & Hutter, F. (2019). Decoupled weight decay regularization. ICLR 2019.] — AdamW 论文
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件中的 AdamW 描述

## 相关
- [[Adam（自适应矩估计）]] — improves
- [[L2 正则化]] — decouples_from
- [[Transformer 架构]] — standard_optimizer
- [[权重衰减]] — correct_implementation
