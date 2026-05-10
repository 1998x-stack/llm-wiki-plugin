---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["Lua", "事件系统", "tolua++", "UrhoX", "数据访问"]
aliases: [eventData访问, tolua++事件数据, 事件参数访问]
relates_to: [UrhoX引擎, Luau]
supersedes: null
---

# Lua-eventData访问模式

## 概述
[[UrhoX引擎|UrhoX]] 基于 tolua++ 绑定的事件系统中，`eventData` 的访问需要使用类型转换方法（`GetInt()`/`GetFloat()` 等），支持索引和键名两种调用方式。

## 关键内容
1. **三种正确访问方式**：`eventData["X"]:GetInt()`（索引+类型方法）；`eventData["TimeStep"]:GetFloat()`（索引+类型方法）；`eventData:GetInt("X")`（键名+类型方法，更高效）。
2. **常用事件字段**：`TimeStep`（delta time，用 `GetFloat()`）；`X`/`Y` 等坐标值（用 `GetInt()` 或 `GetFloat()`）。完整事件字段定义见 `.emmylua/Events.d.lua`。
3. **常见错误**：直接访问 `eventData["X"]` 返回的是 tolua++ 包装对象，不是原生 Lua 值，必须调用类型转换方法。错误用法会导致 `attempt to call method 'GetInt'` 或类型不匹配。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #3

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[Luau]] — relates_to（Lua 方言变体）
