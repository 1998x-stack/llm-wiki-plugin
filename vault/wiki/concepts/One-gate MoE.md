---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 多任务学习, 深度学习, 架构模式]
aliases: [OMoE, One-gate Mixture-of-Experts, 单门控混合专家网络]
relates_to:
  - target: "[[MMoE]]"
    type: extends
  - target: "[[Mixture-of-Experts]]"
    type: extends
  - target: "[[Shared-Bottom]]"
    type: compares_to
  - target: "[[多任务学习]]"
    type: part_of
supersedes: null
---

# One-gate MoE

## 概述
One-gate MoE (OMoE) 是多任务学习中混合专家模型的一种架构变体，使用单一门控网络控制多个专家网络，为 MMoE 架构的前身和对比基准。

## 关键内容

### 核心架构
- **专家网络**：多个专家网络接收同一份输入 x，各自独立计算输出：f_1(x), f_2(x), ..., f_n(x)
- **单一门控网络**：所有任务共享同一个门控网络，根据输入 x 计算一组权重：g(x) = softmax(Wx)
- **输出融合**：所有任务接收门控网络产出的同一份专家加权组合，然后输入各自的塔网络
- 数学表示：y = Σ g(x)_i * f_i(x)，其中 f_i(x) 为第 i 个专家输出，g(x)_i 为门控权重

### 与 MMoE 的区别
- **门控共享**：OMoE 中所有任务共享同一个门控网络，MMoE 为每个任务配备独立门控网络
- **灵活性**：OMoE 的专家选择策略对所有任务是统一的，MMoE 允许任务个性化选择专家组合
- **任务关系建模**：OMoE 提供有限的任务关系建模能力，MMoE 提供显式的任务关系建模

### 优势
- **参数效率**：相比 Shared-Bottom，OMoE 将底层网络模块化，允许不同输入激活不同专家组合
- **结构改进**：相比 Shared-Bottom，OMoE 提供了更好的任务表示灵活性
- **计算效率**：单一门控网络保持了计算效率

### 局限性
- **统一门控限制**：所有任务看到相同的专家组合权重，无法体现不同任务对底层特征的差异化需求
- **任务特定性不足**：无法根据任务特性定制专家选择策略
- **灵活性受限**：相比 MMoE，缺乏对任务关系的精细化建模能力

### 历史意义
- MMoE 架构的直接前身，作为共享参数和完全独立模型之间的中间方案
- 为 MMoE 的创新提供了对比基准，证明了独立门控网络的价值
- 验证了在多任务学习中使用混合专家模型的可行性

## 来源
- [[MMoE 论文]] — Ma et al., KDD 2018
- raw/books/推荐系统/14-mmoe.md — 深度解读文章

## 相关
- [[MMoE]] — 基于 OMoE 的改进版本，提供独立门控
- [[Mixture-of-Experts]] — OMoE 的基础架构来源
- [[多任务学习]] — OMoE 的应用领域
- [[Shared-Bottom]] — 相比 OMoE 更简单的多任务学习架构