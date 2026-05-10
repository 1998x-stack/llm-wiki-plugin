---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "神经网络"]
aliases: ["MLP", "Multi-Layer Perceptron", "多层感知器", "前馈神经网络"]
relates_to:
  - target: "[[感知机（Perceptron）]]"
    type: extends
    confidence: 1.0
  - target: "[[XOR 问题]]"
    type: supersedes
    confidence: 0.9
  - target: "[[反向传播（Backpropagation）]]"
    type: implements
    confidence: 0.9
  - target: "[[AI 寒冬]]"
    type: supersedes
    confidence: 0.7
  - target: "[[Transformer架构]]"
    type: extends
    confidence: 0.6
supersedes: null
---

# 多层感知机（MLP）

## 概述
[[多层感知机]]（Multi-Layer [[感知机（Perceptron）|Perceptron]], MLP）在单层[[感知机]]基础上添加一个或多个隐藏层并引入非线性激活函数，能够学习任意非线性[[决策边界]]，解决了 XOR 等线性不可分问题。

## 关键内容

1. **结构演进**：从单层[[感知机]]（输入→输出）到[[多层感知机]]（输入→隐藏层→输出），每个隐藏层包含多个神经元，层与层之间全连接。关键改进是引入非线性激活函数（sigmoid、tanh、ReLU 等），替代[[感知机]]的 sign 函数。

2. **解决 [[XOR 问题]]**：单层[[感知机]]无法用一条直线分开 XOR 的四类样本。MLP 通过隐藏层将输入映射到新的特征空间，在该空间中样本变为线性可分，从而解决了这一经典难题。

3. **训练方法**：MLP 的训练依赖[[反向传播（Backpropagation）]][[算法]]——通过[[链式法则]]将输出误差逆向传播到每个隐藏层神经元，实现梯度下降优化。这解决了困扰 AI 领域十余年的"信用[[点数问题|分配问题]]"。

4. **历史地位**：MLP 是结束[[AI 寒冬]]的关键技术之一。1980 年代 MLP + [[反向传播]]的组合重新点燃了神经网络研究的热情，为后续深度神经网络的发展奠定了基础。

5. **现代演化**：MLP 是现代深度学习架构的基础组件。从 MLP 出发，加上卷积操作得到 CNN，加上[[注意力机制（Attention Mechanism）|注意力机制]]得到 [[Transformer 架构|Transformer]]，加上循环结构得到 RNN/LSTM。现代大模型（GPT、[[Claude_Code|Claude]]、BERT）的每个神经元本质上仍是[[感知机]]的变体。

## 来源
- [[01_perceptron_1958]] — 感知机原始论文解读

## 相关
- [[感知机（Perceptron）]] — extends
- [[XOR 问题]] — supersedes
- [[反向传播（Backpropagation）]] — implements
- [[AI 寒冬]] — supersedes
- [[Transformer架构]] — extends
