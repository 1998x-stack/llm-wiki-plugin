---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [GPU, 并行计算, 深度学习训练, 硬件加速]
aliases: [GPU Training, GPU Parallel Computing, CUDA 训练]
relates_to: [AlexNet, Alex Krizhevsky, 卷积神经网络（CNN）, 反向传播（Backpropagation）]
supersedes: null
---

# GPU并行计算

## 概述
利用图形处理器（GPU）的大规模并行架构加速深度学习训练和推理的技术。

## 关键内容

1. **CUDA 编程模型**：[[NVIDIA]] CUDA 平台允许开发者利用 GPU 的数千个流并行执行[[矩阵]]运算。深度学习中的卷积、[[矩阵]]乘法等操作天然适合 GPU 的 SIMD（单指令多数据）架构。
2. **[[AlexNet]] 的里程碑意义**：2012 年 [[AlexNet]] 首次大规模使用两块 GTX 580 GPU 进行训练，将 [[ImageNet]] 训练时间从 CPU 的数周缩短至数天，证明了 GPU 在深度学习中的巨大加速潜力。
3. **现代 GPU 训练生态**：当前深度学习框架（[[PyTorch]]、[[TensorFlow]]）均原生支持 GPU 加速，多 GPU 数据并行和模型并行策略使得训练千亿参数模型成为可能。

GPU 并行[[计算]]是深度学习得以实用的关键基础设施，没有 GPU 加速，现代大模型的训练将不可行。

## 来源
- [[AlexNet]] — 首次大规模 GPU 训练实践
- [[Alex Krizhevsky]] — GPU 训练先驱

## 相关
- [[AlexNet]] — uses
- [[卷积神经网络（CNN）]] — accelerates
- [[反向传播（Backpropagation）]] — accelerates
- [[深度学习（Deep Learning）]] — enables
