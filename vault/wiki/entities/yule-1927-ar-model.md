---
type: entity
entity_type: paper
status: active
confidence: 1.0
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [时间序列分析, 自回归模型, 统计学]
aliases: ["On a Method of Investigating Periodicities in Disturbed Series", "Investigating Periodicities in Disturbed Series", "Yule 1927", "On a Method of Investigating Periodicities in Disturbed Series, with Special Reference to Wolfer's Sunspot Numbers"]
relates_to:
  - target: "[[George Udny Yule]]"
    type: author
    confidence: 1.0
  - target: "[[自回归模型]]"
    type: implements
    confidence: 1.0
  - target: "[[太阳黑子]]"
    type: relates_to
    confidence: 0.9
  - target: "[[Yule-Walker方程]]"
    type: implements
    confidence: 1.0
  - target: "[[Eugen Slutsky]]"
    type: compares_to
    confidence: 0.8
  - target: "[[时间序列分析]]"
    type: implements
    confidence: 1.0
  - target: "[[周期图法]]"
    type: contrasts_with
    confidence: 0.9
  - target: "[[Gilbert Walker]]"
    type: relates_to
    confidence: 0.7
  - target: "[[伪相关]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# yule-1927-ar-model

## 概述
[[George Udny Yule]]于1927年发表的论文《On a Method of Investigating Periodicities in Disturbed Series, with Special Reference to [[太阳黑子|Wolfer's Sunspot Numbers]]》，首次提出了[[自回归模型]]，是现代[[时间序列分析]]的基石。

## 关键内容

1. **研究动机**：
   - 研究[[太阳黑子|太阳黑子数]]据中"周期性"是真实节律还是随机扰动制造的幻觉
   - 对比传统[[周期图法]]与新型[[AR 模型（自回归模型）|自回归]]方法的效果
   - 针对Arthur Schuster的[[周期图法]]在处理"野性"数据时的不足

2. **核心创新**：
   - [[区分]]两类受扰序列：叠加噪声的周期（Type I）与扰动作用于机制本身（Type II）
   - 提出[[自回归模型]]，特别是二阶[[自回归模型]]AR(2)：今年的[[太阳黑子|太阳黑子数]] = a × 去年的数值 + b × 前年的数值 + 随机冲击
   - 建立[[Yule-Walker方程]]，连接自相关系数与AR参数
   - 通过钟摆类比生动说明：被小孩随机弹击的钟摆对应[[太阳黑子|太阳黑子数]]据

3. **理论突破**：
   - 证明了AR(2)模型与[[阻尼谐振子]]的微分方程离散化形式一致
   - 揭示深层规律：在随机力驱动下，任何具有"惯性"和"回复力"的系统都会表现出类似周期性的振荡行为
   - 表明即使系统中不存在确定性周期，也可能表现出类似周期性的振荡

4. **历史背景**：
   - 20世纪20年代统计学的重大转折期
   - Yule在1926年发表了关于"伪相关"的重要论文，揭示[[Time Series Analysis|时间序列]]中的虚假相关现象
   - 传统方法（[[周期图法]]）在处理不稳定的[[太阳黑子]]周期时效果不佳

5. **历史意义**：
   - 现代[[时间序列分析]]的基石
   - 与[[Eugen Slutsky]]同年独立发表的滑动平均方法形成完美互补
   - 两条发展路线（AR和MA）最终在1970年发展为[[ARIMA]]框架
   - Yule[[区分]]了两类受扰序列：Yule发展[[AR 模型（自回归模型）|自回归]]方法，Slutsky发展滑动平均方法

6. **现代影响**：
   - 每次手机通话都在每10微秒求解一次[[Yule-Walker方程]]
   - 广泛应用于语音编码、金融预测、气象预报、地震学、脑科学等领域
   - 为信号处理和[[时间序列分析]]奠定了数学基础

## 来源
- [[01-yule-1927-ar-model]] — 源文件
- [[George Udny Yule]] — 研究者介绍

## 相关
- [[George Udny Yule]] — author
- [[自回归模型]] — implements
- [[太阳黑子]] — relates_to
- [[Yule-Walker方程]] — implements
- [[Eugen Slutsky]] — compares_to
- [[时间序列分析]] — relates_to
- [[周期图法]] — contrasts_with
- [[阻尼谐振子]] — relates_to
- [[伪相关]] — relates_to