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
- 计算理论
aliases:
- Paxos
- Paxos 算法
relates_to:
- target: "[[Paxos 论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文中首次提出
- target: "[[Leslie Lamport]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[分布式系统]]"
  type: implements
  confidence: 0.99
  note: 分布式共识的核心算法
- target: "[[拜占庭将军问题]]"
  type: compares_to
  confidence: 0.8
  note: Paxos 处理崩溃故障，拜占庭处理恶意故障
- target: "[[FLP 不可能性定理]]"
  type: related_to
  confidence: 0.85
  note: Paxos 绕过了 FLP 不可能性
supersedes: null
---

# Paxos 算法

## 概述

Paxos 是分布式共识问题的第一个实用算法，由 [[Leslie Lamport]] 于1989年提出，1998年正式发表。它在异步网络中保证安全性，在合理条件下保证活性。

## 关键内容

### 三种角色

| 角色 | 职责 | 类比 |
|------|------|------|
| **提议者（Proposer）** | 提出值，发起共识流程 | 提出法令的议员 |
| **接受者（Acceptor）** | 对提议投票，通过多数派决定是否选定 | 投票的议员 |
| **学习者（Learner）** | 获知最终被选定的值 | 记录法令的书记员 |

### 两阶段协议

**阶段一：准备（Prepare）**
- Proposer 选择新编号 n，向 Acceptor 发送 Prepare(n)
- Acceptor 若 n > n_max，承诺不再接受编号 < n 的提案，返回 Promise

**阶段二：接受（Accept）**
- Proposer 收到多数派 Promise 后，确定值 v，发送 Accept(n, v)
- Acceptor 若未对更高编号作出承诺，则接受并返回 Accepted

### 安全性保证

核心不变式 P2c：如果值 v 被选定，任何编号更大的提案的值也必须是 v。这利用了**多数派交集**的数学性质。

### 工业应用

- **[[Google]]**：Chubby、Spanner、Megastore
- **Apache**：ZooKeeper（ZAB 变体）
- **CNCF**：etcd（Raft 变体）
- **数据库**：CockroachDB、TiKV

## 来源

- [[raw/books/计算机科学/18-lamport-paxos.md]]

## 相关

- [[Paxos 论文]] — 首次提出
- [[Leslie Lamport]] — 发明者
- [[分布式系统]] — 应用领域
- [[拜占庭将军问题]] — 更强故障模型
- [[FLP 不可能性定理]] — 理论边界
