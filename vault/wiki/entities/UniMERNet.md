---
type: entity
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 2
tags: ["文档解析", "AI模型", "公式识别", "文档处理"]
aliases:
- UniMERNet
- Unified Mathematical Expression Recognition Network
relates_to:
- target: '[[MinerU]]'
  type: uses
  confidence: 0.9
- target: '[[公式识别]]'
  type: implements
  confidence: 0.95
- target: '[[上海人工智能实验室]]'
  type: depends_on
  confidence: 0.95
supersedes: null
---

# UniMERNet

## 概述

UniMERNet（Unified Mathematical Expression Recognition Network）是上海 AI Lab 开发的[[公式识别]]模型，采用 Swin [[Transformer 架构|Transformer]] 编码器 + [[Transformer 架构|Transformer]] 解码器的 Image-to-Sequence 架构，[[AR 模型（自回归模型）|自回归]]生成 LaTeX 字符串。

## 关键内容

### 设计哲学：统一

- **统一行内公式和独立公式**：两种公式用同一模型处理
- **统一印刷体和手写体**：虽然 [[MinerU]] 主要处理印刷 PDF
- **统一简单和复杂公式**：从 `x + y = z` 到多行大型[[矩阵]]

### 整体架构：图像 → LaTeX 的 Encoder-Decoder

```
公式区域图像 → 图像编码器（Swin Transformer/ViT）→ 特征序列
           → 文本解码器（Transformer Decoder）→ 自回归生成 LaTeX token
           → LaTeX 字符串
```

这是一个标准的 **Image-to-Sequence** 架构，类似于图像描述（Image Captioning）任务。

### 视觉编码器：Swin Transformer

选择 Swin Transformer 而非 CNN 的原因：
1. **局部笔画特征**：字符的具体形状（∫ vs ∮）
2. **全局位置关系**：上下标的相对位置、分数线的高度
3. **长距离依赖**：公式开头的 `\sum_` 和结尾的 `n=1` 之间的关联

Swin Transformer 的层级窗口注意力机制兼顾了这三点，且比纯 ViT 对小尺寸输入更友好。

### 图像预处理

- 灰度化（公式通常是黑白的）
- 归一化高度（默认 target_height=96），宽度等比缩放
- 白底黑字标准化（检测背景色，深色背景则反转）
- 限制最大宽度（1200px）

### 文本解码器：自回归 LaTeX 生成

解码器按照**自回归**方式逐 token 生成 LaTeX，每一步基于**当前已生成序列**和**图像特征**预测下一个 token。

**Beam Search 解码**：使用 Beam Size = 4（保留 4 条候选序列），在质量和速度间取得平衡，优于贪心解码。

**LaTeX Token 词表设计**：使用**命令级词表**而非字符级——`\frac` 作为一个 token 而非 `\`, `f`, `r`, `a`, `c` 五个 token。词表约 600 个 token，包含 LaTeX 命令（`\frac`, `\sum`, `\int`）、希腊字母（`\alpha`, `\beta`）、结构标记（`_{`, `^{`, `}`）和普通字符。这大大缩短了序列长度，提升了识别速度和准确率。

### LaTeX 后处理

- **语法修复**：修复未闭合的花括号、常见识别错误（如 `\operaorname` → `\operatorname`）、移除多余空格
- **LaTeX 渲染验证**：可选使用 `sympy` 或 `latex2sympy` 解析生成的 LaTeX，解析失败则标记为低置信度
- **输出格式**：行内公式 `$...$`，独立公式 `$$...$$`

### 识别能力边界

| 公式类型 | 识别准确率 | 说明 |
|---------|-----------|------|
| 标准单行公式 | 高（>90%） | LaTeX 生成的标准印刷体 |
| 多行对齐公式（align） | 中（60~80%） | 结构复杂，容易出错 |
| 大型[[矩阵]] | 中（50~70%） | 维度高时出错率增加 |
| 化学结构式 | 低（<30%） | 非训练目标 |
| 手写公式 | 低（40~60%） | 扫描件中的手写[[标注]] |

### 在 MinerU 中的角色

- **[[公式识别]]**：接收布局检测输出的公式检测框，输出对应的 LaTeX 代码
- **高保真还原**：使 [[MinerU]] 能够将 PDF 中以图像形式存储的公式精确转换为可编辑的 LaTeX 格式
- 与同类工具对比：相比 [[Marker]]（公式支持有限）和 [[Nougat]]（支持但不擅长中文），UniMERNet 提供了专项的[[公式识别]]能力

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇：整体架构全景
- [[raw/assets/MinerU/minerU_05_formula.md]] — MinerU 深度解析系列 · 第五篇：公式识别系统

## 相关

- [[MinerU]] — 使用 UniMERNet 作为公式识别引擎
- [[公式识别]] — 所属技术领域
- [[上海人工智能实验室]] — 开发组织
