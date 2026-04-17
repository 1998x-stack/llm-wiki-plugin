---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, 深度学习, Google]
aliases: [DCN, Deep & Cross Network]
relates_to:
  - {target: DeepFM, type: compares_to}
  - {target: 特征交叉, type: uses}
  - {target: CTR 预估, type: implements}
supersedes: null
---

# DCN

## 概述
[[Google]] 于 2017 提出的 [[CTR 预估]]模型，通过 Cross Network 显式建模任意阶[[特征交叉]]，与 [[DeepFM]] 同期但采用不同的显式交叉策略。

## 关键内容

1. **Cross Network**：提出 Cross Network（交叉网络），通过逐层交叉操作显式建模任意阶[[特征交叉|特征交互]]，与 [[DeepFM]] 依赖 FM 二阶 + DNN 隐式高阶的策略不同。
2. **Deep & Cross 架构**：采用 Cross Network（显式交叉）+ Deep Network（隐式交叉）的并行架构，与 [[DeepFM]] 的 FM + DNN 并行架构设计理念相似但实现不同。
3. **DCN V2**：2020 年推出 DCN V2，引入[[矩阵]]核 CrossNet 和 MoE（[[Mixture-of-Experts|Mixture of Experts]]），进一步提升了模型的表达能力和效率。
4. **CTR 模型演化链**：在 CTR 模型演化史上，DCN 与 [[DeepFM]] 处于同一分叉点，确立了"显式交叉组件 + DNN"的标准[[规范化理论|范式]]。

## 来源
- [Deep & Cross Network (Google 2017)](https://arxiv.org/abs/1708.05123)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[DeepFM]] — 同期并行工作
- [[xDeepFM]] — 后续显式交叉改进
- [[Wide & Deep]] — Google 前作
- [[CTR 预估]] — 应用场景
