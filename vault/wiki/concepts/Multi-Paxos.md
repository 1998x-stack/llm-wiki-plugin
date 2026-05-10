---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [分布式系统, 理论基础, 共识算法]
aliases: ["Multi-Paxos", "Multi-Paxos Algorithm"]
relates_to:
  - target: "[[Paxos算法]]"
    type: extends
    confidence: 0.9
  - target: "[[状态机复制]]"
    type: implements
    confidence: 0.8
  - target: "[[日志复制]]
    type: basis_for
    confidence: 0.8
  - target: "[[Raft算法]]"
    type: predecessor
    confidence: 0.8
supersedes: null
---

# Multi-Paxos

## 概述
Multi-Paxos是Paxos算法的扩展形式，用于实现一个有序的操作日志（replicated log），使所有节点能够执行相同顺序的操作以维护一致的状态。它通过为日志的每个位置运行一个独立的Paxos实例来实现多值共识。

## 关键内容

1. **基本概念**：
   - 基本Paxos（Basic Paxos）解决的是就一个值达成共识的问题
   - Multi-Paxos通过为日志的每个位置（slot）运行一个独立的Paxos实例来实现有序操作日志
   - 日志的第i个位置对应第i个Paxos实例，决定第i个操作是什么

2. **关键优化**：
   - **Leader优化**：如果存在稳定Leader，它可以跳过阶段一（Prepare），直接执行阶段二（Accept）
   - **管道化（Pipelining）**：Leader可同时发起多个slot的共识过程
   - **日志压缩（Log Compaction）**：通过快照机制定期清理已执行的旧日志条目

3. **与基本Paxos的区别**：
   - 基本Paxos只解决单值共识，Multi-Paxos解决多值共识
   - Multi-Paxos引入了日志和状态机复制的概念
   - 在实际系统中，Multi-Paxos是真正使用的协议形态

4. **实现复杂性**：
   - 原始论文对Multi-Paxos的描述较粗略
   - Leader选举、日志中空洞处理、配置变更等关键问题没有详述
   - 这导致不同的实现之间存在细微但重要的差异

5. **实际应用**：
   - 作为许多分布式系统共识层的基础
   - 是后来Raft等算法的直接对标对象
   - 现代分布式系统中真正使用的Paxos形态

## 来源
- [[18-lamport-paxos]] — 详细分析了Multi-Paxos的原理和发展
- [[Paxos算法]] — 基础算法

## 相关
- [[Paxos算法]] — extends
- [[Raft算法]] — relates_to
- [[状态机复制]] — implements
- [[日志复制]] — relates_to
- [[分布式共识]] — relates_to