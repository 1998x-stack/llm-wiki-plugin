---
name: akshare
description: >
  全品类中国财经数据专家——AKShare Python 库（1046+ 接口，37 个数据类别）。当用户需要以下任何数据时必须激活：
  A股实时行情/历史数据、港股/美股数据、ETF/基金净值、期货/期权行情、债券数据、外汇汇率、宏观经济（GDP/CPI/PMI/M2）、
  北向资金/沪深港通、龙虎榜/融资融券、行业板块数据、概念板块、研究报告、分析师评级、新闻舆情、商品期货（螺纹钢/铜/原油）、
  数字货币、国际期货（LME/CBOT/NYMEX）。触发关键词：akshare、东方财富、新浪财经数据、A股实时、全市场快照、
  北向资金、融资融券、龙虎榜、基金净值、期货行情、宏观数据、财经多品类、quantitative。
  即使用户只说"帮我查一下今天A股行情""我需要基金净值数据""北向资金今天流入多少"也应立即激活。
---

# AKShare Skill

## 核心定位

AKShare 是 **Python 财经数据库中接口最广**的开源库：1046+ 函数，覆盖 A 股、港股、美股、期货、期权、债券、
外汇、基金、宏观经济、数字货币、国际期货。完全免费，无需注册，持续高频迭代（2025 年仍活跃维护）。

## 安装

```bash
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com --upgrade
```

## 数据源命名约定（函数后缀）

| 后缀 | 数据源 | 特点 |
|------|--------|------|
| `_em` | 东方财富 | 最完整，实时性好 |
| `_sina` | 新浪财经 | 实时行情为主 |
| `_ths` | 同花顺 | 机构数据为主 |
| `_js` | 金十数据 | 宏观/外汇为主 |
| `_bs` | 证券宝 | 历史数据 |

---

## 核心接口速查

### A 股行情

```python
import akshare as ak

# ── 历史 K 线（最常用）──────────────────────────────
df = ak.stock_zh_a_hist(
    symbol="000001",          # 6位纯数字，无前缀
    period="daily",           # daily / weekly / monthly
    start_date="20200101",    # yyyymmdd 格式
    end_date="20241231",
    adjust="hfq"              # "" 不复权 / "qfq" 前复权 / "hfq" 后复权
)
# 列名（中文）：日期 开盘 收盘 最高 最低 成交量 成交额 振幅 涨跌幅 涨跌额 换手率

# ── 全市场实时快照（约5000只股票）──────────────────
spot_df = ak.stock_zh_a_spot_em()
# 包含：代码 名称 最新价 涨跌幅 换手率 市盈率 市净率 总市值 等

# ── 实时分钟数据──────────────────────────────────────
min_df = ak.stock_zh_a_minute(symbol="sh000001", period="5", adjust="qfq")

# ── 科创板 / 创业板──────────────────────────────────
kcb_df = ak.stock_zh_a_hist(symbol="688599", period="daily", start_date="20230101", adjust="hfq")
```

### 北向资金 & 沪深港通

```python
# 当日北向资金净流入（实时）
north_flow = ak.stock_hsgt_north_net_flow_in_em(symbol="沪深港通北向资金")

# 历史北向资金趋势
north_hist = ak.stock_hsgt_hist_em(symbol="北向资金")

# 沪股通十大成交活跃股
top_sh = ak.stock_hsgt_top10_em(market="沪股通", start_date="20240101", end_date="20241231")

# 深股通十大成交活跃股
top_sz = ak.stock_hsgt_top10_em(market="深股通", start_date="20240101", end_date="20241231")
```

### 龙虎榜

```python
# 当日龙虎榜详情
lhb_df = ak.stock_lhb_detail_daily_sina(date="20241231")

# 龙虎榜历史统计（特定营业部）
seat_df = ak.stock_lhb_hyyyb_em(start_date="20240101", end_date="20241231")
```

### 融资融券

```python
# 融资融券明细（上交所）
margin_sh = ak.stock_margin_detail_sse(date="20241231")

# 融资融券明细（深交所）
margin_sz = ak.stock_margin_detail_szse(date="20241231")

# 两市融资余额汇总
margin_total = ak.stock_margin_sz_sse_em()
```

### 基金 & ETF

```python
# 场内 ETF 实时行情（全量）
etf_spot = ak.fund_etf_spot_em()

# ETF 历史净值（场内，如沪深300ETF）
etf_hist = ak.fund_etf_hist_em(symbol="510300", period="daily", adjust="qfq")

# 场外基金每日净值（如天弘余额宝货币）
fund_nav = ak.fund_open_fund_daily_em(symbol="000001")

# 基金十大重仓股（季度持仓）
fund_holding = ak.fund_portfolio_hold_em(symbol="110011", date="2024")

# 公募基金规模排行
fund_rank = ak.fund_aum_em()
```

### 宏观经济数据

```python
# 中国 CPI
cpi = ak.macro_china_cpi()
# 列：日期 全国CPI 城市CPI 农村CPI

# 中国 GDP（季度）
gdp = ak.macro_china_gdp()

# PMI（制造业）
pmi = ak.macro_china_pmi()

# M0/M1/M2 货币供应量
money = ak.macro_china_money_supply()

# LPR 贷款市场报价利率
lpr = ak.macro_china_lpr()

# 美国非农就业
nonfarm = ak.macro_usa_non_farm()

# 美国 CPI
us_cpi = ak.macro_usa_cpi()
```

### 期货 & 商品

```python
# A 股期货实时行情（上期所螺纹钢）
futures_spot = ak.futures_zh_spot(symbol="螺纹钢", market="SHFE")

# 期货历史行情
futures_hist = ak.futures_main_sina(symbol="RB0", start_date="20240101")
# RB=螺纹钢 CU=铜 AU=黄金 AG=白银 AL=铝

# 国际期货（LME/CBOT/NYMEX）
intl_futures = ak.futures_global_commodity_hist(symbol="黄金")

# 大商所交割统计
dce_delivery = ak.futures_dce_delivery()
```

### 期权

```python
# 上证50ETF期权实时行情
option_df = ak.option_current_em(symbol="上证50ETF期权")

# 期权历史数据
option_hist = ak.option_sse_hist_daily_em(symbol="10004971")
```

### 行业 & 板块

```python
# 行业板块实时行情
industry_spot = ak.stock_board_industry_name_em()

# 行业板块历史行情
industry_hist = ak.stock_board_industry_hist_em(
    symbol="半导体",
    period="daily",
    start_date="20230101",
    end_date="20241231",
    adjust="qfq"
)

# 概念板块成分股
concept_cons = ak.stock_board_concept_cons_em(symbol="AIGC")

# 指数成分股（沪深300）
hs300_cons = ak.index_stock_cons(symbol="000300")
```

### 财务报表

```python
# 利润表（年度，东方财富）
income = ak.stock_profit_sheet_by_annual_em(symbol="000001")

# 资产负债表（年度）
balance = ak.stock_balance_sheet_by_annual_em(symbol="000001")

# 现金流量表（年度）
cashflow = ak.stock_cash_flow_sheet_by_annual_em(symbol="000001")

# 财务摘要（同花顺多指标）
summary = ak.stock_financial_abstract_ths(symbol="000001", indicator="按年度")
```

---

## AKTools HTTP API

AKShare 提供 HTTP API 层（FastAPI），供非 Python 环境调用：

```bash
pip install aktools
python -m aktools   # 默认启动在 http://127.0.0.1:8080

# curl 调用示例
curl "http://127.0.0.1:8080/api/public/stock_zh_a_hist?symbol=000001&period=daily&start_date=20240101&end_date=20241231&adjust=qfq"
```

适合 Agent 系统、Go/Java/Node 服务集成。

---

## 容错封装（生产级）

```python
import time, logging, functools
import akshare as ak

def ak_retry(max_retry=3, delay=2.0):
    """AKShare 接口容错重试装饰器（部分接口因数据源改版偶发失效）"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"AKShare attempt {attempt+1}/{max_retry} - {func.__name__}: {e}")
                    if attempt < max_retry - 1:
                        time.sleep(delay)
            raise RuntimeError(f"AKShare {func.__name__} failed after {max_retry} retries")
        return wrapper
    return decorator

@ak_retry(max_retry=3)
def safe_stock_hist(symbol, start, end, adjust="hfq"):
    return ak.stock_zh_a_hist(symbol=symbol, period="daily",
                               start_date=start, end_date=end, adjust=adjust)
```

---

## 批量下载（并发安全）

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import akshare as ak
import time

def fetch_single(code: str) -> dict:
    time.sleep(0.5)  # 适当限速，避免触发目标网站封禁
    df = ak.stock_zh_a_hist(symbol=code, period="daily",
                              start_date="20240101", end_date="20241231", adjust="hfq")
    return {"code": code, "data": df}

codes = ["000001", "000002", "600000", "600519", "300750"]

with ThreadPoolExecutor(max_workers=3) as executor:  # 并发数不宜过高
    futures = {executor.submit(fetch_single, c): c for c in codes}
    results = {}
    for fut in as_completed(futures):
        r = fut.result()
        results[r["code"]] = r["data"]
```

---

## 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `empty DataFrame` | 接口暂时失效（目标网站改版） | 升级 akshare，换用同类接口 |
| 网络超时 | 请求外网数据源 | 配置代理或使用国内源接口 |
| 字段变化 | 上游数据源调整 | `pip install akshare --upgrade` |
| 频繁失败 | 被目标网站限流 | 增加 sleep，降低并发 |

---

## 局限性（务必告知用户）

- ⚠️ **接口稳定性**：依赖公开爬取，个别接口因网站改版偶发失效，升级版本可修复
- ⚠️ **无官方质量保障**：非官方数据源，偶有脏数据
- ⚠️ **接口碎片化**：1000+ 函数，命名不完全统一，查文档成本较高
- ⚠️ **批量限流**：短时间大量请求可能触发目标网站封禁

如需最高质量 A 股历史数据（官方来源），改用 **Baostock**。
