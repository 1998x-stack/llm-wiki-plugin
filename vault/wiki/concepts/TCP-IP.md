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
- 历史
- 计算理论
aliases:
- TCP/IP
- Transmission Control Protocol / Internet Protocol
- 传输控制协议/网际协议
relates_to:
- target: "[[Vinton Cerf]]"
  type: caused_by
  confidence: 0.99
  note: 共同发明者
- target: "[[Robert Kahn]]"
  type: caused_by
  confidence: 0.99
  note: 共同发明者
- target: "[[TCP-IP 论文]]"
  type: caused_by
  confidence: 0.99
  note: 首次提出
- target: "[[端到端原则]]"
  type: implements
  confidence: 0.99
  note: TCP/IP 的核心设计哲学
- target: "[[网关与路由器]]"
  type: depends_on
  confidence: 0.95
  note: 依赖网关进行网络互联
- target: "[[ARPANET]]"
  type: extends
  confidence: 0.9
  note: 取代了 ARPANET 的 NCP 协议
- target: "[[分组交换]]"
  type: depends_on
  confidence: 0.9
  note: 基于分组交换技术
- target: "[[IPv4]]"
  type: implements
  confidence: 0.95
  note: IP 层的标准版本
- target: "[[拥塞控制]]"
  type: implements
  confidence: 0.85
  note: 后来补充的重要机制
- target: "[[UNIX]]"
  type: implements
  confidence: 0.9
  note: BSD UNIX 4.2 内置了 TCP/IP 协议栈
- target: "[[操作系统]]"
  type: implements
  confidence: 0.85
  note: 成为操作系统的标准网络协议
- target: "[[Louis Pouzin]]"
  type: extends
  confidence: 0.8
  note: CYCLADES 数据报模型启发了设计
supersedes: null
---

# TCP-IP

## 概述

TCP/IP 是全球互联网的核心协议族，由 [[Vinton Cerf]] 和 [[Robert Kahn]] 于1974年提出，通过端到端可靠传输和无状态网络互联，使得异构网络能够无缝互联。

## 关键内容

### 协议分层

TCP/IP 最初是一个"巨型协议"，1978年被拆分为两层：

- **IP（Internet Protocol）**：网际层，负责寻址和路由。无连接、不可靠、尽力交付
- **TCP（Transmission Control Protocol）**：传输层，负责端到端的可靠、有序、面向连接的数据传输

### 核心机制

- **序列号**：基于字节的序列号，检测丢失、重复和乱序
- **确认与重传**：累积确认 + 自适应超时
- **滑动窗口**：流量控制，防止快速发送方淹没慢速接收方
- **校验和**：端到端的数据完整性保护
- **分段与重组**：大消息拆分为段，重组只在最终目的地进行

### 设计哲学

- **[[端到端原则]]**：智能在边缘，核心保持简单
- **哑[[网关与路由器|网关]]**：[[网关与路由器|网关]]无状态，只做逐包转发
- **对底层技术不可知**：可运行在任何能传递数据包的网络上

### 历史里程碑

- **1974年**：原始论文发表
- **1977年**：三网互联演示（PRNET → [[ARPANET]] → SATNET）
- **1978年**：TCP 和 IP 分离
- **1981年**：RFC 791（IPv4）和 RFC 793（TCP）
- **1983年**：[[ARPANET]] 从 NCP 切换到 TCP/IP（"旗帜日"）
- **2004年**：Cerf 和 Kahn 获得[[阿兰·图灵|图灵]]奖

### 全球影响

截至2024年，全球55亿互联网用户全部运行在 TCP/IP 之上。从超级[[计算]]机到智能手表，从海底光缆到低轨卫星，TCP/IP 是唯一通用的通信协议。

## 来源

- [[raw/books/计算机科学/10-cerf-kahn-tcp-ip.md]]

## 相关

- [[Vinton Cerf]] — 共同发明者
- [[Robert Kahn]] — 共同发明者
- [[TCP-IP 论文]] — 首次提出
- [[端到端原则]] — 核心设计哲学
- [[网关与路由器]] — 关键组件
- [[ARPANET]] — 取代了 NCP
- [[分组交换]] — 技术基础
- [[IPv4]] — IP 层标准
- [[拥塞控制]] — 后来补充
- [[UNIX]] — BSD 内置 TCP/IP
- [[操作系统]] — 标准网络协议
- [[Louis Pouzin]] — CYCLADES 启发了设计
