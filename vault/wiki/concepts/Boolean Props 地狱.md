---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [react, architecture, design-patterns, AI设计]
aliases: ["Boolean Props Hell", "Boolean Props地狱", "Props地狱"]
relates_to:
  - target: "[[Composition Patterns Skill]]"
    type: implements
    confidence: 0.8
  - target: "[[React Component Design]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Compound Components]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Boolean Props 地狱

## 概述
[[React]] 组件设计中的反模式，指组件接受过多布尔类型属性导致接口复杂、难以维护的问题。

## 关键内容

1. **症状表现**：组件拥有大量的布尔参数，如 is[[上下文压缩（Context Compaction）|Compact]]、showHeader、isRounded、hasBorder、isHighlighted 等

2. **负面影响**：
   - 组件接口变得冗长复杂
   - 组合爆炸导致测试困难
   - 代码可读性和[[可维护性]]下降
   - 组件扩展性差

3. **解决方案**：
   - 使用 Compound Components 模式
   - 采用 Context Provider 替代 Props Drilling
   - 使用显式 [[Hal Varian|Varian]]ts 替代多个布尔开关
   - 应用组合模式构建灵活的 UI 组件

## 来源
- [[05_vercel_agent_skills_react.md]] — Vercel Agent Skills React 系列深度解析

## 相关
- [[Composition Patterns Skill]] — implements
- [[React Component Design]] — relates_to
- [[Compound Components]] — relates_to