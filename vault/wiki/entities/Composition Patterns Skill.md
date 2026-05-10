---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, react, architecture, skills]
aliases: ["composition-patterns", "React Composition Patterns", "Compound Components Pattern"]
relates_to:
  - target: "[[Vercel Agent Skills]]"
    type: part_of
    confidence: 0.9
  - target: "[[React]]"
    type: implements
    confidence: 0.8
  - target: "[[Compound Components]]"
    type: extends
    confidence: 0.7
supersedes: null
---

# Composition Patterns Skill

## 概述
[[Vercel Agent Skills]] 中的组件架构[[Skills|技能]]，专注于解决 [[Boolean Props 地狱]]问题，推广复合组件和其他高级组合模式。

## 关键内容

1. **核心问题**：解决具有大量布尔属性的 [[React]] 组件设计问题，如 is[[上下文压缩（Context Compaction）|Compact]], showHeader, isRounded, hasBorder 等

2. **主要模式**：
   - **Compound Components**：自描述、可组合的组件结构
   - **Context Providers**：替代 Props Drilling 的状态传递
   - **显式 [[Hal Varian|Varian]]ts**：用 variant 替代多个 boolean 开关

3. **实施方法**：通过将组件拆分为多个子组件（如 Card.Body、Card.Content、Card.Footer）来构建灵活的 UI

## 来源
- [[05_vercel_agent_skills_react.md]] — Vercel Agent Skills React 系列深度解析

## 相关
- [[Vercel Agent Skills]] — part_of
- [[React]] — implements
- [[Compound Components]] — extends