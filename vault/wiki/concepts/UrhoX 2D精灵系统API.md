---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, 2D图形, 精灵, Lua, API]
aliases: [Sprite2D系统, StaticSprite2D, SpriteSheet2D]
relates_to: [UrhoX组件系统API, UrhoX场景系统API, UrhoX 2D动画系统API]
supersedes: null
---
# UrhoX 2D精灵系统API

## 概述

[[UrhoX引擎|UrhoX]] 2D精灵系统的核心类群，包含 Sprite2D（纹理资源）、SpriteSheet2D（精灵表）和 StaticSprite2D（可渲染组件）三个核心类。

## 关键内容

### 类层次

- `Drawable2D : Drawable` — 所有2D可绘制对象的基类，提供层序（layer / orderInLayer）控制
- `Sprite2D : Resource` — 精灵资源，封装纹理区域（rectangle）、热点（hotSpot）和偏移（offset）
- `SpriteSheet2D : Resource` — 精灵表，管理命名子精灵，支持 `DefineSprite` 批量定义
- `StaticSprite2D : Drawable2D` — 静态精灵组件，挂载到节点渲染 Sprite2D

### Drawable2D 层级控制

```lua
drawable:SetLayer(int layer)          -- 渲染层（越大越靠前）
drawable:SetOrderInLayer(int order)   -- 同层内排序
```

### Sprite2D 关键属性

| 属性 | 类型 | 说明 |
|------|------|------|
| texture | Texture2D* | 关联纹理 |
| rectangle | IntRect | 纹理中的矩形区域 |
| hotSpot | Vector2 | 锚点（0,0=左上，0.5,0.5=中心） |
| offset | IntVector2 | 像素偏移 |
| textureEdgeOffset | float | 边缘偏移（防止纹理渗色） |

### SpriteSheet2D 用法

```lua
local sheet = cache:GetResource("SpriteSheet2D", "Sprites/atlas.xml")
local sprite = sheet:GetSprite("player_idle")
```

### StaticSprite2D 关键属性

| 属性 | 说明 |
|------|------|
| sprite | 关联的 Sprite2D 资源 |
| blendMode | 混合模式（BlendMode 枚举） |
| flipX / flipY | 水平/垂直翻转 |
| swapXY | 交换 X/Y 轴（旋转90°效果） |
| color / alpha | 颜色调制和透明度 |
| useHotSpot / hotSpot | 启用热点覆盖 |
| useDrawRect / drawRect | 自定义绘制矩形 |
| useTextureRect / textureRect | 自定义纹理采样矩形 |
| customMaterial | 自定义材质覆盖 |

### 最小用法示例

```lua
local spriteNode = scene_:CreateChild("Sprite")
local staticSprite = spriteNode:CreateComponent("StaticSprite2D")
staticSprite.sprite = cache:GetResource("Sprite2D", "Sprites/player.png")
staticSprite.blendMode = BLEND_ALPHA
```

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics-2d.md]] — UrhoX Lua API 2D图形模块文档

## 相关
- [[UrhoX组件系统API]] — relates_to
- [[UrhoX场景系统API]] — relates_to
- [[UrhoX 2D动画系统API]] — relates_to
- [[UrhoX引擎]] — relates_to
