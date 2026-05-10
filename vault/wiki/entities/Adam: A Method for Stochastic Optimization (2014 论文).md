---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["论文", "机器学习", "深度学习", "优化"]
aliases: ["Adam 论文", "Adam: A Method for Stochastic Optimization", "Kingma & Ba 2014"]
relates_to: ["Diederik P. Kingma", "Jimmy Ba", "Adam（自适应矩估计）", "AdamW", "ICLR"]
supersedes: null
---

# Adam: A Method for Stochastic Optimization (2014 论文)

## 概述 (50-200字符)
[[Diederik P. Kingma]] 与 [[Jimmy Ba]] 于 2014 年提交 arXiv、发表于 ICLR 2015 的里程碑论文，提出 Adam [[Adam（自适应矩估计）|自适应矩估计]]优化[[算法]]。该[[算法]]成为深度学习训练默认优化器，引用率超过 10 万次。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题动机**：论文指出[[随机梯度下降（SGD）]]在实际神经网络训练中存在四大痛点：(a) 学习率难以选取；(b) 所有参数共用同一学习率，无法适应梯度尺度差异；(c) [[鞍点（Saddle Point）]]处梯度趋零导致更新停滞；(d) 不同层参数量级相差千倍，统一学习率无法兼顾。
2. **核心[[算法]]**：提出 Adam = [[Momentum（动量）]] + [[RMSProp]] + [[偏差修正（Bias Correction）]]。一阶矩 mₜ 追踪梯度均值（动量），二阶矩 vₜ 追踪梯度方差（自适应学习率），[[偏差修正（Bias Correction）|偏差修正]] m̂ₜ、v̂ₜ 解决初始化时矩估计偏向零的问题。推荐默认超参数：η=0.001, β₁=0.9, β₂=0.999, ε=1e-8，开箱即用。
3. **理论贡献**：论文提供了凸设定下的收敛性证明，展示 Adam 的后悔界（regret bound）与最优静态解相当。[[偏差修正（Bias Correction）|偏差修正]]项 (1-βᵗ) 在训练初期至关重要，随 t 增大自动消失。
4. **历史影响**：Adam 让深度学习训练变成"自动挡"——无需精心调学习率，[[算法]]为每个参数自动找到合适速度。后续衍生出[[AdamW]]（[[AdamW|解耦权重衰减]]）、AMSGrad（修正收敛问题）、Adafactor（内存高效）等变体，形成了完整的自适应优化器家族。

## 来源
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. arXiv:1412.6980. ICLR 2015.] — 原始论文
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件

## 相关
- [[Diederik P. Kingma]] — first_author
- [[Jimmy Ba]] — co_author
- [[Adam（自适应矩估计）]] — introduced
- [[AdamW]] — subsequent_improvement
- [[Momentum（动量）]] — builds_on
- [[RMSProp]] — builds_on
- [[偏差修正（Bias Correction）]] — key_contribution
- [[随机梯度下降（SGD）]] — supersedes_in_practice
