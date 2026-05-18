---
type: project
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ai-tools, coding-assistant, github, microsoft, AI工程]
aliases: ["GitHub Copilot", "Copilot"]
relates_to:
  - target: "[[Claude Code]]"
    type: compares_to
  - target: "[[抗 AI 评测设计]]"
    type: relates_to
  - target: "[[评测驱动开发]]"
    type: relates_to
supersedes: null
---

# GitHub Copilot

## 概述
[[GitHub]] 与 [[OpenAI]] 合作开发的 AI 代码补全工具，提供代码建议、自动补全和对话式编程辅助，是最早广泛采用的 AI 编程助手之一。

## 关键内容

1. **核心功能**：
   - **代码补全**：基于上下文提供实时代码建议
   - **对话式编程**：通过自然语言描述需求生成代码
   - **多语言支持**：支持主流编程语言和框架

2. **对技术评测的影响**：
   - AI 可以在几秒内解决大多数经典[[算法]]题
   - AI 可以通过多数代码完成性测试
   - AI 可以生成看起来合理的系统设计方案
   - 导致"[[评测通货膨胀]]"——通过传统评测不再意味着候选人具备传统评测试图验证的能力

3. **与同类工具比较**：
   - 与 [[Claude Code]] 等工具一起改变了技术招聘的评测范式
   - 推动了从"测试知识记忆"向"测试理解深度和判断能力"的转变

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/19_ai_resistant_evals.md]] — 设计抗 AI 的技术评估

## 相关
- [[Claude Code]] — compares_to（同为 AI 编程助手，但架构和生态不同）
- [[抗 AI 评测设计]] — relates_to（其普及推动了抗 AI 评测的需求）
- [[评测通货膨胀]] — relates_to（是导致评测通货膨胀的工具之一）
- [[评测驱动开发]] — relates_to（评测方法论的演变背景）
