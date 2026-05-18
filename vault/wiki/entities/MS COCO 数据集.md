---
type: project
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [计算机视觉, 数据集, 目标检测, 深度学习]
aliases: ["MS COCO", "Microsoft COCO", "COCO", "Common Objects in Context"]
relates_to: ["ILSVRC", "残差网络（ResNet）", "目标检测"]
supersedes: null
---

# MS COCO 数据集

## 概述
微软发布的大规模目标检测、分割和字幕生成数据集，包含80个物体类别、超过33万张[[标注]]图像，是[[计算]]机视觉领域最全面的基准数据集之一。

## 关键内容
1. **数据集规模**：MS COCO 包含330,000+张图像，其中200,000+张带有[[标注]]，涵盖80个物体类别。每张图像平均包含多个物体实例，总计超过150万个物体实例。[[标注]]类型包括边界框、分割掩码、关键点（人体姿态）和图像字幕。
2. **与 [[ILSVRC]] 的区别**：[[ILSVRC]] 侧重单物体图像分类，每张图像主要包含一个目标物体；COCO 侧重多物体场景，每张图像包含多个物体及其空间关系，更贴近真实世界的视觉理解需求。
3. **[[残差网络（ResNet）|ResNet]] 在 COCO 上的表现**：在 COCO 2015 检测任务中，基于[[残差网络（ResNet）]]的方法获得第一名。[[残差网络（ResNet）|ResNet]] 的深层特征提取能力使其在复杂多物体场景下的检测精度显著优于前代方法。
4. **评估指标**：COCO 使用 mAP（mean Average Precision）作为核心指标，在多个 IoU 阈值（0.50-0.95）下[[计算]]，比单一阈值的评估更加严格。此外还有 AP@50、AP@75、AP-S/M/L（按物体尺寸分组）等细分指标。
5. **下游任务生态**：COCO 不仅用于目标检测，还推动了实例分割（Mask [[R-CNN 系列|R-CNN]]）、全景分割、图像字幕生成、视觉问答等多个研究方向的发展。

## 来源
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — 竞赛成绩部分，COCO 2015 检测第一

## 相关
- [[ILSVRC]] — compares_to（互补基准，多物体 vs 单物体）
- [[残差网络（ResNet）]] — compares_to（COCO 2015 冠军方法）
- [[ImageNet]] — compares_to
