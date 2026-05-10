---
type: concept
status: active
confidence: 0.5
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [技术, 方法论]
aliases: [Harness Engineering, 驾驭工程]
relates_to:
  - target: "[[SDD规格驱动开发]]"
    type: extends
    confidence: 0.7
  - target: "[[Agent Skills]]"
    type: uses
    confidence: 0.75
  - target: "[[Agent Harness模式]]"
    type: compares_to
    confidence: 0.7
  - target: "[[Multi-Agent Orchestration]]"
    type: relates_to
    confidence: 0.6
  - target: "[[OpenAI Harness]]"
    type: exemplified_by
    confidence: 0.9
supersedes: null
---

# Harness Engineering

## 概述
Harness Engineering（驾驭工程）是 OpenAI 在 2026 年初公布的颠覆性工程范式：3 人团队 5 个月从零构建百万行代码生产级产品，全程无手写代码，所有代码由 Agent 自主生成。核心是给 AI 搭建可安全奔跑的"马具"。

## 关键内容
1. **核心三件事**：
   - 设计工程环境和架构约束：定义严格依赖方向、编码规范、黄金原则，避免 AI 产生技术债务
   - 定义任务和意图：将高层目标拆解为 AI 可执行的构建块，用清晰语言描述验收标准
   - 创建反馈循环：建立自动化机制让 AI 自我验证、自我评审、自我修复
2. **范式转变**：人类不再是写代码的工人，而是定义规则和环境的设计者
3. **效率上限**：AI 的效率上限不是模型能力，而是 Harness 的完善程度
4. **与 SDD 的关系**：Harness 中的"定义任务和意图"即 SDD 的核心实践
5. **实际成果**：OpenAI 团队 5 个月、100 万行代码、生产级产品，验证了该范式的可行性

## 来源
- [[raw/articles/essays/thinking-series/008-算法面试]] — 全文

## 相关
- [[SDD规格驱动开发]] — extends（SDD 是 Harness 的核心方法论）
- [[Agent Skills]] — uses（Skill 是 Harness 的柔性约束层）
- [[Agent Harness模式]] — compares_to
- [[Multi-Agent Orchestration]] — relates_to
