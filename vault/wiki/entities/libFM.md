---
type: entity
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 分解模型, 开源工具, CTR预估]
aliases: [libFM, Library for Factorization Machines]
relates_to:
  - {target: Factorization Machines, type: implements}
  - {target: Steffen Rendle, type: implements}
  - {target: xLearn, type: compares_to}
  - {target: CTR 预估, type: uses}
  - {target: 矩阵分解, type: uses}
supersedes: null
---

# libFM

## 概述
[[Steffen Rendle]] 开发的 [[Factorization Machines]] 开源 C++ 实现库，支持 SGD、ALS、MCMC 三种优化方法，是 FM 模型在工业界普及的核心工具。

## 关键内容

1. **功能特性**：完整实现了 [[Factorization Machines]] 模型，支持回归、二分类、排序三种任务类型，对应最小二乘损失、logit/hinge 损失、BPR 成对排序损失。
2. **优化方法**：提供三种优化[[算法]]——SGD（随机梯度下降，适合大规模在线学习）、ALS（交替最小二乘，回归任务稳定）、MCMC（[[马尔可夫链]]蒙特卡洛，[[托马斯·贝叶斯|贝叶斯]]推断可自动调节正则化强度）。
3. **线性复杂度**：利用 FM 的代数变换 $\frac{1}{2} \sum_{f=1}^{k} \left( (\sum_i v_{i,f} x_i)^2 - \sum_i v_{i,f}^2 x_i^2 \right)$，实现 $O(kn)$ 时间复杂度的前向[[计算]]和梯度更新，在稀疏数据下实际复杂度为 $O(k\bar{n})$。
4. **工业影响**：libFM 的开源发布极大推动了 FM 在推荐系统和 [[CTR 预估]]领域的工业应用，美团、阿里巴巴、华为、Twitter 等公司早期推荐/广告系统均基于 libFM 或参考其实现。
5. **配套论文**：Rendle 于 2012 年发表 *[[Factorization Machines]] with libFM*（ACM TIST, 3(3), 57），详细描述了 libFM 的设计原理、实现细节和使用方法。
6. **后续工具**：xLearn 是 libFM 的高性能后继者，进一步扩展了 FFM（Field-aware FM）的支持和分布式训练能力。

## 来源
- [Factorization Machines with libFM (Rendle 2012)](https://doi.org/10.1145/2168752.2168771)
- [Factorization Machines (Rendle 2010)](https://arxiv.org/abs/1209.3994)

## 相关
- [[Factorization Machines]] — 实现的模型
- [[Steffen Rendle]] — 开发者
- [[xLearn]] — 后继高性能工具
- [[CTR 预估]] — 主要应用场景
- [[矩阵分解]] — 支持的特例模型
