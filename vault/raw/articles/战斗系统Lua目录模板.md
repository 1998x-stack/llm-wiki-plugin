---
title: "战斗系统Lua目录模板"
source: "https://chatgpt.com/c/69d65fae-bdcc-8324-91a2-68485c137f90"
author:
published:
created: 2026-04-08
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
可以，下面给你一个适合 **战斗系统 Lua table 配置** 的目录结构模板，按你说的六层来： `cfg / battle / unit / skill / buff / event` 。

我先给一个 **推荐目录树** ，再补每层职责和命名建议。

```markdown
battle_config/
├── cfg/
│   ├── battle_const.lua          -- 战斗全局常量
│   ├── battle_enum.lua           -- 枚举定义
│   ├── battle_formula.lua        -- 通用公式/数值函数映射
│   ├── battle_tag.lua            -- 标签定义（职业、属性、阵营、状态）
│   ├── battle_scene.lua          -- 场景/关卡通用配置
│   └── battle_system.lua         -- 系统开关、默认参数
│
├── battle/
│   ├── battle_1001.lua           -- 单场战斗/关卡配置
│   ├── battle_1002.lua
│   ├── battle_2001.lua           -- Boss战/玩法战斗配置
│   └── ...
│
├── unit/
│   ├── unit_1001.lua             -- 单位基础模板
│   ├── unit_1002.lua
│   ├── monster/
│   │   ├── unit_2001.lua
│   │   └── unit_2002.lua
│   ├── hero/
│   │   ├── unit_3001.lua
│   │   └── unit_3002.lua
│   └── summon/
│       ├── unit_4001.lua
│       └── ...
│
├── skill/
│   ├── skill_1001.lua            -- 技能总表/技能定义
│   ├── skill_1002.lua
│   ├── active/
│   │   ├── skill_2001.lua
│   │   └── ...
│   ├── passive/
│   │   ├── skill_3001.lua
│   │   └── ...
│   └── effect/
│       ├── effect_5001.lua       -- 可复用技能效果片段
│       └── ...
│
├── buff/
│   ├── buff_1001.lua             -- Buff定义
│   ├── buff_1002.lua
│   ├── control/
│   │   ├── buff_2001.lua         -- 眩晕、沉默、冻结等
│   │   └── ...
│   ├── stat/
│   │   ├── buff_3001.lua         -- 加攻、减防、吸血等
│   │   └── ...
│   └── dot/
│       ├── buff_4001.lua         -- 灼烧、中毒、流血等
│       └── ...
│
└── event/
    ├── event_1001.lua            -- 事件模板/触发器定义
    ├── event_1002.lua
    ├── trigger/
    │   ├── on_hit.lua
    │   ├── on_kill.lua
    │   ├── on_dead.lua
    │   ├── on_round_start.lua
    │   └── on_round_end.lua
    └── condition/
        ├── hp_less_than.lua
        ├── has_buff.lua
        ├── target_tag_match.lua
        └── ...
```

## 一、每层职责

### 1\. cfg/

放 **全局静态定义** ，尽量不放具体玩法内容。

适合放：

- 常量：最大怒气、默认暴击倍率、默认命中底值
- 枚举：目标类型、伤害类型、Buff类型、触发时机
- 标签：火、水、前排、召唤物、Boss
- 公式映射： `FORMULA.ATK_100 = function(ctx) ... end`

核心特点：

- 被其他所有目录引用
- 稳定、抽象、低频修改

---

### 2\. battle/

放 **一场战斗/一个关卡/一个玩法实例** 的配置。

适合放：

- 参战双方
- 出生点、阵型、波次
- 胜负条件
- 时间限制
- 环境效果
- 首次进入时的事件挂载

例如：

```markdown
return {
    battle_id = 1001,
    scene_id = 1,
    win_condition = "kill_all",
    max_round = 30,

    player_team = {
        { pos = 1, unit_id = 3001, level = 10 },
        { pos = 2, unit_id = 3002, level = 10 },
    },

    enemy_waves = {
        {
            wave_index = 1,
            units = {
                { pos = 1, unit_id = 2001, level = 8 },
                { pos = 2, unit_id = 2002, level = 8 },
            }
        }
    },

    events = { 1001, 1002 },
}
```

---

### 3\. unit/

放 **单位模板** ，是战斗里被实例化的“角色原型”。

适合放：

- 基础属性
- 成长参数
- 普攻技能、主动技能、被动技能挂载
- 模型资源、体型、阵营、标签
- AI类型

例如：

```markdown
return {
    unit_id = 3001,
    name = "烈焰剑士",
    camp = "player",
    tags = {"hero", "front", "fire"},

    attr = {
        hp = 1200,
        atk = 180,
        def = 80,
        speed = 110,
    },

    normal_skill = 1001,
    active_skill = 2001,
    passive_skills = {3001, 3002},

    ai = "melee_basic",
}
```

---

### 4\. skill/

放 **技能定义** 。建议拆成“技能壳”和“效果片段”两层。

适合放：

- 技能释放条件
- 目标选择
- 段数/表现时序
- 效果列表（伤害、治疗、加Buff、位移、召唤）

例如：

```markdown
return {
    skill_id = 2001,
    name = "烈焰斩",
    skill_type = "active",
    cost_mp = 100,

    target = {
        type = "enemy",
        select = "front_row",
        count = 1,
    },

    phases = {
        {
            time = 0,
            effects = {
                { effect = 5001, value = 180 }, -- 伤害
                { effect = 5002, buff_id = 4001, chance = 0.35 }, -- 挂灼烧
            }
        }
    },

    cd = 2,
}
```

如果技能越来越复杂，建议把可复用效果拆到 `skill/effect/` ：

```markdown
return {
    effect_id = 5001,
    type = "damage",
    formula = "ATK_COEF",
    damage_type = "fire",
}
```

---

### 5\. buff/

放 **持续性状态效果** 。

适合放：

- Buff层数规则
- 持续回合/持续秒数
- 生效时机
- 周期效果
- 覆盖/叠加/互斥逻辑
- 驱散规则

例如：

```markdown
return {
    buff_id = 4001,
    name = "灼烧",
    buff_type = "dot",
    duration = 2,
    max_stack = 3,

    triggers = {
        {
            timing = "on_round_end",
            effects = {
                { type = "damage", formula = "BUFF_SRC_ATK_COEF", value = 40, damage_type = "fire" }
            }
        }
    },

    dispel = {
        positive = false,
        can_be_dispelled = true,
    },
}
```

---

### 6\. event/

放 **战斗事件系统** ，处理非单位自身技能驱动的逻辑。

适合放：

- 回合开始/结束事件
- 击杀触发
- 血线触发
- 波次切换
- 特殊机关
- 剧情战斗机制

例如：

```markdown
return {
    event_id = 1001,
    trigger = "on_round_start",
    condition = {
        round = 3,
    },
    actions = {
        { type = "spawn_unit", unit_id = 2003, pos = 5, camp = "enemy" },
        { type = "play_timeline", timeline = "boss_entry" },
    }
}
```

---

## 二、推荐命名规则

建议统一，不然后面会很乱。

### 文件命名

```markdown
battle_1001.lua
unit_3001.lua
skill_2001.lua
buff_4001.lua
event_1001.lua
```

### table 主键

- `battle_id`
- `unit_id`
- `skill_id`
- `buff_id`
- `event_id`

### 枚举字段

尽量别写魔法数字，优先字符串或 enum 常量：

```markdown
skill_type = "active"
damage_type = "fire"
target_type = "enemy"
trigger = "on_hit"
```

如果项目里追求性能，也可以导表时转数字，策划侧源文件仍保持可读。

---

## 三、推荐索引入口

实际落地时，最好再补一层 `init.lua` 或 `index.lua` ，统一 require。

例如：

```markdown
battle_config/
├── init.lua
├── cfg/
├── battle/
├── unit/
├── skill/
├── buff/
└── event/
```

`init.lua`

```markdown
local M = {}

M.cfg = {
    const = require("battle_config.cfg.battle_const"),
    enum = require("battle_config.cfg.battle_enum"),
    formula = require("battle_config.cfg.battle_formula"),
}

M.battle = {}
M.unit = {}
M.skill = {}
M.buff = {}
M.event = {}

return M
```

如果是导表工具自动生成，也可以做成：

```markdown
return {
    battle = require("gen.battle_index"),
    unit   = require("gen.unit_index"),
    skill  = require("gen.skill_index"),
    buff   = require("gen.buff_index"),
    event  = require("gen.event_index"),
}
```

---

## 四、推荐依赖方向

为了避免循环依赖，建议遵循：

```markdown
cfg  -> 被所有层依赖
unit -> 依赖 cfg / skill
skill -> 依赖 cfg / buff / event(effect hook)
buff -> 依赖 cfg / event(optional)
battle -> 依赖 unit / event / cfg
event -> 依赖 cfg，可引用 unit / buff / skill 的 id
```

尽量避免：

- `unit` 直接 require `battle`
- `buff` 直接 require 整个 `skill`
- `event` 写过多具体业务脚本

最好让它们以 **id 引用** 为主，而不是互相直接嵌套整表。

---

## 五、适合策划协作的“更实战”版本

如果你是给策划或配置同学用，我更推荐这个版本：

```markdown
battle_config/
├── cfg/
│   ├── const.lua
│   ├── enum.lua
│   ├── formula.lua
│   └── tag.lua
├── battle/
│   ├── mainline/
│   ├── tower/
│   ├── arena/
│   └── boss/
├── unit/
│   ├── hero/
│   ├── monster/
│   ├── npc/
│   └── summon/
├── skill/
│   ├── active/
│   ├── passive/
│   ├── common_effect/
│   └── skill_group.lua
├── buff/
│   ├── positive/
│   ├── negative/
│   ├── control/
│   └── dot/
└── event/
    ├── battle_rule/
    ├── wave_event/
    ├── stage_mechanism/
    └── common_trigger/
```

这个更适合中后期项目，不容易失控。

---

## 六、最小可用模板

如果你只想先快速起盘，可以直接用这版：

```markdown
battle_config/
├── cfg/
│   ├── battle_const.lua
│   └── battle_enum.lua
├── battle/
│   └── battle_1001.lua
├── unit/
│   └── unit_1001.lua
├── skill/
│   └── skill_1001.lua
├── buff/
│   └── buff_1001.lua
└── event/
    └── event_1001.lua
```

---

我也可以继续给你补一版：  
**“每个 lua 文件的 table 字段模板”** ，直接把 `battle/unit/skill/buff/event` 五类文件都写成可复制的空白骨架。