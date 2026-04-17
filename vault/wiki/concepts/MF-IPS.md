---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 因果推断, 去偏, 训练方法]
aliases: [MF-IPS, IPS-based Matrix Factorization]
relates_to:
  - {target: 矩阵分解, type: extends}
  - {target: 逆倾向评分, type: uses}
  - {target: 倾向性评分, type: uses}
  - {target: MNAR, type: compares_to}
  - {target: MCAR, type: compares_to}
supersedes: null
---

# MF-IPS

## 概述
基于 IPS 的[[矩阵分解]]（MF-IPS）将逆倾向加权嵌入经验风险最小化框架，在 MNAR 数据上实现近似无偏的[[矩阵分解]]训练。

## 关键内容

1. **核心思想**：传统[[矩阵分解]]在观测到的评分上最小化均方误差，等价于在 MCAR 假设下的经验风险最小化（ERM）。MF-IPS 用 IPS 估计器替代朴素的均方误差，从而在 MNAR 数据上实现近似无偏的 ERM。

2. **优化目标**：$\hat{Y}^* = \arg\min_{\hat{Y} \in \mathcal{H}} \hat{R}_{IPS}(\hat{Y}) + \lambda \cdot \text{reg}(\hat{Y})$，其中 $\mathcal{H}$ 是[[矩阵分解]]模型的假设空间，$\lambda \cdot \text{reg}(\hat{Y})$ 是正则化项。

3. **理论保证**：[[Tobias Schnabel]] 等人推导了泛化误差界（generalization error bound），证明了 IPS-ERM 框架的统计学习理论保证。

4. **与传统的关**：当所有 [[倾向性评分]] 相等时（即 MCAR），MF-IPS 退化为传统的[[矩阵分解]]。这说明传统方法是 MF-IPS 在特殊假设下的特例。

5. **实验结果**：在 [[Yahoo! R3]] 和 Coat Shopping 数据集上，MF-IPS 显著优于所有基线方法（MF-Naive、HL-MAR、HL-MNAR），配对 t 检验 p < 0.001。MF-IPS 的性能甚至超过了计算复杂度远高于它的联合似然方法（HL-MNAR）。

6. **关键启示**：一个概念上简单、计算上高效的方法（IPS 加权的[[矩阵分解]]），通过正确地处理偏差，可以胜过复杂的联合概率模型。

7. **局限性**：MF-IPS 主要关注 [[显式反馈]]（评分）场景。现代推荐系统越来越多地依赖 [[隐式反馈]]（点击、浏览、购买），[[隐式反馈]]中的偏差模式更加复杂。

## 来源
- [Recommendations as Treatments (Schnabel et al., ICML 2016)](https://arxiv.org/abs/1602.05352)

## 相关
- [[矩阵分解]] — MF-IPS 的基础模型
- [[逆倾向评分]] — MF-IPS 的核心加权机制
- [[倾向性评分]] — MF-IPS 的输入
- MNAR — MF-IPS 适用的数据机制
- MCAR — MCAR 下 MF-IPS 退化为传统矩阵分解
- [[Yahoo! R3]] — 验证 MF-IPS 效果的数据集
