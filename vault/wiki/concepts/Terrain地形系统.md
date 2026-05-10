---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["渲染", "地形", "高度图", "UrhoX", "游戏开发"]
aliases: [Terrain, 地形组件, 高度场地形]
relates_to: [UrhoX引擎, LOD（细节层次）, PBR材质系统, StaticModel静态网格体]
supersedes: null
---
# Terrain地形系统

## 概述
[[UrhoX引擎|UrhoX]] 的 Terrain 组件通过高度图（Heightmap Image）生成分块 LOD 地形，由 TerrainPatch 子组件构成，支持法线平滑、多邻居接缝和高精度碰撞查询。

## 关键内容
- **高度图**：`SetHeightMap(image)` 加载灰度图，像素值映射为高度
- **间距控制**：`spacing`（Vector3）定义每像素对应的 XYZ 世界尺寸
- **分块大小**：`patchSize` 每个 TerrainPatch 包含的顶点数（默认 65）
- **LOD 级别**：`maxLodLevels` 控制最多细分层数，远处自动降分辨率
- **法线平滑**：`smoothing` 开启法线插值避免台阶感
- **邻居接缝**：`SetNeighbors(north, south, west, east)` [[Settings|设置]]相邻地形块，消除 LOD 裂缝
- **高度查询**：`GetHeight(worldPos)` 实时查询任意世界坐标的地面高度
- **法线查询**：`GetNormal(worldPos)` 获取地形法线（用于物体贴地对齐）
- **坐标转换**：`WorldToHeightMap` / `HeightMapToWorld` 像素坐标与世界坐标互转

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — Terrain : Component API 文档

## 相关
- [[LOD（细节层次）]] — relates_to
- [[PBR材质系统]] — relates_to
- [[UrhoX引擎]] — relates_to
