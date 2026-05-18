---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [计算机视觉, 特征提取, 传统方法, 小波分析, 机器学习]
aliases: ["Haar 小波", "Haar Wavelet", "Haar-like 特征"]
relates_to: ["特征工程（Feature Engineering）", "计算机视觉", "AlexNet", "SIFT（尺度不变特征变换）", "HOG（方向梯度直方图）"]
supersedes: null
---

# Haar 小波

## 概述
Haar 小波是最简单的小波变换基函数，其衍生出的 Haar-like 特征在 Viola-Jones 人脸检测框架中广泛应用，是深度学习前最成功的视觉特征之一。

## 关键内容

1. **数学基础**：Haar 小波是最早的小波基（1909 年由 Alfréd Haar 提出），由简单的阶梯函数构成。在图像处理中，Haar-like 特征通过[[计算]]相邻矩形区域的像素差值来捕获边缘、线条和纹理等局部模式。
2. **Viola-Jones 人脸检测**：2001 年，Viola 和 Jones 将 Haar-like 特征与 AdaBoost 级联分类器结合，实现了实时人脸检测。这是[[计算]]机视觉史上最有影响力的工作之一，被广泛应用于数码相机、手机等设备。
3. **与深度学习的对比**：Haar-like 特征是[[特征工程（Feature Engineering）]]的典型案例——通过人工设计矩形模式来检测特定视觉模式。其局限在于：(1) 仅适用于特定任务（如人脸检测）；(2) 无法泛化到复杂的多类别识别任务。[[AlexNet]] 证明了深度网络可以自动学习远超手工设计的特征。
4. **历史地位**：Haar 小波/Viola-Jones 代表了[[特征工程（Feature Engineering）|手工特征]]+传统机器学习（AdaBoost）的经典[[规范化理论|范式]]。深度学习时代后，端到端学习的方式取代了这种分阶段设计。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[特征工程（Feature Engineering）]] — exemplar_of
- [[计算机视觉]] — used_in
- [[AlexNet]] — superseded_by
- [[SIFT（尺度不变特征变换）]] — related_technique
- [[HOG（方向梯度直方图）]] — related_technique
