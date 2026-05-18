---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 2
tags:
- 技术
- AI
- 文档处理
aliases:
- PDF Parsing
- PDF Document Parsing
relates_to:
- target: '[[MinerU]]'
  type: implements
  confidence: 0.95
- target: '[[PyMuPDF]]'
  type: implements
  confidence: 0.85
- target: '[[pdfminer]]'
  type: implements
  confidence: 0.8
- target: '[[Marker]]'
  type: implements
  confidence: 0.8
- target: '[[Nougat]]'
  type: implements
  confidence: 0.8
- target: '[[检索增强生成]]'
  type: depends_on
  confidence: 0.85
- target: '[[PDF内容流]]'
  type: part_of
  confidence: 0.95
- target: '[[PDF坐标系]]'
  type: part_of
  confidence: 0.9
- target: '[[Span层级结构]]'
  type: part_of
  confidence: 0.9
- target: '[[MinerUSpan格式]]'
  type: relates_to
  confidence: 0.85
supersedes: null
---

# PDF解析

## 概述

PDF 解析是从 Portable Document Format 文件中提取结构化文本和语义信息的技术。PDF 本质上是"打印指令集"而非语义结构，解析的核心挑战在于还原[[阅读顺序重建|阅读顺序]]、公式、表格等高层语义。

## 关键内容

### 问题的根源

PDF 内部将每个字符、每条线段存储为带坐标的图元（glyph/path），**没有**"这是标题"、"这是公式"、"这是表格"这样的语义信息。这导致：

- **直接文本提取**得到的是乱序字符流，多栏布局、脚注、侧边栏全部混在一起
- **图像化 PDF**（扫描件）根本没有文字层，纯靠 OCR
- **公式**以图像形式存储，无法直接转成 LaTeX
- **表格**的单元格边界仅靠线条暗示，结构难以还原

### 大模型时代的重要性

[[RAG 系统]]、知识库构建、文档问答，全都依赖**精准的文本提取**。PDF 解析质量直接决定下游应用的上限。

### 主要工具对比

| 工具 | 文字型 PDF | 扫描件 | 公式→LaTeX | 表格结构 | [[阅读顺序重建|阅读顺序]] | 中文支持 |
|------|-----------|--------|-----------|---------|---------|---------|
| [[pypdf]]/[[pdfminer]] | ✅ 但乱序 | ❌ | ❌ | ❌ | ❌ | ⚠️ |
| [[PyMuPDF]] | ✅ | ❌ | ❌ | ❌ | ❌ | ⚠️ |
| [[Marker]] | ✅ | ✅ | ⚠️ 有限 | ⚠️ | ✅ | ⚠️ |
| [[Nougat]] | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| [[MinerU]] | ✅ 高质量 | ✅ OCR | ✅ [[UniMERNet]] | ✅ [[TableMaster]] | ✅ 多栏 | ✅ 极佳 |

### 解决路径

现代高质量 PDF 解析采用**多模型协同流水线**：布局检测 → 内容专项识别（OCR/公式/表格）→ [[阅读顺序重建]] → 结构化输出。

### 渲染参数选择

PDF 页面渲染为图像时，分辨率直接影响准确率与速度：

| DPI | 分辨率（A4） | 适用场景 | 显存占用 |
|-----|------------|---------|---------|
| 72 | 595×842 | 仅预览 | 低 |
| 150 | 1240×1754 | 基础 OCR | 中 |
| **200** | **1654×2339** | **[[MinerU]] 默认** | 中 |
| 300 | 2480×3508 | 高精度 OCR | 高 |

200 DPI 是准确率与速度的平衡点。

### 原始数据噪声

从 PDF 提取的原始数据存在多种噪声：
1. **超短碎片**：单字符/空格级别的过度分割，需同行合并
2. **水印文字**：旋转、半透明、大面积覆盖，通过颜色和旋转角度检测
3. **页眉页脚**：固定区域重复出现，在布局检测阶段标记过滤
4. **重叠 Span**：PDF 生成工具产生的内容重复，需去重

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇
- [[raw/assets/MinerU/minerU_02_pdf_parsing.md]] — MinerU 深度解析系列 · 第二篇：底层 PDF 解析引擎

## 相关

- [[MinerU]] — 高质量 PDF 解析工具
- [[文档布局检测]] — PDF 解析的关键环节
- [[光学字符识别]] — 扫描件 PDF 的文字提取手段
- [[公式识别]] — 公式还原为 LaTeX 的技术
- [[表格识别]] — 表格结构还原技术
- [[阅读顺序重建]] — 多栏文档的序列重建
- [[检索增强生成]] — PDF 解析的主要下游应用
- [[PDF内容流]] — PDF 内部的数据结构本质
- [[PDF坐标系]] — 坐标参照系统
- [[Span层级结构]] — 文字提取的嵌套结构
- [[MinerUSpan格式]] — MinerU 的内部数据格式
