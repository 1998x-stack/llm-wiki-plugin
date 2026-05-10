---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["渲染", "视口", "3D引擎", "UrhoX", "游戏开发"]
aliases: [Viewport, 视口配置, 渲染区域]
relates_to: [Renderer渲染器, Camera渲染摄像机, RenderPath渲染管线]
supersedes: null
---
# Viewport渲染视口

## 概述
Viewport 将场景（Scene）、摄像机（Camera）和[[RenderPath渲染管线|渲染路径]]（[[RenderPath渲染管线|RenderPath]]）三者绑定，定义一个渲染区域（rect），由 [[Renderer渲染器|Renderer]] 管理多个 Viewport 实现分屏或后处理叠加。

## 关键内容
- **构造方式**：`Viewport:new(scene, camera)` 或带 `rect` 参数的区域视口
- **场景与摄像机**：`scene` 和 `camera` 属性指定渲染源
- **裁剪摄像机**：`cullCamera` 可与 `camera` 分离，用于反射等特殊效果
- **渲染区域**：`rect`（IntRect）指定视口在屏幕上的像素区域，默认全屏
- **[[RenderPath渲染管线|渲染路径]]**：`renderPath` 覆盖默认[[RenderPath渲染管线|渲染路径]]，每个视口可独立[[Configuration|配置]]
- **坐标转换**：`GetScreenRay(x, y)`、`WorldToScreenPoint`、`ScreenToWorldPoint` 提供视口级坐标映射
- **调试绘制**：`drawDebug` 开启物理碰撞体、骨骼等调试可视化

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — Viewport API 文档

## 相关
- [[Renderer渲染器]] — relates_to
- [[Camera渲染摄像机]] — relates_to
- [[RenderPath渲染管线]] — relates_to
- [[UrhoX引擎]] — relates_to
