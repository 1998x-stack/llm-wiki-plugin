---
type: entity
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["工具与框架", "财经数据", "Python库"]
aliases: ["AKShare", "开源财经数据接口库", "AKShare Python库", "akshare"]
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
  - target: "[[A股行情数据]]"
    type: provides_data_for
    confidence: 0.9
  - target: "[[北向资金]]"
    type: provides_data_for
    confidence: 0.9
  - target: "[[龙虎榜]]"
    type: provides_data_for
    confidence: 0.9
  - target: "[[融资融券]]"
    type: provides_data_for
    confidence: 0.9
  - target: "[[ETF基金]]"
    type: provides_data_for
    confidence: 0.85
  - target: "[[宏观经济数据]]"
    type: provides_data_for
    confidence: 0.85
  - target: "[[期货数据]]"
    type: provides_data_for
    confidence: 0.85
  - target: "[[东方财富]]"
    type: uses
    confidence: 0.8
  - target: "[[新浪财经]]"
    type: uses
    confidence: 0.8
  - target: "[[同花顺]]"
    type: uses
    confidence: 0.8
  - target: "[[AKTools]]"
    type: extends
    confidence: 0.7
  - target: "[[AKQuant]]"
    type: integrates_with
    confidence: 0.75
supersedes: null
entity_type: tool
---

# AKShare

## 概述
AKShare 是 [[Python]] 财经数据库中接口最广的开源库，拥有 1046+ 函数，覆盖 A 股、港股、美股、[[期货数据|期货]]、期权、债券、外汇、基金、宏观经济、数字货币、国际[[期货数据|期货]]等多个领域。完全免费，无需注册，持续高频迭代（2025 年仍活跃维护）。

## 关键内容

1. **安装方式**：
   ```bash
   pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com --upgrade
   ```

2. **数据源命名约定**：函数后缀标识数据来源——`_em`（东方财富，数据最完整实时性好）、`_sina`（新浪财经，实时行情为主）、`_ths`（同花顺，机构数据为主）、`_js`（金十数据，宏观/外汇为主）、`_bs`（证券宝，历史数据）。

3. **A股行情数据**：`stock_zh_a_hist()` 获取历史K线数据，`stock_zh_a_spot_em()` 获取全市场实时快照（约5000只股票），`stock_zh_a_minute()` 获取实时分钟数据。

4. **北向资金数据**：`stock_hsgt_north_net_flow_in_em()` 获取当日北向资金净流入，`stock_hsgt_hist_em()` 获取历史北向资金趋势，`stock_hsgt_top10_em()` 获取沪股通/深股通十大成交活跃股。

5. **特色功能模块**：stock_feature（龙虎榜/融资融券/北向资金）、economic（宏观经济）、fund（公募基金/ETF）、bond（债券）、futures（期货）、option（期权）、forex（外汇）、crypto（数字货币）。

6. **HTTP API层**：通过AKTools（基于FastAPI）提供HTTP API，适用于非Python环境的调用，启动后可通过curl等工具访问接口。

7. **基本面与财务数据**：提供财务三表（资产负债表/利润表/现金流量表）via `stock_financial_report_sina`，还包括历史分红数据、IPO信息、分析师评级等功能。

8. **生态集成**：与[[AKQuant]]（Rust回测框架）原生集成，提供高性能回测能力，并支持通过Docker一键部署，适合Agent系统集成。

9. **生产实践**：支持容错封装、批量并发处理（使用ThreadPoolExecutor规避GIL），建议进行版本锁定以避免上游改版导致的接口突变。

## 来源
- [[akshare]] — AKShare 深度分析报告
- [[raw/assets/finance-knowledge/akshare-skill/SKILL.md]] — akshare技能详细说明
- [[raw/assets/finance-knowledge/akshare.md]] — AKShare深度分析报告

## 相关
- [[Baostock]] — compares_to
- [[A股行情数据]] — provides_data_for
- [[北向资金]] — provides_data_for
- [[龙虎榜]] — provides_data_for
- [[融资融券]] — provides_data_for
- [[ETF基金]] — provides_data_for
- [[宏观经济数据]] — provides_data_for
- [[期货数据]] — provides_data_for
- [[东方财富]] — uses
- [[新浪财经]] — uses
- [[同花顺]] — uses
- [[AKTools]] — extends
- [[AKQuant]] — integrates_with
