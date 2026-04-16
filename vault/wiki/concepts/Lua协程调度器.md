---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, Lua编程]
aliases: [Lua任务调度器, Lua coroutine scheduler, Lua协程任务系统]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.9
  - target: "[[Lua热重载]]"
    type: relates_to
    confidence: 0.5
  - target: "[[Lua沙盒系统]]"
    type: relates_to
    confidence: 0.5
supersedes: null
---
# Lua 协程调度器

## 概述
Lua 协程调度器是利用 coroutine 实现异步任务队列的模式，无需真正多线程即可在游戏[[游戏主循环模式|主循环]]中逐帧推进等待任务。

## 关键内容

### 核心原理
Lua 的 `coroutine` 是协作式多任务：任务主动 `coroutine.yield()` 让出控制权，调度器在下一帧（或满足条件时）调用 `coroutine.resume()` 继续执行。游戏引擎价值：异步等待无需真正多线程，只需等待帧/动画/网络/资源。

### 基本调度循环
```lua
local Scheduler = {}
local tasks = {}   -- {co, wakeTime}

function Scheduler.spawn(fn, ...)
    local co = coroutine.create(fn)
    coroutine.resume(co, ...)
    table.insert(tasks, {co = co, wakeAt = 0})
end

function Scheduler.wait(seconds)
    coroutine.yield(seconds)
end

function Scheduler.update(dt, now)
    local alive = {}
    for _, task in ipairs(tasks) do
        if now >= task.wakeAt and coroutine.status(task.co) ~= "dead" then
            local ok, delay = coroutine.resume(task.co, dt)
            if ok and coroutine.status(task.co) ~= "dead" then
                task.wakeAt = now + (delay or 0)
                table.insert(alive, task)
            end
        else
            table.insert(alive, task)
        end
    end
    tasks = alive
end
```

### 典型使用模式
```lua
-- yield_wait_seconds(1.0) / yield_wait_event("BossDead")
Scheduler.spawn(function()
    print("boss fight start")
    Scheduler.wait(3.0)   -- 3秒后继续
    print("boss enraged")
end)
```

### 关键设计问题
1. **谁恢复 coroutine**：调度器持有 coroutine 引用，主循环每帧调用 `Scheduler.update()`
2. **在哪一帧恢复**：按 `wakeAt` 时间戳判断，避免每帧唤醒无关任务
3. **对象销毁时取消**：任务需持有 owner 引用，owner 销毁后将对应 coroutine 从队列移除
4. **错误冒泡**：`coroutine.resume()` 返回 `false, errMsg` 时需捕获并记录，不能让调度器崩溃

### 与 `async/await` 的对比
Lua 协程本质等价于手动控制的 `async/await`。yield 点对应 `await`，resume 对应事件循环推进。区别：Lua 协程是协作式（需主动 yield），不是抢占式。

## 常见陷阱
- **coroutine.status 忘判**：resume 已死亡的 coroutine 会报错
- **upvalue 过期**：协程闭包捕获了已销毁对象的引用，resume 后访问出错
- **yield 跨 C 边界**：某些嵌入场景（Lua 5.1）不允许在 C 函数调用链中 yield，需用 `lua_yieldk`

## 来源
- [[raw/articles/programming/lua/lua-skill/SKILL.md]] — Lua 专家技能文档，scripts/coroutine_scheduler.lua 模板及协程调度设计要点

## 相关
- [[Lua脚本宿主模式]] — 调度器是第4层"调度与事件层"的核心实现
- [[Lua事件总线]] — 协程常与事件总线配合实现 yield_wait_event
- [[游戏主循环模式]] — 调度器 update() 挂在主循环上
