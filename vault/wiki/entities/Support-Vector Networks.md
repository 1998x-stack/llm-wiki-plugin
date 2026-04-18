---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "论文", "分类算法"]
aliases: ["Support Vector Networks", "SVM论文", "Cortes Vapnik 1995"]
relates_to: ["支持向量机", "核技巧", "VC维理论"]
supersedes: null
---

# Support-Vector Networks

## 概述 (50-200字符)
[[支持向量机]]奠基性论文，由[[Corinna Cortes]]和[[Vladimir Vapnik]]于1995年发表于Machine Learning期刊。首次将SVM从线性扩展到非线性（[[核技巧]]），确立最大间隔分类理论。

## 关键内容 (≥300字符, 用[[双链]])
1. **历史背景**：1990年代神经网络陷入[[梯度消失]]、[[过拟合（Overfitting）|过拟合]]困境。Vapnik在[[贝尔实验室]]提出从[[统计学习理论]]出发直接推导最优分类器，而非在巨大函数空间中盲目搜索。
2. **核心贡献**：在[[VC维理论]]框架下，证明最大化分类间隔的分类器泛化能力最强。提出**硬间隔SVM**（线性可分）和**软间隔SVM**（含噪声，引入松弛变量ξᵢ和参数C）。
3. **[[核技巧]]引入**：将低维非线性不可分数据映射到高维空间，在高维中线性可分。关键突破：无需显式计算φ(x)，只需替换内积xᵢ·xⱼ→K(xᵢ,xⱼ)，实现非线性分类。
4. **历史影响**：1995-2012年间统治机器学习领域，在手写数字识别（MNIST）、文本分类、生物信息学、图像识别等领域超越当时最好方法。深度学习崛起前最强分类器。
5. **数学优雅性**：凸优化保证全局最优解，支持向量可解释，预测公式：ŷ=sign(Σᵢ αᵢyᵢK(xᵢ,x)+b)，仅依赖支持向量。

## 来源
- raw/articles/ai-papers/machine-learning/03_svm_1995.md — Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine learning, 20(3), 273–297.

## 相关
- [[支持向量机]] — implements
- [[核技巧]] — extends
- [[VC维理论]] — depends_on
- [[Vladimir Vapnik]] — authored_by
- [[Corinna Cortes]] — authored_by
