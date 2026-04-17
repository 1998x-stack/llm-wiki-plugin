# 正交相机缩放补偿：orthoSize 参数的 2x 因子陷阱

**日期**: 2026-02-05
**分类**: Math-Algorithm
**严重程度**: High
**游戏/项目**: TapCode-User_Workspace（等距视角游戏）

---

## 🐛 问题现象 (Observed Behavior)

实现"鼠标滚轮缩放时，鼠标指向的世界坐标保持固定"功能时，尽管数学公式看起来正确，但鼠标指向的地面点在缩放后始终发生偏移。

**预期行为**：缩放前后，鼠标指向的世界坐标不变  
**实际行为**：每次缩放后，锚点发生漂移，且漂移量与 orthoSize 变化量成正比

**关键日志线索**：
```
[Zoom] ortho=8.00->6.80 鼠标=(1105,531)
  锚点=(0.371,0.519) delta=(0.1113,0.1558)
  引擎验证: (0.249,0.419) 误差=(0.1224,0.1002) ⚠️
```

---

## 🔍 问题原因 (Root Cause Analysis)

### 根本原因

**UrhoX 引擎的正交投影矩阵使用 `orthoSize * 0.5` 作为半视野高度**，而不是直接使用 `orthoSize`。

这意味着：
- `orthoSize = 8.0` → 视野半高度 = 4.0，视野总高度 = 8.0
- 视野的高度等于 `orthoSize`，但内部计算使用的是半高度

### 引擎源码证据

在 `Camera.cpp` 的 `UpdateProjection()` 函数中：

```cpp
// 第 960 行附近
float h = (1.0f / (orthoSize_ * 0.5f)) * zoom_;
```

这里 `orthoSize_ * 0.5f` 就是关键的 **2x 因子**。

### AI 的错误假设

AI 在实现缩放补偿时，假设 `orthoSize` 直接代表视野半高度：

```lua
-- ❌ 错误假设：orthoSize 是半高度
local viewDeltaX = ndcX * aspect * deltaOrtho
local viewDeltaY = ndcY * deltaOrtho
```

实际上应该是：

```lua
-- ✅ 正确：orthoSize 是全高度，需要 * 0.5
local viewDeltaX = ndcX * aspect * deltaOrtho * 0.5
local viewDeltaY = ndcY * deltaOrtho * 0.5
```

---

## ✅ 解决方案 (Solution)

### 错误做法 (Wrong Approach)

```lua
local function CalcZoomCompensation(screenX, screenY, oldOrthoSize, newOrthoSize)
    local ndcX = (screenX / screenWidth) * 2 - 1
    local ndcY = 1 - (screenY / screenHeight) * 2
    local deltaOrtho = oldOrthoSize - newOrthoSize
    
    -- ❌ 错误：没有乘以 0.5
    local viewDeltaX = ndcX * aspect * deltaOrtho
    local viewDeltaY = ndcY * deltaOrtho
    
    -- ... 转换到世界空间
end
```

### 正确做法 (Correct Approach)

```lua
local function CalcZoomCompensation(screenX, screenY, oldOrthoSize, newOrthoSize)
    local ndcX = (screenX / screenWidth) * 2 - 1
    local ndcY = 1 - (screenY / screenHeight) * 2
    local deltaOrtho = oldOrthoSize - newOrthoSize
    
    -- ✅ 正确：乘以 0.5（因为引擎使用 orthoSize * 0.5 作为半视野）
    local viewDeltaX = ndcX * aspect * deltaOrtho * 0.5
    local viewDeltaY = ndcY * deltaOrtho * 0.5
    
    -- 转换到世界空间（沿相机 right 和 up 方向）
    local offsetX = camRight.x * viewDeltaX + camUp.x * viewDeltaY
    local offsetY = camRight.y * viewDeltaX + camUp.y * viewDeltaY
    local offsetZ = camRight.z * viewDeltaX + camUp.z * viewDeltaY
    
    -- 射线与 y=0 平面相交的补偿
    if math.abs(camForward.y) > 0.001 then
        local t = -offsetY / camForward.y
        offsetX = offsetX + camForward.x * t
        offsetZ = offsetZ + camForward.z * t
    end
    
    return offsetX, offsetZ
end
```

---

## 💡 经验教训 (Lessons Learned)

### 1. 数学公式必须与引擎实现对齐

当手动实现与引擎相关的数学计算时，必须确保：
- 了解引擎内部使用的约定（半径 vs 直径，半高度 vs 全高度）
- 验证公式与引擎的 `GetScreenRay()` 等函数结果一致

### 2. 调试策略：引擎验证 + 误差对比

```lua
-- 用引擎函数验证手动计算结果
local finalWorld = ScreenToWorld(mouseX, mouseY)  -- 使用引擎的 GetScreenRay
local errorX = math.abs(finalWorld.x - anchorX)
local errorZ = math.abs(finalWorld.z - anchorZ)
print(string.format("误差=(%.4f,%.4f) %s", errorX, errorZ, 
    (errorX > 0.05 or errorZ > 0.05) and "⚠️" or "✓"))
```

### 3. 误差模式识别

当误差与变化量成线性关系时，通常意味着存在一个常数因子错误（如 2x、0.5x）。

### 4. 引擎源码是最终真理

当文档不完整时，查阅引擎源码是唯一可靠的方法。对于 AI Agent 而言，这些关键细节需要提前记录在知识库中。

---

## 🤖 AI 局限性分析 (AI Limitations Analysis)

**问题性质分类**：
- [ ] LLM 根本局限（数学推理、空间想象等）
- [x] 知识/经验不足（可通过学习改进）
- [ ] 上下文理解错误
- [ ] 其他

**为什么 AI 反复修错？**

1. **缺乏引擎内部实现细节**：AI 无法访问 C++ 源码，只能基于 API 文档推断
2. **投影矩阵约定不明确**：`orthoSize` 代表全高度而非半高度，这在 API 文档中没有明确说明
3. **调试方向错误**：初期怀疑是 GetScreenRay 缓存问题、矩阵刷新问题等，而非数学因子问题

**改进建议**：

| 对象 | 建议 |
|------|------|
| **对 AI** | 当数学补偿有线性误差时，优先检查是否存在 2x 或 0.5x 因子问题 |
| **对引擎** | 在 API 文档中明确说明 `orthoSize` 代表视野全高度，内部使用半高度 |
| **对文档** | 在 gotchas 中记录正交投影的关键参数约定 |

---

## 📐 技术细节：正交投影矩阵

### UrhoX 正交投影矩阵构造

```
视野半高度 = orthoSize * 0.5
视野半宽度 = orthoSize * 0.5 * aspect

投影矩阵的 scale 因子：
h = 1 / (orthoSize * 0.5) * zoom
w = h / aspect
```

### 屏幕到世界坐标转换

给定屏幕坐标 (screenX, screenY)：

```lua
-- 1. 转换为 NDC (-1 到 1)
local ndcX = (screenX / screenWidth) * 2 - 1
local ndcY = 1 - (screenY / screenHeight) * 2  -- Y 轴翻转

-- 2. 转换为视图空间偏移
local viewX = ndcX * aspect * orthoSize * 0.5
local viewY = ndcY * orthoSize * 0.5

-- 3. 转换为世界空间（使用相机的 right/up 向量）
local worldOffset = camRight * viewX + camUp * viewY

-- 4. 从相机位置出发，沿 forward 方向与地面相交
```

---

## 🔗 相关资源 (Related Resources)

- **引擎源码**：`engine/Source/Urho3D/Graphics/Camera.cpp` (第 460-483 行 GetScreenRay, 第 960 行 UpdateProjection)
- **相关 gotcha**：[gotchas/camera.md](../../engine-docs/gotchas/camera.md)
- **修复文件**：`TapCode-User_Workspace/scripts/Camera/IsometricCamera.lua`

