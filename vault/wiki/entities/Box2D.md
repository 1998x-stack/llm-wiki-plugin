---
type: entity
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["物理引擎", "2D物理", "碰撞检测", "游戏开发"]
aliases: [Box2D物理引擎, Box2D碰撞系统]
relates_to: [UrhoX引擎, 游戏脚手架模式]
supersedes: null
---

# Box2D

## 概述
Box2D 是一个广泛使用的 2D 物理引擎，支持刚体模拟、碰撞检测、关节约束等功能。[[UrhoX引擎|UrhoX]] 的 2D 物理[[游戏脚手架模式|游戏脚手架]]集成了 Box2D。

## 关键内容
1. **在 [[UrhoX引擎|UrhoX]] 中的集成**：2D 物理[[游戏脚手架模式|游戏脚手架]]（`scaffold-2d-physics.lua`）内置 Box2D 物理系统，用于平台跳跃等需要物理模拟的游戏类型。
2. **最佳实践**：Box2D 碰撞体必须在同一刚体节点上，使用 `center` 偏移。错误放置会导致地面检测失败、按空格无法跳跃等问题。
3. **示例参考**：`examples/04-box2d-platformer.lua` 展示了如何正确使用 Box2D 物理系统实现 2D 平台跳跃游戏，避免常见碰撞检测 BUG。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #2（脚手架）

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[游戏脚手架模式]] — relates_to（2D 物理脚手架的组成部分）
