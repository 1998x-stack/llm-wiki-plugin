---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, 物理引擎, API陷阱, Lua, CollisionShape]
aliases: [CollisionShape直径, 碰撞体尺寸陷阱, SetSphere直径]
relates_to: [UrhoX引擎, UrhoX Lua开发准则]
supersedes: null
---
# CollisionShape直径参数陷阱

## 概述

[[UrhoX引擎|UrhoX]] 的 `CollisionShape` 圆形相关 API（`SetSphere`、`SetCylinder`、`SetCapsule`、`SetCone`）第一个参数均为**直径**而非半径，与 Unity 等引擎的习惯相反，是 AI 生成代码时的高频错误来源。

## 关键内容

### 受影响的 API

| API | 第一参数 | 示例 |
|-----|---------|------|
| `SetSphere(diameter)` | 直径 | `SetSphere(1.0)` → 半径 0.5 的球 |
| `SetCylinder(diameter, height)` | 直径, 高度 | `SetCylinder(1.0, 2.0)` |
| `SetCapsule(diameter, height)` | 直径, 高度 | `SetCapsule(1.0, 2.0)` |
| `SetCone(diameter, height)` | 直径, 高度 | `SetCone(1.0, 2.0)` |

### 错误现象

碰撞体只有可视模型的一半大小，导致角色穿模或物体落入地面。

### 根本原因

- 许多图形/物理库（如 Unity 的 `SphereCollider.radius`）使用半径，AI 有惯性思维
- 调用时只传数值（如 `SetSphere(0.5)`），参数名不可见，不易察觉

### 正确用法

```lua
-- ❌ 错误：把直径参数当半径用
shape:SetSphere(0.5)  -- 实际半径只有 0.25！

-- ✅ 正确：明确转换为直径
local radius = 0.5
shape:SetSphere(radius * 2)  -- 直径 1.0 = 半径 0.5

-- ✅ 直接用直径思维
shape:SetSphere(1.0)  -- 直径 1.0，半径 0.5
```

### 排查要点

- 看到 `SetSphere`/`SetCylinder`/`SetCapsule`/`SetCone` 调用时，确认传入值是直径
- 代码中使用 `diameter` 变量名提升可读性
- API 定义见源码：`engine/Source/Urho3D/LuaScript/pkgs/Physics/CollisionShape.pkg`

## 来源

- [[raw/articles/personal/ai-dev-kit/coding-insights/API-Usage/collision-shape-diameter-vs-radius.md]] — UrhoX Lua AI 开发 coding insight，分类 API-Usage，严重程度 Medium

## 相关

- [[UrhoX引擎]] — relates_to，该陷阱属于 UrhoX 物理 API 约定
- [[UrhoX Lua开发准则]] — relates_to，AI 生成代码的高频错误
