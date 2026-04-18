---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 数学
- 信息论
aliases:
- Shannon-Hartley Theorem
- Shannon-Hartley Law
- 香农-哈特莱定理
- 香农-哈特莱信道容量公式
relates_to:
- target: '[[克劳德·香农]]'
  type: caused
  confidence: 0.95
- target: '[[拉尔夫·哈特莱]]'
  type: extends
  confidence: 0.9
- target: '[[信道容量]]'
  type: extends
  confidence: 0.95
- target: '[[信息论]]'
  type: part_of
  confidence: 0.95
- target: '[[采样定理]]'
  type: depends_on
  confidence: 0.9
supersedes: null
---

# Shannon-Hartley公式

## 概述

Shannon-Hartley 公式是 Shannon (1949) 给出的连续[[信道容量]]公式：C = W log₂(1 + S/N)，精确量化了带宽 W、[[信噪比]] S/N 与可靠传输速率上限之间的关系，是通信工程的"[[万有引力定律|万有引力]]公式"。

## 关键内容

### 公式

$$C = W \log_2\left(1 + \frac{S}{N}\right) \quad \text{(bit/s)}$$

其中：
- C：[[信道容量]]（每秒最多可靠传输的比特数）
- W：信道带宽（Hz）
- S：信号平均功率（瓦特）
- N：噪声平均功率（瓦特）
- S/N：[[信噪比]]（无量纲）

### 等价表示（使用噪声功率谱密度 N₀）

$$C = W \log_2\left(1 + \frac{S}{N_0 W}\right)$$

### 三种直觉解释

1. **信号分辨率**：[[信噪比]] S/N 决定了可[[区分]]的信号电平数，约 √(1 + S/N) 个。每秒 2W 个独立样本，每个样本 log₂ √(1 + S/N) bit，总计 W · log₂(1 + S/N)

2. **球填充**：高维空间中，大球（信号+噪声）体积除以小球（噪声）体积给出最大消息数。体积比为 ((S+N)/N)^(n/2)，取对数得到信息量

3. **自由度与精度**：信息量 = 自由度数 × 每个自由度的精度。自由度数 = 2W（每秒独立样本数），精度 = (1/2) · log₂(1 + S/N)

### 带宽-功率权衡

**增加带宽**（W → ∞，S 和 N₀ 固定）：
$$C \to \frac{S}{N_0 \ln 2} \approx 1.44 \frac{S}{N_0}$$

即使带宽无限大，[[信道容量]]也有上界！因为增加带宽也增加了总噪声功率（N = N₀W）。

**增加[[信噪比]]**（S/N → ∞，W 固定）：
$$C \approx W \log_2\frac{S}{N}$$

[[信噪比]]增长可以无限提高容量，但只是对数增长——每增加 3 dB 的[[信噪比]]只多 1 bit/s/Hz。

### Shannon 极限

无限带宽极限下，每 bit 信息需要的最低能量：
$$\frac{E_b}{N_0} \bigg|_{\min} = \ln 2 \approx -1.59 \text{ dB}$$

这是物理上可靠通信所需的最低能量。Turbo 码和 LDPC 码在 2000 年代达到了距 Shannon 极限 0.1 dB 以内的性能。

### 与 Hartley 的关系

Hartley (1928) 给出了无噪声情况下的信息量 H = n · log s。Shannon-Hartley 公式将其推广到有噪声的连续信道，将噪声的影响精确量化为 S/N 项。

## 来源

- [[raw/books/信息论/03_shannon_1949_communication_in_presence_of_noise.md]] — Shannon (1949): Communication in the Presence of Noise 深度解析

## 相关

- [[克劳德·香农]] — 提出者
- [[拉尔夫·哈特莱]] — 无噪声情况下的先驱
- [[信道容量]] — 离散信道容量的连续推广
- [[信息论]] — 所属学科
- [[采样定理]] — 公式推导的前提
