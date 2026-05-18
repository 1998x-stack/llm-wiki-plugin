---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, documentation, agent-guidance, AI工程]
aliases: ["CLAUDE.md Document", "CLAUDE.md 文档", "Agent Configuration Documentation"]
relates_to:
  - target: "[[Harness-Engineering]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Claude-Code]]"
    type: relates_to
    confidence: 0.9
  - target: "[[Agent-Guidance]]"
    type: part_of
    confidence: 0.8
  - target: "[[Context-Management]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# CLAUDE.md文档

## 概述
[[CLAUDE.md]]是为AI Agent（特别是[[Claude Code]]）设计的[[Configuration|配置]]文档，用于定义项目规则、架构约束和开发规范，使Agent能够理解并遵循项目的特定要求。

## 关键内容

1. **作用与意义**：
   - 为AI Agent提供项目的架构规范、命名约定、[[错误处理|错误处理策略]]
   - 包含"禁止做什么"的负面清单和其他约束条件
   - 作为Agent的行为准则和操作指南

2. **演变过程**：
   - 初始时可能只包含基本指导原则
   - 随着Agent犯错，逐步添加规则、调整约束、补充上下文
   - 经过多次迭代后可能变成数百行的详细文档

3. **[[Harness-Engineering|Harness Engineering]]体现**：
   - 代表[[Harness-Engineering|Harness Engineering]]的核心理念：写[[CLAUDE.md]]花的时间比写代码还多，但这不是浪费时间
   - 体现了"设计让代码被正确写出来的系统"这一理念
   - 将项目规则写下来让机器能读懂，而非依赖人工review和口头传达

4. **最佳实践**：
   - 保持[[文档结构化提取|文档结构化]]组织，便于Agent[[渐进式披露（Progressive Disclosure）|按需加载]]
   - 明确列出架构约束和质量标准
   - 定期更新以反映项目变化和Agent学习结果
   - 与CI/CD流程集成以自动验证Agent输出

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 关于CLAUDE.md文档重要性和作用的讨论

## 相关
- [[Harness-Engineering]] — relates_to
- [[Claude-Code]] — relates_to
- [[Agent-Guidance]] — relates_to
- [[Context-Management]] — relates_to
- [[OpenAI百万行代码实验]] — relates_to