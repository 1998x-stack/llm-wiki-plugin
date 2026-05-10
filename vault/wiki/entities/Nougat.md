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
- Nougat
relates_to:
- target: '[[MinerU]]'
  type: compares_to
  confidence: 0.85
- target: '[[PDF解析]]'
  type: implements
  confidence: 0.8
supersedes: null
---

# Nougat

## 概述

Nougat 是 [[Meta AI]] 开源的端到端 PDF 文档解析模型，基于视觉 [[Transformer架构|Transformer]] 将 PDF 页面图像直接转换为 Markdown，速度较慢且不支持中文。

## 关键内容

### 与 MinerU 的对比

| 特性 | Nougat | [[MinerU]] |
|------|--------|--------|
| 文字型 PDF | ✅ | ✅ 高质量 |
| 扫描件 | ✅ | ✅ OCR管道 |
| 公式 → LaTeX | ✅ | ✅ [[UniMERNet]] |
| 表格结构 | ❌ | ✅ [[TableMaster]] |
| [[阅读顺序重建|阅读顺序]] | ✅ | ✅ 多栏支持 |
| 速度 | 慢 | 中（模型推理） |
| 中文支持 | ❌ | ✅ 极佳 |

### 局限

- 不支持中文文档
- 表格结构无法还原
- 推理速度较慢
- 端到端模型，难以针对特定任务（如公式、表格）进行专项优化

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 同类工具，MinerU 在表格/中文/速度方面更优
- [[PDF解析]] — 解决的问题域
- [[Marker]] — 同类工具
