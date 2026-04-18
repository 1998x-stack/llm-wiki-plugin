---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: [user-modeling, ai, hermes]
aliases: []
relates_to:
  - Hermes Agent
  - 闭环学习系统
  - 分层记忆系统
  - 跨会话记忆
  - 辩证推理
  - Plastic Labs
supersedes: null
---

# Honcho

## 概述
[[Hermes Agent]] 内置的用户建模系统，通过[[辩证推理]]跨会话构建动态用户画像，是[[闭环学习系统]]的核心组件之一。

## 关键内容
- **核心功能**：通过[[辩证推理]]（dialectical reasoning）跨会话构建动态用户画像
- **在 [[Hermes Agent|Hermes]] 中的角色**：[[闭环学习系统]]的关键组成部分，与记忆管理、Skill 创建、FTS5 召回协同工作；通过 `honcho-ai` 包集成，可用 `hermes honcho` 查看状态、`hermes honcho reset` 重置
- **工作方式**：在 Agent 跨会话交互中持续收集用户偏好、环境信息、项目约定等，形成结构化的用户模型
- **价值**：使 Agent 能够"下次开口就认识你"，实现真正的个性化体验，而非依赖手动编写 System Prompt
- **[[辩证推理]]机制**：源自哲学的正题-反题-合题循环——观察"用户要求简洁"（正题），观察"用户对代码解释要求很详细"（反题），推断"用户对文字说明要简洁，对技术代码要详细"（合题），持续精炼认知
- **与 USER.md 区别**：USER.md 存储用户告诉 Agent 的事实，静态添加/替换，简单键值式；Honcho 推断用户未明确表达的偏好，[[辩证推理]]动态更新，构建认知模型
- **数据结构**：包含 preferences（明确偏好）、inferred_patterns（推断模式）、contradictions（已发现矛盾待辩证解决）、resolved_dialectics（已解决的辩证矛盾）、confidence_scores（每个推断的置信度）、update_history（模型更新历史）
- **CLI 命令**：`hermes honcho status` 查看用户模型摘要、`hermes honcho show` 查看完整用户模型、`hermes honcho reset` 重置从零学习、`hermes honcho export` 导出用户模型可备份/迁移
- **创建者**：由 [[Plastic Labs]] 构建，[[Hermes Agent|Hermes]] 通过 `honcho-ai` Python 包深度集成

## 来源
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本
- [06_hermes_learning_loop.md](/raw/articles/ai-tools/hermes/06_hermes_learning_loop.md) — Hermes Agent 深度解析第六篇：闭环学习引擎，Honcho 辩证用户建模、数据结构、CLI 命令

## 相关
- [[Hermes Agent]] — part_of
- [[闭环学习系统]] — part_of
- [[跨会话记忆]] — extends
- [[分层记忆系统]] — part_of
- [[辩证推理]] — uses
- [[Plastic Labs]] — created
