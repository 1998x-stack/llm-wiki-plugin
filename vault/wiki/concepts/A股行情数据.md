---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [金融数据, 股票市场, A股, 经济学]
aliases: ["A股行情", "A股实时行情", "A股数据", "A股K线", "A股历史数据"]
relates_to:
  - target: "[[AKShare]]"
    type: provided_by
    confidence: 0.9
  - target: "[[Baostock]]"
    type: provided_by
    confidence: 0.85
  - target: "[[东方财富]]"
    type: sourced_from
    confidence: 0.8
  - target: "[[新浪财经]]"
    type: sourced_from
    confidence: 0.8
  - target: "[[北向资金]]"
    type: related_to
    confidence: 0.7
  - target: "[[龙虎榜]]"
    type: related_to
    confidence: 0.7
  - target: "[[融资融券]]"
    type: related_to
    confidence: 0.7
  - target: "[[AKQuant]]"
    type: used_in
    confidence: 0.7
  - target: "[[金融数据API对比分析]]"
    type: featured_in
    confidence: 0.75
  - target: "[[AKShare生产实践建议]]"
    type: subject_of
    confidence: 0.7
supersedes: null
---

# A股行情数据

## 概述
A股行情数据是指中国上海证券交易所和深圳证券交易所上市股票的实时及历史价格数据，包括开盘价、收盘价、最高价、最低价、成交量、成交额、涨跌幅等核心指标，是投资者进行技术分析和投资决策的重要依据。

## 关键内容

1. **数据维度**：包含实时行情快照、历史日K线、周K线、月K线、分钟K线等多种时间周期数据。每个数据点包含日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率等信息。

2. **数据来源**：主要来自官方交易所（上交所、深交所）以及各大财经门户网站如[[东方财富|东方财富网]]、[[新浪财经]]、[[同花顺]]等。此外，可通过专门的数据API获取，如[[AKShare]]和[[Baostock]]提供的[[Python]]接口。

3. **获取接口**：通过[[AKShare]]库的`stock_zh_a_hist()`函数可以获取指定股票的历史K线数据，`stock_zh_a_spot_em()`函数可获取全市场约5000只股票的实时快照，`stock_zh_a_minute()`函数提供实时分钟级别数据。[[Baostock]]也提供了相应的K线数据接口如`query_history_k_data_plus()`。

4. **复权机制**：包含不复权、前复权、后复权三种处理方式，用于消除股票分红、配股等事件对价格走势的影响，确保技术指标[[计算]]的准确性。

5. **数据应用**：广泛应用于量化分析、程序化交易、技术指标[[计算]]、回测系统等领域，是金融[[数据分析]]的基础。

6. **生产实践**：在实际应用中需要实现容错机制、批量处理和版本管理，以确保数据获取的稳定性和可靠性。

## 来源
- [[raw/assets/finance-knowledge/akshare-skill/SKILL.md]] — A股行情数据获取方法
- [[raw/assets/finance-knowledge/akshare.md]] — AKShare深度分析报告

## 相关
- [[AKShare]] — provided_by
- [[Baostock]] — provided_by
- [[北向资金]] — related_to
- [[龙虎榜]] — related_to
- [[融资融券]] — related_to
- [[东方财富]] — sourced_from
- [[新浪财经]] — sourced_from
- [[AKQuant]] — used_in
- [[金融数据API对比分析]] — featured_in
- [[AKShare生产实践建议]] — subject_of