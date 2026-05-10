---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["机器学习", "计算机视觉", "特征工程"]
aliases: ["SIFT", "Scale-Invariant Feature Transform", "尺度不变特征变换"]
relates_to: ["HOG（方向梯度直方图）", "手工特征工程", "AlexNet", "支持向量机", "ILSVRC"]
supersedes: null
---

# SIFT（尺度不变特征变换）

## 概述
SIFT 是一种经典的局部图像特征描述子，对图像的尺度缩放、旋转和亮度变化保持不变，是深度学习之前[[计算]]机视觉领域最广泛使用的[[特征工程（Feature Engineering）|手工特征]]之一。

## 关键内容

1. **核心思想**：SIFT 通过检测图像中的关键点和描述其局部梯度分布来提取特征。关键步骤包括：构建高斯差分（DoG）金字塔检测极值点、精确定位关键点、分配主方向、生成 128 维描述子。
2. **不变性**：SIFT 特征对尺度缩放（不同大小的同一物体）、旋转（物体方向变化）、亮度变化（光照条件变化）具有一定的不变性，这使其在图像匹配、目标识别、三维重建等任务中非常有效。
3. **在传统 CV 中的地位**：2012 年 [[AlexNet]] 之前，SIFT 与 [[HOG（方向梯度直方图）]] 是[[计算]]机视觉最常用的[[特征工程（Feature Engineering）|手工特征]]。它们需要领域专家设计，针对特定任务有效，但无法泛化到新的视觉任务。
4. **被深度学习取代**：[[AlexNet]] 证明了[[卷积神经网络（CNN）|卷积神经网络]]可以从数据中自动学习特征，无需人工设计。深度学习学到的特征在大规模视觉任务中远超 SIFT 等[[特征工程（Feature Engineering）|手工特征]]的性能，SIFT 逐渐从主流 CV 流程中退出。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[HOG（方向梯度直方图）]] — compares_to
- [[手工特征工程]] — part_of
- [[AlexNet]] — superseded_by
- [[支持向量机]] — used_with
- [[ILSVRC]] — used_in_pre_2012
