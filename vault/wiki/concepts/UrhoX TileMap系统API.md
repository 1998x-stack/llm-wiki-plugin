---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, 2D图形, TileMap, 瓦片地图, Lua, API]
aliases: [TileMap2D, TileMapLayer2D, TmxFile2D]
relates_to: [UrhoX 2D精灵系统API, UrhoX组件系统API, UrhoX场景系统API]
supersedes: null
---
# UrhoX TileMap系统API

## 概述

[[UrhoX引擎|UrhoX]] TileMap 系统基于 TMX 格式，通过 TmxFile2D 资源加载 Tiled 地图，TileMap2D 组件渲染，并提供坐标转换、图层查询及对象层访问 API。

## 关键内容

### 类层次

```
TmxFile2D : Resource          -- TMX 文件资源
TileMap2D : Component         -- 地图渲染组件（挂节点）
TileMapLayer2D : Component    -- 单个图层（自动创建为子节点）
TileMapInfo2D                 -- 地图元信息（方向、尺寸、格子尺寸）
Tile2D                        -- 单格瓦片（gid + sprite）
TileMapObject2D               -- 对象层中的对象（矩形、多边形、精灵等）
PropertySet2D                 -- 任意对象/格子的自定义属性集
```

### TileMap2D 核心用法

```lua
local mapNode = scene_:CreateChild("TileMap")
local tileMap = mapNode:CreateComponent("TileMap2D")
tileMap.tmxFile = cache:GetResource("TmxFile2D", "Maps/level1.tmx")

-- 坐标转换
local worldPos = tileMap:TileIndexToPosition(x, y)
local ok, tx, ty = tileMap:PositionToTileIndex(worldPos)

-- 获取图层
local layerCount = tileMap.numLayers
local layer = tileMap:GetLayer(0)
```

### TileMapInfo2D 字段

| 属性 | 说明 |
|------|------|
| orientation | 地图方向（正交/等距，Orientation2D 枚举） |
| width / height | 地图格子列数 / 行数 |
| tileWidth / tileHeight | 单格像素宽 / 高（浮点） |
| mapWidth / mapHeight | 总像素宽 / 高（readonly，计算值） |

### TileMapLayer2D 图层查询

```lua
-- 图块图层
local tile = layer:GetTile(x, y)       -- 返回 Tile2D
local node = layer:GetTileNode(x, y)   -- 返回该格子的场景节点

-- 对象图层
local objCount = layer.numObjects
local obj = layer:GetObject(0)         -- 返回 TileMapObject2D
local objNode = layer:GetObjectNode(0)

-- 图像图层
local imgNode = layer.imageNode

-- 自定义属性
if layer:HasProperty("collision") then
    local val = layer:GetProperty("collision")
end
```

### Tile2D

```lua
local gid   = tile.gid           -- 全局 tile ID
local sp    = tile.sprite         -- 关联 Sprite2D（readonly）
local flipX = tile:GetFlipX()
local flipY = tile:GetFlipY()
```

### TileMapObject2D

```lua
local objType = obj.objectType    -- TileMapObjectType2D 枚举
local name    = obj.name
local pos     = obj.position      -- Vector2
local size    = obj.size          -- Vector2（矩形/椭圆）
local pts     = obj.numPoints     -- 多边形顶点数
local pt      = obj:GetPoint(i)   -- Vector2 顶点

-- 精灵对象
local gid     = obj.tileGid
local sp      = obj.tileSprite
```

### PropertySet2D

图层、格子、对象均实现此接口：

```lua
if obj:HasProperty("damage") then
    local dmg = obj:GetProperty("damage")
end
```

### TmxFile2D 边缘偏移

```lua
-- 防止瓦片纹理渗色（bleeding）
tmxFile.edgeOffset = 0.5
```

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics-2d.md]] — UrhoX Lua API 2D图形模块文档

## 相关
- [[UrhoX 2D精灵系统API]] — relates_to
- [[UrhoX组件系统API]] — relates_to
- [[UrhoX场景系统API]] — relates_to
- [[UrhoX引擎]] — relates_to
