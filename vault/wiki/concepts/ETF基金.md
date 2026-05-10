---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["基金", "投资品种", "场内基金", "ETF"]
aliases: ["ETF", "ETF基金", "交易型开放式指数基金", "场内基金", "ETF净值"]
relates_to:
  - target: "[[AKShare]]"
    type: provided_by
    confidence: 0.9
  - target: "[[基金]]"
    type: subtype_of
    confidence: 0.9
  - target: "[[指数基金]]"
    type: subtype_of
    confidence: 0.9
  - target: "[[A股行情数据]]"
    type: related_to
    confidence: 0.7
  - target: "[[基金净值]]"
    type: includes
    confidence: 0.9
  - target: "[[基金持仓]]"
    type: includes
    confidence: 0.8
  - target: "[[AKQuant]]"
    type: used_in
    confidence: 0.7
  - target: "[[金融数据API对比分析]]"
    type: featured_in
    confidence: 0.75
supersedes: null
---

# ETF基金

## 概述
ETF（Exchange-Traded Fund，交易型开放式指数基金）是一种在交易所上市交易的基金，兼具开放式基金可申购赎回和封闭式基金可交易的特点，能够跟踪特定指数、行业、商品或其他资产的表现。

## 关键内容

1. **数据内容**：包括场内ETF实时行情、ETF历史净值、场外基金每日净值、基金十大重仓股持仓情况、公募基金规模排行等。涵盖代码、名称、最新价、涨跌幅、跟踪标的等信息。

2. **获取方法**：通过[[AKShare]]库的`fund_etf_spot_em()`函数可获取场内ETF实时行情，`fund_etf_hist_em()`函数可获取ETF历史净值，`fund_open_fund_daily_em()`函数可获取场外基金每日净值，`fund_portfolio_hold_em()`函数可获取基金持仓情况。

3. **分类**：按投资标的可分为股票型ETF、债券型ETF、商品型ETF、货币型ETF等；按跟踪指数可分为宽基指数ETF、行业主题ETF、策略指数ETF等。

4. **特点**：交易灵活（可在交易时间内随时买卖）、费用较低（管理费和托管费通常低于主动型基金）、透明度高（持仓信息公开透明）、分散风险（跟踪指数实现分散投资）。

5. **应用场景**：适合指数化投资策略、资产[[Configuration|配置]]、短期交易等多种投资需求，是重要的投资工具之一。

6. **量化应用**：在量化投资中，ETF基金数据用于构建投资组合、风险对冲策略、套利策略等多种策略。

## 来源
- [[raw/assets/finance-knowledge/akshare-skill/SKILL.md]] — ETF基金数据获取方法
- [[raw/assets/finance-knowledge/akshare.md]] — AKShare深度分析报告

## 相关
- [[AKShare]] — provided_by
- [[基金]] — subtype_of
- [[指数基金]] — subtype_of
- [[A股行情数据]] — related_to
- [[基金净值]] — includes
- [[基金持仓]] — includes
- [[AKQuant]] — used_in
- [[金融数据API对比分析]] — featured_in