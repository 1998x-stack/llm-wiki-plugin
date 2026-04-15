# yfinance 深度分析报告

> **定位**：Yahoo Finance 非官方 Python 封装 · 全球市场 · 研究/原型首选 · 非生产级

---

## 一、项目概览

| 维度 | 详情 |
|------|------|
| 最新版本 | `1.2.1`（2026-04-07，活跃维护） |
| Python 要求 | ≥ 3.8 |
| 许可证 | Apache 2.0 |
| 作者 | Ran Aroussi（2019 年从 fix-yahoo-finance 改名） |
| 官网 | https://yfinance.finance |
| GitHub Stars | 15,000+ ⭐ |
| 数据源 | **Yahoo Finance 公开接口**（非官方，爬取+非公开API） |
| 市场覆盖 | 美股、港股、A 股、ETF、加密货币、外汇、期货、指数 |
| 收费方式 | **完全免费**，无需 API Key |
| 法律声明 | **非 Yahoo 官方**，仅限研究/教育目的 |

> ⚠️ **核心风险提示**：yfinance 使用 Yahoo Finance 非授权接口，Yahoo 可随时改变接口结构，可能导致功能异常。**不建议用于生产交易系统。**

---

## 二、版本里程碑

| 版本 | 时间 | 重要变化 |
|------|------|----------|
| 0.2.x | 2024 年全年 | 频繁小版本修复，适配 Yahoo 接口变化 |
| 1.0 | 2025-12-22 | **重大版本**，API 全面重构，新增 Sector/Industry 类 |
| 1.1.0 | 2026-01-24 | 稳定性增强 |
| 1.2.1 | 2026-04-07 | 最新稳定版 |

---

## 三、核心 API 体系

### 3.1 Ticker 对象（核心）

```python
import yfinance as yf

ticker = yf.Ticker("AAPL")

# ── 行情数据 ──────────────────────────────────────
ticker.history(period="1y")                     # OHLCV + Dividends + Splits
ticker.history(start="2020-01-01", end="2024-12-31", interval="1d")
ticker.fast_info                                # 轻量级实时快照（价格/市值/PE）

# ── 财务报表 ──────────────────────────────────────
ticker.financials                               # 年度利润表
ticker.quarterly_financials                    # 季度利润表
ticker.balance_sheet                            # 年度资产负债表
ticker.quarterly_balance_sheet                 # 季度资产负债表
ticker.cashflow                                 # 年度现金流量表
ticker.quarterly_cashflow                       # 季度现金流量表

# ── 公司信息 ──────────────────────────────────────
ticker.info                                     # 完整公司概况（JSON字典）
ticker.calendar                                 # 财报/股息日历
ticker.analyst_price_targets                   # 分析师目标价
ticker.recommendations                          # 分析师评级历史
ticker.upgrades_downgrades                      # 评级调整记录

# ── 股东结构 ──────────────────────────────────────
ticker.major_holders                            # 大股东分布
ticker.institutional_holders                    # 机构持股
ticker.mutualfund_holders                       # 公募基金持股
ticker.insider_transactions                     # 内部人交易
ticker.insider_purchases                        # 内部人买入

# ── 企业动作 ──────────────────────────────────────
ticker.dividends                                # 历史分红记录
ticker.splits                                   # 历史拆股记录
ticker.actions                                  # 分红 + 拆股（合并）

# ── 期权数据 ──────────────────────────────────────
ticker.options                                  # 可用到期日列表
opt_chain = ticker.option_chain("2025-01-17")   # 期权链（calls + puts）

# ── 新闻 ──────────────────────────────────────────
ticker.news                                     # 最新相关新闻（list of dict）
```

### 3.2 批量下载（`yf.download`）

```python
import yfinance as yf

# 单只股票
df = yf.download("AAPL", start="2020-01-01", end="2024-12-31")

# 多只股票（返回 MultiIndex DataFrame）
df = yf.download(["AAPL", "MSFT", "GOOGL"], period="1y")
# 提取单只：df["Close"]["AAPL"]

# 指定时间间隔
df = yf.download("TSLA", period="60d", interval="1h")   # 1h 级别（仅支持近60天）
df = yf.download("AAPL", period="7d",  interval="1m")   # 1m 级别（仅支持近7天）
```

### 3.3 支持的 interval 及历史深度限制

| interval | 可用历史深度 | 备注 |
|----------|-------------|------|
| 1m | 最近 **7 天** | 约束最严 |
| 2m/5m/15m/30m | 最近 **60 天** | |
| 60m/90m/1h | 最近 **730 天** | |
| 1d | **无限制**（约20年+） | 最稳定 |
| 5d/1wk/1mo/3mo | **无限制** | |

### 3.4 Sector / Industry 新增 API（v1.0+）

```python
from yfinance import Sector, Industry

# 科技行业概览
tech = Sector("technology")
print(tech.top_companies)    # 头部公司 + 分析师评级
print(tech.top_etfs)         # 相关 ETF
print(tech.top_mutual_funds) # 相关公募基金

# 半导体子行业
semi = Industry("semiconductors")
print(semi.top_companies)
```

### 3.5 多 Ticker 批量操作

```python
tickers = yf.Tickers("AAPL MSFT GOOGL")
tickers.tickers["AAPL"].info       # 单独访问
tickers.download(period="1y")       # 批量下载
```

---

## 四、全球市场代码规范

| 市场 | 代码格式 | 示例 |
|------|----------|------|
| 美股 | 直接使用 | `AAPL`, `MSFT`, `TSLA` |
| 港股 | 4-5位数字 + `.HK` | `0700.HK`, `09988.HK` |
| A 股（上交所） | 6位数字 + `.SS` | `600519.SS`（贵州茅台） |
| A 股（深交所） | 6位数字 + `.SZ` | `000001.SZ`（平安银行） |
| 印度 NSE | 股票名 + `.NS` | `RELIANCE.NS` |
| 印度 BSE | 股票代码 + `.BO` | `500325.BO` |
| 指数 | `^` 前缀 | `^GSPC`（S&P500）, `^HSI`（恒指） |
| 外汇 | `XXXYYY=X` | `EURUSD=X`, `CNYJPY=X` |
| 加密货币 | `XXX-USD` | `BTC-USD`, `ETH-USD` |
| ETF | 直接使用 | `SPY`, `QQQ`, `510300.SS` |

---

## 五、快速上手代码

### 5.1 安装

```bash
pip install yfinance
pip install yfinance --upgrade   # 升级（接口变化频繁，务必保持最新）
```

### 5.2 A 股数据获取示例

```python
import yfinance as yf
import pandas as pd

# 茅台日线数据（5年）
maotai = yf.Ticker("600519.SS")
df = maotai.history(period="5y", auto_adjust=True)
print(df[['Open','High','Low','Close','Volume']].tail(10))

# 财务报表（英文，年度）
fs = maotai.financials
print(fs)
```

### 5.3 美股期权分析

```python
import yfinance as yf

aapl = yf.Ticker("AAPL")
# 获取最近到期日
exp_dates = aapl.options
print(f"可用到期日：{exp_dates[:5]}")

# 获取指定到期日的期权链
chain = aapl.option_chain(exp_dates[0])
calls = chain.calls    # 认购期权 DataFrame
puts = chain.puts      # 认沽期权 DataFrame

# 计算隐含波动率分布
import matplotlib.pyplot as plt
calls[['strike','impliedVolatility']].plot(x='strike', y='impliedVolatility', title='Call IV Smile')
plt.show()
```

### 5.4 批量回测数据准备

```python
import yfinance as yf
import pandas as pd

# 批量下载 S&P500 前10大权重股（5年日线）
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "BRK-B", "JPM", "LLY"]

# 使用 download（效率远高于逐只 Ticker.history）
df = yf.download(
    tickers,
    start="2020-01-01",
    end="2024-12-31",
    auto_adjust=True,    # 自动后复权（处理分红/拆股）
    threads=True         # 多线程下载（显著提速）
)

close = df["Close"]
returns = close.pct_change().dropna()
corr_matrix = returns.corr()
print(corr_matrix)
```

---

## 六、限流与反爬处理

### 6.1 已知问题

```
HTTP 429 Too Many Requests
- 原因：Yahoo 检测到频繁请求，触发反爬限速
- 表现：批量下载大量股票时最常见
- 影响：脚本中断，数据缺失

Possible solutions:
1. time.sleep(1~3)  ← 请求间增加延迟
2. requests_cache   ← 本地缓存，避免重复请求
3. 代理池           ← 轮换 IP 规避封禁
4. 换用付费 API     ← Polygon.io / Finnhub（生产推荐）
```

### 6.2 缓存方案（推荐）

```python
import requests_cache
import yfinance as yf

# 安装：pip install requests-cache
requests_cache.install_cache(
    'yfinance_cache',
    backend='sqlite',
    expire_after=86400  # 缓存 24 小时
)

# 此后所有 yfinance 请求自动走缓存
df = yf.download("AAPL", period="1y")  # 第一次走网络，后续命中缓存
```

### 6.3 批量下载节流封装

```python
import yfinance as yf
import time
import pandas as pd

def safe_batch_download(tickers: list, chunk_size: int = 50, delay: float = 2.0, **kwargs):
    """分块批量下载，避免 Yahoo 限流"""
    all_data = []
    for i in range(0, len(tickers), chunk_size):
        chunk = tickers[i:i+chunk_size]
        try:
            df = yf.download(chunk, **kwargs)
            all_data.append(df)
        except Exception as e:
            print(f"Chunk {i//chunk_size} failed: {e}")
        time.sleep(delay)
    return pd.concat(all_data, axis=1) if all_data else pd.DataFrame()
```

---

## 七、优势与局限性

### ✅ 优势

| 优势 | 说明 |
|------|------|
| **零配置** | 无需注册、无 API Key，`pip install` 即用 |
| **全球市场** | 覆盖 60+ 国家/地区市场 |
| **数据丰富** | OHLCV + 财务报表 + 期权链 + 新闻 + 持股 + 分析师评级 |
| **Pythonic** | DataFrame 直接返回，与 pandas/numpy 无缝集成 |
| **活跃维护** | 2025/2026 年仍持续发版 |
| **免费** | 研究/教育场景成本为零 |

### ⚠️ 局限性

| 局限 | 说明 |
|------|------|
| **非官方** | 随时可能因 Yahoo 改版失效 |
| **限流风险** | 批量请求易触发 429 封禁 |
| **A 股数据质量差** | 中文财务报表不可用，OHLCV 有时有缺口 |
| **分钟线历史短** | 1分钟仅7天，1小时仅2年 |
| **不适合生产** | 数据不稳定，不可作为交易系统数据源 |
| **数据延迟** | 实时数据通常有 15 分钟延迟（免费接口） |
| **法律灰色** | 非授权使用 Yahoo 数据，商业用途存在法律风险 |

---

## 八、适用场景

```
✅ 最适合：
  - 学术研究 / 毕业论文数据
  - 全球股票量化策略原型验证
  - 个人投资者数据分析
  - 教学示例 / Jupyter Notebook 演示
  - 快速制作可视化 Dashboard（原型阶段）
  - 期权策略研究（IV / Greeks 探索）

❌ 不适合：
  - 生产级交易系统数据源
  - 高频/日内策略（分钟线历史不足）
  - 大批量股票自动化定时下载（限流）
  - A 股专业量化（Baostock/AKShare 更优）
  - 商业产品内置数据层（法律风险）
```

---

## 九、替代方案（按场景）

| 场景 | 推荐替代 |
|------|----------|
| 美股高质量历史数据 | Polygon.io（付费，$29+/月） |
| 美股免费替代 | Finnhub（60次/分钟免费额度） |
| A 股专业数据 | Baostock / AKShare / Tushare Pro |
| 宏观经济数据 | pandas_datareader（FRED 数据库） |
| 企业基本面 | Financial Modeling Prep（FMP） |
| 低延迟实时 | IEX Cloud / Alpaca Markets API |

---

*最后更新：2025-04 | 数据截至 yfinance v1.2.1*
