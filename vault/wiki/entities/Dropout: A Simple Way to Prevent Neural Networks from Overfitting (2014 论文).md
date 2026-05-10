---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["论文", "机器学习", "深度学习", "正则化"]
aliases: ["Dropout 2014 论文", "Dropout: A Simple Way to Prevent Neural Networks from Overfitting", "Dropout JMLR 论文"]
relates_to:
  - target: "[[Nitish Srivastava]]"
    type: "first_author"
  - target: "[[Geoffrey E. Hinton]]"
    type: "co_author"
  - target: "[[Alex Krizhevsky]]"
    type: "co_author"
  - target: "[[Ilya Sutskever]]"
    type: "co_author"
  - target: "[[Ruslan Salakhutdinov]]"
    type: "co_author"
  - target: "[[Dropout]]"
    type: "introduces"
  - target: "[[AlexNet]]"
    type: "demonstrates_on"
  - target: "[[过拟合]]"
    type: "addresses"
  - target: "[[集成学习（Ensemble Learning）]]"
    type: "theoretical_basis"
  - target: "[[共适应]]"
    type: "addresses"
  - target: "[[MC Dropout]]"
    type: "related_to"
  - target: "[[Inverted Dropout]]"
    type: "related_to"
  - target: "[[DropConnect]]"
    type: "related_to"
  - target: "[[Spatial Dropout]]"
    type: "related_to"
  - target: "[[Stochastic Depth]]"
    type: "related_to"
  - target: "[[DropPath]]"
    type: "related_to"
supersedes: null
---

# Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)

## 概述 (50-200字符)
[[Nitish Srivastava]]、[[Geoffrey E. Hinton]]等人于 2014 年发表在 JMLR 的里程碑论文，正式提出[[Dropout]]正则化方法。论文以极简方案解决了深度神经网络的[[过拟合]]危机，提供数学形式化和多种理论解释，成为深度学习标配技术之一。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题背景与动机**：深度神经网络拥有数百万参数，极易"死记硬背"训练数据导致[[过拟合]]。传统正则化方法（L1/[[权重衰减（Weight Decay）|L2 正则化]]、Early Stopping）对深度网络效果有限。论文提出了一个出人意料的简单方案：训练时随机"杀死"一些神经元，模拟生物神经系统的随机性机制。
2. **核心贡献与机制**：正式定义 [[Dropout]] 机制——训练时每个神经元以概率 p（通常 0.5）被随机置零，测试时所有神经元开启并乘以保留概率 (1-p)。现代实现常采用[[Inverted Dropout]]以简化测试流程。论文提供了三种理论解释：(a) [[集成学习（Ensemble Learning）]]视角：等价于 2^N 种子网络的几何平均集成；(b) 减少[[共适应]]：迫使每个神经元学习独立鲁棒的特征；(c) [[托马斯·贝叶斯|贝叶斯]]近似：可解释为对权重的变分[[托马斯·贝叶斯|贝叶斯]]近似。
3. **数学形式化与实现**：论文给出了完整的数学表述：$\tilde{r}_j^{(l)} \sim \text{Bernoulli}(1-p)$，$\tilde{y}^{(l)} = \tilde{r}^{(l)} \odot y^{(l)}$。详细介绍了在各种网络架构（全连接层、CNN、RNN/LSTM）中的应用方式，并给出了推荐的丢弃率（全连接层 0.5，卷积层 0.1-0.3）。论文还提到了 [[Inverted Dropout]] 的实现优化策略。
4. **实验验证与历史影响**：论文在多个基准数据集上验证了 [[Dropout]] 的有效性，包括 [[MNIST]]、[[CIFAR-10]]、[[ImageNet]] 图像分类、TIMIT 语音识别、Reuters 文本分类和 HIV 药物发现。在 [[MNIST]] 上 [[Dropout]] 将测试错误率从 1.60% 降至 1.25%，在 [[CIFAR-10]] 上从 16.6% 降至 12.6%，在 [[ImageNet]] 上（在 [[AlexNet]] 中）降低了约 2% 的 Top-1 错误率。论文至 2024 年被引用超过 5 万次，后续衍生出 MC [[Dropout]]、[[DropConnect]]、[[Spatial Dropout]]、[[Stochastic Depth]]、[[DropPath]] 等多种变体。此外，论文还催生了 [[MC Dropout|Monte Carlo Dropout]]，可用于估计预测不确定性。

## 来源
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). JMLR, 15(1), 1929–1958.] — 原始论文
- [raw/articles/ai-papers/machine-learning/09_dropout_2014.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_10_dropout.md] — 精读源文件

## 相关
- [[Nitish Srivastava]] — first_author
- [[Geoffrey E. Hinton]] — co_author
- [[Alex Krizhevsky]] — co_author
- [[Ilya Sutskever]] — co_author
- [[Ruslan Salakhutdinov]] — co_author
- [[Dropout]] — introduces
- [[AlexNet]] — demonstrates_on
- [[过拟合]] — addresses
- [[共适应]] — addresses
- [[集成学习（Ensemble Learning）]] — theoretical_basis
- [[MC Dropout]] — related_to
- [[Inverted Dropout]] — related_to
- [[DropConnect]] — related_to
- [[Spatial Dropout]] — related_to
- [[Stochastic Depth]] — related_to
- [[DropPath]] — related_to