---
title: "Lua 文件模板"
source: "https://chatgpt.com/c/69d6605d-41d4-8320-9fa2-371022811347"
author:
published:
created: 2026-04-08
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
下面直接给你五类 Lua 文件的 **可复制空白骨架** ，统一按「返回一个 table」的写法来铺开。字段名先尽量通用、可扩展，具体再按你们项目实际替换。

---

## 1\. battle 文件模板

```markdown
local Battle = {
    -- 基础信息
    id = 0,
    key = "",
    name = "",
    desc = "",

    -- 战斗配置
    type = "",
    mode = "",
    round_limit = 0,
    time_limit = 0,

    -- 参与单位
    attacker = {
        team_id = 0,
        units = {
            -- [1] = { unit_id = 0, pos = 0, level = 0 },
        },
    },

    defender = {
        team_id = 0,
        units = {
            -- [1] = { unit_id = 0, pos = 0, level = 0 },
        },
    },

    -- 地图 / 场景
    scene = {
        scene_id = 0,
        map_id = 0,
        spawn_points = {},
    },

    -- 胜负条件
    win_condition = {
        type = "",
        params = {},
    },

    lose_condition = {
        type = "",
        params = {},
    },

    -- 波次 / 阶段
    waves = {
        -- [1] = {
        --     wave_id = 0,
        --     trigger = {},
        --     units = {},
        -- },
    },

    phases = {
        -- [1] = {
        --     phase_id = 0,
        --     trigger = {},
        --     actions = {},
        -- },
    },

    -- 奖励
    rewards = {
        -- [1] = { type = "", id = 0, count = 0 },
    },

    -- 扩展参数
    tags = {},
    params = {},
    ext = {},
}

return Battle
```

---

## 2\. unit 文件模板

```markdown
local Unit = {
    -- 基础信息
    id = 0,
    key = "",
    name = "",
    desc = "",

    -- 类型 / 阵营
    unit_type = "",
    camp = "",
    race = "",
    job = "",

    -- 展示资源
    model = "",
    icon = "",
    portrait = "",
    animation = "",

    -- 等级 / 品质
    level = 0,
    star = 0,
    quality = 0,

    -- 基础属性
    attr = {
        hp = 0,
        atk = 0,
        def = 0,
        spd = 0,
        cri = 0,
        ten = 0,
        hit = 0,
        dodge = 0,
        rage = 0,
    },

    -- 成长属性
    growth = {
        hp = 0,
        atk = 0,
        def = 0,
        spd = 0,
    },

    -- 技能
    skills = {
        normal = 0,
        active = 0,
        passive = {
            -- [1] = 0,
        },
        ultimate = 0,
    },

    -- Buff / 特性
    buffs = {
        -- [1] = 0,
    },

    traits = {
        -- [1] = "",
    },

    -- AI
    ai = {
        ai_id = 0,
        target_rule = "",
        action_rule = "",
        params = {},
    },

    -- 站位 / 战斗参数
    battle = {
        pos = 0,
        range = 0,
        cost = 0,
        block = 0,
    },

    -- 掉落 / 奖励
    drops = {
        -- [1] = { type = "", id = 0, count = 0 },
    },

    -- 扩展参数
    tags = {},
    params = {},
    ext = {},
}

return Unit
```

---

## 3\. skill 文件模板

```markdown
local Skill = {
    -- 基础信息
    id = 0,
    key = "",
    name = "",
    desc = "",

    -- 技能类型
    skill_type = "",
    sub_type = "",
    quality = 0,

    -- 释放条件
    cost = {
        mp = 0,
        rage = 0,
        cd = 0,
        sp = 0,
    },

    cast = {
        cast_type = "",
        cast_time = 0,
        channel_time = 0,
        interruptible = false,
    },

    -- 目标规则
    target = {
        target_type = "",
        target_count = 0,
        target_range = 0,
        select_rule = "",
        camp_rule = "",
        params = {},
    },

    -- 效果列表
    effects = {
        -- [1] = {
        --     effect_type = "",
        --     value = 0,
        --     formula = "",
        --     chance = 0,
        --     duration = 0,
        --     interval = 0,
        --     params = {},
        -- },
    },

    -- 触发器
    triggers = {
        -- [1] = {
        --     trigger_type = "",
        --     condition = {},
        --     action = {},
        -- },
    },

    -- 命中 / 弹道 / 表现
    hit = {
        hit_type = "",
        hit_time = 0,
        bullet = "",
        effect = "",
        sound = "",
    },

    -- 冷却 / 限制
    cooldown = {
        round = 0,
        turn = 0,
        global_cd = 0,
    },

    limit = {
        use_count = 0,
        per_battle = 0,
        per_round = 0,
    },

    -- 关联 Buff
    buffs = {
        add = {
            -- [1] = 0,
        },
        remove = {
            -- [1] = 0,
        },
    },

    -- 扩展参数
    tags = {},
    params = {},
    ext = {},
}

return Skill
```

---

## 4\. buff 文件模板

```markdown
local Buff = {
    -- 基础信息
    id = 0,
    key = "",
    name = "",
    desc = "",

    -- Buff 类型
    buff_type = "",
    sub_type = "",
    priority = 0,
    stack_type = "",
    max_stack = 0,

    -- 生命周期
    duration = {
        round = 0,
        turn = 0,
        time = 0,
    },

    interval = 0,
    delay = 0,

    -- 生效对象
    target = {
        target_type = "",
        camp_rule = "",
        select_rule = "",
        params = {},
    },

    -- 属性修改
    modifiers = {
        -- [1] = {
        --     attr = "",
        --     mode = "",      -- add / pct / set
        --     value = 0,
        --     formula = "",
        -- },
    },

    -- 周期效果 / 触发效果
    effects = {
        -- [1] = {
        --     effect_type = "",
        --     trigger_type = "",
        --     value = 0,
        --     chance = 0,
        --     params = {},
        -- },
    },

    -- 触发器
    triggers = {
        on_add = {},
        on_remove = {},
        on_tick = {},
        on_hit = {},
        on_be_hit = {},
        on_dead = {},
    },

    -- 免疫 / 驱散 / 覆盖
    control = {
        dispellable = true,
        stealable = false,
        refreshable = true,
        replace_rule = "",
        immune_tags = {},
    },

    -- 表现
    view = {
        icon = "",
        effect = "",
        animation = "",
        sound = "",
    },

    -- 扩展参数
    tags = {},
    params = {},
    ext = {},
}

return Buff
```

---

## 5\. event 文件模板

```markdown
local Event = {
    -- 基础信息
    id = 0,
    key = "",
    name = "",
    desc = "",

    -- 事件类型
    event_type = "",
    sub_type = "",
    priority = 0,

    -- 触发条件
    trigger = {
        trigger_type = "",
        timing = "",
        condition = {
            -- [1] = {
            --     type = "",
            --     params = {},
            -- },
        },
        params = {},
    },

    -- 执行动作
    actions = {
        -- [1] = {
        --     action_type = "",
        --     target = {},
        --     params = {},
        -- },
    },

    -- 限制
    limit = {
        count = 0,
        per_round = 0,
        per_turn = 0,
        cooldown = 0,
    },

    -- 关联资源
    refs = {
        units = {},
        skills = {},
        buffs = {},
        battles = {},
    },

    -- 表现
    view = {
        effect = "",
        animation = "",
        sound = "",
        notice = "",
    },

    -- 扩展参数
    tags = {},
    params = {},
    ext = {},
}

return Event
```

---

如果你想要，我下一条可以继续直接给你一版\*\*更偏“配置表风格”\*\*的模板，也就是：

- 字段名更短
- 注释更少
- 更适合策划直接填表转 Lua
- 五类字段风格完全统一

你喜欢此风格吗？