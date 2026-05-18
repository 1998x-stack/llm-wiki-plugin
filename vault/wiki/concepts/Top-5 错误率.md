---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [计算机视觉, 评估指标, ImageNet, AI工程]
aliases: ["Top-5 Error Rate", "Top-5 错误率", "Top-5 Accuracy"]
relates_to: ["AlexNet", "ImageNet", "ILSVRC", "深度学习（Deep Learning）"]
supersedes: null
---

# Top-5 错误率

## 概述
Top-5 错误率是图像分类任务的评估指标，指模型预测的前 5 个最高概率类别中不包含正确答案的比例，[[ILSVRC]] 竞赛采用此指标以应对细粒度分类的歧义性。

## 关键内容

1. **定义**：对于一张输入图像，模型输出 1000 个类别的概率分布。如果正确答案不在模型预测概率最高的前 5 个类别中，则计为一次错误。Top-5 错误率 = 错误次数 / 总测试次数。
2. **为什么用 Top-5**：[[ImageNet]] 的 1000 个类别中包含许多细粒度亚类（如 120 种犬科亚种），人类[[标注]]者也可能存在歧义。Top-5 指标允许模型有一定的"合理猜测"空间，比 Top-1 更宽容。
3. **[[AlexNet]] 的成绩**：[[AlexNet]] 在 2012 年 [[ILSVRC]] 中达到 Top-5 错误率 16.4%（Top-1 约 37.5%），比 2011 年冠军的 25.8% 降低了 9.4 个百分点。这是[[计算]]机视觉历史上最大的单年进步幅度。
4. **后续发展**：此后 Top-5 错误率持续下降——[[VGGNet]]（2014）约 7.3%，[[残差网络（ResNet）]]（2015）降至 3.57%，超越人类水平（约 5.1%）。Top-5 错误率已成为衡量图像分类模型性能的标准指标之一。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — evaluated_on
- [[ImageNet]] — metric_for
- [[ILSVRC]] — competition_metric
- [[深度学习（Deep Learning）]] — improved_by
