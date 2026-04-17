---
type: concept
status: active
confidence: 0.87
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 性能优化, 游戏开发, Lua编程]
aliases: [Lua性能, Lua热路径优化, Lua GC调优, Lua基准测试]
relates_to:
  - target: "[[LuaJIT]]"
    type: extends
    confidence: 0.9
  - target: "[[Lua对象池]]"
    type: relates_to
    confidence: 0.88
  - target: "Luau"
    type: relates_to
    confidence: 0.6
supersedes: null
---
# Lua 性能优化

## 概述
Lua 性能优化的核心原则：先测量再优化。最大收益点来自局部化全局访问、避免热路径分配、GC 调优和对象池复用。

## 关键内容

### 性能分析原则
1. 用 `os.clock()` 或外部 profiler 测量，锁定真实瓶颈再优化
2. 性能优先级（[[LuaJIT]] 场景）：FFI 调用 > C 函数 > 纯 Lua（JIT 后）> 纯 Lua（解释）
3. 优化前记录基准数值，避免感觉驱动的过早优化

### GC 调优

Lua 5.1–5.3 增量 GC，5.4 引入分代 GC：

```lua
-- 增量 GC 参数（5.1-5.3）
collectgarbage("setpause", 150)    -- 内存增长比例触发阈值（默认200）
collectgarbage("setstepmul", 300)  -- 单步处理量激进度（调大加快回收）

-- 5.4 分代 GC（短命对象多时更高效）
collectgarbage("generational", 20, 200)

-- 帧预算式 GC（游戏推荐方案）
local GC_BUDGET_MS = 0.5
local function gc_update()
    local t = os.clock()
    while (os.clock() - t) * 1000 < GC_BUDGET_MS do
        if collectgarbage("step", 50) then break end
    end
end
```

手动控制：`collectgarbage("stop")` 停止自动 GC，`collectgarbage("step", N)` 分帧步进，避免在帧内调用 `collectgarbage("collect")`（全量停顿）。

### 热路径优化清单

```lua
-- 1. 局部化频繁使用的全局/标准库函数
local sin, cos, sqrt = math.sin, math.cos, math.sqrt
local insert = table.insert
local format = string.format

-- 2. 预计算循环不变量（避免每次迭代查 #t）
local n = #entities
for i = 1, n do update(entities[i]) end

-- 3. 数值 for 比 ipairs 快约 20%（LuaJIT 可 JIT 编译）
for i = 1, n do local v = t[i] end

-- 4. 避免热路径创建临时 table（复用静态表）
local _bounds = {}
function get_bounds(obj)
    _bounds.x = obj.x - obj.w/2
    _bounds.y = obj.y - obj.h/2
    _bounds.w, _bounds.h = obj.w, obj.h
    return _bounds
end

-- 5. 字符串拼接用 table.concat（避免 O(n²) 中间字符串）
local parts = {}
for i = 1, 1000 do parts[i] = items[i] end
local s = table.concat(parts)

-- 6. 缓存 method 查找（极高频调用时）
local entity_update = Entity.update
for _, e in ipairs(entities) do entity_update(e, dt) end

-- 7. LuaJIT：偏好纯 float 运算（可向量化）
```

### LuaJIT FFI 高性能缓冲区

LuaJIT FFI 分配的 C 数组无 GC 压力，适合顶点缓冲等高频写入场景：

```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef struct { float x, y; uint16_t u, v; uint32_t color; } Vertex;
    void render_batch(const Vertex *verts, int count);
]]
local MAX_VERTS = 4096
local vbuf = ffi.new("Vertex[?]", MAX_VERTS)  -- C 内存，无 GC
local vert_count = 0
```

FFI 调用比通过 Lua 栈的 C API 快 5–10×，见 [[LuaJIT]]。

### 基准测试工具

```lua
local Bench = {}
function Bench.run(name, iterations, fn, ...)
    for i = 1, math.min(100, iterations / 10) do fn(...) end  -- 预热
    collectgarbage("collect"); collectgarbage("stop")
    local mem0, t0 = collectgarbage("count"), os.clock()
    for i = 1, iterations do fn(...) end
    local elapsed = os.clock() - t0
    local dmem = collectgarbage("count") - mem0
    collectgarbage("restart")
    print(string.format("[Bench] %-30s %7d iter %8.3f ms %6.1f ns/op mem:%+.1f KB",
        name, iterations, elapsed*1000, elapsed/iterations*1e9, dmem))
end
```

GC 停止后测量可隔离计算成本，`mem` 差值反映分配压力。

## 常见陷阱
- **过早优化**：未 profile 就重写，收益不及预期
- **全量 GC 在帧内**：`collectgarbage("collect")` 会造成明显帧率毛刺
- **停止 GC 后忘记重启**：`collectgarbage("stop")` 后必须 `restart`，否则内存泄漏
- **table.concat 空 parts**：忘记初始化 `parts` 导致 nil 拼接错误

## 来源
- [[raw/articles/programming/lua/lua-skill/references/performance.md]] — Lua 性能优化参考：GC 调优、热路径清单、FFI 缓冲、基准测试工具

## 相关
- [[LuaJIT]] — JIT 编译与 FFI 高性能 C 调用，性能层级最高的优化手段
- [[Lua对象池]] — 热路径分配优化的专项模式，配合 GC 调优使用
- Luau — Roblox 定制 Lua，有自己的性能特性（Native codegen）
