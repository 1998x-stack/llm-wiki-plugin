---
type: entity
entity_type: paper
status: active
confidence: 0.98
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 历史
- 计算理论
aliases:
- The Complexity of Theorem-Proving Procedures
- Cook 1971 论文
- NP 完全性论文
relates_to:
- target: "[[Stephen Cook]]"
  type: caused_by
  confidence: 0.99
  note: 唯一作者
- target: "[[NP 完全性]]"
  type: caused
  confidence: 0.99
  note: 首次定义了 NP 完全性概念
- target: "[[SAT 问题]]"
  type: caused
  confidence: 0.99
  note: 证明了 SAT 是第一个 NP 完全问题
- target: "[[Cook-Levin 定理]]"
  type: caused
  confidence: 0.99
  note: 论文的核心定理
- target: "[[P vs NP]]"
  type: caused
  confidence: 0.95
  note: 为 P vs NP 问题奠定了基础
- target: "[[多项式时间归约]]"
  type: caused
  confidence: 0.95
  note: 确立了归约作为复杂度比较工具
- target: "[[计算复杂度理论]]"
  type: caused
  confidence: 0.95
  note: 建立了该领域的核心框架
- target: "[[图灵机]]"
  type: depends_on
  confidence: 0.9
  note: 使用非确定性图灵机定义 NP
- target: "[[λ 演算]]"
  type: compares_to
  confidence: 0.7
  note: 两者都是计算理论的核心基础
supersedes: null
---

# Cook NP 完全性论文

## 概述

[[Stephen Cook]] 于1971年发表的《The Complexity of Theorem-Proving Procedures》，是[[计算复杂度理论]]史上最具影响力的文献，首次定义了 [[NP 完全性]]概念并证明了 SAT 是第一个 [[NP 完全性|NP 完全问题]]。

## 关键内容

### 论文信息

| 条目 | 内容 |
|------|------|
| **标题** | The Complexity of Theorem-Proving Procedures |
| **作者** | [[Stephen Cook|Stephen Arthur Cook]]（1939–2023） |
| **发表时间** | 1971年 |
| **会议** | Proceedings of the Third Annual ACM Symposium on Theory of Computing (STOC), pp. 151-158 |

### 核心贡献

- **[[NP 完全性]]定义**：一个问题 L 是 [[NP 完全性|NP 完全]]的，如果 L ∈ NP 且所有 NP 问题都可以[[多项式时间归约]]到 L
- **[[Cook-Levin 定理]]**：[[SAT 问题|布尔可满足性问题]]（SAT）是 [[NP 完全性|NP 完全]]的
- **证明方法**：将非确定性[[图灵机]]的[[计算]]过程编码为布尔公式
- **[[多项式时间归约]]**：确立了归约作为复杂度比较的工具

### 历史影响

- Karp（1972）证明了21个经典组合问题都是 [[NP 完全性|NP 完全]]的
- [[P vs NP]] 成为千禧年数学问题（悬赏100万美元）
- Cook 于1982年获得[[阿兰·图灵|图灵]]奖
- 改变了[[算法]]研究的方法论

## 来源

- [[raw/books/计算机科学/08-cook-np-completeness.md]]

## 相关

- [[Stephen Cook]] — 作者
- [[NP 完全性]] — 论文定义的核心概念
- [[SAT 问题]] — 第一个被证明的 NP 完全问题
- [[Cook-Levin 定理]] — 论文的核心定理
- [[P vs NP]] — 论文奠定的问题
- [[计算复杂度理论]] — 建立的领域
