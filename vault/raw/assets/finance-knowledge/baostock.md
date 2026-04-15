# Baostock 深度分析报告

> **定位**：中国 A 股免费历史数据平台 · Python SDK · 无需注册 · 无调用频率限制

---

## 一、项目概览

| 维度 | 详情 |
|------|------|
| 最新版本 | `0.8.9` |
| Python 要求 | ≥ 3.6（64-bit） |
| 许可证 | BSD License |
| 数据源 | 官方交易所数据（上交所 / 深交所） |
| 覆盖市场 | **中国 A 股**（沪深两市） |
| 收费方式 | **完全免费**，无需注册，无 API Key |
| 历史深度 | K 线数据从 **1990-12-19** 至今 |
| 财务数据 | 从 **2007 年**起季度财报 |

---

## 二、核心数据能力矩阵

### 2.1 行情数据

| 数据类型 | 频率 | 起始时间 | 复权支持 |
|----------|------|----------|----------|
| 日 K 线（OHLCV） | 每日 17:30 更新 | 1990-12-19 | 前复权/后复权/不复权 |
| 周 K 线 | 每周六 17:30 | 1990-12-19 | ✅ |
| 月 K 线 | 每月 | 1990-12-19 | ✅ |
| 分钟 K 线（1/5/15/30/60min） | 次日 11:00 | 近期 | ✅ |
| 指数日线（上证、深证、沪深300等） | 每日 | 1990 年代 | ✅ |

### 2.2 基本面数据

| 数据接口 | 覆盖时间 | 说明 |
|----------|----------|------|
| 季度盈利能力 | 2007Q1–今 | ROE/ROA/净利润率 |
| 季度营运能力 | 2007Q1–今 | 资产/应收账款周转率 |
| 季度成长能力 | 2007Q1–今 | 营收/净利润增速 |
| 季度偿债能力 | 2007Q1–今 | 流动/速动比率 |
| 杜邦分析 | 2007Q1–今 | 5 因子分解 |
| 现金流量 | 2007Q1–今 | 经营/投资/筹资活动 |
| 业绩预告 | 2003 年起 | 事件驱动型策略核心 |
| 业绩快报 | 2006 年起 | 比正式报告早约 1 周 |

### 2.3 市场结构数据

| 接口 | 说明 |
|------|------|
| `query_stock_basic` | 全量股票列表 + 状态 |
| `query_trade_dates` | 历史交易日历 |
| `query_sz50_stocks` | 上证50成分股（每周一更新） |
| `query_hs300_stocks` | 沪深300成分股（每周一更新） |
| `query_zz500_stocks` | 中证500成分股（每周一更新） |
| `query_stock_industry` | 行业分类（申万一级） |
| `query_dividend_data` | 历史分红送配数据 |
| `query_adjust_factor` | 复权因子（每日 18:00 更新） |

### 2.4 宏观数据

| 接口 | 内容 |
|------|------|
| `query_deposit_rate_data` | 存款基准利率 |
| `query_loan_rate_data` | 贷款基准利率 |
| `query_required_reserve_ratio_data` | 存款准备金率 |
| `query_money_supply_data_month` | M0/M1/M2 月度 |
| `query_money_supply_data_year` | M0/M1/M2 年度 |
| `query_shibor_data` | SHIBOR 利率 |

---

## 三、数据更新时间表

```
交易日:
  17:30 → 日 K 线数据
  18:00 → 复权因子
  次日 11:00 → 分钟 K 线
  次日 01:30 → 财务/基本面数据

每周六 17:30 → 周线
每周一下午 → 指数成分股更新（50/300/500）
```

---

## 四、技术架构

```
Baostock SDK
    ↓ TCP 长连接（非 HTTP REST）
证券宝数据服务器
    ↓
交易所官方数据源
```

**关键设计特点：**
- 采用**会话（Session）机制**，需显式 `login()` / `logout()`
- 使用**分页迭代**（`rs.next()`）而非一次性返回，适合大数据量
- 返回格式为**自定义 ResultSet**，需手动转换为 DataFrame
- 无 HTTP 接口，不支持其他语言直接调用

---

## 五、快速上手代码

### 5.1 安装

```bash
# 标准安装
pip install baostock

# 国内加速（推荐）
pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 5.2 获取历史 K 线（工业银行 sh.601398）

```python
import baostock as bs
import pandas as pd

# 登录
lg = bs.login()
assert lg.error_code == '0', f"Login failed: {lg.error_msg}"

# 查询日线数据
rs = bs.query_history_k_data_plus(
    code="sh.601398",
    fields="date,code,open,high,low,close,volume,amount,adjustflag,pctChg",
    start_date='2020-01-01',
    end_date='2024-12-31',
    frequency="d",       # d=日线, w=周线, m=月线, 5=5分钟
    adjustflag="3"       # 1=后复权, 2=前复权, 3=不复权
)

# 分页读取
rows = []
while rs.error_code == '0' and rs.next():
    rows.append(rs.get_row_data())

df = pd.DataFrame(rows, columns=rs.fields)
df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].apply(pd.to_numeric)
df['date'] = pd.to_datetime(df['date'])

bs.logout()
print(df.tail())
```

### 5.3 批量获取沪深300成分股历史数据

```python
import baostock as bs
import pandas as pd
from datetime import datetime

bs.login()

# 获取成分股列表
rs_hs300 = bs.query_hs300_stocks(date='2024-01-01')
stocks = []
while rs_hs300.error_code == '0' and rs_hs300.next():
    stocks.append(rs_hs300.get_row_data())
stock_df = pd.DataFrame(stocks, columns=rs_hs300.fields)

# 批量下载
all_data = []
for code in stock_df['code'].tolist()[:5]:  # 示例取前5只
    rs = bs.query_history_k_data_plus(
        code, "date,code,close,pctChg",
        start_date='2024-01-01',
        end_date='2024-12-31',
        frequency="d", adjustflag="2"
    )
    rows = []
    while rs.error_code == '0' and rs.next():
        rows.append(rs.get_row_data())
    all_data.extend(rows)

df = pd.DataFrame(all_data, columns=['date','code','close','pctChg'])
bs.logout()
```

### 5.4 获取季度 ROE 数据

```python
bs.login()
rs = bs.query_roa_data(code="sh.601398", year="2023", quarter="4")
while rs.error_code == '0' and rs.next():
    print(rs.get_row_data())
bs.logout()
```

---

## 六、优势与局限性

### ✅ 优势

| 优势 | 说明 |
|------|------|
| **完全免费** | 无 API Key，无注册，无调用限制 |
| **数据权威** | 直接来自交易所官方数据 |
| **历史深度长** | A 股日线从 1990 年至今 |
| **财务数据完备** | 季度三张表 + 杜邦分析体系 |
| **宏观数据集成** | 利率/准备金/货币供应量 |
| **指数成分历史** | 可还原任意时间点的指数成分股 |

### ⚠️ 局限性

| 局限 | 说明 |
|------|------|
| **仅限 A 股** | 不覆盖港股、美股、期货、期权 |
| **无实时数据** | 最快次日更新，不适合日内策略 |
| **分钟线历史短** | 历史分钟线数据有限，不可溯源多年 |
| **SDK 已停更** | 最新版本 0.8.9，2019 年后无大版本更新 |
| **API 风格老旧** | 分页迭代设计繁琐，需手工转 DataFrame |
| **无 HTTP 接口** | 无法在非 Python 环境直接使用 |
| **并发差** | 单连接串行查询，批量下载慢 |

---

## 七、适用场景

```
✅ 最适合：
  - A 股量化策略回测（日频/周频）
  - 基本面选股模型（ROE/ROA/成长性筛选）
  - 宏观-行业-个股三层联动分析
  - 指数成分股历史变动研究
  - 学术研究 / 毕业论文数据获取

❌ 不适合：
  - 实时行情监控
  - 期货/期权/外汇策略
  - 港股 / 美股研究
  - 分钟级高频回测
  - 生产级交易系统数据源
```

---

## 八、与其他库对比

| 特性 | Baostock | AKShare | yfinance | Tushare Pro |
|------|----------|---------|----------|-------------|
| A 股日线 | ✅ 1990- | ✅ | ✅ 有限 | ✅ |
| 财务报表 | ✅ 季度 | ✅ | ✅ 年报 | ✅ |
| 实时行情 | ❌ | ✅ | ✅ | ✅ |
| 港股/美股 | ❌ | ✅ | ✅ | 部分 |
| 期货/期权 | ❌ | ✅ | 部分 | ✅ |
| 需要注册 | ❌ | ❌ | ❌ | ✅（积分） |
| 调用限制 | 无 | 无（部分源有） | Yahoo 限流 | 有积分上限 |
| 数据质量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| API 设计 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 九、生产实践建议

```python
# 1. 封装 Context Manager 避免忘记 logout
from contextlib import contextmanager
import baostock as bs

@contextmanager
def baostock_session():
    lg = bs.login()
    if lg.error_code != '0':
        raise RuntimeError(f"Baostock login failed: {lg.error_msg}")
    try:
        yield
    finally:
        bs.logout()

with baostock_session():
    rs = bs.query_history_k_data_plus("sh.600000", "date,close", 
                                       start_date='2024-01-01', frequency="d")
    # ...

# 2. 统一 ResultSet → DataFrame 工具函数
def rs_to_df(rs) -> pd.DataFrame:
    rows = []
    while rs.error_code == '0' and rs.next():
        rows.append(rs.get_row_data())
    return pd.DataFrame(rows, columns=rs.fields) if rows else pd.DataFrame()

# 3. 本地缓存（避免重复请求）
import os, pickle
CACHE_DIR = "./baostock_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cached_kdata(code, start, end, freq="d", adjust="3"):
    key = f"{code}_{start}_{end}_{freq}_{adjust}.pkl"
    path = os.path.join(CACHE_DIR, key)
    if os.path.exists(path):
        return pickle.load(open(path, 'rb'))
    with baostock_session():
        rs = bs.query_history_k_data_plus(
            code, "date,open,high,low,close,volume,amount",
            start_date=start, end_date=end,
            frequency=freq, adjustflag=adjust
        )
        df = rs_to_df(rs)
    pickle.dump(df, open(path, 'wb'))
    return df
```

---

## 十、股票代码规范

```
上海证券交易所：sh.xxxxxx
  sh.600000  浦发银行
  sh.601398  工业银行
  sh.000001  上证指数（指数）

深圳证券交易所：sz.xxxxxx
  sz.000001  平安银行
  sz.300750  宁德时代
  sz.399001  深证成指（指数）

科创板：sh.688xxx
  sh.688599  天合光能

创业板：sz.300xxx
  sz.300015  爱尔眼科
```

---

*最后更新：2025-04 | 数据截至版本 baostock 0.8.9*
