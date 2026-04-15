---
name: yfinance
description: >
  Yahoo Finance 全球股票数据专家——yfinance Python 库。当用户需要以下数据时必须激活：
  美股/港股/全球市场历史行情、公司财务报表（利润表/资产负债表/现金流量表）、期权链数据、
  股息历史、机构持股、分析师评级、股票新闻、ETF数据、加密货币(BTC/ETH)、外汇汇率、
  全球指数(S&P500/纳斯达克/恒生指数)。触发关键词：yfinance、yahoo finance、
  美股数据、全球股票数据、ticker、OHLCV历史、股票期权链、公司基本面、分析师目标价、
  股息记录、回购历史、内部人交易、机构持股、美股财务报表、多股票批量下载。
  即使用户只说"帮我下载苹果公司股价""我要做美股回测""查一下特斯拉的期权链"也应立即激活。
  重要提示：yfinance 是非官方接口，仅限研究/教育，不适合生产交易系统。
---

# yfinance Skill

## 核心定位

yfinance 是**全球市场历史数据**最简单的 Python 入口：零配置、无需 API Key、覆盖 60+ 国家市场。
适合学术研究、策略原型验证、个人投资分析。**不建议**用于生产级交易系统（非官方接口，Yahoo 可随时改变）。

## 安装

```bash
pip install yfinance
pip install yfinance --upgrade  # 接口变化频繁，务必保持最新
# 当前最新稳定版：1.2.1 (2026-04)
```

---

## 股票代码格式规范

```python
# 美股：直接使用
"AAPL"    # 苹果
"MSFT"    # 微软
"TSLA"    # 特斯拉
"BRK-B"   # 伯克希尔B类

# 港股
"0700.HK"   # 腾讯（4位+.HK）
"09988.HK"  # 阿里巴巴（5位+.HK）

# A 股
"600519.SS"  # 贵州茅台（上交所 .SS）
"000001.SZ"  # 平安银行（深交所 .SZ）

# 指数
"^GSPC"   # S&P 500
"^NDX"    # NASDAQ 100
"^HSI"    # 恒生指数
"^N225"   # 日经225
"000001.SS"  # 上证指数

# 外汇（Forex）
"EURUSD=X"  # 欧元/美元
"CNYJPY=X"  # 人民币/日元

# 加密货币
"BTC-USD"   # 比特币
"ETH-USD"   # 以太坊

# ETF
"SPY"        # SPDR S&P 500 ETF
"QQQ"        # 纳指100 ETF
"510300.SS"  # 沪深300ETF（A股场内）
```

---

## 核心 API 详解

### 1. 历史 K 线（最常用）

```python
import yfinance as yf

ticker = yf.Ticker("AAPL")

# 方式一：使用 period（推荐快速使用）
df = ticker.history(period="1y")           # 1d/5d/1mo/3mo/6mo/1y/2y/5y/10y/ytd/max

# 方式二：指定日期范围
df = ticker.history(
    start="2020-01-01",
    end="2024-12-31",
    interval="1d",      # 1m/2m/5m/15m/30m/60m/90m/1h/1d/5d/1wk/1mo/3mo
    auto_adjust=True    # 自动后复权（默认True，处理分红和拆股）
)
# 列：Open High Low Close Volume Dividends Stock Splits
```

**interval 历史深度限制：**

| interval | 最大历史 | 说明 |
|----------|---------|------|
| 1m | 7天 | 约束最严 |
| 5m/15m/30m | 60天 | |
| 1h | 730天 | |
| 1d/1wk/1mo | 无限制 | 约20+年，最稳定 |

### 2. 批量下载（多股票）

```python
import yfinance as yf

# 多只股票日线（返回 MultiIndex DataFrame）
df = yf.download(
    tickers=["AAPL", "MSFT", "GOOGL", "NVDA"],
    start="2020-01-01",
    end="2024-12-31",
    interval="1d",
    auto_adjust=True,
    threads=True        # 多线程，显著加速批量下载
)

# 提取单只收盘价
close = df["Close"]          # 所有股票 Close 列
aapl_close = df["Close"]["AAPL"]
```

### 3. 公司信息 & 实时快照

```python
ticker = yf.Ticker("AAPL")

# 完整公司概况（大型字典）
info = ticker.info
print(info.get("marketCap"))           # 总市值
print(info.get("trailingPE"))          # PE（TTM）
print(info.get("dividendYield"))       # 股息率
print(info.get("52WeekHigh"))          # 52周高点
print(info.get("sector"))              # 行业板块
print(info.get("country"))             # 国家

# 轻量级实时快照（比 info 快）
fast = ticker.fast_info
print(fast.last_price)                 # 最新价
print(fast.market_cap)                 # 市值
print(fast.fifty_two_week_high)        # 52周高点
```

### 4. 财务报表

```python
ticker = yf.Ticker("AAPL")

# 利润表（年度）
fs = ticker.financials
# 利润表（季度）
qfs = ticker.quarterly_financials

# 资产负债表（年度）
bs = ticker.balance_sheet
# 资产负债表（季度）
qbs = ticker.quarterly_balance_sheet

# 现金流量表（年度）
cf = ticker.cashflow
# 现金流量表（季度）
qcf = ticker.quarterly_cashflow
```

### 5. 期权链

```python
ticker = yf.Ticker("AAPL")

# 获取所有可用到期日
exp_dates = ticker.options
print(exp_dates[:5])  # e.g. ('2025-01-17', '2025-01-24', ...)

# 获取指定到期日的期权链
chain = ticker.option_chain("2025-01-17")
calls = chain.calls    # 认购期权
puts = chain.puts      # 认沽期权

# 关键字段：contractSymbol, strike, lastPrice, impliedVolatility, openInterest, delta
print(calls[['strike', 'lastPrice', 'impliedVolatility', 'openInterest']].head())
```

### 6. 股东 & 分析师数据

```python
ticker = yf.Ticker("AAPL")

# 分析师评级（升降级历史）
upgrades = ticker.upgrades_downgrades

# 分析师目标价
targets = ticker.analyst_price_targets
print(f"平均目标价: {targets.get('mean')}")
print(f"最高目标价: {targets.get('high')}")

# 机构持股
inst = ticker.institutional_holders

# 内部人交易
insider = ticker.insider_transactions

# 历史分红
div = ticker.dividends

# 历史拆股
splits = ticker.splits
```

### 7. 行业 & 公司新闻（v1.0+）

```python
from yfinance import Sector, Industry
import yfinance as yf

# 科技行业
tech = Sector("technology")
print(tech.top_companies)     # 头部公司 + 分析师评级
print(tech.top_etfs)          # 相关 ETF

# 子行业
semi = Industry("semiconductors")
print(semi.top_companies)

# 股票新闻
ticker = yf.Ticker("NVDA")
news = ticker.news
for item in news[:3]:
    print(item['content']['title'])
```

---

## 批量回测 Pipeline 示例

```python
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 下载 S&P 500 前10大权重股（5年日线）
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
           "META", "TSLA", "BRK-B", "JPM", "LLY"]

df = yf.download(tickers, period="5y", auto_adjust=True, threads=True)
close = df["Close"].dropna()

# 计算年化收益 & 夏普比率
returns = close.pct_change().dropna()
annual_ret = returns.mean() * 252
annual_vol = returns.std() * np.sqrt(252)
sharpe = annual_ret / annual_vol

summary = pd.DataFrame({
    "Annual Return": annual_ret.map("{:.1%}".format),
    "Annual Vol": annual_vol.map("{:.1%}".format),
    "Sharpe": sharpe.map("{:.2f}".format)
})
print(summary.sort_values("Sharpe", ascending=False))
```

---

## 限流问题处理

### 问题表现
```
HTTP 429 Too Many Requests  ← Yahoo 反爬触发
yfinance.exceptions.YFRateLimitError
```

### 解决方案

```python
# 1. 本地请求缓存（最推荐）
import requests_cache
requests_cache.install_cache('yf_cache', expire_after=3600)  # pip install requests-cache
import yfinance as yf
df = yf.download("AAPL", period="1y")  # 第一次走网络，后续命中本地缓存

# 2. 请求间增加延迟
import time
for ticker_sym in tickers:
    t = yf.Ticker(ticker_sym)
    df = t.history(period="1y")
    time.sleep(1.5)  # 至少 1 秒延迟

# 3. 分批下载（每批不超过 50 只）
def batch_download(tickers, batch_size=30, delay=2.0, **kwargs):
    results = []
    for i in range(0, len(tickers), batch_size):
        chunk = tickers[i:i+batch_size]
        df = yf.download(chunk, **kwargs)
        results.append(df)
        time.sleep(delay)
    return pd.concat(results, axis=1)
```

---

## A 股数据使用注意

```python
# A 股代码格式（yfinance 支持，但质量不如 Baostock/AKShare）
maotai = yf.Ticker("600519.SS")    # 上交所加 .SS
ping_an = yf.Ticker("000001.SZ")   # 深交所加 .SZ

# 已知问题：
# - 财务报表为英文标签，中文财务概念可能对应不准
# - OHLCV 偶有数据缺口
# - 不含 A 股特有字段（换手率、涨跌停）

# 推荐：A股数据用 Baostock（官方来源）或 AKShare（更完整）
```

---

## 常用 Ticker 代码速查

```python
# 常用美股
FAANG = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]
TECH  = ["MSFT", "NVDA", "TSLA", "AMD", "INTC", "ORCL"]

# 常用指数
INDICES = {
    "S&P500":    "^GSPC",
    "Nasdaq100": "^NDX",
    "Dow30":     "^DJI",
    "恒生指数":   "^HSI",
    "日经225":    "^N225",
    "A股上证":    "000001.SS",
}

# 常用 ETF
ETFS = {
    "SPY": "SPDR S&P500 ETF",
    "QQQ": "Invesco Nasdaq100 ETF",
    "GLD": "SPDR Gold Shares",
    "TLT": "iShares 20+ Year Treasury",
    "VIX": "^VIX",  # 波动率指数
}
```

---

## 不适合 yfinance 的场景

| 场景 | 推荐替代 |
|------|----------|
| A 股专业量化回测 | Baostock / AKShare |
| 生产级交易系统数据 | Polygon.io / Alpaca |
| 高频/日内实时数据 | Interactive Brokers API |
| 免费全球基本面 | Finnhub（60次/分钟） |
| 中国宏观 + 多品类 | AKShare |

---

## 法律提示

yfinance 使用 Yahoo Finance 非授权接口，**仅限研究和教育目的**。
商业用途请参考 Yahoo Finance 服务条款，或改用 Polygon.io 等官方授权 API。
