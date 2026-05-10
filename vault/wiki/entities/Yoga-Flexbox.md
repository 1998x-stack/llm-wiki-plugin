---
type: entity
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["布局引擎", "Flexbox", "CSS", "UI", "跨平台"]
aliases: [Yoga布局引擎, Yoga Layout, Facebook Yoga]
relates_to: [UI系统选择规范, UrhoX引擎]
supersedes: null
---

# Yoga-Flexbox

## 概述
Yoga 是一个跨平台的 Flexbox 布局引擎，最初由 Facebook 开发。[[UrhoX引擎|UrhoX]] 的新 UI 系统（urhox-libs/UI）基于 Yoga 实现 Flexbox 布局。

## 关键内容
1. **在 UrhoX 中的集成**：新 UI 系统使用 Yoga 实现 Flexbox 布局，支持 `justifyContent`、`alignItems`、`flexDirection` 等标准 CSS Flexbox 属性。
2. **常见陷阱**：Yoga 默认 `flexShrink=0`，子元素溢出容器时需手动设置 `flexShrink = 1`。
3. **使用方式**：通过 `urhox-libs/UI` 高层封装使用，如 `UI.Panel { justifyContent = "center", alignItems = "center", children = {...} }`。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #10

## 相关
- [[UI系统选择规范]] — relates_to（Yoga 是新 UI 系统的布局引擎）
- [[UrhoX引擎]] — relates_to（宿主引擎）
