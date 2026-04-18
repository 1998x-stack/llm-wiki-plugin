---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["游戏引擎", "正交投影", "相机", "数学", "UrhoX", "陷阱", "游戏开发"]
aliases: [orthoSize 2x因子, 正交相机缩放补偿, orthoSize半高度陷阱]
relates_to: [UrhoX引擎, 鼠标滚轮输入API陷阱, 设备像素比, NanoVG分辨率模式]
supersedes: null
---
# 正交缩放补偿orthoSize半高度因子

## 概述

[[UrhoX引擎|UrhoX]] 引擎中 `camera.orthoSize` 代表视野**全高度**，但投影[[矩阵]]内部使用 `orthoSize * 0.5` 作为半高度。手动计算屏幕到世界坐标转换时，若忽略此 0.5 因子会导致缩放补偿漂移。

## 关键内容

### 问题现象

实现"鼠标滚轮缩放时，鼠标指向的世界坐标保持固定"功能时，尽管数学公式看起来正确，每次缩放后锚点发生漂移，且漂移量与 `orthoSize` 变化量成正比（线性误差 = 存在常数因子错误的信号）。

### 根本原因：引擎源码中的 0.5 因子

在 `Camera.cpp` 的 `UpdateProjection()` 函数（约第 960 行）：

```cpp
float h = (1.0f / (orthoSize_ * 0.5f)) * zoom_;
```

`orthoSize_ * 0.5f` 就是关键的 2x 因子——引擎将 `orthoSize` 视为全高度，内部取半高度参与投影矩阵计算。

### 屏幕到视图空间的正确转换

```lua
-- 1. 屏幕坐标 → NDC (-1 到 1)
local ndcX = (screenX / screenWidth) * 2 - 1
local ndcY = 1 - (screenY / screenHeight) * 2  -- Y 轴翻转

-- 2. NDC → 视图空间偏移（必须乘以 0.5）
local viewX = ndcX * aspect * orthoSize * 0.5  -- ✅ 正确
local viewY = ndcY * orthoSize * 0.5            -- ✅ 正确

-- ❌ 错误（忘记 0.5）：
-- local viewX = ndcX * aspect * orthoSize
-- local viewY = ndcY * orthoSize
```

### 缩放补偿完整实现（等距视角）

```lua
local function CalcZoomCompensation(screenX, screenY, oldOrthoSize, newOrthoSize)
    local ndcX = (screenX / screenWidth) * 2 - 1
    local ndcY = 1 - (screenY / screenHeight) * 2
    local deltaOrtho = oldOrthoSize - newOrthoSize

    -- 关键：乘以 0.5，与引擎投影矩阵对齐
    local viewDeltaX = ndcX * aspect * deltaOrtho * 0.5
    local viewDeltaY = ndcY * deltaOrtho * 0.5

    -- 转换到世界空间（沿相机 right/up 方向）
    local offsetX = camRight.x * viewDeltaX + camUp.x * viewDeltaY
    local offsetY = camRight.y * viewDeltaX + camUp.y * viewDeltaY
    local offsetZ = camRight.z * viewDeltaX + camUp.z * viewDeltaY

    -- 与 y=0 平面相交补偿
    if math.abs(camForward.y) > 0.001 then
        local t = -offsetY / camForward.y
        offsetX = offsetX + camForward.x * t
        offsetZ = offsetZ + camForward.z * t
    end

    return offsetX, offsetZ
end
```

### 调试策略

- **误差与变化量成线性关系** → 常数因子错误（2x 或 0.5x），首先检查此类因子
- **引擎函数交叉验证**：用 `GetScreenRay()` 等引擎 API 验证手动计算结果
- **源码是最终真理**：当 API 文档不明确时，查阅引擎 C++ 源码

### 经验规律

| 参数 | 含义 | 内部使用 |
|------|------|---------|
| `orthoSize` | 视野全高度 | `orthoSize * 0.5`（半高度）参与投影矩阵 |
| 投影缩放因子 h | `1 / (orthoSize * 0.5) * zoom` | 直接用于[[矩阵]]构造 |

## 来源

- [[raw/articles/personal/ai-dev-kit/coding-insights/Math-Algorithm/orthographic-zoom-compensation.md]] — 正交相机缩放补偿：orthoSize 参数的 2x 因子陷阱（2026-02-05，等距视角游戏实战记录）

## 相关

- [[UrhoX引擎]] — relates_to（此陷阱源于 UrhoX Camera.cpp 投影矩阵实现）
- [[鼠标滚轮输入API陷阱]] — relates_to（同为 UrhoX 输入/相机交互陷阱）
- [[设备像素比]] — relates_to（屏幕坐标系转换相关概念）
- [[NanoVG分辨率模式]] — relates_to（同属坐标系与分辨率适配范畴）
