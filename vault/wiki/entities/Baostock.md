---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["Baostock", "证券宝", "中国 A 股历史数据平台"]
relates_to:
  - target: "[[AKShare]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Alpha Vantage]]"
    type: compares_to
    confidence: 0.7
  - target: "[[yfinance]]"
    type: compares_to
    confidence: 0.75
supersedes: null
entity_type: tool
---

# Baostock

## 概述
Baostock（证券宝）是中国 A 股免费历史数据平台，提供 Python SDK，无需注册、无调用频率限制，K 线数据从 1990-12-19 至今，财务数据从 2007 年起，是 A 股历史数据研究的可靠选择。

## 关键内容

1. **项目概览**：版本 0.8.9，Python ≥ 3.6（64-bit），BSD License，官方交易所数据源（上交所/深交所）。

2. **行情数据**：日 K 线（每日 17:30 更新，从 1990-12-19）、周 K 线、月 K 线、分钟 K 线（1/5/15/30/60min，次日 11:00 更新）、指数日线。支持前复权/后复权/不复权。

3. **基本面数据**：季度盈利/营运/成长/偿债能力、杜邦分析（5 因子分解）、现金流量、业绩预告（2003 年起）、业绩快报（2006 年起）。

4. **市场结构数据**：全量股票列表、历史交易日历、上证 50/沪深 300/中证 500 成分股（每周一更新）、行业分类（申万一级）、历史分红送配、复权因子。

5. **优势**：完全免费、无需注册、无 API Key、无调用频率限制、历史数据最完整（从 1990 年）。

## 来源
- [[baostock]] — Baostock 深度分析报告

## 相关
- [[AKShare]] — compares_to
- [[Alpha Vantage]] — compares_to
- [[yfinance]] — compares_to
