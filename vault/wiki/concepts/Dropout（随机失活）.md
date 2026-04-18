---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "正则化"]
aliases: ["Dropout", "随机失活", "随机丢弃", "Dropout Regularization"]
relates_to: ["过拟合（Overfitting）", "集成学习（Ensemble Learning）", "正则化（Regularization）", "Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)", "Geoffrey E. Hinton", "Nitish Srivastava", "AlexNet", "MC Dropout（蒙特卡洛 Dropout）", "Inverted Dropout", "DropConnect", "Spatial Dropout", "DropPath（Stochastic Depth）"]
supersedes: null
---

# Dropout（随机失活）

## 概述 (50-200字符)
[[Dropout]] 是一种神经网络正则化技术，训练时以概率 p 随机将神经元输出置零，迫使每个神经元学习更鲁棒、独立的特征表示，有效防止[[过拟合（Overfitting）]]，由[[Geoffrey E. Hinton]]团队于 2014 年正式提出。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心机制**：训练时每个神经元以概率 p（通常 0.5）被随机置零，即 `h = ReLU(W·x + b) ⊙ mask`，其中 `mask ~ Bernoulli(1-p)`。测试时所有神经元开启，权重乘以保留概率 (1-p) 以保证[[期望值]]不变。现代实现采用 **[[Inverted Dropout]]**：训练时直接除以 (1-p)，测试时无需任何调整，只需切换 `model.eval()` 即可。
2. **[[模型融合|集成学习]]视角**：[[Dropout]] 等价于同时训练指数级数量（2^N）的子网络并做集成。每次前向传播随机生成一个"薄"子网络，所有子网络共享参数但只有参与的子集被更新。测试时的权重缩放近似于对所有子网络取几何平均，这是 [[Dropout]] 强大泛化能力的理论基础。
3. **减少共适应（Co-adaptation）**：没有 [[Dropout]] 时，神经元会相互依赖来修正错误（"共谋"），导致单个神经元无法独立工作。[[Dropout]] 强制每个神经元学习更鲁棒、更独立的特征——"你不能依赖你的邻居，因为它随时可能消失"。[[Geoffrey E. Hinton]]用有性生殖作类比：基因随机混合比完全复制更能防止"寄生基因"传播。
4. **变体与应用场景**：**[[Spatial Dropout]]** 随机置零整个特征图通道（适用于 CNN）；**[[DropConnect]]** 随机置零权重而非神经元；**[[MC Dropout（蒙特卡洛 Dropout）]]** 测试时保持 [[Dropout]] 开启以估计预测不确定性（Gal & Ghahramani 2016 证明等价于[[托马斯·贝叶斯|贝叶斯]]近似推断）；**[[DropPath（Stochastic Depth）]]** 随机跳过整个残差块（[[残差网络（ResNet）|ResNet]]、ViT）；**Attention [[Dropout]]** 对注意力权重做 [[Dropout]]（[[Transformer 架构|Transformer]]）。尽管[[Batch Normalization]]在卷积网络中承担了部分正则化作用，[[Dropout]] 在全连接层、[[Transformer 架构|Transformer]]、[[强化学习]]、[[托马斯·贝叶斯|贝叶斯]]估计和小数据集场景中仍不可替代。

## 来源
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. JMLR, 15(1), 1929–1958.] — 原始论文
- [raw/articles/ai-papers/machine-learning/09_dropout_2014.md] — 源文件

## 相关
- [[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]] — described_in
- [[Geoffrey E. Hinton]] — invented_by
- [[Nitish Srivastava]] — first_author
- [[过拟合（Overfitting）]] — prevents
- [[集成学习（Ensemble Learning）]] — interpreted_as
- [[AlexNet]] — used_in
- [[Inverted Dropout]] — variant
- [[MC Dropout（蒙特卡洛 Dropout）]] — variant
- [[DropConnect]] — variant
- [[Spatial Dropout]] — variant
- [[DropPath（Stochastic Depth）]] — variant
