---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["Lua", "类型标注", "EmmyLua", "LSP", "UrhoX", "代码质量"]
aliases: [Lua类型注解, EmmyLua标注, 类型声明]
relates_to: [UrhoX引擎, EmmyLua]
supersedes: null
---

# Lua类型标注规范

## 概述
[[UrhoX引擎|UrhoX]] Lua 开发中，未赋值或赋 nil 的变量必须添加 `---@type` 类型标注，否则 LSP 无法推导类型，访问成员时报 `undefined-field` 错误或无任何提示。

## 关键内容
1. **必须标注的场景**：`local scene = nil` 必须加 `---@type Scene`；`local node`（未赋值）必须加 `---@type Node`。来自全局接口的调用（如 `local scene = Scene()`）自动传递类型推导，无需标注。
2. **事件函数标注**：建议为事件函数参数添加类型标注，如 `---@param eventType string` 和 `---@param eventData UpdateEventData`，完整事件类型定义见 `.emmylua/Events.d.lua`。
3. **类型源头**：`.emmylua/` 目录已提供足够的全局类型声明，用户只需标注空值变量，后续类型推导将自动传递。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #11

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[EmmyLua]] — relates_to（类型定义来源）
