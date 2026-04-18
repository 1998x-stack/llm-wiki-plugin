---
type: entity
entity_type: tool
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags: ["AI", "OCR", "工具", "深度学习", "百度", "文档处理"]
aliases:
- PP-OCRv4
- PP-OCR v4
- PaddleOCR v4
relates_to:
- target: '[[PaddleOCR]]'
  type: part_of
  confidence: 0.95
- target: '[[DBNet++]]'
  type: uses
  confidence: 0.9
- target: '[[SVTR]]'
  type: uses
  confidence: 0.9
- target: '[[光学字符识别]]'
  type: implements
  confidence: 0.9
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
supersedes: null
---

# PP-OCRv4

## 概述

[[PaddleOCR|PP-OCR]]v4 是 [[PaddleOCR]] 的第四代 OCR 系统，包含文字检测、方向分类、文字识别三个子模块，是 [[MinerU]] 默认使用的 OCR 模型系列。

## 关键内容

### 系统组件

```
PP-OCRv4 系统组件：
├── 文字检测（Detection）：[[DBNet++]] 变体
│   输入：图像
│   输出：文字区域的多边形轮廓
│
├── 文字方向分类（Direction Classification）：
│   输入：检测到的文字图像块
│   输出：0° / 90° / 180° / 270°
│
└── 文字识别（Recognition）：[[SVTR]]（Scene Text Recognizer）
    输入：矫正后的文字行图像
    输出：文字字符串 + 置信度
```

### 三个子模块

1. **文字检测（[[DBNet++]]）**：基于可微分二值化的检测模型，输出文字区域的多边形轮廓
2. **文字方向分类**：判断文字图像块的方向（0°/90°/180°/270°），用于处理竖排、倒排等场景
3. **文字识别（[[SVTR]]）**：基于 Vision [[Transformer 架构|Transformer]] 的识别模型，通过 [[CTC解码]] 输出文字

### 在 MinerU 中的应用

[[MinerU]] 主要使用 [[PaddleOCR|PP-OCR]]v4 系列作为默认 OCR 引擎，原因包括：
- **中文识别极强**：专门针对中文优化，字符集包含 6763 个常用汉字（GB2312 标准）
- **速度快**：轻量级模型，区域裁剪 OCR 仅需 0.1~0.5 秒
- **检测+识别一体**：完整的 OCR 流水线
- **版式理解**：PP-Structure 支持文档[[结构力学|结构分析]]
- **工业验证**：阿里、京东等大厂使用

### 中文优化

- 字符集：6763 个常用汉字，覆盖 99% 以上常用中文场景
- 形近字处理：训练集中加入形近字混淆样本（己/已/巳，戊/戌/戍）
- 中英混排：统一字符集，同时包含中文和英文字符
- 垂直排版：方向分类器支持竖排文字识别

## 来源

- [[raw/assets/MinerU/minerU_04_ocr.md]] — MinerU 深度解析系列 · 第四篇：OCR 引擎

## 相关

- [[PaddleOCR]] — PP-OCRv4 是 PaddleOCR 的模型系列
- [[DBNet++]] — 文字检测子模块
- [[SVTR]] — 文字识别子模块
- [[光学字符识别]] — 所属技术领域
- [[MinerU]] — 使用 PP-OCRv4 作为 OCR 引擎
- [[CTC解码]] — 识别解码方法
