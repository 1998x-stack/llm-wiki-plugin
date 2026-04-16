---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, Lua编程]
aliases: [Lua元方法, Lua metamethod, Lua metatable高级用法, Lua运算符重载]
relates_to:
  - target: "[[Lua-OOP]]"
    type: extends
    confidence: 0.9
  - target: "[[Lua-metatable]]"
    type: extends
    confidence: 0.95
  - target: "[[Lua函数式编程]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---
# Lua 元表魔法

## 概述
Lua 元表（metatable）通过 __index/__newindex/__call 等元方法实现懒加载、只读表、可调用对象、运算符重载等高级模式，是 Lua 元编程的核心机制。

## 关键内容

### __index 作为函数（懒加载/代理）

```lua
-- 懒加载：第一次访问时计算并缓存
local lazy = setmetatable({}, {
    __index = function(t, k)
        local val = expensive_computation(k)
        rawset(t, k, val)  -- rawset 绕过 __newindex，直接写入
        return val
    end
})
-- 第二次访问 lazy.foo 直接返回缓存，不再触发 __index
```

### __newindex 拦截赋值（只读表、校验）

```lua
-- 只读表：阻止任何写入
local readonly = setmetatable({x = 1, y = 2}, {
    __newindex = function(t, k, v)
        error("Attempt to modify read-only table: " .. k, 2)
    end
})
-- readonly.x = 99  -- 报错

-- 类型校验表
local typed = setmetatable({}, {
    __newindex = function(t, k, v)
        assert(type(v) == "number", k .. " must be a number")
        rawset(t, k, v)
    end
})
```

### __call 让表可调用

```lua
-- 使类直接作为构造器调用
local Vector = setmetatable({}, {
    __call = function(cls, x, y)
        return setmetatable({x=x, y=y}, Vector)
    end
})
Vector.__index = Vector

-- 实例方法
function Vector:length() return math.sqrt(self.x^2 + self.y^2) end
function Vector:__tostring() return string.format("Vec(%g,%g)", self.x, self.y) end

-- v1 = Vector(3, 4)  -- 触发 __call，得到实例
```

### 运算符重载

完整的运算符元方法覆盖：

```lua
function Vector:__add(b)  return Vector(self.x+b.x, self.y+b.y) end
function Vector:__sub(b)  return Vector(self.x-b.x, self.y-b.y) end
function Vector:__mul(s)
    if type(s) == "number" then return Vector(self.x*s, self.y*s) end
    return self.x*s.x + self.y*s.y  -- 点积（重载为 table 参数时）
end
function Vector:__unm()   return Vector(-self.x, -self.y) end   -- 取负
function Vector:__eq(b)   return self.x==b.x and self.y==b.y end
function Vector:__len()   return self:length() end               -- # 操作符

local v1 = Vector(3, 4)
print(#v1)               -- 5.0
print(v1 + Vector(1,0))  -- Vec(4,4)（借助 __add + __tostring）
```

### __index 链（原型继承 / 默认值）

```lua
-- 多级默认值链：实例 → 子类 → 父类 → 全局默认
local defaults = {speed = 100, hp = 100, damage = 10}
local Player = setmetatable({hp = 150}, {__index = defaults})

print(Player.speed)   -- 100（来自 defaults）
print(Player.hp)      -- 150（Player 自己覆盖）
```

### __pairs 自定义迭代（Lua 5.2+）

```lua
-- 过滤迭代：跳过负数值
local filtered = setmetatable(data, {
    __pairs = function(t)
        local function iter(t, k)
            local nk, nv = next(t, k)
            while nk and nv < 0 do nk, nv = next(t, nk) end
            return nk, nv
        end
        return iter, t, nil
    end
})
for k, v in pairs(filtered) do print(k, v) end  -- 只打印非负值
```

### 关键函数对比

| 函数 | 行为 |
|------|------|
| `rawget(t, k)` | 绕过 `__index` 直接读取 |
| `rawset(t, k, v)` | 绕过 `__newindex` 直接写入 |
| `rawequal(a, b)` | 绕过 `__eq` 比较引用 |
| `rawlen(t)` | 绕过 `__len` 取原始长度 |

## 常见陷阱

- **__eq 只比较同 metatable 的对象**：两个不同 metatable 的 table 用 `==` 不会触发 __eq
- **__index 无限递归**：若 __index 函数内访问同一 key 又触发 __index，会栈溢出；用 `rawget` 避免
- **__newindex + rawset**：__newindex 内必须用 `rawset` 写入，否则递归
- **运算符结合律**：`a + b` 优先用 a 的 `__add`，若不存在则用 b 的，两个都没有才报错

## 来源
- [[raw/articles/programming/lua/lua-skill/references/patterns.md]] — Lua 高级模式参考，元表魔法章节

## 相关
- [[Lua-metatable]] — 元表基础概念与 setmetatable/getmetatable
- [[Lua-OOP]] — OOP 的继承链本质是 __index 链的应用
- [[Lua函数式编程]] — __call 使 table 可作为函数式构造器使用
