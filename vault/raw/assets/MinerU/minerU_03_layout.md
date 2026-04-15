# MinerU 深度解析系列 · 第三篇
# 布局检测系统：DocLayout-YOLO 如何"读懂"版面

> **上一篇回顾**：PyMuPDF 把 PDF 拆成带坐标的字符流和高清图像。本篇深入第三层——视觉布局检测，这是 MinerU 智能化的核心所在。

---

## 一、为什么需要布局检测？

即使有了 PyMuPDF 提取的所有字符坐标，我们依然**不知道**：
- 哪些字符属于同一个段落？
- 哪里是图片的图注，哪里是正文？
- 这是一个单栏 PDF 还是双栏 PDF？
- 这个区域是表格还是普通文字？
- 公式在哪里？

传统方法试图用**纯规则**（启发式）来解决：比如"Y 坐标接近的 Span 属于同一行"，"行间距大于某阈值则换段落"。但这类规则在面对复杂学术论文布局时极其脆弱。

MinerU 的解决方案：**先用深度学习模型对整个页面图像做语义分割式的区域检测，再基于检测结果组织内容**。这是一个典型的"先视觉理解，后文字处理"的架构哲学。

---

## 二、DocLayout-YOLO：专为文档设计的检测模型

### 2.1 模型来源

MinerU 的布局检测核心模型是 **DocLayout-YOLO**，这是上海 AI Lab 团队在标准 YOLO（You Only Look Once）目标检测框架基础上，针对文档页面专门优化的变体。

它属于 **One-Stage 目标检测器**，即一次前向推理即可得到所有区域的类别和边界框，速度比两阶段检测器（如 Faster R-CNN）快得多。

### 2.2 模型输入输出

```
输入：PDF 页面图像（numpy array，RGB，约 1654×2339 @ 200 DPI A4）

输出：N 个检测框，每个包含：
{
    "bbox": [x0, y0, x1, y1],   # 像素坐标
    "label": "text",             # 类别标签
    "score": 0.97                # 置信度
}
```

### 2.3 检测的类别体系

DocLayout-YOLO 输出以下语义类别：

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

---

## 三、YOLO 架构回顾与文档场景的特殊挑战

### 3.1 标准 YOLO 架构

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

### 3.2 文档场景的特殊挑战

文档布局检测与自然图像目标检测有本质差异：

**挑战1：极端长宽比**
表格可能很宽（宽/高 = 5:1），图注可能很窄（宽/高 = 20:1）。标准 YOLO 的 Anchor 设计为自然场景优化，需要专门针对文档调整 Anchor 比例。

**挑战2：密集重叠**
一列文字中，多个段落的 bbox 在竖直方向紧密排列，传统 NMS 容易错误合并。

**挑战3：小目标**
行内公式、上标、脚注序号等都是极小的文字区域，需要更高分辨率的特征图。

**挑战4：无纹理区域**
大段均匀文字区域的纹理特征很弱，模型需要理解"一大块字就是段落"这种语义。

### 3.3 DocLayout-YOLO 的针对性改进

1. **专用 Anchor 设计**：重新聚类文档数据集的 bbox 尺寸分布，生成适合文档的 9 个 Anchor
2. **高分辨率推理**：推理时保持较大的输入分辨率（如 1280×1280），保留文字细节
3. **文档专用训练集**：在 DocLayNet、PubLayNet、D4LA 等大规模文档数据集上预训练
4. **后处理调整**：NMS 阈值针对文档的密集布局重新调优

---

## 四、推理流程详解

### 4.1 预处理

```python
def preprocess_for_layout(img: np.ndarray, target_size=1280) -> np.ndarray:
    h, w = img.shape[:2]
    
    # 等比例缩放，长边对齐 target_size
    scale = target_size / max(h, w)
    new_h, new_w = int(h * scale), int(w * scale)
    img_resized = cv2.resize(img, (new_w, new_h))
    
    # Padding 到正方形（灰色填充，不失真）
    canvas = np.full((target_size, target_size, 3), 114, dtype=np.uint8)
    canvas[:new_h, :new_w] = img_resized
    
    # 归一化
    img_normalized = canvas.astype(np.float32) / 255.0
    img_normalized = (img_normalized - MEAN) / STD
    
    return img_normalized, scale  # scale 用于坐标反算
```

### 4.2 推理

```python
# MinerU 使用 ONNXRuntime 进行推理（GPU/CPU 自动选择）
import onnxruntime as ort

session = ort.InferenceSession(
    "doclayout_yolo.onnx",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)

input_tensor = img_normalized[np.newaxis, :]  # 添加 batch 维度
outputs = session.run(None, {"images": input_tensor})
```

### 4.3 后处理：坐标还原与 NMS

```python
def postprocess_layout(raw_output, scale, conf_threshold=0.25, iou_threshold=0.45):
    # raw_output shape: [1, num_predictions, 4+num_classes]
    predictions = raw_output[0][0]
    
    boxes, scores, class_ids = [], [], []
    
    for pred in predictions:
        x_center, y_center, width, height = pred[:4]
        class_logits = pred[4:]
        
        class_id = np.argmax(class_logits)
        confidence = class_logits[class_id]
        
        if confidence < conf_threshold:
            continue
        
        # 中心坐标格式 → 角点坐标格式
        x0 = (x_center - width / 2) / scale
        y0 = (y_center - height / 2) / scale
        x1 = (x_center + width / 2) / scale
        y1 = (y_center + height / 2) / scale
        
        boxes.append([x0, y0, x1, y1])
        scores.append(float(confidence))
        class_ids.append(int(class_id))
    
    # NMS 去重
    kept_indices = nms(boxes, scores, iou_threshold)
    
    return [
        {"bbox": boxes[i], "label": CLASS_NAMES[class_ids[i]], "score": scores[i]}
        for i in kept_indices
    ]
```

---

## 五、布局框的后处理与精化

### 5.1 布局框与 Span 的对齐

检测到布局框后，MinerU 需要将 PyMuPDF 提取的 **Span** 分配到对应的布局框内：

```python
def assign_spans_to_layout_boxes(spans, layout_boxes):
    for span in spans:
        span_center = (
            (span.bbox[0] + span.bbox[2]) / 2,
            (span.bbox[1] + span.bbox[3]) / 2
        )
        best_box = None
        best_iou = 0
        
        for box in layout_boxes:
            # 判断 span 中心是否在 layout box 内
            if point_in_box(span_center, box.bbox):
                iou = calc_iou(span.bbox, box.bbox)
                if iou > best_iou:
                    best_iou = iou
                    best_box = box
        
        if best_box:
            best_box.spans.append(span)
```

### 5.2 孤儿 Span 处理

有些 Span 可能没有落入任何布局框（比如页眉行间的小字），MinerU 将这些"孤儿 Span"通过就近原则分配，或直接丢弃（如置信度低的区域）。

### 5.3 布局框的合并与拆分

有时模型会把本应是一个段落的区域检测成两个框（漏检），或把两个区域误合并。MinerU 有一套规则：
- **合并**：两个相邻的 `text` 框，水平对齐、间距小于行高，且都在同一栏内 → 合并
- **拆分**：一个 `text` 框内的 Span 存在明显的左/右栏分界 → 按分界拆分

---

## 六、页面结构理解：单栏 vs 多栏

布局检测的一个重要副产品是**分栏信息**。MinerU 通过检测结果的水平分布来推断分栏：

```python
def detect_columns(layout_boxes, page_width):
    # 统计所有文本框的 x 中心分布
    x_centers = [
        (box.bbox[0] + box.bbox[2]) / 2
        for box in layout_boxes
        if box.label == "text"
    ]
    
    # 用 KMeans 或简单阈值判断是否双栏
    if max(x_centers) - min(x_centers) > page_width * 0.4:
        # 双栏：以页面中线为分界
        mid = page_width / 2
        left_boxes = [b for b in layout_boxes if center_x(b) < mid]
        right_boxes = [b for b in layout_boxes if center_x(b) >= mid]
        return [left_boxes, right_boxes]
    else:
        # 单栏
        return [layout_boxes]
```

这个分栏信息在**阅读顺序排序**（第七篇）中至关重要。

---

## 七、置信度阈值的影响

不同的置信度阈值对结果影响很大：

| 阈值 | 效果 |
|------|------|
| 过低（< 0.15） | 大量误检，噪声框增多 |
| **MinerU 默认（0.25）** | **平衡准确率和召回率** |
| 过高（> 0.6） | 漏检增多，小区域（图注、公式编号）大量丢失 |

MinerU 对不同类别使用不同的阈值：公式/表格（类别重要，宁可误检不可漏检）使用较低阈值，页眉/页脚使用较高阈值。

---

## 八、可视化调试

MinerU 提供了布局检测的可视化输出，颜色编码不同类别：

```python
LAYOUT_COLORS = {
    "text":             (0, 128, 255),   # 蓝色
    "title":            (255, 0, 0),     # 红色
    "figure":           (0, 200, 0),     # 绿色
    "figure_caption":   (0, 150, 0),     # 深绿
    "table":            (255, 165, 0),   # 橙色
    "table_caption":    (200, 130, 0),   # 深橙
    "equation":         (128, 0, 255),   # 紫色
    "header":           (128, 128, 128), # 灰色
    "footer":           (100, 100, 100), # 深灰
}
```

这些可视化图（可通过 `--debug` 参数生成）对调试解析问题极其有帮助。

---

## 九、小结

布局检测层是 MinerU 的"智慧之眼"：

- **DocLayout-YOLO**：专为文档设计的 YOLO 变体，输出语义区域标注
- **11个类别**：涵盖文字、标题、图表、公式、页眉页脚等
- **推理管道**：图像预处理 → ONNX 推理 → NMS 后处理 → 坐标还原
- **Span 对齐**：把 PyMuPDF 的字符坐标与检测框对应起来
- **分栏检测**：为后续阅读顺序排序提供结构信息

下一篇，我们将进入 **OCR 引擎层**——当 PDF 没有文字层（或文字层不可信）时，MinerU 如何用 PaddleOCR 识别文字。

---

*← [第二篇：底层 PDF 解析引擎](./minerU_02_pdf_parsing.md) | [第四篇：OCR 引擎](./minerU_04_ocr.md) →*
