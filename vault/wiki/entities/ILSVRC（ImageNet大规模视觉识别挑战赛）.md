---
type: entity
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [竞赛, 计算机视觉, ImageNet, 深度学习, 机器学习]
aliases: ["ILSVRC", "ImageNet Large Scale Visual Recognition Challenge", "ImageNet 竞赛"]
relates_to: ["ImageNet", "ImageNet: A Large-Scale Hierarchical Image Database (2009 论文)", "AlexNet", "李飞飞", "Jia Deng", "计算机视觉", "ZFNet（2013 论文）", "VGGNet", "GoogLeNet: Inception", "残差网络（ResNet）", "Top-5 错误率"]
supersedes: null
---

# ILSVRC（ImageNet大规模视觉识别挑战赛）

## 概述
[[ILSVRC]] 是 2010-2017 年举办的年度[[计算]]机视觉竞赛，基于 [[ImageNet]] 数据集，2012 年 [[AlexNet]] 以 16.4% [[Top-5 错误率]]夺冠，标志着深度学习时代的开启。

## 关键内容

1. **竞赛[[Settings|设置]]**：2010 年由 [[李飞飞]] 团队发起，使用 [[ImageNet]] 数据集的子集：120 万张训练图像、5 万张验证图像、10 万张测试图像，共 1000 个类别。任务为图像分类，评估指标为 Top-1 和 [[Top-5 错误率]]。
2. **历年成绩**：2010 年冠军（[[NEC-UIUC]]，传统方法）[[Top-5 错误率]] 28.2%；2011 年冠军（Xavier，传统方法）25.8%；2012 年 [[AlexNet]] 以 16.4% 夺冠，领先第二名（ISI，传统方法）26.2% 达 9.8 个百分点——这是降维打击式的跨越，而非渐进式改进。2013 年 [[ZFNet]] 再获冠军，[[Top-5 错误率]]进一步降至 11.7%。
3. **历史影响**：[[AlexNet]] 的胜利彻底终结了"[[手工特征工程]]"时代（SIFT、HOG、[[Haar 小波]]等传统方法），宣告深度学习革命正式开始。此后 [[ILSVRC]] 成为深度学习架构的竞技场——[[VGGNet]]（2014）、[[Inception Network|GoogLeNet]]（2014）、[[残差网络（ResNet）|ResNet]]（2015）相继刷新纪录，2015 年 [[残差网络（ResNet）|ResNet]] 首次超越人类[[标注]]者水平。
4. **竞赛终止**：[[ILSVRC]] 于 2017 年举办最后一届，因为分类准确率已接近饱和（[[Top-5 错误率]]低于 3%），研究焦点转向目标检测、分割等更复杂的视觉任务。

## 来源
- [raw/articles/ai-papers/ai-papers/foundations/paper_03_alexnet.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[ImageNet]] — dataset
- [[李飞飞]] — founded_by
- [[Jia Deng]] — organizer
- [[AlexNet]] — 2012_winner
- [[ZFNet（2013 论文）]] — 2013_winner
- [[VGGNet]] — 2014_participant
- [[GoogLeNet: Inception]] — 2014_winner
- [[残差网络（ResNet）]] — 2015_winner
- [[计算机视觉]] — research_field
- [[Top-5 错误率]] — evaluation_metric
