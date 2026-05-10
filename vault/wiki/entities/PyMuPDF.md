---
type: entity
entity_type: tool
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 2
tags: [技术, 工具, 文档处理]
aliases:
- PyMuPDF
- pymupdf
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[PDF解析]]'
  type: implements
  confidence: 0.85
supersedes: null
---

# PyMuPDF

## 概述

PyMuPDF 是 MuPDF 引擎的 [[Python]] 绑定，提供高性能的 PDF 文档解析能力，可直接读取精确到亚像素的字符坐标，是 [[MinerU]] TextBased 管道的核心解析引擎。

## 关键内容

### 为什么是 PyMuPDF

PyMuPDF 底层是 **MuPDF**——业界最优秀的 PDF 渲染引擎之一（Foxit 阅读器也基于它）。相比 `pdfminer`（纯 [[Python]]，慢）和 `pypdf`（精度有限），PyMuPDF 在速度（C++ 内核）、字符精度（亚像素级）、图像渲染、字体信息、嵌入图片提取、中文 PDF 支持上全面领先。

### MinerU 使用 PyMuPDF 的三个核心操作

**操作一：页面渲染为图像**
将每页渲染为高分辨率图像（默认 [[PDF坐标系|200 DPI]]），供[[文档布局检测]]模型和[[光学字符识别]]模型推理使用。通过 `fitz.Matrix(scale, scale)` 控制缩放比例。

**操作二：提取文字 Span（带坐标）**
使用 `page.get_text("rawdict")` 提取四级嵌套结构（Page → Block → Line → Span → Char），每个 Span 携带 bbox、字体名、字号、flags 位掩码、颜色、基线坐标等完整元信息。详见[[Span层级结构]]。

**操作三：提取嵌入图像**
通过 `page.get_images(full=True)` 获取页面上的嵌入图像列表，可用于提取 PDF 中内嵌的图表。

### PDF 类型判断

在解析前，PyMuPDF 支持判断 PDF 类型以选择处理管道：
- **text_based**：>80% 页面有足够文字（>100 字符）
- **ocr_based**：<20% 页面有文字，且有大图覆盖
- **mixed**：介于两者之间

同时处理加密 PDF（`doc.authenticate()`）和损坏 PDF（异常捕获降级到图像模式）等特殊情况。

### 局限性

- 对扫描件（无文字层 PDF）无法直接提取文本，需走 OCR 管道
- 多栏布局下提取的字符流仍然是乱序的，需要后续[[阅读顺序重建]]
- 原始 Span 存在噪声（碎片化、水印、页眉页脚、重叠），需[[MinerU]]清洗

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇
- [[raw/assets/MinerU/minerU_02_pdf_parsing.md]] — MinerU 深度解析系列 · 第二篇：底层 PDF 解析引擎

## 相关

- [[MinerU]] — 使用 PyMuPDF 作为底层解析引擎
- [[PDF解析]] — 解决的问题域
- [[pdfminer]] — 同类工具，但精度较低
