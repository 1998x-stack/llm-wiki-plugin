---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [渲染, 摄像机, 3D引擎, UrhoX]
aliases: [Camera组件, 摄像机组件, 正交摄像机, 透视摄像机]
relates_to: [UrhoX引擎, Viewport渲染视口, StaticModel静态网格体]
supersedes: null
---
# Camera渲染摄像机

## 概述
[[UrhoX引擎]]中的 Camera 组件，挂载于场景节点上，支持透视（Perspective）与正交（Orthographic）两种投影模式，控制场景的视角与裁剪范围。

## 关键内容
- **投影模式**：`orthographic = true` 切换为正交投影，默认为透视投影
- **透视参数**：`fov`（视野角）、`nearClip`/`farClip`（近远裁剪面）、`aspectRatio`
- **正交参数**：`orthoSize` 代表视野**全高度**，引擎内部使用 `orthoSize * 0.5` 作半高度参与[[矩阵]]计算
- **坐标转换**：`GetScreenRay(x, y)` 实时计算射线；`WorldToScreenPoint` / `ScreenToWorldPoint` 双向转换
- **[[LOD（细节层次）|LOD]] 偏置**：`lodBias` 影响可见物体的 [[LOD（细节层次）|LOD]] 级别选择
- **视图遮罩**：`viewMask` 过滤可见 Drawable 对象
- **反射/裁剪**：`useReflection` + `reflectionPlane` 实现水面反射；`useClipping` + `clipPlane` 斜裁剪
- **重要陷阱**：手动将屏幕坐标转视图空间时，NDC 需乘以 `orthoSize * 0.5`，直接用 `orthoSize` 会导致 2× 误差

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — Camera : Component API 文档

## 相关
- [[Viewport渲染视口]] — relates_to
- [[StaticModel静态网格体]] — relates_to
- [[LOD（细节层次）]] — relates_to
- [[UrhoX引擎]] — relates_to
