---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [3D, 游戏引擎, 性能优化, 渲染]
aliases: [LOD, Level of Detail, 细节层次]
relates_to: [UrhoXCLI, FBX格式]
supersedes: null
---

# LOD（细节层次）

## 概述

根据物体与相机的距离动态切换不同精度网格的渲染技术，远处使用低面数模型以大幅提升运行时性能。

## 关键内容

1. **自动生成**：[[UrhoX引擎|UrhoX]] 的 `import-model` 命令默认自动生成 3 级 LOD，使用保守简化比例（85%/65%/45%），无需手动建模。
2. **切换阈值**：通过固定 `screenSize` 阈值（0.2/0.08/0.03）控制 LOD 级别切换距离，值越小表示物体在屏幕中占比越小时切换。
3. **参数控制**：使用 `--no-lod` 关闭自动生成，`--lod-levels <n>`（1-4）调整级数，`--merge-meshes` 可先合并网格再生成 LOD。

## 来源

- [[raw/articles/personal/ai-dev-kit/.claude/skills/import-fbx/SKILL.md]] — UrhoX import-model LOD 自动生成说明

## 相关

- [[UrhoXCLI]] — uses
- [[FBX格式]] — relates_to
