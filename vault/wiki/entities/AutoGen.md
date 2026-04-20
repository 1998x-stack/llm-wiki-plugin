---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["tool", "agent-framework", "multi-agent"]
aliases: ["AutoGen 框架", "Microsoft AutoGen"]
relates_to:
  - "[[AI Agent 架构模式]] — compares_to"
  - "[[LangChain]] — compares_to"
supersedes: null
---

# AutoGen

## 概述
Microsoft 开发的多 Agent 框架，与 LangChain 同属市面上流行的 Agent 开发框架，被 Anthropic 作为复杂性抽象的代表提及。

## 关键内容
1. **框架定位**：AutoGen 是 Microsoft 推出的多 Agent 框架，与 LangChain 等竞相推出越来越精密的抽象层。
2. **Anthropic 的批评**：Anthropic 观察到框架的抽象层往往遮蔽了底层的 prompt 与响应，使调试变得困难，并诱导开发者在不必要时引入额外复杂性。
3. **替代建议**：Anthropic 建议开发者首先直接使用 LLM API，许多模式仅需几行代码即可实现。
4. **行业背景**：在"万能框架"思维盛行时期，Anthropic 的"简单优于复杂"论点对 AutoGen 等框架的复杂性形成了有力反驳。

## 来源
- [[01_building_effective_agents.md]] — 第一章，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[AI Agent 架构模式]] — compares_to (Anthropic 模式与之对比)
- [[LangChain]] — compares_to (同类 Agent 框架)
