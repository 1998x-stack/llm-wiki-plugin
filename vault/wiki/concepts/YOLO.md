---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags: ["技术", "AI", "目标检测", "计算机视觉"]
aliases:
  - YOLO
  - You Only Look Once
relates_to:
  - target: '[[DocLayout-YOLO]]'
    type: extends
    confidence: 0.9
  - target: '[[文档布局检测]]'
    type: implements
    confidence: 0.85
supersedes: null
---

# YOLO

## 概述

YOLO（You Only Look Once）是一类 One-Stage 目标检测框架，一次前向推理即可得到所有目标的类别和边界框，速度显著快于两阶段检测器（如 [[R-CNN 系列|Faster R-CNN]]）。

## 关键内容

### 标准架构

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

### One-Stage vs Two-Stage

| 特性 | One-Stage (YOLO) | Two-Stage ([[R-CNN 系列|Faster R-CNN]]) |
|------|------------------|--------------------------|
| 推理速度 | 快 | 慢 |
| 精度 | 略低 | 略高 |
| 适用场景 | 实时检测、大规模部署 | 高精度要求场景 |

### Anchor 机制

YOLO 使用预定义的 Anchor box 尺寸来匹配不同大小的目标。标准 YOLO 的 Anchor 为自然场景优化，在文档场景需要重新聚类 bbox 尺寸分布来生成专用 Anchor。

### NMS（非极大值抑制）

后处理关键步骤：去除重叠度高的冗余检测框。IoU 阈值的选择直接影响检测结果——过高保留重复框，过低误删正确框。

### 在文档布局中的应用

[[DocLayout-YOLO]] 是 YOLO 针对[[文档布局检测]]的专门变体，解决了四大挑战：极端长宽比、密集重叠、小目标、无纹理区域。

## 来源

- [[raw/assets/MinerU/minerU_03_layout.md]] — MinerU 深度解析系列 · 第三篇：布局检测系统

## 相关

- [[DocLayout-YOLO]] — YOLO 的文档布局专用变体
- [[文档布局检测]] — YOLO 在文档领域的应用场景
