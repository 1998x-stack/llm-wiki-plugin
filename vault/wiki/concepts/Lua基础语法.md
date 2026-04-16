---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, Lua编程]
aliases: [Lua语法, Lua变量, Lua数据类型, Lua运算符]
relates_to:
  - target: "[[Lua作用域与local]]"
    type: extends
    confidence: 0.9
  - target: "[[Lua函数与多返回值]]"
    type: extends
    confidence: 0.85
  - target: "[[Lua-table]]"
    type: extends
    confidence: 0.9
supersedes: null
---
# Lua 基础语法

## 概述
Lua 是动态类型脚本语言，有 8 种基本类型，变量无需声明类型，推荐使用 local 局部变量避免全局污染。

## 关键内容

### 数据类型
Lua 有 8 种基本类型：`nil`、`boolean`、`number`、`string`、`table`、`function`、`thread`（协程）、`userdata`。
```lua
local a = nil          -- nil（空值）
local b = true         -- boolean
local c = 42           -- number（整数与浮点统一为 number）
local d = 3.14         -- number
local e = "hello"      -- string
local f = {}           -- table
local g = print        -- function
print(type(c))         -- "number"
```

### 变量
Lua 变量不需要声明类型，直接赋值即可。支持多重赋值：
```lua
a, b, c = 1, 2, 3      -- 同时赋三个值
a, b = b, a            -- 交换两个变量（原生支持）
```
未赋值的变量值为 `nil`。全局变量自动进入 `_G` 表。

### 字符串
```lua
local s1 = "hello"
local s2 = 'world'
local s3 = [[
多行字符串，
可以跨行。
]]
-- 拼接用 ..，不是 +
print("Hello, " .. "Lua")  -- Hello, Lua
-- 长度用 #
print(#"abc")   -- 3
```

### 运算符

| 类别 | 运算符 |
|------|--------|
| 算术 | `+` `-` `*` `/` `%` `^` `//`（整除，Lua 5.3+） |
| 比较 | `==` `~=`（不等于）`>` `<` `>=` `<=` |
| 逻辑 | `and` `or` `not` |
| 字符串 | `..`（拼接）`#`（长度） |

注意：Lua 不等于是 `~=`，不是 `!=`。

### 逻辑运算短路
`and` 和 `or` 返回操作数本身，不一定是布尔值：
```lua
print(1 and 2)    -- 2（and：左真则返回右）
print(nil and 2)  -- nil（and：左假则返回左）
print(1 or 2)     -- 1（or：左真则返回左）
print(nil or 2)   -- 2（or：左假则返回右）
-- 惯用法：默认值
local x = input or "default"
```

### 注释
```lua
-- 单行注释

--[[
多行注释
可以跨越多行
]]
```

### 常用类型转换
```lua
tonumber("123")     -- 123（字符串转数字，失败返回 nil）
tostring(42)        -- "42"（数字转字符串）
```

## 与其他语言的差异
| 特性 | Lua | 其他语言 |
|------|-----|---------|
| 数组起始索引 | 1 | 0（C/Java/Python） |
| 不等于符号 | `~=` | `!=` |
| 字符串拼接 | `..` | `+`（Python/JS） |
| 逻辑 AND/OR | `and` `or` | `&&` `\|\|` |
| 无三元运算符 | 用 `a and b or c` 模拟 | `a ? b : c` |

## 来源
- [[Lua 语法教程]] — ChatGPT 对话，Lua 初级语法教程，涵盖变量、类型、运算符与字符串 (https://chatgpt.com/c/69d65bb9-90a8-8321-bc95-04e5a304d9b7)

## 相关
- [[Lua作用域与local]] — 变量的作用域规则与 local 关键字
- [[Lua函数与多返回值]] — 函数是 Lua 的一等公民
- [[Lua-table]] — Lua 唯一复合数据结构，承载数组、字典、对象等所有复合语义
- [[Lua控制流]] — 基于基础语法的条件与循环结构
