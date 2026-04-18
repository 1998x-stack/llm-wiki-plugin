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
- MinerUSpan
- MinerU Span Format
- MinerU内部Span格式
relates_to:
- target: '[[Span层级结构]]'
  type: extends
  confidence: 0.95
- target: '[[MinerU]]'
  type: part_of
  confidence: 0.95
- target: '[[PyMuPDF]]'
  type: extends
  confidence: 0.9
- target: '[[PDF坐标系]]'
  type: depends_on
  confidence: 0.85
supersedes: null
---

# MinerUSpan格式

## 概述

[[MinerU]]Span是[[MinerU]]将[[PyMuPDF]]原始Span数据转换后的内部数据格式，统一了坐标系统、字体属性解析和初步类型标注，是贯穿整个解析流水线的核心数据单元。

## 关键内容

### 数据结构定义

```python
@dataclass
class MinerUSpan:
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1)，PDF坐标系
    content: str                             # 文字内容
    font_name: str                           # 字体名
    font_size: float                         # 字号（pt）
    font_weight: str                         # "bold" / "normal"
    font_style: str                          # "italic" / "normal"
    color: int                               # RGB 整数
    page_no: int                             # 所在页码
    type: str                                # "text" / "inline_equation" 等
```

### 与PyMuPDF原始Span的关键转换

从PyMuPDF的原始Span到MinerUSpan经历三个关键转换：

1. **坐标归一化**：PDF坐标（左下原点）→ 图像坐标（左上原点），处理[[PDF坐标系]]的Y轴翻转
2. **字体解析**：从字体名推断是否中文、是否等宽；将flags位掩码解码为`font_weight`和`font_style`字符串
3. **初步类型标注**：检测等宽字体→可能是代码；检测特殊字体→可能是行内公式

### 在流水线中的位置

MinerUSpan是[[MinerU]]七层流水线中第二层（底层PDF解析）的输出产物，后续层（布局检测、内容识别、分类标注、排序）都基于此格式进行扩展和标注。最终`sorted_blocks`中的每个内容块都包含经过多层处理的[[MinerU]]Span集合。

### 设计动机

[[PyMuPDF]]原始数据存在噪声（超短碎片、水印、重叠Span），且坐标系与视觉模型不一致。[[MinerU]]Span格式通过：
- 统一坐标参照系统
- 标准化字体属性表示
- 增加页码和类型字段
为后续处理提供干净、一致的数据基础。

## 来源

- [[raw/assets/MinerU/minerU_02_pdf_parsing.md]] — MinerU 深度解析系列 · 第二篇：底层 PDF 解析引擎

## 相关

- [[MinerU]] — MinerUSpan的所属项目
- [[Span层级结构]] — MinerUSpan的原始数据来源
- [[PyMuPDF]] — 原始Span提取引擎
- [[PDF坐标系]] — 坐标归一化的参照系统
