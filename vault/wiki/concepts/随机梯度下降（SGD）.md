---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "优化", "优化器"]
aliases: ["SGD", "Stochastic Gradient Descent", "随机梯度下降法", "小批量梯度下降"]
relates_to: ["Adam（自适应矩估计）", "Momentum（动量）", "反向传播", "学习率调度"]
supersedes: null
---

# 随机梯度下降（SGD）

## 概述 (50-200字符)
SGD 是最基础的神经网络优化算法：θ ← θ - η·∇L(θ)。使用 mini-batch 梯度近似全梯度，简单但存在学习率难选、鞍点停滞等痛点。配合动量仍是 CNN 训练的首选。

## 关键内容 (≥300字符, 用[[双链]])
1. **基本形式**：θ ← θ - η·∇L(θ)，其中 η 是学习率，∇L(θ) 是 mini-batch 上的损失梯度。每次迭代只使用一小批样本（如 32/64/256）计算梯度，而非全部数据。这使每次更新快速但有噪声——噪声既是缺点（震荡），也是优点（帮助逃离[[鞍点（Saddle Point）]]）。
2. **四大痛点**：(a) 学习率 η 难以选取——太大震荡不收敛，太小收敛极慢；(b) 所有参数共用同一学习率，无法适应梯度尺度差异（如[[词嵌入（Word Embedding）|词嵌入]]中高频词与低频词）；(c) [[鞍点（Saddle Point）]]处梯度趋零，更新停滞；(d) 不同层参数量级相差千倍，统一 η 无法兼顾。
3. **SGD+[[Momentum（动量）|Momentum]]**：加入[[Momentum（动量）]]后（vₜ = β·vₜ₋₁ + gₜ, θ ← θ - η·vₜ），SGD 在 CNN（如 [[ImageNet]] 分类）训练中通常优于自适应方法，能达到更好的最终精度。配合学习率调度（Step Decay、Cosine Annealing）和[[Batch Normalization]]，SGD+[[Momentum（动量）|Momentum]] 仍是计算机视觉领域的标准选择。
4. **与 Adam 的对比**：[[Adam（自适应矩估计）]]收敛更快、默认参数开箱即用，适合快速实验和 NLP/[[Transformer 架构|Transformer]] 场景。但 SGD+[[Momentum（动量）|Momentum]] 在充分调参后往往能达到更好的泛化性能——自适应方法的有效学习率在训练末期可能引入不必要的震荡。实践中常见策略：前期用 Adam 快速收敛，末期切换到 SGD 精细调优。

## 来源
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR 2015.] — Adam 论文中 SGD 的局限性分析
- [raw/articles/ai-papers/machine-learning/11_adam_2014.md] — 源文件

## 相关
- [[Adam（自适应矩估计）]] — supersedes_in_practice
- [[Momentum（动量）]] — improves_with
- [[反向传播]] — uses_gradients_from
- [[学习率调度]] — requires_for_convergence
- [[Batch Normalization]] — often_paired_with
- [[鞍点（Saddle Point）]] — vulnerable_to
