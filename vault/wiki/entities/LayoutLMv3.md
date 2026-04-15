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
- AI
aliases:
- LayoutLMv3
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.85
- target: '[[文档布局检测]]'
  type: implements
  confidence: 0.9
- target: '[[DocLayout-YOLO]]'
  type: compares_to
  confidence: 0.85
supersedes: null
---

# LayoutLMv3

## 概述

LayoutLMv3 是微软推出的多模态文档理解模型，结合视觉和文本信息进行文档布局分析，是 [[MinerU]] 第三层流水线中可选的布局检测模型之一。

## 关键内容

### 在 MinerU 中的角色

- **布局检测备选**：与 [[DocLayout-YOLO]] 并列，[[MinerU]] 支持两种布局检测模型
- **多模态理解**：同时利用视觉特征和文本特征进行布局分类
- **适用场景**：对布局复杂度较高的文档可能提供更高精度

### 技术特点

- 预训练多模态模型（视觉 + 文本）
- 支持文档布局分类和元素检测
- 相比纯视觉的 YOLO 方案，推理成本可能更高但精度更优

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 可选的布局检测模型
- [[文档布局检测]] — 所属技术领域
- [[DocLayout-YOLO]] — 可替代的布局检测模型
