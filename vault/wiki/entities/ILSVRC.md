---
type: project
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [竞赛, 计算机视觉, 深度学习, 数据集, 机器学习]
aliases: ["ILSVRC", "ImageNet Large Scale Visual Recognition Challenge", "ImageNet 竞赛"]
relates_to: ["ImageNet", "李飞飞", "AlexNet", "深度学习", "斯坦福大学"]
supersedes: null
---

# ILSVRC

## 概述
ILSVRC（[[ImageNet]] 大规模视觉识别挑战赛）是 2010-2017 年间举办的年度[[计算]]机视觉竞赛，[[AlexNet]] 在 2012 年的压倒性胜利标志着深度学习时代的到来。

## 关键内容

1. **竞赛[[Settings|设置]]**：由[[斯坦福大学]][[李飞飞]]团队发起，基于 [[ImageNet]] 数据集。任务是从 1000 个类别中识别给定图片的正确类别。训练集包含 120 万张图像，测试集约 15 万张。
2. **历史成绩**：
   - 2010：[[NEC-UIUC]]（传统方法），[[Top-5 错误率]] 28.2%
   - 2011：Xavier（传统方法），[[Top-5 错误率]] 25.8%
   - **2012**：**[[AlexNet]]（深度学习）**，**[[Top-5 错误率]] 16.4%**
   - 2012（亚军）：ISI（传统方法），[[Top-5 错误率]] 26.2%
   - 2015：[[残差网络（ResNet）|ResNet]]，[[Top-5 错误率]] 3.57%（超越人类水平）
3. **历史意义**：2012年 [[AlexNet]] 比第二名低 9.8 个百分点，这不是渐进式改进而是降维打击。此后所有参赛队伍都转向深度学习方法，传统[[特征工程（Feature Engineering）|手工特征]]+SVM 的方案被彻底淘汰。
4. **竞赛终止**：2017年后 ILSVRC 正式结束，因为图像分类任务已被"解决"——深度模型的准确率已超过人类水平。竞赛推动了整个[[计算]]机视觉领域从传统方法向深度学习的[[规范化理论|范式]]转移。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读
- [raw/articles/ai-papers/foundations/paper_05_resnet.md] — ResNet 论文精读，ILSVRC 2015 成绩

## 相关
- [[ImageNet]] — based_on
- [[李飞飞]] — created_by
- [[AlexNet]] — winner_2012
- [[深度学习]] — paradigm_shift
- [[斯坦福大学]] — organized_by
- [[VGGNet]] — participant
- [[GoogLeNet: Inception]] — participant
