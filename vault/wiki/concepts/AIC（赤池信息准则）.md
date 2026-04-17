---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论"]
aliases: ["Akaike Information Criterion", "赤池信息量准则", "AIC"]
relates_to:
  - target: "[[ARIMA 模型]]"
    type: uses
    confidence: 0.9
  - target: "[[最大似然原理]]"
    type: depends_on
    confidence: 0.9
  - target: "[[BIC（贝叶斯信息准则）]]"
    type: compares_to
    confidence: 0.85
supersedes: null
---

# AIC（赤池信息准则）

## 概述
赤池信息量准则由日本统计学家赤池弘次于 1974 年提出，通过平衡模型拟合优度和复杂度来评估统计模型的相对质量，是统计学领域被引用最多的准则之一，彻底改变了模型选择的方法论。

## 关键内容

1. **历史背景**：1974 年前，模型选择依赖假设检验（如似然比检验），存在只能比较嵌套模型、阈值任意性、无法同时比较多个模型、忽视预测能力等根本缺陷。赤池弘次从[[信息论]]角度给出了全新思路。

2. **核心公式**：AIC = 2k - 2ln(L)，其中 k 是模型参数个数，L 是最大似然值。AIC 值越小模型越好。其本质是对模型预测能力的估计——在拟合优度（-2ln(L)）和复杂度惩罚（2k）之间取得平衡。

3. **理论基础**：赤池从 Kullback-Leibler 散度出发，证明 AIC 是对模型预测误差的渐近无偏估计。这把"[[Occam剃刀|奥卡姆剃刀]]"有了精确的数学表达。

4. **影响**：被广泛应用于时间序列分析（[[ARIMA 模型|ARIMA]] 阶数选择）、机器学习模型选择、生态学、经济学等领域。衍生出 AICc（小样本修正）、BIC 等变体。

## 来源
- [[07-akaike-1974-aic]] — 用一把"奥卡姆剃刀"丈量统计模型

## 相关
- [[ARIMA 模型]] — uses
- [[最大似然原理]] — depends_on
- [[BIC（贝叶斯信息准则）]] — compares_to
