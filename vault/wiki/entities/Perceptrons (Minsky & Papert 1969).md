---
type: entity
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "人工智能历史", "书籍"]
aliases: ["Perceptrons", "Minsky Papert 1969", "感知器（书）"]
relates_to:
  - target: "[[感知机（Perceptron）]]"
    type: compares_to
    confidence: 0.9
  - target: "[[XOR 问题]]"
    type: implements
    confidence: 1.0
  - target: "[[AI 寒冬]]"
    type: caused
    confidence: 0.85
supersedes: null
---

# Perceptrons (Minsky & Papert 1969)

## 概述
[[Marvin Minsky|Minsky]] 和 [[Seymour Papert|Papert]] 于 1969 年出版的著作，严格证明了单层[[感知机]]无法解决线性不可分问题（如 XOR），直接导致神经网络研究进入长达十余年的 [[AI 寒冬]]。

## 关键内容

1. **核心定理**：证明了单层[[感知机]]无法解决线性不可分问题，以 XOR（异或）为经典反例——无法用一条直线将 (0,0)/(1,1) 与 (0,1)/(1,0) 分开。

2. **XOR 真值表**：x₁=0,x₂=0→0；x₁=0,x₂=1→1；x₁=1,x₂=0→1；x₁=1,x₂=1→0。四类样本在二维空间中呈对角分布，无法线性分割。

3. **历史影响**：该书出版后，神经网络研究经费大幅削减，学术界转向符号主义 AI，连接主义研究陷入长达十余年的"[[AI 寒冬]]"。

4. **后续修正**：[[Marvin Minsky|Minsky]]-[[Seymour Papert|Papert]] 的结论仅适用于单层[[感知机]]。[[多层感知机（MLP）]]配合[[非线性激活]]和[[反向传播（Backpropagation）|反向传播算法]]最终突破了这一限制。

5. **历史评价**：该书在数学上完全正确，但其结论被过度推广，导致整个神经网络领域被错误地放弃。

## 来源
- [[01_perceptron_1958]] — 感知机原始论文解读

## 相关
- [[感知机（Perceptron）]] — compares_to
- [[XOR 问题]] — implements
- [[AI 寒冬]] — caused
