---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["NanoVG", "渲染事件", "UrhoX", "矢量图形", "游戏开发"]
aliases: [NanoVGRender事件, NanoVG渲染回调, 矢量图形渲染事件]
relates_to: [NanoVG, NanoVG字体创建规范, UI系统选择规范]
supersedes: null
---

# NanoVG渲染事件模式

## 概述
[[UrhoX引擎|UrhoX]] 中 raw [[NanoVG]] 渲染必须订阅 `NanoVGRender` 事件，在回调中调用 `nvgBeginFrame`/`nvgEndFrame`，否则图形不会显示。

## 关键内容
1. **事件订阅**：在 `Start()` 中调用 `SubscribeToEvent("NanoVGRender", "HandleNanoVGRender")`。不使用 `Update` 或其他事件。
2. **渲染框架**：`HandleNanoVGRender(eventType, eventData)` 回调中，先调用 `nvgBeginFrame(vg, width, height, 1.0)`，执行绘制代码，最后调用 `nvgEndFrame(vg)` 完成一帧渲染。
3. **适用场景**：此模式仅适用于自定义矢量图形绘制（粒子、图表、特殊效果）。UI/HUD/字幕等通用界面应使用 `urhox-libs/UI` 组件，而非 raw NanoVG。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #6

## 相关
- [[NanoVG]] — relates_to（渲染库）
- [[NanoVG字体创建规范]] — relates_to（字体创建是 NanoVG 渲染的前置步骤）
- [[UI系统选择规范]] — relates_to（区分 NanoVG 与 UI 组件的使用场景）
