---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "逻辑问题"]
aliases: ["XOR Problem", "异或问题", "XOR Gate Problem"]
relates_to: ["感知机", "多层感知机", "反向传播", "非线性可分"]
supersedes: null
---

# XOR问题

## 概述 (50-200字符)
XOR（异或）问题是感知机无法解决的经典非线性可分问题：XOR 运算的真值表无法用一条直线在二维平面上分隔为正负两类。1969 年 Minsky 指出此问题后，神经网络研究沉寂十余年，直到[[多层感知机]]和[[反向传播]]的出现才被彻底解决。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题定义**：XOR 运算的真值表为 (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0。在二维平面上，这四个点无法用一条直线将输出为 0 和 1 的点分开，因此 XOR 是"非线性可分"的。单层[[感知机]]只能学习线性决策边界，故无法解决 XOR。
2. **历史影响**：1969 年 Minsky 和 Papert 在《[[Perceptrons (Minsky & Papert 1969)|Perceptrons]]》一书中系统分析了感知机的局限性，[[XOR 问题]]成为最著名的例证。这本书直接导致了神经网络研究的第一次"[[AI 寒冬]]"，研究沉寂了十余年。
3. **MLP 的解决**：[[多层感知机]]通过隐藏层引入非线性变换能力，可以学习非线性的决策边界。一个 2→4→1 的 MLP（2 维输入，4 维隐藏层，1 维输出）配合[[反向传播]]训练，可以完美学习 XOR 函数。隐藏层实际上学习了输入空间的非线性映射，使原本不可分的问题在隐藏层空间中变得线性可分。
4. **理论意义**：[[XOR 问题]]揭示了线性模型的表达能力局限，推动了非线性模型的发展。通用近似定理（Universal Approximation Theorem）证明：具有单个隐藏层和足够多神经元的 MLP 可以以任意精度逼近任意连续函数——XOR 只是其中最简单的一个特例。

## 来源
- [Learning Representations by Back-propagating Errors] — Rumelhart, Hinton & Williams, Nature 1986
- [raw/articles/ai-papers/machine-learning/02_backpropagation_1986.md] — 源文件

## 相关
- [[感知机]] — contradicts
- [[多层感知机]] — solves
- [[反向传播]] — uses
- [[非线性可分]] — exemplifies
