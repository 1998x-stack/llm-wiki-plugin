---
type: concept
status: active
confidence: 0.9
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
- Multics
- Multiplexed Information and Computing Service
relates_to:
- target: "[[UNIX]]"
  type: caused
  confidence: 0.9
  note: UNIX 是对 Multics 复杂性的反叛
- target: "[[Dennis Ritchie]]"
  type: related_to
  confidence: 0.8
  note: 曾参与 Multics 项目
- target: "[[Ken Thompson]]"
  type: related_to
  confidence: 0.8
  note: 曾参与 Multics 项目
- target: "[[操作系统]]"
  type: implements
  confidence: 0.85
  note: 早期分时操作系统的代表
- target: "[[UNIX]]"
  type: related_to
  confidence: 0.7
  note: 《人月神话》中的"第二系统效应"部分源于 Multics 教训
supersedes: null
---

# Multics

## 概述

Multics（Multiplexed Information and Computing Service）是1960年代中期由 MIT、通用电气（GE）与贝尔实验室（Bell Labs）三方联合开发的分时操作系统项目，预见了虚拟内存、动态链接、安全访问控制等现代操作系统的核心特性，但因工程复杂度失控而成为"复杂性代价"的经典教训。

## 关键内容

### 项目背景

- 1960年代中期启动，目标是构建功能完备的分时操作系统
- 支持多用户同时在线、层次化文件系统、动态链接、内存分段与分页、安全访问控制
- 这些设计在今天都是标配，但在当时意味着前所未有的工程复杂度

### 失败原因

- 项目越做越庞大，交付一再延期，预算持续膨胀
- Bell Labs 在1969年退出项目
- Fred Brooks 后来在《人月神话》中总结的"没有银弹"和"第二系统效应"等洞见，某种程度上就是这一时代教训的理论提炼

### 遗产

- Multics 最终完成了并投入使用
- 它的失败直接启发了 UNIX 的诞生——Thompson 和 Ritchie 从 Multics 的废墟中汲取了灵感
- UNIX（UNICS）这个名字本身就是对 Multics 的戏谑——"非多路复用的"

### 与 UNIX 的对比

| 特性 | Multics | UNIX |
|------|---------|------|
| 设计哲学 | 功能尽可能多 | 做一件事，做好它 |
| 复杂度 | 极高 | 极低 |
| 开发团队 | 大型团队 | 两个人 |
| 结果 | 交付延期、预算膨胀 | 改变世界 |

## 来源

- [[raw/books/计算机科学/09-ritchie-thompson-unix.md]]

## 相关

- [[UNIX]] — 对 Multics 的反叛
- [[Dennis Ritchie]] — 曾参与者
- [[Ken Thompson]] — 曾参与者
- [[操作系统]] — 早期分时系统
- Fred Brooks — 《人月神话》教训的来源
