---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏, 工具与框架, 游戏开发]
aliases: [delta time, dt运动, 帧率无关移动, 时间步移动, frame-rate-independent movement]
relates_to:
  - target: "[[游戏主循环模式]]"
    type: part_of
    confidence: 0.95
  - target: "[[Love2D]]"
    type: used_in
    confidence: 0.9
supersedes: null
---

# Delta-time运动模式

## 概述
Delta-time（dt）运动模式：以帧间时间差乘以速度[[计算]]位移，使物体移动速度与帧率无关，保证跨帧率一致性。

## 关键内容

1. **核心公式**：`position += speed * dt`，其中 `dt` 为相邻两帧之间经过的秒数。
   - 60fps 时 dt ≈ 0.016 秒，每帧移动 `speed * 0.016` 像素
   - 30fps 时 dt ≈ 0.033 秒，每帧移动 `speed * 0.033` 像素
   - 每秒总位移 ≈ `speed` 像素，与帧率无关

2. **为什么需要 dt**：不同设备帧率不同（30/60/120fps），若直接 `position += speed`，高帧率设备物体移动更快，低帧率设备移动更慢，导致游戏体验不一致。

3. **[[Love2D]] 中的实现**：`love.update(dt)` 回调自动传入帧间时间差，直接用于[[计算]]：
   ```lua
   function love.update(dt)
       if love.keyboard.isDown("right") then
           x = x + speed * dt
       end
   end
   ```

4. **单位换算**：`speed` 的单位为"像素/秒"，而非"像素/帧"。声明 `speed = 200` 表示每秒移动 200 像素。

5. **适用范围**：所有基于 update 循环的实时游戏均应使用 dt 模式，包括角色移动、粒子系统、动画插值、物理模拟等。

## 来源
- [[Lua 移动方块示例]] — Love2D 20行示例，展示 speed * dt 实现帧率无关移动

## 相关
- [[游戏主循环模式]] — dt 在 update(dt) 回调中由引擎自动提供
- [[Love2D]] — Love2D 的 love.update(dt) 是 dt 运动模式的典型使用场景
