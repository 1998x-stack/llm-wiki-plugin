---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["UI系统", "UrhoX", "Yoga", "Flexbox", "NanoVG", "废弃API"]
aliases: [新UI系统, urhox-libs/UI, 原生UI废弃]
relates_to: [UrhoX引擎, NanoVG, NanoVG渲染事件模式]
supersedes: null
---

# UI系统选择规范

## 概述
[[UrhoX引擎|UrhoX]] 有两套 UI 系统，原生 UI（Urho3D UIElement）已废弃，必须使用新 UI 系统（urhox-libs/UI，基于 Yoga Flexbox + NanoVG）。

## 关键内容
1. **新 UI 系统**：`urhox-libs/UI`，基于 Yoga Flexbox 布局引擎和 NanoVG 渲染，提供 40+ 内置控件（Panel、Label、Button、Slider 等），通过 `UI.Init()` 初始化，`UI.SetRoot()` 设置根节点。
2. **原生 UI 系统**：基于 Urho3D UIElement，已标记为废弃，仅用于兼容旧代码，不再维护。新项目不应使用。
3. **选择原则**：文字、按钮、HUD、菜单、字幕 → `urhox-libs/UI` 组件；自定义图形、粒子、图表、特殊效果 → raw [[NanoVG]]；不确定时先查 `urhox-libs/UI` 组件列表，无对应组件再用 NanoVG。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #10

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[NanoVG]] — relates_to（新 UI 系统的渲染层）
- [[NanoVG渲染事件模式]] — relates_to（区分 raw NanoVG 与 UI 组件的使用场景）
