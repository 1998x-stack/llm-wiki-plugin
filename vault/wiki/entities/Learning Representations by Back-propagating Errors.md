---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["论文", "机器学习", "深度学习", "神经网络"]
aliases: ["Learning Representations by Back-Propagating Errors", "Rumelhart 1986 BP论文"]
relates_to: ["反向传播", "多层感知机", "Geoffrey E. Hinton", "David E. Rumelhart", "Ronald J. Williams"]
supersedes: null
---

# Learning Representations by Back-propagating Errors

## 概述 (50-200字符)
1986 年发表于 *Nature* 的里程碑论文，仅 4 页，首次系统阐述了[[反向传播]]算法用于训练多层神经网络。该论文使[[多层感知机]]的训练成为可能，直接开启了现代深度学习的大门。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心贡献**：论文给出了误差从输出层沿计算图逆向传播的完整数学推导，用微积分[[链式法则]]计算每个权重对误差的贡献，然后梯度下降更新。关键洞见是"每一层只需知道从上层传来的误差信号和自己局部的导数"——完全局部化，可以无限叠加层数。
2. **解决的历史难题**：感知机的 XOR 危机后，神经网络研究沉寂了十余年。多层网络理论上可解决非线性问题，但隐藏层权重无法训练。这篇论文彻底解答了"中间隐藏层的权重该怎么训练"这一根本问题。
3. **算法效率**：论文证明了[[反向传播]]相比数值微分（对每个参数做一次前向传播）的效率优势：一次前向+一次反向 = O(1) 次前向传播的计算量，训练速度提升 N 倍（N 为参数量）。这一效率优势使大规模神经网络训练成为现实。
4. **历史地位**：尽管[[反向传播]]的思想更早已有人提出（如 Werbos 1974），但这篇 *Nature* 论文以其简洁性和影响力使其成为深度学习领域的奠基之作。无论 CNN、RNN、[[Transformer 架构|Transformer]]，所有现代深度学习架构的训练都依赖 BP。[[自动微分]]框架（PyTorch/[[TensorFlow]]）的核心即 BP 的工程化实现。

## 来源
- [Nature 323(6088), 533–536] — Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986)
- [raw/articles/ai-papers/machine-learning/02_backpropagation_1986.md] — 源文件

## 相关
- [[反向传播]] — introduces
- [[多层感知机]] — enables
- [[Geoffrey E. Hinton]] — authored_by
- [[David E. Rumelhart]] — authored_by
- [[Ronald J. Williams]] — authored_by
- [[链式法则]] — uses
- [[XOR问题]] — solves
