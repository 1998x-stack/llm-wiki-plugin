---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [3D格式, 模型, glTF, GLB, 坐标系, 纹理]
aliases: [glTF, GLB格式, gltf, glb]
relates_to: [UrhoXCLI, FBX格式, LOD（细节层次）, ANI动画文件格式]
supersedes: null
---

# GLB/glTF格式

## 概述
glTF（GL Transmission Format）是 Khronos 组织制定的开放 3D 资产格式，GLB 为其二进制打包版本，可内嵌纹理和动画。

## 关键内容
1. **坐标系规范**：glTF 采用 Y-up 右手坐标系、米制单位；导入 [[UrhoX引擎|UrhoX]]（左手系）时需自动转换坐标轴方向和 UV 翻转。
2. **内嵌纹理处理**：GLB 文件可将纹理直接打包进二进制，导入时自动提取到 `{模型名}.gbm/` 临时目录，再由工具复制到指定 `--texture-dir`；纹理命名按类型后缀区分：`D`（Diffuse/BaseColor）、`N`（Normal）、`S`（Specular）、`E`（Emissive）。
3. **导入产物**：通过 [[UrhoXCLI]] `import-gltf` 子命令可生成 MDL 模型、材质 XML、纹理（含 sidecar `.xml` 配置）、预制体 `.prefab` 和 ANI 动画；各产物路径独立，不传则跳过。
4. **LOD 自动生成**：默认开启 3 级 [[LOD（细节层次）]] 简化（85%/65%/45%），screenSize 阈值 0.2/0.08/0.03，可用 `--no-lod` 关闭或 `--lod-levels` 调整。

## 来源
- [[raw/articles/personal/ai-dev-kit/.claude/skills/import-glb/SKILL]] — UrhoX import-gltf 完整工作流与参数说明

## 相关
- [[UrhoXCLI]] — uses
- [[FBX格式]] — compares_to
- [[LOD（细节层次）]] — uses
- [[ANI动画文件格式]] — part_of
