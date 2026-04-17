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
- Boolean Satisfiability Problem
- SAT
- 布尔可满足性问题
relates_to:
- target: "[[Cook-Levin 定理]]"
  type: caused_by
  confidence: 0.99
  note: 被证明为第一个 NP 完全问题
- target: "[[NP 完全性]]"
  type: part_of
  confidence: 0.99
  note: 第一个被证明的 NP 完全问题
- target: "[[Stephen Cook]]"
  type: caused_by
  confidence: 0.95
  note: 证明了其 NP 完全性
- target: "[[P vs NP]]"
  type: related_to
  confidence: 0.9
  note: SAT 是 P vs NP 的关键问题
- target: "[[图灵机]]"
  type: related_to
  confidence: 0.8
  note: Cook-Levin 定理中将 NTM 计算编码为 SAT
supersedes: null
---

# SAT 问题

## 概述

布尔可满足性问题（SAT）是计算复杂度理论中最核心的问题之一：给定一个布尔公式，判断是否存在一组变量赋值使得公式为真。1971年被 Cook 证明为第一个 NP 完全问题。

## 关键内容

### 问题定义

给定一个布尔公式 φ（由变量 x₁, x₂, ..., xₙ、逻辑连接词 ∧（与）、∨（或）、¬（非）组成），判断是否存在一组变量赋值（每个变量取 TRUE 或 FALSE），使得 φ 的值为 TRUE。

**示例**：
- `(x₁ ∨ ¬x₂) ∧ (¬x₁ ∨ x₃)` 是可满足的（取 x₁=TRUE, x₂=FALSE, x₃=TRUE）
- `x₁ ∧ ¬x₁` 是不可满足的

### CNF-SAT

Cook 证明了即使是**合取范式**（CNF）形式的 SAT 也是 NP 完全的：公式是若干子句的合取，每个子句是若干文字的析取。

### Cook-Levin 定理

Cook（1971）和 Levin（1973）独立证明了 SAT 是 NP 完全的——任何 NP 问题都可以在多项式时间内归约到 SAT。

### 现代 SAT 求解器

尽管 SAT 是 NP 完全的，现代 SAT 求解器取得了惊人的实际性能：
- **CDCL 算法**（Conflict-Driven Clause Learning）：MiniSat、CaDiCaL、Kissat
- 可以在合理时间内求解包含**数百万变量**和**数千万子句**的工业级实例
- 应用于硬件验证、软件测试、人工智能规划等领域

这并不与 NP 完全性矛盾——工业级 SAT 实例通常具有特殊结构（如社区结构、变量间的局部依赖关系），使得求解器可以避免最坏情况。

## 来源

- [[raw/books/计算机科学/08-cook-np-completeness.md]]

## 相关

- [[Cook-Levin 定理]] — SAT 是 NP 完全的
- [[NP 完全性]] — SAT 是第一个 NP 完全问题
- [[Stephen Cook]] — 证明了 SAT 的 NP 完全性
- [[P vs NP]] — SAT 是关键问题
- [[图灵机]] — 证明中使用的计算模型
