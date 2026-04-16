---
type: entity
entity_type: tool
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, AI, 工具, 文档处理]
aliases:
- PaddleOCR
- 百度PaddleOCR
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[光学字符识别]]'
  type: implements
  confidence: 0.95
supersedes: null
---

# PaddleOCR

## 概述

Paddle[[光学字符识别|OCR]] 是百度飞桨（PaddlePaddle）开源的 [[光学字符识别|OCR]]（[[光学字符识别]]）工具，以强大的中文识别能力著称，是 [[MinerU]] [[光学字符识别|OCR]]Based 管道的核心文字识别引擎。

## 关键内容

### 在 MinerU 中的角色

- **[[光学字符识别|OCR]]Based 管道**：页面渲染为图像后，Paddle[[光学字符识别|OCR]] 负责全量文字识别
- **中文优势**：Paddle[[光学字符识别|OCR]] 的中文识别能力是 [[MinerU]] 相比同类工具（[[Marker]]、[[Nougat]]）的核心差异化优势之一
- **适用场景**：扫描件、图像型 PDF 等没有任何文字层的文档

### 技术特点

- 支持多语言，中文识别精度业界领先
- 轻量级模型，适合工业级部署
- 支持文本检测 + 文字识别两阶段流水线

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 使用 PaddleOCR 作为 OCR 引擎
- [[光学字符识别]] — 所属技术领域
