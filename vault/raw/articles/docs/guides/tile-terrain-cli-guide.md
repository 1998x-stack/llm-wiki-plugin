---
summary: "TileTerrainCLI command-line tool guide for creating, editing, validating, and exporting tile terrain data"
last_updated: "2026-03-16"
---

# TileTerrainCLI 使用指南

TileTerrainCLI 是 UrhoX 引擎配套的瓦片地形命令行工具，用于创建、编辑、验证地形数据，以及将地形导出为可在引擎中加载的流式场景。

---

## 地形系统概述

### 地形数据模型

地形以**二维网格**组织。网格由 W×H 个**格子（Grid）** 组成，格子的四角为**顶点（Point）**，相邻格子之间的边界为**边（Edge）**。

```
Point ── Edge ── Point ── Edge ── Point
  |                |                |
 Edge    Grid     Edge    Grid    Edge
  |                |                |
Point ── Edge ── Point ── Edge ── Point
```

- **顶点**：存储离散高度值和地表类型标记（陆地 / 水域）
- **边**：存储连接标记（路径 / 裂缝），影响相邻格子间的过渡方式
- **格子**：由四个角点和四条边共同描述，关联一个 TileSet（瓦片集）和可选的子风格（SubStyle）

### 高度与尺寸

- 高度以**离散层级**存储，每层对应固定物理高度（默认 1.28m）
- 每个格子的物理尺寸默认为 2.56m × 2.56m

### 瓦片匹配

地形生成的核心是**瓦片匹配**：系统从每个格子提取其四角高度差、边标记和破坏状态，组成一个**匹配签名（TileKey）**。通过对签名做归一化（减去最小高度、旋转对齐），在 TileSet 的瓦片索引中查找最佳匹配。匹配结果决定该格子使用哪个 3D 模型，以及需要旋转多少度放置。

同一个签名可能匹配多个瓦片变体，此时按权重随机选取，保证视觉多样性。

### 装饰物放置

每个瓦片定义了若干**装饰插槽（Decoration Slot）**，描述在特定地表条件下可以放置哪些装饰物（植被、石块、道具等）。匹配瓦片后，系统根据格子四角的地表类型评估每个插槽条件，满足条件则按权重随机选取装饰变体并计算最终放置位置。

### 地表混合（Weight Map）

地形几何形状由瓦片模型决定，但表面纹理由独立的**权重图（Weight Map）** 控制。权重图的分辨率高于地形网格（每个格子 4×4 采样点），每个采样点存储两层纹理 ID 和混合权重。

渲染时，着色器通过**手动双线性插值**读取控制图，对纹理数组中的不同图层进行混合。这种方式确保纹理 ID 不会被错误插值（ID 是离散值），同时实现平滑的纹理过渡。

所有 LOD 层级共享同一张控制图和同一个混合材质，因此远处的简化网格也能获得正确的地表外观。

### 多级 LOD 流式加载（HLOD）

对于大型地图，地形被切分为多级 **WorldPartition** 单元：

| 层级 | 说明 | 典型尺寸 |
|------|------|---------|
| **L0（基础层）** | 原始精度的瓦片网格，运行时合并为子块渲染 | 40.96m（16×16 瓦片） |
| **L1（中距离）** | 多个 L0 单元合并并简化的代理网格 | 81.92m（2×2 L0） |
| **L2（远距离）** | 多个 L1 单元进一步简化的代理网格 | 163.84m（2×2 L1） |
| **装饰层** | 独立于 HLOD 的装饰物流式层 | 128m |

运行时根据摄像机距离动态加载/卸载各层级单元，近处显示高精度 L0，远处切换为简化的 L1/L2 代理，实现大地图的高效渲染。

### UUID 资源引用

生成的所有输出文件会自动分配 UUID 并生成 `.meta` 文件。文件之间的引用统一使用 `uuid://` 路径，运行时通过 UUID 映射表解析为实际文件路径。输出目录下会生成 `uuid_mappings.json` 供引擎加载。

---

## 命令参考

### create — 创建空白地形

创建一个指定尺寸的空白地形文件，所有高度初始化为 0，地表类型为陆地。

```bash
TileTerrainCLI create --width <W> --height <H> --tileset <名称> --output <路径>
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--width` | 10 | 地形宽度（格子数） |
| `--height` | 10 | 地形高度（格子数） |
| `--tileset` | "me_tiles_field" | 初始 TileSet 名称 |
| `--output` | "terrain.json" | 输出文件路径 |

**示例**：

```bash
# 创建 64×32 的地形，使用 me_tiles_field TileSet
TileTerrainCLI create --width 64 --height 32 --tileset me_tiles_field --output terrain.json
```

---

### modify — 修改地形数据

对已有地形进行各种编辑操作。默认使用**约束模式**，自动维护地形规则（如高度差限制、水域扩展）；使用 `--raw` 可绕过约束直接修改。

```bash
TileTerrainCLI modify --input <路径> [--output <路径>] [--raw] <操作...>
```

| 参数 | 说明 |
|------|------|
| `--input` | **（必填）** 输入地形文件 |
| `--output` | 输出文件（默认覆盖输入文件） |
| `--raw` | 绕过约束，直接修改原始数据 |

**顶点操作**：

| 操作 | 格式 | 说明 |
|------|------|------|
| `--set-height` | `x,y,h` | 设置单个顶点高度 |
| `--fill-height` | `x,y,w,h,height` | 批量填充矩形区域高度 |
| `--set-water` | `x,y` | 将顶点标记为水域 |
| `--set-mark` | `x,y,land/water` | 设置顶点地表类型 |

**边操作**：

| 操作 | 格式 | 说明 |
|------|------|------|
| `--set-edge` | `gx,gy,方向,标记` | 设置格子边标记。方向：top/bottom/left/right；标记：path/crack/none |

**格子操作**：

| 操作 | 格式 | 说明 |
|------|------|------|
| `--set-tileset` | `gx,gy,名称` | 设置单个格子的 TileSet |
| `--fill-tileset` | `x,y,w,h,名称` | 批量设置矩形区域 TileSet |
| `--set-substyle` | `gx,gy,名称` | 设置单个格子的子风格 |
| `--fill-substyle` | `x,y,w,h,名称` | 批量设置矩形区域子风格 |

可在一次调用中组合多个操作，按顺序执行。

**示例**：

```bash
# 在 (5,5) 处设置高度为 3，并将 (10,10)-(20,20) 区域填充为水域 TileSet
TileTerrainCLI modify --input terrain.json \
  --set-height 5,5,3 \
  --fill-tileset 10,10,10,10,me_tiles_ds
```

---

### validate — 验证地形一致性

检查地形数据是否满足所有约束规则，报告错误和警告。

```bash
TileTerrainCLI validate --input <路径>
```

| 参数 | 说明 |
|------|------|
| `--input` | **（必填）** 要验证的地形文件 |

验证内容包括：高度差是否超限、边标记是否与周围地表类型矛盾、数据结构完整性等。

退出码：0 = 验证通过，1 = 存在错误。

---

### info — 显示地形信息

只读操作，输出地形的基本统计信息。

```bash
TileTerrainCLI info --input <路径>
```

| 参数 | 说明 |
|------|------|
| `--input` | **（必填）** 地形文件 |

**输出内容**：
- 网格尺寸（W×H）和格子总数
- 顶点尺寸（(W+1)×(H+1)）和顶点总数
- 高度范围（最低 ~ 最高）
- 水域顶点数量
- 各 TileSet 分布统计

---

### convert — 转换旧版 TileSet

将旧编辑器格式的 TileSet 资源转换为 UrhoX 格式，生成 JSON 配置文件和对应的模型/材质资源。

```bash
TileTerrainCLI convert --input <目录> --output <目录> [--res-base <目录>] [--batch] [--strip-missing-textures]
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` | **（必填）** | 输入 TileSet 目录（单个）或 tiles 根目录（批量模式） |
| `--output` | "Output/" | 输出目录 |
| `--res-base` | — | 旧引擎资源根目录，用于解析嵌套 Prefab 路径 |
| `--batch` | — | 批量模式：扫描 `--input` 下所有子目录逐一转换 |
| `--strip-missing-textures` | — | 材质中引用的纹理不存在时自动移除引用 |

**示例**：

```bash
# 转换单个 TileSet
TileTerrainCLI convert \
  --input "C:/Res/tiles/me_tiles_field" \
  --output "C:/UrhoXRes" \
  --res-base "C:/Res/" \
  --strip-missing-textures

# 批量转换所有 TileSet
TileTerrainCLI convert \
  --input "C:/Res/tiles/" \
  --output "C:/UrhoXRes" \
  --res-base "C:/Res/" \
  --batch --strip-missing-textures
```

**输出结构**：

```
<output>/
├── TileSets/
│   └── <tileSetName>.json          # TileSet 配置
└── Environment/Legacy/Tiles/
    └── <tileSetName>/
        ├── <prefab>/model.mdl      # 转换后的模型
        └── <prefab>/material.xml   # 转换后的材质
```

---

### generate — 生成场景

从地形数据和 TileSet 配置生成可加载的引擎场景。支持两种模式：

#### 模式一：单场景（scene）

生成单个 Scene XML 文件，适用于小型地图或预览。

```bash
TileTerrainCLI generate --type scene \
  --input <terrain.json> \
  --tileset-dir <TileSet目录> \
  --output <scene.xml>
```

#### 模式二：HLOD 流式场景（hlod）

生成完整的 WorldPartition 多级 LOD 流式场景，适用于大型开放世界。

```bash
TileTerrainCLI generate --type hlod \
  --input <terrain.json> \
  --tileset-dir <TileSet目录> \
  --res-dir <资源目录> \
  --output <输出目录> \
  [--weightmap <权重图.bin>] \
  [--terrain-albedo <纹理数组路径>] \
  [--terrain-mix <纹理数组路径>] \
  [L0/HLOD/装饰层参数...]
```

**通用参数**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` | **（必填）** | 地形文件 |
| `--tileset-dir` | **（必填）** | TileSet JSON 配置目录（自动扫描 *.json） |
| `--type` | "scene" | 生成模式：`scene` 或 `hlod` |
| `--output` | "scene.xml" | 输出路径（scene 模式为文件，hlod 模式为目录） |

**HLOD 模式额外参数**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--res-dir` | — | 资源根目录（用于加载模型/材质）。与 `--pak` 至少提供其一 |
| `--pak` | — | 瓦片资源包文件（UPAK 格式，由 `pack_tile_resources.py` 生成）。提供 UUID 映射和资源查找。可单独使用，也可与 `--res-dir` 配合使用 |
| `--weightmap` | — | 权重图文件（启用地表纹理混合） |
| `--terrain-albedo` | "TileSets/TerrainMix/BaseColor_Terrain.xml" | 地表反照率纹理数组 |
| `--terrain-mix` | "TileSets/TerrainMix/MixColor_Terrain.xml" | 地表法线/粗糙度纹理数组 |
| `--cell-size` | 40.96 | L0 单元尺寸（米） |
| `--l0-range` | 100.0 | L0 加载距离（米） |
| `--hlod-levels` | 2 | HLOD 层级数（1=仅 L1，2=L1+L2） |
| `--l1-cell-size` | 81.92 | L1 单元尺寸（米） |
| `--l1-range` | 250.0 | L1 加载距离（米） |
| `--l2-cell-size` | 163.84 | L2 单元尺寸（米） |
| `--l2-range` | 500.0 | L2 加载距离（米） |
| `--unload-margin` | 30.0 | 卸载余量（米），防止边界反复加载/卸载 |
| `--deco-cell-size` | 128.0 | 装饰层单元尺寸（米） |
| `--deco-range` | 300.0 | 装饰层加载距离（米） |

**HLOD 输出结构**：

```
<output>/
├── scene.xml                           # 主场景文件（包含 WorldPartition 组件）
├── world_partition.json                # 流式配置（所有层级和单元索引）
├── uuid_mappings.json                  # UUID → 文件路径映射表
├── terrain_control.png                 # 地表控制图（如有权重图）
├── TileTerrainBlend.xml                # 地表混合材质
├── cells/
│   ├── L0/
│   │   ├── cell_0_0.json              # L0 单元元数据
│   │   ├── cell_0_0.xml               # L0 单元场景数据
│   │   ├── cell_0_0_chunk_*.json      # 子块运行时数据
│   │   └── ...
│   ├── L1/
│   │   ├── cell_0_0.json
│   │   ├── cell_0_0.xml
│   │   ├── cell_0_0_proxy.mdl         # L1 简化代理网格
│   │   └── ...
│   ├── L2/                             # （如 hlod-levels >= 2）
│   │   └── ...
│   └── decoration/
│       ├── deco_0_0.json
│       ├── deco_0_0.xml               # 装饰物 HISM 实例数据
│       └── ...
└── *.meta                              # 每个输出文件的 UUID 元数据
```

**示例**：

```bash
# 生成完整 HLOD 场景（含地表混合）
TileTerrainCLI generate --type hlod \
  --input C:/tmp/terrain/terrain.json \
  --output C:/tmp/terrain/world \
  --res-dir C:/UrhoXRes \
  --tileset-dir C:/UrhoXRes/TileSets \
  --weightmap C:/tmp/terrain/terrain_weights.bin \
  --terrain-albedo "TileSets/TerrainMix/BaseColor_Terrain.xml" \
  --terrain-mix "TileSets/TerrainMix/MixColor_Terrain.xml"
```

---

### analyze-mesh — 分析瓦片网格边缘

分析 MDL 模型文件的边缘顶点分布，用于验证瓦片网格是否适合拼接和 LOD 简化时的边缘锁定。

```bash
TileTerrainCLI analyze-mesh --dir <目录>
TileTerrainCLI analyze-mesh --file <文件>
```

| 参数 | 说明 |
|------|------|
| `--dir` | 递归扫描目录下所有 .mdl 文件 |
| `--file` | 分析单个 .mdl 文件 |

输出每个模型在四条边（上/下/左/右）的顶点数量和分布规律。

---

### init-weightmap — 初始化权重图

创建与地形尺寸匹配的空白权重图，所有纹理权重初始化为 0。

```bash
TileTerrainCLI init-weightmap --terrain <terrain.json> --output <路径>
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--terrain` | **（必填）** | 源地形文件（用于确定尺寸） |
| `--output` | "terrain_weights.bin" | 输出权重图文件 |

权重图分辨率为地形网格的 4 倍（每个格子 4×4 采样点），以二进制格式存储。

---

### paint-texture — 绘制地表纹理

使用圆形笔刷在权重图上绘制纹理层，模拟画笔操作。

```bash
TileTerrainCLI paint-texture \
  --weightmap <权重图.bin> \
  --pos <x,z> \
  --layer <纹理ID> \
  [--radius <半径>] \
  [--strength <强度>] \
  [--output <路径>]
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--weightmap` | **（必填）** | 权重图文件 |
| `--pos` | **（必填）** | 世界坐标位置（x,z），逗号分隔 |
| `--layer` | 0 | 纹理层 ID（0-255） |
| `--radius` | 10.0 | 笔刷半径（米） |
| `--strength` | 1.0 | 绘制强度（0.0-1.0），中心最强向边缘衰减 |
| `--output` | — | 输出文件（默认覆盖输入文件） |

可以通过多次调用叠加绘制不同纹理层。

**示例**：

```bash
# 在世界坐标 (100, 50) 处绘制纹理层 3，半径 20m
TileTerrainCLI paint-texture \
  --weightmap terrain_weights.bin \
  --pos 100,50 \
  --layer 3 \
  --radius 20 \
  --strength 0.8
```

---

### bake-controlmap — 烘焙控制图

将权重图烘焙为 PNG 纹理，供渲染材质使用。

```bash
TileTerrainCLI bake-controlmap --weightmap <权重图.bin> --output <路径>
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--weightmap` | **（必填）** | 权重图文件 |
| `--output` | "terrain_control.png" | 输出 PNG 文件 |

输出的 PNG 图像编码了每个采样点的纹理层 ID 和混合权重，可直接作为材质控制贴图使用。也可以用图像编辑器查看和手动调整。

> 注意：`generate --type hlod` 在指定了 `--weightmap` 时会自动执行烘焙，通常无需单独调用此命令。

---

## 瓦片资源打包（pak）

### pack_tile_resources.py — 打包瓦片地形资源

将瓦片地形所需的资源（模型、材质、预制体、TileSet 配置、UUID 映射）打包为 UPAK 格式的 pak 文件，排除纹理以减小体积。

```bash
python tools/project-tools/pack_tile_resources.py --res-dir <资源目录> --output <输出路径> [--dry-run]
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--res-dir` | **（必填）** | 资源根目录（如 UrhoXRes/） |
| `--output` | "tile_resources.pak" | 输出 pak 文件路径 |
| `--dry-run` | — | 只列出文件统计，不实际打包 |

**打包内容**：

| 目录/文件 | 包含扩展名 | 说明 |
|-----------|-----------|------|
| `Environment/Legacy/**` | .mdl, .xml, .material | 瓦片/装饰物模型、材质、预制体 |
| `TileSets/**` | .json | TileSet 配置文件 |
| `uuid_mappings.json` | — | UUID → 路径映射表 |

**排除**：`.png`, `.jpg`, `.jpeg`, `.dds`, `.tga`, `.bmp`, `.ktx`, `.pvr`（纹理），`.meta`（编辑器元数据）

**示例**：

```bash
# 打包瓦片资源（约 31 MB，排除 ~284 MB 纹理）
python tools/project-tools/pack_tile_resources.py \
  --res-dir C:/Workspace/SCE/UrhoXRes \
  --output C:/tmp/tile_resources.pak

# 预览打包内容（不写文件）
python tools/project-tools/pack_tile_resources.py \
  --res-dir C:/Workspace/SCE/UrhoXRes \
  --dry-run
```

**在 TileTerrainCLI 中使用**：

```bash
# 仅使用 pak（无需 --res-dir）
TileTerrainCLI generate --type hlod \
  --input terrain.json \
  --output world/ \
  --pak C:/tmp/tile_resources.pak \
  --tileset-dir C:/UrhoXRes/TileSets \
  --weightmap terrain_weights.bin

# --pak 与 --res-dir 配合使用
TileTerrainCLI generate --type hlod \
  --input terrain.json \
  --output world/ \
  --res-dir C:/UrhoXRes \
  --pak C:/tmp/tile_resources.pak \
  --tileset-dir C:/UrhoXRes/TileSets \
  --weightmap terrain_weights.bin
```

**注意事项**：

- `--res-dir` 和 `--pak` 至少提供其一；同时提供时两者互补，优先从 pak 查找资源
- pak 中的文件路径保留原始大小写，与 `PackageFile::Exists()` 精确匹配一致
- UPAK 格式与引擎 PackageTool 生成的格式完全兼容

---

## 典型工作流

### 1. 转换旧资源

```bash
# 批量转换所有 TileSet
TileTerrainCLI convert --input C:/Res/tiles/ --output C:/UrhoXRes \
  --res-base C:/Res/ --batch --strip-missing-textures
```

### 2. 创建并编辑地形

```bash
# 创建 128×64 地形
TileTerrainCLI create --width 128 --height 64 --output terrain.json

# 设置不同区域的 TileSet
TileTerrainCLI modify --input terrain.json \
  --fill-tileset 0,0,64,64,me_tiles_field \
  --fill-tileset 64,0,64,64,me_tiles_snow

# 设置高度
TileTerrainCLI modify --input terrain.json \
  --fill-height 30,20,10,10,3

# 验证
TileTerrainCLI validate --input terrain.json
```

### 3. 绘制地表纹理

```bash
# 初始化权重图
TileTerrainCLI init-weightmap --terrain terrain.json --output terrain_weights.bin

# 绘制草地层
TileTerrainCLI paint-texture --weightmap terrain_weights.bin \
  --pos 50,50 --layer 1 --radius 30 --strength 1.0

# 绘制泥土路径
TileTerrainCLI paint-texture --weightmap terrain_weights.bin \
  --pos 80,50 --layer 2 --radius 5 --strength 0.9
```

### 4. 生成流式场景

```bash
TileTerrainCLI generate --type hlod \
  --input terrain.json \
  --output world/ \
  --res-dir C:/UrhoXRes \
  --tileset-dir C:/UrhoXRes/TileSets \
  --weightmap terrain_weights.bin
```

### 5. 在引擎中加载

```bash
# 使用 -editor_debug 加载生成目录（多路径用分号分隔）
UrhoXRuntime.exe ScenePreview.lua \
  -editor_debug "C:/UrhoXRes;C:/tmp/terrain/world"
```

---

*最后更新: 2026-03-16*
