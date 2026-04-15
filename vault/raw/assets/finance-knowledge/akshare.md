# AKShare 深度分析报告

> **定位**：开源全品类财经数据接口库 · 1000+ 接口 · 37 个数据分类 · A 股 + 全球市场

---

## 一、项目概览

| 维度 | 详情 |
|------|------|
| 最新版本 | `1.18.48`（2025 年持续更新） |
| Python 要求 | ≥ 3.9（64-bit） |
| 许可证 | MIT License |
| GitHub Stars | 10,000+ ⭐ |
| 数据源 | 东方财富、新浪财经、同花顺、金十数据等多源聚合 |
| 覆盖市场 | **A股、港股、美股、期货、期权、债券、外汇、基金、宏观** |
| 接口数量 | **1,046+** 个函数 |
| 收费方式 | **完全免费**，无需注册，无 API Key |

---

## 二、架构设计

### 2.1 数据源命名约定

AKShare 采用**函数后缀**标识数据来源：

| 后缀 | 数据源 | 特点 |
|------|--------|------|
| `_em` | 东方财富（East Money） | 最完整，实时性好 |
| `_sina` | 新浪财经 | 实时行情为主 |
| `_ths` | 同花顺 | 机构数据为主 |
| `_js` | 金十数据 | 宏观/外汇为主 |
| `_bs` | 证券宝（Baostock） | 历史数据 |
| `_qq` | 腾讯财经 | 港股/行情 |

### 2.2 模块目录结构

```
akshare/
├── stock/              # A 股核心行情
├── stock_feature/      # 龙虎榜、融资融券、北向资金
├── economic/           # 宏观经济指标
├── fund/               # 公募基金 / ETF
├── bond/               # 债券市场
├── futures/            # 期货（商品期货 / 股指期货）
├── option/             # 期权
├── forex/              # 外汇
├── crypto/             # 数字货币
├── index/              # 指数
└── news/               # 财经新闻 / 舆情
```

---

## 三、核心数据能力矩阵

### 3.1 股票行情

| 接口 | 功能 | 示例 |
|------|------|------|
| `stock_zh_a_hist` | A 股历史 OHLCV（日/周/月） | `ak.stock_zh_a_hist(symbol="000001", period="daily")` |
| `stock_zh_a_spot_em` | A 股实时行情（全市场） | `ak.stock_zh_a_spot_em()` |
| `stock_zh_a_minute` | A 股分钟级实时数据 | `ak.stock_zh_a_minute(symbol="sh000001")` |
| `stock_us_daily` | 美股历史行情 | `ak.stock_us_daily(symbol="AAPL")` |
| `stock_hk_daily` | 港股历史行情 | `ak.stock_hk_daily(symbol="00700")` |
| `stock_zh_a_gdp` | 中国 GDP 数据 | - |

### 3.2 基本面与财务

| 接口 | 功能 |
|------|------|
| `stock_financial_report_sina` | 财务三表（资产负债表/利润表/现金流量表） |
| `stock_profit_sheet_by_annual_em` | 利润表（年度，东财） |
| `stock_balance_sheet_by_annual_em` | 资产负债表（年度，东财） |
| `stock_cash_flow_sheet_by_annual_em` | 现金流量表（年度，东财） |
| `stock_financial_abstract_ths` | 财务摘要（同花顺） |
| `stock_fhps_em` | 历史分红数据 |
| `stock_ipo_info` | IPO 信息 |

### 3.3 特色数据

| 接口 | 功能 |
|------|------|
| `stock_lhb_detail_daily_sina` | 龙虎榜详情 |
| `stock_margin_detail_szse` | 融资融券明细（深交所） |
| `stock_hsgt_north_net_flow_in_em` | 北向资金净流入（沪深港通） |
| `stock_hsgt_hist_em` | 北向/南向资金历史 |
| `stock_concept_cons_em` | 概念板块成分股 |
| `stock_board_industry_hist_em` | 行业板块历史行情 |
| `stock_analyst_rank_em` | 分析师评级 |
| `stock_research_report_em` | 研报数据 |

### 3.4 宏观经济

```python
import akshare as ak

# CPI 数据
cpi_df = ak.macro_china_cpi()
# 输出：日期 全国CPI 城市CPI 农村CPI

# GDP 数据
gdp_df = ak.macro_china_gdp()

# M0/M1/M2 货币供应量
m2_df = ak.macro_china_money_supply()

# PMI
pmi_df = ak.macro_china_pmi()

# 非农就业（美国）
nonfarm_df = ak.macro_usa_non_farm()

# LME 铜价
lme_df = ak.futures_lme_hist(symbol="LME铜")
```

### 3.5 基金与 ETF

```python
# 实时 ETF 行情（全量）
etf_df = ak.fund_etf_spot_em()

# 场内基金历史净值
fund_df = ak.fund_etf_hist_em(symbol="510300", period="daily")

# 场外基金每日净值
open_fund_df = ak.fund_open_fund_daily_em(symbol="000001")

# 基金持仓（十大重仓股）
holding_df = ak.fund_portfolio_hold_em(symbol="000001", date="2024")
```

### 3.6 期货与期权

```python
# 商品期货实时行情
futures_df = ak.futures_zh_spot(symbol="螺纹钢", market="SHFE")

# 期权链（上证 50ETF 期权）
option_df = ak.option_current_em(symbol="上证50ETF期权")

# 大商所交割统计
dalian_df = ak.futures_dce_delivery()

# 国际期货（LME/CBOT/NYMEX）
intl_df = ak.futures_global_commodity_hist(symbol="黄金")
```

---

## 四、快速上手代码

### 4.1 安装

```bash
pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com --upgrade

# Docker 方式（推荐生产环境）
docker pull registry.cn-shanghai.aliyuncs.com/akfamily/aktools:jupyter
docker run -it -p 8888:8888 registry.cn-shanghai.aliyuncs.com/akfamily/aktools:jupyter
```

### 4.2 A 股标准化历史数据获取

```python
import akshare as ak
import pandas as pd

# 获取平安银行 (000001) 日线数据
df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",           # daily / weekly / monthly
    start_date="20200101",
    end_date="20241231",
    adjust="hfq"              # "" 不复权 / "qfq" 前复权 / "hfq" 后复权
)
print(df.columns.tolist())
# ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']

df['日期'] = pd.to_datetime(df['日期'])
df.set_index('日期', inplace=True)
```

### 4.3 全市场实时行情快照

```python
import akshare as ak

# 获取全量 A 股实时行情（约 5000 只股票）
spot_df = ak.stock_zh_a_spot_em()
print(spot_df.head())
# 返回：代码、名称、涨跌幅、最新价、成交量、换手率、市盈率 等
```

### 4.4 北向资金监控

```python
import akshare as ak

# 当日北向资金净流入（实时）
north_df = ak.stock_hsgt_north_net_flow_in_em(symbol="沪深港通北向资金")

# 历史北向资金
hist_df = ak.stock_hsgt_hist_em(symbol="北向资金")
```

### 4.5 多维度量化选股 Pipeline

```python
import akshare as ak
import pandas as pd

# Step 1: 全市场快照（过滤 ST 和停牌）
spot = ak.stock_zh_a_spot_em()
spot = spot[~spot['名称'].str.contains('ST|退')]
spot = spot[spot['成交量'] > 0]

# Step 2: 按换手率 + 涨跌幅初步筛选
candidates = spot[
    (spot['换手率'] > 2) &
    (spot['涨跌幅'] > 3) &
    (spot['涨跌幅'] < 9.5)
]['代码'].tolist()

# Step 3: 拉取龙虎榜（近期强势股验证）
lhb = ak.stock_lhb_detail_daily_sina(date="20241231")

print(f"初筛股票数量: {len(candidates)}")
```

---

## 五、AKTools：HTTP API 层

AKShare 官方提供 **AKTools** 项目，将所有 Python 函数封装为 FastAPI 服务，供非 Python 环境调用：

```bash
# 启动本地服务
pip install aktools
python -m aktools

# 调用示例（curl）
curl "http://127.0.0.1:8080/api/public/stock_zh_a_hist?symbol=000001&period=daily&start_date=20240101&end_date=20241231&adjust=qfq"
```

支持 Docker 一键部署，适合 Agent 系统集成。

---

## 六、优势与局限性

### ✅ 优势

| 优势 | 说明 |
|------|------|
| **接口最广** | 1046+ 函数，覆盖 A股/港股/美股/期货/基金/宏观 |
| **持续维护** | 2025 年仍保持高频迭代（每月多次发版） |
| **完全免费** | 无注册、无 Key、无配额 |
| **多市场** | 中国 + 全球主流市场 |
| **HTTP API** | AKTools 提供跨语言调用 |
| **生态丰富** | AKQuant（Rust 回测框架）原生集成 |

### ⚠️ 局限性

| 局限 | 说明 |
|------|------|
| **数据源稳定性** | 依赖公开爬取，个别接口可能因网站改版失效 |
| **接口碎片化** | 1000+ 函数命名不完全统一，学习成本较高 |
| **无质量保证** | 非官方数据源，偶有脏数据或延迟 |
| **并发不友好** | 批量请求容易触发目标网站限流 |
| **文档滞后** | 新接口往往先于文档更新发布 |
| **无历史深度保障** | 部分接口历史数据有限（特别是分钟级） |

---

## 七、与其他库对比定位

```
Baostock  ←  稳定 / A股 / 历史 / 官方数据质量最高
AKShare   ←  广度 / 多品类 / 最新 / 社区生态最佳
yfinance  ←  全球 / 英文生态 / 快速上手
Tushare   ←  专业 / 需积分 / 数据质量高
```

---

## 八、生产实践建议

```python
# 1. 容错封装（接口可能因数据源改版暂时失效）
import time, logging
from functools import wraps

def ak_retry(max_retry=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"AKShare {func.__name__} attempt {attempt+1} failed: {e}")
                    if attempt < max_retry - 1:
                        time.sleep(delay)
            raise RuntimeError(f"AKShare {func.__name__} failed after {max_retry} attempts")
        return wrapper
    return decorator

@ak_retry(max_retry=3)
def safe_get_hist(symbol, start, end):
    return ak.stock_zh_a_hist(symbol=symbol, start_date=start, end_date=end, adjust="hfq")

# 2. 批量并发（使用 ThreadPoolExecutor 规避 GIL）
from concurrent.futures import ThreadPoolExecutor
import akshare as ak

def fetch_stock(code):
    try:
        return ak.stock_zh_a_hist(symbol=code, period="daily",
                                    start_date="20240101", end_date="20241231")
    except:
        return None

codes = ["000001", "000002", "600000", "600519"]
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch_stock, codes))

# 3. 版本锁定（避免上游改版导致接口突变）
# requirements.txt: akshare==1.18.48
```

---

## 九、2025 年重要更新亮点

- **质押股比接口重构**：增加行业分类、平均质押比例等多维字段
- **国际期货扩展**：新增 LME/CBOT/NYMEX 实时报价接口
- **转期现数据**：郑商所/大商所/上期所期转现明细
- **回购利率接口**：银行间流动性监测新维度
- **AKQuant 集成**：Rust 高性能回测框架原生支持 AKShare 数据格式

---

*最后更新：2025-04 | 数据截至 akshare v1.18.48*
