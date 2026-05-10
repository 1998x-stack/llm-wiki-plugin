---
type: project
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["AI工程", "Harness工程", "自动化", "代码生成"]
aliases: ["OpenAI Harness System"]
relates_to:
  - target: "[[Harness Engineering]]"
    type: implements
    confidence: 0.9
  - target: "[[Claude Code]]"
    type: relates_to
    confidence: 0.8
  - target: "[[LLM-工程三阶段]]"
    type: exemplifies
    confidence: 0.85
  - target: "[[Constraints System]]"
    type: utilizes
    confidence: 0.9
supersedes: null
---

# OpenAI Harness

## 概述
OpenAI Harness是由OpenAI开发的Harness工程实践案例，展示了如何构建AI代码生成的约束系统，实现了100万行代码/3人/5个月的惊人生产力。

## 关键内容

1. **核心理念**：
   - 通过环境约束而非直接代码审查来保障代码质量
   - 构建AI友好的代码库结构和文档地图
   - 建立自动化的代码生成、检查、清理循环

2. **技术架构**：
   - 文档地图系统：为AI提供代码库的导航和上下文
   - 约束规则引擎：通过CI门控强制执行代码规范
   - GC Agent：自动清理和重构代码库

3. **显著成果**：
   - 高效的AI辅助开发流程
   - 大规模代码生成的同时保持高质量
   - 小团队高产出的典范

## 来源
- [[LLM-工程三阶段]] — 演化驱动力分析
- [[LLM-工程三阶段对比分析]] — 价值主张对比

## 相关
- [[Harness Engineering]] — implements
- [[Claude Code]] — relates_to
- [[LLM-工程三阶段]] — relates_to
- [[Constraints System]] — relates_to