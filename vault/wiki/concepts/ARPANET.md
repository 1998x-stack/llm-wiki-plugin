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
- 历史
- 计算理论
aliases:
- Advanced Research Projects Agency Network
- 阿帕网
relates_to:
- target: "[[TCP-IP]]"
  type: supersedes
  confidence: 0.95
  note: TCP/IP 取代了 ARPANET 的 NCP 协议
- target: "[[TCP-IP 论文]]"
  type: related_to
  confidence: 0.9
  note: 论文旨在解决 ARPANET 的互联问题
- target: "[[Vinton Cerf]]"
  type: related_to
  confidence: 0.85
  note: NCP 协议的核心设计者
- target: "[[Robert Kahn]]"
  type: related_to
  confidence: 0.85
  note: 在 DARPA 负责 ARPANET 研究
- target: "[[分组交换]]"
  type: implements
  confidence: 0.9
  note: 首个成功的分组交换网络
- target: "[[网关与路由器]]"
  type: implements
  confidence: 0.85
  note: 通过网关与其他网络互联
- target: "[[UNIX]]"
  type: related_to
  confidence: 0.8
  note: BSD UNIX 的 TCP/IP 最初为 ARPANET 设计
- target: "[[操作系统]]"
  type: related_to
  confidence: 0.7
  note: 推动了操作系统网络协议的发展
supersedes: null
---

# ARPANET

## 概述

ARPANET（Advanced Research Projects [[能动性|Agency]] Network）是美国国防部高级研究计划局资助建设的[[分组交换]]网络，1969年投入运行，是互联网的前身。

## 关键内容

### 历史

- **1969年**：投入运行，最初连接4个节点
- **1973年**：已连接约40个节点，覆盖美国各地
- **1983年1月1日**：从 NCP 协议切换到 [[TCP-IP|TCP/IP]]（"旗帜日"）

### NCP 协议

- Network Control Program，ARPANET 的主机间通信协议
- 依赖 ARPANET 的 IMP（接口消息处理机）提供可靠传输
- 核心局限：假设底层网络可靠，无法处理异构网络互联

### 三网互联演示（1977年）

历史性的演示：数据包从旧金山湾区出发，通过 PRNET（分组无线电网络）→ ARPANET → SATNET（大西洋卫星网络）→ 伦敦大学学院，往返94,000英里，经过三种完全不同的链路技术。

### 遗产

- 证明了[[分组交换]]作为数据通信[[规范化理论|范式]]的可行性
- 为 [[TCP-IP|TCP/IP]] 的诞生提供了直接的问题背景
- 1990年正式退役

## 来源

- [[raw/books/计算机科学/10-cerf-kahn-tcp-ip.md]]

## 相关

- [[TCP-IP]] — 取代了 ARPANET 的 NCP
- [[TCP-IP 论文]] — 旨在解决 ARPANET 的互联问题
- [[Vinton Cerf]] — NCP 核心设计者
- [[Robert Kahn]] — DARPA 项目负责人
- [[分组交换]] — 首个成功的分组交换网络
- [[网关与路由器]] — 通过网关与其他网络互联
- [[UNIX]] — BSD 的 TCP/IP 最初为 ARPANET 设计
- [[操作系统]] — 推动了网络协议的发展
