---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-engineering, methodology, workflow, AI工程]
aliases: ["Plan Work Review Compound", "Plan-Work-Review-Compound", "PWRP"]
relates_to:
  - target: "[[Compound-Engineering]]"
    type: part_of
    confidence: 0.9
  - target: "[[AI-Engineering]]"
    type: implements
    confidence: 0.7
  - target: "[[Agile-Development]]"
    type: compares_to
    confidence: 0.6
supersedes: null
---

# Plan-Work-Review-Compound

## 概述
Plan-Work-Review-Compound 是 [[Compound Engineering]] 方法论的[[游戏主循环模式|主循环]]，包含四个阶段的迭代流程，强调通过知识积累实现复利效应。

## 关键内容

1. **Plan（计划）阶段**：
   - 理解需求、研究代码库、外部调研
   - 设计方案并验证计划
   - 可触发深度模式，派生40+个并行研究智能体

2. **Work（执行）阶段**：
   - [[Settings|设置]]隔离环境（Git worktree）
   - 按计划逐步执行并运行验证
   - 跟踪进度并处理问题

3. **Review（审查）阶段**：
   - 多智能体并行审查代码
   - 优先级排序（P1/P2/P3）
   - 解决问题并捕获模式

4. **Compound（积累）阶段**：
   - 捕获解决方案和经验
   - 建立可检索性（YAML frontmatter）
   - 更新系统知识库和模式

## 来源
- [[raw/articles/ai-engineering/prompt-context/compound-engineering-deep-analysis]]
- [[EveryInc/compound-engineering-plugin]]

## 相关
- [[Compound-Engineering]] — part_of
- [[AI-Engineering]] — relates_to
- [[Agile-Development]] — compares_to
- [[Knowledge-Management]] — relates_to