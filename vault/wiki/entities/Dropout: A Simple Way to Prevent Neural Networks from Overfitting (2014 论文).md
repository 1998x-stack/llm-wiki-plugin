---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["论文", "机器学习", "深度学习", "正则化"]
aliases: ["Dropout 2014 论文", "Dropout: A Simple Way to Prevent Neural Networks from Overfitting", "Dropout JMLR 论文"]
relates_to: ["Nitish Srivastava", "Geoffrey E. Hinton", "Alex Krizhevsky", "Ilya Sutskever", "Ruslan Salakhutdinov", "Dropout（随机失活）", "AlexNet", "集成学习（Ensemble Learning）", "过拟合（Overfitting）"]
supersedes: null
---

# Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)

## 概述 (50-200字符)
[[Nitish Srivastava]]、[[Geoffrey E. Hinton]]等人于 2014 年发表在 JMLR 的里程碑论文，正式提出[[Dropout（随机失活）]]正则化方法。论文以极简方案解决了深度神经网络的[[过拟合（Overfitting）|过拟合]]危机，成为深度学习标配技术之一。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题背景**：深度神经网络拥有数百万参数，极易"死记硬背"训练数据导致[[过拟合（Overfitting）]]。传统正则化方法（L1/L2 正则化、Early Stopping）对深度网络效果有限。论文提出了一个出人意料的简单方案：训练时随机"杀死"一些神经元。
2. **核心贡献**：正式定义 [[Dropout]] 机制——训练时每个神经元以概率 p（通常 0.5）被随机置零，测试时所有神经元开启并乘以保留概率 (1-p)。论文提供了三种解释：(a) [[模型融合|集成学习]]视角：等价于 2^N 种子网络的几何平均集成；(b) 减少共适应：迫使每个神经元学习独立鲁棒的特征；(c) 类比有性生殖：防止少数神经元过度特化主导网络。
3. **实验验证**：论文在多个基准数据集上验证了 [[Dropout]] 的有效性，包括 [[ImageNet]] 图像分类、TIMIT 语音识别、Reuters 文本分类和 HIV 药物发现。在 [[ImageNet]] 上，[[Dropout]] 是[[AlexNet]]成功的关键因素之一——[[Alex Krizhevsky]]在全连接层使用 p=0.5 的 [[Dropout]]，将测试误差显著降低。
4. **历史影响**：论文至 2024 年被引用超过 5 万次，是深度学习领域引用率最高的论文之一。[[Dropout]] 至今仍是全连接层、[[Transformer 架构|Transformer]]、[[强化学习]]等场景的正则化标配。后续衍生出 MC [[Dropout]]（[[托马斯·贝叶斯|贝叶斯]]近似）、DropConnect、Spatial [[Dropout]]、DropPath 等多种变体，形成了完整的正则化技术族。

## 来源
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). JMLR, 15(1), 1929–1958.] — 原始论文
- [raw/articles/ai-papers/machine-learning/09_dropout_2014.md] — 源文件

## 相关
- [[Nitish Srivastava]] — first_author
- [[Geoffrey E. Hinton]] — co_author
- [[Alex Krizhevsky]] — co_author
- [[Ilya Sutskever]] — co_author
- [[Ruslan Salakhutdinov]] — co_author
- [[Dropout（随机失活）]] — introduced
- [[AlexNet]] — demonstrated_on
- [[过拟合（Overfitting）]] — addresses
- [[集成学习（Ensemble Learning）]] — theoretical_basis
