---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [分布式系统, 理论基础, 不可能性定理]
aliases: ["FLP不可能性定理", "Fischer-Lynch-Paterson定理", "FLP Impossibility", "Consensus Impossibility"]
relates_to:
  - target: "[[分布式共识]]"
    type: addresses
    confidence: 0.9
  - target: "[[Paxos算法]]"
    type: addressed_by
    confidence: 0.9
  - target: "[[Michael J. Fischer]]"
    type: authored
    confidence: 0.8
  - target: "[[Nancy Lynch]]"
    type: authored
    confidence: 0.8
  - target: "[[Michael S. Paterson]]"
    type: authored
    confidence: 0.8
  - target: "[[异步模型]]
    type: applies_to
    confidence: 0.9
supersedes: null
---

# FLP不可能性定理

## 概述
FLP不可能性定理是分布式系统理论中的一个重要结论，由Michael J. Fischer、Nancy A. Lynch和Michael S. Paterson于1985年提出，证明了在完全异步的系统中，即使只有一个进程可能发生崩溃故障，也不存在任何确定性算法能够保证共识一定能达成。

## 关键内容

1. **定理内容**：
   - 在异步分布式系统中，即使只有一个进程可能发生崩溃故障，也没有任何确定性算法能保证在有限时间内解决共识问题
   - 这个结果适用于完全异步的模型，其中没有时间上限或同步假设

2. **核心观点**：
   - 异步模型中无法区分进程崩溃和极长延迟
   - 在某些执行路径中，算法可能会永远无法终止
   - 算法必须在所有可能的执行路径中都能终止，FLP定理才适用

3. **对领域的影响**：
   - 这个定理曾经被认为是分布式系统领域的悲观结果
   - 导致研究者们转向同步模型或概率算法
   - 促使了如Paxos等算法的诞生，这些算法通过保证安全性、有条件保证活性来绕过不可能性

4. **Paxos的突破**：
   - Paxos算法通过"安全性永远保证，活性在合理条件下保证"的策略绕过了FLP定理的限制
   - 该算法不追求在所有情况下都终止，而是保证永不产生错误结果
   - 为分布式共识问题提供了实用的解决方案

5. **现实意义**：
   - 为分布式系统设计提供了理论边界
   - 指导工程师理解分布式系统的固有复杂性
   - 成为评估共识算法的重要理论基础

## 来源
- [[18-lamport-paxos]] — 详细分析了FLP定理及其与Paxos的关系
- [[Michael J. Fischer]] — 定理作者之一

## 相关
- [[Paxos算法]] — addresses_with
- [[分布式共识]] — relates_to
- [[Michael J. Fischer]] — authored
- [[Nancy Lynch]] — authored
- [[Michael S. Paterson]] — authored
- [[异步模型]] — applies_to