---
type: concept
status: active
confidence: 0.83
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, 设计模式, Lua编程]
aliases: [Lua层次状态机, Lua HSM, Lua FSM, Lua有限状态机]
relates_to:
  - target: "[[Lua-OOP]]"
    type: uses
    confidence: 0.85
  - target: "[[Lua事件总线]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.75
supersedes: null
---
# Lua 状态机

## 概述
Lua 状态机（HSM/FSM）将游戏逻辑拆分为离散状态，每个状态定义 enter/update/exit 回调；层次状态机（HSM）支持状态嵌套，子状态未处理的事件上浮父状态。

## 关键内容

### 基础有限状态机（FSM）
```lua
local StateMachine = {}
StateMachine.__index = StateMachine

function StateMachine.new(owner)
    return setmetatable({owner = owner, current = nil, states = {}}, StateMachine)
end

function StateMachine:add(name, state)
    -- state = {enter=fn, update=fn, exit=fn, transitions={event=nextName}}
    self.states[name] = state
end

function StateMachine:change(name, ...)
    if self.current and self.current.exit then
        self.current.exit(self.owner)
    end
    self.current = self.states[name]
    if self.current and self.current.enter then
        self.current.enter(self.owner, ...)
    end
end

function StateMachine:update(dt)
    if self.current and self.current.update then
        self.current.update(self.owner, dt)
    end
end

function StateMachine:handle(event, ...)
    if not self.current then return end
    local next = self.current.transitions and self.current.transitions[event]
    if next then
        self:change(next, ...)
        return true
    end
    return false
end
```

### 使用示例：敌人 AI
```lua
local enemy = {hp = 100}
local sm = StateMachine.new(enemy)

sm:add("idle", {
    enter = function(e) e.timer = 0 end,
    update = function(e, dt)
        e.timer = e.timer + dt
        if e.timer > 2 then sm:handle("patrol") end
    end,
    transitions = {patrol = "patrol", attack = "attack"},
})

sm:add("patrol", {
    update = function(e, dt) --[[ 巡逻逻辑 ]] end,
    transitions = {attack = "attack", idle = "idle"},
})

sm:change("idle")  -- 初始化

-- 游戏主循环
sm:update(dt)
sm:handle("attack")  -- 外部事件触发状态转换
```

### 层次状态机（HSM）扩展
HSM 核心思想：状态可以有父状态。子状态 `handle(event)` 返回 `false` 时，事件向上冒泡到父状态处理。适合共享行为（如所有"移动中"状态共享"碰墙停止"逻辑）。

```lua
-- 在 handle 中加入父状态回退
function StateMachine:handle(event, ...)
    local state = self.current
    while state do
        local next = state.transitions and state.transitions[event]
        if next then
            self:change(next, ...)
            return true
        end
        state = state.parent  -- 上浮
    end
    return false
end
```

### 与事件总线集成
状态机 `handle()` 可直接连接 EventBus 事件，实现解耦触发：
```lua
EventBus.on("enemy_spotted", function(enemy)
    enemy.sm:handle("attack", enemy)
end)
```

### 设计建议
- **enter/exit 严格配对**：每次 change 保证 exit 先于 enter 执行，不要在 update 中直接修改 current
- **转换表 vs 函数**：简单 FSM 用声明式转换表（`transitions = {}`）；复杂条件判断改为 `on_event` 回调函数
- **状态数据独立**：状态内部临时数据存 owner 上（`e.timer`），状态对象本身保持无状态（可复用）

## 常见陷阱
- **change 中再次 change**：enter 回调内触发新的转换，可能导致 exit 调用顺序混乱；建议 change 加重入保护
- **update 遗漏 nil 检查**：`self.current` 在 change 中短暂为 nil，并发或重入时可能触发 nil 调用

## 来源
- [[raw/articles/programming/lua/lua-skill/SKILL.md]] — Lua 专家技能文档，scripts/state_machine.lua 层次状态机模板

## 相关
- [[Lua-OOP]] — 状态机通常以类模式组织，状态为 table 对象
- [[Lua事件总线]] — 状态切换常由事件总线触发，handle() 订阅外部事件
- [[Lua脚本宿主模式]] — 状态机属于第5层业务框架层的核心架构模式
