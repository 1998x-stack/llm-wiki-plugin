---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, 2D图形, 粒子, Lua, API]
aliases: [ParticleEffect2D, ParticleEmitter2D]
relates_to: [UrhoX 2D精灵系统API, UrhoX组件系统API]
supersedes: null
---
# UrhoX 2D粒子系统API

## 概述

[[UrhoX引擎|UrhoX]] 2D粒子系统由 ParticleEffect2D（粒子效果资源）和 ParticleEmitter2D（粒子发射器组件）组成，支持动态启停和精灵/混合模式配置。

## 关键内容

### 类层次

- `ParticleEffect2D : Resource` — 粒子效果资源，可 Clone 生成独立副本
- `ParticleEmitter2D : Drawable2D` — 粒子发射器组件，挂载到场景节点

### ParticleEffect2D

粒子效果参数（速度、生命周期、颜色渐变等）通常保存在 `.pex` 文件中，通过资源缓存加载。支持 `Clone` 创建独立副本，方便多发射器共享同一基础效果但参数互不干扰。

```lua
local effect = cache:GetResource("ParticleEffect2D", "Particles/explosion.pex")
local effectCopy = effect:Clone("explosion_copy")  -- 创建独立副本
```

### ParticleEmitter2D 关键属性

| 属性 | 类型 | 说明 |
|------|------|------|
| effect | ParticleEffect2D* | 关联粒子效果资源 |
| sprite | Sprite2D* | 粒子使用的精灵图 |
| blendMode | BlendMode | 混合模式（加法混合常用于光效） |
| emitting | bool | 是否正在发射粒子 |

### 典型用法

```lua
local emitterNode = scene_:CreateChild("Particles")
local emitter = emitterNode:CreateComponent("ParticleEmitter2D")
emitter.effect = cache:GetResource("ParticleEffect2D", "Particles/fire.pex")
emitter.blendMode = BLEND_ADDALPHA

-- 动态控制发射
emitter.emitting = true   -- 开始发射
emitter.emitting = false  -- 停止发射（已有粒子继续存活至生命周期结束）
```

### 注意事项

- `ParticleEmitter2D` 继承自 `Drawable2D`，支持 `layer` / `orderInLayer` 层级排序
- `blendMode` 独立设置，不依赖 effect 文件中的混合模式（会覆盖）
- `emitting = false` 不会立刻清除粒子，仅停止新粒子生成

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics-2d.md]] — UrhoX Lua API 2D图形模块文档

## 相关
- [[UrhoX 2D精灵系统API]] — relates_to
- [[UrhoX组件系统API]] — relates_to
- [[UrhoX引擎]] — relates_to
