---
type: entity
entity_type: project
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 4
tags: ["文档解析", "PDF处理", "开源工具", "AI", "文档处理"]
aliases:
- magic-pdf
- MinerU
- MinerU 文档解析工具
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
- target: '[[PDF文档解析流水线]]'
  type: implements
  confidence: 0.95
- target: '[[pdfminer]]'
  type: compares_to
  confidence: 0.8
- target: '[[Nougat]]'
  type: compares_to
  confidence: 0.8
- target: '[[文档布局检测]]'
  type: uses
  confidence: 0.9
- target: '[[光学字符识别]]'
  type: uses
  confidence: 0.9
- target: '[[公式识别]]'
  type: uses
  confidence: 0.9
- target: '[[PDF内容流]]'
  type: depends_on
  confidence: 0.9
- target: '[[PDF坐标系]]'
  type: depends_on
  confidence: 0.85
- target: '[[Span层级结构]]'
  type: depends_on
  confidence: 0.9
- target: '[[MinerUSpan格式]]'
  type: implements
  confidence: 0.9
- target: '[[内容生成器]]'
  type: implements
  confidence: 0.9
- target: '[[标题层级推断]]'
  type: uses
  confidence: 0.85
- target: '[[跨页段落合并]]'
  type: uses
  confidence: 0.85
- target: '[[输出质量控制]]'
  type: uses
  confidence: 0.8
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

### 内容生成器（第 7 层）

经过前六层处理后，MinerU 拥有**有序的内容块列表**，每个块包含 type、content、bbox、page_no 及关联的图片/表格结构。[[内容生成器]]将这些块序列化为人类可读、机器可用的格式。

**支持的输出格式**：
- **Markdown**（`.md`）：主要格式，可直接用于 RAG/LLM 输入
- **JSON**（`.json`）：完整结构化数据，带坐标信息
- **内容目录**（`.md` 附录）：自动提取的标题层级树
- **图片资源**（`images/` 目录）：提取的嵌入图像

**块类型到 Markdown 的映射**：
| 块类型 | Markdown 输出 |
|--------|-------------|
| title | `#`~`####` 标题（由[[标题层级推断]]决定） |
| text | 直接输出段落文字 |
| equation | `$$...$$` 独立公式块 |
| table | Markdown 表格或 HTML（复杂跨单元格时） |
| figure | `![caption](path)` 图片引用 + 图注 |
| header/footer | 跳过 |
| reference | 无序列表 `- ` |

**行内格式处理**：行内公式通过 `{{FORMULA:N}}` 占位符替换为 `$...$`；粗体/斜体/等宽字体从 [[PyMuPDF]] 的字体信息转换为 `**`/`*`/`` ` `` 标记。

**跨页段落合并**：检测前页末尾是否以完整句子结束（句号/问号/叹号），且当前页开头是否为小写字母或中文字符，若是则移除换行直接拼接。

**图片去重**：通过 MD5 哈希前 8 位作为文件名，避免重复保存相同图片。

**标题层级推断**：通过字号相对大小（`size_ratio = font_size / body_font_size`）推断 H1~H4，同时检测编号模式（如 Section 1.2.3）辅助判断。

### 命令行与 Python API

```bash
magic-pdf -p paper.pdf -o output_dir/           # 基本使用
magic-pdf -p scanned.pdf -o output_dir/ --backend ocr  # 强制 OCR
magic-pdf -p papers/ -o output_dir/ --workers 4  # 批量处理
```

Python API 通过 `UNIPipe` 实现 auto 模式，自动判断文字型/扫描件，依次调用 `pipe_classify()` → `pipe_analyze()` → `pipe_parse()`。

### 局限性

- 跨页内容关联（如跨页表格）支持有限
- 复杂手写内容识别精度低
- 特殊排版（竖排中文、RTL 阿拉伯文）支持不完整
- 大型 PDF（500页+）处理速度有优化空间

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
- [[raw/assets/MinerU/minerU_02_pdf_parsing.md]] — MinerU 深度解析系列 · 第二篇：底层 PDF 解析引擎
- [[raw/assets/MinerU/minerU_04_ocr.md]] — MinerU 深度解析系列 · 第四篇：OCR 引擎
- [[raw/assets/MinerU/minerU_08_output.md]] — MinerU 深度解析系列 · 第八篇：内容生成器与输出管道
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
- [[PDF内容流]] — PDF 内部数据结构
- [[PDF坐标系]] — 坐标参照系统
- [[Span层级结构]] — 文字提取嵌套结构
- [[MinerUSpan格式]] — 内部数据格式
- [[内容生成器]] — 第七层：有序块到 Markdown/JSON 的序列化
- [[标题层级推断]] — 基于字号比例推断 H1~H4
- [[跨页段落合并]] — 跨页段落连续性检测与拼接
- [[输出质量控制]] — 输出完整性自检与空白页过滤
