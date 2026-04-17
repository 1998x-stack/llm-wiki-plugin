---
type: entity
entity_type: project
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, AI, 文档处理]
aliases:
- magic-pdf
- MinerU
relates_to:
- target: '[[上海人工智能实验室]]'
  type: depends_on
  confidence: 0.95
- target: '[[PyMuPDF]]'
  type: uses
  confidence: 0.9
- target: '[[PaddleOCR]]'
  type: uses
  confidence: 0.9
- target: '[[UniMERNet]]'
  type: uses
  confidence: 0.9
- target: '[[TableMaster]]'
  type: uses
  confidence: 0.9
- target: '[[DocLayout-YOLO]]'
  type: uses
  confidence: 0.9
- target: '[[PDF解析]]'
  type: implements
  confidence: 0.95
- target: '[[文档布局检测]]'
  type: uses
  confidence: 0.9
- target: '[[光学字符识别]]'
  type: uses
  confidence: 0.9
- target: '[[公式识别]]'
  type: uses
  confidence: 0.9
supersedes: null
---

# MinerU

## 概述

MinerU（项目名 magic-pdf）是[[上海人工智能实验室]]开源的高质量文档解析工具，专为学术论文、技术报告、教材等复杂 PDF 的结构化提取而设计。Apache-2.0 许可。

## 关键内容

### 核心设计目标

| 目标 | 具体含义 |
|------|---------|
| **高保真还原** | 公式转 LaTeX，表格转 Markdown 表格，图注保留 |
| **[[阅读顺序重建|阅读顺序]]正确** | 多栏、脚注、侧边栏按人类[[阅读顺序重建|阅读顺序]]排列 |
| **格式无关** | 支持文字型 PDF 和扫描件（OCR）两种管道 |
| **可扩展输出** | 导出 Markdown、JSON（带 bbox 坐标）、多模态格式 |
| **工业级鲁棒性** | 能处理数千页的大型 PDF，不崩溃 |

### 七层流水线架构

MinerU 的核心处理逻辑是一条串行流水线，按七个阶段逐层处理：

1. **PDF 类型判断 & 后端选择**（TextBased / OCRBased / MixedBased）
2. **底层 PDF 解析**（[[PyMuPDF]] 提取原始 Span/Block + 页面渲染为图像）
3. **[[文档布局检测]]**（[[DocLayout-YOLO]] / [[LayoutLMv3]] → 检测文本区/图/表/公式框）
4. **内容专项识别**（OCR/[[PaddleOCR]]、[[公式识别]]/[[UniMERNet]]、[[表格识别]]/[[TableMaster]]）
5. **内容块分类与属性标注**（title / text / figure / table / formula）
6. **[[阅读顺序重建|阅读顺序]]排序**（基于坐标与分栏分析，重建人类阅读序列）
7. **Markdown / JSON 内容生成**（将有序内容块序列化为目标格式）

### 三条核心管道

- **TextBased**：适用于数字原生 PDF，[[PyMuPDF]] 直接读取亚像素级字符坐标，不需要 OCR
- **OCRBased**：适用于扫描件，页面渲染为图像后 [[PaddleOCR]] 全量识别
- **Mixed**：逐页判断，分别走对应管道

### 核心数据结构：PDFPageInfo

贯穿整个管道的核心数据结构，包含 page_no、width、height、raw_spans、layout_bboxes、para_blocks、table_blocks、formula_blocks、figure_blocks、sorted_blocks 等字段。每一层往其中填充不同字段，最终 `sorted_blocks` 就是生成 Markdown 的直接来源。

### 与同类工具对比

| 特性 | MinerU | [[pypdf]]/[[pdfminer]] | [[Marker]] | [[Nougat]] |
|------|--------|-----------------|--------|--------|
| 文字型 PDF | ✅ 高质量 | ✅ 但乱序 | ✅ | ✅ |
| 扫描件 | ✅ OCR管道 | ❌ | ✅ | ✅ |
| 公式 → LaTeX | ✅ [[UniMERNet]] | ❌ | ⚠️ 有限 | ✅ |
| 表格结构 | ✅ [[TableMaster]] | ❌ | ⚠️ | ❌ |
| [[阅读顺序重建|阅读顺序]] | ✅ 多栏支持 | ❌ | ✅ | ✅ |
| 开源 | ✅ Apache-2.0 | ✅ | ✅ GPL | ✅ |
| 中文支持 | ✅ 极佳 | ⚠️ | ⚠️ | ❌ |

最大差异化优势：**中文文档支持**（[[PaddleOCR]] 中文能力）+ **公式/表格专项识别**的组合。

### 项目代码结构

```
magic-pdf/
├── magic_pdf/
│   ├── pipe/                    # 管道入口（TextPipe, OCRPipe, UnionPipe）
│   ├── pdf_parse_union_core.py  # 核心调度器
│   ├── model/                   # 模型加载与推理
│   ├── pre_proc/                # 预处理
│   ├── post_proc/               # 后处理
│   ├── para/                    # 段落重建
│   └── operators/               # 内容块操作算子
```

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇：整体架构全景
- [magic-pdf GitHub](https://github.com/opendatalab/MinerU)

## 相关

- [[上海人工智能实验室]] — 开发组织
- [[PyMuPDF]] — 底层 PDF 解析引擎
- [[PaddleOCR]] — OCR 识别引擎
- [[UniMERNet]] — 公式识别模型
- [[TableMaster]] — 表格识别模型
- [[DocLayout-YOLO]] — 布局检测模型
- [[PDF解析]] — 解决的问题域
- [[文档布局检测]] — 第三层流水线
- [[光学字符识别]] — 第四层 OCR 管道
- [[公式识别]] — 第四层公式识别
