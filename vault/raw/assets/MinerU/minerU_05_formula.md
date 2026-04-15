# MinerU 深度解析系列 · 第五篇
# 公式识别系统：UniMERNet 如何把数学图像变成 LaTeX 代码

> **上一篇回顾**：PaddleOCR 完成了普通文字的识别。但数学公式有其独特的二维结构，普通 OCR 根本无法处理。本篇深入公式识别这个最精彩的模块。

---

## 一、公式识别：比 OCR 难得多

### 1.1 为什么公式识别是特殊问题？

普通文字是**一维序列**：字符从左到右（或从上到下）线性排列，OCR 的 CTC 解码天然适合。

数学公式是**二维树状结构**：

```
         a²  +  b²  =  c²
           ↑ 上标关系（非线性）

    ∫₀^∞ f(x) dx
     ↑  ↑ 下标/上标同时存在

     ⎛ a  b ⎞
     ⎝ c  d ⎠  矩阵：二维网格结构

    n!
    ──────
    k!(n-k)!  分数：竖直排列关系
```

普通文字识别模型把图像映射为**字符序列**，而公式识别需要把图像映射为 **LaTeX 字符串**——一种包含大量嵌套结构的领域特定语言（DSL）。

### 1.2 LaTeX 的复杂性

一个简单的贝叶斯公式：
```
P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}
```

它的 LaTeX 字符串包含：
- 希腊字母命令（`\frac`、`\cdot`）
- 嵌套结构（分子嵌套在 `\frac` 内）
- 特殊符号
- 精确的括号匹配

生成这样的字符串，不能用简单的 CTC 解码，需要**序列到序列（Seq2Seq）**的生成模型。

---

## 二、UniMERNet：专为数学公式设计的识别模型

### 2.1 模型概述

**UniMERNet**（Unified Mathematical Expression Recognition Network）是上海 AI Lab 开发的公式识别模型，专为 MinerU 配套设计，也单独开源。

它的设计哲学是"统一"：
- **统一行内公式和独立公式**：两种公式用同一模型处理
- **统一印刷体和手写体**：虽然 MinerU 主要处理印刷 PDF
- **统一简单和复杂公式**：从 `x + y = z` 到多行大型矩阵

### 2.2 整体架构：图像 → LaTeX 的 Encoder-Decoder

```
公式区域图像（裁剪后）
    ↓
┌─────────────────────────────┐
│  图像编码器（Vision Encoder） │
│  Swin Transformer / ViT     │
│  提取视觉特征序列            │
└──────────────┬──────────────┘
               │  特征序列（tokens）
               ↓
┌─────────────────────────────┐
│  文本解码器（Text Decoder）   │
│  Transformer Decoder         │
│  自回归生成 LaTeX token       │
└──────────────┬──────────────┘
               │
               ↓
          LaTeX 字符串
    \frac{P(B|A) \cdot P(A)}{P(B)}
```

这是一个标准的 **Image-to-Sequence** 架构，类似于图像描述（Image Captioning）任务。

---

## 三、视觉编码器：Swin Transformer

### 3.1 为什么用 Swin 而不是 CNN？

公式识别的图像特征需要捕获：
1. **局部笔画特征**：字符的具体形状（∫ vs ∮）
2. **全局位置关系**：上下标的相对位置、分数线的高度
3. **长距离依赖**：公式开头的 `\sum_` 和结尾的 `n=1` 之间的关联

Swin Transformer 的层级窗口注意力机制兼顾了这三点，且比纯 ViT 对小尺寸输入更友好。

### 3.2 公式图像的预处理

```python
def preprocess_formula_image(img: np.ndarray, target_height=96) -> torch.Tensor:
    """
    公式图像预处理：
    - 灰度化（公式通常是黑白的）
    - 归一化高度，宽度等比缩放
    - 白底黑字标准化（部分 PDF 可能是黑底白字）
    """
    # 转灰度
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    
    # 检测背景色，标准化为白底黑字
    mean_brightness = gray.mean()
    if mean_brightness < 128:  # 深色背景
        gray = 255 - gray      # 反转
    
    # 按高度缩放
    h, w = gray.shape
    scale = target_height / h
    new_w = min(int(w * scale), 1200)  # 限制最大宽度
    resized = cv2.resize(gray, (new_w, target_height))
    
    # 归一化 [0,1]，转 tensor
    tensor = torch.FloatTensor(resized) / 255.0
    return tensor.unsqueeze(0)  # 添加 channel 维度
```

---

## 四、文本解码器：自回归 LaTeX 生成

### 4.1 解码流程

解码器按照**自回归**方式逐 token 生成 LaTeX：

```
时间步 t=0: 输入 <BOS>  → 输出 \frac
时间步 t=1: 输入 \frac  → 输出 {
时间步 t=2: 输入 {      → 输出 P
时间步 t=3: 输入 P      → 输出 (
...
时间步 t=N: 输入 ...    → 输出 <EOS>  (终止)
```

每一步，解码器基于**当前已生成序列**和**图像特征**预测下一个 token。

### 4.2 Beam Search 解码

为了得到更高质量的 LaTeX 输出，UniMERNet 使用 **Beam Search**（束搜索）而非贪心解码：

```python
# 贪心解码（每步选最高概率的 token）：快，但不是全局最优
next_token = torch.argmax(logits, dim=-1)

# Beam Search（保留 K 条候选序列）：稍慢，但质量更好
from transformers import BeamSearchScorer

beam_scorer = BeamSearchScorer(
    batch_size=1,
    num_beams=4,       # 保留 4 条候选
    device=device,
    length_penalty=1.0  # 惩罚过长序列
)
```

Beam Size = 4 在公式识别中是常用配置，在质量和速度间取得平衡。

### 4.3 LaTeX Token 词表设计

UniMERNet 的词表不是字符级的，而是**LaTeX 命令级**的：

```python
# 词表中的一些例子
TOKEN_TABLE = {
    "<BOS>": 0,      # 序列开始
    "<EOS>": 1,      # 序列结束
    "<PAD>": 2,      # 填充
    "\\frac": 10,    # 分数命令
    "\\sum": 11,     # 求和符号
    "\\int": 12,     # 积分符号
    "\\alpha": 50,   # 希腊字母 α
    "\\beta": 51,
    "_{": 100,       # 下标开始
    "}": 101,        # 括号结束
    "^{": 102,       # 上标开始
    "a": 200,        # 普通字母
    "b": 201,
    # ... 共约 600 个 token
}
```

使用**命令级词表**（`\frac` 作为一个 token）而非字符级（`\`, `f`, `r`, `a`, `c` 五个 token），大大缩短了序列长度，提升了识别速度和准确率。

---

## 五、行内公式 vs 独立公式

MinerU 区分两种公式类型，处理方式略有不同：

### 5.1 独立公式（Display Equation）

```latex
\[
E = mc^2
\]
```

特征：
- 单独占一行（或多行）
- 通常有编号 "(1)"
- DocLayout-YOLO 检测为 `equation` 类别
- 图像区域相对完整，边界清晰

处理：裁剪整个 `equation` 框区域 → UniMERNet 识别 → 输出 `$$...$$`

### 5.2 行内公式（Inline Equation）

```latex
当 $x \to \infty$ 时，函数收敛...
```

特征：
- 嵌入在文字段落内部
- 通常比较短
- 布局检测**不会**单独标出（包含在 `text` 框内）

处理：更复杂，需要先检测行内公式的位置：

```
文字行 Span 序列：
"当 " | [公式图像区域] | " 时，函数收敛..."

→ 对每个 Span 检测：是否是图像（无文字层）？字体是否是数学字体？
→ 对可疑区域裁剪 → UniMERNet 识别
→ 合并回文字序列：当 $x \to \infty$ 时，函数收敛...
```

---

## 六、行内公式的检测：一个更难的子问题

行内公式的检测是 MinerU 中最复杂的逻辑之一。

### 6.1 文字型 PDF 中的行内公式

在文字型 PDF 中，行内公式通常以**特殊数学字体**出现（如 CMMI、Symbol 字体）。MinerU 通过字体名称检测：

```python
MATH_FONT_KEYWORDS = [
    "CMMI",      # Computer Modern Math Italic（LaTeX 默认数学字体）
    "CMSY",      # Computer Modern Symbol
    "CMR",       # Computer Modern Roman（用于数字）
    "MSAM",      # AMS Symbol
    "MSBM",      # AMS Blackboard Bold
    "mtmi",      # MathTime Pro Math Italic
    "Symbol",    # PostScript Symbol font
    "MT-Symbol",
]

def is_math_font(font_name: str) -> bool:
    return any(keyword in font_name for keyword in MATH_FONT_KEYWORDS)
```

检测到数学字体 Span 后，将其标记为行内公式候选，裁剪该区域送入 UniMERNet。

### 6.2 扫描件中的行内公式

扫描件没有字体信息。MinerU 使用一个**行内公式检测模型**（基于轻量 YOLO 变体）对文字行图像进行逐行扫描，检测公式区域的边界框。

---

## 七、LaTeX 后处理与规范化

UniMERNet 输出的原始 LaTeX 需要后处理：

### 7.1 语法修复

```python
def fix_latex_syntax(latex: str) -> str:
    # 修复未闭合的花括号
    open_count = latex.count('{')
    close_count = latex.count('}')
    if open_count > close_count:
        latex += '}' * (open_count - close_count)
    
    # 修复常见的识别错误
    latex = latex.replace('\\operaorname', '\\operatorname')
    latex = latex.replace('\\mathbf {', '\\mathbf{')
    
    # 移除多余的空格
    latex = re.sub(r'\s+', ' ', latex).strip()
    
    return latex
```

### 7.2 LaTeX 渲染验证

MinerU（可选）会尝试用 `sympy` 或 `latex2sympy` 解析生成的 LaTeX，如果解析失败则标记为低置信度：

```python
def verify_latex(latex: str) -> bool:
    try:
        from sympy.parsing.latex import parse_latex
        parse_latex(latex)
        return True
    except Exception:
        return False
```

### 7.3 输出格式

最终，公式以标准 Markdown 格式输出：
- 行内公式：`$E = mc^2$`
- 独立公式：`$$\int_0^\infty e^{-x} dx = 1$$`

---

## 八、识别能力边界

UniMERNet 的能力边界值得了解：

| 公式类型 | 识别准确率 | 说明 |
|---------|-----------|------|
| 标准单行公式 | 高（>90%） | LaTeX 生成的标准印刷体 |
| 多行对齐公式（align） | 中（60~80%） | 结构复杂，容易出错 |
| 大型矩阵 | 中（50~70%） | 维度高时出错率增加 |
| 化学结构式 | 低（<30%） | 非训练目标 |
| 手写公式 | 低（40~60%） | 扫描件中的手写标注 |

对于低置信度的识别结果，MinerU 会在输出 JSON 中标注，方便下游系统做降级处理（如直接引用图片而非 LaTeX）。

---

## 九、小结

公式识别系统是 MinerU 最精密的组件之一：

- **UniMERNet**：Swin Transformer 编码器 + Transformer 解码器，Image-to-LaTeX 架构
- **自回归解码**：逐 token 生成 LaTeX，Beam Search 提升质量
- **命令级词表**：`\frac` 作为单一 token，大幅提升效率
- **行内/独立公式区分**：两种不同的检测和处理策略
- **LaTeX 后处理**：语法修复 + 格式规范化

下一篇，我们将进入**表格识别系统**——另一个高难度的专项识别任务，还原表格的行列结构。

---

*← [第四篇：OCR 引擎](./minerU_04_ocr.md) | [第六篇：表格识别系统](./minerU_06_table.md) →*
