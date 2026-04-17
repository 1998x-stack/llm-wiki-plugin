---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏开发, 架构, 数据导向, ECS]
aliases: [Entity Component System, 实体组件系统]
relates_to: [游戏引擎架构, 场景树]
supersedes: null
---
# ECS架构

## 概述
Entity Component System（ECS）是游戏引擎的数据导向场景组织方案：Entity 是 ID，Component 是纯数据，System 是逻辑处理器，通过连续内存布局提升批处理性能。

## 关键内容
1. **三元素**：Entity（唯一ID，无行为）、Component（纯数据结构，如 Transform/Sprite[[Renderer渲染器|Renderer]]/Rigidbody）、System（遍历特定组件组合并执行逻辑）
2. **优势场景**：游戏对象数量多（大量 NPC、粒子、子弹）；需要批量系统化处理；性能敏感场景（数据局部性好于面向对象继承树）
3. **与[[场景树]]混合**：现代引擎常见方案——Entity 存 ECS，Transform 组件保存 parent/children 实现层级，渲染/物理/动画 System 按 ECS 批处理。"树描述关系，ECS 描述数据和系统执行"
4. **C++ 实现推荐**：初期用轻量 Entity+Component 方案（不需纯粹 ECS），进阶可接 entt 库

## 来源
- [[C++ 游戏引擎搭建指南]] — 介绍 ECS 适用场景、与场景树的互补关系及实践建议

## 相关
- [[游戏引擎架构]] — ECS 是场景层的高性能组织方案
- [[场景树]] — 与 ECS 互补，适合层级明确对象
- entt — C++ ECS 库推荐实现
