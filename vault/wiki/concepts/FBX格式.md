---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [3D, 文件格式, 游戏引擎, 模型]
aliases: [FBX, Filmbox]
relates_to: [UrhoXCLI, LOD（细节层次）]
supersedes: null
---

# FBX格式

## 概述

Autodesk 开发的 3D 资产交换格式，支持几何体、材质、纹理、骨骼动画，是 Blender/Maya/3ds Max 等 DCC 工具的标准导出格式。

## 关键内容

1. **坐标系差异**：不同 DCC 工具（Blender、Tripo 等）导出的 FBX 朝向不同，引擎导入时通常需自动校正坐标系和单位。
2. **内嵌资产**：FBX 内部包含材质名称（如 `Lambert`、`StandardSurface`、`tripo_material_xxx`）、纹理路径引用、[[骨骼系统|骨骼层级]]及动画轨道。
3. **导入产物**：导入 [[UrhoX引擎|UrhoX]] 引擎时可生成 MDL 模型、XML 材质、纹理、预制体（Prefab）和 ANI 动画文件；各产物按需生成，不传路径参数则跳过。

## 来源

- [[raw/articles/personal/ai-dev-kit/.claude/skills/import-fbx/SKILL.md]] — FBX 导入 UrhoX 引擎的完整工作流文档

## 相关

- [[UrhoXCLI]] — uses（import-model 子命令处理 FBX）
- [[LOD（细节层次）]] — relates_to
