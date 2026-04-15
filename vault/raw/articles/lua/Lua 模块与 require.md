---
title: "Lua 模块与 require"
source: "https://chatgpt.com/c/69d65d20-9bf0-8320-9955-c04a83697793"
author:
published:
created: 2026-04-08
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
在 Lua 里， **模块** 就是一组可复用的代码，通常放在单独的 `.lua` 文件里； `require` 用来 **加载模块并返回它导出的内容** 。

## 1\. 最基本理解

比如你有一个文件：

```markdown
-- mymath.lua
local M = {}

function M.add(a, b)
    return a + b
end

function M.sub(a, b)
    return a - b
end

return M
```

然后在别的文件里：

```markdown
local mymath = require("mymath")

print(mymath.add(3, 4))  -- 7
print(mymath.sub(10, 2)) -- 8
```

这里：

- `mymath.lua` 是一个模块
- `require("mymath")` 会加载这个模块
- 模块最后 `return M` ，所以 `require` 的结果就是这个表

---

## 2\. 为什么模块通常返回一个 table

Lua 没有像别的语言那样强制的模块系统，最常见做法是：

- 创建一个表
- 把函数、常量放进去
- 最后 `return` 这个表

例如：

```markdown
local util = {}

util.VERSION = "1.0"

function util.hello(name)
    return "Hello, " .. name
end

return util
```

调用：

```markdown
local util = require("util")
print(util.VERSION)
print(util.hello("Lua"))
```

---

## 3\. require 做了什么

`require("mymath")` 大致会做几件事：

### 先找模块

它会按 `package.path` 去找 Lua 文件。

比如 `require("a.b.c")` ，通常会尝试找类似：

- `a/b/c.lua`
- `a/b/c/init.lua`

取决于 `package.path` 配置。

### 再执行模块文件

如果找到了，就执行这个 `.lua` 文件。

### 缓存结果

**同一个模块只会加载一次。**

```markdown
local a = require("mymath")
local b = require("mymath")

print(a == b)  -- true
```

因为 `require` 会把结果缓存到 `package.loaded` 里。

---

## 4\. require 和 dofile 的区别

### require

- 会缓存
- 会按模块路径查找
- 适合模块加载

### dofile

- 直接执行指定文件
- 每次都会重新执行
- 不做模块缓存

例子：

```markdown
dofile("mymath.lua")
```

这更像“执行脚本文件”，不是正规的模块加载。

---

## 5\. 模块文件路径怎么写

假设目录是：

```markdown
project/
  main.lua
  lib/
    mathutil.lua
```

`main.lua` 里可以这样：

```markdown
local mathutil = require("lib.mathutil")
```

注意：

- 用 `.` 表示目录层级
- 不写 `.lua`

不是：

```markdown
require("lib/mathutil.lua") -- 通常不这么写
```

---

## 6\. 一个更完整的模块例子

```markdown
-- player.lua
local Player = {}
Player.__index = Player

function Player.new(name, hp)
    local self = setmetatable({}, Player)
    self.name = name
    self.hp = hp or 100
    return self
end

function Player:take_damage(dmg)
    self.hp = self.hp - dmg
end

function Player:is_dead()
    return self.hp <= 0
end

return Player
```

使用：

```markdown
local Player = require("player")

local p = Player.new("Hero", 120)
p:take_damage(30)

print(p.hp)         -- 90
print(p:is_dead())  -- false
```

这说明模块不一定只是“工具函数集合”，也可以返回一个“类风格”的表。

---

## 7\. require 只执行一次这一点很重要

看这个例子：

```markdown
-- testmod.lua
print("loading testmod")

local M = {}
return M
```
```markdown
local a = require("testmod")
local b = require("testmod")
```

输出只会有一次：

```markdown
loading testmod
```

因为第二次直接从缓存里拿。

如果你真的想重新加载，可以手动清掉缓存：

```markdown
package.loaded["testmod"] = nil
local m = require("testmod")
```

---

## 8\. 常见错误

### 模块没 return

比如：

```markdown
-- badmod.lua
local M = {}
function M.x() end
```

然后：

```markdown
local m = require("badmod")
print(m)  -- 可能不是你想要的结果
```

通常模块应该显式：

```markdown
return M
```

### require 名称和文件路径不匹配

比如文件在 `lib/mathutil.lua` ，却写成：

```markdown
require("mathutil")
```

那可能找不到。

### 循环 require

A require B，B 又 require A，容易出问题，尤其在模块初始化阶段互相依赖时。

---

## 9\. 老式写法和新式写法

老 Lua 里有过 `module(...)` 这种写法，但现在一般 **不推荐** 。

现在更常见、更清晰的是这种：

```markdown
local M = {}

function M.foo()
end

return M
```

---

## 10\. 一句话总结

- **模块** ：一个返回 table 的 Lua 文件
- **require** ：查找、执行并缓存模块
- **最常见模式** ： `local M = {}; ...; return M`

你要是愿意，我可以接着给你讲：

1. `package.path` 和模块搜索路径
2. Lua 里如何写“类模块”
3. OpenResty / LuaJIT 里的 `require` 行为和普通 Lua 的区别