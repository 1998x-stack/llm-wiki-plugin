---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [connect-operation, external-services, integration, AI工程]
aliases: ["Connect", "Connect操作", "连接操作"]
relates_to: 
  - target: "[[Claude Code]]"
    type: relates_to
  - target: "[[Claude Code四大能力基元]]"
    type: part_of
  - target: "[[Model Context Protocol]]"
    type: relates_to
supersedes: null
---

# Connect

## 概述
Connect是[[Claude Code四大能力基元]]之一，代表连接外部[[服务]]的能力，通过[[MCP（Model Context Protocol）]]协议实现与外部系统的交互。

## 关键内容
1. **功能范围**：通过[[MCP（Model Context Protocol）|MCP协议]]连接到[[GitHub]]、数据库(DB)、监控系统(Sentry)、通讯工具([[Slack]])等各种外部[[服务]]。

2. **标准化接入**：使用[[Model Context Protocol]]作为标准化协议，统一外部[[服务]]的接入方式。

3. **[[服务]]集成**：使AI能够与版本控制系统、数据库、监控系统、协作平台等外部系统进行交互。

4. **扩展能力**：通过连接外部[[服务]]，显著扩展了AI编码代理的功能边界。

5. **在[[Claude Code]]中的角色**：作为四大基础能力之一，Connect使AI能够与开发流程中的各种工具和[[服务]]集成，实现更复杂的任务。

## 来源
- [[01_system_overview.md]] — 四大能力基元部分

## 相关
- [[Claude Code]] — relates_to
- [[Claude Code四大能力基元]] — part_of
- [[Model Context Protocol]] — relates_to
- [[External Services]] — relates_to