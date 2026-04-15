---
type: entity
entity_type: tool
status: active
confidence: 0.6
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 工具
aliases:
- pypdf
- PyPDF
relates_to:
- target: '[[PDF解析]]'
  type: implements
  confidence: 0.8
- target: '[[pdfminer]]'
  type: compares_to
  confidence: 0.8
- target: '[[PyMuPDF]]'
  type: compares_to
  confidence: 0.8
supersedes: null
---

# pypdf

## 概述

pypdf 是 Python 的 PDF 处理库，提供基本的 PDF 读取、写入和文本提取功能，但对复杂布局的处理能力有限。

## 关键内容

### 功能与局限

- **功能**：基本的 PDF 读取、写入、合并、文本提取
- **局限**：
  - 多栏布局下提取的文本乱序
  - 无法处理扫描件
  - 不支持公式和表格的结构化还原
  - [[阅读顺序重建|阅读顺序]]无法重建

### 与 MinerU 的对比

pypdf/[[pdfminer]] 代表传统 PDF 文本提取方案：速度快但质量有限。[[MinerU]] 通过七层流水线解决了这些工具无法处理的核心问题。

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[PDF解析]] — 解决的问题域
- [[pdfminer]] — 同类工具
- [[PyMuPDF]] — 更精确的 PDF 解析引擎
- [[MinerU]] — 高质量替代方案
