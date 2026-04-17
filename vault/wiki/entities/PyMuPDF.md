---
type: entity
entity_type: tool
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
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

PyMuPDF 是 MuPDF 引擎的 Python 绑定，提供高性能的 PDF 文档解析能力，可直接读取精确到亚像素的字符坐标，是 [[MinerU]] TextBased 管道的核心解析引擎。

## 关键内容

### 在 MinerU 中的角色

- **TextBased 管道**：PyMuPDF 直接从 PDF 中提取原始 Span/Block，包含精确到亚像素的字符坐标，不需要 OCR
- **页面渲染**：将 PDF 页面渲染为图像，供后续布局检测和 OCR 使用
- **原始数据提取**：提供 raw_spans（原始字符组）、images（嵌入图像）等底层数据结构

### 与直接文本提取工具的对比

相比 `pdfminer`、`pypdf` 等工具，PyMuPDF 的优势在于：
- 提供更精确的字符位置信息（亚像素级）
- 支持页面渲染为高质量图像
- 能处理嵌入图像和复杂排版

### 局限性

- 对扫描件（无文字层 PDF）无法直接提取文本
- 多栏布局下提取的字符流仍然是乱序的，需要后续[[阅读顺序重建]]

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 使用 PyMuPDF 作为底层解析引擎
- [[PDF解析]] — 解决的问题域
- [[pdfminer]] — 同类工具，但精度较低
