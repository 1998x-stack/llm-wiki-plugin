---
type: tool
entity_type: tool
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏开发, C++, ECS, 工具库]
aliases: [EnTT]
relates_to: [ECS架构, 游戏引擎架构]
supersedes: null
---
# entt

## 概述
entt 是高性能 header-only [[C++]] ECS 库，基于稀疏集（sparse set）实现，提供快速组件迭代和灵活的实体管理，是 [[C++]] 游戏引擎中实现 ECS 架构的主流选择之一。

## 关键内容
1. **特点**：Header-only，无外部依赖；基于稀疏集实现高效组件存储和遍历；支持现代 [[C++]]17，API 设计简洁
2. **使用场景**：[[C++]] 自建游戏引擎中需要 ECS 架构时的可选集成库；适合需要高性能批处理（粒子、NPC、子弹）的场景
3. **定位**：引擎中期扩展选项，新手初期可先用轻量 Entity+Component 方案，后期再接入 entt

## 来源
- [[C++ 游戏引擎搭建指南]] — 推荐技术栈中列为 ECS 可选库

## 相关
- [[ECS架构]] — entt 的实现目标架构
- [[游戏引擎架构]] — 场景层 ECS 方案的具体实现
