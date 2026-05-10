---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, computer-vision, object-detection, yolo]
aliases: [Redmon et al. 2016]
relates_to:
  - target: Joseph Redmon
    relation: authored_by
  - target: YOLO
    relation: introduced
  - target: Faster R-CNN
    relation: compares_to
supersedes: null
---

# You Only Look Once: Unified, Real-Time Object Detection (2016 论文)

## 概述
提出 YOLO 目标检测[[算法]]的论文，将检测视为单一回归问题，实现端到端的实时检测。

## 关键内容

1. **单阶段检测**：YOLO 将图像划分为网格，每个网格预测边界框和类别概率，一次前向传播完成检测。
2. **实时性能**：相比 [[Faster R-CNN]] 等两阶段方法，YOLO 速度大幅提升，可实现 45 FPS 实时检测。
3. **全局理解**：YOLO 在预测时看到整个图像上下文，减少了 [[R-CNN 系列]] 的误报问题。

## 来源
- [[ai_papers_timeline.md]] — 2016 年时间线条目

## 相关
- [[Joseph Redmon]] — authored_by
- [[YOLO]] — introduced
- [[Faster R-CNN]] — compares_to
