---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags: ["AI", "OCR", "文字检测", "深度学习", "文档处理"]
aliases:
- DBNet++
- Differentiable Binarization Network++
- 可微分二值化网络++
relates_to:
- target: '[[PaddleOCR]]'
  type: uses
  confidence: 0.9
- target: '[[光学字符识别]]'
  type: part_of
  confidence: 0.9
- target: '[[PP-OCRv4]]'
  type: part_of
  confidence: 0.9
supersedes: null
---

# DBNet++

## 概述

DBNet++（Differentiable Binarization Network++）是一种基于可微分二值化的文字检测模型，是 [[PaddleOCR]] [[PP-OCRv4]] 系统中的文字检测骨干。

## 关键内容

### 工作原理

1. 输入整个页面图像（或布局框内的裁剪区域）
2. 输出与输入同尺寸的**概率图**，每个像素值表示"属于文字的概率"
3. 通过自适应阈值二值化，生成文字区域的二值蒙版
4. 轮廓提取 + 多边形拟合，得到文字区域的多边形框

```
原始图像 → ResNet/MobileNet 特征提取 → FPN 多尺度融合 
→ 概率图 + 阈值图 → 二值化蒙版 → 多边形文字框
```

### 为什么用多边形而不是矩形框？

文字行可能稍有倾斜（扫描件常见），多边形（通常是四边形）能更精确地框定文字区域，后续[[透视变换]]矫正更准确。

### 在 OCR 流水线中的位置

DBNet++ 是 OCR 三阶段流水线的第一阶段——文字区域检测。它接收原始图像，输出文字区域的多边形坐标，供后续的[[透视变换]]和文字识别使用。

### 在 MinerU 中的应用

在 [[MinerU]] 中，DBNet++ 用于：
- **OCRBased 管道**：对整页图像进行文字区域检测
- **Mixed 管道**：对无文字层的布局框区域进行文字检测
- **区域裁剪优化**：只对特定布局框内的区域做检测，大幅减少[[计算]]量

## 来源

- [[raw/assets/MinerU/minerU_04_ocr.md]] — MinerU 深度解析系列 · 第四篇：OCR 引擎

## 相关

- [[PaddleOCR]] — 使用 DBNet++ 作为文字检测模块
- [[光学字符识别]] — 所属技术领域
- [[PP-OCRv4]] — DBNet++ 是其中的检测组件
- [[SVTR]] — 检测后的文字识别模型
- [[透视变换]] — 检测后的文字矫正步骤
