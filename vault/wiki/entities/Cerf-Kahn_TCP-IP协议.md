---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [计算机网络, 协议, 互联网, 计算理论]
aliases: ["A Protocol for Packet Network Intercommunication", "Cerf-Kahn Protocol", "TCP/IP协议"]
relates_to:
  - target: "[[Vinton Cerf]]"
    type: authored
    confidence: 0.9
  - target: "[[Robert Kahn]]"
    type: authored
    confidence: 0.9
  - target: "[[TCP/IP]]"
    type: extends
    confidence: 0.9
  - target: "[[ARPANET]]"
    type: developed_for
    confidence: 0.8
  - target: "[[网关]]"
    type: introduces
    confidence: 0.9
  - target: "[[端到端原则]]"
    type: introduces
    confidence: 0.9
supersedes: null
entity_type: paper
---

# Cerf-Kahn TCP-IP协议

## 概述
Cerf和Kahn于1974年发表的开创性论文《A Protocol for Packet Network Intercommunication》，提出了[[互联网]]的核心协议架构，定义了[[网关]]概念和[[端到端原则]]，奠定了[[互联网]]技术基础。

## 关键内容

1. **论文核心贡献**：
   - 提出传输控制协议(TCP)的原始设计，通过引入无状态[[网关]]进行异构网络间的数据包转发
   - 将端到端可靠传输的责任从网络转移到主机，首次在技术上实现了"网络的网络"(internetwork)的概念
   - 这一设计后来演化为[[TCP-IP|TCP/IP]]协议族，成为全球[[互联网]]的基石

2. **关键技术概念**：
   - [[网关]]([[网关与路由器|Gateway]])概念：连接不同网络的设备，负责数据包格式转换和路由决策
   - [[端到端原则]]([[端到端原则|End-to-End Principle]])：通信的可靠性由端系统负责保证，中间网络只需尽最大努力递送数据包
   - 分层地址方案：网络号+主机号的结构，为全球[[互联网]]的统一寻址奠定基础

3. **历史意义**：
   - 1983年[[ARPANET]]正式切换到[[TCP-IP|TCP/IP]]协议，标志着现代[[互联网]]的诞生
   - 被广泛认为是"[[互联网]]的出生证明"，作者因此被誉为"[[互联网]]之父"
   - 协议架构保持了长达50年的持久生命力，支撑全球数十亿设备互联

## 来源
- [[10-cerf-kahn-tcp-ip]] — 论文全文分析

## 相关
- [[Vinton Cerf]] — authored
- [[Robert Kahn]] — authored
- [[TCP/IP]] — extends
- [[ARPANET]] — developed_for
- [[网关]] — introduces
- [[端到端原则]] — introduces