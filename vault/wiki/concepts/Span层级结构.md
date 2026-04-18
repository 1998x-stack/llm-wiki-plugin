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
- Span Hierarchy
- Span层级
- Span结构
- Block-Line-Span
relates_to:
- target: '[[PyMuPDF]]'
  type: depends_on
  confidence: 0.95
- target: '[[PDF内容流]]'
  type: part_of
  confidence: 0.9
- target: '[[MinerUSpan格式]]'
  type: relates_to
  confidence: 0.9
- target: '[[PDF解析]]'
  type: part_of
  confidence: 0.85
supersedes: null
---

# Span层级结构

## 概述

[[PyMuPDF]]的文字提取遵循Page → Block → Line → Span → Char五级嵌套结构，其中Span（具有相同字体属性的连续文字片段）是[[MinerU]]最核心的处理单元。

## 关键内容

### 五级嵌套结构

```
Page（页面）
└── Block（块：连续文字或图像区域）
    └── Line（行：同一基线上的文字）
        └── Span（片段：同一字体、大小、颜色的连续文字）
            └── Char（字符，rawdict模式下可获取）
```

- **Block**：页面上的连续区域，type=0为文字块，type=1为图像块
- **Line**：共享同一基线（baseline）的文字序列
- **Span**：具有相同字体名、字号、颜色的连续文字段，带有精确bbox
- **Char**：单个字符，仅在`rawdict`模式下可获取

### Span的核心属性

每个Span携带丰富的元信息：
- `text`：文字内容
- `bbox`：边界框 `(x0, y0, x1, y1)`
- `font`：字体名
- `size`：字号（pt）
- `flags`：位掩码，标识粗体/斜体/衬线/等宽/上标
- `color`：文字颜色（RGB整数）
- `origin`：基线坐标

### flags位掩码解码

```
FLAG_SUPERSCRIPT = 1    # 上标
FLAG_ITALIC      = 2    # 斜体
FLAG_SERIFED     = 4    # 衬线字体
FLAG_MONOSPACED  = 8    # 等宽字体
FLAG_BOLD        = 16   # 粗体
```

[[MinerU]]利用粗体+字号信息**推断标题层级**，这是后续分类系统的重要输入。等宽字体flag可用于初步识别代码块。

### 原始Span的噪声问题

[[PyMuPDF]]提取的原始Span存在多种噪声：
1. **超短Span碎片化**：单字符或空格级别的过度分割，需同行合并
2. **水印文字**：旋转、半透明、大面积覆盖，通过颜色和旋转角度检测
3. **页眉页脚**：页面顶部/底部固定区域，多页重复出现
4. **重叠Span**：部分PDF生成工具产生的内容重复，需去重

[[MinerU]]在接收原始Span后需要清洗这些噪声，然后转换为内部[[MinerUSpan格式]]。

## 来源

- [[raw/assets/MinerU/minerU_02_pdf_parsing.md]] — MinerU 深度解析系列 · 第二篇：底层 PDF 解析引擎

## 相关

- [[PyMuPDF]] — Span层级结构的来源
- [[PDF内容流]] — Span是内容流文字指令的结构化提取
- [[MinerUSpan格式]] — MinerU的内部Span数据格式
- [[PDF解析]] — Span提取是解析流程的基础步骤
