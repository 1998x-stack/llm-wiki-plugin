---
type: entity
entity_type: person
status: active
confidence: 0.9
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 历史
- 研究
aliases:
- Richard Manning Karp
- 理查德·卡普
relates_to:
- target: "[[Stephen Cook]]"
  type: extends
  confidence: 0.9
  note: 在 Cook 的基础上证明了21个 NP 完全问题
- target: "[[NP 完全性]]"
  type: extends
  confidence: 0.95
  note: 极大地拓展了 NP 完全问题的版图
- target: "[[Cook-Levin 定理]]"
  type: extends
  confidence: 0.9
  note: 利用该定理证明了大量问题的 NP 完全性
supersedes: null
---

# Richard Karp

## 概述

美国[[计算]]机科学家（1935–），1972年发表里程碑式论文《Reducibility among combinatorial problems》，通过一系列归约证明了21个经典组合问题都是 [[NP 完全性|NP 完全]]的，极大地拓展了 [[NP 完全性]]理论的应用范围。

## 关键内容

### Karp 的21个 NP 完全问题（1972）

通过从 SAT 出发的[[多项式时间归约]]，证明了以下21个问题都是 [[NP 完全性|NP 完全]]的：

**图论问题**：
- 团问题（CLIQUE）
- 独立集（INDEPENDENT SET）
- 顶点覆盖（VERTEX COVER）
- 图着色（GRAPH COLORING）
- 哈密顿回路（HAMILTONIAN CIRCUIT）

**逻辑问题**：
- 3-SAT

**数论/优化问题**：
- 背包问题（KNAPSACK）
- 子集和问题（SUBSET SUM）
- 整数规划（INTEGER PROGRAMMING）

**调度问题**：
- 作业车间调度（JOB SHOP SCHEDULING）

### 方法论贡献

Karp 的工作展示了多项式归约作为工具的强大威力——一旦知道 SAT 是 [[NP 完全性|NP 完全]]的，只需要把 SAT 归约到一个新问题，就能证明新问题也是 [[NP 完全性|NP 完全]]的。这种"链式传递"的归约方法成为了后来 [[NP 完全性]]证明的标准[[规范化理论|范式]]。

### 影响

今天已知有数千个问题是 [[NP 完全性|NP 完全]]的，Karp 的21个问题是这条归约链的起点。

## 来源

- [[raw/books/计算机科学/08-cook-np-completeness.md]]

## 相关

- [[Stephen Cook]] — 在其基础上拓展
- [[NP 完全性]] — 极大拓展
- [[Cook-Levin 定理]] — 利用该定理
