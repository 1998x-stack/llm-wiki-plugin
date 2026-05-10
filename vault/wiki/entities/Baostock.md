---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["金融数据", "Python库", "A股数据", "免费API"]
aliases: ["baostock", "Baostock SDK", "中国A股数据平台", "证券宝"]
relates_to:
  - target: "[[A股行情数据]]"
    type: provides
    confidence: 0.8
  - target: "[[AKShare]]"
    type: compares_to
    confidence: 0.75
  - target: "[[Tushare Pro]]"
    type: compares_to
    confidence: 0.7
  - target: "[[yfinance]]"
    type: compares_to
    confidence: 0.75
  - target: "[[宏观经济数据]]"
    type: provides
    confidence: 0.8
entity_type: tool
supersedes: null
---

# Baostock

## 概述
Baostock（证券宝）是中国 A 股免费历史数据平台，提供 [[Python]] SDK，无需注册、无调用频率限制，K 线数据从 1990-12-19 至今，财务数据从 2007 年起，是 A 股历史数据研究的可靠选择。

## 关键内容

1. **核心特性**：
   - 完全免费，无需注册，无API Key需求，无调用限制
   - 数据源自官方交易所（上交所/深交所），保证权威性
   - 历史数据深度长，A股日线数据可追溯至1990年12月19日
   - 包含行情数据、基本面数据、市场结构数据和宏观数据

2. **数据覆盖范围**：
   - 行情数据：日K线（每日17:30更新）、周K线、月K线、分钟K线（1/5/15/30/60min，次日11:00更新）、指数日线。支持前复权/后复权/不复权
   - 基本面数据：季度财报（ROE/ROA/净利润率、营运能力、成长能力、偿债能力等）、杜邦分析（5因子分解）、现金流量、业绩预告（2003年起）、业绩快报（2006年起）
   - 市场结构数据：全量股票列表、历史交易日历、上证50/沪深300/中证500成分股（每周一更新）、行业分类（申万一级）、历史分红送配、复权因子
   - 宏观数据：存款基准利率、贷款基准利率、存款准备金率、M0/M1/M2月度/年度数据、SHIBOR利率等

3. **技术架构**：
   - 采用TCP长连接会话机制，需显式登录/登出（bs.login()/bs.logout()）
   - 使用分页迭代方式读取数据（rs.next()），适合大数据量处理
   - 返回自定义ResultSet格式，需手动转换为DataFrame
   - 仅支持[[Python|Python语言]]，不提供HTTP API供其他语言直接调用
   - SDK版本停留在0.8.9，2019年后无大版本更新

4. **使用场景**：
   - A股量化策略回测（日频/周频）
   - 基本面选股模型（ROE/ROA/成长性筛选）
   - 宏观-行业-个股三层联动分析
   - 指数成分股历史变动研究
   - 学术研究/毕业论文数据获取

## 来源
- [[raw/assets/finance-knowledge/baostock.md]] — Baostock深度分析报告

## 相关
- [[A股行情数据]] — provides
- [[AKShare]] — compares_to
- [[Tushare Pro]] — compares_to
- [[yfinance]] — compares_to
- [[宏观经济数据]] — provides
