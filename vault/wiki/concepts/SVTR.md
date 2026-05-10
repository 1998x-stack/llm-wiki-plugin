---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags: ["AI", "OCR", "文字识别", "Vision Transformer", "深度学习", "文档处理"]
aliases:
- SVTR
- Scene Text Recognizer
- 场景文字识别器
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
- target: '[[CTC解码]]'
  type: uses
  confidence: 0.9
- target: '[[DBNet++]]'
  type: compares_to
  confidence: 0.7
supersedes: null
---

# SVTR

## 概述

SVTR（Scene Text Recognizer）是 [[PaddleOCR]] 的文字识别骨干模型，基于 Vision [[Transformer 架构]]，负责将矫正后的文字行图像转换为文字字符串。

## 关键内容

### 识别流程

```
文字行图像（48×W）
→ 特征提取（CNN + Transformer 混合）
→ 序列特征（长度为 W/4）
→ [[CTC解码]]（Connectionist Temporal Classification）
→ 文字字符串
```

输入：矫正后的文字行图像（高度固定为 48px，宽度按比例缩放）
输出：文字字符串 + 置信度

### CTC 解码的妙处

[[CTC解码]] 允许模型输出比输入序列更短的字符序列，天然处理了字符宽度不一、字符间隔不均匀等问题，不需要字符级的对齐[[标注]]。这是 SVTR 能够高效识别文字的关键机制。

### 架构特点

- **CNN + [[Transformer 架构|Transformer]] 混合**：CNN 提取局部特征，[[Transformer 架构|Transformer]] 捕获全局上下文依赖
- **固定高度输入**：文字行图像高度统一为 48px，宽度按比例缩放，便于批处理
- **序列输出**：输出长度为 W/4 的序列特征，经 CTC 解码得到最终文字

### 在 MinerU 中的应用

在 [[MinerU]] 中，SVTR 是 OCR 流水线的第三阶段——文字识别。它接收经过 [[DBNet++]] 检测和[[透视变换]]矫正后的文字行图像，输出最终的文字内容。

## 来源

- [[raw/assets/MinerU/minerU_04_ocr.md]] — MinerU 深度解析系列 · 第四篇：OCR 引擎

## 相关

- [[PaddleOCR]] — 使用 SVTR 作为文字识别模块
- [[光学字符识别]] — 所属技术领域
- [[PP-OCRv4]] — SVTR 是其中的识别组件
- [[CTC解码]] — SVTR 使用的解码方法
- [[DBNet++]] — 检测阶段的模型
