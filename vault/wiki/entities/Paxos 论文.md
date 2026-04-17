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
- The Part-Time Parliament
- Paxos 论文
- Lamport 1998 论文
relates_to:
- target: "[[Leslie Lamport]]"
  type: caused_by
  confidence: 0.99
  note: 作者
- target: "[[Paxos 算法]]"
  type: caused
  confidence: 0.99
  note: 首次提出 Paxos 算法
- target: "[[分布式系统]]"
  type: caused
  confidence: 0.95
  note: 奠定了分布式共识的理论基础
- target: "[[逻辑时钟]]"
  type: related_to
  confidence: 0.8
  note: Lamport 早期工作
- target: "[[拜占庭将军问题]]"
  type: related_to
  confidence: 0.85
  note: Lamport 对更强故障模型的研究
- target: "[[FLP 不可能性定理]]"
  type: depends_on
  confidence: 0.9
  note: Paxos 绕过了 FLP 不可能性
supersedes: null
---

# Paxos 论文

## 概述

[[Leslie Lamport]] 于1998年发表的《The Part-Time Parliament》（初稿完成于1989年），首次提出了 [[Paxos 算法]]——分布式共识问题的第一个实用解决方案。

## 关键内容

### 论文信息

| 条目 | 内容 |
|------|------|
| **标题** | The Part-Time Parliament |
| **作者** | [[Leslie Lamport]] |
| **初稿完成** | 1989年 |
| **正式发表** | 1998年5月，ACM TOCS, Vol. 16, No. 2, pp. 133-169 |
| **发表历程** | 辗转九年，因寓言体裁被多次拒绝 |

### 核心贡献

- **[[Paxos 算法]]**：在异步网络中，即使部分节点崩溃、消息丢失或任意延迟，多个节点仍能安全地就一个值达成共识
- **两阶段协议**：准备（Prepare）和接受（Accept）
- **多数派机制**：任意两个多数派必有交集，这是安全性论证的数学基础
- **安全性无条件保证，活性有条件保证**：绕过 [[FLP 不可能性定理]]

### 历史影响

- [[Google]] Chubby、Spanner、Megastore 基于 [[Paxos 算法|Paxos]]
- ZooKeeper（ZAB）、etcd（Raft）、CockroachDB、TiKV 都是 [[Paxos 算法|Paxos]] 的后裔
- 2001年 Lamport 发表 "[[Paxos 算法|Paxos]] Made Simple" 简化阐述

## 来源

- [[raw/books/计算机科学/18-lamport-paxos.md]]

## 相关

- [[Leslie Lamport]] — 作者
- [[Paxos 算法]] — 首次提出
- [[分布式系统]] — 奠定的领域
- [[逻辑时钟]] — Lamport 早期工作
- [[拜占庭将军问题]] — 更强故障模型
- [[FLP 不可能性定理]] — Paxos 绕过的理论边界
