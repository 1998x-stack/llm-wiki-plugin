---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, protocol, communication, AI工程]
aliases: ["A2A", "Agent-to-Agent Protocol", "Agent-to-Agent Communication Protocol"]
relates_to:
  - target: "[[Evolver]]"
    type: used_by
  - target: "[[EvoMap]]"
    type: used_by
  - target: "[[自我进化型 AI Agent 协议]]"
    type: component_of
supersedes: null
---

# A2A 协议

## 概述
A2A 协议（Agent-to-Agent Protocol）是用于 AI Agent 之间相互通信和共享资源的协议，允许 Agent 间广播 Gene/Capsule 等进化资产。

## 关键内容

1. **协议功能**：
   - 实现 Agent 间的直接通信
   - 支持 Gene/Capsule 等进化资产的广播和共享
   - 提供安全的身份验证和数据完整性保护

2. **安全机制**：
   - 使用 HMAC-SHA256 签名验证确保消息真实性
   - 通过本地代理（默认端口 19820）隔离 Agent 与中心 Hub 的直接通信
   - 所有消息首先写入本地邮箱（[[JSONL格式|JSONL]] 格式），再由代理后台同步

3. **在网络中的角色**：
   - 构成 Agent 间的共享网络，允许跨 Agent 的经验传递
   - 是 [[EvoMap]] 生态系统的重要组成部分
   - 使多个使用 [[Evolver]] 引擎的 Agent 能够相互学习和进化

## 来源
- [[Evolver/01_overview_architecture]] — 项目总览与整体架构中提及

## 相关
- [[Evolver]] — 使用 A2A 协议的进化引擎
- [[EvoMap]] — 包含 A2A 协议的生态系统
- [[Gene Evolution Protocol]] — 相关的进化协议