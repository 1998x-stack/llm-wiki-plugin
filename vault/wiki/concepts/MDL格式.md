---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [3D, 游戏引擎, 模型格式, UrhoX]
aliases: [MDL, .mdl, UrhoX模型格式]
relates_to: [UrhoXCLI, LOD（细节层次）, FBX格式, 动画重定向]
supersedes: null
---

# MDL格式

## 概述

[[UrhoX引擎|UrhoX]]/Urho3D 引擎的原生 3D 模型格式，存储几何体、骨骼、[[LOD（细节层次）|LOD]] 层级、顶点属性及包围盒信息，由 [[FBX格式|FBX]] 等格式导入生成。

## 关键内容

1. **结构组成**：[[最小描述长度原理|MDL]] 文件包含包围盒（Bounding Box）、多个 Geometry（几何体）及其 [[LOD（细节层次）|LOD]] 层级（每级记录顶点数、三角面数、切换距离 lodDist）、顶点属性列表（Position/Normal/Tangent/TexCoord/[[骨骼系统|Bone]]Weights/[[骨骼系统|Bone]]Indices）和骨骼（[[骨骼系统|Skeleton]]）信息。
2. **model-info 查询**：使用 `UrhoXCLI model-info -i <mdl>` 检查模型的完整元信息；加 `--bones` 参数可列出所有骨骼名称及父索引，用于[[动画重定向]]前的骨骼结构验证。
3. **路径规则**：[[最小描述长度原理|MDL]] 文件路径必须使用绝对路径；若同目录存在同名 `.lodgroup` 文件，model-info 还会输出 [[LOD（细节层次）|LOD]] 切换参数（screenSize/maxDeviation）。
4. **典型工作流**：[[FBX格式|FBX]] 导入（`import-model`）→ [[最小描述长度原理|MDL]] 验证（`model-info`）→ 检查顶点数/面数/骨骼数是否符合预期。

## 来源

- [[raw/articles/personal/ai-dev-kit/.claude/skills/model-info/SKILL.md]] — UrhoX model-info 技能文档，MDL 格式信息查询完整说明

## 相关

- [[UrhoXCLI]] — uses
- [[LOD（细节层次）]] — part_of
- [[FBX格式]] — extends
- [[动画重定向]] — relates_to
