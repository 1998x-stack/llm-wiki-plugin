---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["机器学习", "深度学习", "迁移学习", "计算机视觉"]
aliases: ["Transfer Learning", "迁移学习", "迁移学习（Transfer Learning）"]
relates_to: ["AlexNet", "ImageNet", "卷积神经网络（CNN）", "预训练-微调范式", "深度学习（Deep Learning）"]
supersedes: null
---

# 迁移学习（Transfer Learning）

## 概述
[[迁移学习]]将在一个任务上预训练的模型（如 [[ImageNet]] 上的 [[AlexNet]]）学到的特征表示迁移到另一个相关任务，避免从零训练，显著提升小数据集上的性能。

## 关键内容

1. **核心思想**：深度卷积网络在大规模数据集（如 [[ImageNet]]）上训练后，其低层卷积核学到的特征（边缘、纹理、颜色）具有通用性，可以迁移到其他视觉任务（医疗影像、自动驾驶、工业检测）。只需替换并微调最后几层分类头即可。
2. **[[AlexNet]] 的[[迁移学习]]实践**：[[AlexNet]] 训练完成后，其前几层作为"通用特征提取器"被广泛复用。研究者将 [[AlexNet]] 的卷积层权重冻结，仅训练新的全连接层适配目标任务，大幅减少了训练数据和[[计算]]需求。
3. **为什么有效**：视觉世界的底层特征（边缘、角点、纹理）在不同任务间高度共享。深层网络通过分层学习，从简单到抽象逐步构建表征。低层特征通用，高层特征任务特定——[[迁移学习]]利用了这一层次化结构。
4. **现代演进**：从 [[AlexNet]] 的 [[ImageNet]] 预训练，发展到 BERT 的[[Language-Model|语言模型]]预训练、CLIP 的多模态预训练。[[预训练-微调范式]]已成为深度学习的标准工作流，"预训练模型 + 微调"取代了"从零训练"。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — first_major_use_case
- [[ImageNet]] — pretraining_dataset
- [[预训练-微调范式]] — institutionalized_as
- [[卷积神经网络（CNN）]] — architecture_type
- [[深度学习（Deep Learning）]] — paradigm
