---
summary: "Minecraft texture pack system supporting multiple procedural material sets (Classic/HD PBR) with runtime switching"
related_paths:
  - engine/Source/Urho3D/Graphics/**
last_updated: "2026-04-02"
---

# Minecraft Texture Pack System Design

Minecraft 示例项目的材质包系统架构，支持多套程序化生成的材质（Classic/HD PBR），运行时切换，用户可扩展。

---

## 架构概览

```mermaid
classDiagram
    class TexturePackBase {
        +name: string
        +displayName: string
        +tileSize: number
        +atlasSize: number
        +tilesPerRow: number
        +generate(): table
        +getFilterMode(): number
        +getTileUV(row, col): u0,v0,u1,v1
        +createTexture(image, srgb): Texture2D
        +computeNormalFromHeight(): nx,ny,nz
    }

    class ClassicPack {
        tileSize: 16, atlasSize: 256
        filterMode: FILTER_NEAREST
        generate(): {diffuse, normal=nil, specular=nil}
    }

    class HDPack {
        tileSize: 32, atlasSize: 512
        filterMode: FILTER_TRILINEAR
        generate(): {diffuse, normal, specular}
    }

    class TexturePackManager {
        +register(pack)
        +setCurrent(name)
        +getCurrent(): TexturePackBase
        +setOnPackChanged(callback)
    }

    TexturePackBase <|-- ClassicPack
    TexturePackBase <|-- HDPack
    TexturePackManager --> TexturePackBase
```

## 核心设计决策

### 统一返回 Table

`generate()` 始终返回 `{ diffuse, normal, specular }` 格式：
- ClassicPack: `normal` 和 `specular` 为 `nil`，使用 Diff technique
- HDPack: 三个贴图都有值，使用 PBR technique
- 调用方通过 `if textures.normal then` 判断是否 PBR，无需额外标志
- 扩展性好（未来可加 `emissive` 等）

### PBR 渲染流程

```mermaid
flowchart TB
    Pack[TexturePack.generate()] --> Table["{diffuse, normal, specular}"]
    Table --> CMB[ChunkMeshBuilder]
    CMB --> Check{textures.normal ?}
    Check -->|yes| PBR[PBR Technique]
    Check -->|no| Diff[Diff Technique]
```

---

## 文件结构

```
scripts/rendering/
├── TextureAtlas.lua              # 代理，委托到 TexturePackManager
└── texturepacks/
    ├── TexturePackBase.lua        # 基类/接口
    ├── TexturePackManager.lua     # 管理器（注册、切换、通知）
    ├── ClassicPack.lua            # 经典材质（256x256, 16x16 tile, NEAREST）
    └── HDPack.lua                 # HD PBR 材质（512x512, 32x32 tile, TRILINEAR）
```

## 关键接口

### TexturePackBase

```lua
function TexturePackBase:generate()         -- 返回 { diffuse, normal?, specular? }
function TexturePackBase:getTileUV(row, col) -- UV 坐标计算
function TexturePackBase:createTexture(image, srgb)  -- 创建 Texture2D
function TexturePackBase:computeNormalFromHeight(heightMap, x, y, size, strength)
```

### TexturePackManager

```lua
TexturePackManager:register(pack)           -- 注册材质包
TexturePackManager:setCurrent(name)         -- 切换（触发 onPackChanged 回调）
TexturePackManager:getCurrent()             -- 获取当前
TexturePackManager:setOnPackChanged(cb)     -- 注册切换回调
```

### ChunkMeshBuilder 集成

```lua
function ChunkMeshBuilder:setTextures(textures)  -- 设置贴图集合
function ChunkMeshBuilder:getChunkMaterial()      -- 根据 PBR 可用性选择 technique
function ChunkMeshBuilder:refreshTexturePack()    -- 材质包切换后刷新
```

---

## HD PBR 材质参数

Technique: `Techniques/PBR/PBRMetallicRoughDiffNormalSpecVCol.xml`

贴图槽位: TU_DIFFUSE(0), TU_NORMAL(1), TU_SPECULAR(2)

| 方块 | 金属度 | 粗糙度 | 法线强度 |
|------|--------|--------|----------|
| 草地 | 0.0 | 0.9 | 0.3 |
| 泥土 | 0.0 | 0.95 | 0.5 |
| 石头 | 0.0 | 0.7 | 2.0 |
| 木头 | 0.0 | 0.6 | 0.5-0.8 |
| 树叶 | 0.0 | 0.85 | 0.2 |
| 沙子 | 0.0 | 0.95 | 0.4 |
| 水 | 0.0 | 0.1 | 0.1 |

HDPack 采用**合并生成**方案：每个方块的 `generate*` 方法一次遍历同时写入 Diffuse + Normal + Specular 三张 Image，保证视觉一致性。法线从高度图计算（Sobel 差分 + 归一化 + 映射到 0-1）。

---

## 用户扩展

1. 复制 `ClassicPack.lua` 为模板
2. 修改 `name` 和 `displayName`
3. 实现 `createImage()` 方法
4. 在 `TexturePackManager.lua` 中 register

---

## 相关文件

- `engine/bin/Data/LuaScripts/Hand-picked/Minecraft/scripts/rendering/texturepacks/`
- `engine/bin/Data/LuaScripts/Hand-picked/Minecraft/scripts/rendering/TextureAtlas.lua`
- `engine/bin/Data/LuaScripts/Hand-picked/Minecraft/scripts/world/ChunkMeshBuilder.lua`
- `engine/bin/Data/LuaScripts/Hand-picked/Minecraft/scripts/world/World.lua`

---

*最后更新: 2026-04-02*
