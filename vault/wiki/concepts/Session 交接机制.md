---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["agent-pattern", "context-transfer", "session-management", "Agent系统"]
aliases: ["Session Handoff", "Agent 交接", "跨会话状态传递", "三文件交接"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: implemented_by
  - target: "[[PRD 驱动开发]]"
    type: enables
  - target: "[[Context Engineering]]"
    type: part_of
  - target: "[[上下文窗口]]"
    type: relates_to
supersedes: null
---

# Session 交接机制

## 概述
Session 交接机制是一种跨 Agent 会话的状态传递模式，通过 prd.json（进度）、progress.txt（日记）和 [[项目约定手册|AGENTS.md]]（经验）三个核心文件实现知识的持久化和继承，使每个新 Agent 实例无需依赖前一个实例的上下文记忆即可无缝继续工作。

## 关键内容

1. **三文件架构**：
   - **prd.json**：权威进度源，包含所有 User Story 的状态（passes/未完成）、优先级、依赖关系。新 Agent 启动时首先解析此文件确定当前任务。
   - **progress.txt**：交班日记，按 Session 编号追加记录，包含完成的 Story、变更点列表、测试结果、阻塞信息、下一步计划。提供操作级别的上下文。
   - **[[项目约定手册|AGENTS.md]]**：[[项目约定手册]]，包含项目概览、运行方式、文件结构、命名规范、代码约定、[[Environment Variables|环境变量]]、已知坑点（[[Gotchas]]）和 Learnings。由 Agent 在运行过程中持续维护。

2. **启动读取顺序**：新 Agent 实例的[[强制启动序列]]中，第 3 步读取 progress.txt（交班日记），第 4 步读取 [[项目约定手册|AGENTS.md]]（经验手册），第 5 步解析 prd.json（任务源）。这个顺序确保 Agent 先了解历史背景，再确定当前任务。

3. **结束写入规范**：
   - progress.txt 追加 Session 记录：Story ID、状态（COMPLETED/BLOCKED/Early exit）、变更点、测试结果、下一个 Story、剩余数量
   - [[项目约定手册|AGENTS.md]] 在 Learnings 部分追加新发现的规律、坑点、约定
   - prd.json 更新已完成 Story 的 `passes: true`

4. **与 [[上下文窗口]] 的关系**：Session 交接机制本质上是 [[Context Engineering]] 的一种实践——将有限的[[上下文窗口]]内的关键信息外部化到持久文件中，突破[[上下文窗口]]的限制。每个新 Agent 实例通过读取这些文件"恢复"前一个实例的知识状态。

5. **与 [[PRD 驱动开发]] 的关系**：prd.json 作为三文件之一，同时是 [[PRD 驱动开发]]的核心数据源。Session 交接机制确保 prd.json 的状态在 Agent 实例之间一致传递。

6. **设计优势**：
   - **抗上下文丢失**：不依赖 Agent 的上下文记忆，所有关键状态持久化到文件
   - **可审计**：progress.txt 提供完整的操作历史日志
   - **可回退**：Git 历史 + progress.txt 可追溯到任意时间点的状态
   - **可扩展**：新 Agent 实例可以来自不同的[[上下文窗口]]，只要读取相同文件即可继续

## 来源
- [[raw/articles/ai-tools/ralph-loop/CLAUDE.md]] — Ralph Coding Agent 提示词模板中的启动序列和结束流程
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — AGENTS.md 项目约定模板
- [[raw/articles/ai-tools/ralph-loop/coding-agent.md]] — Coding Agent 完整协议中的 progress.txt 更新格式规范

## 相关
- [[Ralph Loop]] — implemented_by（Session 交接机制的具体实现系统）
- [[PRD 驱动开发]] — enables（prd.json 作为进度源在会话间传递）
- [[Context Engineering]] — part_of（上下文外部化的核心实践）
- [[上下文窗口]] — relates_to（突破上下文窗口限制的解决方案）
- [[Agent 迭代循环]] — relates_to（每次迭代结束时执行交接写入）
