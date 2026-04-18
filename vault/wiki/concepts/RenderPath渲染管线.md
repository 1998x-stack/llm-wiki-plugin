---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["渲染", "渲染管线", "前向渲染", "延迟渲染", "UrhoX", "游戏开发"]
aliases: [RenderPath, 渲染路径, Forward渲染, Deferred渲染]
relates_to: [Renderer渲染器, Viewport渲染视口, UrhoX引擎]
supersedes: null
---
# RenderPath渲染管线

## 概述
RenderPath 描述一条完整的渲染管线，由一组 RenderTarget 和 RenderPathCommand 组成，支持前向渲染、延迟渲染及自定义后处理效果，通过 XML 文件定义。

## 关键内容
- **加载方式**：`Load(xmlFile)` 从 XML 文件加载；`Append(xmlFile)` 追加额外 Pass（如后处理）
- **渲染目标**：`AddRenderTarget` / `SetRenderTarget` 管理中间缓冲区（G-Buffer、HDR Buffer 等）
- **命令控制**：`AddCommand` / `InsertCommand` 向管线插入渲染指令（场景绘制、屏幕四边形等）
- **标签开关**：`SetEnabled(tag, active)` 动态开关特定效果（如 SSAO、Bloom）
- **Shader 参数**：`SetShaderParameter` 向全局后处理 Shader 传参
- **克隆修改**：`Clone()` 创建副本后修改，避免影响全局默认路径
- **常用内置路径**：`Forward.xml`（前向）、`Deferred.xml`（延迟）、`PBRDeferred.xml`（PBR延迟）

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — RenderPath API 文档

## 相关
- [[Renderer渲染器]] — relates_to
- [[Viewport渲染视口]] — relates_to
- [[PBR材质系统]] — relates_to
- [[UrhoX引擎]] — relates_to
