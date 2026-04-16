---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, Lua编程]
aliases: [Lua局部变量, Lua作用域, Lua local关键字, Lua全局变量]
relates_to:
  - target: "[[Lua基础语法]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Lua函数与多返回值]]"
    type: extends
    confidence: 0.85
  - target: "[[Lua模块系统]]"
    type: extends
    confidence: 0.8
supersedes: null
---
# Lua 作用域与 local

## 概述
Lua 变量默认全局，加 `local` 限定为词法作用域；推荐所有变量和函数都用 local，避免全局表污染和命名冲突。

## 关键内容

### 全局变量 vs 局部变量
```lua
x = 10       -- 全局变量，存入 _G["x"]
local y = 20 -- 局部变量，只在当前作用域有效
```
全局变量存储在 Lua 的全局表 `_G` 中，任何地方都可访问和修改，容易造成命名冲突和难以追踪的 bug。

### 词法作用域
Lua 使用词法（静态）作用域，作用域由代码块决定：
```lua
local a = 10

do
    local b = 20
    print(a)  -- 10（可见，a 在外层作用域）
    print(b)  -- 20（可见，b 在当前块）
end

-- print(b)  -- 错误：b 超出作用域
```
代码块：`do...end`、`if...end`、`for...end`、`function...end` 都引入新的作用域。

### 为什么推荐用 local
1. **性能**：local 变量存储在寄存器（栈帧），访问比全局变量（哈希表查找 `_G`）快约 30%。
2. **安全**：不会污染全局命名空间，避免不同模块间的变量冲突。
3. **可维护**：作用域有限，变量生命周期清晰。

```lua
-- 不推荐
result = compute()  -- 全局

-- 推荐
local result = compute()  -- 局部
```

### 局部函数
函数也应声明为 local：
```lua
local function helper(x)
    return x * 2
end
```
注意：`local function f() end` 等价于 `local f; f = function() end`，因此在函数体内可以递归调用自身。

### 闭包与 upvalue
local 变量被内层函数捕获后成为 upvalue，即使外层作用域结束，upvalue 仍然存活：
```lua
local function makeAdder(n)
    return function(x)
        return x + n  -- n 是 upvalue
    end
end

local add5 = makeAdder(5)
print(add5(10))  -- 15
```
每次调用 `makeAdder` 创建独立的 `n`，各闭包互不干扰。

### 模块中的 local 惯用法
在模块文件中，所有内部实现函数用 local，只通过 return 导出公共接口：
```lua
local M = {}

local function privateHelper(x)  -- 不导出
    return x * 2
end

function M.publicFn(x)           -- 导出
    return privateHelper(x) + 1
end

return M
```

## 常见坑
- **循环变量自动是 local**：数值 `for` 的循环变量（如 `i`）自动是局部变量，无需加 `local`。
- **重复声明覆盖**：同一作用域内 `local x = 1; local x = 2` 创建了两个不同的 `x`，后者遮蔽前者。
- **upvalue 共享**：多个闭包捕获同一个 local 变量时，共享同一个 upvalue（修改会互相影响）。

## 来源
- [[Lua 语法教程]] — ChatGPT 对话，Lua 初级语法教程，涵盖 local 变量与作用域规则 (https://chatgpt.com/c/69d65bb9-90a8-8321-bc95-04e5a304d9b7)

## 相关
- [[Lua基础语法]] — 变量声明和类型是作用域讨论的基础
- [[Lua函数与多返回值]] — 闭包是 local 变量与函数结合的核心特性
- [[Lua模块系统]] — 模块惯用法大量依赖 local 隔离实现细节
