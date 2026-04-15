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
aliases:
- Chaitin's Omega
- Chaitin's Constant
- Ω 常数
- 停机概率
- 智慧之数
relates_to:
- target: '[[格雷戈里·柴廷]]'
  type: caused
  confidence: 0.95
- target: '[[柯尔莫哥洛夫复杂性]]'
  type: related_to
  confidence: 0.95
- target: '[[算法信息论]]'
  type: part_of
  confidence: 0.95
- target: '[[算法随机性]]'
  type: related_to
  confidence: 0.9
- target: '[[停机问题]]'
  type: related_to
  confidence: 0.9
supersedes: null
---

# Chaitin常数

## 概述

Chaitin 常数 Ω = Σ 2^{-|p|}（对所有停机程序求和）是"随机程序停机的概率"，一个不可计算的超越数，其二进制展开的每一位都是算法随机的，包含了所有有限规模[[停机问题]]的完整信息。

## 关键内容

### 定义

$$\Omega = \sum_{p: U(p) \text{ halts}} 2^{-|p|}$$

其中 U 是一台固定的前缀[[图灵机|通用图灵机]]，求和遍历所有停机的程序 p。

### 惊人性质

1. **良定义**：级数收敛（因为[[前缀码]]的 Kraft 不等式保证 Σ 2^{-|p|} ≤ 1）
2. **不可计算**：不存在算法能计算 Ω 的任意精度的近似值
3. **算法随机**：Ω 的二进制展开的每一位都是算法随机的——无法从前面任何有限位预测下一位
4. **全知性**：Ω 的前 n 位二进制展开包含了关于所有长度不超过 n 的程序是否停机的完整信息

### 直觉

Ω 是"一只猴子随机打字打出一个能停机的程序"的概率。它介于 0 和 1 之间，但你永远无法知道它的具体值。

### 与数学极限的关系

- ZFC 集合论（现代数学的标准基础）只能确定 Ω 的有限多位
- 你能知道 Ω 的前多少位，取决于你的公理系统有多强
- Ω 代表了**数学不可知性的精确度量**

### 与停机问题的关系

如果你知道了 Ω 的精确值，你就能解决所有有限规模的[[停机问题]]——只需枚举所有程序，逐步计算 Ω 的近似值，当近似值的前 n 位稳定时，你就知道哪些长度 ≤ n 的程序会停机。

### 历史

Ω 常数在 Chaitin 1975 年论文中正式提出，但其根基在 1966 年论文中已经埋下。Chaitin 称之为"智慧之数"（the number of wisdom）。

## 来源

- [[raw/books/信息论/10_chaitin_1966_length_of_programs.md]] — Chaitin (1966) 深度解析
- [A Theory of Program Size (Chaitin 1975)](https://doi.org/10.1145/321892.321894)

## 相关

- [[格雷戈里·柴廷]] — 提出者
- [[柯尔莫哥洛夫复杂性]] — Ω 的定义基础
- [[算法信息论]] — 所属学科
- [[算法随机性]] — Ω 的二进制展开是算法随机的
- [[停机问题]] — Ω 编码了所有有限停机问题的答案
