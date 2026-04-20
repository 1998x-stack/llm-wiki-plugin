---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["NanoVG", "字体", "显存泄漏", "UrhoX", "渲染"]
aliases: [NanoVG字体创建, nvgCreateFont规范, 字体句柄复用]
relates_to: [NanoVG, NanoVG渲染事件模式, Emoji自动Fallback]
supersedes: null
---

# NanoVG字体创建规范

## 概述
[[NanoVG]] 文本绘制前必须先创建字体，`nvgCreateFont` 只在初始化时调用一次，返回的句柄可每帧复用，每帧调用会导致显存泄漏。

## 关键内容
1. **初始化时创建**：在 `Start()` 中调用 `fontNormal = nvgCreateFont(vg, "sans", "Fonts/MiSans-Regular.ttf")`，只执行一次。返回值是字体句柄，可全局复用。
2. **渲染时使用**：每帧绘制时先设置字体 `nvgFontFace(vg, "sans")`，再设置字号 `nvgFontSize(vg, 24)`，最后绘制文本 `nvgText(vg, 100, 100, "Hello World")`。
3. **显存泄漏警告**：`nvgCreateFont` 每帧调用会导致显存持续增长，最终崩溃。这是 NanoVG 最常见的性能陷阱之一。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #7

## 相关
- [[NanoVG]] — relates_to（渲染库）
- [[NanoVG渲染事件模式]] — relates_to（字体创建是渲染流程的前置步骤）
- [[Emoji自动Fallback]] — relates_to（同为 NanoVG 文本渲染相关规范）
