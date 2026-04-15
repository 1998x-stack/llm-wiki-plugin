# MinerU 深度解析系列 · 第七篇
# 阅读顺序排序算法：让乱序内容块重新"按人类逻辑排队"

> **上一篇回顾**：布局检测、OCR、公式识别、表格识别各自完成了"内容块是什么"的问题。本篇解决最后的关键问题——"内容块应该按什么顺序排列"。

---

## 一、为什么阅读顺序是难题？

经过前几层处理，我们已经有了一页上所有内容块的列表，每个块都有 `bbox`、`type` 和 `content`。但这个列表是**空间无序**的——布局检测不保证任何特定的输出顺序。

对于单栏、从上到下的简单文档，"按 Y 坐标从小到大排序"就够了。但学术论文远比这复杂：

### 1.1 双栏论文的挑战

```
┌─────────────────────────────────────────┐
│              论文标题（单栏）            │
├────────────────────┬────────────────────┤
│ 摘要（左栏）       │ 摘要（右栏）       │  ← 应该：左栏上半 → 左栏下半
│                    │                    │     → 右栏上半 → 右栏下半
│ 1. 引言（左栏）    │ 2. 方法（右栏）   │     NOT：按Y坐标混排
│                    │                    │
└────────────────────┴────────────────────┘
```

如果简单按 Y 坐标排序，左栏的第一段会跳到右栏的第一段，内容完全混乱。

### 1.2 跨栏元素（span elements）

某些元素横跨多栏：
- 大型图片
- 宽表格
- 公式（有时）
- 章节标题

这些元素打断了分栏结构，需要特殊处理。

### 1.3 脚注（Footnotes）

脚注在页面底部，但语义上属于正文中对应位置，阅读时应该在段落结尾之后（或根本不打断正文流）。

### 1.4 图/表的图注关系

图注（Figure Caption）虽然物理上在图的下方，但在 Markdown 中应该紧跟在图的引用后面，而不是按物理位置出现。

---

## 二、MinerU 阅读顺序算法的总体设计

MinerU 的阅读顺序排序分为**三个子问题**：

```
1. 分区（Zoning）：把页面划分为若干阅读区域
        ↓
2. 区内排序（Intra-zone Ordering）：区域内的块按列排序
        ↓  
3. 区间排序（Inter-zone Ordering）：多个区域按全局逻辑排序
```

---

## 三、子问题一：分区算法

### 3.1 水平分割线检测

MinerU 首先寻找**水平分割线**——即将页面分隔成上下区域的边界。跨栏元素（如大标题、大图）往往就是这样的分割线：

```python
def find_horizontal_dividers(blocks, page_width, column_threshold=0.7):
    """
    找到跨越页面大部分宽度（> page_width * threshold）的块
    这些块将页面分割成多个水平带（bands）
    """
    dividers = []
    
    for block in blocks:
        block_width = block.bbox[2] - block.bbox[0]
        width_ratio = block_width / page_width
        
        if width_ratio > column_threshold:
            # 这是一个跨栏元素
            dividers.append(block)
    
    # 按 Y 坐标排序，得到从上到下的分割线顺序
    dividers.sort(key=lambda b: b.bbox[1])
    return dividers
```

### 3.2 构建水平带（Bands）

有了分割线，就可以把页面切成若干**水平带**：

```python
def build_bands(dividers, all_blocks, page_height):
    """
    根据分割线，把页面所有块分配到对应的水平带
    """
    # 用分割线的 Y 边界划定带的范围
    band_boundaries = [0]
    for div in dividers:
        band_boundaries.append(div.bbox[1])   # 分割块的顶部
        band_boundaries.append(div.bbox[3])   # 分割块的底部
    band_boundaries.append(page_height)
    
    bands = []
    for i in range(0, len(band_boundaries) - 1, 2):
        y_start = band_boundaries[i]
        y_end = band_boundaries[i + 1]
        
        # 找到Y范围在这个带内的普通块
        band_blocks = [
            b for b in all_blocks
            if b not in dividers
            and b.bbox[1] >= y_start
            and b.bbox[3] <= y_end
        ]
        bands.append({"y_range": (y_start, y_end), "blocks": band_blocks})
    
    return bands
```

### 3.3 每个带内的分栏检测

对每个水平带，检测是否有分栏结构：

```python
def detect_columns_in_band(band_blocks, page_width):
    """
    基于 X 坐标分布，检测带内是否有多列布局
    """
    if not band_blocks:
        return [band_blocks]  # 空带，单列
    
    # 统计所有块的 X 中心
    x_centers = [(b.bbox[0] + b.bbox[2]) / 2 for b in band_blocks]
    
    # 检测 X 中心是否形成明显的聚类
    mid_x = page_width / 2
    left_blocks = [b for b, cx in zip(band_blocks, x_centers) if cx < mid_x]
    right_blocks = [b for b, cx in zip(band_blocks, x_centers) if cx >= mid_x]
    
    # 如果左右两侧都有足够多的块，判断为双栏
    if len(left_blocks) >= 2 and len(right_blocks) >= 2:
        return [left_blocks, right_blocks]
    else:
        return [band_blocks]  # 单栏
```

---

## 四、子问题二：列内排序

在每一列（column）内，按 Y 坐标从小到大（从上到下）排序是基本规则。但有一些细节需要处理：

### 4.1 相邻行的合并判断

在同一列内，如果两个 `text` 块的间距小于行高，应该合并为一个段落：

```python
def should_merge_blocks(block_a, block_b):
    """判断两个紧邻的文字块是否应该合并成一段"""
    # 垂直间距
    vertical_gap = block_b.bbox[1] - block_a.bbox[3]
    
    # 估算行高（用块高度近似）
    avg_line_height = (
        block_a.bbox[3] - block_a.bbox[1] +
        block_b.bbox[3] - block_b.bbox[1]
    ) / 2
    
    # 间距小于 1.5 倍行高，且类别都是 text → 合并
    if vertical_gap < avg_line_height * 1.5:
        if block_a.type == "text" and block_b.type == "text":
            return True
    
    return False
```

### 4.2 图注与图的关联

图注（`figure_caption`）应该紧跟对应的图（`figure`），而不是按物理位置独立排序：

```python
def associate_captions(blocks):
    """将图注/表注与对应的图/表关联，并调整顺序"""
    figures = [b for b in blocks if b.type == "figure"]
    captions = [b for b in blocks if b.type == "figure_caption"]
    
    for caption in captions:
        # 找最近的图（Y 方向距离最小）
        best_figure = min(
            figures,
            key=lambda f: abs(
                (f.bbox[1] + f.bbox[3]) / 2 -
                (caption.bbox[1] + caption.bbox[3]) / 2
            ),
            default=None
        )
        if best_figure:
            best_figure.caption = caption
            blocks.remove(caption)  # 从独立列表中移除，附属于图
    
    return blocks
```

---

## 五、子问题三：全局区间排序

把所有水平带按 Y 坐标排序，每个带内的内容按列顺序展开：

```python
def build_global_reading_order(bands, dividers):
    """
    构建整页的全局阅读顺序
    
    策略：
    1. 分割线块（跨栏元素）在对应 Y 位置插入
    2. 普通带内容按列展开（左列 → 右列）
    """
    result_sequence = []
    
    # 将分割线和普通带交错排列（按 Y 坐标）
    all_segments = []
    
    for div in dividers:
        all_segments.append(("divider", div, div.bbox[1]))
    
    for band in bands:
        y_mid = (band["y_range"][0] + band["y_range"][1]) / 2
        all_segments.append(("band", band, y_mid))
    
    all_segments.sort(key=lambda s: s[2])  # 按 Y 坐标排序
    
    for seg_type, seg_data, _ in all_segments:
        if seg_type == "divider":
            result_sequence.append(seg_data)
        else:
            # 展开带内的列（左列先，右列后）
            columns = detect_columns_in_band(seg_data["blocks"], page_width)
            for column in columns:
                column.sort(key=lambda b: b.bbox[1])  # 列内按 Y 排序
                result_sequence.extend(column)
    
    return result_sequence
```

---

## 六、特殊情况：三栏及以上

部分文档（如报纸、宣传册）有三栏甚至四栏布局。MinerU 的分栏检测通过**聚类算法**处理：

```python
from sklearn.cluster import KMeans

def detect_multi_columns(band_blocks, max_columns=4):
    """使用 KMeans 检测多列布局"""
    if len(band_blocks) < 3:
        return [band_blocks]
    
    x_centers = [[
        (b.bbox[0] + b.bbox[2]) / 2
    ] for b in band_blocks]
    
    best_k = 1
    best_score = float('inf')
    
    # 尝试 1 到 max_columns 列
    for k in range(1, min(max_columns + 1, len(band_blocks))):
        kmeans = KMeans(n_clusters=k, n_init=3, random_state=42)
        kmeans.fit(x_centers)
        
        # 用轮廓系数或惯性判断最佳列数
        inertia = kmeans.inertia_
        # 简单启发：每增加一列，inertia 下降超过 30% 才值得
        if k == 1 or inertia < best_score * 0.7:
            best_score = inertia
            best_k = k
    
    # 按聚类中心 X 坐标排序，得到从左到右的列顺序
    if best_k == 1:
        return [band_blocks]
    
    kmeans = KMeans(n_clusters=best_k, n_init=3, random_state=42)
    labels = kmeans.fit_predict(x_centers)
    
    cluster_centers = kmeans.cluster_centers_.flatten()
    sorted_cluster_ids = np.argsort(cluster_centers)  # 按 X 从左到右
    
    columns = []
    for cluster_id in sorted_cluster_ids:
        column_blocks = [b for b, l in zip(band_blocks, labels) if l == cluster_id]
        columns.append(column_blocks)
    
    return columns
```

---

## 七、脚注的处理策略

脚注在 MinerU 的处理中被**降级处理**：

1. DocLayout-YOLO 会把脚注区域标记为 `text`（通常字号较小，Y 坐标很靠下）
2. MinerU 通过**字号检测**识别出脚注：字号比正文小 30% 以上 + 位于页面下 10% 区域
3. 脚注统一放到**页面末尾**，加上简单的 `---` 分隔符

```python
def handle_footnotes(sorted_blocks, page_height):
    """将识别出的脚注移到页面内容末尾"""
    footnote_threshold_y = page_height * 0.85  # 页面下 15% 区域
    
    main_blocks = []
    footnote_blocks = []
    
    for block in sorted_blocks:
        if (block.type == "text" and 
            block.bbox[1] > footnote_threshold_y and
            block.avg_font_size < BODY_FONT_SIZE * 0.8):
            footnote_blocks.append(block)
        else:
            main_blocks.append(block)
    
    if footnote_blocks:
        # 在末尾添加分隔线和脚注
        result = main_blocks + [SeparatorBlock("---")] + footnote_blocks
    else:
        result = main_blocks
    
    return result
```

---

## 八、阅读顺序的可视化验证

MinerU 提供了阅读顺序的可视化工具，用带编号的箭头显示内容块的阅读序列：

```python
def visualize_reading_order(page_image, sorted_blocks):
    """在页面图像上绘制阅读顺序序号"""
    img = page_image.copy()
    
    for idx, block in enumerate(sorted_blocks):
        x0, y0, x1, y1 = [int(c) for c in block.bbox]
        
        # 绘制边框
        color = TYPE_COLORS.get(block.type, (200, 200, 200))
        cv2.rectangle(img, (x0, y0), (x1, y1), color, 2)
        
        # 绘制序号
        label = str(idx + 1)
        cv2.putText(img, label, (x0 + 5, y0 + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    return img
```

这个可视化图在调试复杂布局（如混合单双栏的论文）时极其有用。

---

## 九、常见失败案例与解法

| 失败场景 | 原因 | 解法 |
|---------|------|------|
| 双栏内容混排 | 分栏检测阈值不当 | 调整 `column_threshold` |
| 图注被提前 | 图注与图的 Y 距离过大 | 放宽图注关联的搜索范围 |
| 页眉混入正文 | 页眉未被正确标记 | 加强页眉/页脚的 Y 位置过滤 |
| 跨页表格断裂 | 跨页内容无法关联 | 目前仅在单页内处理（已知局限） |
| 旋转页面 | 部分扫描件有旋转 | 页面级旋转矫正（预处理步骤）|

---

## 十、小结

阅读顺序排序算法是 MinerU 的"智慧大脑"：

- **三层架构**：分区 → 列内排序 → 全局区间排序
- **水平带划分**：用跨栏元素切割页面为水平段落
- **列检测**：KMeans 聚类处理任意栏数
- **图注关联**：确保图/表与说明文字紧密相连
- **脚注降级**：统一移至页面末尾

下一篇，我们将到达整个流水线的终点——**Markdown/JSON 内容生成器**，把有序的内容块序列化为人类可读、机器可用的最终输出。

---

*← [第六篇：表格识别系统](./minerU_06_table.md) | [第八篇：内容生成器](./minerU_08_output.md) →*
