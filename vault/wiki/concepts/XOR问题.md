---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["机器学习", "深度学习", "逻辑问题"]
aliases: ["XOR Problem", "异或问题", "XOR Gate Problem"]
relates_to:
  - target: "[[感知机]]"
    type: contradicts
    confidence: 0.9
  - target: "[[多层感知机]]"
    type: solved_by
    confidence: 0.95
  - target: "[[反向传播]]"
    type: solved_by
    confidence: 0.95
  - target: "[[非线性可分]]"
    type: exemplifies
    confidence: 0.9
  - target: "[[Learning Representations by Back-propagating Errors (1986 论文)]]"
    type: solved_in_paper
    confidence: 0.95
supersedes: null
---

# XOR问题

## 概述 (50-200字符)
XOR（异或）问题是[[感知机]]无法解决的经典非线性可分问题：XOR 运算的真值表无法用一条直线在二维平面上分隔为正负两类。1969 年 [[Marvin Minsky|Minsky]] 指出此问题后，神经网络研究沉寂十余年，直到[[多层感知机]]和[[反向传播]]的出现才被彻底解决。1986年[[Learning Representations by Back-propagating Errors (1986 论文)]]中详细展示了解决方案。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题定义**：XOR 运算的真值表为 (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0。在二维平面上，这四个点无法用一条直线将输出为 0 和 1 的点分开，因此 XOR 是"非线性可分"的。单层[[感知机]]只能学习线性[[决策边界]]，故无法解决 XOR。

2. **历史影响**：1969 年 [[Marvin Minsky|Minsky]] 和 [[Seymour Papert|Papert]] 在《[[Perceptrons (Minsky & Papert 1969)|Perceptrons]]》一书中系统分析了[[感知机]]的局限性，[[XOR 问题]]成为最著名的例证。这本书直接导致了神经网络研究的第一次"[[AI 寒冬]]"，研究沉寂了十余年。

3. **MLP 的解决**：[[多层感知机]]通过隐藏层引入非线性变换能力，可以学习非线性的[[决策边界]]。一个 2→4→1 的 MLP（2 维输入，4 维隐藏层，1 维输出）配合[[反向传播]]训练，可以完美学习 XOR 函数。隐藏层实际上学习了输入空间的非线性映射，使原本不可分的问题在隐藏层空间中变得线性可分。

4. **理论意义**：[[XOR 问题]]揭示了线性模型的表达能力局限，推动了非线性模型的发展。通用近似定理（[[万能近似定理|Universal Approximation Theorem]]）证明：具有单个隐藏层和足够多神经元的 MLP 可以以任意精度逼近任意连续函数——XOR 只是其中最简单的一个特例。

5. **1986年论文中的解决**：[[Learning Representations by Back-propagating Errors (1986 论文)]]中详细演示了如何用两层网络解决XOR问题。论文展示了网络如何通过[[反向传播]][[算法]]学习到正确的权重[[Configuration|配置]]，使得四个输入组合都能被正确分类，这是[[反向传播]][[算法]]有效性的关键证明。

6. **实验演示**：1986年论文中包含了具体的XOR实验，证明了两层网络配合适当的学习[[算法]]确实能够解决这一经典问题，为多层网络的实用性提供了坚实的实验基础。

## 来源
- [[Learning Representations by Back-propagating Errors (1986 论文)]] — 解决方案出处
- [[raw/articles/ai-papers/foundations/paper_02_backpropagation.md]] — 源文件
- [Learning Representations by Back-propagating Errors] — Rumelhart, Hinton & Williams, Nature 1986

## 相关
- [[感知机]] — contradicts
- [[多层感知机]] — solves
- [[反向传播]] — uses
- [[非线性可分]] — exemplifies
- [[David E. Rumelhart]] — solved_by
- [[Geoffrey E. Hinton]] — solved_by
- [[Ronald J. Williams]] — solved_by
