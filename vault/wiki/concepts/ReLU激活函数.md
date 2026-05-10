---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 3
tags: ["机器学习", "深度学习", "激活函数"]
aliases: ["ReLU", "Rectified Linear Unit", "修正线性单元"]
relates_to: ["Sigmoid激活函数", "反向传播", "梯度消失", "AlexNet"]
supersedes: ["Sigmoid激活函数"]
---

# ReLU激活函数

## 概述 (50-200字符)
ReLU（Rectified Linear Unit）f(x) = max(0, x) 是现代深度学习默认的激活函数。正区间导数恒为 1，彻底解决了[[Sigmoid激活函数]]的[[梯度消失]]问题，[[计算]]简单且收敛速度快，2012 年 [[AlexNet]] 使其成为主流。

## 关键内容 (≥300字符, 用[[双链]])
1. **定义与导数**：f(x) = max(0, x)，当 x > 0 时 f(x) = x，否则 f(x) = 0。导数 f'(x) = 1 (x > 0) 或 0 (x ≤ 0)。正区间导数恒为 1 是其核心优势——在[[反向传播]]中，多层 ReLU 的梯度连乘不会衰减（1ⁿ = 1），从根本上解决了深层网络的[[梯度消失]]问题。
2. **对比 Sigmoid**：[[Sigmoid激活函数]]的导数最大值仅 0.25，多层相乘后 0.25ⁿ → 0，深层网络无法训练。ReLU [[计算]]也更简单（无需指数运算，只需阈值比较），训练速度显著提升。Sigmoid 输出范围 (0,1)，ReLU 输出范围 [0, +∞)，无上限。
3. **历史地位**：虽然 ReLU 形式早在 1960 年代就已提出，但直到 2012 年 [[Alex Krizhevsky|Krizhevsky]] 等人的 [[AlexNet]] 在 [[ImageNet]] 竞赛中取得突破性成果，ReLU 才成为深度学习社区的默认选择。[[AlexNet]] 的成功证明了简单激活函数在深层网络中的有效性。
4. **变体**：ReLU 存在一些已知问题（如"死亡 ReLU"——负区间梯度为 0 导致神经元永久失活），衍生出 Leaky ReLU、ELU、GELU 等变体。但标准 ReLU 因其简单性和有效性仍是大多数场景的首选。

## 来源
- [Learning Representations by Back-propagating Errors] — Rumelhart, Hinton & Williams, Nature 1986（作为 Sigmoid 的替代被提及）
- [raw/articles/ai-papers/machine-learning/02_backpropagation_1986.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[Sigmoid激活函数]] — supersedes
- [[反向传播]] — uses
- [[梯度消失]] — solves
- [[AlexNet]] — popularized_by
