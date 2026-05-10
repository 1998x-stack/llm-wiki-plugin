---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, deep-learning, representation-learning]
aliases: [Hinton & Salakhutdinov 2006]
relates_to:
  - target: Geoffrey E. Hinton
    relation: authored_by
  - target: Ruslan Salakhutdinov
    relation: authored_by
  - target: 深度信念网络
    relation: introduced
supersedes: null
---

# Reducing the Dimensionality of Data with Neural Networks (2006 论文)

## 概述
展示[[深度信念网络]]可以有效学习数据层次化表示的论文，引发了深度学习复兴。

## 关键内容

1. **逐层预训练**：提出使用受限玻尔兹曼机（RBM）逐层预训练深度网络，克服 [[梯度消失]] 问题。
2. **维度约减**：展示深度网络可以学习比 PCA 等传统方法更有效的数据低维表示。
3. **历史意义**：该论文被视为 2006 年深度学习复兴的起点，为后续的 [[预训练-微调范式]] 和 [[BERT]] 奠定思想基础。

## 来源
- [[ai_papers_timeline.md]] — 2006 年时间线条目

## 相关
- [[Geoffrey E. Hinton]] — authored_by
- [[Ruslan Salakhutdinov]] — authored_by
- [[深度信念网络]] — introduced
- [[预训练-微调范式]] — influenced
