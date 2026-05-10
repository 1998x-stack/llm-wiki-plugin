---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [Lua, 编程语言, 游戏, 工具, 游戏开发]
aliases: [Lua配置文件模板, Lua数据文件结构, Lua游戏数据模块]
relates_to: [Lua-table, Lua-OOP, Lua-metatable]
supersedes: null
---
# Lua 游戏配置文件模板

## 概述
以 `local T = {...} return T` 为[[骨骼系统|骨架]]的 Lua 游戏数据文件约定，每文件返回一个 table，作为游戏实体[[Configuration|配置]]模块使用。

## 关键内容
1. **模块[[骨骼系统|骨架]]约定**：每个[[Configuration|配置]]文件定义一个局部 table（`local Battle = {...}`）并在末尾 `return Battle`，文件本身即模块，调用方通过 `require` 或 `dofile` 加载得到该 table。这是 Lua 游戏项目中最常见的数据组织惯用法。
2. **五类核心模板**：
   - **battle**：战场[[Configuration|配置]]，含 id/key/name/desc、战斗[[Configuration|配置]]（type/mode/round_limit/time_limit）、attacker/defender 双方阵营、scene 场景、win/lose 条件、waves 波次、phases 阶段、rewards 奖励。
   - **unit**：单位[[Configuration|配置]]，含基础信息、unit_type/camp/race/job、展示资源（model/icon/portrait）、等级/品质、attr 基础属性（hp/atk/def/spd/cri/ten/hit/dodge/rage）、growth 成长属性、skills [[Skills|技能]]组（normal/active/passive/ultimate）、buffs/traits、ai 策略、battle 站位参数、drops 掉落。
   - **skill**：[[Skills|技能]][[Configuration|配置]]，含[[Skills|技能]]类型、cost（mp/rage/cd/sp）、cast（cast_type/cast_time/channel_time/interruptible）、target 目标规则（target_type/count/range/select_rule/camp_rule）、effects 效果列表（含 formula/chance/duration）、triggers 触发器、hit 命中表现、cooldown 冷却、limit 使用限制、关联 buffs。
   - **buff**：增益/减益[[Configuration|配置]]，含 buff_type/priority/stack_type/max_stack、duration（round/turn/time）、interval/delay、modifiers 属性修改（attr/mode=add|pct|set/value/formula）、effects 周期效果、triggers（on_add/on_remove/on_tick/on_hit/on_be_hit/on_dead）、control（dispellable/stealable/refreshable/replace_rule/immune_tags）、view 表现。
   - **event**：事件[[Configuration|配置]]，含 event_type/priority、trigger（trigger_type/timing/condition[]）、actions[]（action_type/target/params）、limit（count/per_round/per_turn/cooldown）、refs 关联资源（units/skills/buffs/battles）、view 表现。
3. **通用字段约定**：所有五类模板末尾均含 `tags = {}` / `params = {}` / `ext = {}` 三个扩展字段，作为未来需求的预留槽位，避免频繁改动已有字段。
4. **嵌套 table 结构**：复杂属性用嵌套 table 表达（如 `attr = { hp=0, atk=0, ... }`），数组型字段用整数下[[标注]]释示例（`-- [1] = {...}`）便于策划填表理解。
5. **返回单 table vs 返回多值**：此模式返回单一 table，而非多个字段分散定义，便于工具链做序列化、热重载和版本 diff。

## 来源
- [[Lua 文件模板]] — ChatGPT 对话，给出五类 Lua 游戏配置文件的可复制空白骨架

## 相关
- [[Lua-table]] — 配置模板的核心数据结构，所有字段均为 table 嵌套
- [[Lua-OOP]] — 同样以 table 返回模块，区别在于 OOP 侧重行为方法，配置模板侧重纯数据
- [[Lua-metatable]] — 若需对配置 table 添加默认值合并或只读保护，可用 metatable 的 __index/__newindex
