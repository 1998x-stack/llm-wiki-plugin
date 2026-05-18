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
- A Protocol for Packet Network Intercommunication
- Cerf-Kahn 1974 论文
- TCP-IP 原始论文
relates_to:
- target: "[[Vinton Cerf]]"
  type: caused_by
  confidence: 0.99
  note: 第一作者
- target: "[[Robert Kahn]]"
  type: caused_by
  confidence: 0.99
  note: 第二作者
- target: "[[TCP-IP]]"
  type: caused
  confidence: 0.99
  note: 论文提出了 TCP/IP 的原始设计
- target: "[[端到端原则]]"
  type: caused
  confidence: 0.95
  note: 论文的核心设计哲学
- target: "[[网关与路由器]]"
  type: caused
  confidence: 0.95
  note: 论文中首次提出网关概念
- target: "[[ARPANET]]"
  type: related_to
  confidence: 0.9
  note: 论文旨在解决 ARPANET 的互联问题
- target: "[[分组交换]]"
  type: depends_on
  confidence: 0.9
  note: 基于分组交换技术
- target: "[[IPv4]]"
  type: caused
  confidence: 0.85
  note: 论文中的地址方案演化为 IPv4
- target: "[[拥塞控制]]"
  type: related_to
  confidence: 0.7
  note: 论文中缺乏拥塞控制，后来补充
supersedes: null
---

# TCP-IP 论文

## 概述

[[Vinton Cerf]] 和 [[Robert Kahn]] 于1974年发表的《[[Cerf-Kahn_TCP-IP协议|A Protocol for Packet Network Intercommunication]]》，被广泛认为是"[[互联网]]的出生证明"，首次提出了 [[TCP-IP|TCP/IP]] 协议的核心设计。

## 关键内容

### 论文信息

| 字段 | 内容 |
|------|------|
| **标题** | [[Cerf-Kahn_TCP-IP协议|A Protocol for Packet Network Intercommunication]] |
| **作者** | [[Vinton_Cerf|Vinton G. Cerf]], [[Robert_Kahn|Robert E. Kahn]] |
| **发表时间** | 1974年5月 |
| **刊物** | IEEE Transactions on Communications, Vol. 22, No. 5, pp. 637-648 |

### 核心贡献

- **[[网关与路由器|网关]]（[[网关与路由器|Gateway]]）概念**：连接异构网络的专用设备，即今天的[[网关与路由器|路由器]]
- **[[端到端原则]]**：通信可靠性由端系统负责，中间网络只做尽力交付
- **TCP 协议机制**：序列号、确认与重传、滑动窗口流量控制、校验和
- **分层地址方案**：网络号 + 主机号

### 历史验证

- **1977年三网互联演示**：PRNET → [[ARPANET]] → SATNET → 伦敦，往返94,000英里
- **1983年旗帜日**：[[ARPANET]] 从 NCP 切换到 [[TCP-IP|TCP/IP]]
- **BSD UNIX 4.2**（1983）：内置 [[TCP-IP|TCP/IP]] 协议栈和 socket API

### 后续演化

- 1978年：TCP 和 IP 分离（IEN 44）
- 1981年：RFC 791（IPv4）和 RFC 793（TCP）成为最终标准
- 2004年：Cerf 和 Kahn 获得[[阿兰·图灵|图灵]]奖

## 来源

- [[raw/books/计算机科学/10-cerf-kahn-tcp-ip.md]]

## 相关

- [[Vinton Cerf]] — 第一作者
- [[Robert Kahn]] — 第二作者
- [[TCP-IP]] — 论文提出的协议
- [[端到端原则]] — 核心设计哲学
- [[网关与路由器]] — 论文首次提出
- [[ARPANET]] — 论文旨在解决的问题背景
- [[分组交换]] — 技术基础
- [[IPv4]] — 地址方案的演化
- [[拥塞控制]] — 论文中缺失，后来补充
