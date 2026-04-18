---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["UrhoX", "2D图形", "动画", "Lua", "API", "游戏开发"]
aliases: [AnimatedSprite2D, AnimationSet2D, StretchableSprite2D]
relates_to: [UrhoX 2D精灵系统API, UrhoX组件系统API]
supersedes: null
---
# UrhoX 2D动画系统API

## 概述

[[UrhoX引擎|UrhoX]] 2D动画系统基于 AnimationSet2D 资源和 AnimatedSprite2D 组件，支持帧动画播放与循环模式控制，另有 StretchableSprite2D 支持九宫格拉伸。

## 关键内容

### 类层次

- `AnimationSet2D : Resource` — 动画集资源，存储多个命名动画
- `AnimatedSprite2D : StaticSprite2D` — 动画精灵组件，在节点上播放动画
- `StretchableSprite2D : StaticSprite2D` — 九宫格拉伸精灵，用于 UI 面板/按钮背景

### AnimationSet2D

```lua
local animSet = cache:GetResource("AnimationSet2D", "Sprites/hero.scml")
-- 查询动画数量和名称
local count = animSet.numAnimations       -- readonly
local name  = animSet:GetAnimation(0)    -- 按索引获取动画名（Lua 0-based 调用）
```

### AnimatedSprite2D 关键属性

| 属性 | 类型 | 说明 |
|------|------|------|
| animationSet | AnimationSet2D* | 关联动画集资源 |
| entity | String | Spriter 实体名（多实体 scml 时使用） |
| animation | String | 当前播放的动画名 |
| loopMode | LoopMode2D | 循环模式（LM_DEFAULT / LM_FORCE_LOOPED / LM_FORCE_CLAMPED） |
| speed | float | 播放速度倍率（1.0=正常） |

### 播放动画

```lua
local animSprite = node:CreateComponent("AnimatedSprite2D")
animSprite.animationSet = cache:GetResource("AnimationSet2D", "Sprites/hero.scml")
animSprite.entity = "hero"
animSprite:SetAnimation("run", LM_DEFAULT)
animSprite.speed = 1.5
```

### StretchableSprite2D

九宫格拉伸精灵，适合按钮背景、对话框等 UI 元素。

```lua
local stretchable = node:CreateComponent("StretchableSprite2D")
stretchable.sprite = cache:GetResource("Sprite2D", "UI/button.png")
-- border 定义九宫格边缘（left, top, right, bottom 像素数）
stretchable.border = IntRect(8, 8, 8, 8)
```

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics-2d.md]] — UrhoX Lua API 2D图形模块文档

## 相关
- [[UrhoX 2D精灵系统API]] — relates_to
- [[UrhoX组件系统API]] — relates_to
- [[UrhoX引擎]] — relates_to
