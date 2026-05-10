---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, 方法论]
aliases: [Lua配置驱动, Lua数据表, Lua工厂模式, Lua本地化, Lua技能系统]
relates_to:
  - target: "[[Lua模块系统]]"
    type: uses
    confidence: 0.9
  - target: "[[Lua-OOP]]"
    type: extends
    confidence: 0.75
  - target: "[[Lua-table]]"
    type: depends_on
    confidence: 0.95
supersedes: null
---
# Lua 数据驱动设计

## 概述
Lua 数据驱动设计将游戏内容（敌人属性、[[Skills|技能]]、本地化文本）以纯数据 table 定义，通过工厂函数按[[Configuration|配置]]实例化对象，实现逻辑与数据分离、无需重编译即可调整内容。

## 关键内容

### 配置表模式（纯数据，无代码）

```lua
-- config/enemies.lua — 仅数据，无逻辑
return {
    goblin = {
        hp = 30, speed = 120, damage = 8, reward = 5,
        sprite = "goblin.png",
        drop_table = {
            {item = "gold",   chance = 0.8, amount = {1, 5}},
            {item = "potion", chance = 0.1, amount = {1, 1}},
        }
    },
    troll = {
        hp = 200, speed = 60, damage = 35, reward = 20,
        sprite = "troll.png",
        abilities = {"regeneration", "boulder_throw"},
    }
}
```

### 数据驱动工厂

```lua
local EnemyConfig = require("config.enemies")

local function spawn_enemy(type_name, x, y)
    local cfg = EnemyConfig[type_name]
    assert(cfg, "Unknown enemy type: " .. type_name)
    return {
        type = type_name,
        hp = cfg.hp, max_hp = cfg.hp,
        speed = cfg.speed, damage = cfg.damage,
        x = x, y = y,
        sprite = load_sprite(cfg.sprite)
    }
end

-- 使用
local e = spawn_enemy("goblin", 100, 200)
```

### 数据 + 行为分离（技能系统）

```lua
-- 技能 DB：配置项包含执行函数，但结构是数据表
local SkillDB = {
    fireball = {
        name = "Fireball", cost = 20, cooldown = 2.0,
        execute = function(caster, target)
            local dmg = caster.magic_power * 2.5
            deal_damage(target, dmg, "fire")
            create_effect("fireball_hit", target.x, target.y)
        end
    },
    heal = {
        name = "Heal", cost = 30, cooldown = 5.0,
        execute = function(caster, target)
            target = target or caster
            local amount = caster.magic_power * 3
            target.hp = math.min(target.max_hp, target.hp + amount)
        end
    }
}

-- 使用方式统一，不需要 if/else 分支
local function cast_skill(caster, skill_name, target)
    local skill = SkillDB[skill_name]
    assert(skill, "Unknown skill: " .. skill_name)
    if caster.mp < skill.cost then return false, "Not enough MP" end
    caster.mp = caster.mp - skill.cost
    skill.execute(caster, target)
    return true
end
```

### 本地化系统

```lua
local Locale = {}

function Locale.load(lang)
    local ok, data = pcall(require, "locale." .. lang)
    Locale._strings = ok and data or require("locale.en")  -- 英语回退
end

function Locale.get(key, ...)
    local s = Locale._strings[key] or key  -- 未找到 key 时返回 key 本身
    if select("#", ...) > 0 then return string.format(s, ...) end
    return s
end

-- locale/zh.lua
return {
    ["menu.start"]    = "开始游戏",
    ["hud.hp"]        = "生命: %d/%d",
    ["dialog.npc_01"] = "勇者，欢迎来到这个世界！",
}

-- 使用
Locale.load("zh")
print(Locale.get("hud.hp", 80, 100))  -- "生命: 80/100"
```

### 设计原则

1. **数据与逻辑分离**：配置文件只有数据，工厂/系统只有逻辑，两者通过 key 关联
2. **assert 快速失败**：`assert(cfg, "Unknown type: " .. name)` 在开发阶段立即暴露拼写错误
3. **数组 drop_table 保持顺序**：用 `ipairs` 遍历，不用 `pairs`，避免顺序依赖问题
4. **函数作为数据字段**：技能 `execute` 函数存入 table，统一调用接口，避免大型 switch/case

### 扩展模式

- **热更新**：配置表是 `require` 加载的模块，清除 `package.loaded` 后重新 require 即可热更新数据
- **继承配置**：基础类型的字段可用 `__index` 实现配置继承，子类型只需声明差异字段
- **验证层**：工厂函数可加入字段校验（类型检查、范围约束），不污染配置文件

## 常见陷阱

- **配置文件混入逻辑**：配置中写复杂条件判断，破坏"纯数据"原则，后期难以工具化编辑
- **共享引用**：工厂直接返回 `cfg`（配置原表），多个实例共享同一 drop_table，修改会互相污染；应浅拷贝或按需引用
- **本地化 key 拼写**：key 不存在时 `Locale.get` 返回 key 字符串，上线前需扫描所有 key 是否已定义

## 来源
- [[raw/articles/programming/lua/lua-skill/references/patterns.md]] — Lua 高级模式参考，配置与数据驱动章节

## 相关
- [[Lua模块系统]] — 配置表以模块形式 require 加载和缓存
- [[Lua-OOP]] — 工厂模式与 OOP 配合，工厂返回 setmetatable 实例
- [[Lua-table]] — 配置表和实例均以 table 为载体
- [[Lua战斗配置目录结构]] — 数据驱动设计在战斗系统的六层目录落地实践
