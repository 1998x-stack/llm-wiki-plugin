---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["agent-identity", "personality", "system-prompt", "SOUL.md", "工具与框架"]
aliases: [SOUL.md, Agent Personality System]
relates_to:
  - Hermes Agent
  - 闭环学习系统
  - 自我进化代理
supersedes: null
---

# SOUL.md 人格系统

## 概述
定义 AI Agent 身份和行为准则的核心文件，注入 System Prompt 的第一个内容且优先级高于一切，用户可直接编辑实现个性化定制。

## 关键内容
- **在 Prompt 组装中的位置**：SOUL.md → [[语义记忆|MEMORY.md]] → USER.md → [[Agent Skills|Skills]] Level 0 → Context Files → Active Tools → Date/Time → Platform Metadata，是注入链的第一环
- **默认结构**：包含 Identity（身份定义）、Core Principles（核心原则：主动学习、记忆卫生、诚实能力表达、用户模型构建）、Behavioral Defaults（行为默认值：语言跟随、简洁优先、实时展示、不确定时提问）、Self-Improvement Nudges（自我改进轻推）
- **用户可编辑**：存储在 `~/.hermes/SOUL.md`，用户可通过 `hermes config show/edit soul` 或直接编辑文件进行自定义，下次会话自动生效
- **自定义能力**：用户可完全替换默认 SOUL.md，定义专属 Agent 身份（如 "CodeReview Pro"）、专业领域、审查哲学、沟通风格等
- **与传统 System Prompt 的对比**：传统 System Prompt 存储在代码或配置中需修改代码/重新部署才能更新，SOUL.md 存储在用户可编辑的文件中直接修改即生效；传统 System Prompt 与记忆独立，SOUL.md 之后紧接着注入 [[语义记忆|MEMORY.md]] 形成关联
- **Agent 修改权限**：Agent 对 SOUL.md 仅有有限度的修改能力（通过工具），主要修改权在用户手中

## 来源
- [06_hermes_learning_loop.md](/raw/articles/ai-tools/hermes/06_hermes_learning_loop.md) — Hermes Agent 深度解析系列第六篇：闭环学习引擎

## 相关
- [[Hermes Agent]] — implements
- [[闭环学习系统]] — part_of
- [[自我进化代理]] — part_of
