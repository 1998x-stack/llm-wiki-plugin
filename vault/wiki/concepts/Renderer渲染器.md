---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["渲染", "渲染管线", "3D引擎", "UrhoX", "游戏开发"]
aliases: [Renderer, 渲染器配置, 全局渲染器]
relates_to: [UrhoX引擎, RenderPath渲染管线, Viewport渲染视口, Light光照系统]
supersedes: null
---
# Renderer渲染器

## 概述
[[UrhoX引擎|UrhoX]] 的全局 Renderer 对象管理所有渲染视口、阴影质量、纹理质量、HDR 和实例化绘制等全局渲染设置，是渲染管线的顶层控制器。

## 关键内容
- **视口管理**：`SetNumViewports(n)` + `SetViewport(index, viewport)` 支持多视口渲染（分屏、后处理等）
- **默认[[RenderPath渲染管线|渲染路径]]**：`SetDefaultRenderPath(renderPath)` 切换前向/延迟渲染管线
- **阴影配置**：`drawShadows`、`shadowMapSize`、`shadowQuality`、`reuseShadowMaps`
- **HDR 渲染**：`HDRRendering` 开启高动态范围，配合 ToneMapping [[RenderPath渲染管线|RenderPath]] 使用
- **纹理质量**：`textureQuality` / `materialQuality` / `textureAnisotropy` 影响纹理过滤
- **动态实例化**：`dynamicInstancing` 自动合批相同材质物体减少 DrawCall
- **遮挡剔除**：`SetMaxOccluderTriangles`、`occlusionBufferSize`、`SetOccluderSizeThreshold` 控制软件遮挡精度
- **移动端优化**：`mobileShadowBiasMul` / `mobileShadowBiasAdd` / `mobileNormalOffsetMul` 针对移动端阴影偏移

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — Renderer API 文档

## 相关
- [[RenderPath渲染管线]] — relates_to
- [[Viewport渲染视口]] — relates_to
- [[Light光照系统]] — relates_to
- [[UrhoX引擎]] — relates_to
