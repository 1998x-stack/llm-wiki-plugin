---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "线性不可分", "神经网络"]
aliases: ["XOR Problem", "异或问题", "Exclusive OR Problem"]
relates_to:
  - target: "[[感知机（Perceptron）]]"
    type: contradicts
    confidence: 1.0
  - target: "[[Perceptrons (Minsky & Papert 1969)]]"
    type: implements
    confidence: 1.0
  - target: "[[AI 寒冬]]"
    type: caused
    confidence: 0.85
  - target: "[[多层感知机（MLP）]]"
    type: supersedes
    confidence: 0.8
supersedes: null
---

# XOR 问题

## 概述
XOR（异或）是单层[[感知机]]无法解决的经典线性不可分问题，由 [[Marvin Minsky|Minsky]] 和 [[Seymour Papert|Papert]] 在 1969 年《[[Perceptrons (Minsky & Papert 1969)|Perceptrons]]》中严格证明，直接导致 [[AI 寒冬]]。

## 关键内容

1. **XOR 真值表**：x₁=0,x₂=0→0；x₁=0,x₂=1→1；x₁=1,x₂=0→1；x₁=1,x₂=1→0。输出为 1 当且仅当两个输入不同。

2. **几何不可分性**：在二维特征空间中，(0,0) 和 (1,1) 为一类（输出 0），(0,1) 和 (1,0) 为另一类（输出 1）。这两类样本呈对角分布，无法用一条直线分开。

3. **[[Marvin Minsky|Minsky]]-[[Seymour Papert|Papert]] 证明**：1969 年《[[Perceptrons (Minsky & Papert 1969)]]》严格证明了单层[[感知机]]只能解决线性可分问题，XOR 作为反例证明了[[感知机]]的根本局限。

4. **历史后果**：该证明发表后，神经网络研究经费大幅削减，学术界转向符号主义 AI，连接主义研究进入长达十余年的[[AI 寒冬]]。

5. **解决方案**：XOR 问题最终通过[[多层感知机（MLP）]]解决——添加隐藏层并引入非线性激活函数（如 sigmoid、ReLU），配合[[反向传播（Backpropagation）]][[算法]]训练，即可学习任意非线性[[决策边界]]。

## 来源
- [[01_perceptron_1958]] — 感知机原始论文解读
- [[paper_01_perceptron.md]] — 不能做的：非线性问题 & Minsky的"毁灭一击"章节

## 相关
- [[感知机（Perceptron）]] — contradicts
- [[Perceptrons (Minsky & Papert 1969)]] — implements
- [[AI 寒冬]] — caused
- [[多层感知机（MLP）]] — supersedes
