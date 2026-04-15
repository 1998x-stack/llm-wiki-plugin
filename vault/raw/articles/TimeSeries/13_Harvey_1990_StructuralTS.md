# 第十三篇：结构时间序列模型——把趋势、季节、周期分开看
> **著作原名**：*Forecasting, Structural Time Series Models and the Kalman Filter*  
> **作者**：Andrew C. Harvey  
> **发表年份**：1990 年  
> **出版社**：Cambridge University Press

---

## 一、历史背景：时序分解的两个传统

在 Harvey 的著作之前，时间序列分解存在两条平行的传统：

**传统一：经典时序分解（统计学）**  
将序列分解为趋势（T）、季节（S）、循环（C）、残差（R）：
$$Y_t = T_t + S_t + C_t + R_t \quad \text{（加法）}$$

代表方法：X-11（Census Bureau）、Holt-Winters 指数平滑。方法直观，但缺乏完整的统计推断框架（无法对参数做假设检验、无法计算置信区间）。

**传统二：状态空间模型（工程）**  
卡尔曼（1960）的状态空间框架提供了严格的最优估计，但主要面向工程信号处理，与统计学传统的时序分解方法之间缺少明确的联系。

Andrew Harvey（生于 1947 年），剑桥大学计量经济学家，在 1990 年的这部著作中完成了两条传统的大综合：

> **将所有经典的时序分解成分（趋势、季节、周期）明确地建模为状态空间模型的状态变量，用 Kalman 滤波进行估计和预测。**

这一框架被称为**结构时间序列模型（Structural Time Series Models, STM）**，也称**不可观测成分模型（Unobserved Components Models, UCM）**。

---

## 二、核心框架：各成分的状态空间表示

### 2.1 局部水平模型（最简单情形）

$$Y_t = \mu_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \sigma_\varepsilon^2)$$

$$\mu_t = \mu_{t-1} + \eta_t, \quad \eta_t \sim \mathcal{N}(0, \sigma_\eta^2)$$

- $\mu_t$：不可观测的"局部水平"（趋势）
- $\varepsilon_t$：观测噪声
- $\eta_t$：趋势的随机扰动

**特殊情形**：
- $\sigma_\eta^2 = 0$：趋势固定，$\mu_t = \mu_0$（静态均值）
- $\sigma_\varepsilon^2 = 0$：无噪声观测，$Y_t = \mu_t$（纯随机游走）
- 两者均非零：等价于 **ARIMA(0,1,1)**（指数平滑的状态空间诠释！）

**与指数平滑的等价性**：在局部水平模型中，Kalman 滤波给出的一步预测 $\hat{Y}_{t+1|t} = \hat{\mu}_{t|t}$ 恰好等于简单指数平滑的更新公式：
$$\hat{\mu}_{t|t} = \hat{\mu}_{t-1|t-1} + K_\infty (Y_t - \hat{\mu}_{t-1|t-1})$$
其中 $K_\infty$（稳态 Kalman 增益）对应指数平滑参数 $\alpha$。

这证明了**简单指数平滑 = 局部水平模型的 Kalman 滤波**，为指数平滑方法提供了状态空间理论基础。

### 2.2 局部线性趋势模型

在局部水平基础上加入斜率（增长率）的随机演化：

$$Y_t = \mu_t + \varepsilon_t$$
$$\mu_t = \mu_{t-1} + \nu_{t-1} + \eta_t$$
$$\nu_t = \nu_{t-1} + \zeta_t$$

其中 $\nu_t$ 是趋势的斜率（瞬时增长率），$\zeta_t \sim \mathcal{N}(0, \sigma_\zeta^2)$ 是斜率的随机扰动。

**特殊情形**：
- $\sigma_\eta^2 = 0, \sigma_\zeta^2 \neq 0$：平滑趋势模型（斜率随机，水平确定）
- $\sigma_\eta^2 \neq 0, \sigma_\zeta^2 = 0$：随机游走加漂移（斜率固定）
- 两者均非零：等价于 **Holt 双参数指数平滑** + 状态空间结构

### 2.3 季节成分

**三角季节（Trigonometric Seasonality）**：将季节效应表示为周期性正弦-余弦对的叠加：

$$\gamma_t = \sum_{j=1}^{\lfloor s/2 \rfloor} \gamma_{j,t}$$

每个谐波分量满足：

$$\begin{pmatrix} \gamma_{j,t} \\ \gamma_{j,t}^* \end{pmatrix} = \begin{pmatrix} \cos\lambda_j & \sin\lambda_j \\ -\sin\lambda_j & \cos\lambda_j \end{pmatrix} \begin{pmatrix} \gamma_{j,t-1} \\ \gamma_{j,t-1}^* \end{pmatrix} + \begin{pmatrix} \omega_{j,t} \\ \omega_{j,t}^* \end{pmatrix}$$

其中 $\lambda_j = 2\pi j / s$ 是第 $j$ 个季节频率，$\omega_{j,t} \sim \mathcal{N}(0, \sigma_\omega^2)$ 是季节扰动。

- 若 $\sigma_\omega^2 = 0$：季节模式固定不变（经典确定性季节）
- 若 $\sigma_\omega^2 > 0$：季节模式随时间缓慢演化（**随机季节**）

**虚拟变量季节模型**（另一种等价实现）：

$$\sum_{j=0}^{s-1} \gamma_{t-j} = \omega_t$$

即每个季节效应等于过去 $s$ 个季节效应的负和加随机扰动，保证季节效应在一年内之和约为零。

### 2.4 完整结构时间序列模型

将上述成分组合，得到完整的 UCM：

$$Y_t = \mu_t + \gamma_t + \psi_t + \varepsilon_t$$

其中：
- $\mu_t$：趋势（局部线性趋势或平滑趋势）
- $\gamma_t$：季节成分（三角或虚拟变量）
- $\psi_t$：周期成分（阻尼正弦过程：$\psi_t = \rho\cos\lambda \psi_{t-1} + \rho\sin\lambda \psi_{t-1}^* + \kappa_t$）
- $\varepsilon_t$：不规则成分（观测噪声）

所有成分合并为一个**状态向量** $\mathbf{x}_t$，写成标准状态空间形式，用 Kalman 滤波估计。

---

## 三、参数估计：最大化预测误差分解似然

状态空间模型的参数（各方差 $\sigma_\varepsilon^2, \sigma_\eta^2, \sigma_\zeta^2, \sigma_\omega^2$ 等，称为**超参数**）通过最大化似然函数估计。

**预测误差分解**：Kalman 滤波的一个重要副产品是对数似然的计算公式：

$$\ln L = -\frac{T}{2}\ln(2\pi) - \frac{1}{2}\sum_{t=1}^{T}\left(\ln f_t + \frac{v_t^2}{f_t}\right)$$

其中 $v_t = Y_t - \hat{Y}_{t|t-1}$（新息/预测误差），$f_t = \text{Var}(v_t)$（预测误差方差）。

这种"从 Kalman 滤波中直接读出似然"的方式是计算效率极高的做法，避免了显式计算高维协方差矩阵的逆。

---

## 四、诊断与模型选择

与 Box-Jenkins 方法类似，结构时间序列模型也有系统的诊断方法：

1. **残差检验**：新息序列 $v_t / \sqrt{f_t}$ 应为标准化白噪声——检验 ACF、Ljung-Box 统计量
2. **正态性检验**：Jarque-Bera 检验残差分布
3. **预测检验**：滚动预测误差的大小和方向
4. **超参数 AIC/BIC**：比较不同结构（是否包含随机趋势、是否包含随机季节等）

**信号-噪声比（SNR）**的估计尤其重要：
$$q = \sigma_\eta^2 / \sigma_\varepsilon^2$$

若 $q \to 0$：趋势几乎固定，序列围绕固定水平波动；  
若 $q \to \infty$：序列几乎完全由趋势主导，相当于随机游走。

---

## 五、与经典方法的统一

Harvey 的框架为诸多经典方法提供了状态空间诠释，揭示了它们的统一根源：

| 经典方法 | 等价的状态空间模型 | 
|---|---|
| 简单指数平滑（SES） | 局部水平模型（LLM） |
| Holt 双参数指数平滑 | 局部线性趋势模型（LLT） |
| Holt-Winters 加法季节 | LLT + 确定性虚拟变量季节 |
| ARIMA(0,1,1) | LLM（特殊超参数约束） |
| ARIMA(0,2,2) | LLT（特殊超参数约束） |
| HP 滤波（宏观经济分解） | 平滑趋势模型（ $\sigma_\eta^2 = 0$）的限定情形 |

---

## 六、实际应用：英国汽车销量分解

Harvey 在书中展示了月度英国汽车登记数据（1962—1975 年）的分解结果：

经过对数变换后，模型识别出：
- **随机趋势**（斜率缓慢变化）：捕捉汽车普及的长期增长
- **随机季节**（季节强度随时间变化）：夏季与年底的购车高峰，强度随年变化
- **不规则成分**：石油危机（1973—74 年）带来的短期冲击

与固定参数方法（如经典 X-11）相比，随机季节的设定使模型能够**自适应**地捕捉季节模式的演化，而非强行假设季节效应年复一年保持相同。

---

## 七、对现代预测的影响

Harvey（1990）的影响在此后三十年持续扩大：

**Hyndman 等（2002）的 ETS 框架**（我们的下一篇）正是在 Harvey 的状态空间思想基础上，将所有指数平滑方法系统化，引入信息准则进行自动模型选择。

**Facebook Prophet（2018）**的核心分解结构（趋势 + 季节 + 节假日效应）与 Harvey 的 UCM 框架一脉相承，差别在于 Prophet 用贝叶斯方法（Stan）估计，并引入了更灵活的趋势断点机制。

**Google Causal Impact**（Brodersen 等 2015），用状态空间模型进行政策效果的因果推断，直接建立在结构时间序列模型框架之上。

**TBATS 模型**（De Livera 等 2011），将 Harvey 的三角季节延伸到多重季节性（如每日-每周-每年的嵌套季节性），被广泛用于能源需求预测。

---

## 八、小结

Harvey（1990）是时间序列分析史上最重要的整合性工作之一：

> **用状态空间语言重新讲述了所有经典时序分解方法，将直觉驱动的分解与严格的统计推断无缝对接。**

三大贡献：
1. **统一性**：将指数平滑、X-11 分解、ARIMA 等主要预测方法统一在 UCM 框架下
2. **灵活性**：允许各成分（趋势、季节）随时间随机演化，比固定参数方法更贴近现实
3. **推断性**：通过 Kalman 滤波和似然估计，赋予时序分解完整的统计推断能力（置信区间、假设检验）

---

*下一篇：Hochreiter & Schmidhuber（1997）——LSTM，用门控机制解决梯度消失问题，奠定深度序列建模的基础。*
