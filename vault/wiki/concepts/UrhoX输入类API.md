---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, Lua, 输入处理, API, 键盘, 鼠标, 触摸, 手柄]
aliases: [Input类, Controls类, TouchState, JoystickState, UrhoX输入系统]
relates_to: [UrhoX引擎, UrhoX鼠标模式, 鼠标滚轮输入API陷阱]
supersedes: null
---
# UrhoX输入类API

## 概述

[[UrhoX引擎|UrhoX Lua]] 输入模块包含四个核心类：`Input`（主输入管理器）、`Controls`（按钮状态快照）、`TouchState`（触摸点状态）、`JoystickState`（手柄/摇杆状态）。

## 关键内容

### Input 类（主要 API）

**键盘查询**

```lua
input:GetKeyDown(KEY_SPACE)          -- 按键是否被按住
input:GetKeyPress(KEY_ESCAPE)        -- 本帧是否刚按下（按一次只触发一次）
input:GetScancodeDown(scancode)      -- 按扫描码查询（与键盘布局无关）
input:GetKeyName(KEY_A)              -- 返回键名字符串
```

**鼠标查询**

```lua
input:GetMouseButtonDown(MOUSEB_LEFT)   -- 鼠标按键按住
input:GetMouseButtonPress(MOUSEB_RIGHT) -- 鼠标按键刚按下
input:GetMousePosition()                -- IntVector2 绝对位置
input:GetMouseMove()                    -- IntVector2 相对移动量
input:GetMouseMoveWheel()               -- int 滚轮值（⚠️ 不是 mouseMove.z）
input:SetMousePosition(pos)             -- 设置鼠标位置
input:CenterMousePosition()             -- 居中鼠标
```

**修饰键**

```lua
input:GetQualifierDown(QUAL_SHIFT)  -- Shift/Ctrl/Alt 按住
input:GetQualifiers()               -- int 组合修饰键状态
```

**触摸**

```lua
input.numTouches                    -- 当前触摸点数量
input:GetTouch(index)               -- TouchState*（index 从 0 开始）
input:SetTouchEmulation(true)       -- 用鼠标模拟触摸
```

**手柄**

```lua
input.numJoysticks
input:GetJoystick(id)               -- JoystickState*
input:GetJoystickByName(name)
input:AddScreenJoystick(layoutFile) -- 添加虚拟摇杆（移动端）
```

**全屏与键盘**

```lua
input:SetToggleFullscreen(true)     -- 允许 F11 切换全屏
input:SetScreenKeyboardVisible(true) -- 显示软键盘（移动端）
```

### Controls 类（按钮状态快照）

用于在帧间传递和比较输入状态，适合联网和回放场景。

```lua
local ctrl = Controls.new()
ctrl:Reset()
ctrl:Set(CTRL_FORWARD, input:GetKeyDown(KEY_W))  -- 设置按钮状态

ctrl:IsDown(CTRL_FORWARD)                         -- 是否按住
ctrl:IsPressed(CTRL_FORWARD, prevControls)        -- 本帧是否刚按下（与上帧比对）

-- 属性
ctrl.buttons   -- unsigned，按钮位掩码
ctrl.yaw       -- float，偏航角
ctrl.pitch     -- float，俯仰角
ctrl.extraData -- VariantMap，自定义扩展数据
```

### TouchState 类

```lua
local touch = input:GetTouch(0)
touch.touchID       -- int
touch.position      -- IntVector2 当前位置
touch.lastPosition  -- IntVector2 上帧位置
touch.delta         -- IntVector2 移动量
touch.pressure      -- float 压力值（0.0~1.0）
touch:GetTouchedElement()  -- 触摸到的 UIElement
```

### JoystickState 类

```lua
local joy = input:GetJoystick(id)
joy:IsController()              -- 是否为游戏控制器
joy:GetNumButtons()
joy:GetButtonDown(index)        -- 按钮按住
joy:GetButtonPress(index)       -- 按钮刚按下
joy:GetAxisPosition(index)      -- float 轴值（-1.0~1.0）
joy:GetHatPosition(index)       -- int 方向键状态
```

### 常用枚举（不要用数字替代）

| 类别 | 枚举值 |
|------|--------|
| 鼠标按钮 | `MOUSEB_LEFT`, `MOUSEB_MIDDLE`, `MOUSEB_RIGHT` |
| 修饰键 | `QUAL_SHIFT`, `QUAL_CT[[强化学习|RL]]`, `QUAL_ALT` |
| 鼠标模式 | `[[UrhoX鼠标模式|MM_ABSOLUTE]]`, `[[UrhoX鼠标模式|MM_RELATIVE]]`, `MM_W[[rust-analyzer|RA]]P`, `MM_FREE` |
| 常用按键 | `KEY_SPACE`, `KEY_ESCAPE`, `KEY_RETURN`, `KEY_W/A/S/D` |

## 来源

- [[raw/articles/personal/ai-dev-kit/engine-docs/api/input.md]] — UrhoX Lua Input Module 完整 API 文档

## 相关

- [[UrhoX引擎]] — relates_to
- [[UrhoX鼠标模式]] — relates_to
- [[鼠标滚轮输入API陷阱]] — relates_to
