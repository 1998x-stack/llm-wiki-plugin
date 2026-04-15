# 论文深度解析 06/20
# 布莱克 & 斯科尔斯《期权与公司负债的定价》（1973）
## ——人类历史上使用最广泛的数学公式之一

---

## 一、论文基本信息

| 项目 | 内容 |
|------|------|
| **论文全名** | The Pricing of Options and Corporate Liabilities |
| **作者** | Fischer Sheffey Black & Myron Samuel Scholes |
| **发表时间** | 1973年5月-6月 |
| **发表刊物** | Journal of Political Economy, Vol. 81, No. 3 |
| **诺贝尔奖** | 1997年经济学奖（Scholes + Merton；Black 1995年去世，未能获奖） |
| **历史意义** | 衍生品定价理论的奠基论文，催生全球衍生品市场（规模超600万亿美元） |
| **论文命运** | 被《Journal of Political Economy》和《Review of Economic Studies》两度拒稿，后靠Merton Milller等人施压才得以发表 |

---

## 二、历史背景：期权市场的蛮荒

### 2.1 1973年之前的期权交易

期权（Option）是一种古老的金融工具，早在17世纪的荷兰郁金香泡沫时代就已存在。但在1973年之前：

- 期权在柜台（OTC）交易，**没有标准化定价**
- 每笔交易都依赖买卖双方的"直觉议价"
- 没有科学方法确定期权的"公平价值"

1973年4月26日，**芝加哥期权交易所（CBOE）**开业，标准化股票期权首次在交易所挂牌。

同月，Black-Scholes论文发表。这是历史上最精准的时机之一。

### 2.2 Fischer Black：华尔街最神秘的天才

Fischer Black（1938-1995）是一个独特的人物。他没有经济学学位（哈佛物理学和应用数学博士），进入金融界后靠着对数学的天才直觉，在MIT与Scholes合作。

他曾多次提出超前的想法，在当时被认为荒谬：CAPM的β系数随时间变化、债券价格对利率的非线性敏感度……后来都被证明是正确的。

他于1995年去世，仅比诺贝尔奖宣布早两年。

---

## 三、Black-Scholes模型的假设

1. **股票价格服从几何布朗运动（Geometric Brownian Motion，GBM）**：
   $$dS = \mu S\, dt + \sigma S\, dW_t$$
   其中 $\mu$ 是漂移率，$\sigma$ 是波动率，$dW_t$ 是维纳过程

2. **波动率 $\sigma$ 是常数**（不随时间变化）
3. **无风险利率 $r$ 是常数**
4. **无交易成本、无税收**
5. **可以连续交易，可以卖空**
6. **欧式期权**（只能在到期日行权）

---

## 四、核心推导：三种等价方法

### 方法一：Delta对冲论证（Black-Scholes原始方法）

**关键洞察：构造一个无风险的对冲组合。**

设欧式买权 $C = C(S, t)$，对冲组合：持有 $-1$ 单位买权，同时持有 $\Delta$ 单位股票：

$$\Pi = -C + \Delta S$$

选择 $\Delta = \frac{\partial C}{\partial S}$（称为Delta），使得组合**在短时间 $dt$ 内无风险**：

$$d\Pi = -dC + \Delta\, dS$$

由**伊藤引理**，期权价格变动：

$$dC = \frac{\partial C}{\partial t}dt + \frac{\partial C}{\partial S}dS + \frac{1}{2}\frac{\partial^2 C}{\partial S^2}(dS)^2$$

代入 $(dS)^2 = \sigma^2 S^2 dt$（伊藤公式）：

$$dC = \left(\frac{\partial C}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 C}{\partial S^2}\right)dt + \frac{\partial C}{\partial S}dS$$

则：
$$d\Pi = -dC + \frac{\partial C}{\partial S}dS = -\left(\frac{\partial C}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 C}{\partial S^2}\right)dt$$

这个组合是**确定性的**（无随机项）！在无套利假设下，它必须以无风险利率增值：

$$d\Pi = r\Pi\, dt = r\left(-C + \frac{\partial C}{\partial S}S\right)dt$$

**等式两边联立，得到 Black-Scholes 偏微分方程（PDE）：**

$$\boxed{\frac{\partial C}{\partial t} + rS\frac{\partial C}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 C}{\partial S^2} - rC = 0}$$

### 4.1 边界条件

欧式买权（Call）在到期日 $T$ 的价值：
$$C(S, T) = \max(S - K, 0)$$

欧式卖权（Put）在到期日 $T$ 的价值：
$$P(S, T) = \max(K - S, 0)$$

### 4.2 B-S方程的解析解

通过变量替换（将PDE转化为标准热传导方程），Black-Scholes方程的解析解为：

**欧式买权（Call）价格：**

$$\boxed{C = S\Phi(d_1) - Ke^{-r(T-t)}\Phi(d_2)}$$

**欧式卖权（Put）价格：**

$$P = Ke^{-r(T-t)}\Phi(-d_2) - S\Phi(-d_1)$$

其中：

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)(T-t)}{\sigma\sqrt{T-t}}$$

$$d_2 = d_1 - \sigma\sqrt{T-t} = \frac{\ln(S/K) + (r - \sigma^2/2)(T-t)}{\sigma\sqrt{T-t}}$$

$\Phi(\cdot)$ 是标准正态分布的累积分布函数（CDF）。

---

## 五、公式的直觉解读

B-S买权公式 $C = S\Phi(d_1) - Ke^{-r(T-t)}\Phi(d_2)$ 可以被理解为：

$$C = \underbrace{S\Phi(d_1)}_{\text{股票价值的期望}} - \underbrace{Ke^{-r(T-t)}\Phi(d_2)}_{\text{行权成本的折现期望}}$$

更精确地：
- $\Phi(d_2)$：在风险中性测度下，期权到期时**价内**（$S_T > K$）的概率
- $\Phi(d_1)$：考虑到股票作为担保品后的**delta**（价格敏感度）
- $Ke^{-r(T-t)}$：行权价的现值

**直觉**：买权的价值 = 股票带来的收益（行权时得到股票）- 支付行权价的成本，两者都以行权概率加权。

---

## 六、希腊字母（Greeks）

B-S模型衍生出一套风险敏感度指标，称为"**希腊字母（Greeks）**"，是期权交易员的核心工具：

| 希腊字母 | 定义 | 经济含义 |
|---------|------|---------|
| $\Delta = \frac{\partial C}{\partial S}$ | 期权对股价的一阶导 | 股价变动1元，期权变动$\Delta$元 |
| $\Gamma = \frac{\partial^2 C}{\partial S^2}$ | 期权对股价的二阶导 | Delta的变化率，凸性度量 |
| $\Theta = \frac{\partial C}{\partial t}$ | 期权对时间的偏导 | 时间流逝对期权的损耗（时间衰减） |
| $\mathcal{V}ega = \frac{\partial C}{\partial \sigma}$ | 期权对波动率的偏导 | 波动率变化1%，期权价值变化 |
| $\rho = \frac{\partial C}{\partial r}$ | 期权对利率的偏导 | 利率变化1%，期权价值变化 |

对于欧式买权：
$$\Delta = \Phi(d_1) \in (0, 1)$$
$$\Gamma = \frac{\phi(d_1)}{S\sigma\sqrt{T-t}} > 0$$
$$\Theta = -\frac{S\sigma\phi(d_1)}{2\sqrt{T-t}} - rKe^{-r(T-t)}\Phi(d_2)$$

---

## 七、方法二：风险中性定价（Merton的贡献）

Merton（1973）提供了一个更优雅的推导：**风险中性定价（Risk-Neutral Pricing）**。

在风险中性测度 $\mathbb{Q}$ 下，所有资产的期望收益率都等于无风险利率 $r$：

$$dS = rS\, dt + \sigma S\, d\tilde{W}_t^{\mathbb{Q}}$$

期权价格等于**到期收益在风险中性测度下的期望值的折现**：

$$C = e^{-r(T-t)} \mathbb{E}^{\mathbb{Q}}[\max(S_T - K, 0)]$$

在GBM假设下，$\ln S_T \sim \mathcal{N}\left(\ln S + (r - \sigma^2/2)(T-t), \sigma^2(T-t)\right)$，直接计算期望值即得B-S公式。

这个方法绕开了复杂的PDE推导，揭示了定价的**概率本质**。

---

## 八、对数学与统计学的影响

### 8.1 随机微积分的普及

B-S论文让**伊藤随机微积分（Itô Calculus）**从数学专业走向了金融工程：
- 伊藤引理（Itô's Lemma）成为金融工程师必备工具
- 随机微分方程（SDE）成为金融建模标准语言

### 8.2 隐含波动率与波动率微笑

B-S公式给出的唯一未知参数是**波动率 $\sigma$**（其他参数都可观测）。

实践中，交易员反过来——从期权市场价格"倒推"波动率：这就是**隐含波动率（Implied Volatility，IV）**。

如果B-S模型完全正确，不同行权价和到期日的期权应该对应相同的 $\sigma$。但实际上：

**隐含波动率曲面（IV Surface）**呈现"**波动率微笑（Volatility Smile）**"或"**波动率偏斜（Skew）**"的形状。

这表明B-S模型存在系统性偏差，催生了大量后续研究：
- **局部波动率模型（Local Volatility）**：Dupire (1994), Derman-Kani (1994)
- **随机波动率模型**：Heston (1993)
- **跳扩散模型**：Merton (1976)

### 8.3 金融工程学科的诞生

B-S论文是**金融工程（Financial Engineering）**这门学科真正的奠基石：
- 产生了对量化金融人才的巨大需求
- 推动了MIT、NYU、Columbia等大学金融工程硕士项目的建立
- 创造了"量化分析师（Quant）"这一职业

---

## 九、局限性

### 9.1 常数波动率假设

实际市场中波动率随时间变化且不可预测，这是B-S模型最主要的缺陷。

### 9.2 对数正态分布假设

实际收益率分布有**厚尾**，极端事件远比模型预测的频繁（"黑天鹅"事件）。

### 9.3 连续交易假设

实际市场有交易成本、流动性限制和市场微观结构噪声，无法实现完美的Delta对冲。

### 9.4 1987年黑色星期一的教训

1987年10月19日，道琼斯指数单日暴跌22.6%。

许多使用B-S模型进行"**投资组合保险（Portfolio Insurance）**"的机构发现，当市场极端下跌时，模型的Delta对冲完全失效，流动性也消失了。

这次崩溃后，**波动率偏斜（Volatility Skew）**在期权市场永久性出现——市场再也不相信B-S的对称分布假设了。

---

## 十、数值例子

设股票当前价格 $S = 100$，行权价 $K = 105$，到期时间 $T-t = 0.5$ 年，无风险利率 $r = 5\%$，波动率 $\sigma = 20\%$：

$$d_1 = \frac{\ln(100/105) + (0.05 + 0.02) \times 0.5}{0.20 \times \sqrt{0.5}} = \frac{-0.0488 + 0.035}{0.1414} = \frac{-0.0138}{0.1414} \approx -0.0976$$

$$d_2 = -0.0976 - 0.1414 \approx -0.2390$$

$$\Phi(d_1) \approx 0.461, \quad \Phi(d_2) \approx 0.406$$

$$C = 100 \times 0.461 - 105 \times e^{-0.05 \times 0.5} \times 0.406$$
$$= 46.1 - 105 \times 0.9753 \times 0.406 \approx 46.1 - 41.5 \approx 4.60$$

这只价外买权的公平价值约为**$4.60**。

---

## 十一、结语：一个改变世界的方程

Black-Scholes方程改变了人类管理金融风险的方式。在它出现之前，期权是少数神秘人物的工具。在它出现之后，任何人都可以用科学方法定价期权，对冲风险。

今天，全球场外衍生品市场名义价值超过600万亿美元，每一笔交易的背后，都有Black-Scholes方程的影子。

**这是一个物理学方程（热传导方程）改变全球金融生态的故事，也是数学与市场之间最深刻的对话之一。**

---

*本文为「金融工程奠基论文深度解析」系列第 06/20 篇*  
*下一篇：Robert Merton (1973) · 理性期权定价理论 · 随机微积分与连续时间金融*
