---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, 模块化, Lua编程]
aliases: [Lua模块, Lua require机制, Lua模块加载]
relates_to:
  - target: "[[Lua-table]]"
    type: depends_on
    confidence: 0.95
  - target: "[[Lua-OOP]]"
    type: extends
    confidence: 0.85
  - target: "[[Lua-metatable]]"
    type: uses
    confidence: 0.7
supersedes: null
---
# Lua 模块系统

## 概述
Lua 模块是一个返回 table 的 `.lua` 文件；`require` 负责查找、执行并缓存该模块，同一模块只加载一次。

## 关键内容

### 模块基本模式
最常见写法：创建局部表，将函数和常量填入，最后 `return M`。

```lua
-- mymath.lua
local M = {}

function M.add(a, b) return a + b end
function M.sub(a, b) return a - b end

return M
```

使用时：
```lua
local mymath = require("mymath")
print(mymath.add(3, 4))  -- 7
```

### require 的执行流程
1. **查找**：按 `package.path` 搜索文件。`require("a.b.c")` 会尝试 `a/b/c.lua` 和 `a/b/c/init.lua`（取决于 `package.path` 配置）。
2. **执行**：找到后执行 `.lua` 文件。
3. **缓存**：结果存入 `package.loaded`，同一模块名第二次调用直接返回缓存值（`a == b` 为 true）。

### require vs dofile
| | `require` | `dofile` |
|--|--|--|
| 缓存 | 是（`package.loaded`） | 否，每次重新执行 |
| 路径查找 | 是（`package.path`） | 直接指定文件路径 |
| 用途 | 模块加载 | 脚本执行 |

### 路径写法
目录层级用 `.` 表示，不写 `.lua` 后缀：
```lua
-- lib/mathutil.lua 对应：
local mathutil = require("lib.mathutil")  -- 正确
require("lib/mathutil.lua")              -- 通常不这么写
```

### 类风格模块
模块可以返回"类"，结合 metatable 实现 OOP：
```lua
-- player.lua
local Player = {}
Player.__index = Player

function Player.new(name, hp)
    return setmetatable({name=name, hp=hp or 100}, Player)
end

function Player:take_damage(dmg) self.hp = self.hp - dmg end

return Player
```

### 强制重新加载
清除缓存后再 require 可重新执行模块文件：
```lua
package.loaded["testmod"] = nil
local m = require("testmod")
```

## 常见陷阱
1. **模块未 return**：`require` 返回值不是预期的 table（返回 true 或 nil）。
2. **路径与名称不匹配**：文件在 `lib/mathutil.lua` 却 `require("mathutil")`，找不到模块。
3. **循环 require**：A require B，B require A，模块初始化阶段互相依赖易出问题。

## 历史写法
`module(...)` 是老 Lua 的模块写法，现已不推荐。当前惯用 `local M = {}; ...; return M`。

## 来源
- [[Lua 模块与 require]] — ChatGPT 对话，Lua 模块系统与 require 机制全面解析

## 相关
- [[Lua-table]] — 模块通常以 table 作为导出容器
- [[Lua-OOP]] — 类风格模块依赖 metatable + table 实现
- [[Lua-metatable]] — `__index` 元方法是类风格模块的基础
