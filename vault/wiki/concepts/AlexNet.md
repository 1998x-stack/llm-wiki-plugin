---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 3
tags: ["机器学习", "深度学习", "计算机视觉", "卷积神经网络"]
aliases: ["AlexNet", "Alex Krizhevsky Network"]
relates_to: ["卷积神经网络（CNN）", "ReLU激活函数", "Dropout（随机失活）", "数据增强（Data Augmentation）", "局部响应归一化（LRN）", "ImageNet", "Geoffrey E. Hinton", "ImageNet Classification with Deep Convolutional Neural Networks (2012 论文)", "ILSVRC（ImageNet大规模视觉识别挑战赛）", "迁移学习（Transfer Learning）", "特征工程（Feature Engineering）", "GPU训练", "稀疏激活", "侧抑制", "权重衰减（Weight Decay）", "卷积核可视化", "Top-5 错误率"]
supersedes: null
---

# AlexNet

## 概述 (50-200字符)
AlexNet 是 [[Alex Krizhevsky]] 于 2012 年提出的深度[[卷积神经网络（CNN）|卷积神经网络]]，在 [[ILSVRC]] 竞赛中以 16.4% [[Top-5 错误率]]夺冠，超越第二名 9.8 个百分点，标志着深度学习时代的正式开启。

## 关键内容 (≥300字符, 用双链)
1. **架构设计**：8 层网络（5 层卷积 + 3 层全连接），输入 224×224×3 RGB 图像，总参数量约 6200 万。Conv1 使用 96 个 11×11 大卷积核（stride=4）捕获低级特征，后续层逐步使用 5×5 和 3×3 [[3×3卷积核|小卷积核]]叠加[[感受野]]。FC6/FC7 各 4096 神经元，FC8 为 1000 类输出。架构具体为：输入(224×224×3) → Conv1(96个11×11卷积核,stride=4) → ReLU → LRN → MaxPool → Conv2(256个5×5卷积核) → ReLU → LRN → MaxPool → Conv3/4/5(384/384/256个[[3×3卷积核]]) → FC1/FC2/FC3(4096/4096/1000神经元) → [[Softmax]]。
2. **五大技术创新**：(1) [[ReLU激活函数]]替代 Sigmoid，训练速度快 6 倍且解决[[梯度消失]]；(2) 双 [[GPU训练|GPU 并行训练]]（GTX 580），将训练时间从数月缩短至 5-6 天；(3) [[Dropout（随机失活）]]（p=0.5）正则化，防止[[过拟合（Overfitting）|过拟合]]；(4) [[数据增强（Data Augmentation）]]（随机裁剪、水平翻转、PCA 色彩扰动），将 120 万样本等效扩展至数十亿；(5) [[局部响应归一化（LRN）]]，受神经科学"[[侧抑制]]"启发。
3. **竞赛结果**：2012 年 [[ILSVRC]] 竞赛中，AlexNet [[Top-5 错误率]] 16.4%，第二名（ISI，传统方法）26.2%，领先 9.8 个百分点。2010 年冠军 28.2%，2011 年 25.8%——AlexNet 是降维打击而非渐进式改进。这一胜利彻底终结了"[[手工特征工程]]"时代，宣告深度学习革命正式开始。
4. **产业涟漪效应**：AlexNet 发表后 6 个月内，[[Google]]、[[Facebook]]、[[百度]]纷纷建立深度学习研究团队。2013.03 [[Geoffrey E. Hinton|Hinton]] 公司 [[DNNresearch]] 以 4400 万美元被 [[Google]] 收购；[[DeepMind]] 被 [[Google]] 以 5 亿美元收购；2014 [[Facebook AI Research (FAIR)]] 成立；[[百度]] IDL 大规模扩张。
5. **可解释性**：研究者可视化了 AlexNet 第一层卷积核学到的特征——边缘检测器、颜色对比检测器、类似 Gabor 滤波器的纹理检测器。这些不是人工设计的，而是网络从数据中自动学到的，与人类视觉系统相似。深层特征越来越抽象：第 1 层边缘/颜色 → 第 2 层纹理/角点 → 第 3-4 层物体部件 → 第 5 层整体概念。
6. **关键超参数**：初始学习率 0.01（验证集停止改善时除以 10），[[Momentum（动量）]] 0.9，[[权重衰减（Weight Decay）]] 0.0005，Batch Size 128，训练 90 epochs 约 5-6 天。
7. **演化路径与影响**：AlexNet 发表后迅速催生了后续研究，包括 [[ZFNet]](2013)、[[VGGNet]](2014)、Goog[[卷积神经网络（CNN）|LeNet]](2014)、[[残差网络（ResNet）|ResNet]](2015)等。它不仅奠定了深度学习在[[计算]]机视觉中的主导地位，还开创了[[迁移学习]]的新时代——预训练的AlexNet特征被应用于医疗图像诊断、自动驾驶、工业检测等多个领域，成为深度学习时代的"通用特征提取器"。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — 原始论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读（新）

## 相关
- [[卷积神经网络（CNN）]] — implements
- [[ReLU激活函数]] — uses
- [[Dropout（随机失活）]] — uses
- [[数据增强（Data Augmentation）]] — uses
- [[局部响应归一化（LRN）]] — uses
- [[ImageNet]] — evaluated_on
- [[Geoffrey E. Hinton]] — advised_by
- [[ImageNet Classification with Deep Convolutional Neural Networks (2012 论文)]] — described_in
- [[LeNet-5]] — extends
- [[Batch Normalization]] — supersedes_lrn
- [[ILSVRC（ImageNet大规模视觉识别挑战赛）]] — won
- [[迁移学习（Transfer Learning）]] — enabled
- [[GPU训练]] — pioneered
- [[稀疏激活]] — produces
- [[侧抑制]] — inspired_lrn
- [[权重衰减（Weight Decay）]] — uses
- [[卷积核可视化]] — demonstrated
- [[Top-5 错误率]] — evaluated_by
- [[特征工程（Feature Engineering）]] — superseded
- [[DNNresearch]] — inspired
- [[ZFNet（2013 论文）]] — followed_by
