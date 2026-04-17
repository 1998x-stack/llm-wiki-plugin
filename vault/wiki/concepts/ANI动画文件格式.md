---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏引擎, 动画, 文件格式, UrhoX]
aliases: [ANI文件, ANI格式]
relates_to: [UrhoXCLI, 动画重定向]
supersedes: null
---

# ANI动画文件格式

## 概述

[[UrhoX引擎|UrhoX]]/Urho3D 引擎的二进制动画文件格式，存储骨骼动画的轨道、关键帧、通道（位移/旋转/缩放）和触发点数据。

## 关键内容

1. **核心数据结构**：包含动画名称、时长（秒）、骨骼轨道列表（每轨道含骨骼名、通道类型、关键帧数）和触发点（Trigger，带时间戳）；轨道数通常等于骨骼数。
2. **通道类型**：P（Position 位移）、R（Rotation 旋转）、S（Scale 缩放）。纯旋转动画最常见，位移通道通常只有根骨骼才有；查询时 Channels 字段统计各类型轨道数量。
3. **使用方式**：通过 [[UrhoXCLI]] 的 `anim-info` 子命令查询文件信息；从 [[FBX格式|FBX]] 导入后需验证轨道数和关键帧数是否正确；[[动画重定向]]前需对比源动画与目标模型的骨骼名称。

## 来源

- [[raw/articles/personal/ai-dev-kit/.claude/skills/anim-info/SKILL.md]] — ANI 文件格式字段说明与示例输出

## 相关

- [[UrhoXCLI]] — part_of
- [[动画重定向]] — compares_to
