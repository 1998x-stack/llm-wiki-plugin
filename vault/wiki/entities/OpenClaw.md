---
type: entity
title: "OpenClaw"
status: active
confidence: 0.85
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
  - 工具
  - AI
  - Agent
aliases:
  - OpenClaw AI
relates_to:
  - target: "[[Pi-Agent]]"
    type: uses
    confidence: 0.95
  - target: "[[Mario-Zechner]]"
    type: caused
    confidence: 0.9
supersedes: null
---

# OpenClaw

## 概述

OpenClaw 是一个多渠道 AI 助手，以 [[Pi-Agent]] 为核心引擎，支持 WhatsApp、Telegram、Discord、Slack、Signal、iMessage 等平台，各渠道共享内存和持久化会话。一周内获得 14.5 万 GitHub Stars，使 [[Pi-Agent|Pi]] Agent 从私人工具走向公众视野。

## 关键内容

### 1. 多渠道架构

OpenClaw 将 [[Pi-Agent|Pi]] Agent 内嵌为核心 Agent 引擎，在其上构建了多平台通道适配层，支持的渠道包括：
- WhatsApp、Telegram、Discord、Slack、Signal
- iMessage、[[Google]] Chat、Microsoft Teams

关键特性：各渠道**共享内存和持久化会话**——在任一平台发起的对话可在另一平台无缝继续。这依赖于 [[Pi-Agent|Pi]] 的 JSONL 会话格式和跨 Provider 迁移能力。

### 2. 对 Pi Agent 的意义

[[Pi-Agent|Pi]] 原本是 [[Mario-Zechner]] 的私人工具，"永远不会有用户"。OpenClaw 作为 [[Pi-Agent|Pi]] 的第一个大规模用户验证了其架构的可扩展性——从个人 CLI 工具到服务百万用户的多渠道平台，核心引擎无需重写。

## 来源

- [[raw/articles/ai-tools/pi-agent/01-overview-philosophy.md]]

## 相关

- [[Pi-Agent]] — 核心引擎
- [[Mario-Zechner]] — 创造者
