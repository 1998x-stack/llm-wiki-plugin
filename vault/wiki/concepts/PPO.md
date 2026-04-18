---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "策略梯度", "算法", "RLHF"]
aliases: ["Proximal Policy Optimization", "近端策略优化", "PPO-Clip", "PPO 2017"]
relates_to:
  - target: "TRPO"
    type: supersedes
    confidence: 0.95
  - target: "[[策略梯度定理]]"
    type: implements
    confidence: 0.95
  - target: "[[广义优势估计]]"
    type: uses
    confidence: 0.95
  - target: "[[重要性采样]]"
    type: uses
    confidence: 0.9
  - target: "[[KL散度]]"
    type: compares_to
    confidence: 0.8
  - target: "[[强化学习三大范式]]"
    type: part_of
    confidence: 0.85
supersedes: null
---

# PPO

## 概述
Schulman et al. ([[OpenAI]], 2017) 提出的近端策略优化算法。通过 Clip 目标函数近似 TRPO 的信赖域约束，在保留近似单调改进保证的同时实现一阶优化（普通 SGD/Adam），成为 2017-2023 年工业界最广泛使用的 RL 算法，也是 RLHF（InstructGPT/ChatGPT）的核心组件。

## 关键内容

1. **PPO-Clip 核心目标**：
   `L^{CLIP}(θ) = E_t [ min(r_t(θ)·Â_t, clip(r_t(θ), 1-ε, 1+ε)·Â_t) ]`
   r_t(θ) = π_θ/π_θ_old 为[[重要性采样]]比，ε=0.2。Clip 操作使梯度在比率超出 [1-ε, 1+ε] 时归零，天然限制更新幅度，无需二阶优化。

2. **完整损失函数**：
   `L^{PPO} = L^{CLIP} - c₁·L^{VF} + c₂·S[π]`
   三项分别为策略目标（最大化）、[[价值函数]]损失（最小化）、熵正则化（最大化，促进探索）。

3. **GAE 优势估计**：使用[[广义优势估计]]（λ=0.95）计算 Â_t，在偏差-方差之间取得平衡，是 PPO 训练稳定的关键。

4. **数据复用（多轮更新）**：每批数据收集后执行 K=10 轮 mini-batch 更新，提高样本效率，是相较 TRPO 的重要工程优势。

5. **工程细节**：优势归一化 (Â-mean)/std；梯度裁剪 max norm 0.5；Adam 学习率 3e-4；并行环境数据收集（N×T transitions）。

6. **广泛应用**：[[OpenAI]] Dactyl（机器人）、[[OpenAI]] Five（Dota2）、InstructGPT/ChatGPT（RLHF）、AlphaStar，是 RLHF 标准算法选择。

## 来源
- [[raw/assets/RL-Analysis/rl_04_reinforce_trpo_ppo]] — P-03：PPO 完整分析（Schulman et al. OpenAI 2017）

## 相关
- TRPO — supersedes
- [[策略梯度定理]] — implements
- [[广义优势估计]] — uses
- [[重要性采样]] — uses
- [[KL散度]] — compares_to
- [[强化学习三大范式]] — part_of
