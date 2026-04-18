---
type: entity
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 2
tags: ["技术", "AI", "文档处理", "目标检测"]
aliases:
  - DocLayout-YOLO
  - DocLayout YOLO
relates_to:
  - target: '[[MinerU]]'
    type: uses
    confidence: 0.9
  - target: '[[文档布局检测]]'
    type: implements
    confidence: 0.95
  - target: '[[YOLO]]'
    type: extends
    confidence: 0.9
  - target: '[[ONNX Runtime]]'
    type: uses
    confidence: 0.85
  - target: '[[DocLayNet]]'
    type: depends_on
    confidence: 0.8
  - target: '[[PubLayNet]]'
    type: depends_on
    confidence: 0.8
  - target: '[[D4LA]]'
    type: depends_on
    confidence: 0.8
supersedes: null
---

# DocLayout-YOLO

## 概述

DocLayout-YOLO 是上海 AI Lab 团队基于标准 YOLO 目标检测框架、针对文档页面专门优化的 One-Stage 检测器变体，专为[[文档布局检测]]设计，一次前向推理即可输出所有语义区域的类别和边界框。

## 关键内容

### 模型架构

DocLayout-YOLO 继承标准 YOLO 的三段式架构：

```
输入图像
    ↓
Backbone（特征提取，如 CSPDarknet）
    ↓
Neck（多尺度特征融合，FPN/PAN）
    ↓
Head（三个尺度的检测头）
    ↓
NMS（非极大值抑制）→ 最终检测框
```

作为 **One-Stage 目标检测器**，相比两阶段检测器（如 Faster R-CNN）推理速度显著更快。

### 11 类检测类别体系

| 类别标签 | 含义 | 说明 |
|---------|------|------|
| `text` | 普通文本段落 | 正文、引言、结论等连续文字区 |
| `title` | 标题 | 各级标题（Section/Subsection 等） |
| `figure` | 图像 | 插图、照片、示意图 |
| `figure_caption` | 图注 | "Figure 1: ..." 这类说明文字 |
| `table` | 表格 | 表格的完整区域 |
| `table_caption` | 表注 | "Table 1: ..." |
| `header` | 页眉 | 页面顶部重复出现的信息 |
| `footer` | 页脚 | 页面底部（含页码） |
| `reference` | 参考文献 | 文献列表区域 |
| `equation` | 独立公式 | 单独成行的数学公式（非行内） |
| `equation_caption` | 公式编号 | 如 "(1)"、"(2)" |

### 文档场景的四大特殊挑战

**挑战1：极端长宽比**
表格可能很宽（宽/高 = 5:1），图注可能很窄（宽/高 = 20:1）。标准 YOLO 的 Anchor 设计为自然场景优化，需要专门针对文档调整 Anchor 比例。

**挑战2：密集重叠**
一列文字中，多个段落的 bbox 在竖直方向紧密排列，传统 NMS 容易错误合并。

**挑战3：小目标**
行内公式、上标、脚注序号等都是极小的文字区域，需要更高分辨率的特征图。

**挑战4：无纹理区域**
大段均匀文字区域的纹理特征很弱，模型需要理解"一大块字就是段落"这种语义。

### 针对性改进

1. **专用 Anchor 设计**：重新聚类文档数据集的 bbox 尺寸分布，生成适合文档的 9 个 Anchor
2. **高分辨率推理**：推理时保持较大的输入分辨率（如 1280×1280），保留文字细节
3. **文档专用训练集**：在 [[DocLayNet]]、[[PubLayNet]]、[[D4LA]] 等大规模文档数据集上预训练
4. **后处理调整**：NMS 阈值针对文档的密集布局重新调优

### 推理流程

#### 输入输出规格

```
输入：PDF 页面图像（numpy array，RGB，约 1654×2339 @ 200 DPI A4）

输出：N 个检测框，每个包含：
{
    "bbox": [x0, y0, x1, y1],   # 像素坐标
    "label": "text",             # 类别标签
    "score": 0.97                # 置信度
}
```

#### 预处理

等比例缩放（长边对齐 target_size，通常 1280）→ Padding 到正方形（灰色填充 114）→ 归一化（减均值除标准差）。

#### 推理引擎

使用 [[ONNX Runtime]] 进行推理，支持 GPU/CPU 自动选择：

```python
import onnxruntime as ort

session = ort.InferenceSession(
    "doclayout_yolo.onnx",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)
```

#### 后处理

- 坐标还原：将推理坐标按缩放比例反算回原始图像坐标
- NMS 去重：conf_threshold 默认 0.25，iou_threshold 默认 0.45
- 中心坐标格式 → 角点坐标格式转换

### 置信度阈值策略

| 阈值 | 效果 |
|------|------|
| 过低（< 0.15） | 大量误检，噪声框增多 |
| **默认（0.25）** | **平衡准确率和召回率** |
| 过高（> 0.6） | 漏检增多，小区域（图注、公式编号）大量丢失 |

对不同类别使用不同阈值：公式/表格（类别重要，宁可误检不可漏检）使用较低阈值，页眉/页脚使用较高阈值。

### 在 MinerU 中的后处理

- **Span 对齐**：将 [[PyMuPDF]] 提取的 Span 通过中心点 + IoU 分配到对应布局框
- **孤儿 Span 处理**：未落入任何布局框的 Span 通过就近原则分配或丢弃
- **布局框合并与拆分**：相邻 text 框水平对齐且间距小于行高 → 合并；text 框内存在明显分栏 → 拆分
- **分栏检测**：通过 text 框 x 中心分布推断单栏/双栏，以页面中线为分界

## 来源

- [[raw/assets/MinerU/minerU_01_architecture.md]] — MinerU 深度解析系列 · 第一篇：整体架构全景
- [[raw/assets/MinerU/minerU_03_layout.md]] — MinerU 深度解析系列 · 第三篇：布局检测系统

## 相关

- [[MinerU]] — 使用 DocLayout-YOLO 作为核心布局检测模型
- [[文档布局检测]] — 所属技术领域
- [[YOLO]] — 基础架构
- [[ONNX Runtime]] — 推理引擎
- [[DocLayNet]] — 训练数据集之一
- [[PubLayNet]] — 训练数据集之一
- [[D4LA]] — 训练数据集之一
- [[LayoutLMv3]] — 可替代的布局检测模型
