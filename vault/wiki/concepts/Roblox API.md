---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, 游戏开发, Lua]
aliases: [Roblox内建API, Roblox平台API, Roblox Instance API]
relates_to:
  - target: "Luau"
    type: implements
    confidence: 0.95
  - target: "[[Roblox]]"
    type: implements
    confidence: 0.98
  - target: "[[游戏引擎架构]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---

# Roblox API

## 概述
[[Roblox]] 平台提供的内建类型与服务 API，涵盖值类型（Vector3/CFrame）、Instance 操作、动画（TweenService）、射线检测、玩家角色及 RunService [[游戏主循环模式|游戏循环]]。

## 关键内容

### 内建值类型（无 GC 压力）
[[Roblox]] 的几何与颜色类型是值类型，与普通 [[Lua-table-用法|Lua table]] 不同，不产生[[垃圾回收]]压力：
- **Vector3**：3D 坐标，支持 `+`/`*` 运算，`.Magnitude`、`.Unit`、`:Dot`、`:Cross`、`:Lerp`
- **Vector2**：2D 坐标
- **CFrame**：位置+姿态复合变换；`CFrame.lookAt(from, to)`；`*` 复合；`:ToObjectSpace` / `:ToWorldSpace` 坐标系转换；`:ToEulerAnglesXYZ` 提取欧拉角
- **Color3**：`Color3.fromRGB(r, g, b)`
- **UDim2**：GUI 布局尺寸，`UDim2.new(relX, absX, relY, absY)`（相对+绝对混合）
- **Rect / Ray**：矩形区域和射线
- [[Roblox]] 须用 `typeof()` 检测类型，`type(Vector3.new())` 返回 `"userdata"`，`typeof` 才返回 `"Vector3"`

### Instance 操作
```
Instance.new("ClassName")          -- 创建实例
parent:FindFirstChild("name")      -- 查找子级（第二参数 true 递归）
parent:FindFirstChildOfClass("X")  -- 按类名精确匹配
parent:FindFirstChildWhichIsA("X") -- 含子类匹配
parent:WaitForChild("name", timeout)
parent:GetChildren() / :GetDescendants()
instance:Clone() / :Destroy()
part:GetPropertyChangedSignal("Prop"):Connect(fn)
```
常用属性：`Name`、`Parent`、`Anchored`、`Size`、`Position`、`CFrame`、`Color`、`Material`、`Transparency`、`CanCollide`

### TweenService 动画
```lua
local info = TweenInfo.new(duration, EasingStyle, EasingDirection, repeatCount, reverses, delay)
local tween = TweenService:Create(instance, info, {Position = ..., Transparency = ...})
tween:Play()
tween.Completed:Connect(function(state) end)
```
- `Enum.EasingStyle.Quad` / `Enum.EasingDirection.Out` 等缓动参数
- `repeatCount = -1` 为无限循环

### 射线检测（Raycast）
```lua
local params = RaycastParams.new()
params.FilterDescendantsInstances = {character}
params.FilterType = Enum.RaycastFilterType.Exclude
local result = workspace:Raycast(origin, direction, params)
-- result.Instance / result.Position / result.Normal / result.Material
```

### 玩家与角色
```lua
local Players = game:GetService("Players")
local player = Players.LocalPlayer  -- 仅客户端
local character = player.Character or player.CharacterAdded:Wait()
local humanoid = character:WaitForChild("Humanoid")
local rootPart = character:WaitForChild("HumanoidRootPart")
humanoid:TakeDamage(25)
humanoid:MoveTo(Vector3.new(0, 0, 0))
humanoid.Died:Connect(function() end)
```

### GUI
```lua
local screenGui = Instance.new("ScreenGui")
screenGui.Parent = player.PlayerGui
-- Frame: Size = UDim2, Position = UDim2, BackgroundColor3
-- TextButton: .Text, .MouseButton1Click:Connect(fn)
```

### RunService 游戏循环
三种循环时机，均传入 `dt`（帧时间）：
- **Heartbeat**：物理计算后，每帧；用于游戏逻辑
- **RenderStepped**：渲染前，仅客户端；用于摄像机等视觉更新
- **Stepped**：物理计算前，传 `(time, dt)`；用于物理前处理

### task 库（帧调度）
`wait()` 的精确替代：
- `task.wait(seconds)` — 等待
- `task.spawn(fn, args)` — 立即执行（下一帧）
- `task.defer(fn, args)` — 延迟到帧末尾
- `task.delay(seconds, fn, args)` — 延迟执行
- `task.cancel(thread)` — 取消协程

## 来源
- [[luau-types]] — Luau 类型系统与 Roblox API 参考，含完整代码示例

## 相关
- Luau — Roblox 的 Lua 方言，提供类型注解和性能优化
- [[Roblox]] — 平台背景
- [[游戏引擎架构]] — Roblox 引擎设计与通用游戏引擎的对比
