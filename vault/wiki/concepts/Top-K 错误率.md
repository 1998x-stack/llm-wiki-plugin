---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ImageNet, 评估指标, 分类精度, 竞赛, AI工程]
aliases: [Top-5 Error Rate, Top-1 Error Rate, ImageNet 错误率]
relates_to: [ImageNet, AlexNet, VGGNet, 残差网络（ResNet）]
supersedes: null
---

# Top-K 错误率

## 概述
[[ImageNet]] 竞赛中使用的分类评估指标，衡量模型预测中前 K 个最可能类别是否包含正确答案。

## 关键内容

1. **Top-1 错误率**：模型预测的最高概率类别是否正确。这是最严格的评估标准，直接反映模型的精确分类能力。
2. **[[Top-5 错误率]]**：模型预测的前 5 个最高概率类别中是否包含正确类别。由于 [[ImageNet]] 的 1000 个类别中存在视觉相似类别，[[Top-5 错误率]]更能反映模型的实用价值。
3. **历史里程碑**：[[AlexNet]]（2012）将 [[Top-5 错误率]]从 26.2% 降至 15.3%；[[VGGNet]]（2014）降至 7.3%；[[残差网络（ResNet）|ResNet]]（2015）首次超越人类水平（3.57% vs 人类约 5.1%）。

Top-K 错误率是衡量图像分类模型性能的标准指标，尤其在细粒度分类任务中比 Top-1 更具参考价值。

## 来源
- [[ImageNet]] — ILSVRC 竞赛官方评估指标

## 相关
- [[ImageNet]] — used_by
- [[AlexNet]] — evaluated_by
- [[VGGNet]] — evaluated_by
- [[残差网络（ResNet）]] — evaluated_by
