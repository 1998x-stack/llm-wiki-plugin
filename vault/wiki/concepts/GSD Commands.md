---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["gsd", "workflow", "cli", "commands", "工具与框架"]
aliases: ["GSD Commands", "GSD 命令", "gsd commands"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[多智能体编排]]"
    type: implements
  - target: "[[波次并行执行]]"
    type: implements
---

# GSD Commands

## 概述
GSD 系统的核心命令集，覆盖从项目初始化到里程碑完成的完整开发链路，每个命令对应特定职责，形成单向信息流。

## 关键内容

1. **项目生命周期命令**：
   - `/gsd:new-project` — 项目初始化（提问→研究→需求→路线图）
   - `/gsd:new-milestone` — 新版本里程碑
   - `/gsd:complete-milestone` — 里程碑归档

2. **阶段工作流命令**：
   - `/gsd:discuss-phase N` — 捕获实现偏好（生成 CONTEXT.md）
   - `/gsd:ui-phase N` — [[UI Design Contract|UI 设计契约]]（生成 [[UI Design Contract|UI-SPEC]].md）
   - `/gsd:plan-phase N` — 研究 + 规划（生成 RESEARCH.md + [[XML Plan|PLAN.md]]）
   - `/gsd:execute-phase N` — [[Wave Execution|波次并行执行]]
   - `/gsd:verify-work N` — 人工验收测试
   - `/gsd:ship N` — 创建 PR

3. **辅助命令**：
   - `/gsd:next` — 自动推进（分析状态执行下一步）
   - `/gsd:quick` — 临时任务（轻量流程）
   - `/gsd:fast "task"` — 极小微调（内联执行）
   - `/gsd:resume-work` — 恢复会话
   - `/gsd:pause-work` — 暂停会话
   - `/gsd:progress` — 查看进度
   - `/gsd:help` — 帮助

4. **代码库命令**：
   - `/gsd:map-codebase` — 棕地代码库分析

5. **工作流原则**：
   - 每个步骤单一职责
   - 信息单向流动：discuss → CONTEXT.md → plan → [[XML Plan|PLAN.md]] → execute → SUMMARY.md → verify

## 来源
- [[03-core-workflow]] — 核心工作流

## 相关
- [[GSD]] — part_of
- [[GSD Planning Directory]] — uses
- [[多智能体编排]] — implements
- [[波次并行执行]] — implements
