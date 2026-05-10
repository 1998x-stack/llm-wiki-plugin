---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [superpowers, skill, planning, execution]
aliases: ["executing-plans", "executing-plans Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[writing-plans Skill]]"
    type: follows
  - target: "[[subagent-driven-development Skill]]"
    type: alternative
---

# executing-plans Skill

## 概述
[[Superpowers]] [[Skills|技能]]，用于在没有[[子 Agent & 多 Agent 系统|子 Agent]] 功能的平台上执行计划文档中的任务。作为 [[subagent-driven-development Skill]] 的替代方案，在单一会话中按顺序执行原子级任务清单。

## 关键内容

1. **适用场景**：
   - 无[[子 Agent & 多 Agent 系统|子 Agent]] 功能的平台（如 [[Gemini CLI]]）
   - 需要在独立会话中批量执行计划
   - 适合无人值守执行的任务

2. **执行方式**：
   - 在新会话中使用 executing-plans
   - 批量执行，有人工检查点
   - 每个任务按顺序执行，有验证步骤

3. **与 [[subagent-driven-development Skill|subagent-driven-development]] 的区别**：
   - ❌ 无[[子 Agent & 多 Agent 系统|子 Agent]] 派遣
   - ❌ 无双阶段代码评审
   - ✅ 顺序执行
   - ✅ 人工检查点

4. **执行流程**：
   - 读取计划文档（通常在 `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`）
   - 按顺序执行每个 Task
   - 每个任务完成后进行验证
   - 在适当时机进行提交（[[commit]]）

5. **Task 执行结构**：
   - Step 1: 写失败测试
   - Step 2: 运行确认失败
   - Step 3: 写最少实现代码
   - Step 4: 运行确认通过
   - Step 5: Commit

## 来源
- [[03-writing-plans]] — executing-plans 作为 subagent-driven-development 替代方案

## 相关
- [[writing-plans Skill]] — precedes
- [[subagent-driven-development Skill]] — alternative_to
- [[Superpowers]] — part_of