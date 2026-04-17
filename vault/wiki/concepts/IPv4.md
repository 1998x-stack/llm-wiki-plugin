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
- Internet Protocol version 4
- IPv4
- 互联网协议第4版
relates_to:
- target: "[[TCP-IP]]"
  type: part_of
  confidence: 0.99
  note: TCP/IP 协议族的网际层标准
- target: "[[TCP-IP 论文]]"
  type: extends
  confidence: 0.9
  note: 论文中的地址方案演化为 IPv4
- target: "[[Vinton Cerf]]"
  type: caused_by
  confidence: 0.85
  note: 论文作者
- target: "[[Robert Kahn]]"
  type: caused_by
  confidence: 0.85
  note: 论文作者
- target: "[[网关与路由器]]"
  type: implements
  confidence: 0.9
  note: 路由器基于 IPv4 地址进行路由决策
- target: "[[端到端原则]]"
  type: implements
  confidence: 0.8
  note: IPv4 地址实现端到端寻址
supersedes: null
---

# IPv4

## 概述

IPv4（Internet Protocol version 4）是互联网协议的第4版，使用32位地址（约43亿个唯一地址），1981年通过 RFC 791 标准化，至今仍是互联网的主要协议。

## 关键内容

### 地址结构

- **32位地址**：分为网络号和主机号两部分
- **分层设计**：[[网关与路由器|网关]]只需根据网络号路由，减少路由表规模
- **约43亿个地址**：1974年似乎绰绰有余，但2011年已耗尽

### 历史

- 源于 Cerf-Kahn 1974年论文中的分层地址方案
- 1978年 TCP 和 IP 分离时正式确立
- 1981年 RFC 791 标准化

### 地址耗尽

- 2011年全球 IPv4 地址耗尽
- 应对策略：NAT（网络地址转换）和 IPv6
- NAT 破坏了[[端到端原则]]——内部设备无法被外部主动访问

### 与 IPv6 的关系

- IPv6 使用128位地址（约 $3.4 \times 10^{38}$ 个地址）
- 1998年标准化，2024年全球部署率约45%
- 基础协议变更极端困难

## 来源

- [[raw/books/计算机科学/10-cerf-kahn-tcp-ip.md]]

## 相关

- [[TCP-IP]] — 协议族的网际层
- [[TCP-IP 论文]] — 地址方案的来源
- [[Vinton Cerf]] — 论文作者
- [[Robert Kahn]] — 论文作者
- [[网关与路由器]] — 基于 IPv4 路由
- [[端到端原则]] — IPv4 实现端到端寻址
