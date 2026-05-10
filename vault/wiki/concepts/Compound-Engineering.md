---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-engineering, methodology, productivity, automation]
aliases: ["复利工程", "Compound Engineering", "CE"]
relates_to:
  - target: "[[AI-Engineering]]"
    type: part_of
    confidence: 0.8
  - target: "[[Agent-Native-Architecture]]"
    type: implements
    confidence: 0.7
  - target: "[[LLM-Wiki]]"
    type: alternative_to
    confidence: 0.6
supersedes: null
---

# Compound Engineering

## 概述
[[Compound Engineering]] 是一种 AI 工程方法论，核心思想是每个工程工作单元应该让后续工作更轻松而非更困难，通过复利效应使系统持续变强。

## 关键内容

1. **核心哲学**：
   - 每个工程工作单元应让后续工作更轻松
   - 与传统软件工程的熵增规律对抗
   - 通过知识积累实现复利效应

2. **[[游戏主循环模式|主循环]]流程**：
   - Plan（计划）→ Work（执行）→ Review（审查）→ Compound（积累）
   - 80/20 时间分配原则：80% 计划和审查，20% 执行和积累
   - 思考发生在代码编写之前和之后

3. **智能体[[矩阵]]**：
   - 35+ 个专业智能体用于不同审查任务
   - 并行审查架构提高效率
   - 专注领域包括安全、性能、架构、数据、框架专项等

## 来源
- [[raw/articles/ai-engineering/prompt-context/compound-engineering-deep-analysis]]
- [[EveryInc/compound-engineering-plugin]]

## 相关
- [[AI-Engineering]] — part_of
- [[Agent-Native-Architecture]] — implements
- [[Plan-Work-Review-Compound]] — part_of
- [[AI-Agent]] — relates_to