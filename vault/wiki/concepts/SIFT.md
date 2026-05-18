---
type: concept
status: active
confidence: 0.8
created: 2026-04-21
updated: 2026-04-21
last_accessed: 2026-04-21
source_count: 1
tags: [计算机视觉, 特征提取, 传统方法, 机器学习]
aliases: ["SIFT", "Scale-Invariant Feature Transform", "尺度不变特征变换"]
relates_to: ["手工特征工程", "HOG", "Haar 小波", "AlexNet", "卷积神经网络（CNN）"]
supersedes: null
---

# SIFT

## 概述
[[SIFT（尺度不变特征变换）]]是一种经典的局部特征描述子[[算法]]，能够在不同尺度、旋转和光照条件下检测和描述图像关键点，是深度学习时代前最成功的视觉特征之一。

## 关键内容

1. **核心思想**：SIFT 通过构建高斯金字塔检测尺度空间极值点（DoG 算子），为每个关键点分配主方向（实现旋转不变性），然后提取 128 维特征描述子。整个过程完全基于图像局部梯度统计，无需任何训练数据。
2. **三大不变性**：**尺度不变性**——通过高斯金字塔和多尺度 DoG 检测，同一物体在不同距离下能被识别；**旋转不变性**——基于梯度方向直方图确定主方向，描述子相对主方向[[计算]]；**光照不变性**——描述子归一化后对线性光照变化鲁棒。
3. **与深度学习的对比**：在 [[AlexNet]]（2012）之前，SIFT + SVM/词袋模型是[[计算]]机视觉的主流[[规范化理论|范式]]。SIFT 需要领域专家设计，泛化能力有限——它擅长局部匹配但不擅长高层语义理解。[[AlexNet]] 证明端到端学习的特征远优于手工设计的 SIFT，[[Top-5 错误率]]从 ~26% 降至 16.4%。
4. **遗留价值**：尽管被深度学习取代，SIFT 在特定场景仍有应用：3D 重建（SfM）、图像拼接、小样本匹配、以及作为深度学习模型的辅助特征。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读（传统方法对比）

## 相关
- [[手工特征工程]] — exemplar_of
- [[HOG]] — compares_to
- [[Haar 小波]] — compares_to
- [[AlexNet]] — superseded_by
- [[卷积神经网络（CNN）]] — superseded_by
