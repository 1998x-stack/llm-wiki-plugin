---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [finance, stocks, data, api, python-library, market-data, quantitative-finance, 工具与框架]
aliases: [yfinance, Yahoo Finance, Yahoo Finance API]
relates_to: 
  - target: "[[Yahoo Finance]]"
    type: part_of
  - target: "[[Ran Aroussi]]"
    type: implements
  - target: "[[Alpha Vantage]]"
    type: compares_to
  - target: "[[Baostock]]"
    type: compares_to
  - target: "[[AKShare]]"
    type: compares_to
  - target: "[[Financial Modeling Prep]]"
    type: compares_to
  - target: "[[Polygon.io]]"
    type: compares_to
  - target: "[[Finnhub]]"
    type: compares_to
  - target: "[[requests-cache]]"
    type: uses
  - target: "[[A股行情数据]]"
    type: compares_to
  - target: "[[美股数据]]"
    type: compares_to
supersedes: null
entity_type: tool
---

# yfinance

## 概述
yfinance是Yahoo Finance非官方[[Python]]封装库，提供零[[Configuration|配置]]访问全球60+国家市场的股票数据，包括历史行情、财务报表、期权链等，适用于学术研究和策略原型验证。

## 关键内容

1. **项目背景**：
   - 最新版本：1.2.1（2026-04-07，活跃维护）
   - 作者：Ran Aroussi（2019年从fix-yahoo-finance改名）
   - 许可证：Apache 2.0
   - [[Python]]要求：≥ 3.8
   - 数据源：Yahoo Finance公开接口（非官方，爬取+非公开API）
   - 市场覆盖：美股、港股、A股、ETF、加密货币、外汇、[[期货数据|期货]]、指数

2. **核心API体系**：
   - **Ticker对象**：核心功能模块
     - `ticker.history()` - 获取历史K线数据（OHLCV + Dividends + Splits）
     - `ticker.fast_info` - 轻量级实时快照（价格/市值/PE）
     - `ticker.financials`, `ticker.quarterly_financials` - 财务报表（年度/季度）
     - `ticker.balance_sheet`, `ticker.quarterly_balance_sheet` - 资产负债表
     - `ticker.cashflow`, `ticker.quarterly_cashflow` - 现金流量表
     - `ticker.info` - 公司概况（完整JSON字典）
     - `ticker.calendar` - 财报/股息日历
     - `ticker.analyst_price_targets`, `ticker.recommendations` - 分析师评级
     - `ticker.major_holders`, `ticker.institutional_holders` - 股东结构
     - `ticker.option_chain()` - 期权链数据（calls + puts）
     - `ticker.dividends`, `ticker.splits`, `ticker.actions` - 股息拆股记录
     - `ticker.news` - 相关新闻
   - **批量下载**：`yf.download()`函数用于批量获取多股票数据
     - 支持时间范围参数：`start`, `end`, `period`
     - 支持多只股票返回MultiIndex DataFrame
     - 支持多线程下载：`threads=True`
     - 支持自动复权：`auto_adjust=True`
   - **Sector/Industry API**：v1.0+新增的行业分析API
     - `Sector("technology")` - 行业概览（头部公司、相关ETF等）
     - `Industry("semiconductors")` - 子行业分析
   - **Multi-Ticker操作**：`yf.Tickers()`批量管理多个Ticker对象

3. **全球市场代码规范**：
   - 美股：直接使用代码（如`AAPL`, `MSFT`）
   - 港股：4-5位数字 + `.HK`（如`0700.HK`, `09988.HK`）
   - A股：6位数字 + `.SS`（上交所）或 `.SZ`（深交所）（如`600519.SS`, `000001.SZ`）
   - 指数：`^`前缀（如`^GSPC`, `^HSI`）
   - 外汇：`XXXYYY=X`（如`EURUSD=X`）
   - 加密货币：`XXX-USD`（如`BTC-USD`）
   - ETF：直接使用代码（如`SPY`, `QQQ`）

4. **历史数据限制**：
   - `1m` (1分钟) - 仅最近7天
   - `2m/5m/15m/30m` - 仅最近60天  
   - `60m/90m/1h` - 仅最近730天
   - `1d` (1日) - 无限制（约20年+）
   - `5d/1wk/1mo/3mo` - 无限制

5. **限流与反爬处理**：
   - 常见HTTP 429错误（Too Many Requests）
   - 解决方案：请求间增加延迟、使用requests_cache本地缓存、代理池
   - 推荐使用requests_cache进行缓存，避免重复请求
   - 分块批量下载可降低单次请求压力

6. **优势与局限性**：
   - 优势：零[[Configuration|配置]]、全球市场覆盖、数据丰富、免费、[[Python]]ic集成、活跃维护
   - 局限性：非官方（随时可能失效）、限流风险、[[A股行情数据|A股数据]]质量差、不适合生产环境、法律灰色地带、数据延迟（约15分钟）

7. **适用场景**：
   - 适合：学术研究、量化策略原型验证、个人投资者分析、教学演示、期权策略研究
   - 不适合：生产级交易系统、高频/日内策略、大批量自动化下载、商业产品内置数据层

## 来源
- [[yfinance.md]] — Yahoo Finance深度分析报告
- [[SKILL.md]] — Yahoo Finance技能定义文件
- [[raw/assets/finance-knowledge/yfinance.md]] — yfinance深度分析报告

## 相关
- [[Yahoo Finance]] — part_of
- [[Ran Aroussi]] — author
- [[Alpha Vantage]] — compares_to
- [[Baostock]] — compares_to
- [[AKShare]] — compares_to
- [[Financial Modeling Prep]] — compares_to
- [[Polygon.io]] — compares_to
- [[Finnhub]] — compares_to
- [[requests-cache]] — dependency
- [[A股行情数据]] — compares_to
- [[美股数据]] — compares_to
