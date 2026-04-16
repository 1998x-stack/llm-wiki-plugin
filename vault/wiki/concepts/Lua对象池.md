---
type: concept
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, Lua编程]
aliases: [Lua object pool, Lua GC优化, Lua内存池]
relates_to:
  - target: "[[LuaJIT]]"
    type: relates_to
    confidence: 0.85
  - target: "[[Lua脚本宿主模式]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Lua-OOP]]"
    type: uses
    confidence: 0.75
supersedes: null
---
# Lua 对象池

## 概述
Lua 对象池通过预分配并复用 table 对象来减少 GC 压力，适用于游戏中高频创建/销毁的临时对象（子弹、粒子、特效）。

## 关键内容

### 核心问题：Lua GC 压力
Lua 使用增量式垃圾回收。高频 `{}` 创建会产生大量短命 table，触发 GC 步进时引起帧率毛刺。对象池通过回收复用对象绕过 GC。

### 基础对象池实现
```lua
local ObjectPool = {}
ObjectPool.__index = ObjectPool

function ObjectPool.new(factory, reset, maxSize)
    return setmetatable({
        _factory = factory,   -- 创建新对象的函数
        _reset   = reset,     -- 归还时重置对象状态的函数
        _pool    = {},        -- 空闲对象列表
        _maxSize = maxSize or 128,
    }, ObjectPool)
end

function ObjectPool:acquire(...)
    local obj = table.remove(self._pool)  -- O(1) 从尾部取
    if obj then
        return obj
    end
    return self._factory(...)
end

function ObjectPool:release(obj)
    if #self._pool < self._maxSize then
        self._reset(obj)
        table.insert(self._pool, obj)  -- 归还到尾部
    end
    -- 超过上限则抛弃，让 GC 回收
end

return ObjectPool
```

### 使用示例
```lua
local bulletPool = ObjectPool.new(
    function() return {x=0, y=0, vx=0, vy=0, alive=false} end,
    function(b) b.x=0; b.y=0; b.vx=0; b.vy=0; b.alive=false end,
    256
)

-- 发射子弹
local b = bulletPool:acquire()
b.x, b.y, b.vx, b.vy, b.alive = px, py, vx, vy, true

-- 子弹死亡
bulletPool:release(b)
```

### GC 调优参数
除对象池外，可通过 `collectgarbage` 调整 GC 行为：
```lua
-- 降低 GC 步进频率（pause 值越大，GC 越少触发）
collectgarbage("setpause", 200)   -- 默认 200，可调大至 400
-- 降低 GC 单步消耗
collectgarbage("setstepmul", 100) -- 默认 200，调小减少单次停顿
-- 手动在帧末做一小步
collectgarbage("step", 1)
```

### 热路径局部化
对象池之外，还应将高频访问的全局变量局部化：
```lua
-- 热路径前缓存为局部变量，避免每次走全局 _G 查找
local sin, cos, sqrt = math.sin, math.cos, math.sqrt
```

### LuaJIT 下的注意事项
[[LuaJIT]] 的 JIT 编译器对循环内频繁创建 table 有特殊处理，但对象池仍然有效减少 GC 压力。FFI（Foreign Function Interface）可进一步绕过 Lua GC，直接分配 C 内存。

## 常见陷阱
- **reset 不彻底**：归还时未清除所有字段，旧数据污染新的使用
- **pool 持有引用阻止 GC**：池中对象引用了外部重型资源（纹理、socket），即使"空闲"也不会被 GC 回收
- **超出 maxSize 的对象静默丢弃**：release 超限时对象被抛弃，调用方不应再持有引用

## 来源
- [[raw/articles/programming/lua/lua-skill/SKILL.md]] — Lua 专家技能文档，scripts/object_pool.lua 模板及 GC 调优、热路径优化要点

## 相关
- [[LuaJIT]] — LuaJIT FFI 可进一步绕过 Lua GC 分配 C 内存
- [[Lua脚本宿主模式]] — 对象池用于游戏业务层高频对象管理
- [[Lua-OOP]] — 对象池通常配合类系统管理游戏实体实例
