---
type: concept
status: active
confidence: 0.87
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [Lua, 游戏开发, 战斗系统, 架构, 配置]
aliases: ["Lua战斗配置分层", "战斗config目录", "Lua六层战斗配置", "battle_config目录结构"]
relates_to:
  - target: "[[Lua-table-游戏战斗架构]]"
    type: extends
    confidence: 0.92
  - target: "[[Lua数据驱动设计]]"
    type: uses
    confidence: 0.88
  - target: "[[Lua事件总线]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Lua 战斗配置目录结构

## 概述
手游战斗系统 Lua [[Configuration|配置]]的六层目录模板：cfg/battle/unit/skill/buff/event，以 id 引用替代直接嵌套，避免循环依赖。

## 关键内容

### 六层目录职责

```
battle_config/
├── cfg/      -- 全局静态常量、枚举、公式映射、标签（被所有层引用）
├── battle/   -- 单场战斗/关卡实例（出生点、阵型、胜负条件、波次）
├── unit/     -- 单位模板（属性、技能挂载、AI类型、阵营标签）
├── skill/    -- 技能定义（技能壳 + effect/ 可复用效果片段）
├── buff/     -- 持续性状态（层数、触发时机、覆盖/叠加/互斥/驱散规则）
└── event/    -- 战斗事件（trigger/ 触发器 + condition/ 条件判断）
```

**cfg 层特点**：稳定、抽象、低频修改，被其他所有目录 require。

### 推荐依赖方向（避免循环依赖）

```
cfg    -> 被所有层依赖（基础）
unit   -> 依赖 cfg / skill
skill  -> 依赖 cfg / buff / event(effect hook)
buff   -> 依赖 cfg / event(optional)
battle -> 依赖 unit / event / cfg
event  -> 依赖 cfg，以 id 引用 unit / buff / skill
```

**核心原则**：各层以 **id 引用** 为主，不互相直接嵌套整表，避免 unit require battle、buff require skill 等反向依赖。

### 典型配置骨架

**battle 层**（关卡实例）：
```lua
return {
    battle_id = 1001,
    win_condition = "kill_all",
    max_round = 30,
    player_team = { {pos=1, unit_id=3001, level=10} },
    enemy_waves = { {wave_index=1, units={{pos=1, unit_id=2001, level=8}}} },
    events = {1001, 1002},
}
```

**unit 层**（单位模板）：
```lua
return {
    unit_id = 3001,
    camp = "player",
    tags = {"hero", "front", "fire"},
    attr = {hp=1200, atk=180, def=80, speed=110},
    normal_skill = 1001,
    active_skill = 2001,
    passive_skills = {3001, 3002},
    ai = "melee_basic",
}
```

**skill 层**（技能壳 + effect 片段）：
```lua
-- skill/skill_2001.lua
return {
    skill_id = 2001, skill_type = "active", cost_mp = 100,
    target = {type="enemy", select="front_row", count=1},
    phases = {{time=0, effects={{effect=5001, value=180}}}},
    cd = 2,
}
-- skill/effect/effect_5001.lua（可复用效果）
return {effect_id=5001, type="damage", formula="ATK_COEF", damage_type="fire"}
```

**buff 层**（持续状态）：
```lua
return {
    buff_id = 4001, name = "灼烧", buff_type = "dot",
    duration = 2, max_stack = 3,
    triggers = {{timing="on_round_end",
        effects={{type="damage", formula="BUFF_SRC_ATK_COEF", value=40}}}},
    dispel = {positive=false, can_be_dispelled=true},
}
```

**event 层**（战斗触发器）：
```lua
return {
    event_id = 1001, trigger = "on_round_start",
    condition = {round = 3},
    actions = {
        {type="spawn_unit", unit_id=2003, pos=5, camp="enemy"},
        {type="play_timeline", timeline="boss_entry"},
    }
}
```

### 统一入口 init.lua

```lua
local M = {}
M.cfg   = {const=require("battle_config.cfg.battle_const"), enum=require("..."), formula=require("...")}
M.battle = {}  M.unit = {}  M.skill = {}  M.buff = {}  M.event = {}
return M
```

导表工具自动生成场景可改为：
```lua
return {
    battle=require("gen.battle_index"), unit=require("gen.unit_index"),
    skill=require("gen.skill_index"),   buff=require("gen.buff_index"),
    event=require("gen.event_index"),
}
```

### 命名规范

文件命名统一 `{类型}_{数字id}.lua`（`battle_1001.lua`、`unit_3001.lua`）。枚举字段优先字符串常量（`skill_type="active"`、`damage_type="fire"`），禁用魔法数字，导表时可转数字。

### 策划协作版扩展目录

适合中后期项目，对 battle 按玩法分目录（mainline/tower/arena/boss），buff 按性质分（positive/negative/control/dot），event 按层级分（battle_rule/wave_event/stage_mechanism/common_trigger）。

## 来源
- [[raw/articles/programming/lua/战斗系统Lua目录模板.md]] — ChatGPT 对话：战斗系统 Lua table 配置六层目录结构模板 (https://chatgpt.com/c/69d65fae-bdcc-8324-91a2-68485c137f90)

## 相关
- [[Lua-table-游戏战斗架构]] — 战斗运行时 table 结构（Battle/Unit 骨架）
- [[Lua数据驱动设计]] — 配置表模式与工厂函数，该目录结构的数据层实现
- [[Lua事件总线]] — event 层的触发/条件机制与事件总线的关系
