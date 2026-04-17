---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 3
tags: [Lua, 编程语言, 面向对象, 设计模式, Lua编程]
aliases: [Lua面向对象, Lua类, Lua原型继承]
relates_to: [Lua-table, Lua-metatable, Lua模块系统, lua-language-server]
supersedes: null
---
# Lua OOP

## 概述
Lua 无内建 class 系统，通过 table + metatable + 冒号语法糖实现面向对象编程，核心是原型继承链。

## 关键内容
1. **冒号语法糖**：`obj:method(x)` 等价于 `obj.method(obj, x)`；定义时 `function T:foo(x)` 等价于 `function T.foo(self, x)`。冒号自动传入 `self`，是 Lua OOP 的语法基础。
2. **经典类模式**：将类本身既作命名空间又作 metatable，令 `Class.__index = Class`，实例通过 `setmetatable({}, Class)` 创建。实例访问不到的字段会沿 `__index` 链在 Class 上查找，实现方法共享。
3. **构造器约定**：通常写 `Class.new(...)` 而非 `Class:new(...)` 以避免多余的 self 参数。构造器内 `local self = setmetatable({}, Class)` 后设置实例字段并 return self。另一种风格是 `Class:new(...)` 使 `self` 可以是子类，对继承更友好。
4. **私有辅助函数**：模块内用 `local function helper(...)` 声明的函数外部无法访问，起到私有方法作用。如 `local function clamp(v, min, max)` 在模块内部使用，不随 return 导出。
5. **静态方法**：直接挂在类表上的普通函数（用 `.` 定义），不接受 self，常用于工厂方法和类型检查，如 `Class.isInstance(obj)`。
6. **继承扩展**：子类可设 `Child.__index = Child`，并令 `setmetatable(Child, {__index = Parent})`，形成两级原型链——实例 → 子类 → 父类。子类构造器调用 `Parent.new(self, ...)` 复用父类初始化逻辑。
7. **局限性**：无访问控制（无 private/protected），无多态类型检查，需手动维护继承链。实践中常借助闭包或 `__index` 函数实现信息隐藏。

## Mixin 混入模式

Mixin 是一种将可复用行为横向注入类的模式，无需继承即可组合多个来源的方法：

```lua
local function mixin(target, ...)
    for _, source in ipairs({...}) do
        for k, v in pairs(source) do
            if target[k] == nil then  -- 不覆盖已有方法
                target[k] = v
            end
        end
    end
    return target
end

-- 行为 Mixin 定义（纯方法集合）
local Serializable = {
    serialize = function(self)
        local parts = {}
        for k, v in pairs(self) do
            if type(v) ~= "function" then parts[#parts+1] = k.."="..tostring(v) end
        end
        return "{" .. table.concat(parts, ",") .. "}"
    end
}

local Collidable = {
    collides_with = function(self, other)
        return math.abs(self.x - other.x) < self.w/2 + other.w/2 and
               math.abs(self.y - other.y) < self.h/2 + other.h/2
    end
}

-- 应用：Sprite 获得序列化 + 碰撞能力，无需继承任何父类
local Sprite = {}
mixin(Sprite, Serializable, Collidable)
```

Mixin 与继承的区别：继承是纵向"是一种"关系；Mixin 是横向"具有某能力"组合，避免多重继承的菱形问题。

## 常见陷阱
- **忘写 `__index`**：`Class.__index = Class` 缺失时，实例无法找到类方法，调用报错。
- **冒号与点混用**：`function Class:method()` 定义后必须用 `obj:method()` 调用，否则 `self` 不自动传入。
- **require 返回的是类而非实例**：`local Class = require("Class")` 得到类表，需再调用 `Class:new(...)` 创建实例。

## 推荐模板
```lua
local ClassName = {}
ClassName.__index = ClassName

function ClassName:new(...)
    local obj = setmetatable({}, self)
    -- 初始化字段
    return obj
end

return ClassName
```

## 来源
- [[Lua table 深入解析]] — ChatGPT 对话，涵盖冒号语法、类实现模式与综合示例
- [[Lua 类模块实现]] — ChatGPT 对话，私有函数、静态方法、继承模式与常见陷阱
- [[raw/articles/programming/lua/lua-skill/references/patterns.md]] — Lua 高级模式参考，Mixin 混入模式

## 相关
- [[Lua-table]] — OOP 的载体数据结构
- [[Lua-metatable]] — OOP 的实现机制
- [[Lua模块系统]] — 类模块以 module 形式组织和导出
- [[游戏引擎架构]] — Lua 常作为游戏引擎脚本层，OOP 模式广泛用于游戏对象建模
