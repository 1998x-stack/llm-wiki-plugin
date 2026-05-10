---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "优化", "数学"]
aliases: ["Saddle Point", "鞍点问题", "高维鞍点"]
relates_to: ["Adam（自适应矩估计）", "Momentum（动量）", "随机梯度下降（SGD）", "梯度消失"]
supersedes: null
---

# 鞍点（Saddle Point）

## 概述 (50-200字符)
鞍点是高维优化空间中梯度为零但非局部最优的点——某些方向是极小值，某些方向是极大值。[[随机梯度下降（SGD）]]在鞍点附近更新极慢，是神经网络训练的主要障碍之一。

## 关键内容 (≥300字符, 用[[双链]])
1. **定义**：在多元函数中，鞍点是梯度 ∇f(θ)=0 但 Hessian [[矩阵]]既有正特征值又有负特征值的点。形象地说，一个方向看是山谷（极小），垂直方向看是山脊（极大）。在高维空间中，鞍点远比局部极小值常见——随维度增加，所有特征值同号的概率指数级下降。
2. **对 SGD 的威胁**：[[随机梯度下降（SGD）]]在鞍点附近梯度趋零，更新步长 η·∇L(θ) 极小，训练几乎停滞。这是 SGD 的四大痛点之一。高维神经网络的损失曲面中鞍点极其密集，是训练缓慢的主要原因。
3. **Adam 的解决方案**：[[Adam（自适应矩估计）]]通过二阶矩 vₜ 追踪梯度方差——即使梯度均值 m̂ 趋零（鞍点特征），只要梯度有波动（不同方向曲率不同），v̂ 就非零，有效学习率 η/√v̂ 仍能提供更新动力。同时[[Momentum（动量）]]的惯性帮助穿越梯度趋零区域。
4. **与其他方法对比**：二阶优化方法（如 Newton 法）通过 Hessian 的负特征值方向逃离鞍点，但[[计算]]代价过高。一阶方法中，[[Momentum（动量）|Momentum]] 和自适应学习率是逃离鞍点最实用的策略。随机噪声（如 SGD 的 mini-batch 采样噪声）也有助于逃离鞍点。

## 来源
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR 2015.] — Adam 论文中鞍点问题的动机
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件

## 相关
- [[Adam（自适应矩估计）]] — addressed_by
- [[Momentum（动量）]] — helps_escape
- [[随机梯度下降（SGD）]] — problem_for
- [[梯度消失]] — related_phenomenon
- [[Hessian 矩阵]] — mathematical_definition
