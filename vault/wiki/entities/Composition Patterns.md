---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [React, Architecture, Components, AI工程]
aliases: ["composition-patterns", "React Composition Patterns"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相關頁面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Composition Patterns

## 概述
[[Vercel]] 提供的 [[React]] 組件組合模式[[Skills|技能]]，旨在解決 Boolean Props 地獄問題，建立可擴展的組件架構。

## 關鍵內容

1. **核心問題**：解決具有大量布爾屬性的組件設計問題
   - 避免 `isCompact`, `showHeader`, `isRounded`, `hasBorder` 等布爾參數氾濫

2. **主要模式**：
   - **Compound Components**：自描述、可組合的組件結構
   - **Context Providers**：替代 Props Drilling
   - **顯式 [[Hal Varian|Varian]]ts**：替代布爾開關

3. **實現技術**：
   - 使用 `cva` (class-variance-authority) 進行變體管理
   - 組件嵌套結構（如 `Card.Body`, `Card.Content`, `Card.Footer`）

## 來源
- [[raw/articles/ai-tools/claude-skills/05_vercel_agent_skills_react.md]] — 深度解析

## 相關
- [[Vercel Agent Skills]] — 所屬集合
- [[React]] — 技術棧
- [[Component Architecture]] — 架構概念