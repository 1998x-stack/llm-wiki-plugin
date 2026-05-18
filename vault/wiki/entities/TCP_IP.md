---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [计算机网络, 协议, 互联网, 计算理论]
aliases: ["Transmission Control Protocol", "Internet Protocol", "传输控制协议-网际协议"]
relates_to:
  - target: "[[Cerf-Kahn TCP-IP协议]]"
    type: implements
    confidence: 0.9
  - target: "[[Vinton Cerf]]"
    type: invented_by
    confidence: 0.9
  - target: "[[Robert Kahn]]"
    type: invented_by
    confidence: 0.9
  - target: "[[网关]]"
    type: requires
    confidence: 0.9
  - target: "[[端到端原则]]"
    type: follows
    confidence: 0.9
  - target: "[[互联网]]"
    type: enables
    confidence: 0.9
  - target: "[[IP地址]]"
    type: includes
    confidence: 0.8
supersedes: null
entity_type: tool
---

# TCP/IP

## 概述
[[TCP-IP|传输控制协议/网际协议]](Transmission Control Protocol/[[互联网|Internet]] Protocol)，[[互联网]]的核心协议族，由传输层TCP和网际层IP构成，定义了数据如何在网络中传输和路由。

## 关键内容

1. **协议组成**：
   - IP协议([[互联网|Internet]] Protocol)：负责寻址和路由，是无连接、不可靠的协议，只做尽力交付
   - TCP协议(Transmission Control Protocol)：负责端到端的可靠、有序、面向连接的数据传输
   - 后续发展出UDP(User Datagram Protocol)等传输层协议，提供更多选择

2. **核心机制**：
   - 分段与重组：将大数据拆分为适合网络传输的数据包，在接收端重新组装
   - 序列号机制：为数据包分配序列号，用于检测丢失、重复和乱序
   - 确认与重传：接收方发送确认，发送方超时重传丢失的数据包
   - 滑动窗口：实现流量控制，防止快速发送方淹没慢速接收方

3. **发展历程**：
   - 1974年由Cerf和Kahn在论文中首次提出
   - 1978年[[TCP-IP|TCP/IP]]分离，协议架构更加清晰
   - 1983年[[ARPANET]]正式切换到[[TCP-IP|TCP/IP]]，标志现代[[互联网]]诞生
   - 成为全球[[互联网]]的基石协议

## 来源
- [[Cerf-Kahn TCP-IP协议]] — 原始设计
- [[互联网]] — 实施应用

## 相关
- [[Cerf-Kahn TCP-IP协议]] — implements
- [[Vinton Cerf]] — invented_by
- [[Robert Kahn]] — invented_by
- [[网关]] — requires
- [[端到端原则]] — follows
- [[互联网]] — enables
- [[IP地址]] — includes