# 论文深度解析 11/20
# 罗伯特·恩格尔《自回归条件异方差模型及英国通胀方差的估计》（1982）
## ——ARCH：波动率聚集的统计学发现，时间序列的革命

---

## 一、论文基本信息

| 项目 | 内容 |
|------|------|
| **论文全名** | Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation |
| **作者** | Robert Fry Engle III（罗伯特·恩格尔） |
| **发表时间** | 1982年7月 |
| **发表刊物** | Econometrica, Vol. 50, No. 4 |
| **诺贝尔奖** | 2003年经济学奖（与Clive Granger共享） |
| **核心贡献** | 自回归条件异方差（ARCH）模型，将时间序列方差建模为可预测的动态过程 |
| **引用次数** | 超过25,000次，计量经济学史上被引用最多的论文之一 |

---

## 二、问题的起源：波动率的"记忆"

### 2.1 金融市场的一个显著特征

任何观察过金融市场的人都会注意到一个现象：

**"大波动之后跟大波动，小波动之后跟小波动。"**

这被称为**波动率聚集（Volatility Clustering）**：市场的波动率不是恒定的，它在时间上是**有记忆、可预测的**。

直观例子：2008年金融危机期间，标普500指数每天上下波动4-8%；而在平静时期，每天只波动0.5-1%。

### 2.2 传统计量经济学的局限

在ARCH之前，时间序列模型（如ARMA）假设误差项 $\epsilon_t$ 是**独立同分布（i.i.d.）**的：

$$r_t = \mu + \epsilon_t, \quad \epsilon_t \sim i.i.d. \mathcal{N}(0, \sigma^2)$$

这意味着**方差 $\sigma^2$ 是常数**。

但实际金融数据显示：
- 误差项的平方（代表方差）存在显著的**自相关性**
- 这违反了OLS回归的同方差假设
- 导致标准误估计错误，推断失效

### 2.3 Engle的洞察

Engle（当时在加州大学圣地亚哥分校）注意到：**方差本身是随时间变化的，且这种变化是可以用过去信息预测的——但预测的是方差，不是均值。**

这个洞察导致了ARCH模型的诞生。

---

## 三、ARCH模型的数学框架

### 3.1 ARCH(q) 模型定义

**自回归条件异方差（Autoregressive Conditional Heteroscedasticity，ARCH）模型：**

$$r_t = \mu_t + \epsilon_t$$
$$\epsilon_t = \sigma_t z_t, \quad z_t \sim i.i.d. \mathcal{N}(0, 1)$$
$$\sigma_t^2 = \omega + \alpha_1 \epsilon_{t-1}^2 + \alpha_2 \epsilon_{t-2}^2 + ... + \alpha_q \epsilon_{t-q}^2$$

参数约束（确保方差为正）：$\omega > 0$，$\alpha_i \geq 0$。

**关键特性：**
- $z_t$ 是i.i.d.的，但 $\epsilon_t$ **不是i.i.d.的**（因为条件方差 $\sigma_t^2$ 时变）
- 在给定过去信息 $\mathcal{F}_{t-1}$ 的条件下，$\epsilon_t | \mathcal{F}_{t-1} \sim \mathcal{N}(0, \sigma_t^2)$
- 当 $\alpha_i = 0$ 时，退化为常数方差（传统模型）

### 3.2 ARCH(1) 的详细分析

最简单的情形 ARCH(1)：

$$\sigma_t^2 = \omega + \alpha_1 \epsilon_{t-1}^2$$

**无条件方差（长期均值）：**
$$\text{Var}(\epsilon_t) = \frac{\omega}{1 - \alpha_1} \quad \text{（需要 } \alpha_1 < 1 \text{）}$$

**四阶矩（厚尾）：**

ARCH(1)模型生成的 $\epsilon_t$ 的**峰度（Kurtosis）**：

$$\kappa = 3 \cdot \frac{1 - \alpha_1^2}{1 - 3\alpha_1^2} > 3 \quad \text{（需要 } \alpha_1 < \frac{1}{\sqrt{3}} \text{）}$$

这解释了为什么金融收益率往往呈现**超额峰度（Fat Tails）**！

**自相关结构：**
- $\epsilon_t$ 本身**无自相关**（白噪声）
- $\epsilon_t^2$（方差的代理）有显著的**正自相关**

$$\text{Corr}(\epsilon_t^2, \epsilon_{t-k}^2) = \alpha_1^k$$

这正是波动率聚集的数学体现。

---

## 四、ARCH的统计推断

### 4.1 最大似然估计

ARCH参数通过**最大似然估计（MLE）**：

对数似然函数：

$$\mathcal{L}(\theta) = -\frac{T}{2}\ln(2\pi) - \frac{1}{2}\sum_{t=1}^T \left[\ln(\sigma_t^2) + \frac{\epsilon_t^2}{\sigma_t^2}\right]$$

其中 $\sigma_t^2$ 依赖于参数 $\theta = (\omega, \alpha_1, ..., \alpha_q)$，通过递推计算：
$$\sigma_1^2 = \omega / (1 - \alpha_1) \quad \text{（用无条件方差初始化）}$$
$$\sigma_t^2 = \omega + \sum_{i=1}^q \alpha_i \hat{\epsilon}_{t-i}^2 \quad t = 2, ..., T$$

### 4.2 ARCH-LM 检验（Lagrange Multiplier Test）

**检验 $H_0$：无ARCH效应（$\alpha_1 = ... = \alpha_q = 0$）**

步骤：
1. 对时间序列拟合均值方程，得到残差 $\hat{\epsilon}_t$
2. 对 $\hat{\epsilon}_t^2$ 对其滞后项回归：
   $$\hat{\epsilon}_t^2 = c + a_1 \hat{\epsilon}_{t-1}^2 + ... + a_q \hat{\epsilon}_{t-q}^2 + v_t$$
3. **ARCH-LM 统计量**：$LM = T \cdot R^2 \sim \chi^2(q)$

$R^2$ 越大，说明残差平方越具有可预测性，ARCH效应越显著。

---

## 五、GARCH：Bollerslev（1986）的推广

Engle的ARCH模型需要很多滞后项才能捕捉持续的波动率聚集。Tim Bollerslev（1986，Engle的学生）提出**广义ARCH（GARCH）**，优雅地解决了这个问题。

### 5.1 GARCH(p,q) 模型

$$\sigma_t^2 = \omega + \sum_{i=1}^q \alpha_i \epsilon_{t-i}^2 + \sum_{j=1}^p \beta_j \sigma_{t-j}^2$$

实践中，**GARCH(1,1)** 是最广泛使用的模型：

$$\boxed{\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2}$$

参数约束：$\omega > 0$，$\alpha \geq 0$，$\beta \geq 0$，$\alpha + \beta < 1$（平稳性）。

### 5.2 GARCH(1,1) 的解读

$$\underbrace{\sigma_t^2}_{\text{今天的方差}} = \underbrace{\omega}_{\text{长期均值部分}} + \underbrace{\alpha \epsilon_{t-1}^2}_{\text{昨天的冲击}} + \underbrace{\beta \sigma_{t-1}^2}_{\text{昨天的方差}}$$

- $\alpha$（ARCH项）：衡量新信息（冲击）对波动率的即时冲击强度
- $\beta$（GARCH项）：衡量波动率的持续性（惯性）
- $\alpha + \beta$：越接近1，波动率聚集越持久

典型的金融数据参数估计：$\alpha \approx 0.09$，$\beta \approx 0.90$，$\alpha + \beta \approx 0.99$

**这意味着波动率冲击极为持续——今天的高波动率，一个月后仍有显著影响。**

无条件方差（长期波动率）：

$$\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \beta}$$

---

## 六、ARCH/GARCH的家族谱系

Engle的ARCH开创了一个庞大的模型家族：

| 模型 | 全名 | 主要贡献 |
|------|------|---------|
| ARCH | 自回归条件异方差 | 原始模型（Engle, 1982） |
| GARCH | 广义ARCH | 加入方差的自回归项（Bollerslev, 1986） |
| IGARCH | 积分GARCH | $\alpha+\beta=1$，波动率永久冲击（Engle & Bollerslev, 1986） |
| EGARCH | 指数GARCH | 捕捉杠杆效应（负收益→更高波动率）（Nelson, 1991） |
| GJR-GARCH | 非对称GARCH | 好消息/坏消息的不对称效应（Glosten et al., 1993） |
| TGARCH | 阈值GARCH | 分段线性结构（Zakoian, 1994） |
| FIGARCH | 分数积分GARCH | 长记忆波动率过程（Baillie et al., 1996） |
| DCC-GARCH | 动态条件相关 | 多资产动态相关结构（Engle, 2002） |

### 6.1 杠杆效应（Leverage Effect）

Black（1976）和Christie（1982）发现：**股票价格下跌比上涨引起更大的波动率增加。**

这是因为股价下跌 → 财务杠杆提高（债务/股权比上升）→ 股权风险上升 → 波动率上升。

数学上，GJR-GARCH 捕捉这种非对称性：

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \gamma \epsilon_{t-1}^2 \mathbf{1}[\epsilon_{t-1} < 0] + \beta \sigma_{t-1}^2$$

当 $\gamma > 0$ 时，负冲击（$\epsilon_{t-1} < 0$）导致更大的方差增加。

---

## 七、对统计学的深远影响

### 7.1 重新定义"误差项"的统计性质

ARCH之前，计量经济学假设误差项i.i.d.。ARCH之后：
- **条件异方差**成为时间序列分析的标准考虑
- **加权最小二乘（WLS）**的重要性被重新认识
- **拟最大似然估计（QMLE）**成为标准工具

### 7.2 波动率预测的统计学

GARCH模型的主要应用之一是**波动率预测**，这在风险管理中极为重要：

**多步前向预测**（GARCH(1,1)）：

$$\mathbb{E}[\sigma_{t+h}^2 | \mathcal{F}_t] = \bar{\sigma}^2 + (\alpha+\beta)^h (\sigma_{t+1}^2 - \bar{\sigma}^2)$$

波动率预测以 $(\alpha+\beta)^h$ 的速度均值回归到长期水平 $\bar{\sigma}^2$。

### 7.3 VaR 计算的统计基础

GARCH模型是**风险价值（VaR）**计算的核心工具：

在 $t+1$ 时刻，基于GARCH预测的一日99%置信度VaR：

$$VaR_{t+1}^{99\%} = \hat{\sigma}_{t+1} \cdot z_{0.01}$$

其中 $z_{0.01} = -2.326$（标准正态分位数），$\hat{\sigma}_{t+1}$ 是GARCH预测的条件标准差。

巴塞尔协议（Basel II/III）明确允许银行使用内部GARCH模型计算资本要求。

---

## 八、实际应用案例

### 8.1 期权定价中的GARCH

Duan（1995）将GARCH波动率引入期权定价：
- 在GARCH-EMM下，期权价格与路径依赖的波动率有关
- 解释了B-S模型的"波动率微笑"
- 提供了更接近市场价格的期权定价

### 8.2 风险管理中的 DCC-GARCH

Engle（2002）的**动态条件相关（DCC-GARCH）**模型同时估计多个资产的时变相关系数：

$$\sigma_{ij,t} = \rho_{ij,t} \sigma_{i,t} \sigma_{j,t}$$

在金融危机期间，资产相关性显著上升（"相关性崩溃"），DCC-GARCH能够捕捉这一现象，对投资组合风险管理至关重要。

---

## 九、数值例子

用标普500日收益率（2010-2020）估计GARCH(1,1)的典型结果：

$$\hat{\sigma}_t^2 = 0.000002 + 0.087 \epsilon_{t-1}^2 + 0.906 \sigma_{t-1}^2$$

- $\alpha + \beta = 0.993$（接近1，波动率高度持续）
- 长期波动率：$\bar{\sigma} = \sqrt{0.000002 / (1 - 0.993)} \approx 1.7\%$/天 ≈ $27\%$/年
- 波动率半衰期：$\frac{\ln(0.5)}{\ln(0.993)} \approx 99$ 天（波动率冲击需要约100个交易日消散一半）

---

## 十、结语

Robert Engle的ARCH论文，是计量经济学史上最重要的方法论创新之一。

它告诉我们：**金融数据中存在一种特殊的"信号"——不是均值的可预测性，而是方差的可预测性。** 这种信号在传统统计方法中被完全忽视，但它对风险管理至关重要。

诺贝尔委员会的评语：

> "Engle发现了一类在经济时间序列中极为普遍的特征，并发展了对其建模的方法——时变波动率（ARCH）。这些方法已成为金融经济学的核心工具。"

今天，全球每一家银行的风险部门、每一个期权定价模型、每一个资产管理系统，都在用ARCH/GARCH家族的某个成员来测量和预测风险。

**Engle用一个方程改变了全球金融机构理解风险的方式。**

---

*本文为「金融工程奠基论文深度解析」系列第 11/20 篇*  
*下一篇：Cox, Ingersoll & Ross (1985) · CIR利率模型 · 非负利率的随机建模*
