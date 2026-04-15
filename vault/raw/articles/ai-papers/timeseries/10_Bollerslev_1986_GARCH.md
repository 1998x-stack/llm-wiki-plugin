# 第十篇：GARCH——用三个参数征服金融波动率
> **论文原名**：*Generalized Autoregressive Conditional Heteroskedasticity*  
> **作者**：Tim Bollerslev  
> **发表年份**：1986 年  
> **发表期刊**：*Journal of Econometrics*

---

## 一、历史背景：ARCH 的实用困境

Engle（1982）的 ARCH 模型揭示了金融序列波动率聚集的本质，但在实际应用中面临一个尴尬的问题：

真实金融数据的波动率记忆往往**非常长**。例如，日股票收益率的波动率聚集效应可能延续数周乃至数月。要用 ARCH(q) 捕捉这种长记忆，往往需要 $q \geq 8$ 甚至 $q = 20$，这意味着需要估计大量参数，且难以保证参数全部非负（$h_t > 0$ 的约束）。

Tim Bollerslev（生于 1956 年），丹麦经济学家，1986 年在博士论文中提出了一个类比 ARMA 对 MA 的推广思路：

> **既然 GARCH 就是对 $\varepsilon_t^2$ 做"ARMA"，为何不在方差方程中也加入滞后的条件方差项？**

这一思路催生了 **GARCH（Generalized ARCH）**，成为迄今最广泛使用的金融波动率模型。

---

## 二、GARCH(p, q) 模型

### 2.1 方差方程

**均值方程**：$r_t = \mu_t + \varepsilon_t$，$\varepsilon_t = \sqrt{h_t} z_t$，$z_t \sim \text{i.i.d.}(0,1)$

**GARCH(p, q) 方差方程**：

$$h_t = \omega + \underbrace{\sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2}_{\text{ARCH 项（过去冲击）}} + \underbrace{\sum_{j=1}^{p} \beta_j h_{t-j}}_{\text{GARCH 项（过去方差）}}$$

**参数约束**（保证 $h_t > 0$ 且平稳）：
- $\omega > 0$，$\alpha_i \geq 0$，$\beta_j \geq 0$
- **弱平稳条件**：$\sum_{i=1}^{q} \alpha_i + \sum_{j=1}^{p} \beta_j < 1$

### 2.2 GARCH(1,1)：行业标准

实践中绝大多数场景只需 GARCH(1,1)：

$$h_t = \omega + \alpha \varepsilon_{t-1}^2 + \beta h_{t-1}$$

**三个参数的含义**：
- $\omega > 0$：长期无条件方差的基础水平
- $\alpha \geq 0$（ARCH 项）：对新冲击的**即时响应**——$\alpha$ 越大，波动率对新冲击越敏感
- $\beta \geq 0$（GARCH 项）：波动率的**持续性**——$\beta$ 越大，波动率变化越缓慢、记忆越长

---

## 三、GARCH(1,1) 的三个关键性质

### 3.1 均值回复：长期无条件方差

当 $\alpha + \beta < 1$ 时，条件方差均值回复到：

$$\bar{h} = E[h_t] = \frac{\omega}{1 - \alpha - \beta}$$

**冲击的半衰期**（$h_t$ 偏离 $\bar{h}$ 后衰减一半所需时间）：

$$\tau_{1/2} = \frac{\ln(0.5)}{\ln(\alpha + \beta)}$$

对于典型的日收益率数据，$\alpha + \beta \approx 0.95$—$0.99$，意味着半衰期约为数周到数月。

### 3.2 MA(∞) 表示

将 GARCH(1,1) 的 $h_{t-1}$ 递推代入，可以展开为：

$$h_t = \frac{\omega}{1-\beta} + \alpha \sum_{j=0}^{\infty} \beta^j \varepsilon_{t-1-j}^2$$

这说明 GARCH(1,1) 等价于无穷阶 ARCH——对过去所有冲击平方的指数加权平均，权重以 $\beta$ 的幂次衰减。这正是 GARCH 能够用三个参数捕捉长记忆波动的原因。

### 3.3 胖尾分布

即使假设条件分布 $z_t \sim \mathcal{N}(0,1)$，GARCH(1,1) 生成的无条件分布也是**超额峰度**（fat tails）的：

$$\text{Kurt}(r_t) = 3 \cdot \frac{1 - (\alpha+\beta)^2}{1 - (\alpha+\beta)^2 - 2\alpha^2} > 3 \quad (\text{当 } 1 - (\alpha+\beta)^2 > 2\alpha^2)$$

这解释了金融数据普遍观察到的"尖峰胖尾"现象。

---

## 四、GARCH 的"ARMA 类比"

Bollerslev 在论文中明确指出，GARCH 与 ARMA 之间存在深刻的类比关系。

定义"波动率冲击"（波动率的创新项）：$\eta_t = \varepsilon_t^2 - h_t$（$E[\eta_t] = 0$）

则 GARCH(p,q) 对 $\varepsilon_t^2$ 的方程可以改写为：

$$\varepsilon_t^2 = \omega + (\alpha_1 + \beta_1)\varepsilon_{t-1}^2 + \eta_t - \beta_1 \eta_{t-1}$$

这正是一个 **ARMA(max(p,q), p) 结构**！

| ARMA 模型 | GARCH 模型 |
|---|---|
| $X_t$（可观测） | $\varepsilon_t^2$（可观测） |
| $\varepsilon_t$（新息） | $\eta_t = \varepsilon_t^2 - h_t$（"方差新息"） |
| AR(p) 系数 | $\alpha_i + \beta_i$ |
| MA(q) 系数 | $-\beta_j$ |

这一类比使得 ARMA 建模的丰富工具箱（ACF/PACF 识别、模型选择准则等）可以直接迁移到 GARCH 建模中。

---

## 五、最大似然估计

GARCH 参数通过**最大似然**估计。在高斯条件分布假设下：

$$\ell(\theta) = -\frac{T}{2}\ln(2\pi) - \frac{1}{2}\sum_{t=1}^{T}\left(\ln h_t(\theta) + \frac{\varepsilon_t^2}{h_t(\theta)}\right)$$

初始化：$h_1 = \hat{\sigma}^2_{\text{样本}}$（或用无条件方差）

然后递推计算 $h_2, h_3, \ldots$，并用数值优化（BHHH、BFGS 等）最大化似然。

**实践注意**：金融数据的条件分布往往比高斯分布有更厚的尾部，常替换为：
- **学生 $t$ 分布**：$z_t \sim t(\nu)$，自由度 $\nu$ 作为额外参数估计
- **广义误差分布（GED）**：形状参数控制尾部厚度

---

## 六、非对称效应与扩展模型

GARCH(1,1) 的一个已知缺陷：它对正、负冲击（涨、跌）的响应是**对称的**——只关心 $\varepsilon_{t-1}^2$，不区分正负。

但金融数据存在著名的"**杠杆效应（Leverage Effect）**"（Black 1976）：
- **股价下跌** $\implies$ 公司财务杠杆上升 $\implies$ 股票风险增加 $\implies$ **波动率上升更大**
- 相反，股价上涨后波动率上升的幅度较小

捕捉杠杆效应的扩展模型：

| 模型 | 方差方程 | 特点 |
|---|---|---|
| **EGARCH** (Nelson 1991) | $\ln h_t = \omega + \alpha(|z_{t-1}| - E|z|) + \gamma z_{t-1} + \beta \ln h_{t-1}$ | 自然满足 $h_t > 0$；$\gamma < 0$ 捕捉杠杆效应 |
| **GJR-GARCH** (Glosten 1993) | $h_t = \omega + (\alpha + \gamma I_{t-1}^-)\varepsilon_{t-1}^2 + \beta h_{t-1}$ | $I_{t-1}^- = 1$ 当 $\varepsilon_{t-1} < 0$；简单直观 |
| **TGARCH** (Zakoian 1994) | 对条件标准差而非方差建模 | 计算更稳定 |

对于股票收益率，实证结果通常发现 $\gamma > 0$（GJR-GARCH）或 $\gamma < 0$（EGARCH），证实杠杆效应的存在。

---

## 七、实证典型结果：S&P 500 日收益率

典型的 S&P 500 日收益率 GARCH(1,1) 估计结果：

$$\hat{\omega} \approx 0.00001, \quad \hat{\alpha} \approx 0.09, \quad \hat{\beta} \approx 0.90$$

**解读**：
- $\hat{\alpha} + \hat{\beta} \approx 0.99$：波动率高度持久，半衰期约 70 天
- $\hat{\alpha} \approx 0.09$：新冲击对波动率的即时影响约 9%
- $\hat{\beta} \approx 0.90$：前一期条件方差的贡献约 90%
- 长期年化无条件波动率：$\bar{h}^{1/2} \times \sqrt{252} \approx 15\%-20\%$（视时间段而异）

这一参数结构（$\alpha$ 小，$\beta$ 大，$\alpha+\beta$ 接近 1）在全球各股市中极为普遍，被称为"**GARCH 效应的普世性**"。

---

## 八、多变量扩展：DCC-GARCH

金融组合管理中，不仅需要各资产的条件方差，还需要资产间的**条件协方差**（相关性也会随时间变化，危机时期往往急剧上升）。

Engle（2002）提出**动态条件相关（DCC-GARCH）**模型：

$$\mathbf{H}_t = \mathbf{D}_t \mathbf{R}_t \mathbf{D}_t$$

其中 $\mathbf{D}_t = \text{diag}(\sqrt{h_{1t}}, \ldots, \sqrt{h_{nt}})$ 是各资产 GARCH 波动率的对角矩阵，$\mathbf{R}_t$ 是时变相关矩阵（由简化参数模型描述）。这使得多资产波动率建模在维度诅咒下仍然可行。

---

## 九、波动率预测与风险管理

GARCH 模型的核心应用之一是**波动率预测**，进而计算风险指标：

**$h$ 步预测**：

对 GARCH(1,1)，$h$ 步条件方差预测为：

$$E[h_{t+h}|{\mathcal{F}_t}] = \bar{h} + (\alpha+\beta)^{h-1}(h_t - \bar{h})$$

随 $h$ 增大指数速度收敛到无条件方差 $\bar{h}$。

**风险价值（VaR）**：

$$\text{VaR}_{1\%}(t+1) = -\hat{\mu}_{t+1} + z_{0.01} \sqrt{\hat{h}_{t+1}}$$

其中 $z_{0.01} = -2.326$（正态）或更厚尾的分布分位数。GARCH-VaR 在巴塞尔协议框架下是银行风险资本计算的标准方法。

---

## 十、小结

Bollerslev（1986）完成了从 ARCH 到 GARCH 的关键推广：

> **将波动率方程从"纯 MA"扩展为"ARMA"，用三个参数捕捉金融序列的长期波动记忆。**

GARCH(1,1) 的三大优势：
1. **简洁**：仅三个参数，估计稳定，数值行为良好
2. **灵活**：等价于无穷阶 ARCH，隐式捕捉长记忆
3. **普适**：在全球几乎所有金融市场均能拟合良好，参数范围高度相似

GARCH 家族至今仍是金融波动率建模的**行业标准**，每年被引用数千次，是计量金融文献中影响力最持久的模型之一。

---

*下一篇：Engle & Granger（1987）——协整理论，两个随机游走之间可能存在稳定的长期均衡，误差修正模型描述短期动态。*
