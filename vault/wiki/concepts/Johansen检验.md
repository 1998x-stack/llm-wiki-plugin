---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [计量经济学, 时间序列分析, 假设检验, 经济学]
aliases: ["Johansen Test", "Johansen协整检验"]
relates_to:
  - target: "[[Soren Johansen]]"
    type: created_by
    confidence: 1.0
  - target: "[[协整 (Cointegration)]]"
    type: tests
    confidence: 1.0
  - target: "[[向量自回归模型]]"
    type: based_on
    confidence: 0.9
  - target: "[[最大似然估计 (Maximum Likelihood Estimation)]]"
    type: uses
    confidence: 0.9
  - target: "[[迹检验]]"
    type: includes
    confidence: 0.9
  - target: "[[最大特征值检验]]"
    type: includes
    confidence: 0.9
supersedes: null
---

# Johansen检验

## 概述
Johansen检验是用于检验多个[[Time Series Analysis|时间序列]]变量之间[[协整 (Cointegration)|协整关系]]的统计方法，由[[Soren Johansen]]在1988年提出。

## 关键内容

1. **核心思想**：
   - 基于[[向量自回归模型]](VAR)框架
   - 通过确定[[矩阵]]Π的秩来判断[[协整 (Cointegration)|协整关系]]的数量
   - 如果Π的秩为零，变量之间没有[[协整 (Cointegration)|协整关系]]；如果秩为r(0<r<p)，则存在恰好r个[[协整 (Cointegration)|协整关系]]

2. **方法优势**：
   - 可以发现所有r个[[协整 (Cointegration)|协整关系]]（相比Engle-Granger方法只能发现一个）
   - 天然适合多变量系统
   - 使用[[最大似然原理|最大似然估计]]，渐近最优
   - 不受变量排序影响
   - 可以灵活检验各种参数约束

3. **检验统计量**：
   - [[迹检验]]([[迹检验|Trace Test]])：检验原假设"至多有r个[[协整 (Cointegration)|协整关系]]"
   - [[最大特征值检验]]([[最大特征值检验|Maximum Eigenvalue Test]])：检验原假设"恰好有r个[[协整 (Cointegration)|协整关系]]"

4. **应用场景**：
   - 购买力平价理论检验
   - 利率期限[[结构力学|结构分析]]
   - 股票配对交易策略开发

## 来源
- [[10-johansen-1988-cointegration]] — 基本原理
- [[Soren Johansen]] — 创立者

## 相关
- [[协整 (Cointegration)]] — tests
- [[Soren Johansen]] — created_by
- [[向量自回归模型]] — based_on
- [[迹检验]] — includes
- [[最大特征值检验]] — includes
- [[最大似然估计 (Maximum Likelihood Estimation)]] — uses
- [[误差修正模型]] — connected_to