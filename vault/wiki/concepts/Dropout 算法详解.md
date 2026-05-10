---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["机器学习", "深度学习", "正则化", "数学形式化", "代码实现"]
aliases: ["Dropout 数学形式化", "Dropout 代码实现", "Dropout 算法详解"]
relates_to:
  - target: "[[Dropout]]"
    type: "elaborates"
  - target: "[[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]]"
    type: "elaborates"
  - target: "[[PyTorch]]"
    type: "implemented_in"
  - target: "[[神经网络]]"
    type: "applies_to"
supersedes: null
---

# Dropout 算法详解

## 概述 (50-200字符)
详细阐述 [[Dropout]] 的数学形式化表达、代码实现方式以及最佳实践。包含前向传播公式、[[Inverted Dropout]] 实现、以及在不同网络层中应用的具体细节。

## 关键内容 (≥300字符, 用[[双链]])
1. **数学形式化**：[[Dropout]] 在前向传播中的数学表达为：$\tilde{r}_j^{(l)} \sim \text{Bernoulli}(1-p)$，$\tilde{y}^{(l)} = \tilde{r}^{(l)} \odot y^{(l)}$，$z_i^{(l+1)} = \mathbf{w}_i^{(l+1)} \tilde{y}^{(l)} + b_i^{(l+1)}$，$y_i^{(l+1)} = f(z_i^{(l+1)})$。其中 $\odot$ 是元素级乘法，$\tilde{r}^{(l)}$ 是 0/1 掩码向量。训练时每个神经元以概率 $(1-p)$ 被保留，测试时全部开启但权重乘以 $(1-p)$ 补偿期望。
2. **[[Inverted Dropout]] 实现**：现代深度学习框架普遍采用 [[Inverted Dropout]]，即训练时直接缩放：`mask = (torch.rand(x.shape) > p).float()`，`x = x * mask / (1 - p)`。这样测试时无需修改权重，简化了推理过程。这种实现已成为标准方式。
3. **代码实现细节**：在 [[PyTorch]] 中，`nn.Dropout(p)` 会在训练时随机置零神经元并保持期望一致，推理时直接返回原输入。关键是要正确调用 `model.train()` 和 `model.eval()` 来切换模式。实现时需注意保留概率与丢弃概率的[[区分]]（[[PyTorch]] 中 p 指丢弃概率）。
4. **在不同层中的应用**：在全连接层通常使用 0.5 的丢弃率，在卷积层使用 0.1-0.3 的较低丢弃率（由于权重共享已有一定正则效果），在 LSTM/RNN 中用于非循环连接通常使用 0.2-0.5，[[Transformer 架构|Transformer]] 中通常使用 0.1。输出层一般不使用 [[Dropout]]。

## 来源
- [raw/articles/ai-papers/foundations/paper_10_dropout.md] — 精读源文件

## 相关
- [[Dropout]] — elaborates
- [[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]] — elaborates
- [[PyTorch]] — implemented_in
- [[神经网络]] — applies_to
- [[Inverted Dropout]] — variant
- [[MC Dropout]] — variant