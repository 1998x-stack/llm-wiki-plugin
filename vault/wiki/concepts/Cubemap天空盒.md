---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [3D渲染, 天空盒, 贴图, 游戏引擎]
aliases: [Cubemap, Skybox, 天空球, 立方体贴图]
relates_to: [等距柱状投影, UrhoXCLI]
supersedes: null
---

# Cubemap天空盒

## 概述
Cubemap 是由 6 个面（Face）组成的立方体贴图，常用于渲染天空盒（Skybox）或天空球（Skydome），模拟无限远处的环境背景。

## 关键内容
1. **存储格式**：常见格式为 DDS（DirectDraw Surface，GPU 原生，Windows/通用推荐）和 KTX（Khronos Texture，移动端/跨平台）；两者均支持 GPU 直接解码。
2. **Face 尺寸**：每个面尺寸相同，常用 256/512/1024/2048；建议配合 Mipmap 生成（`--mips`）以提升远距离渲染质量，减少摩尔纹。
3. **在引擎中使用**：以 `TextureCube` 资源类型加载，绑定到 `DiffSkybox.xml` Technique 的材质，挂载到 `Skybox` 组件的 Box 模型节点上即可渲染天空。

## 来源
- [[raw/articles/personal/ai-dev-kit/.claude/skills/convert-panorama/SKILL]] — UrhoX convert-panorama 技能文档

## 相关
- [[等距柱状投影]] — 全景图转 Cubemap 的输入来源
- [[UrhoXCLI]] — 执行全景图到 Cubemap 转换的工具
