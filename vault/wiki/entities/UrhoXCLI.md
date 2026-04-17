---
type: entity
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 3
tags: [游戏引擎, CLI工具, 3D渲染, 天空盒, 模型导入, glTF, GLB]
aliases: [UrhoX CLI, urhoxcli]
relates_to: [Cubemap天空盒, 等距柱状投影, FBX格式, LOD（细节层次）, GLB/glTF格式, MDL格式]
supersedes: null
entity_type: tool
---

# UrhoXCLI

## 概述
[[UrhoX引擎|UrhoX]] 引擎配套命令行工具，支持全景图转 [[Cubemap天空盒|Cubemap]] 等资源处理操作，路径为 `/workspace/.cli/UrhoXCLI`。

## 关键内容
1. **全景图转换**：`convert-panorama` 子命令将 HDR/PNG/JPG/TGA 全景图转为 DDS 或 KTX 格式的 [[Cubemap天空盒|Cubemap]]，支持自动检测[[等距柱状投影]]（2:1）和横条（6:1）布局。
2. **主要参数**：`-i` 输入路径、`-o` 输出路径、`--size N` 指定 Face 尺寸、`--strip` 强制横条模式、`--mips` 生成 Mipmap 链。
3. **路径要求**：输入和输出必须使用绝对路径；HDR 输出保持 RGBA32F 浮点精度（适合 IBL 光照）；LDR 输出为 RGBA8（适合天空盒背景）。
4. **FBX 模型导入**：`import-model` 子命令将 FBX 转为引擎 MDL 格式；可选生成材质 XML、纹理（含 sidecar `.xml` 配置）、预制体和 ANI 动画；各产物路径独立，不传则跳过。默认开启 3 级 [[LOD（细节层次）]] 自动生成（85%/65%/45% 简化比例），可用 `--no-lod` 关闭或 `--lod-levels` 调整级数。
5. **GLB/glTF 模型导入**：`import-gltf` 子命令将 [[GLB_glTF格式|GLB/glTF]] 转为引擎 MDL 格式；自动处理右手系→左手系坐标转换、UV 翻转和单位转换；GLB 内嵌纹理自动提取；输出产物（MDL、材质、纹理、预制体、动画）均独立可选，不传则跳过。
6. **MDL 模型信息查询**：`model-info -i <mdl>` 输出包围盒（Min/Max/Size）、Geometry 数量及每个几何体的 LOD 层级（顶点数/三角面数/切换距离）、顶点属性、骨骼数；加 `--bones` 列出完整骨骼列表（骨骼名+父索引），用于导入验证和 [[动画重定向]] 前检查。

## 来源
- [[raw/articles/personal/ai-dev-kit/.claude/skills/convert-panorama/SKILL]] — UrhoX convert-panorama 技能文档
- [[raw/articles/personal/ai-dev-kit/.claude/skills/import-fbx/SKILL.md]] — UrhoX import-model FBX 导入完整工作流
- [[raw/articles/personal/ai-dev-kit/.claude/skills/import-glb/SKILL.md]] — UrhoX import-gltf GLB/glTF 导入完整工作流
- [[raw/articles/personal/ai-dev-kit/.claude/skills/model-info/SKILL.md]] — UrhoX model-info MDL 模型信息查询技能文档

## 相关
- [[Cubemap天空盒]] — uses
- [[等距柱状投影]] — uses
- [[FBX格式]] — uses
- [[LOD（细节层次）]] — uses
- [[GLB_glTF格式]] — uses
- [[MDL格式]] — uses
