---
type: concept
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [computer-vision, object-detection, architecture]
aliases: [R-CNN, Fast R-CNN, Faster R-CNN, R-CNN 系列]
relates_to:
  - target: Ross Girshick
    relation: relates_to
  - target: Shaoqing Ren
    relation: relates_to
  - target: YOLO
    relation: compares_to
supersedes: null
---

# R-CNN 系列

## 概述
基于区域提议的两阶段目标检测[[算法]]系列，包括 R-CNN、Fast R-CNN 和 Faster R-CNN。

## 关键内容

1. **[[两阶段推荐架构|两阶段范式]]**：第一阶段生成候选区域，第二阶段进行分类和边界框回归。
2. **RPN 创新**：Faster R-CNN 引入区域提议网络（RPN），用神经网络替代选择性搜索。
3. **与 YOLO 对比**：R-CNN 系列精度高但速度慢，与 [[YOLO]] 的单阶段实时检测形成互补。

## 来源
- [[ai_papers_timeline.md]] — 2015 年时间线条目

## 相关
- [[Ross Girshick]] — relates_to
- [[Shaoqing Ren]] — relates_to
- [[YOLO]] — compares_to
