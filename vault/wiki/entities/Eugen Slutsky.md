---
type: entity
entity_type: person
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [统计学家, 经济学家, 时间序列分析, 经济学]
aliases: ["Eugen Slutsky", "尤金·斯卢茨基"]
relates_to:
  - target: "[[George Udny Yule]]"
    type: compares_to
    confidence: 0.9
  - target: "[[时间序列分析]]"
    type: contributes_to
    confidence: 0.9
  - target: "[[滑动平均模型]]"
    type: implements
    confidence: 0.9
  - target: "[[yule-1927-ar-model]]"
    type: relates_to
    confidence: 0.9
  - target: "[[ARIMA模型]]"
    type: contributes_to
    confidence: 0.9
  - target: "[[伪相关]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Eugen Slutsky

## 概述
俄国统计学家和经济学家，独立于Yule提出了滑动平均方法，与Yule的工作共同奠定现代[[时间序列分析]]基础。

## 关键内容

1. **主要贡献**：
   - **滑动平均方法**（1927）：与Yule同年独立发表论文《The Summation of Random Causes as the Source of Cyclic Processes》，发展了滑动平均（MA）方法
   - **斯卢茨基效应**：在经济学中提出消费者需求理论的重要概念
   - **随机过程理论**：展示了对随机序列取滑动平均也能产生逼真的"周期"

2. **与[[时间序列分析]]的关系**：
   - 与Yule形成完美互补：Yule发展[[AR 模型（自回归模型）|自回归]]（AR）方法，Slutsky发展滑动平均（MA）方法
   - Slutsy证明了，对一列完全随机的数字反复做滑动平均，就能得到看起来和经济周期几乎一模一样的波浪形曲线
   - 这意味着经济周期可能根本不需要什么深层的"真实原因"——纯粹的随机冲击经过经济系统的传导，就足以产生繁荣与衰退的交替
   - 与Yule的工作共同构成了[[时间序列分析]]的理论基础

3. **与Yule工作的对比**：
   - Yule通过[[太阳黑子|太阳黑子数]]据研究[[AR 模型（自回归模型）|自回归]]方法，关注"用过去预测现在"
   - Slutsky通过随机序列滑动平均研究，展示随机过程如何产生周期性幻觉
   - 两者工作在同一年（1927年）发表，为[[时间序列分析]]奠定了两大基石

4. **历史意义**：
   - 与Yule的工作共同构成[[时间序列分析]]的理论基础
   - 两条发展线索（AR和MA）在此后数十年间各自发展，最终在1970年合流为[[ARIMA]]框架
   - 他的发现对经济学理论产生了深刻影响，挑战了经济周期需要深层原因的传统观点

5. **对经济理论的贡献**：
   - 揭示了经济周期可能是随机冲击在系统中传递的结果
   - 为宏观经济分析提供了新的视角
   - 影响了后来的经济建模方法

## 来源
- [[yule-1927-ar-model]] — 历史背景与贡献
- [[时间序列分析]] — 相关理论

## 相关
- [[时间序列分析]] — relates_to
- [[滑动平均模型]] — implements
- [[George Udny Yule]] — compares_to
- [[ARIMA模型]] — extends
- [[伪相关]] — relates_to