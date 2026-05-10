---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["PBR", "材质", "渲染", "3D图形", "物理渲染", "游戏开发"]
aliases: [PBR渲染, 基于物理的渲染, Physically Based Rendering]
relates_to: [UrhoX材质库, UrhoXCLI]
supersedes: null
---

# PBR材质系统

## 概述
基于物理的渲染（PBR）材质系统，通过金属度（Metallic）和粗糙度（Roughness）参数模拟真实材质光学特性。

## 关键内容
1. **核心参数**：`MatDiffColor`（漫反射颜色 RGBA）、`Metallic`（金属度 0-1，0=非金属，1=金属）、`Roughness`（粗糙度 0-1，0=光滑，1=粗糙）、`MatEmissiveColor`（自发光颜色）。
2. **Technique 分类**：程序化纯色材质只用 `PBRNoTexture.xml`（不透明）或 `PBRNoTextureAlpha.xml`（透明）；需要纹理贴图时使用 `PBRMetallicRough*` 或 `PBRDiff*` 系列。
3. **常见效果参数组合**：光滑金属（Metallic 0.9-1.0，Roughness 0.1-0.2）、磨砂金属（Metallic 0.9-1.0，Roughness 0.4-0.6）、光滑塑料（Metallic 0.0，Roughness 0.3-0.5）、陶瓷（Metallic 0.0，Roughness 0.1-0.3）。
4. **自发光（Emissive）**：在 PBRNoTexture 材质上[[Settings|设置]] `MatEmissiveColor`，颜色值大于 1.0 可增强 HDR 发光强度；透明材质使用 `PBRNoTextureAlpha.xml` 并通过 Alpha 通道控制透明度。

## 来源
- [[raw/articles/personal/ai-dev-kit/.claude/skills/materials/SKILL]] — UrhoX 材质系统与 PBR 参数完整指南

## 相关
- [[UrhoX材质库]] — part_of
- [[UrhoXCLI]] — part_of
