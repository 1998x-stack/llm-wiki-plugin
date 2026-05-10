---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 深度学习, 协同过滤]
aliases: ["Multi-Layer Perceptron in NCF", "MLP for NCF"]
relates_to:
  - target: "[[Neural Collaborative Filtering 论文]]"
    type: introduced_by
    confidence: 0.9
  - target: "[[NeuMF]]"
    type: component_of
    confidence: 0.9
  - target: "[[神经协同过滤]]"
    type: instance_of
    confidence: 0.9
  - target: "[[多层感知机]]"
    type: variant_of
    confidence: 0.8
supersedes: null
---

# MLP (NCF)

## 概述
神经协同过滤(NCF)框架中的多层感知机模型，专门用于学习用户-物品交互中的非线性模式。

## 关键内容
1. **架构特点**：将用户嵌入和物品嵌入首先拼接(concatenation)，然后通过多个全连接层逐层变换，每一层维度逐渐减半，激活函数选用ReLU。

2. **非线性建模**：与GMF的逐元素乘积不同，MLP通过拼接和多层变换，能够学习到用户和物品潜在因子之间任意复杂的交叉模式。

3. **与GMF对比**：MLP从零开始自由探索交互模式空间，而GMF像是在已知"交互应该是乘法形式"的前提下做精细调整，MLP在多数实验设置下性能优于GMF。

## 来源
- [[10-ncf.md]] — raw/books/推荐系统/10-ncf.md
- [[Neural Collaborative Filtering 论文]] — 原始论文

## 相关
- [[神经协同过滤]] — 所属框架
- [[NeuMF]] — 组成部分
- [[GMF]] — 对比模型
- [[多层感知机]] — 基础模型
- [[拼接]] — 采用的操作
- [[非线性]] — 捕捉的模式