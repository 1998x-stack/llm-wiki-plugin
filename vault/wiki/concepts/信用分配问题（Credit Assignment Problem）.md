---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["机器学习", "深度学习", "理论问题"]
aliases: ["Credit Assignment Problem", "信用分配问题", "责任分配问题", "梯度分配问题"]
relates_to:
  - target: "[[反向传播（Backpropagation）]]"
    type: solved_by
    confidence: 0.95
  - target: "[[Learning Representations by Back-propagating Errors (1986 论文)]]"
    type: addressed_in
    confidence: 0.9
  - target: "[[链式法则]]"
    type: uses_solution_of
    confidence: 0.9
  - target: "[[多层感知机]]"
    type: prevented_training_of
    confidence: 0.9
  - target: "[[感知机]]"
    type: solved_problem_for
    confidence: 0.85
supersedes: null
---

# 信用分配问题（Credit Assignment Problem）

## 概述 (50-200字符)
信用[[点数问题|分配问题]]是指在一个多层神经网络中，如何将最终的预测误差合理地分配给网络中每一个权重或组件的问题。这是一个困扰AI领域十余年的核心问题，直到1986年[[反向传播（Backpropagation）]][[算法]]的提出才得到解决。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题定义**：当一个深层网络产生错误输出时，如何知道是哪个权重或哪一层的神经元导致了这个错误？输出层的误差可以直接[[计算]]，但隐藏层没有"正确答案"供参考，因此无法直接[[计算]]其误差贡献。

2. **历史背景**：1969年[[Marvin Minsky|Minsky]]在《[[Perceptrons (Minsky & Papert 1969)|Perceptrons]]》中指出了单层[[感知机]]的局限性，特别是无法解决[[XOR问题]]。虽然添加隐藏层理论上可以解决这些问题，但如何训练隐藏层成为一个无法克服的障碍。信用[[点数问题|分配问题]]导致了AI的第一次"[[AI 寒冬]]"。

3. **[[反向传播]]解决方案**：1986年，[[David E. Rumelhart]]、[[Geoffrey E. Hinton]]和[[Ronald J. Williams]]在[[Learning Representations by Back-propagating Errors (1986 论文)]]中提出了通过[[链式法则]]将误差从输出层[[反向传播]]到隐藏层的解决方案。这个[[算法]]完美解决了信用[[点数问题|分配问题]]。

4. **数学实现**：通过[[链式法则]]，可以[[计算]]复合函数对任意中间变量的偏导数。对于网络中的每个权重，都可以[[计算]]其对最终误差的贡献，即 ∂L/∂w = ∂L/∂output × ∂output/∂intermediate × ∂intermediate/∂w。

5. **深远影响**：信用[[点数问题|分配问题]]的解决使得[[多层感知机]]的训练成为可能，直接引发了深度学习的复兴。这个问题的解决不仅是技术上的突破，更是理论上的验证——证明了神经网络确实可以学习有意义的内部表示。

## 来源
- [Learning Representations by Back-propagating Errors] — Rumelhart, Hinton & Williams, Nature 1986
- [[raw/articles/ai-papers/foundations/paper_02_backpropagation.md]] — 源文件
- [Minsky, M. L., & Papert, S. A. (1969). Perceptrons.] — 原始问题提出

## 相关
- [[反向传播（Backpropagation）]] — solved_by
- [[Learning Representations by Back-propagating Errors (1986 论文)]] — addressed_in
- [[链式法则]] — uses_solution_of
- [[David E. Rumelhart]] — addressed_by
- [[Geoffrey E. Hinton]] — addressed_by
- [[Ronald J. Williams]] — addressed_by
- [[多层感知机]] — enabled_by_solution
- [[感知机]] — problem_prevented_solution
