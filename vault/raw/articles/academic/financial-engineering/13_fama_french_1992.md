# 论文深度解析 13/20
# Fama & French《预期股票收益率的截面特征》（1992）
## ——三因子模型：CAPM的终结者，多因子时代的开创者

---

## 一、论文基本信息

| 项目 | 内容 |
|------|------|
| **论文全名** | The Cross-Section of Expected Stock Returns |
| **作者** | Eugene F. Fama & Kenneth R. French |
| **发表时间** | 1992年6月 |
| **发表刊物** | The Journal of Finance, Vol. 47, No. 2 |
| **诺贝尔奖** | Fama 2013年获奖（部分基于此研究） |
| **引用次数** | 超过25,000次 |
| **历史意义** | 实证上宣告CAPM"死亡"，开创三因子定价框架，推动Smart Beta/因子投资革命 |

---

## 二、历史背景：CAPM在实证上的崩塌

### 2.1 一系列令人困惑的"异象"

1980年代，一系列实证研究发现了CAPM无法解释的超额收益来源：

- **规模效应（Size Effect）**：Banz（1981）——小市值股票长期跑赢大市值股票，且差异无法被 $\beta$ 解释
- **价值效应（Value Effect）**：Stattman（1980）、Rosenberg et al.（1985）——高账面市值比（B/M）股票跑赢低B/M股票
- **盈利效应**：高盈利公司股票跑赢低盈利公司
- **一月效应**：小盘股在一月份有异常高收益

这些"异象"每出现一个，都被一些人解释为CAPM的失败，也被另一些人解释为"风险的新维度"。

### 2.2 Fama & French的雄心

Fama和French决定做一件系统性的工作：**在美国所有股票的长时间历史数据上，同时检验所有主要变量对截面收益率的解释力。**

这是一项"总清算"式的研究，结论震惊了整个金融学界。

---

## 三、核心实证发现

### 3.1 数据

- 样本：1963年7月—1990年12月，纽交所（NYSE）、美交所（AMEX）和纳斯达克（NASDAQ）上市的所有非金融股票
- 月度收益率数据
- 公司财务数据：市值、账面市值比、盈利、杠杆等

### 3.2 主要发现：β 对截面收益率毫无解释力

**Fama & French (1992) 的核心结论（原文）：**

> "我们的主要结论是，β（即CAPM中唯一被定价的风险变量）不能解释预期收益率的截面差异。"

在控制规模（市值）和账面市值比（B/M）后：
- $\beta$ 的截面收益率系数**统计上不显著**（$t$值约为0）
- 而市值和B/M的系数都**高度显著**

**这几乎是CAPM的"死亡公告"。**

### 3.3 规模效应（Size Effect）

按市值将股票分成10组（从最小到最大），每组的月均收益率：

| 市值分组（10=最大） | 月均收益率 |
|-------------------|----------|
| 1（最小） | 约1.70% |
| 5 | 约1.10% |
| 10（最大） | 约0.89% |

**规模溢价（Size Premium）**：小盘股比大盘股月均高约0.8%，年化约9.6%！

### 3.4 价值效应（Value Effect）

按账面市值比（Book-to-Market Ratio，B/M）分成10组：

| B/M分组（10=最高） | 月均收益率 |
|-------------------|----------|
| 1（最低，成长股） | 约0.64% |
| 5 | 约1.17% |
| 10（最高，价值股） | 约1.65% |

**价值溢价（Value Premium）**：高B/M股票比低B/M股票月均高约1%，年化约12%！

### 3.5 规模和价值的联合解释力

当同时控制规模和B/M时，几乎可以**解释全部的截面收益率变化**，而 $\beta$ 对额外解释力的贡献可忽略不计。

---

## 四、Fama-French 三因子模型（1993）

基于1992年的实证发现，Fama & French（1993年，同样发表在Journal of Finance）提出了**三因子模型**：

$$\boxed{r_i - r_f = \alpha_i + \beta_i^{MKT}(r_M - r_f) + \beta_i^{SMB} \cdot SMB + \beta_i^{HML} \cdot HML + \epsilon_i}$$

### 4.1 三个因子的定义

**因子1：市场因子（Market Factor，RMRF）**
$$RMRF_t = r_{M,t} - r_{f,t}$$
市场组合超额收益。（保留了CAPM的市场因子）

**因子2：规模因子（Small Minus Big，SMB）**

每年6月，将股票按市值中位数分为"小盘"和"大盘"，按B/M三分为"成长（Low）"、"中（Mid）"、"价值（High）"：

$$SMB_t = \frac{1}{3}(Small/Value + Small/Neutral + Small/Growth) - \frac{1}{3}(Big/Value + Big/Neutral + Big/Growth)$$

$SMB$ 是小盘股相对大盘股的超额收益，捕捉**规模溢价**。

**因子3：价值因子（High Minus Low，HML）**

$$HML_t = \frac{1}{2}(Small/Value + Big/Value) - \frac{1}{2}(Small/Growth + Big/Growth)$$

$HML$ 是高B/M股票相对低B/M股票的超额收益，捕捉**价值溢价**。

### 4.2 历史因子溢价（美国1963-2023，月均）

| 因子 | 月均溢价 | 年化溢价 | $t$统计量 |
|------|---------|---------|---------|
| RMRF | 0.50% | 6.0% | 2.82 |
| SMB | 0.20% | 2.4% | 1.55（较弱） |
| HML | 0.37% | 4.4% | 2.78 |

---

## 五、统计检验框架

### 5.1 时序检验（Time-Series Tests）

用三因子模型对各类投资组合进行时序回归：

$$r_{P,t} - r_{f,t} = \alpha_P + \beta_P^{MKT} RMRF_t + \beta_P^{SMB} SMB_t + \beta_P^{HML} HML_t + \epsilon_{P,t}$$

若模型正确定价，**截距 $\alpha_P$ 应统计上不显著（接近零）**。

Gibbons-Ross-Shanken（GRS）检验联合检验所有组合的 $\alpha$：

$$GRS = \frac{T-N-K}{N}\left(1 + \bar{\mathbf{f}}^T \hat{\Omega}_f^{-1} \bar{\mathbf{f}}\right)^{-1} \hat{\boldsymbol{\alpha}}^T \hat{\boldsymbol{\Sigma}}^{-1} \hat{\boldsymbol{\alpha}} \sim F(N, T-N-K)$$

三因子模型对美国股票的GRS检验：$p$值显著（不能完全被接受），但远优于CAPM。

### 5.2 Fama-MacBeth 截面检验

见论文08（APT），两步回归检验各因子的截面定价能力：
- 第一步：时序回归得到因子载荷 $\hat{\beta}$
- 第二步：每期截面回归得到风险溢价估计 $\hat{\lambda}$
- 检验：$\bar{\lambda}_{SMB}$ 和 $\bar{\lambda}_{HML}$ 是否显著正

---

## 六、对规模效应和价值效应的解释之争

### 6.1 理性风险解释（Fama & French的立场）

Fama & French认为：SMB和HML是**真实风险因子**的代理：

- **规模溢价**：小公司更脆弱，在经济衰退时更可能破产，承担了"困境风险（distress risk）"
- **价值溢价**：高B/M公司往往是经营困难的"困境股（distressed stocks）"，投资者要求更高的风险溢价

这是**理性定价**的解释——规模和价值溢价是对真实风险的合理补偿。

### 6.2 行为金融解释

Lakonishok、Shleifer & Vishny（LSV, 1994）提出**非理性解释**：

- 投资者对"成长股"过度乐观（推高价格），对"价值股"过度悲观（压低价格）
- 这导致价值股被低估、成长股被高估
- 随着时间推移，价格向基本面回归，产生价值溢价

这是**错误定价（mispricing）**的解释，暗示价值投资策略可以获得真正的超额收益。

**这一争论至今未有定论，是资产定价领域最重要的未解问题之一。**

---

## 七、后续发展：因子动物园的爆发

三因子模型打开了潘多拉的盒子：

### 7.1 Carhart 四因子（1997）

加入**动量因子（Momentum，MOM/WML）**：过去12个月（排除最近1个月）收益最高的股票减去最低的：

$$r_i - r_f = \alpha_i + \beta_i^{MKT}RMRF + \beta_i^{SMB}SMB + \beta_i^{HML}HML + \beta_i^{MOM}MOM + \epsilon_i$$

### 7.2 Fama-French 五因子（2015）

Fama & French在三因子基础上加入：
- **盈利因子（Profitability，RMW）**：高盈利股票（Robust）减去低盈利（Weak）
- **投资因子（Investment，CMA）**：低投资公司（Conservative）减去高投资公司（Aggressive）

$$r_i - r_f = \alpha_i + \beta^{MKT}RMRF + \beta^{SMB}SMB + \beta^{HML}HML + \beta^{RMW}RMW + \beta^{CMA}CMA + \epsilon_i$$

### 7.3 更多因子（Harvey, Liu & Zhu 2016 统计）

超过**316个**被学术文献提出并认为"显著"的因子，包括：
- 流动性因子（Amihud, 2002）
- 质量因子（Asness et al., 2013）
- 低波动率因子（Baker et al., 2011）
- 应计利润因子（Sloan, 1996）

---

## 八、Smart Beta：三因子的产业化

Fama-French三因子模型直接催生了**Smart Beta（智慧贝塔）**投资产品：

| 策略 | 因子暴露 | 代表ETF（美国） |
|------|---------|--------------|
| 价值ETF | 高HML | VTV（Vanguard Value） |
| 小盘ETF | 高SMB | IWM（Russell 2000） |
| 动量ETF | 高MOM | MTUM |
| 质量ETF | 高RMW | QUAL |
| 多因子ETF | 综合暴露 | LRGF |

全球Smart Beta ETF规模已超过**1万亿美元**，Fama-French模型是其理论基础。

---

## 九、数据与可重复性

Ken French在其网站（mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html）免费提供：
- 三/五因子每日、每月、每年数据（更新至今）
- 25个规模-B/M组合的收益率
- 世界各地市场的因子数据

这种数据开放性是学术研究可重复性的典范，使得全球数千篇后续研究得以开展。

---

## 十、结语

Fama & French（1992/1993）是金融实证研究历史上影响最深远的论文之一。

它做了一件在当时极为勇敢的事：**用大量严格的实证证据，挑战并推翻了金融学最核心的理论——CAPM。**

更重要的是，它不仅仅是批评，而是建立了一个**替代框架**——三因子模型——既有实证基础，又有（争议中的）理论依据，而且被证明是可操作的投资策略。

这篇论文的遗产是双重的：
1. **学术上**：将实证资产定价从CAPM时代带入多因子时代
2. **实践上**：为Smart Beta/因子投资奠定了数万亿美元产业的理论基础

---

*本文为「金融工程奠基论文深度解析」系列第 13/20 篇*  
*下一篇：Heath, Jarrow & Morton (1992) · HJM框架 · 利率期限结构无套利建模的革命*
