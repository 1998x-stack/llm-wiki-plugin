---
type: entity
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 3
tags: [工具与框架, 游戏, 游戏开发]
aliases: [LÖVE, Love2D, LOVE, love2d, LÖVE2D]
relates_to:
  - target: "[[游戏引擎架构]]"
    type: implements
    confidence: 0.8
  - target: "[[游戏主循环模式]]"
    type: uses
    confidence: 0.9
  - target: "[[Defold]]"
    type: relates_to
    confidence: 0.6
  - target: "[[Solar2D]]"
    type: relates_to
    confidence: 0.6
supersedes: null
entity_type: tool
---

# Love2D

## 概述
Love2D（LÖVE）是以 Lua 为脚本语言的开源 2D 游戏框架，提供窗口、图形、输入、音频等游戏能力，开发者只需在回调函数中填写逻辑即可跑起游戏。

## 关键内容

1. **定位**：Love2D 不是完整游戏引擎，而是"游戏能力提供者"。Lua 写逻辑，LÖVE 提供平台能力（开窗口、画图、播放声音、接收键盘输入）。

2. **核心回调**：引擎在生命周期中主动调用开发者定义的函数：
   - `love.load()` — 启动时执行一次，初始化变量/加载资源
   - `love.update(dt)` — 每帧更新逻辑，`dt` 为帧间时间差（秒）
   - `love.draw()` — 每帧绘制画面
   - `love.keypressed(key)` — 按键按下瞬间触发

3. **主要模块**：
   - `love.graphics` — 绘图（`print`、`rectangle`、`circle`、`draw`、`newImage`）
   - `love.keyboard` — 键盘（`isDown` 持续检测、`keypressed` 单次触发）
   - `love.audio` — 音频（`newSource`）
   - `love.window` — 窗口管理（`setTitle`）

4. **输入两种模式**：`love.keyboard.isDown()` 适合持续移动；`love.keypressed` 适合单次触发动作（跳跃、发射子弹）。

5. **dt 时间无关移动**：`x = x + speed * dt` 使物体速度与帧率无关，保证低帧率/高帧率下行为一致。

6. **[[Lua-table-用法|Lua table]] 作为对象**：惯用 table 组织角色状态（`player = {x, y, speed}`），是 Love2D 项目的标准写法。

7. **物理模块**：`love.physics.newWorld(gx, gy)` 创建物理世界，`newBody/newRectangleShape/newFixture` 创建刚体。每帧调用 `world:update(dt)` 推进物理模拟。

8. **内部实现机制**：LÖVE 在 [[C++]] 层实现所有 Module（graphics、audio、physics 等），通过 `luaL_newlib` 注册为 Lua 模块，[[游戏主循环模式|主循环]]从 [[C++]] 触发 `love.update(dt)` 和 `love.draw()`。这是典型的 [[C++]] 引擎 + 全 Lua 暴露 API 的架构模式。

9. **配置文件 conf.lua**：`love.conf(t)` 在引擎初始化前执行，控制窗口尺寸、VSYNC、MSAA、模块开关等：`t.window.width/height`、`t.window.resizable`、`t.window.vsync`、`t.window.msaa`、`t.modules.physics`。是 Love2D 项目的标准初始化入口。

10. **完整生命周期回调集**：除核心三件套外，还有 `love.quit()`（返回 true 可取消退出）、`love.resize(w,h)`、`love.focus(f)`、`love.mousereleased/moved/wheelmoved`、`love.touchpressed/released`、`love.gamepadpressed/released`、`love.errhand(msg)`（全局错误处理）。

11. **Canvas 离屏渲染**：`love.graphics.newCanvas(w,h)` 创建离屏渲染目标，`love.graphics.setCanvas(canvas)` 切换渲染目标（nil 恢复默认屏幕），配合 Shader 实现后处理效果。`love.graphics.setShader(shader)` / `love.graphics.newShader(vert,frag)` 支持自定义着色器。

## 来源
- [[Lua 与 Love2D 交互]] — ChatGPT 对话整理，介绍 Lua 与 Love2D 的交互机制、回调系统与 API 用法
- [[Lua 移动方块示例]] — 20 行示例代码，展示 love.keyboard.isDown 持续检测与 love.graphics.rectangle 绘制
- [[lua-gameengine-deep-research]] — 深度研究报告，第4.1节 LÖVE2D 生命周期回调、物理集成与内部实现机制

## 相关
- [[游戏引擎架构]] — Love2D 是轻量 2D 游戏框架，Scripting 层用 Lua
- [[游戏主循环模式]] — Love2D 的 load/update/draw 是游戏主循环模式的典型实现
- [[Defold]] — 同为 Lua 游戏框架，Defold 使用消息传递架构而非回调函数风格
- [[Solar2D]] — 同为全 Lua 2D 框架，Solar2D 偏移动端，Love2D 偏桌面端
