---
type: entity
entity_type: tool
status: active
confidence: 0.65
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- AI
aliases:
- UniMERNet
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[公式识别]]'
  type: implements
  confidence: 0.95
supersedes: null
---

# UniMERNet

## 概述

UniMERNet 是用于[[公式识别|数学公式识别]]的深度学习模型，可将图像中的公式检测框转换为 LaTeX 代码，是 [[MinerU]] 第四层流水线中的[[公式识别]]引擎。

## 关键内容

### 在 MinerU 中的角色

- **[[公式识别]]**：接收布局检测输出的公式检测框，输出对应的 LaTeX 代码
- **高保真还原**：使 [[MinerU]] 能够将 PDF 中以图像形式存储的公式精确转换为可编辑的 LaTeX 格式
- **与同类工具对比**：相比 [[Marker]]（公式支持有限）和 [[Nougat]]（支持但不擅长中文），UniMERNet 提供了专项的[[公式识别]]能力

### 技术特点

- 端到端[[公式识别]]：检测框 → LaTeX
- 支持复杂公式结构（分式、积分、[[矩阵]]等）
- 与 [[MinerU]] 的布局检测和内容块分类协同工作

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇

## 相关

- [[MinerU]] — 使用 UniMERNet 作为公式识别引擎
- [[公式识别]] — 所属技术领域
