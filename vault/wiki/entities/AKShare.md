---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["AKShare", "开源财经数据接口库", "东方财富数据接口"]
relates_to:
  - target: "[[Baostock]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Alpha Vantage]]"
    type: compares_to
    confidence: 0.75
  - target: "[[yfinance]]"
    type: compares_to
    confidence: 0.75
supersedes: null
entity_type: tool
---

# AKShare

## 概述
AKShare 是开源全品类财经数据接口库（Python），提供 1000+ 接口覆盖 37 个数据分类，数据源包括东方财富、新浪财经、同花顺等，完全免费无需注册，覆盖 A 股、港股、美股、期货、期权、债券、外汇、基金、宏观等市场。

## 关键内容

1. **项目概览**：版本 1.18.48（2025 持续更新），Python ≥ 3.6（64-bit），MIT License，GitHub Stars 10,000+。

2. **数据源命名约定**：函数后缀标识数据来源——`_em`（东方财富）、`_sina`（新浪财经）、`_ths`（同花顺）、`_js`（金十数据）、`_bs`（[[Baostock]]）、`_qq`（腾讯财经）。

3. **模块结构**：stock（A 股核心行情）、stock_feature（龙虎榜/融资融券/北向资金）、economic（宏观经济）、fund（公募基金/ETF）、bond（债券）、futures（期货）、option（期权）、forex（外汇）、crypto（数字货币）、index（指数）、news（财经新闻/舆情）。

4. **优势**：完全免费、无需注册、无 API Key、接口数量最多（1,046+）、覆盖市场最广。

## 来源
- [[akshare]] — AKShare 深度分析报告

## 相关
- [[Baostock]] — compares_to
- [[Alpha Vantage]] — compares_to
- [[yfinance]] — compares_to
