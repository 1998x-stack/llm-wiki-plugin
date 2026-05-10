---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["cron", "scheduling", "automation", "proactive-agent", "Agent系统"]
aliases: [Cron Scheduler, Natural Language Cron, 定时任务调度]
relates_to:
  - target: "[[Gateway 消息网关]]"
    type: extends
    confidence: 0.8
  - target: "[[Hermes Agent]]"
    type: implements
    confidence: 0.7
  - target: "[[冻结快照模式]]"
    type: contradicts
    confidence: 0.6
supersedes: null
---

# Cron 调度系统

## 概述
[[Hermes Agent|Hermes]] 内置的定时任务调度系统，支持自然语言定义任务，让 Agent 从被动响应转为主动执行。

## 关键内容
- **自然语言调度**：无需记忆 crontab 格式，直接用自然语言定义任务，如"每天早上 9 点，搜集科技新闻摘要，发到我的 Telegram"
- **执行流程**：调度器每分钟检查 → 从 jobs.json 加载到期任务 → 创建全新 AIAgent（无会话历史）→ 注入任务附加 [[Agent Skills|Skills]] → 运行任务提示词 → delivery.send() 投递 → 更新 next_run 时间戳
- **关键设计：每次创建全新 AIAgent**：Cron 任务是隔离的，不携带历史，确保结果的确定性和可重现性。这与[[冻结快照模式]]（会话开始时加载 [[语义记忆|MEMORY.md]] + USER.md 快照）形成对比——Cron 任务完全无状态
- **任务管理命令**：`hermes cron list/show/run/disable/delete`，支持列出、查看、手动执行、暂停、删除任务
- **与 [[网关与路由器|Gateway]] 的协同**：[[网关与路由器|Gateway]] 处理被动响应，Cron 处理主动触发，两者共用相同的 AIAgent 执行引擎和 delivery 投递系统，实现"被动 + 主动双模式"
- **存储格式**：任务定义存储在 jobs.json 中，包含 cron 表达式、目标平台、任务提示词、附加 [[Agent Skills|Skills]] 等
- **典型场景**：新闻摘要推送、[[Git Commit|Git 提交]]分析周报、API 费用统计月报、定期数据监控告警

## 来源
- [05_hermes_gateway.md](/raw/articles/ai-tools/hermes/05_hermes_gateway.md) — Hermes Agent 深度解析第五篇：Gateway 消息网关，2026 年 4 月版本

## 相关
- [[Gateway 消息网关]] — extends
- [[Hermes Agent]] — implements
- [[冻结快照模式]] — contradicts
