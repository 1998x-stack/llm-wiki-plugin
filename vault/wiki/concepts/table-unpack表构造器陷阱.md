---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Lua, table, unpack, 陷阱, UrhoX, 表构造器, Lua编程]
aliases: [table.unpack陷阱, unpack展开位置, Lua表构造器unpack]
relates_to: [Lua数组索引从1开始, Lua数据驱动设计]
supersedes: null
---

# table-unpack表构造器陷阱

## 概述
Lua 的 `table.unpack()` 只有在表构造器的最后位置才会完全展开所有元素，其他位置只取第一个值，这与 JavaScript `[...arr, x]` 或 [[Python]] `[*arr, x]` 的行为完全不同。

## 关键内容
1. **错误用法**：`{ table.unpack(items), "extra" }` 只展开第一个元素，结果为 `{1, "extra"}` 而非 `{1, 2, 3, "extra"}`。原因是 unpack 不在最后位置时，Lua 只取第一个返回值。
2. **正确用法**：`{ "header", table.unpack(items) }` 将 unpack 放在最后，结果为 `{"header", 1, 2, 3}`。unpack 必须是表构造器的最后一个元素才能完全展开。
3. **跨语言对比**：JavaScript 的 `[...arr, x]` 和 [[Python]] 的 `[*arr, x]` 可以在任意位置展开，但 Lua 不支持这种灵活性，需要特别注意。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #4.5

## 相关
- [[Lua数组索引从1开始]] — relates_to（同为 Lua 数组操作陷阱）
- [[Lua数据驱动设计]] — relates_to（数据驱动中常用表操作）
