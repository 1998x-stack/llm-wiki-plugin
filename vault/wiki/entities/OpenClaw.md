---
type: entity
title: "OpenClaw"
status: active
confidence: 0.85
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [工具, AI, Agent, Agent系统]
aliases:
  - OpenClaw AI
relates_to:
  - target: "[[Pi-Agent]]"
    type: uses
    confidence: 0.95
  - target: "[[Mario-Zechner]]"
    type: caused
    confidence: 0.9
  - target: "[[agentskills.io]]"
    type: implements
    confidence: 0.7
  - target: "[[Hermes Agent]]"
    type: compares_to
    confidence: 0.7
  - target: "[[开放技能标准]]"
    type: implements
    confidence: 0.7
supersedes: null
---

# OpenClaw

## 概述

OpenClaw 是一个多渠道 AI 助手，以 [[Pi-Agent]] 为核心引擎，支持 WhatsApp、Telegram、Discord、[[Slack]]、Signal、iMessage 等平台，各渠道共享内存和持久化会话。一周内获得 14.5 万 [[GitHub]] Stars，使 Pi Agent 从私人工具走向公众视野。

## 关键内容

### 1. 多渠道架构

OpenClaw 将 Pi Agent 内嵌为核心 Agent 引擎，在其上构建了多平台通道适配层，支持的渠道包括：
- WhatsApp、Telegram、Discord、[[Slack]]、Signal
- iMessage、[[Google]] Chat、Microsoft Teams

关键特性：各渠道**共享内存和持久化会话**——在任一平台发起的对话可在另一平台无缝继续。这依赖于 Pi 的 [[JSONL格式|JSONL]] 会话格式和跨 Provider 迁移能力。

### 2. 对 Pi Agent 的意义

Pi 原本是 [[Mario-Zechner]] 的私人工具，"永远不会有用户"。OpenClaw 作为 Pi 的第一个大规模用户验证了其架构的可扩展性——从个人 CLI 工具到[[服务]]百万用户的多渠道平台，核心引擎无需重写。

### 3. 与 agentskills.io 开放标准的关系

OpenClaw 的[[Skills|技能]]格式兼容 [[agentskills.io]] 开放规范，支持通过 `hermes claw migrate` 工具从 OpenClaw 迁移到 [[Hermes Agent]]。迁移命令支持 `--dry-run` 预览、`--preset user-data` 只迁移用户数据、`--overwrite` 覆盖冲突文件。这体现了[[开放技能标准]]的核心价值：[[Skills|技能]]可在不同 Agent 框架间流通，而非某个系统的私有数据。

### 4. 与 Hermes Gateway 的架构差异

OpenClaw 把 [[网关与路由器|Gateway]] 作为**控制平面**：一个拥有会话、路由、工具执行和状态的单一长期进程，所有东西都流过它。[[Hermes Agent|Hermes]] 的 [[网关与路由器|Gateway]] 更轻：它是消息路由层，核心逻辑在 AIAgent 循环里，[[网关与路由器|Gateway]] 只负责"把消息送进去、把结果送出来"。这反映了两种设计哲学：OpenClaw 偏向集中式控制，[[Hermes Agent|Hermes]] 偏向轻量解耦。

## 来源

- [[raw/articles/ai-tools/pi-agent/01-overview-philosophy.md]]
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本，Hermes Agent 深度解析第四篇
- [05_hermes_gateway.md](/raw/articles/ai-tools/hermes/05_hermes_gateway.md) — Hermes Agent 深度解析第五篇：Gateway 消息网关，2026 年 4 月版本

## 相关

- [[Pi-Agent]] — 核心引擎
- [[Mario-Zechner]] — 创造者
- [[agentskills.io]] — implements
- [[Hermes Agent]] — compares_to
- [[开放技能标准]] — implements
