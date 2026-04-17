---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [渲染, 光照, 阴影, 3D引擎, UrhoX]
aliases: [Light组件, 灯光系统, 动态光照, 阴影贴图]
relates_to: [UrhoX引擎, PBR材质系统, Renderer渲染器]
supersedes: null
---
# Light光照系统

## 概述
[[UrhoX引擎|UrhoX]] 的 Light 组件（继承自 Drawable）支持方向光、点光源、聚光灯三种类型，提供物理值模式、阴影级联、[[向量空间模型|VSM]]软阴影等高级光照特性。

## 关键内容
- **光照类型**：通过 `lightType` 设置（方向光 / 点光源 / 聚光灯）
- **颜色与亮度**：`color`、`brightness`、`specularIntensity`；`usePhysicalValues` 开启物理单位
- **光照范围**：点光/聚光使用 `range` 和 `fadeDistance` 控制衰减
- **阴影系统**：`castShadows` 开启阴影；`shadowBias`、`shadowCascade`（CSM）控制质量
- **软阴影**：[[Renderer渲染器|Renderer]] 层支持 [[向量空间模型|VSM]]（`SetVSMShadowParameters`），Light 级可设 `shadowSoftness`
- **色温**：`temperature` + `usePhysicalValues` 模拟真实灯泡颜色温度
- **光照遮罩**：`lightMask` / `shadowMask` 精确控制哪些物体受光/投影
- **Ramp/Shape 贴图**：通过 `rampTexture` / `shapeTexture` 自定义光照形状与衰减曲线

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — Light : Drawable API 文档

## 相关
- [[PBR材质系统]] — relates_to
- [[Renderer渲染器]] — relates_to
- [[UrhoX引擎]] — relates_to
