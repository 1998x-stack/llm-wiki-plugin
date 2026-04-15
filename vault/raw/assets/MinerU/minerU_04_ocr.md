# MinerU 深度解析系列 · 第四篇
# OCR 引擎：PaddleOCR 如何识别文字，以及中文优化的秘密

> **上一篇回顾**：DocLayout-YOLO 把页面图像分割成有语义标签的区域框。本篇深入第四层的第一个组件——OCR 文字识别引擎。

---

## 一、OCR 在 MinerU 中的角色

OCR（Optical Character Recognition，光学字符识别）在 MinerU 里不是全程都用，而是**按需激活**：

```
文字型 PDF（TextBased 管道）：
    → PyMuPDF 直接提取文字 Span（精确）
    → OCR 仅用于：图注区域、表格内文字、公式周边等特殊区域

扫描件 PDF（OCRBased 管道）：
    → 整页 OCR，所有文字都靠识别
    → PyMuPDF 只提供图像，不提供文字
    
混合 PDF（Mixed 管道）：
    → 逐个布局框判断：有文字层 → 直接提取；无文字层 → OCR
```

这个设计非常精明：对于文字型 PDF，PyMuPDF 的精确坐标远优于 OCR 识别结果，没有必要浪费计算资源。OCR 只在**真正需要的地方**使用。

---

## 二、为什么选择 PaddleOCR？

MinerU 选择了百度 PaddlePaddle 框架下的 **PaddleOCR** 作为默认 OCR 引擎。

### 2.1 PaddleOCR 的技术优势

| 维度 | PaddleOCR | Tesseract | EasyOCR | TrOCR |
|------|-----------|-----------|---------|-------|
| **中文识别** | ✅ 极强，专门优化 | ⚠️ 一般 | ✅ 较好 | ⚠️ |
| **速度** | ✅ 快（PP-OCR 轻量级） | 中 | 慢 | 极慢 |
| **检测+识别一体** | ✅ | ⚠️ | ✅ | ✅ |
| **版式理解** | ✅ PP-Structure | ❌ | ❌ | ❌ |
| **开源协议** | Apache-2.0 | Apache-2.0 | Apache-2.0 | MIT |
| **工业验证** | ✅ 阿里/京东等 | ✅ | ⚠️ | ⚠️ |

对于 MinerU 最重要的场景——**中文学术论文/教材扫描件**，PaddleOCR 有无可比拟的优势。

### 2.2 PaddleOCR 的模型家族

MinerU 主要使用 PaddleOCR 的 **PP-OCRv4** 系列：

```
PP-OCRv4 系统组件：
├── 文字检测（Detection）：DBNet++ 变体
│   输入：图像
│   输出：文字区域的多边形轮廓
│
├── 文字方向分类（Direction Classification）：
│   输入：检测到的文字图像块
│   输出：0° / 90° / 180° / 270°
│
└── 文字识别（Recognition）：SVTR（Scene Text Recognizer）
    输入：矫正后的文字行图像
    输出：文字字符串 + 置信度
```

---

## 三、OCR 流水线详解

### 3.1 阶段一：文字区域检测（DBNet++）

DBNet++ 是一种基于**可微分二值化（Differentiable Binarization）**的文字检测模型。

**工作原理**：
1. 输入整个页面图像（或布局框内的裁剪区域）
2. 输出一张与输入同尺寸的**概率图**，每个像素值表示"属于文字的概率"
3. 通过自适应阈值二值化，生成文字区域的二值蒙版
4. 轮廓提取 + 多边形拟合，得到文字区域的多边形框

```
原始图像 → ResNet/MobileNet 特征提取 → FPN 多尺度融合 
→ 概率图 + 阈值图 → 二值化蒙版 → 多边形文字框
```

**为什么用多边形而不是矩形框？**
文字行可能稍有倾斜（扫描件常见），多边形（通常是四边形）能更精确地框定文字区域，后续透视变换矫正更准确。

### 3.2 阶段二：透视矫正

对于检测到的文字多边形，需要做透视变换（Perspective Transform）将其矫正为水平的矩形图像：

```python
import cv2
import numpy as np

def correct_perspective(image, polygon_points):
    """
    polygon_points: 4个顶点 [(x0,y0), (x1,y1), (x2,y2), (x3,y3)]
    按照 左上、右上、右下、左下 顺序
    """
    pts = np.array(polygon_points, dtype=np.float32)
    
    # 计算目标矩形的宽高
    width = int(max(
        np.linalg.norm(pts[1] - pts[0]),  # 上边宽
        np.linalg.norm(pts[2] - pts[3])   # 下边宽
    ))
    height = int(max(
        np.linalg.norm(pts[3] - pts[0]),  # 左边高
        np.linalg.norm(pts[2] - pts[1])   # 右边高
    ))
    
    dst = np.array([
        [0, 0], [width-1, 0],
        [width-1, height-1], [0, height-1]
    ], dtype=np.float32)
    
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (width, height))
    return warped
```

### 3.3 阶段三：文字识别（SVTR）

**SVTR（Scene Text Recognizer）** 是 PaddleOCR 的识别骨干，基于 Vision Transformer 架构。

输入：矫正后的文字行图像（高度固定为 48px，宽度按比例缩放）

**识别流程**：
```
文字行图像（48×W）
→ 特征提取（CNN + Transformer 混合）
→ 序列特征（长度为 W/4）
→ CTC 解码（Connectionist Temporal Classification）
→ 文字字符串
```

**CTC 解码的妙处**：CTC 允许模型输出比输入序列更短的字符序列，天然处理了字符宽度不一、字符间隔不均匀等问题，不需要字符级的对齐标注。

---

## 四、中文 OCR 的特殊挑战与 PaddleOCR 的解法

### 4.1 挑战：字符集规模

- 英文：约 100 个字符（大小写+数字+标点）
- 中文：常用字 3500+，完整字符集 70000+

PaddleOCR 的解法：使用包含 **6763 个常用汉字**的字符集（GB2312 标准），覆盖 99% 以上的常用中文场景。

### 4.2 挑战：字形相似度

中文中存在大量形近字（己/已/巳，戊/戌/戍），传统 OCR 容易混淆。PaddleOCR 通过：
- 大规模训练数据（数百万中文文字图像）
- 在训练集中加入形近字的混淆样本
- 语言模型后处理（上下文纠错）

### 4.3 挑战：中英混排

学术论文中大量存在中英文混排，如"本文提出了一种新的 Transformer 架构，在 ImageNet 数据集上..."。

PaddleOCR 的混合识别模型使用**统一字符集**，同时包含中文和英文字符，不需要先判断语言再切换模型。

### 4.4 挑战：垂直排版

部分中文文档（尤其是古籍、传统排版）使用从上到下、从右到左的竖排。PaddleOCR 通过方向分类器先识别文字方向，再旋转90°送入识别模型。

---

## 五、MinerU 中 OCR 的调用方式

### 5.1 基本调用

```python
from paddleocr import PaddleOCR

# 初始化（首次调用会下载模型）
ocr_engine = PaddleOCR(
    use_angle_cls=True,      # 启用方向分类
    lang="ch",               # 中文模式（同时支持英文）
    use_gpu=True,            # 使用 GPU
    show_log=False,          # 关闭日志
    rec_batch_num=6,         # 识别批次大小
)

# 对图像进行 OCR
results = ocr_engine.ocr(image_array, cls=True)

# 解析结果
for line in results[0]:
    polygon = line[0]        # 四边形坐标：[[x0,y0],[x1,y1],[x2,y2],[x3,y3]]
    text = line[1][0]        # 识别文字
    confidence = line[1][1]  # 置信度 (0~1)
    
    print(f"文字: {text}, 置信度: {confidence:.2f}")
    print(f"位置: {polygon}")
```

### 5.2 MinerU 的区域裁剪 OCR（关键优化）

在文字型 PDF 中，MinerU **不对整页做 OCR**，而是只对特定布局框内的区域做 OCR：

```python
def ocr_specific_region(page_image, layout_box, ocr_engine):
    """只对布局框内的区域做 OCR，减少计算量"""
    x0, y0, x1, y1 = [int(c) for c in layout_box.bbox]
    
    # 加少量 padding 避免边界截断
    padding = 5
    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(page_image.shape[1], x1 + padding)
    y1 = min(page_image.shape[0], y1 + padding)
    
    region = page_image[y0:y1, x0:x1]
    results = ocr_engine.ocr(region, cls=True)
    
    # 坐标转换：区域坐标 → 页面坐标
    if results[0]:
        for line in results[0]:
            for point in line[0]:
                point[0] += x0
                point[1] += y0
    
    return results
```

这个优化**非常关键**：整页 OCR 约需 2~5 秒，而裁剪区域 OCR 通常在 0.1~0.5 秒。对于数百页的论文，节省的时间极为可观。

---

## 六、OCR 结果的质量过滤

PaddleOCR 的原始输出需要过滤，MinerU 应用以下规则：

### 6.1 置信度过滤

```python
MIN_CONFIDENCE = 0.5  # MinerU 默认阈值

filtered_results = [
    line for line in ocr_results
    if line[1][1] >= MIN_CONFIDENCE
]
```

### 6.2 乱码检测

```python
import re

def is_garbled(text: str) -> bool:
    """检测是否为乱码"""
    # 检测是否包含大量特殊字符
    special_char_ratio = len(re.findall(r'[^\u4e00-\u9fff\w\s\.,，。；：]', text)) / len(text)
    if special_char_ratio > 0.3:
        return True
    
    # 检测字符多样性（乱码通常重复字符多）
    if len(set(text)) / len(text) < 0.3 and len(text) > 5:
        return True
    
    return False
```

### 6.3 空白行和极短文本过滤

```python
def is_valid_ocr_line(text: str) -> bool:
    text = text.strip()
    if len(text) < 2:          # 过短
        return False
    if text in ['。', '，', '.', ',', '-', '—']:  # 仅有标点
        return False
    return True
```

---

## 七、OCR Span 与 PyMuPDF Span 的融合

在混合 PDF 中，某些区域有 PyMuPDF 的 Span，某些区域只有 OCR 的 Span，MinerU 需要将两者统一：

```python
def merge_native_and_ocr_spans(native_spans, ocr_spans, layout_box):
    """
    优先使用 native spans（来自 PyMuPDF，精度更高）
    OCR spans 仅用于 native spans 未覆盖的区域
    """
    merged = list(native_spans)
    
    for ocr_span in ocr_spans:
        # 检查是否与任何 native span 重叠
        has_overlap = any(
            calc_iou(ocr_span.bbox, native.bbox) > 0.3
            for native in native_spans
        )
        
        if not has_overlap:
            ocr_span.source = "ocr"   # 标记来源
            merged.append(ocr_span)
    
    return merged
```

---

## 八、小结

OCR 引擎层是 MinerU 处理扫描件的核心能力：

- **PaddleOCR**：DBNet++ 检测 + SVTR 识别，中文能力业界领先
- **按需 OCR**：文字型 PDF 仅对特定区域做 OCR，大幅节省计算
- **区域裁剪**：不做整页 OCR，速度提升 10×+
- **质量过滤**：置信度、乱码、空白行的多层过滤
- **两路 Span 融合**：PyMuPDF（高精度）+ OCR（补漏）统一处理

下一篇，我们进入**公式识别系统**——这是 MinerU 最精彩的能力之一：用 UniMERNet 把数学公式图像转换成可编辑的 LaTeX 代码。

---

*← [第三篇：布局检测系统](./minerU_03_layout.md) | [第五篇：公式识别系统](./minerU_05_formula.md) →*
