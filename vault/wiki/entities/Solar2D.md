---
type: entity
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具与框架, 游戏, 游戏开发]
aliases: [Corona SDK, Solar2D引擎, Corona]
relates_to:
  - target: "[[游戏引擎架构]]"
    type: implements
    confidence: 0.8
  - target: "[[Love2D]]"
    type: relates_to
    confidence: 0.6
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.85
supersedes: null
entity_type: tool
---

# Solar2D

## 概述
Solar2D（原 Corona SDK）是以 Lua 为唯一脚本语言的 2D 游戏框架，通过 Runtime 事件系统驱动游戏逻辑，内置 display 对象系统和 Box2D 物理集成，适合移动端 2D 游戏开发。

## 关键内容

1. **全 Lua 架构**：Solar2D 与 [[Love2D]] 类似，属于"全 Lua"引擎路线。开发者所有逻辑均用 Lua 编写，无需接触 C/[[C++]]。

2. **display 对象系统**：通过 `display.newRect`、`display.newCircle`、`display.newGroup` 等 API 创建可视对象。对象以 display group 组织层级，支持 `x/y/rotation/alpha` 等属性直接赋值。

3. **物理集成**：通过 `require("physics")` 引入，`physics.addBody(object, "static"|"dynamic", params)` 将任意 display 对象绑定物理属性（`radius/friction/bounce/density`）。重力通过 `physics.setGravity(x, y)` 设置。

4. **Runtime 事件系统**：使用 `Runtime:addEventListener(eventName, handler)` 订阅全局事件。`"enterFrame"` 用于帧更新，`"collision"` 用于碰撞处理，`"tap"` 用于触摸输入。与 [[Love2D]] 的回调函数风格不同，Solar2D 采用发布-订阅模式。

5. **视口跟随**：通过在 `enterFrame` 中移动 display group 实现摄像机跟随（`gameGroup.y = display.contentCenterY - player.y`），是 Solar2D 的惯用模式。

6. **移动端优先**：Solar2D 原名 Corona SDK，面向 iOS/Android 移动端设计，提供原生触摸事件和设备传感器接口。

7. **Composer 场景管理**：`require("composer")` 引入场景路由系统，`composer.gotoScene("scenes.game", {effect="fade", params={level=1}})` 切换场景。场景模块实现 `scene:create`、`scene:show`（will/did 两阶段）、`scene:hide`、`scene:destroy` 四个生命周期钩子，通过 `scene:addEventListener` 注册。

8. **关节系统**：`physics.newJoint("pivot", bodyA, bodyB, anchorX, anchorY)` 创建铰接关节，支持 `setRotationLimits` 限制旋转角度范围，是 Solar2D 实现布娃娃、机械臂等复杂物理结构的基础。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，Solar2D（Corona SDK）Lua 游戏开发架构与 API 分析

## 相关
- [[游戏引擎架构]] — Solar2D 属于 "全 Lua 引擎" 模式，性能上限受 Lua 解释器约束
- [[Lua脚本宿主模式]] — Solar2D 是 Lua 作为唯一逻辑层的典型实现
- [[Love2D]] — 同为全 Lua 2D 框架，Solar2D 偏移动端，Love2D 偏桌面端
