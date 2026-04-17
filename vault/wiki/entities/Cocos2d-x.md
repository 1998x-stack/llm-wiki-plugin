---
type: entity
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具与框架, 游戏, 游戏开发]
aliases: [Cocos2d, cocos2d-lua, Cocos引擎]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.88
  - target: "[[Lua C API 绑定层]]"
    type: uses
    confidence: 0.85
  - target: "[[游戏引擎架构]]"
    type: implements
    confidence: 0.8
supersedes: null
entity_type: tool
---

# Cocos2d-x

## 概述
Cocos2d-x 是开源跨平台 2D 游戏引擎，通过官方 cocos2d-lua binding 支持 Lua 脚本，提供 Scene/Layer/Sprite 层级节点系统、动作系统和物理引擎集成。

## 关键内容

1. **Lua 绑定机制**：Cocos2d-x 通过 `tolua++` 自动生成 C++ → Lua 的 wrapper 代码，C++ 类以 `cc.ClassName` 形式暴露给 Lua。引擎核心类（Scene、Layer、Sprite 等）均可在 Lua 侧直接调用。

2. **节点系统**：以 Scene/Layer 为根，Sprite 等节点通过 `addChild(node, zOrder)` 构建层级树。位置用 `cc.p(x, y)` 表示，锚点/位置/旋转在 Lua 侧设置。

3. **动作系统**：`cc.MoveBy`、`cc.MoveTo`、`cc.Sequence`、`cc.RepeatForever` 等动作对象通过 `sprite:runAction(action)` 驱动，是 Cocos2d 的核心动画机制。

4. **物理集成**：通过 `scene:getPhysicsWorld()` 获取物理世界，`cc.PhysicsBody:createBox` 创建刚体，附加到节点上实现物理模拟。

5. **事件系统**：`cc.EventListenerTouchOneByOne` 等监听器通过 `EventDispatcher` 注册，`registerScriptHandler` 将 Lua 函数作为回调。

6. **生命周期路线**：属于 Lua 脚本宿主模式中的 "Cocos/Lua 官方桥路线"，ComponentLua 直接绑定节点生命周期，热更新通过替换 Lua 脚本文件实现。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，分析 Cocos2d-x Lua 绑定架构与 API 使用模式

## 相关
- [[Lua脚本宿主模式]] — Cocos/Lua 是四大工业方案之一
- [[Lua C API 绑定层]] — tolua++ 是典型的代码生成自动绑定方案
- [[游戏引擎架构]] — Cocos2d-x 代表 C++ 引擎 + Lua 脚本模式
