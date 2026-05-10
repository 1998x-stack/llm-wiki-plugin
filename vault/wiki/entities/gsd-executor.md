---
type: entity
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, executor, implementation]
aliases: ["gsd-executor", "GSD Executor", "GSD执行智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-planner]]"
    type: follows_after
    confidence: 0.8
supersedes: null
---

# gsd-executor

## 概述
GSD框架中的执行智能体，负责根据计划文件执行具体的开发任务，拥有独立的干净上下文环境，确保执行过程不受其他执行者的干扰。

## 关键内容

1. **职责与功能**：
   - 根据[[XML Plan|PLAN.md]]文件中的XML结构任务列表执行具体实现
   - 拥有独立的200k上下文，不受其他执行者影响
   - 逐任务执行，每完成一个任务立即[[Git Commit|git commit]] --no-verify
   - 执行<verify>标签中的验证命令（如curl、pnpm test等）
   - 执行完成后退出，不保留历史状态

2. **上下文构建**：
   - 输入：PROJECT.md（项目约束）、当前N-M-[[XML Plan|PLAN.md]]（XML结构任务列表）
   - 不包含：其他阶段的计划文件、REQUIREMENTS.md、RESEARCH.md等冗余信息
   - 精确的上下文构建确保信号噪声比最优

3. **执行特点**：
   - 最小化上下文输入，只包含必要信息
   - 保证执行过程的纯净性
   - 每个任务完成后立即提交，便于追踪和回滚
   - 支持实时验证命令执行

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-planner]] — 前置计划生成者