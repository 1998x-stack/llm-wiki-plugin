---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 4
tags: ["概率论", "深度学习", 时间序列]
aliases: ["Backpropagation", "反向传播算法", "误差反向传播", "BP算法"]
relates_to:
  - target: "[[McCulloch-Pitts 神经元模型]]"
    type: extends
    confidence: 0.9
  - target: "[[LSTM（长短期记忆网络）]]"
    type: extends
    confidence: 0.85
  - target: "[[Transformer架构]]"
    type: extends
    confidence: 0.75
  - target: "[[Learning Representations by Back-propagating Errors (1986 论文)]]"
    type: formalized_in
    confidence: 0.95
  - target: "[[David E. Rumelhart]]"
    type: developed_by
    confidence: 0.9
  - target: "[[Geoffrey E. Hinton]]"
    type: developed_by
    confidence: 0.9
  - target: "[[Ronald J. Williams]]"
    type: developed_by
    confidence: 0.9
  - target: "[[XOR问题]]"
    type: solves
    confidence: 0.95
  - target: "[[信用分配问题（Credit Assignment Problem）]]"
    type: addresses
    confidence: 0.95
  - target: "[[链式法则]]"
    type: uses
    confidence: 0.95
  - target: "[[Sigmoid激活函数]]"
    type: works_with
    confidence: 0.85
  - target: "[[梯度下降（Gradient Descent）]]"
    type: complements
    confidence: 0.95
  - target: "[[家族关系学习]]"
    type: demonstrated_in_experiment
    confidence: 0.8
supersedes: null
---

# 反向传播（Backpropagation）

## 概述
Rumelhart、[[Geoffrey E. Hinton|Hinton]] 和 Williams 于 1986 年在 *[[Nature]]* 发表论文，系统展示了[[反向传播]][[算法]]如何通过[[链式法则]]将输出误差逆向传播到隐藏层，使多层神经网络能够自动学习有用的内部表示，解决了困扰 AI 领域十余年的"信用[[点数问题|分配问题]]"。该[[算法]]是现代深度学习的基石。

## 关键内容

1. **历史背景**：1969 年 [[Marvin Minsky|Minsky]]-[[Seymour Papert|Papert]]《[[感知机（Perceptron）|感知器]]》证明单层[[感知机（Perceptron）|感知器]]无法解决 [[XOR 问题]]，导致神经网络研究陷入"[[AI 寒冬]]"。出路是添加隐藏层，但如何训练隐藏层成为核心难题。

2. **信用[[信用分配问题（Credit Assignment Problem）|分配问题]]**：当系统整体犯错时，如何将责任分配给每个组件？输出层误差可直接[[计算]]，但隐藏层没有"期望输出"可供参考。

3. **核心[[算法]]**：通过[[链式法则]]逐层[[计算]]复合函数导数，将误差从输出层逆向传播到每个隐藏层神经元，实现梯度下降优化。具体来说，对于第l层权重W^(l)，梯度为：∂L/∂W^(l) = ∂L/∂ŷ · ∂ŷ/∂h^(l+1) · ... · ∂h^(l+1)/∂h^l · ∂h^l/∂W^l。

4. **1986年突破**：[[Learning Representations by Back-propagating Errors (1986 论文)]]中，Rumelhart、[[Geoffrey E. Hinton|Hinton]]和Williams不仅给出了完整的数学推导，还通过[[XOR问题]]和[[家族关系学习]]实验展示了[[算法]]的有效性，证明了网络能够自动学习有意义的内部表示。

5. **[[算法]]步骤**：1)前向传播：输入数据通过网络得到预测输出；2)[[计算]]损失：比较预测值与真实标签；3)[[反向传播]]：使用[[链式法则]][[计算]]各层梯度；4)参数更新：梯度下降更新权重。

6. **实验验证**：论文中的两个关键实验包括：[[XOR问题]]的解决，证明了多层网络能处理非线性可分问题；[[家族关系学习]]实验，展示了网络自动学习抽象概念的能力。

7. **历史优先权**：Werbos（1974 博士论文）最早提出，Linnainmaa（1970）描述[[自动微分]]反向模式，Parker（1985）独立再发现。但 Rumelhart 等人的论文通过令人信服的实验展示了隐藏层自动学习有意义内部表示的能力。

8. **[[规范化理论|范式]]意义**：标志着连接主义对符号主义的强势回归，证明了多层网络的理论和实践可行性。

## 来源
- [[Learning Representations by Back-propagating Errors (1986 论文)]] — 反向传播学习表示
- [[raw/articles/ai-papers/foundations/paper_02_backpropagation.md]] — 源文件
- [Nature 323, 533–536 (1986)] — 原始论文

## 相关
- [[McCulloch-Pitts 神经元模型]] — extends
- [[LSTM（长短期记忆网络）]] — extends
- [[Transformer架构]] — extends
- [[Learning Representations by Back-propagating Errors (1986 论文)]] — formalized_in
- [[David E. Rumelhart]] — developed_by
- [[Geoffrey E. Hinton]] — developed_by
- [[Ronald J. Williams]] — developed_by
- [[XOR问题]] — solves
- [[信用分配问题（Credit Assignment Problem）]] — addresses
- [[链式法则]] — uses
- [[家族关系学习]] — demonstrated_in
- [[梯度下降（Gradient Descent）]] — complements
