---
name: baostock
description: >
  中国 A 股历史数据专家——Baostock Python SDK。当用户需要获取 A 股历史 K 线数据（日/周/月线）、
  季度财务报表（ROE/ROA/杜邦分析）、宏观经济数据（利率/M2/SHIBOR）、指数成分股历史（沪深300/中证500/上证50）、
  复权因子、交易日历、行业分类等数据时必须激活此 Skill。触发词包括但不限于：baostock、证券宝、A股历史数据、
  日线周线月线回测数据、季度财报数据、沪深300成分股历史、复权数据、量化回测数据准备、A股宏观数据、
  存款利率数据、SHIBOR、龙虎榜历史。即使用户只说"帮我下载A股历史数据""我需要沪深300的成分股"也应立即激活。
  注意：Baostock 仅覆盖 A 股，不含港股/美股/期货/期权/实时数据。
---

# Baostock Skill

## 核心定位

Baostock 是中国 A 股**最稳定的免费历史数据平台**。完全免费，无需注册，无 API Key，无调用频率限制。
数据直接来自交易所官方，质量最高。**唯一短板**：仅限 A 股，无实时数据。

## 安装

```bash
pip install baostock
# 国内加速
pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## Session 管理（必须遵守）

Baostock 使用**长连接 Session**，必须显式登录/登出：

```python
import baostock as bs
import pandas as pd

# 必须先 login
lg = bs.login()
assert lg.error_code == '0', f"Login failed: {lg.error_msg}"

# ... 业务操作 ...

# 必须 logout，否则占用连接
bs.logout()
```

**推荐封装为 Context Manager**：

```python
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

# 使用方式
with baostock_session():
    rs = bs.query_history_k_data_plus(...)
```

## ResultSet → DataFrame 工具函数

Baostock 返回自定义 ResultSet，需手动转换：

```python
def rs_to_df(rs) -> pd.DataFrame:
    rows = []
    while rs.error_code == '0' and rs.next():
        rows.append(rs.get_row_data())
    return pd.DataFrame(rows, columns=rs.fields) if rows else pd.DataFrame()
```

---

## 数据接口速查

### 1. 历史 K 线（最核心接口）

```python
rs = bs.query_history_k_data_plus(
    code="sh.600519",    # 股票代码：sh.xxxxxx 或 sz.xxxxxx
    fields="date,code,open,high,low,close,volume,amount,adjustflag,pctChg,turn",
    start_date='2020-01-01',
    end_date='2024-12-31',
    frequency="d",       # d=日 w=周 m=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟
    adjustflag="2"       # 1=后复权 2=前复权 3=不复权
)
df = rs_to_df(rs)
```

**频率与数据覆盖：**

| frequency | 说明 | 历史深度 |
|-----------|------|----------|
| `"d"` | 日线 | 1990-12-19 至今 |
| `"w"` | 周线 | 1990-12-19 至今 |
| `"m"` | 月线 | 1990-12-19 至今 |
| `"5"` | 5分钟线 | 有限（近期） |
| `"60"` | 60分钟线 | 有限（近期） |

**可用字段（fields 参数）：**

```
date, code, open, high, low, close, preclose, volume, amount,
adjustflag, turn, tradestatus, pctChg, peTTM, psTTM, pcfNcfTTM, pbMRQ, isST
```

### 2. 指数成分股（历史点位）

```python
# 沪深300（还原任意时间点成分股）
rs_hs300 = bs.query_hs300_stocks(date='2024-01-01')
df_hs300 = rs_to_df(rs_hs300)

# 中证500
rs_zz500 = bs.query_zz500_stocks(date='2024-01-01')

# 上证50
rs_sz50 = bs.query_sz50_stocks(date='2024-01-01')
```

### 3. 财务数据（季度）

```python
# 盈利能力（ROE、ROA、净利润率等）
rs = bs.query_profit_data(code="sh.600519", year=2023, quarter=4)

# 营运能力（资产周转率等）
rs = bs.query_operation_data(code="sh.600519", year=2023, quarter=4)

# 成长能力（营收增速、净利润增速）
rs = bs.query_growth_data(code="sh.600519", year=2023, quarter=4)

# 偿债能力（流动比率、速动比率）
rs = bs.query_balance_data(code="sh.600519", year=2023, quarter=4)

# 杜邦分析（5因子分解ROE）
rs = bs.query_dupont_data(code="sh.600519", year=2023, quarter=4)

# 现金流量
rs = bs.query_cash_flow_data(code="sh.600519", year=2023, quarter=4)

df = rs_to_df(rs)
```

### 4. 宏观数据

```python
# 存款利率（中国人民银行基准）
rs = bs.query_deposit_rate_data(start_date='2015-01-01', end_date='2024-12-31')

# 贷款利率
rs = bs.query_loan_rate_data(start_date='2015-01-01', end_date='2024-12-31')

# 存款准备金率
rs = bs.query_required_reserve_ratio_data(start_date='2015-01-01', end_date='2024-12-31')

# 货币供应量（M0/M1/M2）—— 月度
rs = bs.query_money_supply_data_month(start_date='2020-01', end_date='2024-12')

# SHIBOR 利率
rs = bs.query_shibor_data(start_date='2020-01-01', end_date='2024-12-31')
```

### 5. 股票基础信息

```python
# 全量股票列表（含状态、行业、上市日期）
rs = bs.query_stock_basic(code="", code_name="")  # 全部
rs = bs.query_stock_basic(code="sh.600519")        # 单只

# 交易日历
rs = bs.query_trade_dates(start_date="2024-01-01", end_date="2024-12-31")

# 行业分类（申万一级）
rs = bs.query_stock_industry()

# 历史分红送配
rs = bs.query_dividend_data(code="sh.600519", year="2023", yearType="report")

# 复权因子（用于手动复权计算）
rs = bs.query_adjust_factor(code="sh.600519", start_date="2010-01-01", end_date="2024-12-31")
```

---

## 股票代码规范

```
上交所：sh.600000（浦发银行），sh.601398（工商银行），sh.688599（天合光能 科创板）
深交所：sz.000001（平安银行），sz.300750（宁德时代 创业板）
指数：sh.000001（上证指数），sz.399001（深证成指），sh.000300（沪深300）
```

---

## 数据更新时间表

```
交易日 17:30 → 日K线
交易日 18:00 → 复权因子
次日 11:00  → 分钟K线
次日 01:30  → 财务/基本面
每周六 17:30 → 周线
每周一 下午  → 指数成分股
```

---

## 完整 Pipeline 示例：批量下载沪深300成分股日线

```python
import baostock as bs
import pandas as pd
import time

with baostock_session():
    # 1. 获取指定时间点的成分股
    rs_hs300 = bs.query_hs300_stocks(date='2024-01-02')
    hs300 = rs_to_df(rs_hs300)
    codes = hs300['code'].tolist()
    
    # 2. 批量下载（串行，注意 Baostock 无并发优化）
    all_df = []
    for code in codes:
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,close,volume,pctChg,turn",
            start_date='2024-01-01',
            end_date='2024-12-31',
            frequency="d",
            adjustflag="2"
        )
        df = rs_to_df(rs)
        if not df.empty:
            all_df.append(df)
    
    result = pd.concat(all_df, ignore_index=True)
    
print(f"下载完成，共 {len(result)} 条记录")
result.to_parquet("hs300_2024.parquet", index=False)
```

---

## 常见错误排查

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `error_code != '0'` | 登录失败/网络问题 | 检查网络，重试 |
| 返回空 DataFrame | 代码格式错误/停牌 | 检查 `sh.`/`sz.` 前缀 |
| 分钟线数据为空 | 历史太久 | 分钟线仅支持近期数据 |
| 财务接口无数据 | year/quarter 超范围 | 财务数据从 2007Q1 起 |

---

## 局限性（务必告知用户）

- ❌ **无实时行情**（最快次日 17:30 更新）
- ❌ **仅限 A 股**（无港股/美股/期货）
- ❌ **无日内分钟线历史**（历史有限）
- ❌ **串行查询**（批量下载较慢，无并发接口）
- ❌ **SDK 停更**（最新版 0.8.9，2019 年后无大版本）

如需实时数据或多市场数据，推荐改用 **AKShare**。
