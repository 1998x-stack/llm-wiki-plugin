---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [architecture-pattern, agent-system, hooks, lifecycle, AI工程]
aliases: ["Hooks 系统", "Hook System", "Lifecycle Hooks"]
relates_to:
  - target: "[[Claude Code]]"
    type: component_of
  - target: "[[PreToolUse]]"
    type: includes
  - target: "[[PostToolUse]]"
    type: includes
  - target: "[[Security Gate]]"
    type: implements
  - target: "[[Quality Gate]]"
    type: implements
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Hooks 系统

## 概述
[[Hooks]] 系统是 [[Claude Code]] 中的确定性控制层，包含 21 个生命周期事件和 4 种处理器类型，用于实现安全门和质量[[门控机制（Gating Mechanism）|门控]]制。

## 关键内容
1. **组成结构**：
   - 21 个生命周期事件
   - 4 种处理器类型：command、http、prompt、agent
   - PreToolUse（安全门，可拦截）
   - PostToolUse（质量门，可注入）

2. **功能分类**：
   - **安全门**：在 PreToolUse 阶段执行，可以拦截潜在危险操作
   - **质量门**：在 PostToolUse 阶段执行，可以注入额外的验证或修复操作

3. **应用场景**：
   - 在工具调用前验证参数安全性
   - 在工具调用后验证结果质量
   - 实现[[Permissions|权限]]控制和操作审计
   - 在系统关键节点插入自定义逻辑

4. **设计目的**：提供一种可扩展的机制来增强 [[Claude Code]] 的安全性和[[质量保障|质量控制]]，同时保持系统的灵活性。

## 来源
- [[01_system_overview.md]] — Claude Code 系统总览

## 相关
- [[Claude Code]] — component_of
- [[PreToolUse]] — includes
- [[PostToolUse]] — includes
- [[Security Gate]] — implements
- [[Quality Gate]] — implements

## 指令