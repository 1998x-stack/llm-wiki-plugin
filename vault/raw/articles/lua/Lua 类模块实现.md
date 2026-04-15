---
title: "Lua 类模块实现"
source: "https://chatgpt.com/c/69d65f8d-e598-8321-ae0e-3bdac4d090d2"
author:
published:
created: 2026-04-08
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
在 Lua 里，“类模块”通常就是：

1. **一个模块文件**
2. **返回一张表**
3. 这张表既充当“类”，也作为实例的方法集合
4. 用 `__index` 和 `setmetatable` 模拟面向对象

最常见写法如下。

## 基本写法

### Player.lua

```markdown
local Player = {}
Player.__index = Player

function Player.new(name, hp)
    local self = setmetatable({}, Player)
    self.name = name or "Unknown"
    self.hp = hp or 100
    return self
end

function Player:attack(target)
    print(self.name .. " attacks " .. target.name)
end

function Player:getHP()
    return self.hp
end

return Player
```

### 使用

```markdown
local Player = require("Player")

local p1 = Player.new("Alice", 100)
local p2 = Player.new("Bob", 80)

p1:attack(p2)
print(p1:getHP())
```

---

## 这其实在做什么

`Player` 这张表有两个角色：

- **模块导出的对象**
- **类的方法表**

这一句最关键：

```markdown
Player.__index = Player
```

意思是实例查不到字段时，就去 `Player` 表里找方法。

这一句把实例和类关联起来：

```markdown
local self = setmetatable({}, Player)
```

于是 `self:attack()` 就能找到 `Player.attack` 。

---

## 为什么方法常写成:

例如：

```markdown
function Player:attack(target)
```

等价于：

```markdown
function Player.attack(self, target)
```

调用：

```markdown
p1:attack(p2)
```

等价于：

```markdown
p1.attack(p1, p2)
```

所以：

- **定义实例方法** ，一般用 `:`
- **调用实例方法** ，也一般用 `:`
- **构造函数** 常用 `.`，如 `Player.new(...)`

---

## 更像“类”的写法

有的人喜欢把构造函数也写成冒号风格：

```markdown
local Player = {}
Player.__index = Player

function Player:new(name, hp)
    local obj = setmetatable({}, self)
    obj.name = name or "Unknown"
    obj.hp = hp or 100
    return obj
end

function Player:attack(target)
    print(self.name .. " attacks " .. target.name)
end

return Player
```

使用：

```markdown
local Player = require("Player")
local p1 = Player:new("Alice", 100)
```

这个写法对继承更友好，因为这里的 `self` 可以是子类表。

---

## 带私有辅助函数的类模块

模块里还可以放“不导出”的局部函数：

```markdown
local Player = {}
Player.__index = Player

local function clamp(v, min, max)
    if v < min then return min end
    if v > max then return max end
    return v
end

function Player.new(name, hp)
    local self = setmetatable({}, Player)
    self.name = name or "Unknown"
    self.hp = clamp(hp or 100, 0, 999)
    return self
end

function Player:takeDamage(dmg)
    self.hp = clamp(self.hp - dmg, 0, 999)
end

return Player
```

`clamp` 就像模块内部私有方法，外面拿不到。

---

## 加“静态方法”也很常见

所谓静态方法，本质上就是挂在类表上的普通函数：

```markdown
local Player = {}
Player.__index = Player

function Player.new(name, hp)
    local self = setmetatable({}, Player)
    self.name = name or "Unknown"
    self.hp = hp or 100
    return self
end

function Player.isPlayer(obj)
    return getmetatable(obj) == Player
end

return Player
```

使用：

```markdown
local p = Player.new("Alice", 100)
print(Player.isPlayer(p))  -- true
```

---

## 简单继承写法

### Animal.lua

```markdown
local Animal = {}
Animal.__index = Animal

function Animal:new(name)
    local obj = setmetatable({}, self)
    self.__index = self
    obj.name = name or "Animal"
    return obj
end

function Animal:speak()
    print(self.name .. " makes a sound")
end

return Animal
```

### Dog.lua

```markdown
local Animal = require("Animal")

local Dog = setmetatable({}, { __index = Animal })
Dog.__index = Dog

function Dog:new(name, breed)
    local obj = Animal.new(self, name)
    obj.breed = breed or "Unknown"
    return obj
end

function Dog:speak()
    print(self.name .. " barks")
end

return Dog
```

### 使用

```markdown
local Dog = require("Dog")

local d = Dog:new("Buddy", "Golden Retriever")
d:speak()
```

---

## 更实用的推荐模板

如果你只是想稳定地写“类模块”，我建议直接用这个模板：

```markdown
local ClassName = {}
ClassName.__index = ClassName

function ClassName:new(...)
    local obj = setmetatable({}, self)
    return obj
end

return ClassName
```

然后按需扩展：

```markdown
local User = {}
User.__index = User

function User:new(name, age)
    local obj = setmetatable({}, self)
    obj.name = name or ""
    obj.age = age or 0
    return obj
end

function User:getName()
    return self.name
end

function User:setName(name)
    self.name = name
end

return User
```

---

## 常见坑

### 1\. 忘了写 \_\_index

如果没有：

```markdown
User.__index = User
```

实例找不到类里的方法。

### 2.: 和. 混用错了

比如定义：

```markdown
function User:getName()
```

调用就要：

```markdown
u:getName()
```

不要写成：

```markdown
u.getName()
```

否则 `self` 不会自动传进去。

### 3\. require 返回的是类表，不是实例

```markdown
local User = require("User")
```

这里拿到的是“类模块表”，还得自己 `User:new(...)` 或 `User.new(...)` 。

---

## 一句话理解

Lua 没有内建 class，所谓“类模块”就是：

**用一个模块返回一张表，把方法放在这张表上，再用 metatable 让实例去这个表上找方法。**

如果你愿意，我可以接着给你一份：

- **最简类模块模板**
- **支持继承的模板**
- **适合游戏项目的 Lua OOP 模板**