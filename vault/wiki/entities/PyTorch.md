---
type: tool
status: active
confidence: 0.8
created: 2026-04-21
updated: 2026-04-21
last_accessed: 2026-04-21
source_count: 1
tags: ["工具", "深度学习", "框架", "Python"]
aliases: ["PyTorch", "PyTorch 框架"]
relates_to: ["AlexNet", "深度学习", "卷积神经网络（CNN）", "GPU训练", "迁移学习"]
supersedes: null
---

# PyTorch

## 概述
PyTorch 是由 Meta（原 [[Facebook]]）开发的开源深度学习框架，以动态[[计算]]图和 [[Python]]ic API 著称，是当前学术界和工业界最主流的深度学习工具之一。

## 关键内容

1. **核心设计哲学**：PyTorch 采用**动态[[计算]]图**（Define-by-Run），每次前向传播即时构建[[计算]]图，支持原生 [[Python]] 控制流（if/for/while），调试体验极佳。这与 [[TensorFlow]] 1.x 的静态图（Define-and-Run）形成鲜明对比。
2. **与 [[AlexNet]] 的关系**：虽然 [[AlexNet]] 原始实现使用 CUDA/C++（2012 年 PyTorch 尚未诞生），但 PyTorch 已成为复现和研究 [[AlexNet]] 等经典 CNN 架构的首选框架。`torchvision.models.alexnet()` 提供了预训练的 [[AlexNet]] 模型，可直接用于[[迁移学习]]。
3. **生态系统**：PyTorch 2.0 引入 `torch.compile()` 和 TorchDynamo 编译器，性能大幅提升。配套生态包括：TorchVision（[[计算]]机视觉）、TorchText（NLP）、TorchAudio（音频）、TorchServe（部署）。
4. **产业采用**：Meta 开源 PyTorch 后，迅速成为学术界首选。2023 年后，PyTorch 在论文引用率、[[GitHub]] star 数、工业部署中均超越 [[TensorFlow]]，成为深度学习事实标准。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读（PyTorch 复现代码）

## 相关
- [[AlexNet]] — implements
- [[深度学习]] — framework_for
- [[卷积神经网络（CNN）]] — supports
- [[GPU训练]] — accelerates
- [[迁移学习]] — enables
