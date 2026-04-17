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
- DocLayout-YOLO
- DocLayout YOLO
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[文档布局检测]]'
  type: implements
  confidence: 0.95
supersedes: null
---

# DocLayout-YOLO

## 概述

DocLayout-YOLO 是面向[[文档布局检测]]的 YOLO 系列模型变体，可检测 PDF 页面中的文本区、图像、表格、公式框等布局区域，是 [[MinerU]] 第三层流水线的核心布局检测模型之一。

## 关键内容

### 在 MinerU 中的角色

- **布局检测**：接收 PDF 页面（原始或渲染为图像），输出带类别标签的布局框列表（layout_bboxes）
- **检测类别**：文本区、图像区域、表格区域、公式框等
- **与 [[LayoutLMv3]] 的关系**：[[MinerU]] 支持 DocLayout-YOLO 和 [[LayoutLMv3]] 两种布局检测模型，可根据场景选择

### 技术特点

- 基于 YOLO 架构，推理速度快
- 专为文档布局场景优化
- 输出带类别标签的边界框，供后续内容专项识别使用

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 使用 DocLayout-YOLO 作为布局检测模型
- [[文档布局检测]] — 所属技术领域
- [[LayoutLMv3]] — 可替代的布局检测模型
