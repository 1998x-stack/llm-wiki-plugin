---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["人工智能历史", "机器学习", "研究停滞", "LLM能力"]
aliases: ["AI Winter", "人工智能寒冬", "Neural Network Winter"]
relates_to:
  - target: "[[XOR 问题]]"
    type: caused
    confidence: 0.85
  - target: "[[Perceptrons (Minsky & Papert 1969)]]"
    type: caused
    confidence: 0.85
  - target: "[[感知机（Perceptron）]]"
    type: caused
    confidence: 0.7
  - target: "[[反向传播（Backpropagation）]]"
    type: supersedes
    confidence: 0.7
supersedes: null
---

# AI 寒冬

## 概述
AI 寒冬指 1969 年 [[Marvin Minsky|Minsky]]-[[Seymour Papert|Papert]]《[[Perceptrons (Minsky & Papert 1969)|Perceptrons]]》出版后，神经网络研究经费大幅削减、连接主义研究陷入停滞的十余年时期，直到[[反向传播（Backpropagation）|反向传播算法]]的复兴才结束。

## 关键内容

1. **触发事件**：1969 年 [[Marvin Minsky|Minsky]] 和 [[Seymour Papert|Papert]] 出版《[[Perceptrons (Minsky & Papert 1969)]]》，严格证明单层[[感知机]]无法解决线性不可分问题（如[[XOR 问题]]）。该结论被过度推广，导致整个神经网络领域被错误地放弃。

2. **研究停滞**：神经网络研究经费大幅削减，学术界转向符号主义 AI（基于规则和逻辑推理的方法），连接主义（基于神经网络的方法）研究几乎完全停滞。

3. **持续时间**：约从 1969 年持续到 1980 年代中期，长达十余年。

4. **结束标志**：1986 年 Rumelhart、[[Geoffrey E. Hinton|Hinton]] 和 Williams 发表[[反向传播]]论文，系统展示了多层网络的训练方法，标志着神经网络研究的复兴。

5. **历史教训**：[[XOR 问题]]的局限性仅针对单层[[感知机]]，[[多层感知机]]配合非线性激活和[[反向传播]]完全可以解决。但当时的学术界未能[[区分]]这一点，导致整个领域被错误地否定。

## 来源
- [[01_perceptron_1958]] — 感知机原始论文解读

## 相关
- [[XOR 问题]] — caused
- [[Perceptrons (Minsky & Papert 1969)]] — caused
- [[感知机（Perceptron）]] — caused
- [[反向传播（Backpropagation）]] — supersedes
