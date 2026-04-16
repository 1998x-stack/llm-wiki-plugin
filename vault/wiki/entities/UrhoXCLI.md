---
type: entity
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏引擎, CLI工具, 3D渲染, 天空盒]
aliases: [UrhoX CLI, urhoxcli]
relates_to: [Cubemap天空盒, 等距柱状投影]
supersedes: null
entity_type: tool
---

# UrhoXCLI

## 概述
UrhoX 引擎配套命令行工具，支持全景图转 Cubemap 等资源处理操作，路径为 `/workspace/.cli/UrhoXCLI`。

## 关键内容
1. **全景图转换**：`convert-panorama` 子命令将 HDR/PNG/JPG/TGA 全景图转为 DDS 或 KTX 格式的 Cubemap，支持自动检测等距柱状投影（2:1）和横条（6:1）布局。
2. **主要参数**：`-i` 输入路径、`-o` 输出路径、`--size N` 指定 Face 尺寸、`--strip` 强制横条模式、`--mips` 生成 Mipmap 链。
3. **路径要求**：输入和输出必须使用绝对路径；HDR 输出保持 RGBA32F 浮点精度（适合 IBL 光照）；LDR 输出为 RGBA8（适合天空盒背景）。

## 来源
- [[raw/articles/personal/ai-dev-kit/.claude/skills/convert-panorama/SKILL]] — UrhoX convert-panorama 技能文档

## 相关
- [[Cubemap天空盒]] — uses
- [[等距柱状投影]] — uses
