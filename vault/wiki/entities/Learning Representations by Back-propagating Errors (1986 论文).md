---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [paper, deep-learning, backpropagation, neural-networks, 机器学习]
aliases: ["Rumelhart, Hinton, Williams 1986", "Learning Representations by Back-propagating Errors", "反向传播算法论文"]
relates_to:
  - target: "[[David E. Rumelhart]]"
    type: authored_by
    confidence: 0.95
  - target: "[[Geoffrey E. Hinton]]"
    type: authored_by
    confidence: 0.95
  - target: "[[Ronald J. Williams]]"
    type: authored_by
    confidence: 0.95
  - target: "[[反向传播（Backpropagation）]]"
    type: introduced
    confidence: 0.95
  - target: "[[XOR问题]]"
    type: demonstrates_solution_to
    confidence: 0.9
  - target: "[[信用分配问题（Credit Assignment Problem）]]"
    type: addresses
    confidence: 0.95
  - target: "[[链式法则]]"
    type: uses
    confidence: 0.9
  - target: "[[Sigmoid激活函数]]"
    type: uses
    confidence: 0.85
  - target: "[[家族关系学习]]"
    type: demonstrates_with_experiment
    confidence: 0.8
supersedes: null
---

# Learning Representations by Back-propagating Errors (1986 论文)

## 概述
[[反向传播]][[算法]]的经典论文，系统化描述了如何通过[[链式法则]]训练多层神经网络，引发深度学习复兴。该论文在[[Nature]]期刊发表，证明了多层网络能自动学习有意义的内部表示。

## 关键内容

1. **[[算法]]描述**：清晰展示了误差从输出层向输入层逐层传播的数学过程，使多层网络训练成为可能。通过[[链式法则]]将最终的预测错误合理分配给网络中每一个权重。

2. **[[链式法则]]应用**：将微积分中的 [[链式法则]] 应用于神经网络梯度[[计算]]，奠定了现代深度学习框架的核心[[算法]]。公式：∂L/∂W^(1) = ∂L/∂ŷ · ∂ŷ/∂h^(2) · ∂h^(2)/∂h^(1) · ∂h^(1)/∂W^(1)

3. **历史意义**：该论文被视为深度学习复兴的关键文献，解决了困扰AI领域十余年的"[[信用分配问题（Credit Assignment Problem）|信用分配问题]]"。直接催生了 [[多层感知机]] 的实用化和后续 [[卷积神经网络（CNN）]] 的发展。

4. **[[XOR问题]]解决**：论文演示了如何用两层网络配合[[反向传播]]解决[[XOR问题]]，这曾是单层[[感知机]]无法解决的经典案例。网络在训练后能够正确预测所有四种输入组合。

5. **[[家族关系学习]]实验**：论文中最具启发性的实验之一——让网络学习家族关系，结果网络在隐藏层自动形成了"国籍"、"辈分"等抽象概念，证明了神经网络能学到有意义的内部表示。

6. **[[Sigmoid激活函数]]**：1986年论文选用Sigmoid函数作为激活函数，因其处处可导便于梯度[[计算]]，但这也为后来的[[梯度消失]]问题埋下了伏笔。

## 来源
- [[raw/articles/ai-papers/foundations/paper_02_backpropagation.md]] — 源文件
- [[ai_papers_timeline.md]] — 1986 年时间线条目
- [Nature 323, 533–536 (1986)] — 原始论文

## 相关
- [[David E. Rumelhart]] — authored_by
- [[Geoffrey E. Hinton]] — authored_by
- [[Ronald J. Williams]] — authored_by
- [[反向传播（Backpropagation）]] — introduced
- [[XOR问题]] — demonstrates_solution_to
- [[信用分配问题（Credit Assignment Problem）]] — addresses
- [[Sigmoid激活函数]] — uses
- [[家族关系学习]] — demonstrates_with_experiment
