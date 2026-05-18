---
type: tool
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [javascript-library, frontend-framework, react, AI设计]
aliases: ["React 19", "React v19"]
relates_to:
  - target: "[[React]]"
    type: extends
  - target: "[[jezweb/claude-skills]]"
    type: uses
  - target: "[[Frontend Plugin]]"
    type: used_by
  - target: "[[shadcn/ui]]"
    type: integrates_with
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# React 19

## 概述
[[React]] 19 是 [[React]] 库的重要版本，引入了新的 API 和现代化的组合设计模式，重点关注简化异步数据处理和表单操作。

## 关键内容
1. **use() API**：[[React]] 19 引入的新 API，用于直接读取 Promise，简化异步数据读取，配合 Suspense 自动处理加载状态，无需手动处理 Promise。

2. **Actions 特性**：引入简化的表单提交方式，支持[[服务]]端和客户端动作，通过 `'use server'` 或 `'use client'` 指令[[区分]]执行环境，简化了表单处理逻辑。

3. **性能优化**：提供更智能的自动 memoization（通过 [[React]] Compiler），减少了对 `useMemo` 和 `useCallback` 的过度使用，但仍需在特定场景下手动优化。

4. **组合模式**：继续推广复合组件模式（Compound Components），允许组件之间共享状态和行为，提高组件的可复用性和一致性。

5. **开发体验改进**：简化了常见的异步操作和副作用处理，减少了样板代码，提高了开发者效率。

## 来源
- [[04_jezweb_claude_skills_frontend]] — React 19 性能与组合模式解析

## 相关
- [[React]] — 基础框架的扩展
- [[jezweb/claude-skills]] — 包含 React 19 模式技能