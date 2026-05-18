---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: [ai-tools, agent-patterns, AI工程]
aliases: ["Coding Agent Protocol", "编码代理协议", "Coding Agent"]
relates_to:
  - target: "[[Ralph Loop 系统]]"
    type: part_of
  - target: "[[项目约定手册]]"
    type: uses
  - target: "[[强制启动序列]]"
    type: implements
supersedes: null
---

# 编码 Agent 协议

## 概述

编码 Agent 协议定义了 [[Ralph Loop 系统]]中工作主力 Agent 的完整行为规范，包括启动序列、核心约束、实现流程、验证方式和特殊情况处理。

## 关键内容

1. **角色定位**：Coding Agent 是 [[Ralph Loop]] 的工作主力，每次迭代一个全新实例启动，从文件继承进度，完成一个 Story 后退出。
2. **[[强制启动序列]]（7 步）**：确认工作目录 → 查看最近提交 → 读取 progress.txt（交班日记）→ 加载 [[项目约定手册|AGENTS.md]]（经验手册）→ 查找最高优先级未完成任务 → 启动环境（init.sh）→ 冒烟测试验证代码库正常。
3. **核心铁规则**：每次只实现 ONE 个 User Story；前端变更必须用[[浏览器自动化验证]]；每次迭代以 [[Git Commit|git commit]] 结束；必须更新 progress.txt；Bug 2 次无法解决则 git revert + 记录 + 跳到下一个。
4. **验证方式分层**：前端 Story 用 dev-browser skill 打开浏览器操作验证；API Story 用 curl 测试所有 endpoint；逻辑 Story 运行相关[[单元测试]]。
5. **状态更新流程**：验证通过后才能将 `passes` 设为 true → [[Git Commit|git commit]]（含 PRD 进度信息）→ 追加 progress.txt → 如有新发现更新 [[项目约定手册|AGENTS.md]]。
6. **特殊情况处理**：上下文快满时 git stash 保存进度并退出；需求冲突时选择最合理实现并在代码注释中说明；依赖未完成时跳过该 Story 继续下一个。
7. **progress.txt 格式**：每次迭代追加 Session 记录，包含 Story ID、状态（COMPLETED/PARTIAL/BLOCKED/REVERTED）、变更点、测试方式、下一个 Story、剩余数量、本次发现。

## 来源

- [[raw/articles/ai-tools/ralph-loop/coding-agent.md]] — 完整协议文档
- [[raw/articles/ai-tools/ralph-loop/CLAUDE.md]] — Agent 提示词模板

## 相关

- [[Ralph Loop 系统]] — part_of
- [[项目约定手册]] — uses
- [[强制启动序列]] — implements
