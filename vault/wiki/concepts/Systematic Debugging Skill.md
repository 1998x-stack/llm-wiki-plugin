---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["superpowers", "debugging", "workflow", "Agent系统"]
aliases: ["systematic-debugging", "Debugging Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
---

# Systematic Debugging Skill

## 概述
[[Superpowers]] 刚性[[Skills|技能]]，以"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"为铁律，用 4 个必须按顺序完成的阶段将猜测式调试替换为证据驱动的根因调查。

## 关键内容

1. **铁律**：
   > NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

2. **适用场景**：
   - ✅ 测试失败
   - ✅ 生产 Bug
   - ✅ 性能问题
   - ✅ 构建失败
   - ✅ 任何"不按预期工作"的行为

3. **4 个阶段**：
   - **Phase 1**：根因调查（理解故障）
   - **Phase 2**：模式分析（寻找规律）
   - **Phase 3**：假设与验证（形成假设并测试）
   - **Phase 4**：实现修复（执行修复并验证）

4. **Phase 1 步骤**：
   - 仔细阅读错误信息（完整 stack trace）
   - 稳定复现（不能复现则不开始）
   - 检查最近变更（git diff）

## 来源
- [[09-systematic-debugging]] — systematic-debugging Skill 解析

## 相关
- [[Superpowers]] — part_of
- [[TDD Skill]] — relates_to
