---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "优化", "优化器"]
aliases: ["Bias Correction", "偏差修正", "Adam 偏差修正", "矩估计偏差修正"]
relates_to: ["Adam（自适应矩估计）", "Momentum（动量）", "RMSProp", "指数移动平均"]
supersedes: null
---

# 偏差修正（Bias Correction）

## 概述 (50-200字符)
偏差修正解决指数移动平均初始化偏差问题。Adam 中 m₀=v₀=0 导致早期矩估计严重偏向零，修正项 m̂ₜ=mₜ/(1-βᵗ) 在训练初期恢复真实估计值。

## 关键内容 (≥300字符, 用[[双链]])
1. **问题根源**：[[Momentum（动量）]]和[[RMSProp]]的二阶矩都从零初始化（m₀=v₀=0）。以 β₁=0.9 为例，第一步 m₁ = 0.9×0 + 0.1×g₁ = 0.1×g₁，仅为真实梯度的 10%！这意味着训练初期的更新幅度严重不足，收敛极慢。
2. **修正公式**：m̂ₜ = mₜ/(1-β₁ᵗ)，v̂ₜ = vₜ/(1-β₂ᵗ)。第一步修正后：m̂₁ = 0.1×g₁/(1-0.9) = g₁，完美恢复真实梯度。随着 t 增大，(1-βᵗ)→1，修正项自动消失，后期几乎无影响。
3. **在 Adam 中的实现**：[[Adam（自适应矩估计）]]同时对一阶矩和二阶矩做偏差修正。代码中常将修正合并到学习率：lr_t = η·√(1-β₂ᵗ)/(1-β₁ᵗ)，等价于分别修正后[[计算]]。这确保训练初期更新幅度合理，收敛速度与中后期一致。
4. **数学本质**：偏差修正是指数移动平均（EMA）的无偏估计。EMA 的期望 E[mₜ] = (1-βᵗ)·E[g]，除以 (1-βᵗ) 后得到无偏估计。这是统计学中偏差-方差权衡的经典应用——修正消除了偏差，但略微增加了方差。

## 来源
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR 2015.] — Adam 论文中的偏差修正机制
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件

## 相关
- [[Adam（自适应矩估计）]] — key_component_of
- [[Momentum（动量）]] — corrects_bias_in
- [[RMSProp]] — corrects_bias_in
- [[指数移动平均（EMA）]] — statistical_basis
