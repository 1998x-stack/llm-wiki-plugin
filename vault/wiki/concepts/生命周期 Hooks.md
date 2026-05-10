---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [hooks, lifecycle, extensibility, event-driven]
aliases: [Lifecycle Hooks, Gateway Hooks]
relates_to:
  - target: "[[Gateway 消息网关]]"
    type: part_of
    confidence: 0.9
  - target: "[[Hermes Agent]]"
    type: implements
    confidence: 0.7
  - target: "[[工具注册机制]]"
    type: extends
    confidence: 0.5
supersedes: null
---

# 生命周期 Hooks

## 概述
[[Gateway 消息网关|Hermes Gateway]] 在关键事件点插入自定义逻辑的扩展机制，支持用户自定义和内置两种 [[Hooks]]。

## 关键内容
- **Hook 注册方式**：通过 `@on_event("event_name")` 装饰器注册，在特定事件触发时执行自定义逻辑
- **关键事件点**：`session_start`（会话开始）、`message_received`（消息接收）、`session_end`（会话结束）等
- **用户自定义示例**：会话开始时记录日志、特定关键词（如 "URGENT"）触发高优先级处理、消息内容过滤或转换
- **内置 [[Hooks]]（builtin_hooks/）**：心跳检测、日报日志、周报摘要、错误通知，开箱即用
- **与[[工具注册机制]]的对比**：[[工具注册机制]]通过 `@register_tool` 在导入时自动注册工具函数；生命周期 [[Hooks]] 通过 `@on_event` 注册事件回调，两者都是声明式注册模式
- **扩展性价值**：无需修改 [[网关与路由器|Gateway]] 核心代码即可添加自定义行为，符合[[SOLID原则|开闭原则]]，是 [[网关与路由器|Gateway]] 平台化能力的重要组成部分

## 来源
- [05_hermes_gateway.md](/raw/articles/ai-tools/hermes/05_hermes_gateway.md) — Hermes Agent 深度解析第五篇：Gateway 消息网关，2026 年 4 月版本

## 相关
- [[Gateway 消息网关]] — part_of
- [[Hermes Agent]] — implements
- [[工具注册机制]] — extends
