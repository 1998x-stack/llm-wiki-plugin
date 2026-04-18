---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["gateway", "messaging", "integration", "ai-agent", "工具与框架"]
aliases: [Hermes Gateway, 统一消息网关]
relates_to:
  - target: "[[Hermes Agent]]"
    type: part_of
    confidence: 0.9
  - target: "[[平台适配器模式]]"
    type: uses
    confidence: 0.9
  - target: "[[会话持久化]]"
    type: uses
    confidence: 0.9
  - target: "[[DM 配对授权]]"
    type: uses
    confidence: 0.8
  - target: "[[Cron 调度系统]]"
    type: extends
    confidence: 0.8
  - target: "[[ACP 编辑器集成]]"
    type: compares_to
    confidence: 0.7
  - target: "[[消息镜像同步]]"
    type: uses
    confidence: 0.8
  - target: "[[生命周期 Hooks]]"
    type: uses
    confidence: 0.8
  - target: "[[OpenClaw]]"
    type: compares_to
    confidence: 0.8
  - target: "[[跨会话记忆]]"
    type: extends
    confidence: 0.7
supersedes: null
---

# Gateway 消息网关

## 概述
[[Hermes Agent]] 的入口层组件，将 Agent 能力暴露到 15+ 消息平台的统一通信总线，实现"随时随地可达"的持续在线 AI 体验。

## 关键内容
- **核心价值**：打破"必须坐到电脑前打开终端"的使用限制，让用户通过 Telegram、WhatsApp、Slack、Discord 等任意平台与 Agent 交互
- **架构定位**：在[[三层分离架构]]的入口层中，与 CLI、ACP、[[Batch Runner]] 并列，最终都调用 `AIAgent.run_conversation()`
- **与 [[OpenClaw]] 的根本差异**：[[OpenClaw]] 把 [[网关与路由器|Gateway]] 作为控制平面（单一长期进程，所有东西流过它）；[[Hermes Agent|Hermes]] 的 [[网关与路由器|Gateway]] 更轻，只做消息路由，核心逻辑在 AIAgent 循环里
- **五大职责**：接收各平台消息 → 标准化为 MessageEvent → 管理会话状态 → 调用 AIAgent 处理 → 将结果发回原平台
- **消息处理链路**：平台事件到达 → Adapter.on_message() 解析 → 转换为 MessageEvent → 授权验证 → 解析 session_key → 加载历史 → 创建 AIAgent → 执行对话 → 投递响应 → 持久化会话 → 触发 hooks
- **双模式支持**：[[网关与路由器|Gateway]] 处理被动响应（用户发消息→Agent 回复），[[Cron 调度系统]]处理主动触发（定时任务→Agent 执行→投递结果），两者共用相同的 AIAgent 执行引擎
- **配置方式**：通过 `hermes gateway setup` [[交互式配置]]，`hermes gateway start [--daemon]` 启动，支持 webhook 和 polling 两种模式
- **平台无关性设计**：新增一个平台只需实现适配器接口，不改变 AIAgent 核心逻辑，15 个适配器统一接口

## 来源
- [05_hermes_gateway.md](/raw/articles/ai-tools/hermes/05_hermes_gateway.md) — Hermes Agent 深度解析第五篇：Gateway 消息网关，2026 年 4 月版本

## 相关
- [[Hermes Agent]] — part_of
- [[平台适配器模式]] — uses
- [[会话持久化]] — uses
- [[DM 配对授权]] — uses
- [[Cron 调度系统]] — extends
- [[ACP 编辑器集成]] — compares_to
- [[消息镜像同步]] — uses
- [[生命周期 Hooks]] — uses
- [[OpenClaw]] — compares_to
- [[跨会话记忆]] — extends
