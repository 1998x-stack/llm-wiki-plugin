---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "计算机视觉", "卷积神经网络"]
aliases: ["AlexNet", "Alex Krizhevsky Network"]
relates_to: ["卷积神经网络（CNN）", "ReLU激活函数", "Dropout（随机失活）", "数据增强（Data Augmentation）", "局部响应归一化（LRN）", "ImageNet", "Geoffrey E. Hinton", "ImageNet Classification with Deep Convolutional Neural Networks (2012 论文)"]
supersedes: null
---

# AlexNet

## 概述 (50-200字符)
AlexNet 是 [[Alex Krizhevsky]] 于 2012 年提出的深度[[卷积神经网络（CNN）|卷积神经网络]]，在 [[ImageNet]] 竞赛中将 Top-5 错误率从 25.8% 降至 15.3%，标志着深度学习时代的正式开启。

## 关键内容 (≥300字符, 用[[双链]])
1. **架构设计**：8 层网络（5 层卷积 + 3 层全连接），输入 224×224×3 RGB 图像，总参数量约 6200 万。Conv1 使用 96 个 11×11 大卷积核（stride=4）捕获低级特征，后续层逐步使用 5×5 和 3×3 小卷积核叠加感受野。FC6/FC7 各 4096 神经元，FC8 为 1000 类输出。
2. **五大技术创新**：(1) [[ReLU激活函数]]替代 Sigmoid，训练速度快 6 倍且解决[[梯度消失]]；(2) 双 GPU 并行训练（GTX 580），将训练时间从数月缩短至 5-6 天；(3) [[Dropout（随机失活）]]（p=0.5）正则化，防止[[过拟合（Overfitting）|过拟合]]；(4) [[数据增强（Data Augmentation）]]（随机裁剪、水平翻转、PCA 色彩扰动），将 120 万样本等效扩展至数十亿；(5) [[局部响应归一化（LRN）]]，受神经科学"侧抑制"启发。
3. **历史影响**：2012 年 ILSRC 竞赛中领先第二名 10 个百分点，是跨越式突破而非渐进式改进。此后深度学习彻底取代手工特征+SVM 的传统 CV [[规范化理论|范式]]，催生了 VGGNet（2014）、Goog[[卷积神经网络（CNN）|LeNet]]（2014）、[[ResNet]]（2015）等后续架构，并直接引爆 AI 产业投资浪潮——NVIDIA GPU 从游戏显卡变为 AI 芯片，[[Google]] 收购 [[DeepMind]]，自动驾驶、医疗影像等商业应用爆发。
4. **演化路径**：AlexNet → VGGNet（更深、全 3×3）→ Goog[[卷积神经网络（CNN）|LeNet]]（Inception 模块）→ [[残差网络（ResNet）|ResNet]]（[[残差连接]]、152 层）→ DenseNet（密集连接）→ EfficientNet（复合缩放）→ ViT（[[Transformer 架构|Transformer]] 取代 CNN）。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — 原始论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件

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
