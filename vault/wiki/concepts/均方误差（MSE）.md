---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["机器学习", "优化", "损失函数", "统计学"]
aliases: ["MSE", "Mean Squared Error", "平方误差损失", "L2 损失"]
relates_to:
  - target: "[[反向传播]]"
    type: used_in
  - target: "[[梯度下降（Gradient Descent）]]"
    type: optimized_by
  - target: "[[交叉熵]]"
    type: compares_to
supersedes: null
---

# 均方误差（MSE）

## 概述
均方误差（Mean Squared Error）是最常用的回归损失函数，[[计算]]预测值与真实值之差的平方的平均值，衡量预测的准确性。

## 关键内容
1. **数学定义**：L = ½(ŷ - y)²（单样本）或 L = (1/n)Σ(ŷᵢ - yᵢ)²（多样本）。平方操作确保误差始终为正，且对大误差给予更大惩罚。系数 ½ 是为了求导后消去 2，使梯度形式更简洁：∂L/∂ŷ = ŷ - y。
2. **在[[反向传播]]中的角色**：1986 年 Rumelhart 等人的原始[[反向传播]]论文使用 MSE 作为损失函数。MSE 的导数形式简单（ŷ - y），使得输出层的误差信号可以直接[[计算]]，然后通过[[链式法则]][[反向传播]]到隐藏层。
3. **优点与局限**：MSE 对异常值敏感（平方放大大误差的影响），在回归任务中表现良好。但在分类任务中，[[交叉熵]]损失通常更合适，因为它与概率解释兼容，且在预测错误时梯度更大、学习更快。
4. **与梯度下降的配合**：MSE 是凸函数（对于线性模型），[[梯度下降（Gradient Descent）]]可以找到全局最优。但对于非线性神经网络，损失面是非凸的，存在多个局部最优和[[鞍点（Saddle Point）]]。

## 来源
- [[paper_02_backpropagation]] — 损失函数（Loss Function）章节

## 相关
- [[反向传播]] — used_in
- [[梯度下降（Gradient Descent）]] — optimized_by
- [[交叉熵]] — compares_to
- [[梯度消失]] — relates_to
