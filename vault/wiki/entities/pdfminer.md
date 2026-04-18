---
type: entity
entity_type: tool
status: active
confidence: 0.6
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, 工具, 文档处理]
aliases:
- pdfminer
- PDFMiner
relates_to:
- target: '[[PDF解析]]'
  type: implements
  confidence: 0.8
- target: '[[PyMuPDF]]'
  type: compares_to
  confidence: 0.8
- target: '[[pypdf]]'
  type: compares_to
  confidence: 0.8
supersedes: null
---

# pdfminer

## 概述

pdfminer 是 Python 的 PDF 文本提取库，可从 PDF 中提取文本内容，但对多栏布局的处理能力有限，提取结果常为乱序字符流。

## 关键内容

### 功能与局限

- **功能**：从文字型 PDF 中提取文本内容
- **局限**：
  - 多栏布局、脚注、侧边栏全部混在一起，无法保持[[阅读顺序重建|阅读顺序]]
  - 无法处理扫描件（无文字层 PDF）
  - 公式以图像形式存储时无法提取
  - 表格结构难以还原

### 与 MinerU 的对比

[[MinerU]] 通过[[PDF文档解析流水线|七层流水线]]（布局检测 + [[阅读顺序重建]] + 内容专项识别）解决了 pdfminer 无法处理的核心问题：乱序字符流、扫描件、公式[[表格识别|表格还原]]。

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[PDF解析]] — 解决的问题域
- [[PyMuPDF]] — 更精确的 PDF 解析引擎
- [[pypdf]] — 同类 PDF 处理库
- [[MinerU]] — 高质量替代方案
