---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "优化", "优化器"]
aliases: ["Adam", "Adaptive Moment Estimation", "自适应矩估计", "Adam 优化器"]
relates_to: ["Adam: A Method for Stochastic Optimization (2014 论文)", "Diederik P. Kingma", "Jimmy Ba", "Momentum（动量）", "RMSProp", "AdamW", "随机梯度下降（SGD）"]
supersedes: null
---

# Adam（自适应矩估计）

## 概述 (50-200字符)
Adam 是深度学习的"自动挡"优化器，结合动量和自适应学习率，为每个参数自动调节更新速度。默认参数开箱即用，是 [[Transformer 架构|Transformer]]、GAN、[[强化学习]]等场景的默认选择。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[算法]]核心**：Adam = [[Momentum（动量）]] + [[RMSProp]] + [[偏差修正（Bias Correction）]]。每步更新包含六个步骤：(1) [[计算]]梯度 gₜ；(2) 更新一阶矩 mₜ = β₁·mₜ₋₁ + (1-β₁)·gₜ（梯度指数移动平均）；(3) 更新二阶矩 vₜ = β₂·vₜ₋₁ + (1-β₂)·gₜ²（梯度平方指数移动平均）；(4)(5) [[偏差修正（Bias Correction）|偏差修正]] m̂ₜ = mₜ/(1-β₁ᵗ)、v̂ₜ = vₜ/(1-β₂ᵗ)；(6) 参数更新 θₜ = θₜ₋₁ - η·m̂ₜ/(√v̂ₜ + ε)。
2. **自适应直觉**：梯度方向稳定的参数 → m̂ 大、v̂ 小 → 有效学习率大（加速）；梯度剧烈震荡的参数 → m̂ 趋零、v̂ 大 → 有效学习率小（自动减速）。这解决了[[随机梯度下降（SGD）]]的四大痛点：学习率难选、参数共用学习率、[[鞍点（Saddle Point）]]停滞、梯度尺度差异。
3. **默认超参数**：η=0.001, β₁=0.9, β₂=0.999, ε=1e-8。这组值在绝大多数任务上开箱即用，无需调整。β₁=0.9 意味着动量窗口约 10 步，β₂=0.999 意味着二阶矩窗口约 1000 步。
4. **局限与改进**：(a) 某些任务收敛不如 SGD+[[Momentum（动量）|Momentum]]（如 CNN [[ImageNet]] 训练）；(b) [[权重衰减（Weight Decay）|权重衰减]]与自适应学习率耦合 → [[AdamW]] 解耦修正；(c) 早期二阶矩估计偏差 → AMSGrad 用历史最大 v̂；(d) 内存占用是 SGD 的 3 倍（需存 m、v）→ Adafactor 内存高效版。训练末期常配合 Cosine Annealing 学习率调度减少震荡。

## 来源
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR 2015.] — 原始论文
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件

## 相关
- [[Adam: A Method for Stochastic Optimization (2014 论文)]] — introduced_by
- [[Diederik P. Kingma]] — co_inventor
- [[Jimmy Ba]] — co_inventor
- [[Momentum（动量）]] — builds_on
- [[RMSProp]] — builds_on
- [[偏差修正（Bias Correction）]] — key_component
- [[AdamW]] — improved_by
- [[随机梯度下降（SGD）]] — supersedes_in_practice
- [[鞍点（Saddle Point）]] — addresses
