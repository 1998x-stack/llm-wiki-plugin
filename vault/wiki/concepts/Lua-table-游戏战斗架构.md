---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [Lua, 游戏开发, 战斗系统, 架构]
aliases: ["Lua战斗table架构", "Lua战斗系统表结构"]
relates_to:
  - target: "[[Lua-table-用法]]"
    type: extends
    confidence: 0.9
  - target: "[[Lua-table]]"
    type: part_of
    confidence: 0.7
  - target: "[[Lua战斗配置目录结构]]"
    type: relates_to
    confidence: 0.85
supersedes: null
---

# Lua table 游戏战斗架构

## 概述
手游战斗系统（Unity/[[Lua脚本宿主模式|xLua]]、Cocos Lua）中 [[Lua-table-用法|Lua table]] 的标准落地架构模板，涵盖 Battle/Unit 骨架与最佳实践。

## 关键内容

### 稳定落地模板

```lua
Battle = {
  frame = 0,
  round = 0,
  units = {},       -- array: 顺序遍历
  unitMap = {},     -- uid -> unit: O(1) 查询
  eventQueue = {},
  context = {},     -- 全局临时战斗数据
}

Unit = {
  id = 0,
  cfgId = 0,
  team = 0,
  pos = 0,
  attr = { hp = 0, maxHp = 0, atk = 0, def = 0 },
  state = { dead = false, dizzy = false, silence = false },
  skill = { cdMap = {} },
  buff = { list = {}, map = {} },
}
```

该模板同时满足四个分离原则：配置与状态分离、遍历与查询分离、永久状态与临时上下文分离、逻辑结果与表现事件分离。

### 索引双结构模式

同一批实体同时维护两种访问结构：

```lua
battle.units         -- {u1, u2, u3}  顺序遍历用
battle.unitMap[uid]  -- O(1) 按 uid 直查
battle.teamMap[1]    -- 我方单位列表（分组 map）
```

**一份主数据，多份视图索引**：其他 table 只持有引用，不复制数据。

### 上下文表（ctx）使用规范

技能释放/伤害结算流程通过 ctx table 统一传参：

```lua
local ctx = {
  caster = attacker,
  target = defender,
  skillId = 1001,
  damageType = "magic",
  baseDamage = 120,
  finalDamage = 0,
  flags = { isCrit = false, isBlock = false, isDodge = false },
  ext = {},
}
```

优点：插中间逻辑方便、便于 hook/埋点/回放；约束：每次结算新建 ctx，不跨阶段复用。

### 事件表（event table）

逻辑层输出结构化 event，表现层消费，实现解耦：

```lua
local event = {
  type = "Damage",
  attackerId = 10001,
  targetId = 10002,
  value = 256,
  isCrit = true,
}
```

好处：支持录像/回放、断线重连、战报同步；逻辑层不直接操作特效/UI。

### Unity/xLua 分离模式

```lua
self.view = {
  go = csGameObject,    -- C# Unity 对象
  anim = csAnimator,
}
self.data = {
  hp = 100,             -- Lua 侧逻辑状态
  state = "idle",
}
```

分离原因：Unity 对象与 Lua table 生命周期不同步，混合易出引用悬挂或对象已销毁但 Lua 还持有引用的问题。

### Cocos Lua 节点模式

```lua
local Player = {}
function Player:onEnter() end
function Player:update(dt) end
return Player
```

Cocos Lua 中 table 充当脚本实例，生命周期跟节点组件事件走。大型项目需拆分 model/view/controller 避免 table 过肥。

## 来源
- [[Lua表格组织方式]] — ChatGPT 对话：Unity/xLua、Cocos Lua、手游战斗系统中 table 组织模式 (https://chatgpt.com/c/69d65e85-e85c-8321-855d-38aeba85c657)

## 相关
- [[Lua-table-用法]] — Lua table 游戏开发全面用法，含 5 层组织模型
- [[Lua-table]] — Lua table 内部机制与语言特性
- [[Lua-OOP]] — setmetatable 实现类对象，用于战斗单位建模
- [[Lua战斗配置目录结构]] — 战斗配置的六层目录模板（cfg/battle/unit/skill/buff/event）
