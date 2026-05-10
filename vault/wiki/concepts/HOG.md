---
type: concept
status: active
confidence: 0.8
created: 2026-04-21
updated: 2026-04-21
last_accessed: 2026-04-21
source_count: 1
tags: ["计算机视觉", "特征提取", "传统方法"]
aliases: ["HOG", "Histogram of Oriented Gradients", "方向梯度直方图"]
relates_to: ["手工特征工程", "SIFT", "Haar 小波", "AlexNet", "卷积神经网络（CNN）"]
supersedes: null
---

# HOG

## 概述
[[HOG（方向梯度直方图）]]是一种用于物体检测的特征描述子，通过统计图像局部区域的梯度方向分布来表征物体形状，在行人检测等任务中曾取得显著成功。

## 关键内容

1. **核心思想**：HOG 将图像划分为小的细胞单元（cell，如 8×8 像素），在每个细胞内[[计算]]梯度方向的直方图（通常 9 个 bin）。多个细胞组成一个块（block），块内直方图归一化后串联形成最终描述子。这种局部归一化使 HOG 对光照变化鲁棒。
2. **设计直觉**：物体的局部形状主要由边缘和轮廓决定，而边缘的方向信息（梯度方向）比像素强度本身更具判别力。HOG 捕捉的正是这种"形状的方向签名"。
3. **经典应用**：Dalal & Triggs（2005）将 HOG + 线性 SVM 用于行人检测，在 INRIA 数据集上取得当时最佳结果。这一组合成为 2005-2012 年间物体检测的标准基线。
4. **与深度学习的对比**：HOG 是典型的[[手工特征工程]]产物——需要专家设计、针对特定任务优化、无法泛化到新领域。[[AlexNet]]（2012）证明端到端学习的卷积特征在 [[ImageNet]] 上将 [[Top-5 错误率]]从 ~26% 降至 16.4%，HOG 等传统特征从此退出主流。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读（传统方法对比）

## 相关
- [[手工特征工程]] — exemplar_of
- [[SIFT]] — compares_to
- [[Haar 小波]] — compares_to
- [[AlexNet]] — superseded_by
- [[卷积神经网络（CNN）]] — superseded_by
