# Alpha Vantage 深度分析报告

> **定位**：NASDAQ 官方授权全球市场数据 API · REST 接口 · 50+ 内置技术指标 · MCP 原生支持

---

## 一、项目概览

| 维度 | 详情 |
|------|------|
| 服务类型 | 商业 REST API（有免费套餐） |
| 公司背景 | Y Combinator 孵化，NASDAQ 官方授权数据供应商 |
| 接口数量 | **100+ API 端点** |
| 市场覆盖 | 美股、全球20+ 交易所、外汇、加密货币、大宗商品、宏观经济 |
| 技术指标 | **50+ 内置预计算指标**（SMA/EMA/RSI/MACD/BB 等） |
| 数据格式 | JSON / CSV |
| 历史深度 | **20+ 年**（premium 全量），免费 compact=100条 |
| 免费配额 | **25 次/天**（2025年最新限制） |
| Python 库 | `alpha_vantage`（官方支持） |
| MCP 支持 | **官方 MCP Server**（AI Agent 生态第一） |

---

## 二、定价体系

### 2.1 免费套餐

| 指标 | 限制 |
|------|------|
| 每日请求数 | **25 次/天** |
| 历史数据量 | compact 模式（最近 100 条） |
| 实时美股数据 | ❌ 不含（需付费 + 数据权利授权） |
| 支持 | 社区支持 |

> ⚠️ 2025 年 Alpha Vantage 将免费配额从 500/天大幅降至 **25 次/天**，对原型开发影响显著。

### 2.2 付费套餐（参考价格）

| 套餐 | 价格/月 | 每分钟请求数 | 特性 |
|------|---------|-------------|------|
| Plan 30 | ~$49.99 | 30 次/min | 历史完整数据 |
| Plan 75 | ~$99.99 | 75 次/min | + 批量报价 |
| Plan 150 | ~$149.99 | 150 次/min | 机构级用量 |
| Enterprise | ~$249.99+ | 600+ 次/min | 实时数据 + SLA |

> 实时美股数据（非延迟）需额外通过 **Alpha X Terminal** 完成数据授权流程（FINRA 合规要求）。

---

## 三、核心 API 分类体系

### 3.1 股票时间序列

| API 函数 | 说明 | 注意 |
|----------|------|------|
| `TIME_SERIES_INTRADAY` | 日内 OHLCV（1/5/15/30/60 分钟） | 实时需付费 |
| `TIME_SERIES_DAILY` | 日线（原始价格，未复权） | 免费可用 |
| `TIME_SERIES_DAILY_ADJUSTED` | 日线（复权，含拆股/分红） | **推荐** |
| `TIME_SERIES_WEEKLY` | 周线 | 免费 |
| `TIME_SERIES_WEEKLY_ADJUSTED` | 周线（复权） | 免费 |
| `TIME_SERIES_MONTHLY` | 月线 | 免费 |
| `GLOBAL_QUOTE` | 单只股票最新报价（轻量） | 最常用 |
| `REALTIME_BULK_QUOTES` | 批量实时报价（最多 100 只） | 付费 |
| `LISTING_STATUS` | 股票上市/退市状态列表 | 免费 |
| `EARNINGS_CALENDAR` | 即将公布财报日历 | 免费 |
| `IPO_CALENDAR` | IPO 日历 | 免费 |

### 3.2 50+ 内置技术指标

Alpha Vantage **核心竞争力**：所有技术指标均由服务端预计算，直接返回数值序列。

| 分类 | 指标 |
|------|------|
| 移动平均 | SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA, MAMA, T3 |
| 动量振荡器 | RSI, STOCH, STOCHF, STOCHRSI, WILLR, ADX, ADXR, APO, PPO, MOM, BOP, CCI, CMO, ROC, ROCP, ROCR, AROON, AROONOSC, MFI, TRIX, ULTOSC, DX, MINUS_DI, PLUS_DI, MINUS_DM, PLUS_DM |
| 趋势 | MACD, MACDEXT, MACDFIX |
| 波动率 | BBANDS, ATR, NATR, TRANGE |
| 成交量 | OBV, AD, ADOSC |
| 价格变换 | AVGPRICE, MEDPRICE, TYPPRICE, WCLPRICE |

```
# 示例 URL（RSI 14日）
https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=close&apikey=YOUR_KEY
```

### 3.3 基本面数据

| API 函数 | 内容 |
|----------|------|
| `OVERVIEW` | 公司概况（市值/PE/PB/股息率/52周高低等） |
| `INCOME_STATEMENT` | 利润表（年度+季度，最近5年） |
| `BALANCE_SHEET` | 资产负债表 |
| `CASH_FLOW` | 现金流量表 |
| `EARNINGS` | EPS 历史 + 预期 vs 实际对比 |
| `EARNINGS_CALL_TRANSCRIPT` | 财报电话会议文字稿（Premium） |

### 3.4 外汇与加密货币

| API 函数 | 说明 |
|----------|------|
| `CURRENCY_EXCHANGE_RATE` | 实时汇率（150+ 货币对） |
| `FX_INTRADAY` | 外汇日内数据 |
| `FX_DAILY/WEEKLY/MONTHLY` | 外汇历史数据 |
| `CRYPTO_INTRADAY` | 加密货币日内 |
| `DIGITAL_CURRENCY_DAILY` | 数字货币日线（100+ 币种） |

### 3.5 宏观经济

| API 函数 | 内容 |
|----------|------|
| `REAL_GDP` | 美国实际 GDP（季度/年度） |
| `CPI` | 美国 CPI（月度） |
| `INFLATION` | 通胀率（年度） |
| `RETAIL_SALES` | 美国零售销售（月度） |
| `DURABLES` | 耐用品订单 |
| `UNEMPLOYMENT` | 失业率 |
| `NONFARM_PAYROLL` | 非农就业人数 |
| `FEDERAL_FUNDS_RATE` | 联邦基金利率（日/周/月） |
| `TREASURY_YIELD` | 美国国债收益率（2/5/10/30年） |

### 3.6 新闻与情感分析

```
NEWS_SENTIMENT
- 覆盖 50+ 新闻媒体
- 返回：标题、摘要、来源、发布时间
- AI 情感分数：bullish/bearish/neutral（0~1）
- 支持按 ticker 筛选
- 支持按 topic 筛选（finance/technology/IPO 等）
```

---

## 四、快速上手代码

### 4.1 安装

```bash
# 官方 Python 封装库
pip install alpha_vantage

# 直接用 requests（无需专用库）
pip install requests pandas
```

### 4.2 使用官方 Python 库

```python
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

API_KEY = "YOUR_API_KEY"  # 在 alphavantage.co/support 免费领取

# 股票日线数据
ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta = ts.get_daily_adjusted(symbol='AAPL', outputsize='full')
print(data.tail())

# RSI 技术指标
ti = TechIndicators(key=API_KEY, output_format='pandas')
rsi_data, rsi_meta = ti.get_rsi(
    symbol='AAPL',
    interval='daily',
    time_period=14,
    series_type='close'
)
rsi_data.plot(title='AAPL RSI(14)')
plt.show()
```

### 4.3 直接使用 requests（推荐用于生产）

```python
import requests
import pandas as pd
from io import StringIO

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://www.alphavantage.co/query"

def get_daily_adjusted(symbol: str, outputsize: str = "compact") -> pd.DataFrame:
    """获取日线（复权）数据
    
    Args:
        symbol: 股票代码（如 'AAPL', 'IBM'）
        outputsize: 'compact'=100条 / 'full'=20年全量（需付费）
    """
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": outputsize,
        "datatype": "csv",      # JSON 或 CSV
        "apikey": API_KEY
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    df = pd.read_csv(StringIO(resp.text))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    return df

# 使用
df = get_daily_adjusted("AAPL")
print(df[['open','high','low','close','adjusted_close','volume']].tail(10))
```

### 4.4 批量报价（付费接口）

```python
def get_bulk_quotes(symbols: list) -> pd.DataFrame:
    """批量获取实时报价（最多100只，需付费）"""
    params = {
        "function": "REALTIME_BULK_QUOTES",
        "symbol": ",".join(symbols[:100]),
        "apikey": API_KEY
    }
    data = requests.get(BASE_URL, params=params).json()
    return pd.DataFrame(data.get("data", []))

quotes = get_bulk_quotes(["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"])
print(quotes[['symbol','price','change','change_percent']])
```

### 4.5 新闻情感分析

```python
def get_news_sentiment(ticker: str, limit: int = 50):
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "limit": limit,
        "sort": "LATEST",
        "apikey": API_KEY
    }
    data = requests.get(BASE_URL, params=params).json()
    feed = data.get("feed", [])
    
    records = []
    for item in feed:
        for ts in item.get("ticker_sentiment", []):
            if ts["ticker"] == ticker:
                records.append({
                    "time": item["time_published"],
                    "title": item["title"],
                    "source": item["source"],
                    "sentiment": ts["ticker_sentiment_label"],
                    "score": float(ts["ticker_sentiment_score"])
                })
    
    return pd.DataFrame(records)

sentiment_df = get_news_sentiment("AAPL")
print(sentiment_df.groupby('sentiment').size())
```

### 4.6 限流管理封装

```python
import time
import functools
from collections import deque

class RateLimiter:
    """Alpha Vantage 速率限制管理"""
    
    def __init__(self, calls_per_minute: int = 5):
        """免费: 5/min; Plan30: 30/min; Plan75: 75/min"""
        self.calls_per_minute = calls_per_minute
        self.call_times = deque()
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 清理1分钟前的记录
            while self.call_times and now - self.call_times[0] > 60:
                self.call_times.popleft()
            # 如果已满，等待
            if len(self.call_times) >= self.calls_per_minute:
                sleep_time = 60 - (now - self.call_times[0]) + 0.1
                time.sleep(sleep_time)
            self.call_times.append(time.time())
            return func(*args, **kwargs)
        return wrapper

limiter = RateLimiter(calls_per_minute=5)

@limiter
def safe_av_request(params: dict) -> dict:
    resp = requests.get(BASE_URL, params={**params, "apikey": API_KEY})
    data = resp.json()
    if "Note" in data:  # API 限流提示
        raise Exception(f"Rate limited: {data['Note']}")
    if "Information" in data:
        raise Exception(f"API Error: {data['Information']}")
    return data
```

---

## 五、MCP Server 集成（AI Agent）

Alpha Vantage 是**首个提供官方 MCP Server** 的金融数据提供商：

```bash
# 通过 MCP 协议集成到 Claude Code / 其他 AI Agent
# 官方文档：https://www.alphavantage.co/mcp
```

```json
// Claude Code MCP 配置示例
{
  "mcpServers": {
    "alpha-vantage": {
      "url": "https://mcp.alphavantage.co/sse",
      "apiKey": "YOUR_API_KEY"
    }
  }
}
```

**MCP 可用工具（示例）：**
- `get_stock_quote` → 实时报价
- `get_historical_data` → 历史 OHLCV
- `get_technical_indicator` → 任意技术指标
- `get_company_overview` → 公司基本面
- `get_news_sentiment` → 新闻情感

---

## 六、优势与局限性

### ✅ 优势

| 优势 | 说明 |
|------|------|
| **NASDAQ 官方授权** | 数据质量有保障，法律合规 |
| **50+ 技术指标** | 同类产品中最丰富的内置指标库 |
| **官方 MCP Server** | AI Agent 生态最友好的金融 API |
| **全球覆盖** | 200,000+ 股票，20+ 交易所 |
| **20+ 年历史** | 足够支撑长期回测 |
| **多数据类型** | 股票+外汇+加密+宏观+新闻情感 |
| **格式标准** | REST JSON/CSV，开发者接入简单 |

### ⚠️ 局限性

| 局限 | 说明 |
|------|------|
| **免费配额极低** | 25次/天，实际开发几乎不够用 |
| **A 股数据质量差** | 不是核心市场，中文财务数据缺失 |
| **付费门槛不低** | 最低 $49.99/月，比 Finnhub 贵 |
| **实时数据额外收费** | 需走 Alpha X Terminal 权利流程 |
| **接口命名冗长** | URL 参数设计不如 Python 库直观 |
| **历史深度依赖付费** | 免费只能拿最近100条数据 |

---

## 七、适用场景

```
✅ 最适合：
  - 美股量化策略开发（日线级别）
  - 技术分析系统（50+ 指标开箱即用）
  - AI Agent 金融工具集成（官方 MCP）
  - 美股情感分析 Pipeline
  - 宏观-股票联动研究（美国市场）
  - 教学 / 个人投资者研究（免费额度够用）
  - 多资产类别系统（股+外汇+加密+宏观同一 API）

❌ 不适合：
  - A 股/港股专业量化（Baostock/AKShare 更优）
  - 高频/分钟级大批量数据拉取（限流）
  - 纯免费场景下的规模化数据采集
  - 低延迟实时交易（Polygon.io 更专业）
```

---

## 八、与竞品对比

| 特性 | Alpha Vantage | yfinance | Polygon.io | Finnhub |
|------|---------------|----------|------------|---------|
| 官方授权 | ✅ NASDAQ | ❌ 非官方 | ✅ | ✅ |
| 免费配额 | 25次/天 | 无限制(有限流) | 5次/min | 60次/min |
| 内置技术指标 | ✅ 50+ | ❌ 需自算 | ❌ | 部分 |
| 官方 MCP | ✅ | ❌ | ❌ | ❌ |
| 实时数据（免费） | ❌ | 15min 延迟 | ❌ | 延迟 |
| A 股覆盖 | ⭐⭐ | ⭐⭐⭐ | ❌ | ❌ |
| 最低付费 | $49.99/月 | 免费 | $199/月 | $0（免费好用） |
| 宏观数据 | ✅ 完整 | 部分 | ❌ | 部分 |

---

## 九、最佳实践

```python
# 生产级使用模板
import os
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import pickle, hashlib

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "demo")
BASE_URL = "https://www.alphavantage.co/query"
CACHE_TTL = 3600  # 缓存1小时

# 简单磁盘缓存
def cached_request(params: dict, ttl: int = CACHE_TTL):
    cache_key = hashlib.md5(str(sorted(params.items())).encode()).hexdigest()
    cache_file = f".av_cache/{cache_key}.pkl"
    os.makedirs(".av_cache", exist_ok=True)
    
    if os.path.exists(cache_file):
        mtime = os.path.getmtime(cache_file)
        if time.time() - mtime < ttl:
            return pickle.load(open(cache_file, 'rb'))
    
    resp = requests.get(BASE_URL, params={**params, "apikey": API_KEY})
    data = resp.json()
    pickle.dump(data, open(cache_file, 'wb'))
    return data

# 使用示例
data = cached_request({
    "function": "OVERVIEW",
    "symbol": "AAPL"
})
print(f"PE Ratio: {data.get('PERatio')}")
print(f"Market Cap: {data.get('MarketCapitalization')}")
```

---

*最后更新：2025-04 | Alpha Vantage 官方免费配额：25次/天*
