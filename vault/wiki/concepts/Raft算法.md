---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [分布式系统, 理论基础, 一致性模型, 计算理论]
aliases: ["Raft算法", "Raft Consensus Algorithm"]
relates_to:
  - target: "[[Paxos算法]]"
    type: successor
    confidence: 0.9
  - target: "[[分布式共识]]"
    type: solves
    confidence: 0.9
  - target: "[[状态机复制]]"
    type: implements
    confidence: 0.9
  - target: "[[Diego Ongaro]]"
    type: authored
    confidence: 0.9
  - target: "[[John Ousterhout]]"
    type: authored
    confidence: 0.9
  - target: "[[Multi-Paxos]]"
    type: successor
    confidence: 0.8
supersedes: null
---

# Raft算法

## 概述
Raft[[算法]]是2014年由Diego Ongaro和John Ousterhout提出的[[分布式共识]][[算法]]，明确以"可理解性"为首要设计目标，是[[Paxos算法]]的替代方案。Raft在理论能力上与[[Multi-Paxos]]等价，但通过更好的分解和简化大幅降低了理解和实现的难度。

## 关键内容

1. **设计理念**：
   - 以可理解性为首要目标
   - 将共识问题分解为更简单的子问题
   - 提供清晰的协议描述和实现指导

2. **核心特性**：
   - **强Leader**：所有写请求必须经过Leader，简化了推理
   - **日志连续性**：不允许日志中出现空洞，简化了恢复逻辑
   - **明确的Leader选举**：使用随机超时机制，规则清晰
   - **成员变更的联合共识**：提供了详细的[[Configuration|配置]]变更方案

3. **与[[Paxos 算法|Paxos]]的对比**：
   - 在理论能力上与[[Multi-Paxos]]等价
   - 通过更好的表述方式降低了工程实现的复杂性
   - 成为现代[[分布式系统]]中更常用的共识[[算法]]

4. **组成部分**：
   - Leader选举：当现有Leader失效时选举新Leader
   - 日志复制：将日志条目从Leader复制到所有节点
   - 安全性：保证状态机安全的属性

5. **实际应用**：
   - 被广泛应用于现代[[分布式系统]]
   - etcd使用Raft[[算法]]，支撑Kubernetes集群
   - 成为云原生基础设施的重要组成部分

## 来源
- [[18-lamport-paxos]] — 详细比较了Raft与Paxos的关系
- [[Paxos算法]] — 相关算法

## 相关
- [[Paxos算法]] — predecessor
- [[分布式共识]] — solves
- [[状态机复制]] — implements
- [[Diego Ongaro]] — authored
- [[John Ousterhout]] — authored
- [[Multi-Paxos]] — relates_to