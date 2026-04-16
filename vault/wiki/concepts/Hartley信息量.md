---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 信息论
aliases:
- Hartley Entropy
- Hartley Measure
- 哈特莱信息量
- Hartley 度量
relates_to:
- target: '[[拉尔夫·哈特莱]]'
  type: caused
  confidence: 0.95
- target: '[[信息论]]'
  type: part_of
  confidence: 0.9
- target: '[[克劳德·香农]]'
  type: extends
  confidence: 0.9
supersedes: null
---

# Hartley信息量

## 概述

Hartley 信息量是 [[拉尔夫·哈特莱|R. V. L. Hartley]] (1928) 提出的信息度量公式：H = n · log s，表示在 s 个不同符号中传输 n 个符号所携带的信息量，是 Shannon [[信息熵]]在均匀分布下的特殊情况。

## 关键内容

### 公式

**H = n · log s**

- H：信息量
- n：消息中的符号个数
- s：字母表大小（可用的不同符号数）
- log：对数（底数决定度量单位）

### 直觉解释

- 在 2 个选项中选择 1 个：log 2 = 1 bit
- 在 4 个选项中选择 1 个：log 4 = 2 bit（等于做了 2 次二选一）
- 发送 10 个二进制符号：10 × log 2 = 10 bit
- 选择空间越大，一次选择传达的信息越多

### 为什么用对数？

基于**可加性**要求：两个独立选择过程，总选择数是 s₁ × s₂（乘积），但希望总信息量等于两次信息量之和。唯一满足此性质的函数是对数：H = log(s₁ × s₂) = log s₁ + log s₂

### 与 Shannon 熵的关系

Shannon 熵：H(X) = -Σ pᵢ log pᵢ

当所有符号等概率（pᵢ = 1/s）时：H(X) = log s，恰好就是 Hartley 的单符号信息量。因此 **Hartley 度量是 Shannon 熵在均匀分布下的特殊情况。**

### 现代视角

- Hartley 熵等价于 Rényi 熵在 α = 0 时的取值，度量的是"支撑集的大小"
- 在密码学和安全性分析中仍有独立价值
- 在加密后的数据流等场景中，等概率假设实际上是合理的

### 度量单位

以 10 为底时单位为"Hartley"（也称 ban 或 dit），1 Hartley = log₂ 10 ≈ 3.322 bit。

## 来源

- [[raw/books/信息论/01_hartley_1928_transmission_of_information.md]] — Hartley (1928): Transmission of Information 深度解析

## 相关

- [[拉尔夫·哈特莱]] — 提出者
- [[信息论]] — 所属学科
- [[克劳德·香农]] — 理论推广者（概率化信息熵）
