---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [分布式系统, 共识算法, 理论基础]
aliases: ["Paxos", "The Part-Time Parliament", "Paxos Consensus Algorithm"]
relates_to:
  - target: "[[Leslie Lamport]]"
    type: authored
    confidence: 0.9
  - target: "[[分布式共识]]"
    type: solves
    confidence: 0.9
  - target: "[[Raft算法]]"
    type: predecessor
    confidence: 0.8
  - target: "[[FLP不可能性定理]]"
    type: addresses
    confidence: 0.9
  - target: "[[拜占庭将军问题]]"
    type: related
    confidence: 0.8
  - target: "[[Multi-Paxos]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Paxos算法

## 概述
Paxos算法是由Leslie Lamport提出的一种分布式共识算法，是第一个在异步网络中实用的共识解决方案，用于在部分节点可能发生故障的分布式系统中就单一值达成一致。

## 关键内容

1. **核心思想**：
   - Paxos解决了分布式系统中的共识问题，即多个地理分散、通信不可靠、可能随时故障的节点如何就某个值达成一致决定
   - 算法基于"多数派交集"的数学性质：任意两个多数派必然存在交集，确保了不同阶段间的信息连续性

2. **算法结构**：
   - **角色划分**：提议者(Proposer)、接受者(Acceptor)、学习者(Learner)
   - **两阶段协议**：准备阶段(Prepare)和接受阶段(Accept)
   - **提案编号**：每个提案由唯一编号和值组成，编号用于解决冲突

3. **安全性和活性**：
   - **安全性**：无条件保证，包括合法性(被选定的值必须是某个进程实际提出的)和一致性(所有进程学习到的值相同)
   - **活性**：在足够多进程运行且网络最终连通的条件下保证系统终止

4. **关键创新**：
   - 提出了多数派思想，不需要所有节点同意，只需多数节点同意
   - 通过提案编号+承诺机制实现无锁冲突解决
   - 连接了理论和工程实践，在尊重FLP定理边界的同时提供了实用算法

5. **实际应用**：
   - 成为众多分布式系统的基础，如Google的Chubby、Megastore、Spanner
   - 影响了后续算法如ZooKeeper的ZAB、etcd的Raft等
   - 是现代云原生基础设施的重要理论支柱

## 来源
- [[18-lamport-paxos]] — 原始论文分析文档
- [[Leslie Lamport]] — 原作者及其贡献
- [[分布式共识]] — 领域背景

## 相关
- [[Leslie Lamport]] — authored
- [[Raft算法]] — predecessor
- [[分布式共识]] — relates_to
- [[FLP不可能性定理]] — addresses
- [[Multi-Paxos]] — extends
- [[状态机复制]] — relates_to