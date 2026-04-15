# MinerU 深度解析系列 · 第六篇
# 表格识别系统：从像素到 Markdown 表格的结构还原

> **上一篇回顾**：UniMERNet 把公式图像转成 LaTeX。本篇处理另一个高难度任务——把表格图像还原成行列对齐的结构化数据。

---

## 一、表格识别：远比看起来难

### 1.1 表格结构的多样性

人眼看到表格，瞬间就能理解行列关系。但对算法来说，表格的变体数量惊人：

```
简单边框表格：         无边框表格（三线表）：    跨单元格表格：
┌──────┬──────┐         指标    A     B           ┌──┬────────┐
│ 姓名 │ 年龄 │         ──────────────────         │编│ 科目   │
├──────┼──────┤         准确率  90%  85%           │号│数学│英语│
│ 张三 │  25  │         召回率  88%  92%           ├──┼──┬─┼──┤
└──────┴──────┘                                    │1 │A │B│C │
                                                   └──┴──┴─┴──┘
```

三线表（无垂直线）在学术论文中极为常见，但"仅靠横线"来理解列关系，对算法是极大的挑战。跨行/跨列单元格（rowspan/colspan）更是将复杂度再上一个台阶。

### 1.2 PDF 中的表格存储

表格在 PDF 中有两种存储方式：

**方式一：矢量线条 + 文字**（常见于文字型 PDF）
- 边框线条是 PDF 路径命令
- 文字直接存储在表格内（可用 PyMuPDF 提取）
- 但文字的"哪个字属于哪个单元格"无法直接得知

**方式二：光栅图像**（常见于扫描件）
- 整个表格是一张图
- 必须用视觉方法识别

MinerU 的表格识别系统针对两种情况都有处理策略。

---

## 二、MinerU 的表格识别框架

MinerU 的表格识别分为两个阶段：

```
布局检测输出：table 框区域（bbox）
        ↓
┌───────────────────────────────┐
│  阶段一：表格结构识别           │
│  TableMaster / RapidTable     │
│  输入：表格图像                │
│  输出：HTML 格式的表格结构      │
└───────────────────┬───────────┘
                    │
                    ↓
┌───────────────────────────────┐
│  阶段二：单元格内容填充         │
│  文字型：PyMuPDF 坐标对应      │
│  扫描件：OCR 识别              │
│  输出：含文字的完整表格         │
└───────────────────┬───────────┘
                    │
                    ↓
           Markdown / HTML 表格
```

---

## 三、TableMaster：结构识别的核心模型

### 3.1 模型概述

MinerU 默认使用 **TableMaster**（来自 PaddleOCR 的 PP-Structure 模块），这是一个专为表格结构识别设计的模型。

TableMaster 的核心思路是将表格结构识别转化为**序列生成问题**：

```
输入：表格图像
输出：HTML token 序列，如：
  <html><body><table>
    <tr><td>姓名</td><td>年龄</td></tr>
    <tr><td>张三</td><td>25</td></tr>
  </table></body></html>
```

注意：输出的 HTML 中，单元格内容先用空的 `<td></td>` 占位，实际文字在第二阶段填充。

### 3.2 架构设计

```
表格图像
    ↓
ResNet + FPN（特征提取）
    ↓
特征图（含位置编码）
    ↓
Transformer Decoder（自回归生成 HTML tokens）
    ↓
HTML 结构字符串（含空单元格）
    ↓
解析为单元格网格（cell grid）
```

TableMaster 的词表包含 HTML 相关的特殊 token：

```python
TABLE_TOKEN_TABLE = {
    "<BOS>": 0,
    "<EOS>": 1,
    "<td>": 10,
    "</td>": 11,
    "<tr>": 12,
    "</tr>": 13,
    # 跨单元格
    '<td colspan="2">': 20,
    '<td colspan="3">': 21,
    '<td rowspan="2">': 30,
    '<td rowspan="2" colspan="2">': 40,
    # ... 覆盖常见的跨行/跨列组合
    "<b>": 50,   # 粗体（表头常见）
    "<i>": 51,   # 斜体
}
```

---

## 四、单元格边界框的预测

TableMaster 不仅生成 HTML token 序列，还需要预测**每个单元格的边界框**（bbox）。这个 bbox 用于第二阶段将文字内容分配到正确的单元格。

### 4.1 双任务输出

TableMaster 的 Decoder 头有两个分支：

```python
class TableMasterDecoder(nn.Module):
    def __init__(self):
        self.transformer_decoder = TransformerDecoder(...)
        
        # 分支1：token 分类（HTML token 是哪个）
        self.token_classifier = nn.Linear(hidden_dim, vocab_size)
        
        # 分支2：bbox 回归（单元格的位置）
        self.bbox_regressor = nn.Linear(hidden_dim, 4)  # (x0,y0,x1,y1)
    
    def forward(self, visual_features, target_tokens):
        hidden = self.transformer_decoder(visual_features, target_tokens)
        
        token_logits = self.token_classifier(hidden)  # 用于生成 HTML
        bbox_preds = self.bbox_regressor(hidden)       # 用于定位单元格
        
        return token_logits, bbox_preds
```

### 4.2 结果示例

对于一个 2×2 的简单表格，输出可能是：

```json
{
  "html": "<tr><td>姓名</td><td>年龄</td></tr><tr><td></td><td></td></tr>",
  "cell_bboxes": [
    {"row": 0, "col": 0, "bbox": [10, 5, 120, 30]},
    {"row": 0, "col": 1, "bbox": [125, 5, 230, 30]},
    {"row": 1, "col": 0, "bbox": [10, 35, 120, 60]},
    {"row": 1, "col": 1, "bbox": [125, 35, 230, 60]}
  ]
}
```

（注：bbox 是相对于表格图像裁剪区域的坐标）

---

## 五、单元格内容填充

### 5.1 文字型 PDF 的内容填充

对于文字型 PDF，表格内的文字在 PyMuPDF 提取的 Span 中已经存在，只需要根据坐标对应关系填充：

```python
def fill_table_cells_from_spans(cell_grid, page_spans, table_bbox):
    """
    cell_grid: 二维列表，每个元素是 cell 的 bbox（页面坐标）
    page_spans: 当前页面所有 Span
    table_bbox: 表格在页面中的位置
    """
    for row_idx, row in enumerate(cell_grid):
        for col_idx, cell in enumerate(row):
            # 将 cell bbox 从表格坐标转换为页面坐标
            cell_bbox_page = transform_to_page_coords(cell.bbox, table_bbox)
            
            # 找到中心点在这个 cell 内的所有 Span
            cell_spans = [
                span for span in page_spans
                if point_in_box(span_center(span), cell_bbox_page)
            ]
            
            # 按阅读顺序排列并拼接
            cell_spans.sort(key=lambda s: (s.bbox[1], s.bbox[0]))  # y 优先，x 其次
            cell.content = "".join(span.content for span in cell_spans)
```

### 5.2 扫描件的内容填充

扫描件需要对每个单元格区域单独做 OCR：

```python
def fill_table_cells_with_ocr(cell_grid, table_image, ocr_engine):
    for row in cell_grid:
        for cell in row:
            x0, y0, x1, y1 = [int(c) for c in cell.bbox]
            
            # 加 padding，避免裁剪到边框线
            padding = 3
            cell_img = table_image[
                max(0, y0+padding) : y1-padding,
                max(0, x0+padding) : x1-padding
            ]
            
            if cell_img.size == 0:
                cell.content = ""
                continue
            
            # 单元格 OCR（通常内容很短，速度快）
            results = ocr_engine.ocr(cell_img, cls=False)
            
            if results and results[0]:
                texts = [line[1][0] for line in results[0]]
                cell.content = " ".join(texts)
            else:
                cell.content = ""
```

---

## 六、跨单元格的处理逻辑

跨单元格（merged cells）是表格识别中最复杂的部分：

```
原始表格：
┌──────────────┬──────┐
│    课程信息   │      │  ← 跨 2 列的单元格
├──────┬───────┤ 成绩 │
│ 科目 │ 教师  │      │
└──────┴───────┴──────┘
```

TableMaster 通过 `colspan` / `rowspan` token 来表达这种关系：

```html
<tr>
  <td colspan="2">课程信息</td>
  <td rowspan="2">成绩</td>
</tr>
<tr>
  <td>科目</td>
  <td>教师</td>
</tr>
```

MinerU 在转换为 Markdown 时，由于 **Markdown 不支持跨单元格**，会做降级处理：

```python
def table_html_to_markdown(html: str) -> str:
    """将 HTML 表格转换为 Markdown 格式"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")
    
    markdown_rows = []
    for row_idx, row in enumerate(rows):
        cells = row.find_all(["td", "th"])
        cell_texts = []
        
        for cell in cells:
            text = cell.get_text(strip=True)
            colspan = int(cell.get("colspan", 1))
            
            # 跨列：复制内容到多个列（降级处理）
            for _ in range(colspan):
                cell_texts.append(text if _ == 0 else "↑")
        
        markdown_rows.append("| " + " | ".join(cell_texts) + " |")
        
        # 第一行后加分隔符
        if row_idx == 0:
            markdown_rows.append("|" + "|".join(["---"] * len(cell_texts)) + "|")
    
    return "\n".join(markdown_rows)
```

对于跨单元格，MinerU 在 JSON 输出中保留完整的 HTML 结构，Markdown 中做简化处理，并附注 `<!-- complex table, see JSON for full structure -->`。

---

## 七、三线表的特殊处理

学术论文最常见的是**三线表**（只有顶线、表头分隔线、底线，无竖线）：

```
指标     方法A   方法B   方法C
────────────────────────────
准确率   90.1   88.3   92.5
召回率   87.6   91.2   89.0
F1       88.8   89.7   90.7
```

检测三线表的挑战：没有垂直边框线，列边界靠"列内文字的水平对齐"来推断。

MinerU 的处理策略：
1. DocLayout-YOLO 识别出 `table` 框
2. TableMaster 通过学习到的特征，理解"列对齐"即使无竖线也能识别列边界
3. 表头行（第一行）通常是粗体，用来确定列数

---

## 八、输出格式

### 8.1 Markdown 输出（标准情况）

```markdown
| 方法 | 准确率 | 召回率 | F1 |
|------|--------|--------|-----|
| 方法A | 90.1 | 87.6 | 88.8 |
| 方法B | 88.3 | 91.2 | 89.7 |
| 方法C | 92.5 | 89.0 | 90.7 |
```

### 8.2 JSON 输出（带完整结构）

```json
{
  "type": "table",
  "bbox": [100, 200, 800, 450],
  "page_no": 3,
  "html": "<table>...</table>",
  "markdown": "| 方法 | 准确率 | ... |",
  "cell_data": [
    [{"content": "方法", "rowspan": 1, "colspan": 1, "bbox": [...]}],
    ...
  ]
}
```

---

## 九、小结

表格识别系统是 MinerU 最复杂的专项模块：

- **TableMaster**：Transformer 架构，生成 HTML token 序列 + 单元格 bbox
- **双阶段**：①结构识别（HTML）→②内容填充（Span 对应或 OCR）
- **跨单元格**：colspan/rowspan 处理，Markdown 降级
- **三线表**：无竖线情况下靠列对齐理解结构
- **输出多格式**：Markdown（通用）+ HTML（完整结构）+ JSON（机器可读）

下一篇，我们将进入 MinerU 的"大脑"——**阅读顺序排序算法**，这决定了最终内容的排列顺序是否符合人类阅读习惯。

---

*← [第五篇：公式识别系统](./minerU_05_formula.md) | [第七篇：阅读顺序算法](./minerU_07_reading_order.md) →*
