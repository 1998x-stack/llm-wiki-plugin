---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [计量经济学, 时间序列分析, 协整理论]
aliases: ["Cointegration", "协整关系", "共整合"]
relates_to:
  - target: "[[Soren Johansen]]"
    type: developed_by
    confidence: 0.9
  - target: "[[Clive Granger]]"
    type: related_to
    confidence: 0.9
  - target: "[[Johansen检验]]"
    type: tested_by
    confidence: 0.9
  - target: "[[误差修正模型]]"
    type: connected_to
    confidence: 0.9
  - target: "[[伪回归]]"
    type: solves
    confidence: 0.9
supersedes: null
---

# 协整 (Cointegration)

## 概述
协整是时间序列分析中的重要概念，指两个或多个非平稳变量的某种线性组合是平稳的，揭示了变量之间的长期均衡关系。

## 关键内容

1. **基本定义**：
   - 两个(或多个)单整变量的某种线性组合是平稳的
   - 解决了非平稳变量回归中的"伪回归"问题
   - 允许在保持变量长期关系的同时分析其动态变化

2. **历史发展**：
   - 1987年Engle和Granger正式定义了协整概念，为此获得了2003年诺贝尔经济学奖
   - 1988年Soren Johansen提出基于最大似然估计的系统性检验框架

3. **核心意义**：
   - 解决了"差分丢失长期信息"与"直接回归产生伪回归"的两难困境
   - 允许对非平稳经济变量建立有意义的长期均衡模型
   - 为经济政策分析和金融建模提供了理论基础

4. **实际应用**：
   - 购买力平价理论的检验
   - 利率期限结构分析
   - 股票配对交易策略

## 来源
- [[10-johansen-1988-cointegration]] — 历史发展
- [[伪回归]] — 问题解决
- [[误差修正模型]] — 相关概念

## 相关
- [[Johansen检验]] — tested_by
- [[伪回归]] — solves
- [[误差修正模型]] — connected_to
- [[Soren Johansen]] — developed_by
- [[Clive Granger]] — related_to
- [[醉汉遛狗类比]] — explained_by