---
type: entity
entity_type: tool
status: active
confidence: 0.65
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, AI, 文档处理]
aliases:
- TableMaster
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[表格识别]]'
  type: implements
  confidence: 0.95
supersedes: null
---

# TableMaster

## 概述

TableMaster 是用于[[表格识别|表格结构识别]]的深度学习模型，可将 PDF 中的表格检测框还原为结构化表格数据，是 [[MinerU]] 第四层流水线中的[[表格识别]]引擎。

## 关键内容

### 在 MinerU 中的角色

- **[[表格识别]]**：接收布局检测输出的表格检测框，输出结构化的表格数据（Markdown 表格格式）
- **单元格还原**：PDF 表格的单元格边界仅靠线条暗示，TableMaster 负责还原完整的表格结构
- **差异化优势**：相比 [[pypdf]]/[[pdfminer]]（完全不支持）、[[Marker]]（有限支持）和 [[Nougat]]（不支持），TableMaster 提供了专项的表格结构还原能力

### 技术特点

- 检测框 → 结构化表格
- 支持复杂表格（合并单元格、嵌套表头等）
- 输出为 Markdown 表格格式，可直接用于下游应用

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 使用 TableMaster 作为表格识别引擎
- [[表格识别]] — 所属技术领域
