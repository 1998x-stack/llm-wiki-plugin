---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, 设计模式, Lua编程]
aliases: [Lua事件系统, Lua信号系统, Lua发布订阅, Lua EventBus, Lua pub-sub]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.9
  - target: "[[Lua协程调度器]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Lua模块系统]]"
    type: uses
    confidence: 0.75
supersedes: null
---
# Lua 事件总线

## 概述
Lua 事件总线（EventBus）是发布-订阅模式的实现，允许模块间解耦通信；订阅者注册回调，发布者 emit 事件名触发所有监听器。

## 关键内容

### 基础实现
```lua
local EventBus = {}
local listeners = {}  -- {eventName: [fn, ...]}

function EventBus.on(event, fn)
    listeners[event] = listeners[event] or {}
    table.insert(listeners[event], fn)
end

function EventBus.off(event, fn)
    local list = listeners[event]
    if not list then return end
    for i = #list, 1, -1 do
        if list[i] == fn then table.remove(list, i) end
    end
end

function EventBus.emit(event, ...)
    local list = listeners[event]
    if not list then return end
    for _, fn in ipairs(list) do
        local ok, err = pcall(fn, ...)
        if not ok then
            -- 错误隔离：单个回调崩溃不影响其他监听器
            print("[EventBus] error in " .. event .. ": " .. tostring(err))
        end
    end
end

return EventBus
```

### 设计要点
1. **可失效**：对象销毁时必须调用 `EventBus.off()`，否则持有过期闭包引用是高频 bug
2. **可追踪**：跨帧回调中旧闭包捕获过期 upvalue 难以发现，建议在回调第一行检查 owner 是否存活
3. **可清理**：场景切换时可直接重置整个 `listeners` 表，或用命名空间前缀区分场景事件
4. **错误隔离**：每个回调独立 `pcall`，一个失败不影响其他订阅者

### 与协程集成
```lua
-- yield_wait_event 实现：协程等待特定事件后恢复
function Scheduler.wait_event(event)
    local co = coroutine.running()
    local function handler(...)
        EventBus.off(event, handler)
        coroutine.resume(co, ...)
    end
    EventBus.on(event, handler)
    coroutine.yield()
end
```

### 引用存储规则
引擎保存 Lua function 引用时，必须存入注册表（`lua_ref`），不能保存栈上临时值。存注册表的引用在 GC 标记为存活，栈临时值随函数返回即可能被回收。

### 命名空间约定
大型项目建议给事件名加前缀区分系统：`"ui:button_click"`, `"com[[bat]]:boss_dead"`, `"net:data_recv"`，避免全局命名冲突。

## 常见陷阱
- **忘记 off**：订阅者对象已销毁但仍在 listeners 中，emit 时访问已释放数据
- **回调中 emit 同一事件**：可能导致递归或无限循环，需加重入保护标志
- **table.remove 遍历中**：在 emit 遍历 listeners 时 off 同一事件的监听器会跳过元素，应先浅拷贝再遍历

## 来源
- [[raw/articles/programming/lua/lua-skill/SKILL.md]] — Lua 专家技能文档，scripts/event_bus.lua 模板及引擎事件回调桥设计要点

## 相关
- [[Lua脚本宿主模式]] — 事件桥是第4层"调度与事件层"的核心组件
- [[Lua协程调度器]] — 协程可订阅事件实现 yield_wait_event
- [[Lua模块系统]] — EventBus 作为模块导出使用
