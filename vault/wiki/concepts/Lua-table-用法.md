---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [Lua, 编程语言, 游戏开发, Lua编程]
aliases: ["Lua table", "Lua 表", "Lua table 用法"]
relates_to:
  - target: "[[lua-language-server]]"
    type: part_of
    confidence: 0.6
  - target: "[[Lua Metatable]]"
    type: extends
    confidence: 0.8
supersedes: null
---

# Lua table 用法

## 概述
Lua table 是 Lua 唯一的复合数据结构，同时覆盖 array、map、object、struct、set、namespace 六种语义，是游戏开发中的万能容器。

## 关键内容

### 核心用途（游戏开发）

1. **配置表**：存静态数据（关卡、角色、技能、掉落、商店），是数据驱动架构的核心。
   ```lua
   local heroConfig = { id = 1001, name = "Knight", hp = 1200, skills = {101, 102, 103} }
   ```

2. **数组 / 列表容器**：存实体列表、背包列表、敌人波次，配合 `ipairs` 遍历。

3. **字典 / Map**：key-value 快速索引（playerId → 玩家数据、buffId → buff 实例），比线性遍历高效。

4. **模拟对象**：table + metatable 实现 OOP，`__index` 做继承，`setmetatable` 绑定方法。
   ```lua
   local Player = {}
   Player.__index = Player
   function Player:new(name) ... end
   ```

5. **状态存储**：运行时状态（分数、波次、暂停标志）、玩家存档、战斗上下文。

6. **事件系统 / 回调注册**：table 存监听器列表，消息分发、UI 按钮回调、状态机回调。

7. **组件系统 / ECS 风格**：entity 以 table 存组件数据，位置/速度/HP 各自为嵌套 table。

8. **协议消息结构**：客户端/服务器消息对象，发送前编码为 JSON / protobuf。

9. **树形结构**：任务树、UI 节点树、剧情分支，用嵌套 table 自然表达。

10. **缓存 / 对象池**：spriteCache、资源引用表，避免重复加载。

### 典型混合模式
真实项目一个系统同时用多种角色：
```lua
local SkillSystem = {
    configs = {},      -- 技能配置表（静态数据）
    activeSkills = {}, -- 当前实例（运行时状态）
    listeners = {},    -- 事件监听（回调）
    cache = {}         -- 运行缓存
}
```

### 常见坑

| 坑 | 说明 |
|---|---|
| 数组与字典混用 | `{1, 2, a=10}` 遍历和 `#` 语义混乱 |
| 浅拷贝问题 | `b = a` 只是引用，修改 `b.pos` 影响 `a` |
| nil 删键 | `t.hp = nil` 是删除字段，不是置空值 |
| GC 压力 | 高频 new table（子弹/特效循环）造成垃圾回收抖动 |
| pairs vs ipairs | `ipairs` 适合连续数组；`pairs` 适合字典或混合表 |

### 游戏战斗系统 5 层组织模型

手游战斗逻辑最常见的 table 分层（Unity/xLua、Cocos Lua 均适用）：

1. **配置表**：静态只读数据，按 id 索引 `cfg[id] -> row`，不写入运行时状态
2. **对象表**：单位/技能/Buff 实例，分块组织（base/attr/state/combat 等子 table）
3. **索引表**：同一批数据建多份视图——数组（遍历）+ map（O(1) 查询）+ 分组 map
4. **上下文表**：一次技能/伤害结算的临时载体，统一传参避免参数爆炸
5. **事件/消息表**：逻辑层产出 event table，表现层消费，实现逻辑/表现解耦

核心原则：**配置负责定义，状态负责变化，索引负责查询，上下文负责流程，事件负责解耦**

### Unity/xLua 特有模式

- **Lua 侧逻辑对象**：`setmetatable + __index` 模拟 class，管理逻辑状态
- **Lua/C# 生命周期分离**：`self.view = {go=csObj}` 与 `self.data = {hp=100}` 分开，避免引用悬挂
- **代理缓存表**：`cachedAttr = {atk=csUnit:GetAtk()}` 减少高频跨语言访问开销

### 战斗对象表 4 种方案对比

| 方案 | 特征 | 适用 |
|------|------|------|
| 大平铺表 | 字段全摊平，快速但易失控 | 小项目/原型 |
| 分块对象表 | `base/attr/state/com[[bat]]` 分块，清晰维护 | 中大型手游（推荐） |
| ECS-ish | `Position[entity]` 等组件 table，批处理友好 | 大量单位/数据驱动 |
| 状态树+事件流 | `[[bat]]tleState + eventQueue`，适合录像/回放 | 复杂战斗/战报需求 |

### 实战坑（补充）

| 坑 | 说明 |
|---|---|
| 配置表写运行时数据 | `SkillCfg[1001].cd = 0` 污染所有实例 |
| 数组/map 混用不自知 | `t[1]=a; t[10001]=b` 导致遍历/length/序列化异常 |
| ctx table 成垃圾桶 | 字段越塞越多，生命周期不清，残留字段跨阶段污染 |
| 对象表混管逻辑/表现/网络 | 短期快，迭代后牵一发动全身 |

## 来源
- [[Lua table 用法]] — ChatGPT 会话：Lua table 在游戏开发中的典型用法 (https://chatgpt.com/c/69d65da5-a1e4-8322-bd0c-907517ed043e)
- [[Lua表格组织方式]] — ChatGPT 对话：Unity/xLua、Cocos Lua、手游战斗系统中 table 组织模式 (https://chatgpt.com/c/69d65e85-e85c-8321-855d-38aeba85c657)

## 相关
- [[lua-language-server]] — part_of（Lua 生态）
- [[Lua-table-游戏战斗架构]] — 战斗系统 table 架构模板与落地模式
