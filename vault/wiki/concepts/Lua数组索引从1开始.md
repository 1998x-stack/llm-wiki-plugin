---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Lua, 数组, 索引, UrhoX, 陷阱, 游戏开发, Lua编程]
aliases: [Lua 1-based索引, Lua数组索引, 1-based indexing]
relates_to: [UrhoX引擎, table-unpack表构造器陷阱]
supersedes: null
---

# Lua数组索引从1开始

## 概述
Lua 数组索引从 1 开始而非 0，这是 Lua 语言的核心设计，在 [[UrhoX引擎|UrhoX]] 开发中极易引发 `attempt to index a nil value` 错误。

## 关键内容
1. **循环写法**：`for i = 1, n do` 是正确的遍历方式，不是 `for i = 0, n-1 do`。边界[[计算]]时用 `math.max(1, index)` 确保索引 >= 1。
2. **典型错误**：`array[0]` 在 Lua 中不存在，返回 `nil`，后续访问会触发 `attempt to index a nil value` 错误。这是从 JavaScript/[[Python]]/C 转 Lua 最常见的陷阱。
3. **与 table.unpack 的关系**：`table.unpack()` 返回的元素索引同样从 1 开始，在表构造器中展开时需注意位置（只在最后位置才能完全展开）。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #4

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[table-unpack表构造器陷阱]] — relates_to（同为 Lua 表操作陷阱）
