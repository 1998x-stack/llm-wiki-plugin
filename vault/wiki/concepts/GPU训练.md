---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["机器学习", "深度学习", "硬件", "训练"]
aliases: ["GPU Training", "GPU 加速训练", "GPU 并行训练"]
relates_to: ["AlexNet", "NVIDIA", "深度学习", "卷积神经网络（CNN）"]
supersedes: null
---

# GPU训练

## 概述
GPU 训练利用图形处理器的并行[[计算]]能力加速深度神经网络的训练过程。[[AlexNet]] 首次大规模验证了 GPU 在深度学习中的革命性价值。

## 关键内容

1. **[[AlexNet]] 的 GPU 实践**：[[AlexNet]] 使用两块 [[NVIDIA]] GTX 580 GPU（各 3GB 显存）进行并行训练。网络被分为两半分别运行在两个 GPU 上，通过特定的层间通信机制同步。训练时间从 CPU 的数月缩短至 5-6 天。
2. **为什么 GPU 适合深度学习**：深度神经网络的核心运算——[[矩阵]]乘法和卷积——是高度并行的。GPU 拥有数千个[[计算]]核心，可以同时处理大量独立运算，而 CPU 只有少数核心，适合串行任务。
3. **算力之门**：[[AlexNet]] 证明了 GPU 可以将原本不可行的大规模深度学习训练变为现实。这为整个深度学习领域打开了算力之门，此后 GPU 成为 AI 训练的标准硬件。
4. **现代演进**：从 [[AlexNet]] 时代的 GTX 580（3GB 显存），到 [[NVIDIA]] A100（80GB HBM2）、H100（80GB HBM3），GPU 显存和算力呈指数增长。现代大[[Language-Model|语言模型]]训练需要数百甚至数千块 GPU 并行运行。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — pioneered_by
- [[NVIDIA]] — hardware_provider
- [[深度学习]] — enabled
- [[卷积神经网络（CNN）]] — accelerated
