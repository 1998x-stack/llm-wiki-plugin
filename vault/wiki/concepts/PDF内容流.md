---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags:
- 技术
- 文档处理
- PDF
aliases:
- PDF Content Stream
- PDF内容流
- PostScript绘图命令
relates_to:
- target: '[[PDF解析]]'
  type: part_of
  confidence: 0.95
- target: '[[PyMuPDF]]'
  type: depends_on
  confidence: 0.9
- target: '[[PDF坐标系]]'
  type: relates_to
  confidence: 0.9
- target: '[[Span层级结构]]'
  type: relates_to
  confidence: 0.85
supersedes: null
---

# PDF内容流

## 概述

PDF内容流（Content Stream）是PDF文件内部的核心数据结构，由一系列PostScript风格的绘图命令组成，决定了PDF"存储坐标而非语义"的本质特征。

## 关键内容

### 内容流的本质

PDF内部不存储"段落"或"语义结构"，只存储**绘图指令**。一条典型的内容流命令序列：

```postscript
BT                          % Begin Text
/F1 12 Tf                   % 使用字体 F1，字号 12pt
100 700 Td                  % 移动到坐标 (100, 700)
(Hello, World!) Tj          % 绘制字符串
ET                          % End Text
```

这意味着三个关键推论：
1. **字符顺序由坐标隐含**，而非显式的语义结构
2. **多栏布局、页眉页脚、侧边注释在内部没有任何区别**，全是同级别的绘图命令
3. PDF是"打印指令集"而非"文档结构描述"

### 与语义结构的根本冲突

内容流的设计初衷是**精确渲染**而非**语义表达**。这导致所有[[PDF解析]]工具面临的根本问题：需要从纯坐标信息中逆向推导出人类理解的文档结构（标题、段落、表格、公式等）。[[MinerU]] 等现代工具通过多模型协同流水线（布局检测 + OCR + [[阅读顺序重建]]）来解决这一冲突。

### 对解析策略的影响

理解内容流的本质直接影响解析策略的选择：
- **文字型PDF**：可直接从内容流提取字符坐标，但需要[[阅读顺序重建]]
- **扫描件PDF**：内容流中只有图像绘制命令，必须走[[光学字符识别]]管道
- **混合型PDF**：逐页判断内容流特征，动态选择管道

## 来源

- [[raw/assets/MinerU/minerU_02_pdf_parsing.md]] — MinerU 深度解析系列 · 第二篇：底层 PDF 解析引擎

## 相关

- [[PDF解析]] — 内容流是PDF解析的问题根源
- [[PyMuPDF]] — 解析内容流的底层引擎
- [[PDF坐标系]] — 内容流中坐标的参照系统
- [[Span层级结构]] — 内容流文字提取的嵌套结构
