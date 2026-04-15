---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
- 技术
- 研究
- 数值分析
aliases:
- CFL Condition
- Courant-Friedrichs-Lewy Condition
- 柯朗条件
- 柯朗数
- CFL number
- CFL数
relates_to:
- target: '[[理查德·柯朗]]'
  type: caused
  confidence: 0.95
- target: '[[冯·诺依曼稳定性分析]]'
  type: related_to
  confidence: 0.9
  note: 冯·诺依曼稳定性分析提供了验证CFL条件的具体傅里叶工具
- target: '[[Richardson外推法]]'
  type: related_to
  confidence: 0.7
  note: 理查森1922年天气预报失败的主因之一正是违反了CFL条件
- target: '[[有限元方法]]'
  type: related_to
  confidence: 0.7
  note: 有限元显式时间步进（如显式中心差分）同样受CFL条件约束
- target: '[[谱方法]]'
  type: related_to
  confidence: 0.65
  note: 谱方法显式时间积分也受CFL类约束，通常比有限差分更严格
- target: '[[Lax-Richtmyer等价定理]]'
  type: related_to
  confidence: 0.9
  note: CFL是稳定性的必要条件；等价定理指出违反CFL（不稳定）的格式也不收敛——二者完美衔接
supersedes: null
---

# CFL 条件

## 概述

CFL 条件（Courant-Friedrichs-Lewy Condition）由[[理查德·柯朗]]、Kurt Friedrichs 和 Hans Lewy 于 1928 年发表。其核心陈述是：求解双曲型偏微分方程的**显式有限差分格式**要收敛，必须满足"数值信息传播速度不慢于物理信息传播速度"的约束，量化为 CFL 数 $\nu = c\Delta t / \Delta x \leq 1$。这一条件原本是出于纯数学目的（PDE 存在性证明）被发现的，却成为所有显式时间步进数值方法必须遵守的基本约束，是计算科学中最重要的稳定性判据之一。

## 关键内容

### 数学表述

**一维波动方程**：$u_{tt} = c^2 u_{xx}$，显式中心差分格式

$$\frac{u_j^{n+1} - 2u_j^n + u_j^{n-1}}{(\Delta t)^2} = c^2 \frac{u_{j+1}^n - 2u_j^n + u_{j-1}^n}{(\Delta x)^2}$$

**CFL 条件**（一维，差分格式收敛的必要条件）：

$$\nu = \frac{c\Delta t}{\Delta x} \leq 1$$

**二维推广**（$\Delta x = \Delta y$ 时）：$c\Delta t/\Delta x \leq 1/\sqrt{2}$（更严格）

**一般形式（依赖域论证）**：

> 差分格式的**数值依赖域**（numerical domain of dependence）必须包含微分方程的**物理依赖域**（physical domain of dependence）。

### 依赖域论证

**物理依赖域**：波动方程中，$(x_0, t_0)$ 处的解只依赖于特征线 $x = x_0 \pm c(t_0-t)$ 界定的初始区间 $[x_0-ct_0,\; x_0+ct_0]$。

**数值依赖域**：显式格式中，$u_j^n$ 只依赖于初始时刻 $[x_j - n\Delta x,\; x_j + n\Delta x]$ 内的值（"信息锥"）。

若 $c\Delta t/\Delta x > 1$，特征线斜率大于信息锥边界斜率——特征线"穿出"信息锥，格式看不到沿这些特征线传播的初始数据，必然不能收敛到正确解。

### CFL 条件与稳定性

CFL 条件是**必要条件**，不是充分条件：满足 CFL 条件的格式还可能因截断误差、耗散误差等原因不稳定。

但对许多常用格式，CFL 条件恰好同时是稳定性的充要条件（如上述显式中心差分格式）。[[冯·诺依曼稳定性分析]]提供了精确验证：当 $\nu > 1$ 时，至少一个傅里叶模式的放大因子 $> 1$，误差指数增长。

**Lax 等价定理**（Peter Lax，1956）：对一致性差分格式，稳定性 ⟺ 收敛性。CFL 条件所代表的稳定性要求因此是收敛性的充要条件（在一致性保证的前提下）。

### 热传导方程的类比

对显式差分格式的**抛物型方程**（热传导 $u_t = \alpha u_{xx}$），类似稳定性条件为：

$$\frac{\alpha \Delta t}{(\Delta x)^2} \leq \frac{1}{2}$$

物理解释：扩散速度而非波速；约束更严格（$\Delta t \sim (\Delta x)^2$，空间步长减半时间步长须减四分之一）。

### 历史意义：超前计算机时代的理论

CFL 论文发表于 1928 年——第一台电子计算机出现之前约 20 年。三位作者的初衷是**纯数学**：用差分方程作为工具证明 PDE 解的存在性，而非设计实际的计算算法。CFL 条件是证明过程中的"副产品"。

这是科学史上"基础研究意想不到的实用价值"的经典案例。当[[刘易斯·弗赖·理查森]]1922 年的数值天气预报产生荒谬结果时（预测气压变化 145 百帕 vs. 实际 <1 百帕），原因之一正是他使用的时间步长违反了 CFL 条件——而此时 CFL 条件尚未被发现（1928 年）。

### 显式 vs 隐式方法的核心权衡

| 维度 | 显式方法 | 隐式方法 |
|------|---------|---------|
| CFL 限制 | 有（$\nu \leq 1$） | 无条件稳定（或宽松得多）|
| 每步计算 | 简单，天然并行 | 需解线性方程组 |
| 适用场景 | 非刚性问题，波动方程，GPU 并行 | 刚性问题，扩散为主 |
| 代表格式 | Lax-Friedrichs，Lax-Wendroff，显式 RK | Crank-Nicolson，ADI，BDF |

CFL 条件的严格性是选择隐式方法的重要动机。

### 实际应用中的 CFL 数

工程实践中，用户根据当前流场状态自适应调整时间步长：

$$\Delta t = \text{CFL}_{\max} \cdot \frac{\Delta x_{\min}}{c_{\max}}$$

常取 $\text{CFL}_{\max} \approx 0.5 \sim 0.9$（安全余量）。

| 应用领域 | 波速 $c$ | 典型约束 |
|---------|---------|---------|
| CFD（可压缩流） | 声速（$\sim 340$ m/s 大气） | 典型 CFL 数 0.5–0.8 |
| 全球天气模型（10 km 网格） | 大气波速 | 时间步长 $\sim 30$ 秒 |
| FDTD 电磁模拟 | 光速 $c = 1/\sqrt{\mu\epsilon}$ | Yee 网格（1966）自然满足 |
| 地震波模拟 | 地震波速 | 空间分辨率决定 $\Delta t$ |

## 来源

- [[raw/books/数值分析/11_cfl_condition.md]]

## 相关

- [[理查德·柯朗]]
- [[冯·诺依曼稳定性分析]]
- [[刘易斯·弗赖·理查森]]
- [[有限元方法]]
- [[谱方法]]
