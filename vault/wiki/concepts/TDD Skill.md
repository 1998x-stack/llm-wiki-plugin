---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["superpowers", "tdd", "testing", "workflow", "Agent系统"]
aliases: ["test-driven-development", "TDD Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[TDD]]"
    type: implements
---

# TDD Skill

## 概述
[[Superpowers]] 最严苛的刚性技能，以"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"为铁律，构建带强制验证门的 5 阶段 RED-GREEN-REFACTOR 循环。

## 关键内容

1. **铁律**：
   > NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
   
   违规代码必须删除，不能保留、不能适配、不能偷看。

2. **适用范围**：
   - ✅ 新功能实现
   - ✅ Bug 修复
   - ✅ 重构
   - ✅ 行为变更
   - ❓ 一次性原型（询问人类）

3. **5 阶段循环**：
   - **Phase 1 — RED**：写失败测试
   - **Phase 2 — 验证 RED**：确认测试正确失败
   - **Phase 3 — GREEN**：写最少实现代码
   - **Phase 4 — 验证 GREEN**：确认测试通过
   - **Phase 5 — REFACTOR**：重构（保持测试通过）

4. **测试要求**：
   - 每个测试只测一个行为
   - 清晰的测试名称（描述行为）
   - 测试真实代码（非 mock）

## 来源
- [[08-test-driven-development]] — test-driven-development Skill 解析

## 相关
- [[Superpowers]] — part_of
- [[TDD]] — implements
- [[writing-plans Skill]] — precedes
