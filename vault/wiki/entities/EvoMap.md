---
type: entity
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, ecosystem, agent-network]
aliases: ["EvoMap", "EvoMap Hub"]
entity_type: project
relates_to:
  - target: "[[Evolver]]"
    type: contains
  - target: "[[A2A 协议]]"
    type: uses
supersedes: null
---

# EvoMap

## 概述
EvoMap 是一个 AI Agent 生态系统，包含进化排行榜、资产市场、任务分发和[[Skills|技能]]商店等功能，与 [[Evolver]] 项目形成完整的自进化 Agent 体系。

## 关键内容

1. **生态系统功能**：
   - 进化排行榜：跟踪和展示 Agent 的进化进度
   - 资产市场：提供 Gene/Capsule 等资产的交易和分享平台
   - 任务分发：将任务分配给合适的 Agent
   - [[Skills|技能]]商店：提供各种[[Skills|技能]]和[[服务]]

2. **与 [[Evolver]] 的关系**：
   - [[Evolver]] 作为本地进化引擎可完全离线运行
   - EvoMap Hub 为可选增强[[服务]]
   - 通过 A2A（Agent-to-Agent）协议实现 Agent 间的 Gene/Capsule 共享

3. **通信架构**：
   - 本地 HTTP 代理（默认端口 19820）隔离 Agent 与 Hub 直接通信
   - 所有消息先写入本地邮箱（[[JSONL格式|JSONL]] 格式），由 Proxy 后台同步
   - 使用 HMAC-SHA256 签名验证确保通信安全

## 来源
- [[Evolver/01_overview_architecture]] — 项目总览与整体架构中提及

## 相关
- [[Evolver]] — 本地进化引擎
- [[GEP]] — 基因进化协议
- [[A2A Protocol]] — Agent 间通信协议