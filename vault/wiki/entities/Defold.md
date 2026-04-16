---
type: entity
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具与框架, 游戏]
aliases: [Defold引擎, King引擎]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.9
  - target: "[[游戏引擎架构]]"
    type: implements
    confidence: 0.85
  - target: "[[Love2D]]"
    type: relates_to
    confidence: 0.6
supersedes: null
entity_type: tool
---

# Defold

## 概述
Defold 是由 King/Defold Foundation 开发的 2D 游戏引擎，以消息传递架构为核心设计，使用 Lua 5.1 作为脚本语言，组件之间通过 U[[强化学习|RL]] 寻址和 hash 消息通信。

## 关键内容

1. **消息传递架构**：Defold 最核心的设计哲学。组件之间不直接调用方法，而通过 `msg.post(url, message_id, data)` 发送消息。`message_id` 用 `hash()` 压缩为整数，高效比较。

2. **脚本生命周期**：Script 组件有固定入口函数：
   - `init(self)` — 初始化，相当于 constructor
   - `update(self, dt)` — 每帧逻辑更新
   - `on_message(self, message_id, message, sender)` — 消息处理
   - `on_input(self, action_id, action)` — 输入事件
   - `final(self)` — 销毁回调

3. **U[[强化学习|RL]] 寻址系统**：对象、组件通过 U[[强化学习|RL]] 字符串（如 `"#sprite"`、`"/player#script"`）寻址。`msg.url("#sprite")` 获取当前 Game Object 的 sprite 组件引用。

4. **输入焦点机制**：脚本必须主动调用 `msg.post(".", "acquire_input_focus")` 才能接收输入事件，离开场景时需释放。

5. **游戏对象（GO）层级**：`go.get_position()` / `go.set_position()` 操作当前 GO，位置在世界空间中管理；物理碰撞响应通过消息 `contact_point_response` 传递。

6. **热更新策略**：Defold 支持运行时迭代 Lua 脚本，非注入式补丁方案，属于 Lua-first 运行时协议路线。

7. **Factory 对象创建**：`factory.create("#enemy_factory", pos, rot, props, scale)` 从 Factory 组件生成游戏对象，返回 ID；`go.delete(id)` 销毁单个对象，`go.delete_all()` 删除 factory 所有创建物。是 Defold 实现对象池/动态生成的核心机制。

8. **属性动画系统**：`go.animate(url, property, playback, to, easing, duration)` 对任意属性做补间动画（如 sprite 的 `tint`），支持 `PLAYBACK_ONCE_FORWARD`、`EASING_OUTSINE` 等常量。`go.get/set(url, key)` 读写组件属性，无需消息往返。

9. **fixed_update 与 on_reload**：`fixed_update(self, dt)` 以固定时间步执行（解耦物理与帧率）；`on_reload(self)` 在脚本热重载时调用，可用于重置内部状态、保证热迭代正确性。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，Defold 消息传递架构、脚本生命周期与 Lua 集成分析

## 相关
- [[Lua脚本宿主模式]] — Defold 是 "Lua 作为主逻辑层 + 消息驱动范式" 路线的代表实现
- [[游戏引擎架构]] — Defold 属于 Lua-first 引擎，脚本层即逻辑层
- [[Love2D]] — 同为 Lua 游戏框架，架构风格不同（回调 vs 消息）
