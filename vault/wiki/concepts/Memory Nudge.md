---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["memory-nudge", "self-reflection", "ai-agent", "memory-hygiene", "Agent系统"]
aliases: [Memory Nudge, Nudge Mechanism, 轻推机制]
relates_to:
  - 闭环学习系统
  - 分层记忆系统
  - 技能自我改进
  - Hermes Agent
supersedes: null
---

# Memory Nudge

## 概述
[[Hermes Agent]] 在长对话自然暂停点主动自我反思的机制，检查是否有值得保存的经验、偏好或技能，确保信息不流失。

## 关键内容
- **触发时机**：完成一个完整任务后、用户说"谢谢就这些"等结束语时、对话出现较长暂停时、达到预设的消息计数阈值时
- **自我反思清单**：
  - 学到了关于环境的新事实吗？→ 保存到 [[语义记忆|MEMORY.md]]
  - 用户表达了新的偏好吗？→ 保存到 USER.md，更新 [[Honcho]] 模型
  - 刚完成了可复用的工作流吗？→ 创建 [[SKILL.md 格式规范|SKILL.md]]
  - 发现了现有技能的问题吗？→ 更新 [[SKILL.md 格式规范|SKILL.md]]
  - 纠正了之前的错误认知吗？→ 删除/替换旧记忆
- **设计哲学**：即使用户没有主动要求"记住这个"，Agent 也会通过自我反思确保经验不流失，这是记忆卫生（Memory Hygiene）的核心实践
- **在 [[SOUL.md 人格系统|SOUL.md]] 中的体现**：默认 [[SOUL.md 人格系统|SOUL.md]] 的 Self-Improvement Nudges 部分明确指示 Agent 在长会话自然暂停点检查是否有值得保存的内容
- **与闭环学习的关系**：Nudge 是[[闭环学习系统]]的驱动引擎——每次 Nudge 都可能触发记忆更新、技能创建或技能改进，推动学习飞轮持续运转

## 来源
- [06_hermes_learning_loop.md](/raw/articles/ai-tools/hermes/06_hermes_learning_loop.md) — Hermes Agent 深度解析系列第六篇：闭环学习引擎

## 相关
- [[闭环学习系统]] — part_of
- [[分层记忆系统]] — extends
- [[技能自我改进]] — extends
- [[Hermes Agent]] — implements
