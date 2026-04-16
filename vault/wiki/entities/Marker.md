---
type: entity
entity_type: tool
status: active
confidence: 0.6
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, AI, 文档处理]
aliases:
- Marker
relates_to:
- target: '[[MinerU]]'
  type: compares_to
  confidence: 0.85
- target: '[[PDF解析]]'
  type: implements
  confidence: 0.8
supersedes: null
---

# Marker

## 概述

Marker 是一款开源 PDF 文档解析工具，支持文字型 PDF 和扫描件的解析，但在公式和表格的结构化还原方面能力有限，采用 GPL 许可。

## 关键内容

### 与 MinerU 的对比

| 特性 | Marker | [[MinerU]] |
|------|--------|--------|
| 文字型 PDF | ✅ | ✅ 高质量 |
| 扫描件 | ✅ | ✅ [[光学字符识别|OCR]]管道 |
| 公式 → LaTeX | ⚠️ 有限 | ✅ [[UniMERNet]] |
| 表格结构 | ⚠️ | ✅ [[TableMaster]] |
| [[阅读顺序重建|阅读顺序]] | ✅ | ✅ 多栏支持 |
| 开源 | ✅ GPL | ✅ Apache-2.0 |
| 中文支持 | ⚠️ | ✅ 极佳 |

### 局限

- [[公式识别]]能力有限
- 表格结构还原不完整
- 中文文档支持较弱
- GPL 许可对商业应用有约束

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 同类工具，MinerU 在公式/表格/中文方面更优
- [[PDF解析]] — 解决的问题域
- [[Nougat]] — 同类工具
