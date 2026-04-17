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
- 数学
- 计算理论
aliases:
- FLP Impossibility Theorem
- FLP 不可能性
relates_to:
- target: "[[Paxos 算法]]"
  type: related_to
  confidence: 0.9
  note: Paxos 绕过了 FLP 不可能性
- target: "[[分布式系统]]"
  type: part_of
  confidence: 0.9
  note: 分布式系统理论的核心定理
- target: "[[Leslie Lamport]]"
  type: related_to
  confidence: 0.7
  note: Lamport 的工作绕过了 FLP 的约束
supersedes: null
---

# FLP 不可能性定理

## 概述

FLP 不可能性定理（1985年）严格证明了：在完全异步的[[分布式系统]]中，即使只有一个进程可能崩溃，也不存在任何确定性算法能够保证共识一定能达成。

## 关键内容

### 定理内容

[[恩斯特·菲舍尔|Fischer]]、Lynch 和 Paterson 于1985年证明：在异步模型中，任何确定性共识算法都存在至少一个执行路径，使得算法永远无法终止。

### Paxos 的绕过策略

[[Paxos 算法|Paxos]] 没有违反 FLP 定理，而是巧妙地绕过了它：
- **安全性无条件保证**：无论发生什么，永远不会产生错误结果
- **活性有条件保证**：在合理条件下（稳定的 Leader、网络连通），系统一定会终止

### 实际意义

- FLP 定理告诉我们：不可能在所有情况下都保证共识达成
- 但实践中，FLP 的"坏路径"极少发生
- [[Paxos 算法|Paxos]]、Raft 等算法在实践中几乎总是能终止

## 来源

- [[raw/books/计算机科学/18-lamport-paxos.md]]

## 相关

- [[Paxos 算法]] — 绕过了 FLP 不可能性
- [[分布式系统]] — 所属领域
- [[Leslie Lamport]] — 工作绕过 FLP 约束
