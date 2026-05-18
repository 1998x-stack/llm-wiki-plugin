---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, computer-vision, object-detection, 机器学习]
aliases: [Ren et al. 2015, Faster R-CNN 论文]
relates_to:
  - target: Shaoqing Ren
    relation: authored_by
  - target: Faster R-CNN
    relation: introduced
  - target: R-CNN 系列
    relation: extends
supersedes: null
---

# Faster R-CNN: Towards Real-Time Object Detection with Region Proposals (2015 论文)

## 概述
提出 [[R-CNN 系列|Faster R-CNN]] 的论文，通过区域提议网络（RPN）实现端到端的目标检测。

## 关键内容

1. **区域提议网络（RPN）**：用神经网络替代传统的选择性搜索，将区域提议与目标检测统一到单个网络中。
2. **两阶段检测**：第一阶段 RPN 生成候选区域，第二阶段进行分类和边界框回归，精度高于单阶段方法。
3. **与 YOLO 对比**：[[R-CNN 系列|Faster R-CNN]] 精度高但速度慢，与 [[YOLO]] 的单阶段实时检测形成互补路线。

## 来源
- [[ai_papers_timeline.md]] — 2015 年时间线条目

## 相关
- [[Shaoqing Ren]] — authored_by
- [[Faster R-CNN]] — introduced
- [[R-CNN 系列]] — extends
- [[YOLO]] — compares_to
