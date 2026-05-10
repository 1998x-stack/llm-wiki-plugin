---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["机器学习", "计算机视觉", "特征工程"]
aliases: ["HOG", "Histogram of Oriented Gradients", "方向梯度直方图"]
relates_to: ["SIFT（尺度不变特征变换）", "手工特征工程", "AlexNet", "支持向量机", "行人检测"]
supersedes: null
---

# HOG（方向梯度直方图）

## 概述
HOG 是一种经典的图像特征描述子，通过统计局部区域的梯度方向分布来描述物体形状，在行人检测等任务中表现优异，是深度学习之前的主流[[特征工程（Feature Engineering）|手工特征]]之一。

## 关键内容

1. **核心思想**：HOG 将图像划分为小的空间单元（cell），在每个单元内[[计算]]像素梯度的方向直方图。这些直方图组合起来形成特征向量，捕捉局部物体的形状和外观信息。
2. **优势**：HOG 对光照变化有较好的鲁棒性（因为使用梯度而非绝对像素值），且能捕捉物体的局部形状结构。Dalal & Triggs（2005）将 HOG 与 [[支持向量机]] 结合，在行人检测任务上取得了当时最好的结果。
3. **与传统 CV [[规范化理论|范式]]**：HOG 与 [[SIFT（尺度不变特征变换）]] 同属[[手工特征工程]]的代表。这些方法需要领域专家根据视觉任务的先验知识设计特征描述子，泛化能力有限。
4. **被深度学习取代**：[[AlexNet]]（2012）证明了[[卷积神经网络（CNN）|卷积神经网络]]可以自动学习比 HOG 更有效的特征表示。深度学习模型在大规模视觉任务中全面超越 HOG+SVM 的传统方案，HOG 逐渐退出主流应用。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[SIFT（尺度不变特征变换）]] — compares_to
- [[手工特征工程]] — part_of
- [[AlexNet]] — superseded_by
- [[支持向量机]] — used_with
