---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["渲染", "3D模型", "网格体", "UrhoX", "游戏开发"]
aliases: [StaticModel, 静态模型组件, 静态网格]
relates_to: [UrhoX引擎, PBR材质系统, LOD（细节层次）, AnimatedModel骨骼动画模型]
supersedes: null
---
# StaticModel静态网格体

## 概述
StaticModel 是 [[UrhoX引擎|UrhoX]] 中最基础的 3D 渲染组件（继承自 Drawable），用于渲染不含骨骼动画的静态网格模型，支持多材质槽和遮挡 LOD。

## 关键内容
- **[[Settings|设置]]模型**：`model` 属性指向 Model 资源（`.mdl` 文件）
- **材质绑定**：`SetMaterial(index, material)` 按几何体槽分配材质；无索引版本全槽应用
- **材质列表**：`ApplyMaterialList(fileName)` 批量加载 `.txt` 格式材质列表
- **几何体数量**：`numGeometries` 对应模型内的子网格数量，每个可独立[[Settings|设置]]材质
- **遮挡 LOD**：`occlusionLodLevel` 指定用于遮挡剔除的 LOD 级别
- **包围盒**：`boundingBox`（只读）用于碰撞检测和视锥剔除
- **点包含检测**：`IsInside(worldPos)` / `IsInsideLocal(localPos)` 判断点是否在模型内
- **继承关系**：[[Cubemap天空盒|Skybox]]、[[AnimatedModel骨骼动画模型|AnimatedModel]]、StaticModelGroup 均继承自 StaticModel

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — StaticModel : Drawable API 文档

## 相关
- [[PBR材质系统]] — relates_to
- [[LOD（细节层次）]] — relates_to
- [[AnimatedModel骨骼动画模型]] — relates_to
- [[CustomGeometry程序化几何体]] — relates_to
- [[UrhoX引擎]] — relates_to
