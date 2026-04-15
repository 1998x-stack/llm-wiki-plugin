# MinerU 深度解析系列 · 第二篇
# 底层 PDF 解析引擎：PyMuPDF 如何把 PDF 拆解成坐标字符流

> **上一篇回顾**：MinerU 的整体架构是一条七层流水线。本篇深入第一层——底层 PDF 解析，这是整个系统的数据源头。

---

## 一、PDF 内部结构：你以为在看文字，实际在看坐标

理解 MinerU 的解析引擎，必须先理解 PDF 格式的本质。

一个 PDF 文件的内部，核心是**内容流（Content Stream）**，这是一系列 PostScript 风格的绘图命令。例如：

```postscript
BT                          % Begin Text
/F1 12 Tf                   % 使用字体 F1，字号 12pt
100 700 Td                  % 移动到坐标 (100, 700)
(Hello, World!) Tj          % 绘制字符串
ET                          % End Text
```

这意味着：
1. PDF 不存储"段落"，只存储"在 X,Y 位置用 Z 字体画出字符 C"
2. 字符的顺序由**坐标位置**隐含，而非显式的语义结构
3. 多栏布局、页眉页脚、侧边注释，在内部没有任何区别，全是同级别的绘图命令

### 1.1 PDF 坐标系

PDF 使用以**左下角为原点**的坐标系，单位是 **point（pt）**：
- 1 inch = 72 pt
- A4 纸：595.28 × 841.89 pt
- 坐标 `(0, 0)` 是页面左下角

> ⚠️ 注意：渲染到屏幕/图像时通常会 Y 轴翻转（屏幕坐标以左上角为原点），MinerU 内部需要处理这个转换。

---

## 二、PyMuPDF（fitz）：MinerU 的底层 PDF 解析库

MinerU 选择 **PyMuPDF**（Python 绑定名为 `fitz`）作为底层 PDF 解析库，而非 `pdfminer` 或 `pypdf`。

### 2.1 为什么是 PyMuPDF？

| 特性 | PyMuPDF | pdfminer | pypdf |
|------|---------|---------|-------|
| **速度** | ✅ 极快（C++ 内核 MuPDF） | 慢（纯 Python） | 中 |
| **字符精度** | ✅ 亚像素级坐标 | ✅ | ⚠️ 有限 |
| **图像渲染** | ✅ 可渲染为 PIL/numpy | ❌ | ❌ |
| **字体信息** | ✅ 字体名/大小/粗斜体 | ✅ | ⚠️ |
| **嵌入图片提取** | ✅ | ⚠️ | ⚠️ |
| **中文 PDF** | ✅ | ⚠️ 有问题 | ⚠️ |

PyMuPDF 底层是 **MuPDF**——这是业界公认最优秀的 PDF 渲染引擎之一（Foxit 阅读器也基于它）。

### 2.2 MinerU 使用 PyMuPDF 的三个核心操作

**操作一：页面渲染为图像**
```python
import fitz  # PyMuPDF

doc = fitz.open("paper.pdf")
page = doc[0]  # 第一页

# 渲染为图像（DPI 控制分辨率）
# matrix = fitz.Matrix(dpi/72, dpi/72)
matrix = fitz.Matrix(2.0, 2.0)  # 2x 缩放 ≈ 144 DPI
pixmap = page.get_pixmap(matrix=matrix)
img_bytes = pixmap.tobytes("png")
```

MinerU 将每页渲染为高分辨率图像，用于后续的**布局检测模型**和**OCR 模型**推理。

**操作二：提取文字 Span（带坐标）**
```python
# 提取页面文字块（详细模式）
blocks = page.get_text("rawdict", flags=fitz.TEXT_PRESERVE_WHITESPACE)

# 结构：blocks → lines → spans → chars
for block in blocks["blocks"]:
    if block["type"] == 0:  # type=0 是文字块，type=1 是图像块
        for line in block["lines"]:
            for span in line["spans"]:
                print({
                    "text": span["text"],
                    "bbox": span["bbox"],      # (x0, y0, x1, y1)
                    "font": span["font"],      # 字体名
                    "size": span["size"],      # 字号（pt）
                    "flags": span["flags"],    # 粗体/斜体等标志位
                    "color": span["color"],    # 文字颜色
                    "origin": span["origin"],  # 基线坐标
                })
```

**操作三：提取嵌入图像**
```python
# 获取页面上的图像列表
image_list = page.get_images(full=True)
for img in image_list:
    xref = img[0]
    base_image = doc.extract_image(xref)
    img_bytes = base_image["image"]
    img_ext = base_image["ext"]  # "png", "jpeg" 等
```

---

## 三、Span 层级结构与信息提取

### 3.1 四级嵌套结构

PyMuPDF 的文字提取遵循四级嵌套：

```
Page（页面）
└── Block（块：连续文字或图像区域）
    └── Line（行：同一基线上的文字）
        └── Span（片段：同一字体属性的连续字符）
            └── Char（字符，rawdict 模式下可获取）
```

**Span** 是 MinerU 最核心的处理单元。一个 Span 代表一段具有**相同字体、大小、颜色**的连续文字，且 bbox 精确。

### 3.2 flags 字段解码

`span["flags"]` 是一个位掩码，MinerU 用它来判断文字属性：

```python
# PyMuPDF 字体 flags 位定义
FLAG_SUPERSCRIPT = 1    # 上标
FLAG_ITALIC      = 2    # 斜体
FLAG_SERIFED     = 4    # 衬线字体（Times 风格）
FLAG_MONOSPACED  = 8    # 等宽字体（Courier 风格）
FLAG_BOLD        = 16   # 粗体

# 示例：判断是否粗体
is_bold = bool(span["flags"] & 16)
# 判断是否斜体
is_italic = bool(span["flags"] & 2)
```

MinerU 用粗体+字号来**推断标题层级**，是后续分类系统的重要输入。

---

## 四、PDF 类型判断算法

在解析之前，MinerU 先要判断这个 PDF 是"文字型"还是"扫描件"，这决定走哪条管道。

### 4.1 判断逻辑

```python
def classify_pdf_type(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    text_page_count = 0
    image_page_count = 0
    
    for page in doc:
        # 获取页面文字
        text = page.get_text().strip()
        # 获取页面图像列表
        images = page.get_images()
        
        # 判断：有足够文字 → 文字页
        if len(text) > 100:
            text_page_count += 1
        # 判断：大图覆盖全页且无文字 → 扫描页
        elif images and len(text) < 10:
            image_page_count += 1
    
    text_ratio = text_page_count / total_pages
    
    if text_ratio > 0.8:
        return "text_based"
    elif text_ratio < 0.2:
        return "ocr_based"
    else:
        return "mixed"
```

### 4.2 特殊情况处理

**情况1：文字型 PDF 但有图表**
论文中的图、表通常以图像形式嵌入，即使是文字型 PDF，这些区域也需要 OCR。MinerU 在 Layout 检测后，对图/表区域内的文字（图注、表头等）补充 OCR。

**情况2：加密 PDF**
PyMuPDF 支持解密：
```python
doc = fitz.open("encrypted.pdf")
if doc.is_encrypted:
    doc.authenticate("password")
```

**情况3：损坏/非标准 PDF**
MinerU 捕获 PyMuPDF 的异常，降级到图像模式处理。

---

## 五、图像渲染参数的影响

MinerU 渲染 PDF 页面时，分辨率选择至关重要：

| DPI | 分辨率（A4） | 适用场景 | 显存占用 |
|-----|------------|---------|---------|
| 72 | 595×842 | 仅预览 | 低 |
| 150 | 1240×1754 | 基础 OCR | 中 |
| **200** | **1654×2339** | **MinerU 默认** | 中 |
| 300 | 2480×3508 | 高精度 OCR | 高 |

MinerU 默认使用 **200 DPI**，在准确率和速度之间取得平衡。

**实际渲染代码（MinerU 简化版）**：
```python
def render_page_to_image(page, dpi=200):
    scale = dpi / 72
    matrix = fitz.Matrix(scale, scale)
    pixmap = page.get_pixmap(
        matrix=matrix,
        alpha=False,        # 不需要透明通道
        colorspace=fitz.csRGB  # RGB 彩色
    )
    # 转为 numpy array 供模型推理
    import numpy as np
    img_array = np.frombuffer(pixmap.samples, dtype=np.uint8)
    img_array = img_array.reshape(pixmap.height, pixmap.width, 3)
    return img_array
```

---

## 六、原始 Span 的噪声问题

PyMuPDF 提取的原始 Span 数据质量良莠不齐，MinerU 需要处理以下噪声：

### 6.1 常见噪声类型

**噪声1：超短 Span（单字符/空格）**
```
[" ", " ", "H", "e", "l", "l", "o"]  # 不合理的碎片化
```
MinerU 通过**同行 Span 合并**处理：相邻 Span 如果字体相同且间距合理，合并成一个。

**噪声2：水印文字**
水印通常以旋转、半透明、覆盖整页的方式出现。MinerU 通过检测：
- `span["color"]` 接近页面背景色（浅灰）
- Span 的旋转角度（通过变换矩阵检测）
- Span bbox 面积过大

**噪声3：页眉页脚**
通过页面顶部/底部固定区域的文字，且多页相似内容来识别。后续在布局检测阶段会被标记为 `header`/`footer` 类型过滤。

**噪声4：重叠 Span**
部分 PDF 生成工具会生成内容完全相同、位置重叠的 Span（为了达到"加粗"视觉效果）。MinerU 检测重叠并去重。

---

## 七、Span → MinerU 内部格式转换

MinerU 把 PyMuPDF 的原始数据转换为自己的内部 Span 格式：

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
    type: str                               # "text" / "inline_equation" 等
```

关键转换步骤：
1. **坐标归一化**：PDF 坐标（左下原点）→ 图像坐标（左上原点）
2. **字体解析**：从字体名推断是否中文、是否等宽
3. **初步类型标注**：检测等宽字体 → 可能是代码

---

## 八、小结

底层 PDF 解析层是整个 MinerU 系统的**数据基础**：

- **PyMuPDF 负责两件事**：①渲染为图像（供视觉模型使用）；②提取字符坐标（供文字管道使用）
- **PDF 类型判断**决定走哪条处理管道
- **原始 Span 数据有噪声**，MinerU 需要清洗
- **200 DPI 渲染**是准确率与速度的平衡点

下一篇，我们将深入**布局检测系统**——这是 MinerU 最关键的视觉智能层，决定了"这一块区域是什么"。

---

*← [第一篇：整体架构全景](./minerU_01_architecture.md) | [第三篇：布局检测系统](./minerU_03_layout.md) →*
