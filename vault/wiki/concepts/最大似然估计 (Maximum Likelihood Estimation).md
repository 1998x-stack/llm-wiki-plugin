---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [计量经济学, 统计学, 参数估计]
aliases: ["Maximum Likelihood Estimation", "MLE", "最大似然法"]
relates_to:
  - target: "[[Johansen检验]]"
    type: used_by
    confidence: 0.9
  - target: "[[Soren Johansen]]"
    type: employed_by
    confidence: 0.9
  - target: "[[协整 (Cointegration)]]"
    type: applied_to
    confidence: 0.8
supersedes: null
---

# 最大似然估计 (Maximum Likelihood Estimation)

## 概述
最大似然估计是一种常用的参数估计方法，通过最大化似然函数来估计模型参数。

## 关键内容

1. **基本原理**：
   - 选择使观测数据出现概率最大的参数值作为估计值
   - 基于已知的概率分布形式，通过样本数据推断总体参数

2. **在协整分析中的应用**：
   - Johansen方法采用最大似然估计，相比于Engle-Granger的OLS方法更加高效
   - Johansen证明协整检验问题可转化为求解广义特征值问题
   - 特征值按从大到小排列，每个对应一个可能的协整向量

3. **优势**：
   - 渐近最优的估计性质
   - 可以同时估计多个协整向量
   - 允许进行参数约束的统计检验

## 来源
- [[10-johansen-1988-cointegration]] — 方法描述
- [[Johansen检验]] — 应用

## 相关
- [[Johansen检验]] — used_by
- [[Soren Johansen]] — employed_by
- [[协整 (Cointegration)]] — applied_to
- [[迹检验]] — method_used_in
- [[最大特征值检验]] — method_used_in