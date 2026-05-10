---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [authorization, security, pairing, access-control]
aliases: [DM Pairing, Pairing Authorization]
relates_to:
  - target: "[[Gateway 消息网关]]"
    type: part_of
    confidence: 0.9
  - target: "[[Hermes Agent]]"
    type: implements
    confidence: 0.7
  - target: "[[记忆安全扫描]]"
    type: extends
    confidence: 0.5
supersedes: null
---

# DM 配对授权

## 概述
[[Gateway 消息网关|Hermes Gateway]] 的安全机制，通过配对码验证用户身份，防止未授权访问 Agent 能力。

## 关键内容
- **配对流程**：CLI 生成配对码（`hermes gateway pair`）→ 用户在 Telegram 等平台发送 `/pair <配对码>` → 配对成功后该账户被授权
- **多用户支持**：支持家庭成员、团队成员等多用户授权，每个用户在 `allowed_users` 中[[Configuration|配置]]（如 `telegram:123456789`）
- **会话隔离**：每个授权用户有独立的会话隔离，互不干扰，即使在同一平台同一群组中
- **授权验证时机**：每条消息到达时首先执行 `pairing.is_authorized(user_id, platform)`，未授权则拒绝并提示配对
- **安全意义**：作为 [[网关与路由器|Gateway]] 入口层的第一道防线，与[[记忆安全扫描]]（防止敏感信息持久化）共同构成 [[Hermes Agent|Hermes]] 的安全体系
- **[[Configuration|配置]]模式**：`authorization.mode: pairing` 启用配对模式，也可通过 `allowed_users` 白名单直接授权

## 来源
- [05_hermes_gateway.md](/raw/articles/ai-tools/hermes/05_hermes_gateway.md) — Hermes Agent 深度解析第五篇：Gateway 消息网关，2026 年 4 月版本

## 相关
- [[Gateway 消息网关]] — part_of
- [[Hermes Agent]] — implements
- [[记忆安全扫描]] — extends
