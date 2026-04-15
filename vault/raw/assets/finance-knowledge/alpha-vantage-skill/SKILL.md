---
name: alpha-vantage
description: >
  NASDAQ官方授权全球金融数据API——Alpha Vantage。当用户需要以下任何内容时必须激活：
  美股历史/实时行情、技术指标（SMA/EMA/RSI/MACD/布林带/ATR/OBV等50+指标）、公司基本面（PE/PB/EPS/市值）、
  财务报表（利润表/资产负债表/现金流量表）、外汇汇率、加密货币数据、宏观经济指标（美国GDP/CPI/非农/国债收益率）、
  股票新闻情感分析、IPO日历、财报日历、Alpha Vantage API集成、AI Agent金融数据工具、MCP金融数据。
  触发关键词：alpha vantage、alphavantage、技术指标API、RSI接口、MACD数据、内置技术指标、
  官方股票API、NASDAQ授权数据、新闻情感评分、美股宏观数据、金融数据REST API。
  即使用户只说"帮我接入股票API""我需要RSI数据""查一下宏观经济指标"也应立即激活。
  注意：免费配额仅25次/天，生产环境建议购买付费套餐。
---

# Alpha Vantage Skill

## 核心定位

Alpha Vantage 是 **NASDAQ 官方授权**的全球金融数据 REST API，核心竞争力是：
1. **50+ 内置技术指标**（服务端预计算，直接返回数值）
2. **官方 MCP Server**（AI Agent 生态中最完善的金融数据接入）
3. 法律合规的实时美股数据（付费套餐）

## 获取 API Key

```
免费申请：https://www.alphavantage.co/support/#api-key
免费配额：25 次/天（2025 年起调整）
付费套餐：$49.99~$249.99/月，速率从 30次/min 到 600次/min
```

## 安装

```bash
# 官方 Python 封装库
pip install alpha_vantage requests pandas

# 或直接使用 requests（更灵活）
pip install requests pandas
```

---

## API 架构

所有请求格式：

```
GET https://www.alphavantage.co/query?function=FUNCTION_NAME&symbol=SYMBOL&apikey=KEY&...
```

支持 JSON（默认）和 CSV（`&datatype=csv`）两种格式。

---

## 核心接口速查

### 1. 股票时间序列

```python
import requests
import pandas as pd
from io import StringIO

API_KEY = "YOUR_KEY"
BASE_URL = "https://www.alphavantage.co/query"

def av_request(params: dict) -> dict:
    """通用请求函数（含错误检测）"""
    resp = requests.get(BASE_URL, params={**params, "apikey": API_KEY})
    resp.raise_for_status()
    data = resp.json()
    if "Note" in data:
        raise RateLimitError(data["Note"])
    if "Information" in data:
        raise APIError(data["Information"])
    return data

# 日线数据（复权，含拆股/分红调整）
def get_daily_adjusted(symbol: str, outputsize: str = "compact") -> pd.DataFrame:
    """
    outputsize: 'compact'=最近100条（免费可用）/ 'full'=20年全量（需付费）
    """
    data = av_request({
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": outputsize
    })
    ts = data["Time Series (Daily)"]
    df = pd.DataFrame(ts).T
    df.index = pd.to_datetime(df.index)
    df.columns = ['open','high','low','close','adjusted_close',
                  'volume','dividend','split_coeff']
    df = df.astype(float).sort_index()
    return df

# 使用示例
df = get_daily_adjusted("AAPL")
print(df.tail(10))
```

**全部时间序列接口：**

| 函数名 | 说明 | 参数 |
|--------|------|------|
| `TIME_SERIES_INTRADAY` | 日内 OHLCV | interval=1min/5min/15min/30min/60min |
| `TIME_SERIES_DAILY` | 日线（原始价格） | outputsize=compact/full |
| `TIME_SERIES_DAILY_ADJUSTED` | 日线（复权） | outputsize=compact/full |
| `TIME_SERIES_WEEKLY_ADJUSTED` | 周线（复权） | - |
| `TIME_SERIES_MONTHLY_ADJUSTED` | 月线（复权） | - |
| `GLOBAL_QUOTE` | 最新报价（单只） | symbol |
| `REALTIME_BULK_QUOTES` | 批量实时报价（≤100只） | symbol（逗号分隔，付费） |

### 2. 50+ 内置技术指标（核心竞争力）

```python
from alpha_vantage.techindicators import TechIndicators

ti = TechIndicators(key=API_KEY, output_format='pandas')

# RSI（相对强弱指数）
rsi, _ = ti.get_rsi(symbol="AAPL", interval="daily", time_period=14, series_type="close")

# MACD
macd, _ = ti.get_macd(symbol="AAPL", interval="daily", 
                       fastperiod=12, slowperiod=26, signalperiod=9)

# 布林带
bbands, _ = ti.get_bbands(symbol="AAPL", interval="daily", 
                           time_period=20, series_type="close",
                           nbdevup=2, nbdevdn=2)

# SMA / EMA
sma, _ = ti.get_sma(symbol="AAPL", interval="daily", time_period=50)
ema, _ = ti.get_ema(symbol="AAPL", interval="daily", time_period=20)

# STOCH（随机指标）
stoch, _ = ti.get_stoch(symbol="AAPL", interval="daily")

# ATR（真实波幅）
atr, _ = ti.get_atr(symbol="AAPL", interval="daily", time_period=14)

# OBV（能量潮）
obv, _ = ti.get_obv(symbol="AAPL", interval="daily")
```

**直接 URL 调用技术指标：**

```python
# 不依赖官方库，直接 requests
def get_indicator(function: str, symbol: str, **kwargs) -> pd.DataFrame:
    params = {"function": function, "symbol": symbol, **kwargs}
    data = av_request(params)
    # 找到技术分析结果键
    ta_key = [k for k in data if k.startswith("Technical")][0]
    df = pd.DataFrame(data[ta_key]).T
    df.index = pd.to_datetime(df.index)
    return df.astype(float).sort_index()

# 获取 MACD
macd_df = get_indicator("MACD", "TSLA", interval="daily",
                         fastperiod=12, slowperiod=26, signalperiod=9)
```

**全部支持的指标分类：**

```
移动平均：SMA EMA WMA DEMA TEMA TRIMA KAMA MAMA T3
趋势:     MACD MACDEXT MACDFIX ADX ADXR AROON AROONOSC PLUS_DI MINUS_DI
动量:     RSI STOCH STOCHF STOCHRSI WILLR MOM BOP CCI CMO ROC ROCP ROCR TRIX MFI
波动率:   BBANDS ATR NATR TRANGE
成交量:   OBV AD ADOSC
价格:     AVGPRICE MEDPRICE TYPPRICE WCLPRICE
```

### 3. 公司基本面

```python
def get_company_overview(symbol: str) -> dict:
    """获取公司概况（市值/PE/PB/EPS/股息率等）"""
    data = av_request({"function": "OVERVIEW", "symbol": symbol})
    return data

overview = get_company_overview("AAPL")
print(f"市盈率(TTM): {overview.get('TrailingPE')}")
print(f"市净率: {overview.get('PriceToBookRatio')}")
print(f"市值: ${float(overview.get('MarketCapitalization',0))/1e12:.2f}T")
print(f"股息率: {overview.get('DividendYield')}")
print(f"52周高点: {overview.get('52WeekHigh')}")
print(f"分析师评级: {overview.get('AnalystRatingBuy')} Buy")

# 财务报表
def get_financials(symbol: str, report_type: str) -> pd.DataFrame:
    """
    report_type: INCOME_STATEMENT / BALANCE_SHEET / CASH_FLOW
    """
    data = av_request({"function": report_type, "symbol": symbol})
    annual = data.get("annualReports", [])
    return pd.DataFrame(annual)

income = get_financials("AAPL", "INCOME_STATEMENT")
print(income[['fiscalDateEnding', 'totalRevenue', 'netIncome']].head())
```

### 4. 宏观经济数据

```python
def get_macro(function: str) -> pd.DataFrame:
    """获取美国宏观经济指标"""
    data = av_request({"function": function})
    return pd.DataFrame(data.get("data", []))

# 美国实际 GDP（季度）
gdp = get_macro("REAL_GDP")

# CPI（月度）
cpi = get_macro("CPI")

# 非农就业（月度）
nonfarm = get_macro("NONFARM_PAYROLL")

# 美联储基金利率
fed_rate = get_macro("FEDERAL_FUNDS_RATE")

# 国债收益率（10年）
treasury = av_request({"function": "TREASURY_YIELD", "interval": "monthly", "maturity": "10year"})
yield_df = pd.DataFrame(treasury.get("data", []))

# 失业率
unemployment = get_macro("UNEMPLOYMENT")
```

### 5. 新闻情感分析

```python
def get_news_sentiment(ticker: str, limit: int = 50) -> pd.DataFrame:
    """
    获取股票新闻 + AI 情感评分
    sentiment_label: Bullish / Somewhat-Bullish / Neutral / Somewhat-Bearish / Bearish
    sentiment_score: -1 到 1
    """
    data = av_request({
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "limit": limit,
        "sort": "LATEST"
    })
    
    records = []
    for item in data.get("feed", []):
        for ts in item.get("ticker_sentiment", []):
            if ts["ticker"] == ticker:
                records.append({
                    "time": item["time_published"],
                    "title": item["title"],
                    "source": item["source"],
                    "label": ts["ticker_sentiment_label"],
                    "score": float(ts["ticker_sentiment_score"]),
                    "relevance": float(ts["relevance_score"])
                })
    
    df = pd.DataFrame(records)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'])
    return df

# 情感分析
sentiment = get_news_sentiment("NVDA", limit=100)
print(sentiment.groupby('label')['score'].agg(['count','mean']))
```

### 6. 外汇 & 加密货币

```python
# 实时汇率
def get_fx_rate(from_ccy: str, to_ccy: str) -> dict:
    return av_request({
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_ccy,
        "to_currency": to_ccy
    })["Realtime Currency Exchange Rate"]

usd_cny = get_fx_rate("USD", "CNY")
print(f"USD/CNY: {usd_cny['5. Exchange Rate']}")

# 外汇历史数据
fx_daily = av_request({
    "function": "FX_DAILY",
    "from_symbol": "EUR",
    "to_symbol": "USD",
    "outputsize": "compact"
})

# 加密货币日线
crypto = av_request({
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": "BTC",
    "market": "USD"
})
```

### 7. 批量报价（付费）

```python
def get_bulk_quotes(symbols: list[str]) -> pd.DataFrame:
    """批量实时报价，最多100只，需付费 Plan30+"""
    data = av_request({
        "function": "REALTIME_BULK_QUOTES",
        "symbol": ",".join(symbols[:100])
    })
    return pd.DataFrame(data.get("data", []))

quotes = get_bulk_quotes(["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"])
```

---

## 限流管理（关键）

```python
import time, functools, os
from collections import deque

class AVRateLimiter:
    """Alpha Vantage 速率限制器"""
    
    LIMITS = {
        "free":    5,    # 5次/分钟（免费）
        "plan30":  30,   # 30次/分钟
        "plan75":  75,
        "plan150": 150,
    }
    
    def __init__(self, tier: str = "free"):
        self.rpm = self.LIMITS.get(tier, 5)
        self.call_times = deque()
    
    def wait_if_needed(self):
        now = time.time()
        while self.call_times and now - self.call_times[0] > 60:
            self.call_times.popleft()
        if len(self.call_times) >= self.rpm:
            sleep_sec = 60 - (now - self.call_times[0]) + 0.5
            print(f"Rate limit reached, sleeping {sleep_sec:.1f}s...")
            time.sleep(sleep_sec)
        self.call_times.append(time.time())

limiter = AVRateLimiter(tier="free")

def rate_limited_request(params: dict) -> dict:
    limiter.wait_if_needed()
    return av_request(params)
```

---

## 磁盘缓存封装（生产推荐）

```python
import pickle, hashlib, os, time

CACHE_DIR = ".av_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def cached_av_request(params: dict, ttl: int = 3600) -> dict:
    """带过期时间的磁盘缓存"""
    key = hashlib.md5(str(sorted(params.items())).encode()).hexdigest()
    path = f"{CACHE_DIR}/{key}.pkl"
    
    if os.path.exists(path) and (time.time() - os.path.getmtime(path) < ttl):
        return pickle.load(open(path, 'rb'))
    
    data = rate_limited_request(params)
    pickle.dump(data, open(path, 'wb'))
    return data
```

---

## MCP Server 集成（AI Agent）

Alpha Vantage 是**唯一提供官方 MCP Server** 的金融数据提供商：

```json
// Claude Code mcp 配置（.mcp.json 或 claude_desktop_config.json）
{
  "mcpServers": {
    "alpha-vantage": {
      "url": "https://mcp.alphavantage.co/sse",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

MCP 工具可直接被 Claude 调用：`get_stock_quote`、`get_historical_data`、`get_technical_indicator`、
`get_company_overview`、`get_news_sentiment`、`get_macro_indicator`。

---

## 常见错误处理

```python
def robust_av_request(params: dict, max_retry: int = 3) -> dict:
    for attempt in range(max_retry):
        try:
            limiter.wait_if_needed()
            resp = requests.get(BASE_URL, params={**params, "apikey": API_KEY}, timeout=10)
            data = resp.json()
            
            if "Note" in data:
                # 速率限制提示（免费用户每分钟5次/每天25次）
                print("Rate limit note:", data["Note"])
                time.sleep(60)  # 等待1分钟
                continue
            
            if "Information" in data:
                # 通常是超过每日配额
                raise DailyLimitExceeded(data["Information"])
            
            if "Error Message" in data:
                raise InvalidSymbol(data["Error Message"])
            
            return data
            
        except requests.Timeout:
            print(f"Timeout, retry {attempt+1}/{max_retry}")
            time.sleep(2 ** attempt)
    
    raise RuntimeError("Max retries exceeded")
```

---

## 定价与配额选择建议

| 使用场景 | 推荐套餐 | 理由 |
|----------|---------|------|
| 个人学习/原型 | 免费（25次/天） | 够用 |
| 小型应用（单用户） | Plan30（$49.99/月） | 1800次/小时 |
| 多用户 Dashboard | Plan75（$99.99/月） | 4500次/小时 |
| 技术分析批量系统 | Plan150（$149.99/月） | 9000次/小时 |
| 实时美股 + 大规模 | Enterprise | 联系销售 |

> 注意：实时美股/期权数据需额外在 **Alpha X Terminal** 完成数据权利申请（FINRA/SEC 合规）。

---

## 不适合 Alpha Vantage 的场景

| 场景 | 推荐替代 |
|------|----------|
| A 股/港股专业数据 | Baostock / AKShare |
| 低延迟实时数据 | Polygon.io |
| 高 QPS 免费请求 | Finnhub（60次/分钟免费） |
| 大批量历史下载 | EODHD（按需付费） |
| 纯 Python 全球快速原型 | yfinance（零配置） |
