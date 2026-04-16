---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, Lua编程]
aliases: [Lua函数, Lua多返回值, Lua first-class function]
relates_to:
  - target: "[[Lua基础语法]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Lua作用域与local]]"
    type: extends
    confidence: 0.85
  - target: "[[Lua-table]]"
    type: uses
    confidence: 0.7
supersedes: null
---
# Lua 函数与多返回值

## 概述
Lua 函数是一等公民，支持多返回值、可变参数与闭包，是构建模块和 OOP 的基础语法单元。

## 关键内容

### 函数定义与调用
```lua
-- 全局函数
function sayHello()
    print("Hello")
end

-- 局部函数（推荐）
local function add(a, b)
    return a + b
end

sayHello()
print(add(3, 5))  -- 8
```

### 多返回值
Lua 原生支持函数返回多个值，无需包装成 table：
```lua
function calc(a, b)
    return a + b, a - b
end

local x, y = calc(8, 3)
print(x, y)  -- 11  5
```

多余的返回值被丢弃，变量不足时补 `nil`：
```lua
local sum = calc(8, 3)   -- sum=11，第二个返回值被丢弃
local a, b, c = calc(8, 3)  -- c=nil
```

### 函数是一等公民
函数可以赋值给变量、作为参数传递、存入 table：
```lua
local ops = {
    add = function(a, b) return a + b end,
    sub = function(a, b) return a - b end,
}
print(ops.add(10, 3))  -- 13
```

### 可变参数
使用 `...` 接收可变参数，`select("#", ...)` 获取参数个数：
```lua
local function sum(...)
    local total = 0
    for _, v in ipairs({...}) do
        total = total + v
    end
    return total
end
print(sum(1, 2, 3, 4))  -- 10
```

### 闭包
函数捕获外层局部变量（upvalue），形成闭包：
```lua
local function makeCounter()
    local count = 0
    return function()
        count = count + 1
        return count
    end
end

local counter = makeCounter()
print(counter())  -- 1
print(counter())  -- 2
```

### 尾调用优化
Lua 支持尾调用优化（TCO）：形如 `return f(...)` 的调用不增加调用栈，适合递归算法。

### 冒号语法糖
在 OOP 场景下，`obj:method(x)` 是 `obj.method(obj, x)` 的语法糖，自动传入 `self`。详见 [[Lua-OOP]]。

## 常见坑
- **多返回值只在最后一个位置展开**：`local t = {calc(8,3), 100}` 中 `calc(8,3)` 只保留第一个返回值（11），结果为 `{11, 100}`。
- **忘记 `local`**：不加 `local` 的函数名会成为全局变量，污染全局命名空间。
- **`nil` 截断可变参数**：`...` 中含 `nil` 时 `ipairs({...})` 会在 nil 处停止；用 `select` 代替。

## 来源
- [[Lua 语法教程]] — ChatGPT 对话，Lua 初级语法教程，涵盖函数定义、多返回值与可变参数 (https://chatgpt.com/c/69d65bb9-90a8-8321-bc95-04e5a304d9b7)

## 相关
- [[Lua基础语法]] — 函数的基础语法环境（变量、类型、运算符）
- [[Lua作用域与local]] — 闭包依赖 local 变量的作用域规则
- [[Lua-OOP]] — 冒号语法糖与函数是 OOP 的语法基础
- [[Lua-table]] — 函数常存入 table 作为方法
