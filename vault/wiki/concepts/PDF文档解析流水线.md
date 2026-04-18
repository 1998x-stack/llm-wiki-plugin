---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags: ["文档解析", "PDF处理", "流水线架构", "信息提取", "文档处理"]
aliases:
- PDF文档解析流水线
- PDF Parsing Pipeline
- 七层流水线
relates_to:
- target: '[[MinerU]]'
  type: implements
  confidence: 0.95
- target: '[[PyMuPDF]]'
  type: uses
  confidence: 0.9
- target: '[[PaddleOCR]]'
  type: uses
  confidence: 0.9
supersedes: null
---

# PDF文档解析流水线

## 概述

PDF文档解析流水线是将打印指令格式的PDF转换为结构化语义数据的分层处理架构，通过类型判断、布局检测、专项识别、排序重建等阶段实现高保真内容还原。

## 关键内容

### 为什么需要流水线架构

PDF（Portable Document Format）本质上是一种**打印指令集**，而非语义结构化数据格式。每个字符、线段在内部存储为带坐标的图元（glyph/path），完全没有"这是标题"、"这是公式"、"这是表格"的语义信息。这导致：
- **直接文本提取**（如 [[pdfminer]]、[[PyMuPDF]]）得到乱序字符流，多栏布局、脚注、侧边栏混在一起
- **图像化 PDF**（扫描件）没有文字层，纯靠 OCR
- **公式**以图像形式存储，无法直接转 LaTeX
- **表格**的单元格边界仅靠线条暗示，结构难以还原

### 七层流水线设计

典型的 PDF 文档解析流水线包含七个阶段：

1. **PDF 类型判断 & 后端选择**：识别 PDF 是文字型、扫描件还是混合类型，选择对应处理管道（TextBased / OCRBased / MixedBased）
2. **底层 PDF 解析**：使用 [[PyMuPDF]] 等引擎提取原始 Span/Block（字符组）并将页面渲染为图像
3. **[[文档布局检测]]**：通过 [[DocLayout-YOLO]] 或 [[LayoutLMv3]] 等模型检测文本区、图像、表格、公式框的位置和类别
4. **内容专项识别**：针对不同内容类型使用专用模型——OCR（[[PaddleOCR]]）识别文字、[[公式识别]]（[[UniMERNet]]）输出 LaTeX、[[表格识别]]（[[TableMaster]]）还原结构
5. **内容块分类与属性标注**：将检测结果分类为 title / text / figure / table / formula 等语义类别
6. **[[阅读顺序重建|阅读顺序]]排序**：基于坐标与分栏分析，重建人类阅读序列，解决多栏文档的顺序问题
7. **Markdown / JSON 内容生成**：将有序内容块序列化为目标格式，输出结构化数据

### 两条核心管道

- **TextBased 管道**：PDF → [[PyMuPDF]] 提取字符坐标 → Layout 检测 → 内容识别 → 顺序排列 → 输出。适用于数字原生 PDF（LaTeX 生成、Word 导出等），文字层完整，不需要 OCR
- **OCRBased 管道**：PDF → 页面渲染为图像 → Layout 检测 → [[PaddleOCR]] 全量识别 → 内容识别 → 顺序排列 → 输出。适用于扫描件、图像型 PDF

### 核心数据结构

流水线中流转的核心数据结构是 **PDFPageInfo**，包含 page_no、width、height、raw_spans、layout_bboxes、para_blocks、table_blocks、formula_blocks、sorted_blocks 等字段。每一层往其中填充不同字段，最终 sorted_blocks 是生成 Markdown 的直接来源。

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇：整体架构全景

## 相关

- [[MinerU]] — 实现此七层流水线的具体工具
- [[PyMuPDF]] — 底层 PDF 解析引擎
- [[PaddleOCR]] — OCR 文字识别引擎
- [[UniMERNet]] — 公式识别模型
- [[TableMaster]] — 表格识别模型
- [[pdfminer]] — 传统 PDF 文本提取工具（对比）
