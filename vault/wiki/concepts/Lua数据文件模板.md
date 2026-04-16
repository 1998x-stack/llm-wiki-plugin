---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [Lua, 编程语言, 游戏开发, 数据驱动, Lua编程]
aliases: [Lua配置文件模板, Lua游戏数据模板, return table模式]
relates_to: [Lua-table, Lua-OOP, Love2D]
supersedes: null
---
# Lua 数据文件模板

## 概述
Lua 游戏开发中常见的数据文件惯用法：每个文件定义并 `return` 一张 table，作为可热加载的结构化配置/数据单元。

## 关键内容
1. **return table 模式**：文件以 `local T = { ... } return T` 收尾，调用方用 `require("path")` 获得该 table。无全局污染，可被模块系统缓存或重加载。
2. **五类典型模板**：
   - **Battle**：含基础信息、战斗配置、attacker/defender 双方单位列表、地图场景、胜负条件、波次/阶段、奖励等字段。
   - **Unit**：含基础信息、类型阵营、展示资源（model/icon/portrait）、等级品质、基础属性（hp/atk/def/spd/cri…）、成长属性、技能列表、Buff/特性、AI 配置、站位参数、掉落奖励。
   - **Skill**：含技能类型、释放条件（cost/cast）、目标规则（ta[[ripgrep|rg]]et）、效果列表（effects）、触发器（triggers）、命中/弹道、冷却限制、关联 Buff。
   - **Buff**：含 Buff 类型、堆叠规则（stack_type/max_stack）、生命周期（duration/interval/delay）、属性修改（modifiers）、周期效果、触发器（on_add/on_remove/on_tick/on_hit…）、免疫/驱散/覆盖控制、表现资源。
   - **Event**：含事件类型、触发条件（trigger_type/timing/condition）、执行动作（actions）、限制（count/per_round）、关联资源（refs）、表现。
3. **扩展字段三件套**：每类模板末尾统一保留 `tags = {}`、`params = {}`、`ext = {}`，用于业务扩展而不破坏基础结构。
4. **嵌套 table 作子结构**：复杂字段（如 attacker/defender、ta[[ripgrep|rg]]et、cost、view）用内嵌 table 分组，保持同类字段聚合、可独立访问。
5. **注释即文档**：数组元素模板以注释形式预置（`-- [1] = { ... }`），策划可对照填写，LLM 或脚本可解析生成代码。
6. **配置表风格变体**：字段名可进一步缩短、注释精简，使文件更适合策划直接填表后转 Lua，同类字段风格完全统一。

## 来源
- [[Lua 文件模板]] — ChatGPT 对话，给出五类 Lua 游戏数据文件的可复制空白骨架（battle/unit/skill/buff/event）

## 相关
- [[Lua-table]] — return table 模式的基础数据结构
- [[Lua-OOP]] — 同样基于 table，但侧重行为建模；数据文件模板侧重纯数据配置
- [[Love2D]] — 常见的 Lua 游戏框架，数据文件模板在其生态中广泛使用
