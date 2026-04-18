---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["gsd", "ui", "design-system", "frontend", "工具与框架"]
aliases: ["UI Design Contract", "UI-SPEC", "UI 设计契约"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[shadcn/ui]]"
    type: uses
---

# UI Design Contract

## 概述
GSD 系统的 UI 设计契约机制，在执行前生成 UI-SPEC.md 锁定设计规范，解决 AI 生成前端组件视觉不一致问题，包含 6 维度验证和 shadcn 集成。

## 关键内容

1. **问题背景**：
   - Claude 单独写一个组件时很好
   - 写第五、第十个组件时视觉不一致
   - 原因：执行前没有共享设计规范

2. **工作流位置**：
   ```
   discuss-phase → ui-phase → plan-phase → execute-phase
   ```

3. **核心命令**：
   - `/gsd:ui-phase N`：执行前生成设计契约（UI-SPEC.md）
   - `/gsd:ui-review`：执行后量化审计结果

4. **6 维度验证**：
   - 间距系统一致性
   - 字体层级合理性
   - 颜色策略统一性
   - 文案风格一致性
   - 空状态/加载状态规范
   - 无障碍基础要求

5. **shadcn 集成**：
   - 检测 components.json
   - 提供初始化指引
   - Preset 字符串编码设计系统

## 来源
- [[06-ui-design-contract]] — UI 设计契约系统

## 相关
- [[GSD]] — part_of
- [[shadcn/ui]] — uses
- [[frontend-design Skill]] — relates_to
