---
type: entity
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Lua绑定, C++, tolua, UrhoX, Lua-C互操作, Lua编程]
aliases: [tolua++, tolua绑定, tolua++绑定系统]
relates_to: [UrhoX引擎, Lua-eventData访问模式]
supersedes: null
---

# tolua++

## 概述
[[Lua脚本宿主模式|tolua]]++ 是一个将 C++ 类绑定到 Lua 的自动绑定工具，[[UrhoX引擎|UrhoX]] 的事件系统（eventData 访问）基于 [[Lua脚本宿主模式|tolua]]++ 绑定实现。

## 关键内容
1. **在 [[UrhoX引擎|UrhoX]] 中的作用**：[[Lua脚本宿主模式|tolua]]++ 绑定使得 C++ 事件数据可以通过 Lua 访问，但返回的是包装对象而非原生 Lua 值，需要调用 `GetInt()`/`GetFloat()` 等方法进行类型转换。
2. **访问模式**：`eventData["X"]:GetInt()` 或 `eventData:GetInt("X")`，后者更高效。这是 [[Lua脚本宿主模式|tolua]]++ 绑定的特定访问方式。
3. **类型定义**：绑定信息反映在 `.emmylua/Events.d.lua` 中，定义了 177 个事件的事件数据结构。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #3

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[Lua-eventData访问模式]] — relates_to（tolua++ 绑定的直接体现）
