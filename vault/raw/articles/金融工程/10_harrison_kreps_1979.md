# 论文深度解析 10/20
# Harrison & Kreps《多期证券市场中的鞅与套利》（1979）
## ——资产定价第一基本定理：无套利 ⟺ 等价鞅测度存在

---

## 一、论文基本信息

| 项目 | 内容 |
|------|------|
| **论文全名** | Martingales and Arbitrage in Multiperiod Securities Markets |
| **作者** | J. Michael Harrison & David M. Kreps |
| **发表时间** | 1979年 |
| **发表刊物** | Journal of Economic Theory, Vol. 20, No. 3 |
| **核心贡献** | 资产定价第一基本定理（FTAP）：无套利 ⟺ 等价鞅测度存在 |
| **数学工具** | 函数分析、概率测度论、鞅理论 |
| **历史地位** | 现代资产定价理论的数学基础，将B-S/CRR/APT统一在一个框架下 |

---

## 二、背景：定价理论需要统一的数学语言

### 2.1 1979年前的分散状态

到1979年，金融定价理论已有：
- Black-Scholes（1973）：连续时间PDE方法
- CRR（1979）：离散时间风险中性概率
- APT（1976）：线性因子无套利约束

这些方法各有各的推导逻辑，彼此之间缺乏统一的数学联系。

Harrison和Kreps要做的是：**找到一个统一的数学语言，将所有这些定价结果纳入同一框架。**

### 2.2 鞅论（Martingale Theory）的引入

**鞅（Martingale）**是概率论中的核心概念：

随机过程 $\{M_t\}$ 是鞅，若对所有 $s < t$：
$$\mathbb{E}[M_t | \mathcal{F}_s] = M_s$$

直觉：鞅是"公平博弈"——给定现在的信息，对未来的最佳预测就是现在的值。

这与巴舍利耶（1900）的直觉完全一致：在有效市场中，价格是公平博弈。

---

## 三、资产定价第一基本定理（FTAP）

### 3.1 核心定理（离散时间版本）

**定理（Harrison-Kreps 1979）：**

在一个多期证券市场中，以下两个命题等价：

$$\text{市场不存在套利机会} \iff \text{存在等价鞅测度（等价概率测度 } \mathbb{Q}\text{）}$$

其中**等价鞅测度（Equivalent Martingale Measure，EMM）**，也称**风险中性测度**，满足：

1. $\mathbb{Q}$ 与真实概率测度 $\mathbb{P}$ **等价**：两者对于同一事件，概率同时为零或同时非零（$\mathbb{Q} \sim \mathbb{P}$）
2. 在 $\mathbb{Q}$ 下，**贴现后的资产价格是鞅**：
   $$\mathbb{E}^{\mathbb{Q}}\left[\frac{S_t}{B_t} \bigg| \mathcal{F}_s\right] = \frac{S_s}{B_s} \quad \forall s < t$$
   其中 $B_t = e^{rt}$ 是货币市场账户（无风险资产）

### 3.2 定理的深刻含义

"无套利 ⟺ EMM存在"这个等价关系，是现代资产定价理论的**核心支柱**：

**（→方向）**：若存在套利，则无法定义一致的风险中性定价。（套利机会意味着用零成本策略获得正收益，这与任何概率测度下的鞅条件矛盾。）

**（←方向）**：若存在EMM，则在 $\mathbb{Q}$ 下，任何资产的贴现价格都是鞅，无套利自然成立。

**推论（定价公式）**：任何衍生品的公平价格为：

$$V_0 = B_0 \cdot \mathbb{E}^{\mathbb{Q}}\left[\frac{V_T}{B_T}\right] = e^{-rT} \mathbb{E}^{\mathbb{Q}}[V_T]$$

**这将所有定价问题统一为：在EMM下计算期望值，然后折现。**

---

## 四、关键数学工具

### 4.1 Radon-Nikodym 导数（测度变换）

两个等价测度 $\mathbb{P}$ 和 $\mathbb{Q}$ 之间通过 **Radon-Nikodym 导数** $\frac{d\mathbb{Q}}{d\mathbb{P}}$ 联系：

$$\mathbb{E}^{\mathbb{Q}}[X] = \mathbb{E}^{\mathbb{P}}\left[\frac{d\mathbb{Q}}{d\mathbb{P}} \cdot X\right]$$

在连续时间（Girsanov定理下）：

$$\frac{d\mathbb{Q}}{d\mathbb{P}}\bigg|_T = \exp\left(-\int_0^T \theta_t dW_t^{\mathbb{P}} - \frac{1}{2}\int_0^T \theta_t^2 dt\right)$$

其中 $\theta_t = \frac{\mu - r}{\sigma}$ 是**市场风险价格（Market Price of Risk）**。

### 4.2 Girsanov 定理

在 $\mathbb{P}$ 下，股价满足：
$$dS = \mu S\,dt + \sigma S\,dW_t^{\mathbb{P}}$$

通过测度变换（Girsanov定理），在 $\mathbb{Q}$ 下：
$$W_t^{\mathbb{Q}} = W_t^{\mathbb{P}} + \int_0^t \theta_s ds$$
是新的标准布朗运动，且：
$$dS = rS\,dt + \sigma S\,dW_t^{\mathbb{Q}}$$

漂移率从 $\mu$（真实收益率）变为 $r$（无风险利率）——这正是"风险中性"的数学实现。

---

## 五、资产定价第二基本定理（完备市场）

Harrison & Kreps 还给出了第二基本定理：

**定理：市场是完备的（complete）当且仅当等价鞅测度唯一。**

**完备市场**：任意收益结构都可以被现有资产复制（没有"定价不确定性"）。

| 市场类型 | EMM数量 | 含义 |
|---------|--------|------|
| 完备市场 | 唯一EMM | 所有衍生品有唯一无套利价格 |
| 不完备市场 | 多个EMM | 衍生品价格在一个区间内（无唯一定价） |

**B-S框架是完备市场**：一只股票 + 无风险资产，可以复制任何期权，EMM唯一。

**含有随机波动率的市场是不完备的**：额外的波动率风险无法对冲，EMM不唯一，产生"波动率风险溢价"的不确定性。

---

## 六、随机折现因子（Stochastic Discount Factor）

FTAP的另一个等价表述是**随机折现因子（SDF，又称定价核 Pricing Kernel）** $M$：

$$V_0 = \mathbb{E}^{\mathbb{P}}[M \cdot V_T]$$

其中 $M = e^{-rT} \frac{d\mathbb{Q}}{d\mathbb{P}}$。

SDF框架统一了几乎所有资产定价模型：

| 定价模型 | SDF 的形式 |
|---------|----------|
| CAPM | $M = a - b \cdot r_M$（市场收益的线性函数） |
| B-S模型 | $M = e^{-rT}\exp(-\theta W_T - \frac{1}{2}\theta^2 T)$ |
| 消费CAPM（CCAPM） | $M = \beta \frac{u'(c_{T})}{u'(c_0)}$（边际效用之比） |
| APT | $M = 1 - \sum_k \lambda_k \tilde{f}_k$（因子的线性组合） |

**无论使用哪个模型，资产定价的核心公式都是 $V_0 = \mathbb{E}^{\mathbb{P}}[M \cdot V_T]$。**

---

## 七、对统计学和数量金融的影响

### 7.1 确立了"测度论概率"在金融中的地位

FTAP之后，现代数量金融需要扎实的测度论概率基础：
- Kolmogorov公理体系
- Lebesgue积分、Radon-Nikodym定理
- 鞅收敛定理、可选抽样定理

这使得金融数学真正成为"严格数学"的一个分支。

### 7.2 统一了所有定价方法

| 之前 | 之后（FTAP框架） |
|------|----------------|
| B-S用PDE | 等价：在EMM下求期望 |
| CRR用风险中性概率 | 等价：EMM下的离散近似 |
| APT用无套利约束 | 等价：EMM存在的必要条件 |
| CAPM用均衡 | 等价：特殊形式的SDF |

### 7.3 催生了随机微积分金融应用的严格化

FTAP为以下工作奠定了基础：
- **Delbaen & Schachermayer（1994）**：将FTAP推广到一般连续时间半鞅模型（"无有界套利 NFLVR"条件）
- **Heath, Jarrow & Morton（1992）**：用EMM直接约束利率期限结构的无套利条件

---

## 八、不完备市场中的定价

现实金融市场通常是不完备的（存在无法对冲的风险）。FTAP指出，此时存在**多个EMM**，对应一个价格区间。

不完备市场的定价策略：
- **超对冲（Super-hedging）**：找到最小超复制成本（EMM集合下期望值的上确界）
- **效用无差异定价（Utility Indifference Pricing）**：选择使投资者效用不变的价格
- **模型选择**：在多个EMM中选择"经济上合理"的一个

---

## 九、结语：数学的胜利

Harrison & Kreps（1979）的论文，是现代数量金融史上最重要的数学论文之一。

它的意义在于：它不仅解决了一个具体问题，而且提供了一种**看待所有金融定价问题的统一视角**。

从此，资产定价不再是一堆分散的公式和技巧，而是一个有着严格数学基础的完整理论体系。

每一个衍生品定价员在使用"风险中性测度"时，每一个风险管理员在进行"Q-measure"下的蒙特卡洛模拟时，都站在Harrison & Kreps所建立的数学大厦之上。

**这是概率论遇见金融学最美丽的一次拥抱。**

---

*本文为「金融工程奠基论文深度解析」系列第 10/20 篇*  
*下一篇：Robert Engle (1982) · ARCH模型 · 波动率聚集的统计学发现*
