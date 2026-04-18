---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "正则化", "神经网络"]
aliases: ["Dropout", "随机失活", "Dropout 正则化"]
relates_to: ["AlexNet", "过拟合", "Geoffrey E. Hinton", "深度学习"]
supersedes: null
---

# Dropout

## 概述 (50-200字符)
Dropout 是一种神经网络正则化技术，训练时以概率 p 随机关闭神经元，防止[[过拟合（Overfitting）|过拟合]]。2012 年 [[AlexNet]] 使用 p=0.5 显著降低验证集错误率，成为深度学习标准组件。

## 关键内容 (≥300字符, 用[[双链]])
1. **机制**：训练阶段，每个神经元以概率 p（通常 0.5）被随机"关闭"（输出置零）。这强迫网络学习冗余、独立的特征表示，而不是依赖特定神经元的协同作用。相当于同时训练 2^N 个共享参数的子网络，是一种高效的模型集成方法。
2. **测试时补偿**：推理阶段所有神经元保持开启，但权重乘以 (1-p) 进行缩放。这是对训练时所有子网络的近似平均——如果训练时 50% 神经元被丢弃，测试时每个神经元的输出期望减半，因此需要补偿。
3. **在 [[AlexNet]] 中的应用**：[[AlexNet]]在 FC6 和 FC7 两个全连接层（各 4096 神经元）使用 Dropout(p=0.5)，显著降低了验证集错误率。全连接层参数量大（占网络总参数大部分），是[[过拟合（Overfitting）|过拟合]]的高发区域，Dropout 在此处效果最明显。
4. **理论解释与变体**：Dropout 可理解为一种[[托马斯·贝叶斯|贝叶斯]]近似推断，或一种自适应的正则化方法。后续衍生出 DropConnect（[[Dropout（随机失活）|随机丢弃]]权重而非激活）、Spatial Dropout（丢弃整个特征图）、Variational Dropout 等变体。[[Geoffrey E. Hinton]]是 Dropout 的主要提出者之一。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — AlexNet 论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件

## 相关
- [[AlexNet]] — used_in
- [[Geoffrey E. Hinton]] — invented_by
- [[过拟合]] — prevents
- [[Batch Normalization]] — alternative_to
- [[深度学习]] — standard_technique
