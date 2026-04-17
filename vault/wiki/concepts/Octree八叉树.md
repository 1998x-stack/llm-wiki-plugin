---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [渲染, 空间分区, 射线检测, UrhoX]
aliases: [Octree, 八叉树场景管理, 空间索引]
relates_to: [UrhoX引擎, Camera渲染摄像机, StaticModel静态网格体]
supersedes: null
---
# Octree八叉树

## 概述
Octree 是 [[UrhoX引擎|UrhoX]] 场景的空间分区组件，负责管理所有 Drawable 对象的位置索引，支持按点/包围盒/视锥/球体查询可见物体，以及射线检测（Raycast）。

## 关键内容
- **场景根组件**：每个 Scene 自动包含一个 Octree，通常不需手动创建
- **大小设置**：`SetSize(boundingBox, numLevels)` 定义八叉树覆盖范围和最大深度
- **空间查询**：`GetDrawables(point/box/frustum/sphere)` 按区域获取相交 Drawable
- **射线检测**：`Raycast(ray, level, maxDistance, flags)` 返回所有命中；`RaycastSingle` 返回最近命中
- **查询级别**：`RayQueryLevel` 控制精度（包围盒/三角形/OBB等）
- **视图遮罩**：查询时可传 `viewMask` 过滤特定类别物体
- **手动注册**：`AddManualDrawable` / `RemoveManualDrawable` 手动管理不在场景节点上的 Drawable
- **用途**：视锥剔除、鼠标拾取、AI 视线检测、碰撞广播等

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — Octree : Component API 文档

## 相关
- [[Camera渲染摄像机]] — relates_to
- [[StaticModel静态网格体]] — relates_to
- [[UrhoX引擎]] — relates_to
