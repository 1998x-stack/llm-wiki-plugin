---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, Lua, 输入处理, 鼠标, Web平台]
aliases: [鼠标模式, MouseMode, MM_RELATIVE, MM_ABSOLUTE, Pointer Lock]
relates_to: [UrhoX引擎, UrhoX Lua开发准则, 鼠标滚轮输入API陷阱]
supersedes: null
---
# UrhoX鼠标模式

## 概述

[[UrhoX引擎|UrhoX]] 引擎默认显示鼠标光标（`mouseVisible = true`）。对于需要鼠标控制视角的游戏（FPS/TPS/飞行模拟），需在启动时将 `input.mouseMode` 设为 `MM_RELATIVE`。

## 关键内容

### 四种鼠标模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `MM_ABSOLUTE` | 默认，鼠标自由移动，可显示/隐藏光标 | 菜单、RTS、编辑器 |
| `MM_RELATIVE` | 鼠标锁定在窗口内，**强制隐藏光标**，获取相对移动量 | FPS、TPS、飞行模拟 |
| `MM_WRAP` | 鼠标到达边界时环绕到另一边 | 特殊需求 |
| `MM_FREE` | 鼠标不被限制，即使隐藏也不锁定 | 需要自定义光标渲染 |

### 典型使用场景

```lua
-- 普通 UI 界面（菜单、商店等）
input.mouseMode = MM_ABSOLUTE
input.mouseVisible = true

-- FPS/TPS 游戏主循环
input.mouseMode = MM_RELATIVE
-- mouseVisible 自动设为 false，用 input:GetMouseMove() 获取移动量

-- RTS/策略游戏（自定义 UI 光标）
input.mouseMode = MM_ABSOLUTE
input.mouseVisible = false  -- 隐藏系统光标，使用 UI Cursor 组件

-- 暂停菜单时临时释放鼠标
input.mouseMode = MM_ABSOLUTE
input.mouseVisible = true
```

### ⚠️ Web 平台特殊限制（Pointer Lock API）

在 Web 平台上，`MM_RELATIVE` 使用浏览器的 Pointer Lock API，有以下重要限制：

| 限制 | 说明 |
|------|------|
| **ESC 强制退出** | 用户按 ESC，浏览器强制退出 Pointer Lock，`mouseMode` 自动变为 `MM_FREE` |
| **ESC 后冷却期** | ESC 退出后约 1-2 秒内无法重新锁定，否则报 `SecurityError`（不影响逻辑，仅控制台报错） |
| **需要用户交互** | 必须在用户点击事件中请求锁定 |

**推荐做法**：使用 `Sample.lua` 提供的 `SampleInitMouseMode(MM_RELATIVE)` 函数，自动处理 Web 平台兼容（点击恢复锁定、ESC 退出等）。

```lua
-- LuaScripts/Utilities/Sample.lua 中已封装：
-- SampleInitMouseMode(MM_RELATIVE)
-- HandleMouseModeRequest
-- HandleMouseModeChange
```

### 属性与方法

```lua
input.mouseMode          -- 读写 MouseMode
input.mouseVisible       -- 读写 bool
input.mouseGrabbed       -- 读写 bool
input.mouseLocked        -- 只读，当前是否锁定
input:GetMouseMove()     -- IntVector2，鼠标移动量
input:IsMouseLocked()    -- bool
```

## 来源

- [[raw/articles/personal/ai-dev-kit/engine-docs/api/input.md]] — UrhoX Lua Input Module API 文档（鼠标模式设置指南章节）

## 相关

- [[UrhoX引擎]] — relates_to
- [[UrhoX Lua开发准则]] — relates_to
- [[鼠标滚轮输入API陷阱]] — relates_to
