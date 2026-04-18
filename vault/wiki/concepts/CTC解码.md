---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags: ["AI", "OCR", "解码", "序列模型", "深度学习", "文档处理"]
aliases:
- CTC解码
- CTC Decoding
- Connectionist Temporal Classification
- 连接时序分类
relates_to:
- target: '[[SVTR]]'
  type: uses
  confidence: 0.9
- target: '[[PaddleOCR]]'
  type: uses
  confidence: 0.85
- target: '[[光学字符识别]]'
  type: part_of
  confidence: 0.8
supersedes: null
---

# CTC解码

## 概述

CTC（Connectionist Temporal Classification，连接时序分类）是一种序列解码方法，允许模型输出比输入序列更短的字符序列，是 [[SVTR]] 文字识别的核心解码机制。

## 关键内容

### CTC 解码的妙处

CTC 天然处理了以下问题：
- **字符宽度不一**：不同字符在图像中占据的宽度不同
- **字符间隔不均匀**：文字行中字符之间的间距不一致
- **不需要字符级对齐标注**：训练时不需要知道每个字符在图像中的精确位置

这使得 CTC 成为文字识别任务的理想解码方法。

### 在 OCR 流水线中的位置

在 [[SVTR]] 的识别流程中，CTC 解码是最后一步：

```
文字行图像（48×W）
→ 特征提取（CNN + Transformer 混合）
→ 序列特征（长度为 W/4）
→ CTC 解码
→ 文字字符串
```

CTC 接收长度为 W/4 的序列特征，输出最终的文字字符串。

### 工作原理

CTC 通过引入"空白"符号（blank），允许模型在多个时间步输出同一个字符或空白，最终通过合并重复字符和去除空白得到目标序列。这种机制避免了输入输出长度必须一致的约束。

### 在 MinerU 中的应用

在 [[MinerU]] 的 OCR 管道中，CTC 解码是 [[PaddleOCR]] [[PP-OCRv4]] 系统的关键组件，负责将 [[SVTR]] 模型输出的序列特征转换为可读的文字字符串。

## 来源

- [[raw/assets/MinerU/minerU_04_ocr.md]] — MinerU 深度解析系列 · 第四篇：OCR 引擎

## 相关

- [[SVTR]] — 使用 CTC 解码的文字识别模型
- [[PaddleOCR]] — 使用 CTC 解码的 OCR 系统
- [[光学字符识别]] — 所属技术领域
- [[PP-OCRv4]] — 包含 CTC 解码的 OCR 系统
