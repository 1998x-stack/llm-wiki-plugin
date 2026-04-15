# V-02/03/04：DQN 三大改进
## Double DQN · Dueling DQN · Prioritized Experience Replay

---

# Part A：Double DQN（V-02）
## Deep Reinforcement Learning with Double Q-learning

**论文信息**
- 作者：Hado van Hasselt, Arthur Guez, David Silver（DeepMind）
- 发表：AAAI 2016
- arXiv：1509.06461

---

## A.1 核心问题：Q值过估计（Overestimation Bias）

### A.1.1 过估计的数学根源

DQN 使用以下 TD 目标：
```
y_DQN = r + γ · max_{a'} Q_{θ̄}(s', a')
```

**问题**：`max` 操作在有噪声的Q函数估计上**系统性地产生正偏差**。

**严格证明（van Hasselt 2010）**：

设 Q*(s',a') 的真实值为 q*，对所有动作 a' 的噪声估计量 Q(s',a') 满足 E[Q(s',a')] = q*。则：

```
E[ max_{a'} Q(s',a') ] ≥ max_{a'} E[ Q(s',a') ] = max_{a'} q* = q*
```

**Jensen 不等式**直接给出：max 的期望 ≥ 期望的 max。即只要存在估计噪声（哪怕无偏），max 操作就会产生正偏差。

**直觉**：在 n 个动作中取最大值，噪声中偶然较高的那个会被选中，导致系统性高估。

### A.1.2 过估计的危害

1. **偏差传播**：TD bootstrapping 将过估计的目标向下传播，错误累积
2. **策略退化**：过估计的Q值导致次优动作被高估，影响策略改进
3. **训练不稳定**：正反馈循环加剧训练不稳定

---

## A.2 解决方案：解耦选择与评估

### A.2.1 原始 Double Q-learning（van Hasselt 2010）

维护两套独立的Q函数 Q^A 和 Q^B，交替更新：
```
y^A = r + γ · Q^B(s', argmax_{a'} Q^A(s', a'))
y^B = r + γ · Q^A(s', argmax_{a'} Q^B(s', a'))
```

**核心思想**：**选择**动作（argmax）和**评估**Q值（Q()）使用两个不同的网络，打破正相关性。

### A.2.2 Double DQN：利用目标网络

DQN 已经有两个网络（在线网络 θ 和目标网络 θ̄），Double DQN 直接利用这一现有结构：

**DQN 目标**（有过估计）：
```
y_DQN = r + γ · max_{a'} Q_{θ̄}(s', a')
       = r + γ · Q_{θ̄}(s', argmax_{a'} Q_{θ̄}(s', a'))
```
（选择和评估都用目标网络）

**Double DQN 目标**（去偏）：
```
y_DoubleDQN = r + γ · Q_{θ̄}(s', argmax_{a'} Q_θ(s', a'))
```
- **选择**最优动作：用**在线网络** Q_θ
- **评估** Q 值：用**目标网络** Q_{θ̄}

**只改变一行代码**，却从根本上解决了过估计问题。

---

## A.3 算法伪代码

```
Double DQN 仅修改目标计算部分（相比 DQN）：

// DQN 的目标计算：
a*_target = argmax_{a'} Q_{θ̄}(s', a')      ← 目标网络选择
y_DQN = r + γ · Q_{θ̄}(s', a*_target)       ← 目标网络评估

// Double DQN 的目标计算：
a*_online = argmax_{a'} Q_θ(s', a')          ← 在线网络选择（★改变点）
y_DDQN = r + γ · Q_{θ̄}(s', a*_online)      ← 目标网络评估
```

---

## A.4 实验结果

**在 49 款 Atari 游戏上的对比：**

| 方法 | 中位数得分（相对人类）| 过估计量 |
|------|---------------------|---------|
| DQN | 79% | 严重（平均 ~300% 高估）|
| Double DQN | 117% | 显著降低 |

- Double DQN 在 **49 个游戏中的 41 个**表现优于 DQN
- Q值过估计从平均 300% 降至接近真实值
- 在 Wizard of Wor 等游戏中提升超过 2 倍

---

## A.5 局限性

- 过估计未完全消除（仅降低，理论上仍存在偏差）
- 两网络仍然高度相关（非独立），完全去偏需要独立的两套网络
- 在某些游戏中（低估情况）Double DQN 反而略差

---

---

# Part B：Dueling DQN（V-03）
## Dueling Network Architectures for Deep Reinforcement Learning

**论文信息**
- 作者：Ziyu Wang, Tom Schaul, Matteo Hessel 等（DeepMind）
- 发表：ICML 2016
- arXiv：1511.06581

---

## B.1 核心洞察：Q值的结构分解

### B.1.1 状态价值 vs 动作优势

**关键观察**：在很多状态下，动作的选择根本不重要！

例如在 Atari 赛车游戏中，当赛道前方无障碍时，向左/向右/直行的Q值差异极小，真正重要的是**这个状态有多好**（V(s)），而不是各动作的相对优势（A(s,a)）。

**数学分解**：
```
Q^π(s,a) = V^π(s) + A^π(s,a)

其中：
V^π(s) = E_{a~π}[ Q^π(s,a) ]              ← 状态价值，与动作无关
A^π(s,a) = Q^π(s,a) - V^π(s)              ← 动作优势，均值为0
```

### B.1.2 为什么要分离学习？

**问题**：标准 DQN 必须对每个 (s,a) 对都有足够的样本才能准确估计 Q(s,a)

**优势**：
- **V(s)** 可以从所有动作的经验中学习（样本效率更高）
- **A(s,a)** 只需要学习动作之间的相对差异
- 在动作不重要的状态下，V(s) 更新更频繁更准确

---

## B.2 网络架构

```
标准 DQN 架构：
  卷积层 → 全连接层 → Q(s,a₁), Q(s,a₂), ..., Q(s,a_|A|)
                        ↑ 单一输出流

Dueling DQN 架构：
  卷积层 → 全连接层 → 分叉 → 价值流（Value Stream）:    V(s;θ,β)      ← 标量
                           → 优势流（Advantage Stream）: A(s,a;θ,α)   ← |A| 维向量
                           → 合并 → Q(s,a;θ,α,β)
```

**合并操作（去均值技巧）**：

朴素合并：`Q(s,a) = V(s) + A(s,a)` 存在**不可辨识问题**（unidentifiability）：
V 和 A 的绝对值不唯一，可以同时加减任意常数而Q值不变。

**解决方案**：对优势流去均值：
```
Q(s,a;θ,α,β) = V(s;θ,β) + [ A(s,a;θ,α) - (1/|A|) Σ_{a'} A(s,a';θ,α) ]
```

**效果**：
- 强制 A 的均值为 0，使得 V 真正代表状态价值
- 梯度更稳定，每次更新都同时改进 V 和 A 的估计

**另一种变体（最大值去均值）**：
```
Q(s,a;θ,α,β) = V(s;θ,β) + [ A(s,a;θ,α) - max_{a'} A(s,a';θ,α) ]
```
这确保最优动作的A值为0，V(s) = max_a Q(s,a) = Q*(s)。

---

## B.3 伪代码（仅架构差异）

```python
class DuelingDQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        # 共享特征提取层（与 DQN 相同）
        self.features = nn.Sequential(
            nn.Conv2d(4, 32, 8, stride=4), nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1), nn.ReLU(),
            nn.Flatten()
        )
        # 价值流：输出标量 V(s)
        self.value_stream = nn.Sequential(
            nn.Linear(3136, 512), nn.ReLU(),
            nn.Linear(512, 1)
        )
        # 优势流：输出 |A| 维向量 A(s,a)
        self.advantage_stream = nn.Sequential(
            nn.Linear(3136, 512), nn.ReLU(),
            nn.Linear(512, action_dim)
        )

    def forward(self, x):
        features = self.features(x)
        V = self.value_stream(features)          # (B, 1)
        A = self.advantage_stream(features)      # (B, |A|)
        # 去均值合并（关键）
        Q = V + (A - A.mean(dim=1, keepdim=True))
        return Q
```

---

## B.4 实验结果

- 在 49 款 Atari 游戏中，**57% 的游戏**（28/49）优于 Double DQN
- 在动作选择不关键的游戏（如 Centipede）上提升最显著
- 在 Atari 平均得分上比 Double DQN 提升约 **15-20%**

---

---

# Part C：Prioritized Experience Replay（V-04）
## Prioritized Experience Replay

**论文信息**
- 作者：Tom Schaul, John Quan, Ioannis Antonoglou, David Silver（DeepMind）
- 发表：ICLR 2016
- arXiv：1511.05952

---

## C.1 核心问题：均匀采样的低效性

**DQN 的均匀采样假设**：回放缓冲区中所有 transition 对学习同等重要。

**这是错的！**

**直觉**：
- 智能体已经学得很好的 transition（TD 误差小）→ 再学一遍收益小
- 罕见但信息量大的 transition（TD 误差大）→ 应该更频繁地学习
- 监督学习中的"难例挖掘"（Hard Example Mining）与此类似

---

## C.2 优先级采样机制

### C.2.1 优先级定义

使用 **TD 误差**的绝对值作为优先级指标：

```
p_i = |δ_i| + ε

其中：
δ_i = r + γ max_{a'} Q_{θ̄}(s', a') - Q_θ(s, a)   ← TD 误差
ε = 小正常数（避免优先级为0）
```

### C.2.2 采样概率

```
P(i) = p_i^α / Σ_k p_k^α

其中 α 控制优先化程度：
  α = 0 → 均匀采样（退化为 DQN）
  α = 1 → 完全按优先级采样
  典型值：α = 0.6
```

### C.2.3 重要性采样修正（IS Correction）

**问题**：非均匀采样改变了数据分布，引入偏差，破坏梯度估计的无偏性。

**解决**：重要性采样权重修正：
```
w_i = (1 / (N · P(i)))^β / max_j w_j

其中 β 从初始值 β_0 线性退火至 1.0
  β = 0 → 不做修正（有偏）
  β = 1 → 完全修正（无偏）
  β_0 = 0.4（从偏置开始，训练后期恢复无偏）

修正后的损失：Loss = Σ_i w_i · (δ_i)^2
```

**β 退火策略的直觉**：训练初期高优先级样本差异大，IS修正可能引入高方差；训练后期需要精确的无偏梯度，β→1 恢复无偏。

---

## C.3 高效实现：SumTree

### C.3.1 问题

每次更新所有样本的优先级并重新计算采样概率在 O(N) 时间复杂度下不可行（N=10^6）。

### C.3.2 SumTree 数据结构

```
SumTree（线段树）：叶节点存储每个transition的p_i^α，
                  内部节点存储子树的 Σp^α

        58
       /  \
     29    29
    / \   / \
  13  16 15  14
  /\  /\
 3 10 12 4
（叶节点 = 实际优先级）

操作复杂度：
- 更新优先级：O(log N)
- 按优先级采样：O(log N)（将目标值逐层二分查找）
- 总复杂度：O(N log N) 而非 O(N²)
```

---

## C.4 完整算法

```
PER（优先经验回放）算法
======================
初始化：
  SumTree 结构的回放缓冲区，容量 N
  优先化指数 α = 0.6
  IS 修正指数 β₀ = 0.4，β_max = 1.0，退火步数 T

每步训练：
  1. 执行动作，存储 transition (s,a,r,s',done)
     初始优先级 p = max(已有p的最大值)  ← 新样本优先级最高（保证至少被采样一次）

  2. 从 SumTree 按 P(i) ∝ p_i^α 采样 B 个 transition

  3. 计算重要性权重：
     w_i = (1/(N·P(i)))^β
     归一化：w_i ← w_i / max_j w_j

  4. 计算 TD 误差 δ_i（使用 Double DQN 目标）

  5. 加权损失：Loss = (1/B) Σ_i w_i · (δ_i)^2

  6. 更新 SumTree 中对应 transition 的优先级：
     p_i ← |δ_i| + ε

  7. β ← min(1.0, β + β_step)  ← β 退火
```

---

## C.5 实验结果

| 方法 | Atari 平均提升 |
|------|--------------|
| DQN | 基准 |
| DQN + PER | +46% |
| Double DQN | +30%（相对DQN） |
| Double DQN + PER | +97%（相对DQN） |

PER 与 Double DQN 有很强的协同效应，组合使用性能接近翻倍。

---

## C.6 PER 的变体：基于排名的优先级（Rank-based）

除了比例优先级，论文还提出基于排名的方法：

```
P(i) = rank(i)^{-α} / Σ_k rank(k)^{-α}

rank(i) = transition i 按 TD 误差从大到小的排名

优点：对异常值（outlier TD errors）更鲁棒
缺点：更新复杂，需要维护有序结构
```

---

## D. 三篇论文横向对比

| 维度 | Double DQN | Dueling DQN | PER |
|------|-----------|-------------|-----|
| **问题** | Q值过估计 | 状态/动作价值混淆 | 均匀采样低效 |
| **修改位置** | 目标计算 | 网络架构 | 数据采样 |
| **实现难度** | ⭐（一行代码）| ⭐⭐（架构修改）| ⭐⭐⭐（SumTree）|
| **理论依据** | 概率论（Jensen）| 价值分解 | 非均匀采样 |
| **正交性** | 与其他三者正交 | 与其他三者正交 | 与其他三者正交 |
| **Atari 提升** | +38% | +15-20% | +46% |
| **组合效果** | 强协同 | 强协同 | 强协同 |
| **被Rainbow采用** | ✅ | ✅ | ✅ |

**关键结论**：这三项改进**相互正交**，可以任意组合，这为 Rainbow 的诞生奠定了基础。

---

## 总结

| 论文 | 一句话总结 |
|------|-----------|
| **Double DQN** | max 操作导致过估计；用在线网络选动作、目标网络评估Q值，解耦两步 |
| **Dueling DQN** | Q(s,a) = V(s) + A(s,a)；通过网络架构分离学习状态价值和动作优势 |
| **PER** | TD误差大的样本更有学习价值；SumTree实现O(logN)优先采样+IS权重修正 |
