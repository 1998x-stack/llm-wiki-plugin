---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [transformer, feed-forward, deep-learning, nlp]
aliases: ["FFN", "Position-wise Feed-Forward Networks", "Feed-Forward Network"]
relates_to:
  - target: "[[Attention Is All You Need]]"
    type: introduced_in
    confidence: 0.9
  - target: "[[Transformer]]"
    type: component_of
    confidence: 0.9
  - target: "[[Self-Attention]]"
    type: complement_to
    confidence: 0.8
  - target: "[[Multi-Layer Perceptron]]"
    type: specialization_of
    confidence: 0.85
supersedes: null
---

# Feed-Forward Network

## 概述
前馈网络（Feed-Forward Network, FFN）是[[Transformer架构]]中的关键组件，是一个位置无关的两层MLP（[[多层感知机]]）。它对每个位置的表示独立地进行相同的非线性变换，与[[注意力机制（Attention Mechanism）|注意力机制]]的跨位置信息聚合形成互补。

## 关键内容

1. **网络结构**：
   - 两层全连接网络：[[ReLU激活函数]]
   - 输入/输出维度：d_model = 512
   - 内部维度：d_ff = 2048（4倍扩展）
   - 公式：FFN(x) = max(0, xW₁ + b₁)W₂ + b₂

2. **功能分工**：
   - [[注意力机制（Attention Mechanism）|注意力机制]]：跨位置信息聚合（"哪些词相关？"）
   - FFN：逐位置特征变换（"这个词的特征如何处理？"）
   - 两者协同实现全局信息整合与局部特征处理

3. **实现方式**：
   - 位置无关的变换：每个位置共享相同的权重[[矩阵]]
   - 维度扩展：内部维度扩展4倍增强表达能力
   - 非线性激活：ReLU函数引入非线性变换能力

4. **在架构中的作用**：
   - 每个注意力子层之后都有一个FFN
   - 与[[注意力机制（Attention Mechanism）|注意力机制]]交替出现，形成层叠结构
   - [[残差连接]]和[[Layer Normalization|层归一化]]保证训练稳定性

## 来源
- [[Attention Is All You Need]] — 原始论文
- [[paper_06_transformer.md]] — 论文精读笔记
- [[raw/articles/ai-papers/foundations/paper_06_transformer.md]] — 原始资料

## 相关
- [[Transformer]] — component_of
- [[Self-Attention]] — complement_to
- [[Multi-Layer Perceptron]] — specialization_of
- [[Attention Is All You Need]] — introduced_in
- [[Feed Forward Networks]] — relates_to