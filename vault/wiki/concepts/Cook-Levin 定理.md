---
type: concept
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 数学
- 计算理论
aliases:
- Cook-Levin Theorem
- 库克-莱文定理
relates_to:
- target: "[[Stephen Cook]]"
  type: caused_by
  confidence: 0.99
  note: 1971年证明
- target: "[[Leonid Levin]]"
  type: caused_by
  confidence: 0.95
  note: 1973年独立证明
- target: "[[SAT 问题]]"
  type: caused
  confidence: 0.99
  note: 定理的核心结论
- target: "[[NP 完全性]]"
  type: part_of
  confidence: 0.99
  note: 定理确立了第一个 NP 完全问题
- target: "[[图灵机]]"
  type: depends_on
  confidence: 0.9
  note: 证明中将 NTM 计算编码为布尔公式
supersedes: null
---

# Cook-Levin 定理

## 概述

Cook-Levin 定理是计算复杂度理论的核心定理，由 Stephen Cook（1971）和 Leonid Levin（1973）独立证明，断言布尔可满足性问题（SAT）是 NP 完全的。

## 关键内容

### 定理陈述

**布尔可满足性问题（SAT）是 NP 完全的。**

更精确地说，即使是合取范式形式的可满足性问题（CNF-SAT）也是 NP 完全的。

### 证明思路

证明分为两部分：

**第一部分（SAT ∈ NP）**：给定布尔公式和一组变量赋值（证书），可以在多项式时间内验证该赋值是否使公式为真。

**第二部分（所有 NP 问题归约到 SAT）**：
1. 设 L 是任意 NP 语言，M 是在多项式时间 p(n) 内判定 L 的非确定性图灵机
2. 用**计算表**（computation tableau）描述 M 的计算：p(n) × p(n) 的二维表格
3. 为表格的每个单元格引入布尔变量：
   - Q_{i,k}：第 i 步处于状态 q_k
   - H_{i,j}：第 i 步读写头在位置 j
   - S_{i,j,k}：第 i 步位置 j 上写着符号 s_k
4. 构造布尔公式 Φ，包含：初始条件子句、合法性子句、转移规则子句、接受条件子句
5. 证明：M 接受 x 当且仅当 Φ 可满足

### 核心推论

- 如果 SAT ∈ P，则 P = NP
- 如果 P ≠ NP，则 SAT 不存在多项式时间算法
- 所有 NP 完全问题在复杂度上等价

### 历史意义

- 开启了 NP 完全性理论的整个领域
- Karp（1972）在此基础上证明了21个经典问题的 NP 完全性
- 今天已知有数千个 NP 完全问题

## 来源

- [[raw/books/计算机科学/08-cook-np-completeness.md]]

## 相关

- [[Stephen Cook]] — 1971年证明
- [[Leonid Levin]] — 1973年独立证明
- [[SAT 问题]] — 定理的结论
- [[NP 完全性]] — 定理确立的概念
- [[图灵机]] — 证明中使用的计算模型
