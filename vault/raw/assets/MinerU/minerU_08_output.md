# MinerU 深度解析系列 · 第八篇
# 内容生成器：从有序内容块到 Markdown、JSON 与多模态输出

> **上一篇回顾**：阅读顺序算法把乱序的内容块重新排列为正确的序列。本篇是系列的终篇，讲解 MinerU 如何把这个有序序列序列化为最终输出。

---

## 一、内容生成器的核心职责

经过七层处理后，我们拥有了一个**有序的内容块列表**，每个块已经包含：
- `type`：内容类型（text/title/figure/table/formula/...）
- `content`：文字内容（或 LaTeX 字符串）
- `bbox`：页面坐标
- `page_no`：所在页码
- 关联的图片、表格结构等

内容生成器的任务是把这个列表序列化为**人类可读、机器可用**的格式。

MinerU 主要支持以下输出格式：
1. **Markdown**（`.md`）：主要格式，可直接用于 RAG/LLM 输入
2. **JSON**（`.json`）：完整的结构化数据，带坐标信息
3. **内容目录**（`.md` 附录）：自动提取的标题层级树
4. **图片资源**（`images/` 目录）：提取的嵌入图像

---

## 二、Markdown 生成器

### 2.1 块类型到 Markdown 的映射规则

```python
def block_to_markdown(block: ContentBlock) -> str:
    """将单个内容块转换为 Markdown 字符串"""
    
    if block.type == "title":
        # 标题：根据字号和层级判断 H1~H4
        level = estimate_heading_level(block)
        prefix = "#" * level
        return f"{prefix} {block.content}\n\n"
    
    elif block.type == "text":
        # 普通段落：直接输出，尾部加空行
        return f"{block.content}\n\n"
    
    elif block.type == "equation":
        # 独立公式：$$...$$
        return f"$$\n{block.latex}\n$$\n\n"
    
    elif block.type == "table":
        # 表格：输出 Markdown 表格
        if block.has_complex_structure:
            # 复杂表格（有跨单元格）：先输出原始 HTML
            return f"\n<!-- Table with merged cells -->\n{block.html}\n\n"
        else:
            return f"{block.markdown_table}\n\n"
    
    elif block.type == "figure":
        # 图像：输出图片引用
        img_path = save_figure_image(block)
        caption = block.caption.content if block.caption else ""
        return f"![{caption}]({img_path})\n\n{caption}\n\n"
    
    elif block.type in ("header", "footer"):
        # 页眉页脚：跳过
        return ""
    
    elif block.type == "figure_caption":
        # 已被附属到 figure，不单独输出
        return ""
    
    elif block.type == "reference":
        # 参考文献：作为无序列表输出
        refs = split_references(block.content)
        lines = [f"- {ref}" for ref in refs]
        return "\n".join(lines) + "\n\n"
    
    else:
        # 未知类型：原样输出
        return f"{block.content}\n\n"
```

### 2.2 标题层级推断

MinerU 通过**字号相对大小**来推断标题层级：

```python
def estimate_heading_level(title_block: ContentBlock) -> int:
    """
    根据字号和粗体状态，推断标题层级（H1~H4）
    """
    font_size = title_block.avg_font_size
    
    # 全局字号统计（在页面分析阶段计算）
    body_font_size = title_block.document_body_font_size  # 正文基准字号
    
    size_ratio = font_size / body_font_size
    
    if size_ratio >= 1.8:
        return 1  # H1：章标题
    elif size_ratio >= 1.4:
        return 2  # H2：节标题
    elif size_ratio >= 1.15:
        return 3  # H3：小节标题
    else:
        return 4  # H4：段落标题（与正文字号接近但有粗体）
```

**注意**：纯靠字号推断并不总是可靠，部分论文使用 Section 1.2.3 这样的编号系统，MinerU 也会检测编号模式辅助判断层级。

---

## 三、行内格式的处理

### 3.1 行内公式

行内公式以 `$...$` 形式嵌入段落：

```python
def merge_inline_formulas(text_block: ContentBlock) -> str:
    """
    将行内公式占位符替换为真实的 LaTeX
    
    text_block.content 可能包含：
    "当 {{FORMULA:0}} 时，函数收敛到 {{FORMULA:1}}"
    
    block.inline_formulas = {0: "x \\to \\infty", 1: "L"}
    """
    result = text_block.content
    for formula_id, latex in text_block.inline_formulas.items():
        placeholder = f"{{{{FORMULA:{formula_id}}}}}"
        result = result.replace(placeholder, f"${latex}$")
    return result
```

### 3.2 粗体和斜体

在文字型 PDF 中，PyMuPDF 提供了字体的粗体/斜体信息，MinerU 将其转换为 Markdown 格式：

```python
def apply_text_styles(spans: List[MinerUSpan]) -> str:
    """将带样式的 Span 序列转换为带 Markdown 格式标记的文字"""
    result = ""
    for span in spans:
        text = span.content
        
        # 粗体
        if span.font_weight == "bold":
            text = f"**{text}**"
        
        # 斜体
        if span.font_style == "italic":
            text = f"*{text}*"
        
        # 等宽（代码）
        if span.is_monospace:
            text = f"`{text}`"
        
        result += text
    
    return result
```

---

## 四、图片资源管理

每个 `figure` 块对应一张图片，MinerU 需要提取并保存它：

```python
import os
import hashlib

def save_figure_image(figure_block: ContentBlock, output_dir: str) -> str:
    """
    提取图像并保存到 output_dir/images/ 目录
    返回相对路径，用于 Markdown 引用
    """
    img_dir = os.path.join(output_dir, "images")
    os.makedirs(img_dir, exist_ok=True)
    
    # 计算图像内容的哈希，作为文件名（去重）
    img_bytes = figure_block.image_bytes
    img_hash = hashlib.md5(img_bytes).hexdigest()[:8]
    
    filename = f"figure_p{figure_block.page_no}_{img_hash}.png"
    filepath = os.path.join(img_dir, filename)
    
    if not os.path.exists(filepath):
        with open(filepath, "wb") as f:
            f.write(img_bytes)
    
    # 返回相对路径（相对于 md 文件的位置）
    return f"images/{filename}"
```

---

## 五、JSON 输出格式

JSON 输出保留了比 Markdown 更丰富的结构信息：

```json
{
  "pdf_info": [
    {
      "page_no": 1,
      "width": 595.28,
      "height": 841.89,
      "blocks": [
        {
          "type": "title",
          "bbox": [72.0, 60.0, 523.0, 85.0],
          "content": "Attention Is All You Need",
          "font_size": 18.0,
          "heading_level": 1
        },
        {
          "type": "text",
          "bbox": [72.0, 120.0, 523.0, 200.0],
          "content": "The dominant sequence transduction models...",
          "lines": [
            {"bbox": [...], "content": "The dominant sequence..."},
            {"bbox": [...], "content": "transduction models..."}
          ]
        },
        {
          "type": "equation",
          "bbox": [200.0, 350.0, 395.0, 380.0],
          "latex": "\\text{Attention}(Q,K,V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V",
          "equation_number": "(1)"
        },
        {
          "type": "table",
          "bbox": [72.0, 450.0, 523.0, 600.0],
          "markdown": "| 模型 | BLEU | ... |\n|---|---|...|\n",
          "html": "<table>...</table>",
          "caption": "Table 1: Machine translation results."
        },
        {
          "type": "figure",
          "bbox": [150.0, 650.0, 445.0, 820.0],
          "image_path": "images/figure_p1_a3f2c1b0.png",
          "caption": "Figure 1: The Transformer architecture."
        }
      ]
    }
  ],
  "metadata": {
    "total_pages": 15,
    "parse_time_seconds": 23.4,
    "pipeline": "text_based",
    "models_used": ["doclayout_yolo", "unimernet", "tablemaster"],
    "minerU_version": "1.x.x"
  }
}
```

---

## 六、内容目录（TOC）生成

MinerU 自动从标题块中提取目录：

```python
def generate_table_of_contents(all_sorted_blocks: List[ContentBlock]) -> str:
    """从所有页面的有序块中提取标题，生成 Markdown 目录"""
    toc_lines = ["# 目录\n"]
    
    for block in all_sorted_blocks:
        if block.type != "title":
            continue
        
        level = block.heading_level
        indent = "  " * (level - 1)
        
        # 生成 Markdown 锚点（标题文字转小写，空格→-）
        anchor = block.content.lower().replace(" ", "-")
        anchor = re.sub(r"[^\w-]", "", anchor)  # 只保留字母数字和-
        
        toc_lines.append(f"{indent}- [{block.content}](#{anchor})")
    
    return "\n".join(toc_lines)
```

---

## 七、多页面内容的拼接

MinerU 逐页处理后，需要将所有页面的输出拼接为完整文档：

```python
def assemble_full_document(pages_output: List[str]) -> str:
    """
    拼接多页输出
    
    核心问题：跨页段落合并
    如果第 N 页最后一个段落和第 N+1 页第一个段落是同一个段落的两部分
    （段落在分页处被打断），需要合并。
    """
    
    result_parts = []
    
    for page_idx, page_md in enumerate(pages_output):
        if page_idx == 0:
            result_parts.append(page_md)
            continue
        
        prev_page = result_parts[-1] if result_parts else ""
        
        # 检测跨页段落：前页末尾不以句号/问号等结束，
        # 且当前页开头是小写字母（英文）或中文字符
        prev_ends_incomplete = not re.search(r'[。！？.!?]\s*$', prev_page.rstrip())
        curr_starts_continuation = re.match(r'^[a-z\u4e00-\u9fff]', page_md.lstrip())
        
        if prev_ends_incomplete and curr_starts_continuation:
            # 跨页段落：移除前页末尾的换行，直接拼接
            result_parts[-1] = result_parts[-1].rstrip('\n')
            result_parts.append(" " + page_md.lstrip())
        else:
            result_parts.append("\n\n" + page_md)
    
    return "".join(result_parts)
```

---

## 八、输出质量控制

### 8.1 内容完整性检查

```python
def quality_check(markdown_output: str, source_pdf_path: str) -> dict:
    """简单的输出质量自检"""
    doc = fitz.open(source_pdf_path)
    total_pages = len(doc)
    
    # 统计各类内容
    formula_count = markdown_output.count("$$")
    table_count = markdown_output.count("|---|")
    word_count = len(markdown_output.split())
    
    # 估算：平均每页应有的词数（中英文混合按字符估算）
    chars_per_page = len(markdown_output) / total_pages
    
    return {
        "total_pages": total_pages,
        "output_chars": len(markdown_output),
        "chars_per_page_avg": chars_per_page,
        "formula_blocks": formula_count // 2,  # $$ 出现成对
        "table_count": table_count,
        "quality_warning": chars_per_page < 200  # 过少说明可能有问题
    }
```

### 8.2 空白页过滤

```python
def filter_empty_pages(pages_output: List[str]) -> List[str]:
    """过滤掉几乎没有内容的页面输出（如纯图像页、版权页等）"""
    return [
        page for page in pages_output
        if len(page.strip()) > 50  # 少于 50 字符视为空白页
    ]
```

---

## 九、命令行接口与 Python API

### 9.1 命令行使用

```bash
# 基本使用（文字型 PDF）
magic-pdf -p paper.pdf -o output_dir/

# 指定后端（强制使用 OCR 管道）
magic-pdf -p scanned.pdf -o output_dir/ --backend ocr

# 调试模式（输出布局检测可视化）
magic-pdf -p paper.pdf -o output_dir/ --debug

# 批量处理
magic-pdf -p papers/ -o output_dir/ --workers 4
```

### 9.2 Python API

```python
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.data.data_reader_writer import FileBasedDataWriter

# 读取 PDF
pdf_bytes = open("paper.pdf", "rb").read()

# 输出目录
writer = FileBasedDataWriter("output/")

# 创建管道（auto 模式自动判断文字型/扫描件）
pipe = UNIPipe(
    pdf_bytes=pdf_bytes,
    jso_useful_key={"_pdf_type": "auto", "model_list": []},
    image_writer=writer,
)

# 分类（判断 PDF 类型）
pipe.pipe_classify()

# 分析（运行布局检测、公式/表格识别）
pipe.pipe_analyze()

# 解析（生成输出）
pipe.pipe_parse()

# 获取 Markdown 内容
md_content = pipe.get_markdown(image_dir="images")

# 获取 JSON 内容
json_content = pipe.get_json()

print(md_content[:500])
```

---

## 十、输出示例：一个完整的 Markdown 片段

以下是 MinerU 处理一篇论文页面后的 Markdown 输出示例：

```markdown
## 3. Methodology

### 3.1 Attention Mechanism

The scaled dot-product attention is defined as:

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

where $Q$, $K$, $V$ are query, key, and value matrices respectively,
and $d_k$ is the dimension of the key vectors.

### 3.2 Experimental Results

| Model | BLEU-4 | ROUGE-L | Params |
|-------|--------|---------|--------|
| Baseline | 28.4 | 42.1 | 65M |
| **Ours** | **31.7** | **45.3** | 67M |

![The overall architecture of our proposed model.](images/figure_p3_b2a1c4d0.png)

Figure 3: The overall architecture of our proposed model.
```

---

## 十一、系列总结：MinerU 的七层流水线全图

至此，我们完成了对 MinerU 完整框架的深度解析。让我们做一个最终的全景总结：

```
PDF 文件
   │
   ▼ [第二篇：底层 PDF 解析]
PyMuPDF 提取字符 Span + 渲染页面图像
   │
   ▼ [第三篇：布局检测]
DocLayout-YOLO → 11类语义区域框
   │
   ├──▶ [第四篇：OCR] PaddleOCR → 文字 Span
   │
   ├──▶ [第五篇：公式识别] UniMERNet → LaTeX
   │
   └──▶ [第六篇：表格识别] TableMaster → HTML/Markdown
   │
   ▼ [第七篇：阅读顺序]
分区 + 分栏检测 + 全局排序 → 有序内容块序列
   │
   ▼ [第八篇：内容生成]
块类型映射 + 行内格式 + 跨页拼接
   │
   ▼
Markdown + JSON + 图片资源
```

### 技术选型总结

| 层次 | 模型/工具 | 选型理由 |
|------|---------|---------|
| PDF 解析 | PyMuPDF | 速度快，坐标精确，中文支持好 |
| 布局检测 | DocLayout-YOLO | 文档专用 YOLO，速度快，精度高 |
| OCR | PaddleOCR PP-OCRv4 | 中文能力最强，工业验证 |
| 公式识别 | UniMERNet | 专为数学公式设计，准确率高 |
| 表格识别 | TableMaster | 支持复杂跨单元格，HTML 输出 |
| 阅读顺序 | 规则 + 简单聚类 | 可解释性强，无需额外模型 |
| 输出生成 | 自定义渲染器 | 精细控制输出格式 |

---

## 十二、MinerU 的局限性与未来方向

**当前局限**：
- 跨页内容关联（如跨页表格）支持有限
- 复杂手写内容（批注、手写公式）识别精度低
- 某些特殊排版（竖排中文、RTL 阿拉伯文）支持不完整
- 大型 PDF（500页+）处理速度仍有优化空间

**未来方向**：
- 引入更强的多模态模型（如 DocVLM）做端到端理解
- 支持 Word/PowerPoint 等非 PDF 格式
- 流式处理（边解析边输出）降低首字节延迟
- 与 RAG 框架的深度集成（带 chunk 策略的结构化输出）

---

*← [第七篇：阅读顺序算法](./minerU_07_reading_order.md)*

---

**系列完结** | *MinerU 深度解析系列 · 共 8 篇*

| 篇序 | 主题 | 文件 |
|------|------|------|
| 1 | 整体架构全景 | `minerU_01_architecture.md` |
| 2 | 底层 PDF 解析引擎 | `minerU_02_pdf_parsing.md` |
| 3 | 布局检测系统 | `minerU_03_layout.md` |
| 4 | OCR 引擎 | `minerU_04_ocr.md` |
| 5 | 公式识别系统 | `minerU_05_formula.md` |
| 6 | 表格识别系统 | `minerU_06_table.md` |
| 7 | 阅读顺序排序算法 | `minerU_07_reading_order.md` |
| 8 | 内容生成器与输出管道 | `minerU_08_output.md` |
