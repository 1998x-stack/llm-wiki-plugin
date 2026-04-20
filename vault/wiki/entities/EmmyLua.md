---
type: entity
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["LSP", "类型定义", "Lua", "IDE", "代码补全"]
aliases: [EmmyLua LSP, EmmyLua类型系统, .d.lua]
relates_to: [UrhoX引擎, Lua类型标注规范]
supersedes: null
---

# EmmyLua

## 概述
EmmyLua 是 Lua 语言的 Language Server Protocol 实现，提供类型定义、代码补全、错误检查等功能。[[UrhoX引擎|UrhoX]] 使用 `.emmylua/` 目录存放 LSP 类型定义。

## 关键内容
1. **在 UrhoX 中的使用**：`.emmylua/` 目录包含 `*.d.lua` 类型定义文件和 `Events.d.lua` 事件类型定义（177 个事件），LSP 自动加载，通常不需手动阅读。
2. **类型标注配合**：`.emmylua/` 已提供足够的全局类型声明，用户只需为未赋值或赋 nil 的变量添加 `---@type` 标注，后续类型推导将自动传递。
3. **LSP 报错预防**：未添加类型标注的 nil 变量访问成员时，LSP 报 `undefined-field` 错误；标注后获得完整的代码补全和类型检查。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #11

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[Lua类型标注规范]] — relates_to（类型标注的来源和配合方式）
