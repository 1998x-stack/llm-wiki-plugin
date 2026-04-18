---
type: concept
status: active
confidence: 0.75
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags:
- 技术
- 文档处理
- PDF
aliases:
- PDF Coordinate System
- PDF坐标系
- PDF坐标系统
- Point单位
relates_to:
- target: '[[PDF内容流]]'
  type: part_of
  confidence: 0.9
- target: '[[PDF解析]]'
  type: part_of
  confidence: 0.85
- target: '[[PyMuPDF]]'
  type: depends_on
  confidence: 0.85
- target: '[[MinerU]]'
  type: relates_to
  confidence: 0.8
supersedes: null
---

# PDF坐标系

## 概述

PDF使用以页面左下角为原点、point（pt）为单位的笛卡尔坐标系，1 inch = 72 pt，与屏幕坐标系（左上角原点）存在Y轴翻转差异。

## 关键内容

### 坐标系定义

- **原点**：页面左下角 `(0, 0)`
- **单位**：point（pt），1 inch = 72 pt
- **A4纸尺寸**：595.28 × 841.89 pt
- **方向**：X轴向右，Y轴向上

### 与屏幕坐标系的冲突

渲染到屏幕或图像时通常需要**Y轴翻转**，因为屏幕坐标系以左上角为原点、Y轴向下。[[MinerU]] 内部需要处理这个转换：
- PDF坐标：`(x, y)`，原点在左下
- 图像坐标：`(x, height - y)`，原点在左上

### 在解析中的关键作用

坐标系是[[PDF解析]]的基石：
1. **字符定位**：每个Span的bbox使用PDF坐标系表示 `(x0, y0, x1, y1)`
2. **布局检测**：[[文档布局检测]]模型的检测框需要与PDF坐标对齐
3. **[[阅读顺序重建]]**：基于坐标的排序算法依赖正确的坐标参照
4. **多模态对齐**：文字Span的坐标需要与图像像素坐标对应

### 坐标归一化

[[MinerU]]将[[PyMuPDF]]提取的原始坐标转换为其内部[[MinerUSpan格式]]时，关键步骤之一就是坐标归一化：从PDF坐标（左下原点）转换为图像坐标（左上原点），确保文字管道和视觉管道的坐标系统一致。

## 来源

- [[raw/assets/MinerU/minerU_02_pdf_parsing.md]] — MinerU 深度解析系列 · 第二篇：底层 PDF 解析引擎

## 相关

- [[PDF内容流]] — 坐标系是内容流中绘图命令的参照
- [[PDF解析]] — 坐标系是解析的基础设施
- [[PyMuPDF]] — 提供PDF坐标系的原始数据
- [[MinerUSpan格式]] — 内部格式需要坐标归一化
