---
type: entity
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 2
tags: ["文档解析", "AI", "表格识别", "深度学习", "文档处理"]
aliases:
- TableMaster
- 表格结构识别模型
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[表格识别]]'
  type: implements
  confidence: 0.95
- target: '[[PaddleOCR]]'
  type: part_of
  confidence: 0.9
- target: '[[文档布局检测]]'
  type: depends_on
  confidence: 0.9
- target: '[[PyMuPDF]]'
  type: compares_to
  confidence: 0.7
- target: '[[表格单元格填充]]'
  type: extends
  confidence: 0.9
- target: '[[三线表]]'
  type: relates_to
  confidence: 0.8
supersedes: null
---

# TableMaster

## 概述

TableMaster 是 [[PaddleOCR]] PP-Structure 模块中的[[表格识别|表格结构识别]]模型，将[[表格识别]]转化为**序列生成问题**：输入表格图像，[[AR 模型（自回归模型）|自回归]]生成 HTML token 序列 + 预测每个单元格的边界框（bbox）。是 [[MinerU]] 第四层流水线的核心表格引擎。

## 关键内容

### 架构设计

TableMaster 采用 **[[残差网络（ResNet）|ResNet]] + FPN（特征提取）→ [[Transformer 架构|Transformer]] Decoder（[[AR 模型（自回归模型）|自回归]]生成）** 的架构：

1. **特征提取**：[[残差网络（ResNet）|ResNet]] + FPN 从表格图像中提取多尺度特征图，加入[[位置编码]]
2. **[[Transformer 架构|Transformer]] Decoder**：[[AR 模型（自回归模型）|自回归]]地生成 HTML token 序列
3. **双任务输出头**：
   - **Token 分类头**：`nn.Linear(hidden_dim, vocab_size)` — 预测每个位置的 HTML token
   - **Bbox 回归头**：`nn.Linear(hidden_dim, 4)` — 预测每个单元格的边界框 `(x0, y0, x1, y1)`

### HTML 词表设计

TableMaster 的词表包含 HTML 相关的特殊 token，覆盖表格结构的各种情况：

| Token | 用途 |
|-------|------|
| `<BOS>` / `<EOS>` | 序列起止标记 |
| `<td>` / `</td>` | 单元格起止 |
| `<tr>` / `</tr>` | 行列起止 |
| `<td colspan="2">` / `<td colspan="3">` | 跨列单元格 |
| `<td rowspan="2">` / `<td rowspan="2" colspan="2">` | 跨行/跨行+跨列 |
| `<b>` / `<i>` | 粗体/斜体（表头常见） |

### 双阶段表格识别

TableMaster 在 [[MinerU]] 中是**第一阶段（结构识别）**的核心：

```
阶段一：表格结构识别（TableMaster）
  输入：表格图像
  输出：HTML 格式的表格结构（含空 <td></td> 占位）+ 每个单元格的 bbox

阶段二：[[表格单元格填充]]
  文字型 PDF：[[PyMuPDF]] Span 坐标对应
  扫描件：OCR 逐单元格识别
  输出：含文字的完整表格
```

### 跨单元格处理

TableMaster 通过 `colspan` / `rowspan` token 表达合并单元格关系。[[MinerU]] 在转换为 Markdown 时做**降级处理**（Markdown 不支持跨单元格）：跨列单元格复制内容到多个列，用 `↑` 标记重复，并在 JSON 输出中保留完整 HTML 结构。

### 三线表支持

学术论文常见的**[[三线表]]**（无竖线，仅顶线、表头分隔线、底线）对算法是极大挑战。TableMaster 通过学习到的特征理解"列对齐"，即使无竖线也能识别列边界，表头行粗体特征帮助确定列数。

### 输出格式

TableMaster 经 [[MinerU]] 管道后输出三种格式：
- **Markdown**：通用表格格式，跨单元格做降级处理
- **HTML**：完整结构，保留 colspan/rowspan
- **JSON**：机器可读，含 bbox、cell_data、page_no 等元信息

### 与同类工具对比

| 工具 | 表格结构还原 |
|------|-------------|
| [[pypdf]]/[[pdfminer]] | ❌ |
| [[Marker]] | ⚠️ |
| [[Nougat]] | ❌ |
| TableMaster（[[MinerU]]） | ✅ 专项优化 |

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇：整体架构全景
- [[raw/assets/MinerU/minerU_06_table.md]] — MinerU 深度解析系列 · 第六篇：表格识别系统

## 相关

- [[MinerU]] — 使用 TableMaster 作为第四层表格识别引擎
- [[表格识别]] — 所属技术领域
- [[PaddleOCR]] — TableMaster 来源框架
- [[表格单元格填充]] — TableMaster 结构识别后的第二阶段
- [[三线表]] — TableMaster 支持的特殊表格类型
- [[文档布局检测]] — 提供表格检测框作为 TableMaster 输入
