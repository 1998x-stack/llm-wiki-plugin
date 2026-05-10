---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [渲染, 粒子效果, 广告牌, UrhoX]
aliases: [BillboardSet, 广告牌集合, Sprite3D]
relates_to: [StaticModel静态网格体, UrhoX引擎, PBR材质系统]
supersedes: null
---
# BillboardSet广告牌

## 概述
BillboardSet 是 [[UrhoX引擎|UrhoX]] 中用于渲染始终朝向摄像机的 2D 四边形集合（继承自 Drawable），常用于粒子效果、草丛、远景植被等场景。

## 关键内容
- **广告牌数量**：`numBillboards` 控制池大小，通过 `GetBillboard(index)` 访问单个广告牌
- **朝向模式**：`faceCameraMode` 控制朝向策略（全向/仅Y轴旋转/固定等）
- **固定屏幕尺寸**：`fixedScreenSize` 保持广告牌在屏幕上的像素大小不变（适合 UI [[标注]]）
- **相对坐标**：`relative = true` 时广告牌位置相对于节点，否则为世界坐标
- **排序**：`sorted = true` 按距离排序，保证半透明正确叠加
- **UV 动画**：每个 Billboard 有独立的 `uv`（Rect）属性，实现贴图集动画
- **提交**：修改 Billboard 数据后必须调用 `Commit()` 才生效

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — BillboardSet : Drawable API 文档

## 相关
- [[StaticModel静态网格体]] — relates_to
- [[PBR材质系统]] — relates_to
- [[UrhoX引擎]] — relates_to
