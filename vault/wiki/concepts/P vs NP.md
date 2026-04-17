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
- P versus NP
- P vs NP 问题
- P = NP ?
relates_to:
- target: "[[NP 完全性]]"
  type: related_to
  confidence: 0.99
  note: NP 完全问题的存在使该问题具有"全有或全无"的性质
- target: "[[Cook NP 完全性论文]]"
  type: caused_by
  confidence: 0.95
  note: 论文为该问题奠定了基础
- target: "[[Stephen Cook]]"
  type: caused_by
  confidence: 0.9
  note: 奠基者
- target: "[[SAT 问题]]"
  type: related_to
  confidence: 0.9
  note: SAT 是该问题的关键
- target: "[[计算复杂度理论]]"
  type: part_of
  confidence: 0.95
  note: 该领域最重要的未解问题
- target: "[[图灵机]]"
  type: depends_on
  confidence: 0.85
  note: 复杂度类基于图灵机定义
supersedes: null
---

# P vs NP

## 概述

P vs NP 是[[计算复杂度理论]]中最重要的未解问题，问的是：是否所有能快速验证答案的问题都能快速找到答案？被 Clay 数学研究所列为七大千禧年数学问题之一，悬赏100万美元。

## 关键内容

### 问题表述

**P = NP ?**

- **P**（Polynomial time）：所有可以被确定性[[图灵机]]在多项式时间内求解的判定问题的集合
- **NP**（Non-deterministic Polynomial time）：所有可以被非确定性[[图灵机]]在多项式时间内求解的判定问题的集合

**注意**：NP 不是"Non-Polynomial"的缩写，而是"Non-deterministic Polynomial"。

### 直观理解

- P = "容易求解"的问题
- NP = "容易验证"的问题
- P ⊆ NP（P 中的所有问题都属于 NP）
- P vs NP 问的是：P 是否等于 NP？

### NP 完全性的关键作用

[[NP 完全性]]的存在使该问题具有"全有或全无"的性质：
- 如果任何一个 [[NP 完全性|NP 完全问题]]有多项式算法，则 P = NP
- 如果任何一个 [[NP 完全性|NP 完全问题]]没有多项式算法，则 P ≠ NP

### 当前状态

- 自1971年提出以来已超过50年，至今悬而未决
- 2000年被列为千禧年数学问题（悬赏100万美元）
- 2012年调查显示约83%的受访专家相信 P ≠ NP
- 但没有任何证明

### 如果 P = NP 的后果

- 所有 [[NP 完全性|NP 完全问题]]都有多项式算法
- 现代密码学（RSA、Diffie-Hellman 等）的安全性将崩溃
- 数学证明的自动发现成为可能

### 如果 P ≠ NP 的后果

- 存在本质上困难的问题，没有快速算法
- 密码学的安全性基础得到理论支撑
- "创造比验证更难"的直觉得到数学证明

## 来源

- [[raw/books/计算机科学/08-cook-np-completeness.md]]

## 相关

- [[NP 完全性]] — 使问题具有"全有或全无"性质
- [[Cook NP 完全性论文]] — 奠定基础
- [[Stephen Cook]] — 奠基者
- [[SAT 问题]] — 关键问题
- [[计算复杂度理论]] — 所属领域
- [[图灵机]] — 定义基础
