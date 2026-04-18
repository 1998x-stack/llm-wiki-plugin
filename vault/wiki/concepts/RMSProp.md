---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "优化", "优化器"]
aliases: ["RMSProp", "Root Mean Square Propagation", "均方根传播"]
relates_to: ["Adam（自适应矩估计）", "Momentum（动量）", "AdaGrad", "随机梯度下降（SGD）"]
supersedes: null
---

# RMSProp

## 概述 (50-200字符)
RMSProp 为每个参数维护梯度平方的指数移动平均，实现自适应学习率。梯度大的参数自动减速，梯度小的参数自动加速。是 [[Adam（自适应矩估计）|Adam 优化器]]的二阶矩组件。

## 关键内容 (≥300字符, 用[[双链]])
1. **算法**：vₜ = β₂·vₜ₋₁ + (1-β₂)·gₜ²，θ ← θ - η/(√vₜ + ε)·gₜ。二阶矩 vₜ 追踪梯度平方的指数移动平均，有效学习率为 η/√vₜ。β₂ 通常取 0.999，窗口约 1000 步。ε=1e-8 防止除零。
2. **自适应直觉**：梯度大的参数 → vₜ 大 → 有效学习率 η/√vₜ 小（自动减速，防止震荡）；梯度小的参数 → vₜ 小 → 有效学习率 η/√vₜ 大（自动加速，加快收敛）。这解决了[[随机梯度下降（SGD）]]中所有参数共用同一学习率的问题——例如[[词嵌入（Word Embedding）|词嵌入]]中高频词梯度大、低频词梯度小，RMSProp 能自动平衡。
3. **与 AdaGrad 的关系**：RMSProp 改进了 AdaGrad 的单调递减学习率问题。AdaGrad 累积所有历史梯度平方和，学习率只会单调下降，可能过早停止学习。RMSProp 使用指数移动平均，赋予近期梯度更大权重，学习率可以回升。
4. **在 Adam 中的角色**：[[Adam（自适应矩估计）]]将 RMSProp 作为二阶矩组件（β₂=0.999），与[[Momentum（动量）]]的一阶矩结合。Adam 额外引入了[[偏差修正（Bias Correction）|偏差修正]]机制，解决 RMSProp 初始化时 v₀=0 导致的早期学习率过大问题。

## 来源
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR 2015.] — Adam 论文中的 RMSProp 组件
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件

## 相关
- [[Adam（自适应矩估计）]] — component_of
- [[Momentum（动量）]] — combined_in_adam
- [[AdaGrad]] — improves
- [[随机梯度下降（SGD）]] — improves
- [[偏差修正（Bias Correction）]] — requires_in_adam
