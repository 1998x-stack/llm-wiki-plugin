# 强化学习核心范式：价值函数、策略梯度与演员-评论家
## 系统性论文分析路线图

---

## 一、强化学习问题的数学框架

### 1.1 马尔可夫决策过程（MDP）

强化学习的标准形式化为一个五元组 **MDP = (S, A, P, R, γ)**：

| 符号 | 含义 | 说明 |
|------|------|------|
| S | 状态空间 | 环境所有可能状态的集合 |
| A | 动作空间 | 智能体可执行的所有动作集合 |
| P(s'&#124;s,a) | 转移概率 | 在状态 s 执行动作 a 后转移至 s' 的概率 |
| R(s,a,s') | 奖励函数 | 状态转移后获得的即时奖励 |
| γ ∈ [0,1) | 折扣因子 | 未来奖励的折现率 |

**目标**：找到策略 π，使期望累积折扣回报最大化：

```
J(π) = E_π [ Σ_{t=0}^{∞} γ^t R(s_t, a_t, s_{t+1}) ]
```

### 1.2 核心价值函数定义

**状态价值函数（V-function）：**
```
V^π(s) = E_π [ Σ_{t=0}^{∞} γ^t r_{t+k+1} | s_t = s ]
```

**动作价值函数（Q-function）：**
```
Q^π(s,a) = E_π [ Σ_{t=0}^{∞} γ^t r_{t+k+1} | s_t = s, a_t = a ]
```

**优势函数（Advantage function）：**
```
A^π(s,a) = Q^π(s,a) - V^π(s)
```

**贝尔曼方程（Bellman Equation）：**
```
Q^π(s,a) = E_{s'~P} [ R(s,a,s') + γ Σ_{a'} π(a'|s') Q^π(s',a') ]
```

**贝尔曼最优方程（Bellman Optimality Equation）：**
```
Q*(s,a) = E_{s'~P} [ R(s,a,s') + γ max_{a'} Q*(s',a') ]
```

---

## 二、三大范式的本质区别

```
强化学习算法
├── Value-Based（基于价值）
│   ├── 核心思想：学习价值函数，策略由价值函数导出（贪心）
│   ├── 策略表示：隐式（argmax Q(s,a)）
│   ├── 优化目标：最小化 TD 误差
│   └── 代表：DQN, Double DQN, Dueling, PER, Rainbow
│
├── Policy-Based（基于策略）
│   ├── 核心思想：直接参数化并优化策略
│   ├── 策略表示：显式（π_θ(a|s)）
│   ├── 优化目标：最大化 J(θ) = E[R]，用梯度上升
│   └── 代表：REINFORCE, TRPO, PPO
│
└── Actor-Critic（演员-评论家）
    ├── 核心思想：同时学习策略（Actor）和价值函数（Critic）
    ├── 策略表示：显式策略 + 显式价值函数
    ├── 优化目标：Actor用策略梯度，Critic用TD误差
    └── 代表：A3C, DDPG, TD3, SAC
```

### 三大范式的核心张力

| 维度 | Value-Based | Policy-Based | Actor-Critic |
|------|------------|--------------|-------------|
| **方差** | 低（BootStrapping） | 高（MC采样） | 中（两者结合） |
| **偏差** | 高（函数逼近误差） | 低（无偏估计） | 中 |
| **连续动作** | 困难（需离散化） | 天然支持 | 天然支持 |
| **样本效率** | 高（经验回放） | 低（on-policy） | 中-高 |
| **稳定性** | 中（收敛难） | 低（高方差） | 高（互补） |
| **可解释性** | 高（Q值直观） | 低 | 中 |

---

## 三、论文分析路线图

### 📘 Volume I：Value-Based Methods

| 编号 | 论文 | 年份 | 核心贡献 |
|------|------|------|----------|
| V-01 | **DQN** - Playing Atari with Deep RL | 2013/2015 | 经验回放 + 目标网络，开创深度RL时代 |
| V-02 | **Double DQN** - Deep RL with Double Q-learning | 2016 | 解决过估计问题，分离选择与评估 |
| V-03 | **Dueling DQN** - Dueling Network Architectures | 2016 | V(s)+A(s,a) 网络分解，状态价值单独建模 |
| V-04 | **PER** - Prioritized Experience Replay | 2016 | TD误差驱动的优先采样，打破均匀假设 |
| V-05 | **Rainbow** - Combining Improvements in DRL | 2018 | 六大改进集成，SOTA综合性能 |

### 📗 Volume II：Policy-Based Methods

| 编号 | 论文 | 年份 | 核心贡献 |
|------|------|------|----------|
| P-01 | **REINFORCE** - Simple Statistical Gradient-Following | 1992 | 策略梯度定理，RL梯度优化奠基 |
| P-02 | **TRPO** - Trust Region Policy Optimization | 2015 | 单调策略改进保证，KL散度约束 |
| P-03 | **PPO** - Proximal Policy Optimization | 2017 | TRPO的实用简化，Clip目标函数 |

### 📙 Volume III：Actor-Critic Methods

| 编号 | 论文 | 年份 | 核心贡献 |
|------|------|------|----------|
| A-01 | **A3C** - Asynchronous Methods for Deep RL | 2016 | 异步并行Actor，打破经验回放依赖 |
| A-02 | **DDPG** - Continuous Control with DRL | 2016 | 连续动作确定性策略梯度 |
| A-03 | **TD3** - Addressing Function Approximation Error | 2018 | 双Critic + 延迟更新，修复DDPG |
| A-04 | **SAC** - Soft Actor-Critic | 2018 | 最大熵框架，自动调温探索 |

### 📕 Volume IV：最终对比分析

| 编号 | 内容 |
|------|------|
| F-01 | 算法家族演化图谱 |
| F-02 | 多维度横向对比矩阵 |
| F-03 | 适用场景决策树 |
| F-04 | 工程实践选型指南 |

---

## 四、关键数学工具速查

### 4.1 策略梯度定理（Policy Gradient Theorem）

```
∇_θ J(θ) = E_{τ~π_θ} [ Σ_t ∇_θ log π_θ(a_t|s_t) · Q^π(s_t,a_t) ]
```

这是整个策略梯度家族的数学基石。

### 4.2 重要性采样（Importance Sampling）

用于 off-policy 学习，将期望从行为策略 β 转移至目标策略 π：

```
E_{x~π}[f(x)] = E_{x~β}[ (π(x)/β(x)) · f(x) ]
```

### 4.3 KL 散度（KL Divergence）

衡量两个策略分布的差异，TRPO 约束的核心：

```
KL(π_old || π_new) = Σ_a π_old(a|s) log [π_old(a|s) / π_new(a|s)]
```

### 4.4 时序差分误差（TD Error）

```
δ_t = r_t + γ V(s_{t+1}) - V(s_t)
```

### 4.5 广义优势估计（GAE，Schulman 2016）

```
Â_t^GAE(γ,λ) = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}
```

λ=0 退化为单步TD，λ=1 退化为MC回报。

---

## 五、符号系统约定

| 符号 | 含义 |
|------|------|
| θ | 策略网络参数 |
| φ | 价值网络参数 |
| π_θ(a&#124;s) | 参数化随机策略 |
| μ_θ(s) | 参数化确定性策略 |
| Q_φ(s,a) | 参数化Q函数 |
| V_φ(s) | 参数化状态价值函数 |
| θ̄, φ̄ | 目标网络参数（软更新或延迟复制） |
| D | 经验回放缓冲区 |
| τ | 轨迹 (s_0,a_0,r_0,s_1,...) |
| N | batch size |
| α | 学习率 |
| β_IS | 重要性采样修正指数 |

---

> **阅读建议**：按照 V-01 → V-05 → P-01 → P-03 → A-01 → A-04 → F-01 的顺序阅读，每篇均包含：论文背景、核心问题、关键创新、数学推导、伪代码、优缺点分析、实验结果、与前作的联系。
