---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: ["机器学习", "深度学习", "优化", "优化器"]
aliases: ["Momentum", "动量法", "动量优化", "Momentum Optimizer"]
relates_to: ["Adam（自适应矩估计）", "RMSProp", "随机梯度下降（SGD）", "梯度消失"]
supersedes: null
---

# Momentum（动量）

## 概述 (50-200字符)
Momentum 为梯度下降引入"惯性"——梯度的指数移动平均。方向一致时加速，方向震荡时减速，有效加速收敛并抑制噪声。是 [[Adam（自适应矩估计）|Adam 优化器]]的一阶矩组件。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[算法]]**：mₜ = β·mₜ₋₁ + (1-β)·gₜ，θ ← θ - η·mₜ。其中 β 通常取 0.9，意味着当前更新 90% 来自历史动量、10% 来自当前梯度。一阶矩 mₜ 是梯度的指数移动平均（Exponential Moving Average, EMA）。
2. **直觉类比**：如同一个球在碗里滚动。当梯度方向一致时，动量持续累积，步子越迈越大（加速收敛）；当梯度方向震荡时（如损失曲面的狭长峡谷），正负动量相互抵消，步子缩小（抑制震荡）。这使 Momentum 能穿越[[梯度消失]]区域和[[鞍点（Saddle Point）]]。
3. **在 Adam 中的角色**：[[Adam（自适应矩估计）]]将 Momentum 作为一阶矩组件（β₁=0.9），与[[RMSProp]]的二阶矩结合，同时获得动量加速和自适应学习率的优势。Adam 的[[偏差修正（Bias Correction）|偏差修正]]机制专门解决了 Momentum 初始化时 m₀=0 导致的早期低估问题。
4. **与 SGD 对比**：SGD+Momentum 在 CNN（如 [[ImageNet]] 分类）训练中通常优于 Adam，能达到更好的最终精度。这是因为自适应学习率在训练末期可能引入不必要的震荡，而固定学习率配合动量有更稳定的收敛行为。

## 来源
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR 2015.] — Adam 论文中的 Momentum 组件
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读（AlexNet 使用 SGD+Momentum β=0.9）

## 相关
- [[Adam（自适应矩估计）]] — component_of
- [[RMSProp]] — combined_in_adam
- [[随机梯度下降（SGD）]] — improves
- [[偏差修正（Bias Correction）]] — requires
- [[鞍点（Saddle Point）]] — helps_escape
