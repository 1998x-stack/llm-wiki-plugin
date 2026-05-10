---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["机器学习", "深度学习", "正则化", "神经网络"]
aliases: ["Dropout", "随机失活", "Dropout 正则化", "Dropout regularization"]
relates_to:
  - target: "[[AlexNet]]"
    type: "used_in"
  - target: "[[Geoffrey E. Hinton]]"
    type: "invented_by"
  - target: "[[过拟合]]"
    type: "prevents"
  - target: "[[Batch Normalization]]"
    type: "alternative_to"
  - target: "[[深度学习]]"
    type: "standard_technique"
  - target: "[[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]]"
    type: "described_in"
  - target: "[[MC Dropout]]"
    type: "has_variant"
  - target: "[[Inverted Dropout]]"
    type: "has_variant"
  - target: "[[集成学习（Ensemble Learning）]]"
    type: "theoretical_basis"
  - target: "[[共适应]]"
    type: "addresses"
supersedes: null
---

# Dropout

## 概述 (50-200字符)
Dropout 是一种神经网络正则化技术，训练时以概率 p 随机关闭神经元，防止[[过拟合]]。2012 年 [[AlexNet]] 使用 p=0.5 显著降低验证集错误率，成为深度学习标准组件。2014年[[Nitish Srivastava]]等人在JMLR论文中正式提出该方法并提供了理论基础。

## 关键内容 (≥300字符, 用[[双链]])
1. **机制与实现**：训练阶段，每个神经元以概率 p（通常 0.5）被随机"关闭"（输出置零）。这强迫网络学习冗余、独立的特征表示，而不是依赖特定神经元的协同作用。现代实现常采用 [[Inverted Dropout]]：训练时进行缩放以避免测试时修改权重。相当于同时训练 2^N 个共享参数的子网络，是一种高效的模型集成方法。
2. **数学形式化**：训练时前向传播中的 Dropout 可形式化为：$\tilde{r}_j^{(l)} \sim \text{Bernoulli}(1-p)$，$\tilde{y}^{(l)} = \tilde{r}^{(l)} \odot y^{(l)}$。测试时权重乘以 $(1-p)$ 进行期望补偿：$w_{test} = w_{train} \times (1 - p)$。
3. **理论解释**：Dropout 的有效性可从三个角度理解：(a) 隐式[[集成学习（Ensemble Learning）]]视角——训练 2^n 个子网络的几何平均；(b) 打破神经元[[共适应]]——强迫神经元独立有意义；(c) [[托马斯·贝叶斯|贝叶斯]]近似——可解释为对权重的变分[[托马斯·贝叶斯|贝叶斯]]近似。
4. **应用与最佳实践**：通常在全连接层使用 0.5 丢弃率，在卷积层使用 0.1-0.3 丢弃率，输出层一般不用。需注意测试时切换 model.eval() 模式。[[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]] 中详细验证了其在 MNIST、[[CIFAR-10 数据集|CIFAR-10]]、[[ImageNet]] 等多个基准上的有效性。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — AlexNet 论文
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). JMLR, 15(1), 1929–1958.] — Dropout 论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — AlexNet 源文件
- [raw/articles/ai-papers/foundations/paper_10_dropout.md] — Dropout 精读源文件

## 相关
- [[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]] — described_in
- [[Geoffrey E. Hinton]] — invented_by
- [[过拟合]] — prevents
- [[集成学习（Ensemble Learning）]] — theoretical_basis
- [[共适应]] — addresses
- [[MC Dropout]] — variant
- [[Inverted Dropout]] — variant
- [[DropConnect]] — variant
- [[Spatial Dropout]] — variant
