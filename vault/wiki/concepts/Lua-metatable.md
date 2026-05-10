---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [Lua, 编程语言, 元编程, Lua编程]
aliases: [Lua元表, Lua元方法, metamethod]
relates_to: [Lua-table, Lua-OOP, lua-language-server]
supersedes: null
---
# Lua metatable

## 概述
Lua 通过 metatable 机制允许对 table 的行为进行拦截和重定义，是实现 OOP、运算符重载、原型继承的基础。

## 关键内容
1. **[[Settings|设置]]与获取**：`setmetatable(t, mt)` 为 table `t` 指定 metatable `mt`；`getmetatable(t)` 取回。每个 table 最多关联一个 metatable。
2. **`__index` 元方法**：访问 table 中不存在的字段时触发。可以是函数 `function(tbl, key) ... end` 或另一张 table（原型查找）。原型链继承即利用此机制：`setmetatable(t, {__index = proto})`，访问 `t` 中不存在的字段时自动在 `proto` 中查找。
3. **`__newindex` 元方法**：对不存在的字段赋值时触发，可用于只读 table 或代理写入。
4. **运算符重载**：`__add`/`__sub`/`__mul`/`__div`/`__mod`/`__unm`（一元负）等对应算术操作；`__eq`/`__lt`/`__le` 对应比较操作。
5. **其他元方法**：`__tostring`（`tostring()` 时触发）、`__len`（`#` 运算符）、`__call`（table 当函数调用）、`__concat`（`..` 拼接）。
6. **经典用法——默认值**：`setmetatable(t, {__index = function(_, k) return 0 end})` 使任意未定义字段返回默认值 0。
7. **注意**：metatable 的 `__index` 查找只对"不存在的 key"触发，已存在的 key 直接返回，不经过 metatable。

## 来源
- [[Lua table 深入解析]] — ChatGPT 对话，详解 metatable 机制及 __index 两种写法

## 相关
- [[Lua-table]] — metatable 依附于 table 使用
- [[Lua-OOP]] — metatable 是 Lua OOP 的实现基础
