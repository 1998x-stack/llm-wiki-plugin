---
type: entity
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 2
tags: ["技术", "AI", "工具", "文档处理", "OCR"]
aliases:
- PaddleOCR
- 百度PaddleOCR
- PP-OCR
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[光学字符识别]]'
  type: implements
  confidence: 0.95
- target: '[[PP-OCRv4]]'
  type: implements
  confidence: 0.95
- target: '[[DBNet++]]'
  type: uses
  confidence: 0.9
- target: '[[SVTR]]'
  type: uses
  confidence: 0.9
- target: '[[CTC解码]]'
  type: uses
  confidence: 0.85
- target: '[[透视变换]]'
  type: uses
  confidence: 0.8
supersedes: null
---

# PaddleOCR

## 概述

PaddleOCR 是[[百度]]飞桨（PaddlePaddle）开源的 OCR（[[光学字符识别]]）工具，以强大的中文识别能力著称，是 [[MinerU]] OCRBased 管道的核心文字识别引擎。Apache-2.0 许可。

## 关键内容

### 在 MinerU 中的角色

OCR 在 [[MinerU]] 里**按需激活**，而非全程使用：

- **文字型 PDF（TextBased 管道）**：[[PyMuPDF]] 直接提取文字 Span，OCR 仅用于图注区域、表格内文字、公式周边等特殊区域
- **扫描件 PDF（OCRBased 管道）**：整页 OCR，所有文字都靠识别，[[PyMuPDF]] 只提供图像
- **混合 PDF（Mixed 管道）**：逐个布局框判断，有文字层直接提取，无文字层走 OCR

这个设计非常精明：对于文字型 PDF，[[PyMuPDF]] 的精确坐标远优于 OCR 识别结果，没有必要浪费[[计算]]资源。

### 技术优势对比

| 维度 | PaddleOCR | Tesseract | EasyOCR | TrOCR |
|------|-----------|-----------|---------|-------|
| **中文识别** | ✅ 极强，专门优化 | ⚠️ 一般 | ✅ 较好 | ⚠️ |
| **速度** | ✅ 快（PP-OCR 轻量级） | 中 | 慢 | 极慢 |
| **检测+识别一体** | ✅ | ⚠️ | ✅ | ✅ |
| **版式理解** | ✅ PP-Structure | ❌ | ❌ | ❌ |
| **开源协议** | Apache-2.0 | Apache-2.0 | Apache-2.0 | MIT |
| **工业验证** | ✅ 阿里/[[京东]]等 | ✅ | ⚠️ | ⚠️ |

对于 [[MinerU]] 最重要的场景——**中文学术论文/教材扫描件**，PaddleOCR 有无可比拟的优势。

### PP-OCRv4 系统组件

[[MinerU]] 主要使用 PaddleOCR 的 **[[PP-OCRv4]]** 系列，包含三个子模块：

1. **文字检测（Detection）**：[[DBNet++]] 变体，输入图像，输出文字区域的多边形轮廓
2. **文字方向分类（Direction Classification）**：输入检测到的文字图像块，输出 0°/90°/180°/270°
3. **文字识别（Recognition）**：[[SVTR]]（[[SVTR|Scene Text Recognizer]]），输入矫正后的文字行图像，输出文字字符串 + 置信度

### OCR 流水线

完整的 OCR 处理流程：

1. **文字区域检测（[[DBNet++]]）**：基于可微分二值化，输出概率图 → 自适应阈值二值化 → 轮廓提取 → 多边形文字框。多边形而非矩形框能更精确地框定倾斜的文字行
2. **[[透视变换]]矫正**：将检测到的文字多边形通过[[透视变换]]矫正为水平的矩形图像（高度固定 48px）
3. **文字识别（[[SVTR]]）**：CNN + [[Transformer 架构|Transformer]] 混合特征提取 → 序列特征 → [[CTC解码]] → 文字字符串

### 中文 OCR 的特殊挑战与解法

- **字符集规模**：中文常用字 3500+，完整字符集 70000+。PaddleOCR 使用包含 **6763 个常用汉字**的字符集（GB2312 标准），覆盖 99% 以上常用场景
- **字形相似度**：大量形近字（己/已/巳，戊/戌/戍）。通过大规模训练数据、形近字混淆样本、[[Language-Model|语言模型]]后处理解决
- **中英混排**：使用统一字符集，同时包含中文和英文字符，不需要先判断语言再切换模型
- **垂直排版**：方向分类器先识别文字方向，再旋转 90° 送入识别模型

### MinerU 中的关键优化

- **区域裁剪 OCR**：不对整页做 OCR，只对特定布局框内的区域做 OCR，速度从 2~5 秒/页降至 0.1~0.5 秒/区域，提升 10×+
- **两路 Span 融合**：优先使用 [[PyMuPDF]] native spans（精度更高），OCR spans 仅用于未覆盖的区域，通过 IoU > 0.3 判断重叠
- **质量过滤**：置信度阈值（默认 0.5）、乱码检测（特殊字符比例 > 0.3）、空白行和极短文本过滤

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇
- [[raw/assets/MinerU/minerU_04_ocr.md]] — MinerU 深度解析系列 · 第四篇：OCR 引擎

## 相关

- [[MinerU]] — 使用 PaddleOCR 作为 OCR 引擎
- [[光学字符识别]] — 所属技术领域
- [[PP-OCRv4]] — PaddleOCR 的模型系列
- [[DBNet++]] — 文字检测子模块
- [[SVTR]] — 文字识别子模块
- [[CTC解码]] — 识别解码方法
- [[透视变换]] — 文字矫正技术
- [[PyMuPDF]] — 在 MinerU 中与 OCR 互补使用
