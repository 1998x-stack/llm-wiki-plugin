---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, Lua编程]
aliases: [Lua循环, Lua条件语句, Lua if, Lua for, Lua while]
relates_to:
  - target: "[[Lua基础语法]]"
    type: depends_on
    confidence: 0.95
  - target: "[[Lua-table]]"
    type: uses
    confidence: 0.8
  - target: "[[Lua函数与多返回值]]"
    type: uses
    confidence: 0.7
supersedes: null
---
# Lua 控制流

## 概述
Lua 提供 if/elseif/else 条件语句和三种循环（while、for 数值/泛型、repeat-until），配合 break 控制流程。

## 关键内容

### 条件语句
```lua
local score = 85

if score >= 90 then
    print("优秀")
elseif score >= 60 then
    print("及格")
else
    print("不及格")
end
```
注意：`then` 和 `end` 是必须的关键字；Lua 没有 `switch/case`，用 `elseif` 链或 table dispatch 模拟。

### while 循环
当条件为真时持续执行：
```lua
local i = 1
while i <= 5 do
    print(i)
    i = i + 1
end
```

### 数值 for 循环
`for var = start, stop, step do`，step 默认为 1，可为负数：
```lua
for i = 1, 5 do print(i) end         -- 1 2 3 4 5
for i = 10, 1, -1 do print(i) end    -- 10 9 ... 1
for i = 1, 10, 2 do print(i) end     -- 1 3 5 7 9
```
循环变量 `i` 是局部的，循环内修改 `i` 无效（Lua 内部使用独立变量控制步进）。

### 泛型 for 循环
配合迭代器函数遍历 table：
```lua
-- ipairs：从 1 开始，遇 nil 停止，适合数组
local arr = {10, 20, 30}
for i, v in ipairs(arr) do
    print(i, v)
end

-- pairs：遍历所有键值，顺序不确定，适合字典
local user = {name = "Tom", age = 18}
for k, v in pairs(user) do
    print(k, v)
end
```

### repeat-until 循环
至少执行一次，直到条件为真才退出（与 while 相反）：
```lua
local i = 1
repeat
    print(i)
    i = i + 1
until i > 5
```
`until` 条件中可访问循环体内定义的 local 变量（这是 Lua 的特殊设计，其他语言少见）。

### break
退出最内层循环，Lua 没有 `continue`（跳过当前迭代），可用反向条件或 `goto` 模拟：
```lua
for i = 1, 10 do
    if i == 5 then break end
    print(i)
end
```

### goto（Lua 5.2+）
`goto label` 可跳转到同一函数内的标签，常用于模拟 `continue`：
```lua
for i = 1, 10 do
    if i % 2 == 0 then goto continue end
    print(i)  -- 只打印奇数
    ::continue::
end
```

### Table dispatch（替代 switch）
用 table 存储处理函数，替代长 `elseif` 链：
```lua
local handlers = {
    ["start"] = function() print("开始") end,
    ["stop"]  = function() print("停止") end,
}
local action = "start"
local fn = handlers[action]
if fn then fn() end
```

## 常见坑
- **忘记 `then` 或 `do`**：`if ... then`、`for ... do`、`while ... do` 都需要这些关键字。
- **无 `continue`**：Lua 5.1 没有 continue，需用 goto（5.2+）或反向 if 条件。
- **数值 for 循环变量只读**：循环内修改 `i` 不影响步进，不要依赖它控制循环。
- **`ipairs` 遇 nil 停止**：稀疏数组用 `ipairs` 会提前终止，应用 `pairs` 或数字 for + `#`。

## 来源
- [[Lua 语法教程]] — ChatGPT 对话，Lua 初级语法教程，涵盖 if/while/for/repeat 等控制结构 (https://chatgpt.com/c/69d65bb9-90a8-8321-bc95-04e5a304d9b7)

## 相关
- [[Lua基础语法]] — 控制流依赖的变量、类型和运算符基础
- [[Lua-table]] — 泛型 for 配合 table 迭代是 Lua 最常见的遍历模式
- [[Lua函数与多返回值]] — 迭代器本质是返回多值的函数
