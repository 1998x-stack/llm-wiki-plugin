---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["graphics", "geometry", "urho3d", "urhox", "lua", "rendering", "游戏开发"]
aliases: [CustomGeometry, 程序化几何体, 缺失图元替代方案]
relates_to: [UrhoX引擎, PBR材质系统, 三角形绕序与面朝向]
supersedes: null
---
# CustomGeometry程序化几何体

## 概述
当引擎内置模型（Box、Sphere、Cylinder 等）不支持所需基础形状时，使用 `CustomGeometry` 组件程序化生成任意几何体，如半球、圆锥台、楔形、扇形等。

## 关键内容

### 引擎内置模型（UrhoX/Urho3D）
Box、Sphere、Cylinder、Cone、Plane、Torus、TeaPot。**不支持**：半球、圆锥台、楔形、扇形、胶囊体（非物理）、任意多边形柱体。

### CustomGeometry 工作流
```lua
local geom = node:CreateComponent("CustomGeometry")
geom:BeginGeometry(0, TRIANGLE_LIST)  -- 开始定义，索引0，三角形列表模式

-- 每个顶点必须依次定义三属性
geom:DefineVertex(Vector3(x, y, z))
geom:DefineNormal(Vector3(nx, ny, nz))  -- 法线用于光照
geom:DefineTexCoord(Vector2(u, v))

-- 用顶点索引定义三角形
geom:DefineTriangle(idx0, idx1, idx2)

geom:Commit()
geom:SetMaterial(material)
```

### TRIANGLE_LIST 核心规则
- 每 3 个连续顶点构成 1 个三角形，**必须逐顶点定义**，不能批量传入后期望自动分组
- 不同三角形共享位置的顶点仍需**重新定义**（无共享顶点机制）
- 绕序：从正面看，顶点按**逆时针（CCW）** = 正面朝外（默认背面剔除）

### 半球生成原理
球面坐标转笛卡尔：
```
x = r·sin(φ)·cos(θ)
y = r·cos(φ)
z = r·sin(φ)·sin(θ)
```
上半球 φ ∈ [0, π/2]，下半球 φ ∈ [π/2, π]。上下半球绕序相反以保证面朝外。底面（切面）单独构建，可赋不同材质模拟截面效果。

### 性能建议
- 分段数（segments）推荐 16–32，过高增加顶点数但视觉收益递减
- 如需双面显示，材质设置 `<cull value="none"/>`

### 常用几何公式
```lua
-- 圆柱侧面：x=r·cos(θ), y=h·t, z=r·sin(θ)
-- 圆锥侧面：x=r·(1-t)·cos(θ), y=h·t, z=r·(1-t)·sin(θ)
```

## 来源
- [[raw/articles/personal/ai-dev-kit/coding-insights/Graphics-Rendering/custom-geometry-for-missing-primitives.md]] — CustomGeometry 完整示例与陷阱分析（2025-12-23）

## 相关
- [[UrhoX引擎]] — relates_to，CustomGeometry 是其图形组件
- [[PBR材质系统]] — relates_to，几何体需配合材质使用
- [[三角形绕序与面朝向]] — relates_to，绕序规则决定面的正反
