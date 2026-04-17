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
- 计算理论
aliases:
- NP-completeness
- NP 完全
- NP 完全问题
relates_to:
- target: "[[Stephen Cook]]"
  type: caused_by
  confidence: 0.99
  note: 定义者
- target: "[[Cook NP 完全性论文]]"
  type: caused_by
  confidence: 0.99
  note: 首次定义
- target: "[[Cook-Levin 定理]]"
  type: depends_on
  confidence: 0.99
  note: SAT 是第一个 NP 完全问题
- target: "[[SAT 问题]]"
  type: related_to
  confidence: 0.99
  note: 第一个被证明的 NP 完全问题
- target: "[[P vs NP]]"
  type: related_to
  confidence: 0.95
  note: NP 完全问题的存在使 P vs NP 具有"全有或全无"的性质
- target: "[[多项式时间归约]]"
  type: depends_on
  confidence: 0.95
  note: NP 完全性的定义依赖归约
- target: "[[计算复杂度理论]]"
  type: part_of
  confidence: 0.95
  note: 该领域的核心概念
- target: "[[Leonid Levin]]"
  type: related_to
  confidence: 0.85
  note: 独立提出
- target: "[[Richard Karp]]"
  type: extends
  confidence: 0.85
  note: 证明了21个 NP 完全问题
supersedes: null
---

# NP 完全性

## 概述

NP 完全性（NP-completeness）是计算复杂度理论中的核心概念，由 Stephen Cook 于1971年定义。一个问题 L 是 NP 完全的，如果 L ∈ NP 且 NP 中所有问题都可以多项式时间归约到 L。

## 关键内容

### 定义

一个问题 L 是 **NP 完全的**，如果满足两个条件：
1. **L ∈ NP**（它属于 NP）
2. **对于所有 L' ∈ NP，L' ≤ₚ L**（NP 中所有问题都可以多项式时间归约到它）

如果一个问题只满足条件（2）而不一定属于 NP，则称之为 **NP 困难的**（NP-hard）。

### 核心性质

**"一荣俱荣、一损俱损"**：
- 如果任何一个 NP 完全问题有多项式算法，则 P = NP，所有 NP 完全问题都有多项式算法
- 如果任何一个 NP 完全问题被证明没有多项式算法，则 P ≠ NP，所有 NP 完全问题都没有多项式算法

### 第一个 NP 完全问题

[[Cook-Levin 定理]]证明了**布尔可满足性问题（SAT）**是第一个 NP 完全问题。此后，[[Richard Karp|Karp]]（1972）证明了21个经典组合问题都是 NP 完全的，今天已知有数千个 NP 完全问题。

### 实际意义

- 如果一个问题被证明是 NP 完全的，继续寻找精确的多项式算法是徒劳的（假设 P ≠ NP）
- 应当转向近似算法、启发式方法或特殊情况的高效算法
- 现代 SAT 求解器（如 MiniSat、CaDiCaL）可以在合理时间内求解数百万变量的工业级实例

## 来源

- [[raw/books/计算机科学/08-cook-np-completeness.md]]

## 相关

- [[Stephen Cook]] — 定义者
- [[Cook NP 完全性论文]] — 首次定义
- [[Cook-Levin 定理]] — SAT 是 NP 完全的
- [[SAT 问题]] — 第一个 NP 完全问题
- [[P vs NP]] — NP 完全性使其具有"全有或全无"性质
- [[多项式时间归约]] — 定义的基础工具
- [[计算复杂度理论]] — 所属领域
- [[Leonid Levin]] — 独立提出
- [[Richard Karp]] — 拓展者
