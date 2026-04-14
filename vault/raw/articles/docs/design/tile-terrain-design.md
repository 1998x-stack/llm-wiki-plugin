---
summary: "TileTerrain system design migrating old engine TileEditorModule algorithms to UrhoX with component architecture"
related_paths:
  - engine/Source/Urho3D/TileTerrain/**
last_updated: "2026-04-02"
---

# TileTerrain 系统设计文档

> 基于旧引擎 TileEditorModule 的核心地形算法，迁移到 UrhoX 引擎的全新设计。
> 采用组件化架构，解耦为程序化数据层和场景生成层，供 MCP 工具链调用。

---

## 目录

- [1. 背景与目标](#1-背景与目标)
- [2. 整体架构](#2-整体架构)
- [3. Module 1: TileTerrainData（程序化地形数据）](#3-module-1-tileterraindata程序化地形数据)
- [4. Module 2: TileSceneGenerator（场景资源生成）](#4-module-2-tilescenegenerator场景资源生成)
- [5. TileSet JSON 格式规范](#5-tileset-json-格式规范)
- [6. 程序化数据 JSON 格式规范](#6-程序化数据-json-格式规范)
- [7. 命令行工具设计](#7-命令行工具设计)
- [8. TileSet 资源转换（XPrefabConverterLib 扩展）](#8-tileset-资源转换xprefabconverterlib-扩展)
- [9. 关键算法](#9-关键算法)
- [10. TerrainOperator（约束求解层）](#10-terrainoperator约束求解层)
- [11. 单元测试](#11-单元测试)
- [12. PrefabReference（引擎级 Prefab 实例化）](#12-prefabinstance引擎级-prefab-实例化)

---

## 1. 背景与目标

### 1.1 旧系统问题

旧引擎的 TileEditorModule 存在以下设计问题：

- **Tile/Decoration 继承自 Node** — 耦合过深，地形数据与引擎场景图绑定
- **Protobuf 序列化** — 不符合 UrhoX 生态，AI 不可读
- **编辑器逻辑与核心算法混杂** — Brush、Behavior、OperationRecord 等编辑器代码与地形算法耦合
- **Z-up 坐标系 / cm 单位** — 与 UrhoX 的 Y-up / 米制不兼容
- **嵌套 Prefab 结构** — 旧引擎 Prefab 有多层嵌套，需引擎级 PrefabReference 支持才能保留引用链

### 1.2 设计目标

1. **解耦为两层** — 程序化数据层（纯算法）+ 场景生成层（资源映射）
2. **组件化设计** — 不使用 Node 继承，用数据结构 + 算法的形式
3. **JSON 可读** — 所有配置和数据均使用 JSON，AI 可直接读写和二次编辑
4. **MCP 友好** — 提供命令行工具，分库和二进制两层
5. **UrhoX Scene XML 输出** — 最终生成标准的 UrhoX 场景文件
6. **引擎级 Prefab 实例化** — 新增 PrefabReference 组件，支持 Prefab 嵌套引用

### 1.3 不迁移的内容

- 编辑器 UI（Brush、Indicator、Behavior、MiniMap）
- Undo/Redo（OperationRecord）
- Camera/Light 控制
- fixHeight 高度约束

---

## 2. 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        MCP Tool                             │
│                                                             │
│  ┌────────────────────┐       ┌──────────────────────────┐  │
│  │  Module 1:         │       │  Module 2:               │  │
│  │  TileTerrainData   │──────>│  TileSceneGenerator      │  │
│  │  (纯算法/数据)      │       │  (场景资源生成)           │  │
│  │                    │       │                          │  │
│  │  - TerrainMap      │       │  - TileSetConfig         │  │
│  │  - 创建/修改地形    │       │  - TileSetMatcher        │  │
│  │  - 保存/加载 JSON   │       │  - SceneBuilder          │  │
│  └────────────────────┘       └──────────────────────────┘  │
│         ↕ 读写                           ↓                  │
│  程序化数据 JSON                   Scene XML + 资源引用      │
│  (可二次编辑)                           ↓                   │
│                                  外部 Cooking 工具          │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 代码位置

```
engine/Source/Tools/TileTerrain/
├── CMakeLists.txt
├── Lib/                           # 第一层：库（供内部代码调用）
│   ├── TileTerrainLib.h           # 库的统一头文件
│   │
│   ├── Data/                      # Module 1: 程序化地形数据
│   │   ├── TerrainMap.h/cpp       # 地形网格数据结构 + 操作
│   │   ├── TerrainPoint.h         # 顶点（高度、标记）
│   │   ├── TerrainEdge.h          # 边（标记）
│   │   ├── TerrainGrid.h          # 格子（4顶点+4边+destruction）
│   │   ├── TerrainTypes.h         # 枚举和常量定义
│   │   └── TerrainSerializer.h/cpp # JSON 序列化/反序列化
│   │
│   ├── Operator/                  # 约束求解层（基于 SPFA 的地形操作）
│   │   ├── TerrainOperator.h/cpp  # 带约束的地形修改操作
│   │   └── ConstraintSolver.h/cpp # SPFA 约束求解器
│   │
│   ├── TileSet/                   # TileSet 配置和匹配
│   │   ├── TileSetConfig.h/cpp    # TileSet JSON 数据结构
│   │   ├── TileKey.h/cpp          # 匹配键 + 归一化算法
│   │   └── TileSetMatcher.h/cpp   # 匹配引擎
│   │
│   └── Generator/                 # Module 2: 场景生成
│       ├── TileSceneGenerator.h/cpp  # 场景组装（TerrainMap + TileSet → Scene XML）
│       └── DecorationEvaluator.h/cpp # 装饰条件评估
│
└── CLI/                           # 第二层：命令行工具（供 MCP 调用）
    └── TileTerrainCLI.cpp         # main()，解析命令行参数，调用 Lib
```

### 2.2 依赖关系

```
TileTerrainCLI
  └─> TileTerrainLib
        ├─> Data/TerrainMap          (纯数据，无约束)
        ├─> Operator/TerrainOperator (带约束，SPFA 求解)
        ├─> TileSet/TileSetMatcher   (瓦片匹配)
        ├─> Generator/TileSceneGenerator (场景生成)
        ├─> Urho3D (基础类型: String, Vector, HashMap, Vector3, Quaternion, JSONValue...)
        ├─> Urho3D Scene (Scene, Node, Component, StaticModel 用于生成 XML)
        └─> Urho3D IO (File, Serializer, Deserializer)
```

---

## 3. Module 1: TileTerrainData（程序化地形数据）

### 3.1 核心数据结构

#### TerrainTypes.h — 枚举定义

```cpp
namespace TileTerrain
{

/// 顶点标记（地形类型）
enum PointMark
{
    PM_LAND = 0,       // 陆地
    PM_WATER = 1,      // 水面
};

/// 边标记（位标志）
enum EdgeMark : unsigned
{
    EM_NONE = 0,       // 无标记
    EM_PATH = 1 << 0,  // 坡道
    EM_CRACK = 1 << 1, // 悬崖/裂缝
};

/// 格子分类（根据顶点和边标记自动推导）
enum GridType
{
    GT_LAND,           // 平地
    GT_WATER,          // 水面
    GT_PATH,           // 坡道
    GT_CRACKS,         // 悬崖
};

/// 格子顶点索引
///  TL(3) --- TR(2)
///    |         |
///  BL(0) --- BR(1)
enum Corner { BL = 0, BR = 1, TR = 2, TL = 3 };

/// 格子边索引
///       Top(2)
///  Left(3)   Right(1)
///      Bottom(0)
enum Edge { BOTTOM = 0, RIGHT = 1, TOP = 2, LEFT = 3 };

/// 邻居方向（6 方向，含对角）
enum Neighbor { N = 0, NE, E, SE, S, SW };

} // namespace TileTerrain
```

#### TerrainPoint.h — 顶点

```cpp
struct TerrainPoint
{
    int height = 0;            // 离散高度（单位：tileThickness 的倍数）
    int expectHeight = 0;      // 期望高度（坡道计算用）
    PointMark mark = PM_LAND;  // 地形标记
};
```

#### TerrainEdge.h — 边

```cpp
struct TerrainEdge
{
    unsigned mark = EM_NONE;   // 边标记（位标志，可组合）
};
```

#### TerrainGrid.h — 格子

```cpp
struct TerrainGrid
{
    int destruction[4] = {0, 0, 0, 0};  // 四角破坏值
    String tileSetName;                  // 该格子使用的 TileSet 名称

    /// 根据关联的顶点和边数据推导格子类型
    GridType GetGridType(const TerrainPoint points[4],
                         const TerrainEdge edges[4]) const;
};
```

#### TerrainMap.h — 地形网格

```cpp
class TerrainMap
{
public:
    /// 创建指定尺寸的地形（width × height 个格子）
    void Create(int width, int height, const String& defaultTileSet);

    /// 尺寸
    int GetWidth() const;
    int GetHeight() const;

    // === 顶点操作 ===
    // 顶点网格比格子网格大 1: (width+1) × (height+1)

    /// 设置/获取顶点高度
    void SetPointHeight(int x, int y, int height);
    int GetPointHeight(int x, int y) const;

    /// 设置/获取顶点期望高度
    void SetPointExpectHeight(int x, int y, int expectHeight);
    int GetPointExpectHeight(int x, int y) const;

    /// 设置/获取顶点标记（陆地/水面）
    void SetPointMark(int x, int y, PointMark mark);
    PointMark GetPointMark(int x, int y) const;

    // === 边操作 ===
    // 水平边: width × (height+1) 条
    // 垂直边: (width+1) × height 条

    /// 设置/获取边标记
    void SetEdgeMark(int gridX, int gridY, Edge edge, unsigned mark);
    unsigned GetEdgeMark(int gridX, int gridY, Edge edge) const;

    // === 格子操作 ===

    /// 设置/获取格子破坏值
    void SetDestruction(int x, int y, const int destruction[4]);
    void GetDestruction(int x, int y, int destruction[4]) const;

    /// 设置/获取格子的 TileSet 名称
    void SetGridTileSet(int x, int y, const String& tileSetName);
    const String& GetGridTileSet(int x, int y) const;

    /// 获取格子类型（自动推导）
    GridType GetGridType(int x, int y) const;

    // === 批量操作 ===

    /// 区域填充高度
    void FillHeight(int x, int y, int w, int h, int height);

    /// 区域填充顶点标记
    void FillPointMark(int x, int y, int w, int h, PointMark mark);

    // === 查询 ===

    /// 获取格子的 4 个顶点数据
    void GetGridPoints(int x, int y, TerrainPoint points[4]) const;

    /// 获取格子的 4 条边数据
    void GetGridEdges(int x, int y, TerrainEdge edges[4]) const;

    // === 约束 ===

    /// 最大坡度约束
    int GetMaxDeltaGrade() const;
    void SetMaxDeltaGrade(int maxDelta);

    // === 序列化 ===

    /// 保存/加载 JSON
    bool SaveJSON(const String& path) const;
    bool LoadJSON(const String& path);

    /// 与 JSONValue 互转
    JSONValue ToJSON() const;
    bool FromJSON(const JSONValue& json);

private:
    int width_ = 0;
    int height_ = 0;
    int maxDeltaGrade_ = 1;

    // 顶点: (width+1) * (height+1)
    Vector<TerrainPoint> points_;
    // 水平边: width * (height+1), 垂直边: (width+1) * height
    Vector<TerrainEdge> hEdges_;
    Vector<TerrainEdge> vEdges_;
    // 格子: width * height
    Vector<TerrainGrid> grids_;
};
```

### 3.2 顶点/边/格子的索引关系

```
顶点 (width+1) × (height+1):
  pointIndex = y * (width+1) + x

        x=0   x=1   x=2   x=3
  y=3:  P03 — P13 — P23 — P33
         |  G02 |  G12 |  G22 |
  y=2:  P02 — P12 — P22 — P32
         |  G01 |  G11 |  G21 |
  y=1:  P01 — P11 — P21 — P31
         |  G00 |  G10 |  G20 |
  y=0:  P00 — P10 — P20 — P30

格子 Grid(gx, gy) 的 4 个顶点:
  BL = Point(gx,   gy)
  BR = Point(gx+1, gy)
  TR = Point(gx+1, gy+1)
  TL = Point(gx,   gy+1)

格子 Grid(gx, gy) 的 4 条边:
  Bottom = HEdge(gx,   gy)       水平
  Top    = HEdge(gx,   gy+1)     水平
  Left   = VEdge(gx,   gy)       垂直
  Right  = VEdge(gx+1, gy)       垂直
```

---

## 4. Module 2: TileSceneGenerator（场景资源生成）

### 4.1 TileSetConfig — 数据容器

从 TileSet JSON 文件加载的纯数据结构，不含逻辑。

```cpp
namespace TileTerrain
{

struct TilePrefabRef
{
    String prefab;                 // prefab 资源路径（如 "Prefabs/Tiles/hope/ground_flat.xml"）
    Vector3 position;
    Quaternion rotation;
    Vector3 scale;
};

struct DecoSlotDef
{
    String group;                  // 引用 decorationGroups 的 key
    String condition[4];           // BL/BR/TR/TL: "land" / "water" / "any"
    Vector3 position;
    Quaternion rotation;
    Vector3 scale;
};

struct TileDef
{
    String id;                     // 唯一标识（如 "ground_0_0_0_0_0_0_0_0"）
    String type;                   // "land" / "water" / "path" / "cracks"
    TileKey key;                   // 匹配键
    Vector<String> pointMarks;     // 顶点标记（水面瓦片需要），默认全 "land"
    Vector<TilePrefabRef> models;  // 瓦片模型 prefab 引用（可能多个）
    Vector<DecoSlotDef> decorationSlots;  // 装饰槽位
    float weight = 1.0f;          // 随机选择权重
};

struct DecoVariant
{
    String prefab;                 // 装饰 prefab 资源路径
    Vector3 position;              // 变体自身偏移
    Quaternion rotation;
    Vector3 scale;
    float weight = 1.0f;
};

struct TileSetConfig
{
    String name;                   // TileSet 名称
    int version = 1;
    float tileSize = 2.56f;       // 单个瓦片边长（米）
    float tileThickness = 1.28f;  // 一级高度差（米）
    int maxDeltaGrade = 1;

    Vector<TileDef> tiles;         // 所有瓦片定义
    HashMap<String, Vector<DecoVariant>> decorationGroups;  // 装饰组

    /// 从 JSON 文件加载
    bool LoadJSON(const String& path);
    /// 保存为 JSON 文件
    bool SaveJSON(const String& path) const;
};

} // namespace TileTerrain
```

### 4.2 TileKey — 匹配键

```cpp
struct TileKey
{
    int heights[4] = {};        // BL, BR, TR, TL
    int edgeMarks[4] = {};      // Bottom, Right, Top, Left
    int destruction[4] = {};    // BL, BR, TR, TL

    /// 高度归一化：减去最小高度，返回 baseHeight
    /// [128, 128, 256, 128] → [0, 0, 128, 0], baseHeight = 128
    TileKey AdjustHeight(int& outBaseHeight) const;

    /// 旋转归一化：找到字典序最小的旋转，返回旋转次数 (0-3)
    /// [0, 0, 128, 0] 旋转 1 次 → [0, 0, 0, 128]
    TileKey Normalize(int& outRotation) const;

    /// 旋转 key（逆时针 90° × n 次）
    TileKey Rotate(int n) const;

    unsigned ToHash() const;
    bool operator==(const TileKey& rhs) const;
};
```

### 4.3 TileSetMatcher — 匹配引擎

```cpp
class TileSetMatcher
{
public:
    /// 从 TileSetConfig 构建索引
    void Build(const TileSetConfig& config);

    /// 匹配结果
    struct MatchResult
    {
        const TileDef* tile = nullptr;  // 命中的瓦片定义
        int rotation = 0;               // 需旋转几个 90°（0-3）
        int baseHeight = 0;             // 最低点高度值
        bool valid = false;             // 是否匹配成功
    };

    /// 核心匹配：给定地形数据，匹配瓦片定义
    MatchResult Match(const int heights[4],
                      const int edgeMarks[4],
                      const int destruction[4]) const;

    /// 装饰评估结果
    struct DecoResult
    {
        String prefab;                 // 装饰 prefab 资源路径
        Vector3 position;              // 最终位置 = slot × variant
        Quaternion rotation;           // 最终旋转
        Vector3 scale;                 // 最终缩放
    };

    /// 评估装饰：根据匹配结果 + 周围顶点标记，生成装饰列表
    Vector<DecoResult> EvaluateDecorations(
        const MatchResult& match,
        const PointMark pointMarks[4]) const;

private:
    /// 归一化 key 的哈希 → 候选瓦片定义列表
    HashMap<unsigned, Vector<const TileDef*>> index_;

    const TileSetConfig* config_ = nullptr;

    /// 按权重随机选择
    const TileDef* SelectByWeight(const Vector<const TileDef*>& candidates) const;
    const DecoVariant* SelectVariant(const Vector<DecoVariant>& variants) const;
};
```

### 4.4 TileSceneGenerator — 场景组装

```cpp
class TileSceneGenerator
{
public:
    TileSceneGenerator(Context* context);

    /// 注册 TileSet（支持多 TileSet 混用）
    void AddTileSet(const TileSetConfig& config);

    /// 从 TerrainMap 生成 Scene XML
    /// 返回是否成功
    bool Generate(const TerrainMap& map, const String& outputPath);

    /// 获取生成统计
    struct Stats
    {
        int totalGrids = 0;        // 总格子数
        int matchedGrids = 0;      // 成功匹配的格子数
        int failedGrids = 0;       // 匹配失败的格子数
        int decorationsPlaced = 0; // 放置的装饰数
    };
    const Stats& GetStats() const;

private:
    Context* context_;
    HashMap<String, TileSetMatcher> matchers_;  // TileSet 名称 → Matcher
    Stats stats_;

    /// 为单个格子生成 Node
    Node* GenerateGridNode(Node* parent,
                           const TerrainMap& map,
                           int gx, int gy,
                           const TileSetMatcher& matcher,
                           const TileSetConfig& config);
};
```

### 4.5 场景生成流程

```
TileSceneGenerator::Generate(map, outputPath):

  1. 创建 Scene
     - 添加 Octree 组件（空间查询）

  2. 创建 TileMap 根节点
     - name = "TileMap"
     - 附加自定义属性: width, height, tileSize, tileThickness

  3. 遍历 TerrainMap 的每个 grid(gx, gy):

     a. 获取 grid 的 tileSetName → 查找对应的 TileSetMatcher

     b. 从 map 提取该 grid 的:
        - heights[4]（4 个顶点高度）
        - edgeMarks[4]（4 条边标记）
        - destruction[4]（4 角破坏值）
        - pointMarks[4]（4 个顶点地形标记）

     c. TileSetMatcher::Match(heights, edgeMarks, destruction)
        → MatchResult { tile, rotation, baseHeight }

     d. 创建 Grid Node:
        - name = "Tile_{gx}_{gy}"
        - position = (gx * tileSize, baseHeight * tileThickness, gy * tileSize)
        - rotation = Quaternion(0, rotation * 90, 0)

     e. 对 tile.models 中每个 TilePrefabRef:
        - 创建子 Node
        - 添加 PrefabReference 组件，设置 prefab 资源路径
        - 设置 local transform

     f. TileSetMatcher::EvaluateDecorations(match, pointMarks)
        → Vector<DecoResult>

     g. 对每个 DecoResult:
        - 创建子 Node
        - 添加 PrefabReference 组件，设置 prefab 资源路径
        - 设置 transform (已合并 slot × variant)

  4. Scene::SaveXML(outputPath)
```

### 4.6 生成的 Scene XML 结构

```xml
<?xml version="1.0"?>
<scene id="1">
    <component type="Octree" id="1" />

    <node id="2">
        <attribute name="Name" value="TileMap" />

        <!-- Grid (0, 0) — 平地 -->
        <node id="3">
            <attribute name="Name" value="Tile_0_0" />
            <attribute name="Position" value="0 0 0" />
            <attribute name="Rotation" value="1 0 0 0" />

            <!-- 瓦片主模型 — 通过 PrefabReference 引用 -->
            <node id="4">
                <component type="PrefabReference" id="5">
                    <attribute name="Prefab"
                        value="PrefabResource;Prefabs/Tiles/me_tiles_hope/ground_flat.xml" />
                </component>
                <!-- PrefabReference 运行时会在此 node 下实例化 prefab 子树 (temporary) -->
            </node>

            <!-- 装饰 — 通过 PrefabReference 引用 -->
            <node id="6">
                <attribute name="Position" value="0.5 0 0.3" />
                <component type="PrefabReference" id="7">
                    <attribute name="Prefab"
                        value="PrefabResource;Prefabs/Decorations/me_tiles_hope/decal_grass_01.xml" />
                </component>
            </node>
        </node>

        <!-- Grid (1, 0) — 坡道 -->
        <node id="8">
            <attribute name="Name" value="Tile_1_0" />
            <attribute name="Position" value="2.56 0 0" />
            <attribute name="Rotation" value="0.707 0 0.707 0" />
            <!-- ... -->
        </node>
    </node>
</scene>
```

---

## 5. TileSet JSON 格式规范

### 5.1 完整结构

```jsonc
{
  // === 元信息 ===
  "name": "me_tiles_hope",        // TileSet 名称
  "version": 1,                   // 配置版本号
  "tileSize": 2.56,               // 单个瓦片边长（米）
  "tileThickness": 1.28,          // 一级高度差（米）
  "maxDeltaGrade": 1,             // 最大坡度约束

  // === 瓦片定义 ===
  "tiles": [
    {
      "id": "ground_0_0_0_0_0_0_0_0",    // 唯一标识
      "type": "land",                      // 类型: land/water/path/cracks
      "key": {
        "heights": [0, 0, 0, 0],           // 4 角高度 [BL, BR, TR, TL]
        "edgeMarks": [0, 0, 0, 0],         // 4 边标记 [Bottom, Right, Top, Left]
        "destruction": [0, 0, 0, 0]        // 4 角破坏值
      },
      "pointMarks": ["land", "land", "land", "land"],  // 可选，默认全 "land"
      "models": [
        {
          "prefab": "Prefabs/Tiles/me_tiles_hope/ground_flat.xml",  // prefab 资源引用
          "position": [0, 0, 0],           // [x, y, z]
          "rotation": [0, 0, 0, 1],        // [x, y, z, w] quaternion
          "scale": [1, 1, 1]
        }
      ],
      "decorationSlots": [
        {
          "group": "decal_ground_01",      // 引用 decorationGroups 的 key
          "condition": {
            "BL": "land",                  // "land" / "water" / "any"
            "BR": "land",
            "TR": "land",
            "TL": "land"
          },
          "position": [0.5, 0, 0.3],
          "rotation": [0, 0, 0, 1],
          "scale": [1, 1, 1]
        }
      ],
      "weight": 1.0                        // 随机选择权重
    }
  ],

  // === 装饰组 ===
  "decorationGroups": {
    "decal_ground_01": [
      {
        "prefab": "Prefabs/Decorations/me_tiles_hope/decal_grass_01.xml",  // prefab 资源引用
        "position": [0, 0, 0],            // 变体自身偏移
        "rotation": [0, 0, 0, 1],
        "scale": [1, 1, 1],
        "weight": 1.0
      }
    ]
  }
}
```

### 5.2 字段规则

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `tiles[].id` | 是 | — | 唯一标识，用于调试和日志 |
| `tiles[].type` | 是 | — | 影响格子分类语义 |
| `tiles[].key` | 是 | — | 匹配键 |
| `tiles[].pointMarks` | 否 | 全 `"land"` | 仅水面瓦片需要设置 |
| `tiles[].models` | 是 | — | 至少一个 prefab 引用 |
| `tiles[].decorationSlots` | 否 | `[]` | 无装饰的瓦片可省略 |
| `tiles[].weight` | 否 | `1.0` | 同 key 多变体时的选择权重 |
| `decorationSlots[].condition` | 是 | — | 4 个角的条件 |
| `decorationGroups` 的 transform | 否 | 单位变换 | position=[0,0,0], rotation=[0,0,0,1], scale=[1,1,1] |

### 5.3 同 Key 多变体

相同 `key` 的多个 tile 条目会被归为一组，按 `weight` 概率随机选择：

```jsonc
// 变体 1: 权重 1.0
{ "id": "ground_flat_v1", "key": {...}, "weight": 1.0, ... }
// 变体 2: 权重 0.3（约 23% 概率）
{ "id": "ground_flat_v2", "key": {...}, "weight": 0.3, ... }
// 变体 3: 权重 0.1（约 7.7% 概率）
{ "id": "ground_flat_v3", "key": {...}, "weight": 0.1, ... }

// 选中概率 = weight / sum(所有变体 weight)
```

---

## 6. 程序化数据 JSON 格式规范

Module 1 输出的地形数据格式，供 AI 读写和二次编辑。

### 6.1 完整结构

```jsonc
{
  // === 元信息 ===
  "version": 1,
  "width": 10,                     // 格子宽度
  "height": 8,                     // 格子高度
  "maxDeltaGrade": 1,
  "defaultTileSet": "me_tiles_hope",

  // === 顶点数据 (width+1) × (height+1) ===
  // 行优先存储: points[y * (width+1) + x]
  "points": {
    "heights": [0, 0, 0, 0, 128, ...],    // 逐顶点高度值
    "expectHeights": [0, 0, 0, 0, 128, ...],
    "marks": [0, 0, 0, 1, 1, ...]         // 0=land, 1=water
  },

  // === 边数据 ===
  "edges": {
    // 水平边: width × (height+1) 条, 行优先
    "horizontal": [0, 0, 1, 0, ...],      // 边标记值
    // 垂直边: (width+1) × height 条, 行优先
    "vertical": [0, 0, 0, 2, ...]
  },

  // === 格子数据 width × height ===
  "grids": {
    // 每个格子 4 个破坏值，展平为 width × height × 4
    "destruction": [0,0,0,0, 0,0,0,0, ...],
    // 每个格子的 TileSet 名称（仅记录与 defaultTileSet 不同的）
    "tileSetOverrides": {
      "3,5": "me_tiles_field",
      "4,5": "me_tiles_field"
    }
  }
}
```

### 6.2 设计原则

- **紧凑数组** — 高度、标记等用平铺数组而非逐对象，大幅减小 JSON 体积
- **稀疏覆盖** — `tileSetOverrides` 仅记录与默认值不同的格子，大部分格子使用 `defaultTileSet`
- **AI 友好** — 结构扁平，AI 可以直接修改数组中的值进行二次编辑
- **可计算** — 格子类型（land/water/path/cracks）不存储，由程序从顶点和边数据推导

### 6.3 体积估算

以 100×100 的地图为例：
- 顶点数: 101 × 101 = 10,201
- 水平边: 100 × 101 = 10,100
- 垂直边: 101 × 100 = 10,100
- 格子数: 100 × 100 = 10,000

```
heights:       10,201 个 int → ~50 KB (每个 ~5 字节含逗号)
expectHeights: 10,201 个 int → ~50 KB
marks:         10,201 个 int → ~30 KB (多为 0，1 字节)
horizontal:    10,100 个 int → ~30 KB
vertical:      10,100 个 int → ~30 KB
destruction:   40,000 个 int → ~80 KB (多为 0)
tileSetOverrides: 稀疏，通常 < 5 KB

总计: ~275 KB (100×100 地图)
```

---

## 7. 命令行工具设计

### 7.1 命令格式

```bash
TileTerrainCLI <command> [options]
```

### 7.2 命令列表

#### `create` — 创建空白地形

```bash
TileTerrainCLI create \
  --width 10 --height 8 \
  --tileset me_tiles_hope \
  --output terrain.json
```

#### `modify` — 修改地形数据

默认走 `TerrainOperator`（带约束传播），加 `--raw` 跳过约束直接写 `TerrainMap`。

```bash
# 设置单个顶点高度（自动传播邻居约束 + 推导边标记）
TileTerrainCLI modify \
  --input terrain.json \
  --set-height 3,5,128 \
  --output terrain.json
# 输出:
# Modified point (3,5) height: 0 → 128
# Propagated: (4,5) height: 0 → 64 (constrained)
# Updated edge: G(3,4) top → PATH
# Total: 2 points modified, 1 edge updated

# 区域填充（自动传播边界约束）
TileTerrainCLI modify \
  --input terrain.json \
  --fill-height 0,0,5,5,128 \
  --output terrain.json

# 设置水面（自动处理水陆高度差约束）
TileTerrainCLI modify \
  --input terrain.json \
  --set-water 3,5 \
  --output terrain.json

# 设置顶点标记
TileTerrainCLI modify \
  --input terrain.json \
  --set-mark 3,5,water \
  --output terrain.json

# 设置边标记
TileTerrainCLI modify \
  --input terrain.json \
  --set-edge 2,3,top,path \
  --output terrain.json

# 设置格子 TileSet
TileTerrainCLI modify \
  --input terrain.json \
  --set-tileset 3,5,me_tiles_field \
  --output terrain.json

# 跳过约束，直接写裸数据（批量导入、精确控制时使用）
TileTerrainCLI modify \
  --input terrain.json \
  --set-height 3,5,128 \
  --raw \
  --output terrain.json
```

#### `validate` — 验证地形数据合法性

```bash
TileTerrainCLI validate --input terrain.json

# 输出:
# ERROR: Point(3,5) h=128, neighbor Point(4,5) h=0, delta=128 > limit=3
# ERROR: Grid(3,4) edge Top: height diff exists but no PATH mark
# WARNING: Grid(7,2) no matching tile in TileSet "me_tiles_hope"
# Result: 2 errors, 1 warning
```

#### `generate` — 生成 Scene XML

```bash
TileTerrainCLI generate \
  --input terrain.json \
  --tileset-dir ./TileSets/ \
  --output scene.xml
```

`--tileset-dir` 指向包含 TileSet JSON 文件的目录：
```
TileSets/
├── me_tiles_hope.json
├── me_tiles_field.json
└── ...
```

#### `info` — 查看地形信息

```bash
TileTerrainCLI info --input terrain.json

# 输出:
# Size: 10 x 8 (80 grids)
# Points: 11 x 9 (99)
# TileSets: me_tiles_hope (72 grids), me_tiles_field (8 grids)
# Height range: 0 ~ 256
# Water grids: 12
```

### 7.3 MCP 调用示例

MCP Tool 通过命令行调用，读取 stdout 的 JSON 输出：

```bash
# 创建地形 → 返回 terrain.json 路径
TileTerrainCLI create --width 20 --height 20 --tileset me_tiles_hope --output /tmp/terrain.json

# AI 修改地形数据（可多次调用）
TileTerrainCLI modify --input /tmp/terrain.json --fill-height 5,5,10,10,128 --output /tmp/terrain.json
TileTerrainCLI modify --input /tmp/terrain.json --set-mark 7,7,water --output /tmp/terrain.json

# 生成场景
TileTerrainCLI generate --input /tmp/terrain.json --tileset-dir /data/TileSets/ --output /tmp/scene.xml

# AI 也可以直接读取/编辑 terrain.json（二次编辑）
```

---

## 8. TileSet 资源转换（XPrefabConverterLib 扩展）

在 `XPrefabConverterLib` 中新增 TileSet 转换功能，将旧引擎的 TileSet 目录转换为新格式。

### 8.1 转换流程

```
输入: Res/tiles/me_tiles_hope/    （旧引擎 TileSet 目录）
                                     ├── config.json
                                     ├── ground/*.prefab
                                     ├── pathbase/*.prefab
                                     ├── decal_path/*.prefab
                                     └── water_*/*.prefab

                    ↓ XPrefabConverterLib::ConvertTileSet()

输出: TileSets/me_tiles_hope.json               （新格式 TileSet JSON）
      Prefabs/Tiles/me_tiles_hope/*.xml          （Prefab XML 文件，保留嵌套）
      Prefabs/Decorations/me_tiles_hope/*.xml    （装饰 Prefab XML 文件）
      Tiles/me_tiles_hope/Models/                （转换后的 .mdl 文件，Y-up / 米制）
      Tiles/me_tiles_hope/Materials/             （拷贝的 .material 文件）
```

### 8.2 转换步骤

1. **扫描目录** — 遍历 TileSet 下所有 `.prefab` 文件
2. **解析 Prefab** — 读取每个 prefab 的 archetype 列表
3. **提取 TileAttribute** — 解析 `tileAttribute` archetype → `key`（heights, edgeMarks, destruction）
4. **生成 Prefab XML（保留嵌套）** — 递归转换旧 EPrefab 结构：
   - 每个 EPrefab 生成一个独立的 Prefab XML 文件
   - 嵌套的子 EPrefab 转为 PrefabReference 组件引用
   - 叶子节点（staticMesh）转为 StaticModel 组件
   - 例：`EPrefab_A → EPrefab_B → mesh` 生成 `A.xml`（含 PrefabReference→B.xml）+ `B.xml`（含 StaticModel）
5. **提取 DecorationProxy** — 解析 `decorationProxy` → `decorationSlots` 条目
6. **构建 DecorationGroups** — 扫描各子目录中的 decoration prefab，生成装饰 Prefab XML，按 group 名归类
7. **坐标转换** — 所有 position/rotation 使用 `AssetsCoordConverter` 转换（Z-up cm → Y-up m）
8. **MDL 转换** — 调用 `AssetsCoordConverter::ConvertMdlFile()` 转换模型文件
9. **材质拷贝** — 原样拷贝 `.material` 和纹理文件
10. **输出 TileSet JSON** — 组装 TileSet JSON，`models[].prefab` 和 `decorationGroups[].prefab` 引用生成的 Prefab XML 路径

### 8.3 API

```cpp
// 在 XPrefabConverterLib 中新增
struct TileSetConvertResult
{
    bool success;
    String outputJsonPath;
    int tilesConverted;
    int modelsConverted;
    int groupsConverted;
    Vector<String> errors;
};

/// 转换单个 TileSet
TileSetConvertResult ConvertTileSet(
    const String& inputTileSetDir,     // 如 "Res/tiles/me_tiles_hope/"
    const String& outputDir,           // 如 "Output/"
    const String& resBasePath = ""     // 旧引擎资源根目录（解析嵌套 prefab 用）
);

/// 批量转换所有 TileSet
Vector<TileSetConvertResult> ConvertAllTileSets(
    const String& inputTilesDir,       // 如 "Res/tiles/"
    const String& outputDir
);
```

---

## 9. 关键算法

### 9.1 TileKey 归一化

目的：相同形状不同朝向的瓦片应匹配到同一个定义。

```
原始 key: heights=[0, 0, 128, 0], edgeMarks=[0, 0, 0, 1]

Step 1: AdjustHeight — 减去最小高度
  minHeight = 0
  heights → [0, 0, 128, 0] (不变)

Step 2: Normalize — 尝试 4 种旋转，选字典序最小的
  rot=0: heights=[0, 0, 128, 0], edgeMarks=[0, 0, 0, 1]
  rot=1: heights=[0, 0, 0, 128], edgeMarks=[0, 0, 1, 0]  ← 最小
  rot=2: heights=[0, 128, 0, 0], edgeMarks=[0, 1, 0, 0]
  rot=3: heights=[128, 0, 0, 0], edgeMarks=[1, 0, 0, 0]

结果: normalizedKey = rot=1 的值, outRotation = 1
```

旋转规则（逆时针 90°）：
```
heights:  [BL, BR, TR, TL] → [BR, TR, TL, BL]
edgeMarks: [Bottom, Right, Top, Left] → [Right, Top, Left, Bottom]
destruction: 同 heights
```

### 9.2 装饰条件评估

条件中的角对应瓦片的 4 个顶点，需要考虑瓦片旋转：

```
瓦片旋转 rotation=1 (逆时针 90°):
  原始条件 [BL, BR, TR, TL] 旋转后变为:
  实际检查 [BR, TR, TL, BL]

  即: condition[(i + rotation) % 4] 对应实际的 pointMarks[i]
```

匹配规则：
```
对每个角 i (0-3):
  rotatedCondition = slot.condition[(i + rotation) % 4]
  if rotatedCondition == "any":  → 跳过（任意都匹配）
  if rotatedCondition == "land"  && pointMarks[i] == PM_LAND:  → 匹配
  if rotatedCondition == "water" && pointMarks[i] == PM_WATER: → 匹配
  否则: → 不匹配，跳过整个 slot
```

### 9.3 Transform 合成

装饰的最终世界 transform 由三层叠加：

```
worldTransform = tileTransform × slotTransform × variantTransform

其中:
  tileTransform:
    position = (gx * tileSize, baseHeight * tileThickness, gy * tileSize)
    rotation = Quaternion(0, rotation * 90, 0)
    scale    = (1, 1, 1)

  slotTransform:
    从 decorationSlots[i] 的 position/rotation/scale

  variantTransform:
    从 decorationGroups[group][selectedVariant] 的 position/rotation/scale
```

### 9.4 格子类型推导

```
GridType GetGridType(points[4], edges[4]):
  // 检查边标记
  combinedEdgeMark = edges[0].mark | edges[1].mark | edges[2].mark | edges[3].mark

  if (combinedEdgeMark & EM_CRACK):
    return GT_CRACKS

  if (combinedEdgeMark & EM_PATH):
    return GT_PATH

  // 检查顶点标记
  for i in 0..3:
    if points[i].mark == PM_WATER:
      return GT_WATER

  return GT_LAND
```

优先级：CRACKS > PATH > WATER > LAND

---

## 10. TerrainOperator（约束求解层）

基于旧引擎 `TileCalc` 的核心算法迁移，采用 **SPFA（Shortest Path Faster Algorithm）约束求解**。
这不是简单的邻居高度检查，而是一个完整的约束满足求解器。

### 10.1 分层设计

```
┌─────────────────────────────────────────────────────┐
│ CLI / MCP                                            │
│   modify --set-height 3,5,128                        │
└───────────┬─────────────────────────────┬────────────┘
            │ 默认                         │ --raw
            ▼                             ▼
  ┌─────────────────────┐      ┌──────────────────┐
  │  TerrainOperator    │      │  TerrainMap      │
  │  (带约束 + 传播)     │      │  (裸读写)        │
  │                     │      │                  │
  │  1. 构建约束图       │      │  直接 set/get    │
  │  2. SPFA 求解       │      │  不做任何检查     │
  │  3. 推导边标记       │      │                  │
  │  4. 返回修改列表     │      │                  │
  └──────────┬──────────┘      └──────────────────┘
             │ 内部调用
             ▼
       TerrainMap
```

### 10.2 TerrainOperator 类设计

```cpp
class TerrainOperator
{
public:
    TerrainOperator(TerrainMap& map);

    /// 地形操作类型（对应旧引擎 TileOperation）
    enum Operation
    {
        OP_LAND_UP,       // 抬升地形
        OP_LAND_DOWN,     // 降低地形
        OP_LAND_LEVEL,    // 平整到指定高度
        OP_WATER,         // 刷水面
        OP_PATH,          // 刷坡道
        OP_CRACKS,        // 刷悬崖
    };

    /// 操作结果（每次修改后返回，让调用方知道影响范围）
    struct ModifyResult
    {
        Vector<IntVector2> modifiedPoints;     // 被改动的顶点坐标
        Vector<IntVector2> modifiedGrids;      // 受影响的格子坐标
        Vector<String> warnings;               // 警告信息
        bool success = false;
    };

    /// 核心操作：修改指定顶点集合的高度
    /// @param points      要修改的顶点坐标列表
    /// @param op          操作类型
    /// @param targetHeight 目标高度（OP_LAND_LEVEL 时使用，其他为 M_MAX_INT）
    /// @param wholeChange  整体变化 vs 部分变化
    ModifyResult ApplyOperation(const Vector<IntVector2>& points,
                                Operation op,
                                int targetHeight = M_MAX_INT,
                                bool wholeChange = true);

    /// 便捷方法：升高单个顶点
    ModifyResult RaisePoint(int x, int y);

    /// 便捷方法：降低单个顶点
    ModifyResult LowerPoint(int x, int y);

    /// 便捷方法：平整区域到指定高度
    ModifyResult LevelArea(int x, int y, int w, int h, int height);

    /// 便捷方法：刷水面
    ModifyResult SetWater(const Vector<IntVector2>& points);

    /// 便捷方法：刷坡道
    ModifyResult SetPath(const Vector<IntVector2>& points);

    /// 便捷方法：刷悬崖
    ModifyResult SetCracks(const Vector<IntVector2>& points);

    /// 验证整个地图合法性（不修改数据）
    struct ValidationResult
    {
        bool valid;
        Vector<String> errors;
        Vector<String> warnings;
    };
    ValidationResult Validate() const;

private:
    TerrainMap& map_;
    ConstraintSolver solver_;
};
```

### 10.3 ConstraintSolver — SPFA 约束求解器

旧引擎 `TileCalc` 的核心算法，重构为独立的求解器类。

```cpp
class ConstraintSolver
{
public:
    ConstraintSolver(const TerrainMap& map);

    /// 求解结果：每个顶点的新高度
    struct SolveResult
    {
        HashMap<int, int> newHeights;     // pointIndex → newHeight
        HashMap<int, unsigned> newEdgeMarks; // edgeIndex → newMark
        bool success = false;
    };

    /// 求解：给定操作和受影响的顶点，计算所有顶点的新高度
    SolveResult Solve(TerrainOperator::Operation op,
                      const Vector<IntVector2>& targetPoints,
                      int targetHeight,
                      bool wholeChange);

private:
    const TerrainMap& map_;

    // === 约束图 ===

    struct Edge
    {
        int from;
        int to;
        int weight;
        enum Flag { FIXED, REVERSE } flag;
    };

    Vector<Edge> edges_;
    Vector<Vector<int>> adjacency_;    // 邻接表: nodeId → edge indices

    void AddEdge(int from, int to, int weight, Edge::Flag flag);
    void ClearGraph();

    // === 图构建阶段 ===

    /// Phase 1: 计算调整高度和方向
    struct SetupResult
    {
        int adjustHeight;
        bool raise;          // true=抬升方向, false=降低方向
        int deltaHeight;     // +1, -1, or 0
        bool twiceSpfa;      // 是否需要两遍 SPFA
    };
    SetupResult Setup(TerrainOperator::Operation op,
                      const Vector<IntVector2>& targetPoints,
                      int targetHeight);

    /// Phase 2: 将目标顶点加入图（初始高度映射）
    void AddTargetVertices(const Vector<IntVector2>& targetPoints,
                           const SetupResult& setup,
                           bool wholeChange);

    /// Phase 3: 添加虚拟源点 → 所有顶点的锚定边
    void AddSourceAnchors();

    /// Phase 4: BFS 从目标顶点出发，添加邻居约束边
    void AddNeighborConstraints(const Vector<IntVector2>& targetPoints,
                                const SetupResult& setup);

    /// Phase 5: 添加已有 Path 边的额外约束
    void AddExistingPathConstraints(const SetupResult& setup);

    // === SPFA 求解 ===

    /// @param type  0=最长路（抬升），1=最短路（降低）
    /// @return false 表示存在负环（约束无法满足）
    bool RunSPFA(int source, int nodeCount, int type);

    /// 反转所有 REVERSE 边的方向和权重符号
    void ReverseEdges();

    // === 后处理 ===

    /// 根据新高度推导边标记
    void DeriveEdgeMarks(TerrainOperator::Operation op,
                         const HashMap<int, int>& newHeights,
                         HashMap<int, unsigned>& outEdgeMarks);

    // === 辅助 ===

    /// 顶点坐标 → 线性索引
    int PointIndex(int x, int y) const;

    /// 获取顶点的邻居列表（直接邻居 + 对角邻居）
    void GetPointNeighbors(int x, int y, Vector<IntVector2>& direct,
                           Vector<IntVector2>& diagonal) const;
};
```

### 10.4 SPFA 约束求解算法详解

此算法来自旧引擎 `TileCalc`，经过实际验证。

#### 10.4.1 算法概述

将地形高度约束问题建模为 **差分约束系统（System of Difference Constraints）**，
通过 SPFA 求解最长路/最短路来得到满足所有约束的高度值。

**核心思想**：
- 每个顶点是图中的一个节点，"高度"对应距离值
- 约束 `h(A) - h(B) <= w` 表示为有向边 `B → A`，权重 `w`
- 求最短路 → 所有约束满足的最小高度方案
- 求最长路 → 所有约束满足的最大高度方案
- 抬升操作求最长路（尽量高），降低操作求最短路（尽量低）

#### 10.4.2 约束图构建

**Step 1: 虚拟源点锚定**

```
为每个已有顶点创建源点锚定边：
  S → Point(x,y), weight = currentHeight

作用：将未被直接修改的顶点锚定在当前高度
```

**Step 2: 目标顶点初始化**

```
对于每个被修改的顶点:
  if (顶点有 expectHeight):
      期望高度 = expectHeight
  else if (wholeChange):
      期望高度 = currentHeight + deltaHeight
  else:
      期望高度 = adjustHeight  （计算得到的目标高度）

  加入 BFS 队列

  if (!wholeChange):
      // 部分修改时，目标顶点之间互加零权边强制同步
      对目标顶点两两之间:
          AddEdge(A, B, 0, FIXED)
          AddEdge(B, A, 0, FIXED)
```

**Step 3: BFS 邻居约束传播**

从目标顶点出发 BFS，为每个访问到的顶点添加与邻居的约束：

```
while BFS队列非空:
    point = dequeue()

    for each neighbor of point:
        if neighbor 未访问:

            // 确定约束权重
            if (neighbor 是直接邻居（上下左右）):
                deltaH = 3    // 最大高度差 3 个单位
            else (对角邻居):
                deltaH = 6    // 最大高度差 6 个单位

            // 添加双向约束边
            if (raise):   // 抬升方向
                AddEdge(point, neighbor, -deltaH, REVERSE)
                AddEdge(neighbor, point, -deltaH, REVERSE)
            else:         // 降低方向
                AddEdge(point, neighbor, deltaH, REVERSE)
                AddEdge(neighbor, point, deltaH, REVERSE)

            enqueue(neighbor)
```

**隐含的高度差约束（不是 maxDeltaGrade 参数）**：

| 邻居关系 | 最大高度差 | 来源 |
|---------|-----------|------|
| 直接邻居（上下左右） | **3 个高度单位** | 边权 ±3 |
| 对角邻居 | **6 个高度单位** | 边权 ±6 |
| Path 边相邻顶点 | **1 个高度单位** | 边权 ±1 |
| Path 边对角顶点 | **2 个高度单位** | 边权 ±2 |

**Step 4: 已有 Path 边的额外约束**

```
for each 已有 PATH 标记的格子:
    for each 角的顶点三元组 (u, v, w):
        if (raise):
            AddEdge(u, v, -1, REVERSE)  // 相邻最多差 1
            AddEdge(v, u, -1, REVERSE)
            AddEdge(u, w, -2, REVERSE)  // 对角最多差 2
        else:
            AddEdge(u, v, 1, REVERSE)
            AddEdge(v, u, 1, REVERSE)
            AddEdge(w, u, 2, REVERSE)
```

#### 10.4.3 SPFA 求解

```cpp
bool RunSPFA(int source, int nodeCount, int type)
{
    // type=0: 最长路（Longest: a > b 时更新）
    // type=1: 最短路（Shortest: a < b 时更新）

    Vector<int> dist(nodeCount, type == 0 ? INT_MIN : INT_MAX);
    Vector<bool> inQueue(nodeCount, false);
    Vector<int> visitCount(nodeCount, 0);

    dist[source] = 0;
    queue.push(source);
    inQueue[source] = true;

    while (!queue.empty())
    {
        int u = queue.front(); queue.pop();
        inQueue[u] = false;
        visitCount[u]++;

        // 环检测：访问次数超过节点数 → 存在负环/正环，约束无法满足
        if (visitCount[u] > nodeCount)
            return false;

        for (each edge (u → v, weight) in adjacency_[u])
        {
            int newDist = dist[u] + weight;
            bool improved = (type == 0) ? (newDist > dist[v])    // 最长路
                                        : (newDist < dist[v]);   // 最短路
            if (improved)
            {
                dist[v] = newDist;
                if (!inQueue[v])
                {
                    queue.push(v);
                    inQueue[v] = true;
                }
            }
        }
    }
    return true;  // 所有约束满足
}
```

#### 10.4.4 双遍 SPFA（twiceSpfa）

当使用 `OP_LAND_LEVEL` 设置指定高度时，可能出现"有的顶点需要抬升，有的需要降低"的情况：

```
场景: 当前高度 [30, 70]，目标高度 50
  - 顶点 A (h=30) 需要抬升到 50
  - 顶点 B (h=70) 需要降低到 50

解法:
  Pass 1: RunSPFA(type=0)    // 最长路，处理抬升方向
  ReverseEdges()              // 反转所有 REVERSE 边的方向和权重符号
  Pass 2: RunSPFA(type=1)    // 最短路，处理降低方向
```

`ReverseEdges()` 的规则：
```
对每条边:
  if (flag == REVERSE):
      (from → to, weight) 变为 (to → from, -weight)
  if (flag == FIXED):
      不变（锚定边不参与反转）
```

#### 10.4.5 边标记后处理

SPFA 求解完成后，根据新高度推导边标记：

```
DeriveEdgeMarks(op, newHeights, outEdgeMarks):

  for each 受影响的格子的每条边:
      oldMark = edge.mark
      newMark = oldMark

      // 如果是当前操作涉及的边，叠加操作标记
      if (edge 在目标区域内):
          switch (op):
              OP_PATH:  newMark |= EM_PATH   // 设置坡道标记
              OP_CRACKS: newMark |= EM_CRACK  // 设置悬崖标记
              其他:      // 不添加新标记

      // 高度变化时的清理规则
      if (边两端高度发生了变化):
          switch (op):
              OP_LAND_UP / OP_LAND_DOWN / OP_LAND_LEVEL / OP_WATER:
                  // 地形操作清除 CRACK 标记，保留 PATH
                  newMark &= ~EM_CRACK

              OP_PATH / OP_CRACKS:
                  // 坡道/悬崖操作中，高度变化的边只保留 PATH
                  if (edge 不是本次操作的目标边):
                      newMark &= EM_PATH  // 只保留 path bit

      outEdgeMarks[edgeIndex] = newMark
```

**规则总结**：

| 操作 | 边标记行为 |
|------|-----------|
| `OP_LAND_UP/DOWN/LEVEL` | 清除 CRACK，保留 PATH |
| `OP_WATER` | 清除 CRACK，保留 PATH |
| `OP_PATH` | 设置 PATH (bit 0) |
| `OP_CRACKS` | 设置 CRACK (bit 1) |

#### 10.4.6 各操作类型的 adjustHeight 计算

```
OP_LAND_UP:
    adjustHeight = min(所有目标顶点高度) + 1
    raise = true, deltaHeight = +1

OP_LAND_DOWN:
    adjustHeight = max(所有目标顶点高度) - 1
    raise = false, deltaHeight = -1

OP_LAND_LEVEL:
    adjustHeight = targetHeight  （由调用方指定）
    raise = (adjustHeight >= 当前高度)
    deltaHeight = 0
    twiceSpfa = (有的顶点高于目标 且 有的低于目标)

OP_WATER:
    adjustHeight = min(所有目标顶点高度) + deltaHeight
    raise = true/false (根据 deltaHeight)

OP_PATH:
    adjustHeight = min(所有目标顶点高度) + 1
    raise = true, deltaHeight = +1
    额外约束: 相邻顶点最大差 1，对角最大差 2

OP_CRACKS:
    adjustHeight = average(所有边界顶点高度)
    raise = false, deltaHeight = 0
    额外约束: 同格子内顶点零差约束（强制平整）
```

### 10.5 完整流程示例

以 `RaisePoint(3, 5)` 为例：

```
输入: 将顶点 (3,5) 抬升，当前高度为 128

Step 1: Setup
  op = OP_LAND_UP
  adjustHeight = 128 + 1 = 129
  raise = true
  deltaHeight = +1
  twiceSpfa = false

Step 2: AddTargetVertices
  Point(3,5): 期望高度 = 129
  加入 BFS 队列

Step 3: AddSourceAnchors
  S → 所有顶点, weight = currentHeight

Step 4: AddNeighborConstraints (BFS from (3,5))
  访问 (3,5) 的邻居:
    (2,5), (4,5), (3,4), (3,6) — 直接邻居, deltaH=3
    (2,4), (4,4), (2,6), (4,6) — 对角邻居, deltaH=6

  对 (4,5) (当前高度=0):
    AddEdge((3,5) → (4,5), -3, REVERSE)
    AddEdge((4,5) → (3,5), -3, REVERSE)

  继续 BFS 到 (4,5) 的邻居...

Step 5: AddExistingPathConstraints
  如果周围有 PATH 格子，添加更严格的 ±1 / ±2 约束

Step 6: RunSPFA(source=S, type=0)  // 最长路
  SPFA 传播：
    dist[(3,5)] = 129
    dist[(4,5)] = max(0, 129-3) = 126  (被约束拉升)
    dist[(5,5)] = max(0, 126-3) = 123
    ...逐步衰减直到不再更新

Step 7: DeriveEdgeMarks
  (3,5) h: 128→129, (4,5) h: 0→126
  Grid(3,5) 的 Right 边：两端高度差 = |129-126| = 3
  → 不需要 PATH 标记（差值在合法范围内，由 TileSet 匹配处理）

Step 8: 写入 TerrainMap
  map_.SetPointHeight(3, 5, 129)
  map_.SetPointHeight(4, 5, 126)
  ...

Step 9: 返回 ModifyResult
  modifiedPoints = [(3,5), (4,5), (5,5), ...]
  modifiedGrids = [(2,4), (3,4), (4,4), (2,5), (3,5), ...]
  success = true
```

---

## 11. 单元测试

### 11.1 测试框架

使用引擎已有的 **Google Test** 框架（`3rd/googletest/`），遵循 `engine/Tests/` 下的现有惯例。

### 11.2 测试位置

```
engine/Tests/TileTerrain/
├── CMakeLists.txt
├── TerrainMapTests.cpp
├── ConstraintSolverTests.cpp
├── TileKeyTests.cpp
├── TileSetMatcherTests.cpp
├── DecorationEvalTests.cpp
└── TerrainSerializerTests.cpp
```

### 11.3 CMake 配置

遵循 `engine/Tests/Server/CMakeLists.txt` 的模式：

```cmake
if (NOT URHO3D_TESTING)
    return ()
endif ()

if (EMSCRIPTEN OR IOS OR ANDROID)
    return ()
endif ()

set (TARGET_NAME TileTerrainTests)

file (GLOB TEST_SOURCES *.cpp)

add_executable (${TARGET_NAME} ${TEST_SOURCES})

target_link_libraries (${TARGET_NAME}
    PRIVATE
        TileTerrainLib        # 被测试的库
        Urho3D
        gtest
        gtest_main
)

target_include_directories (${TARGET_NAME}
    PRIVATE
        ${CMAKE_SOURCE_DIR}/Source/Tools/TileTerrain/Lib
)

add_test (NAME ${TARGET_NAME} COMMAND ${TARGET_NAME})

set_tests_properties (${TARGET_NAME} PROPERTIES
    TIMEOUT 60
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

set_target_properties (${TARGET_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    FOLDER "Tests"
)
```

### 11.4 测试用例设计

#### TerrainMapTests — 地形数据基础操作

| 用例 | 验证内容 |
|------|---------|
| `CreateMap` | 创建后 width/height 正确，所有顶点初始化为 0/PM_LAND |
| `PointIndexing` | 顶点索引计算：`(0,0)`, `(width,height)`, 边界值 |
| `SetGetHeight` | 设置/读取顶点高度，验证值一致 |
| `SetGetPointMark` | 设置/读取顶点标记（PM_LAND, PM_WATER） |
| `SetGetEdgeMark` | 设置/读取边标记（EM_NONE, EM_PATH, EM_CRACK, 组合） |
| `GridPoints` | `GetGridPoints(gx,gy)` 返回正确的 4 个顶点 |
| `GridEdges` | `GetGridEdges(gx,gy)` 返回正确的 4 条边 |
| `GridType` | 验证 GetGridType 的推导逻辑（LAND/WATER/PATH/CRACKS 优先级） |
| `FillHeight` | 区域填充，验证区域内外的值 |
| `FillPointMark` | 区域填充标记 |
| `Destruction` | 设置/读取格子破坏值 |
| `GridTileSet` | 设置/读取格子 TileSet 名称，defaultTileSet 覆盖 |
| `BoundsCheck` | 越界访问不崩溃（防御性） |

#### TerrainSerializerTests — JSON 序列化

| 用例 | 验证内容 |
|------|---------|
| `SaveLoadRoundTrip` | 创建地形 → 修改数据 → SaveJSON → LoadJSON → 数据完全一致 |
| `EmptyMap` | 空地形序列化/反序列化 |
| `SparseOverrides` | tileSetOverrides 只记录非默认值 |
| `LargeMap` | 50×50 地图的序列化性能和正确性 |
| `InvalidJSON` | 加载损坏/不完整的 JSON 不崩溃，返回 false |

#### TileKeyTests — 匹配键算法

| 用例 | 验证内容 |
|------|---------|
| `AdjustHeight` | `[128,128,256,128]` → `[0,0,128,0]`, baseHeight=128 |
| `AdjustHeightZero` | 全零高度不变 |
| `Normalize` | 4 种旋转的 key 归一化到同一结果 |
| `NormalizeRotation` | 验证 outRotation 值正确 (0-3) |
| `Rotate` | 单次旋转的 heights/edgeMarks/destruction 变换正确 |
| `RotateFull` | 旋转 4 次回到原始 |
| `HashConsistency` | 相同 key → 相同 hash |
| `HashNormalized` | 4 种旋转归一化后 hash 相同 |
| `Equality` | `operator==` 精确比较 |
| `DifferentKeys` | 不同 key → 不同 hash（大概率） |

#### ConstraintSolverTests — SPFA 约束求解

| 用例 | 验证内容 |
|------|---------|
| `RaiseSinglePoint` | 抬升一个点，邻居被约束传播 |
| `LowerSinglePoint` | 降低一个点 |
| `LevelToHeight` | 平整到指定高度，双向传播 |
| `NeighborConstraint` | 直接邻居高度差 ≤ 3 |
| `DiagonalConstraint` | 对角邻居高度差 ≤ 6 |
| `PathConstraint` | Path 区域相邻 ≤ 1, 对角 ≤ 2 |
| `WaterOperation` | 水面操作使用 minHeight |
| `CracksAveraging` | 悬崖操作使用平均高度 |
| `TwiceSpfa` | 双遍 SPFA 场景：部分顶点高部分低 |
| `EdgeMarkDerivation` | 高度变化后边标记正确推导 |
| `CrackMarkCleared` | 地形操作清除 CRACK 保留 PATH |
| `PropagationBoundary` | 传播在地图边界正确停止 |
| `LargeArea` | 大面积操作性能和正确性 |

#### TileSetMatcherTests — 瓦片匹配

| 用例 | 验证内容 |
|------|---------|
| `BuildIndex` | 从 TileSetConfig 构建索引，条目数正确 |
| `ExactMatch` | 精确 key 匹配 |
| `RotatedMatch` | 旋转后的 key 能匹配到同一 tile，rotation 值正确 |
| `HeightAdjustedMatch` | 不同基础高度的 key 匹配到同一 tile |
| `NoMatch` | 不存在的 key 返回 valid=false |
| `WeightSelection` | 多变体按 weight 分布（统计验证） |
| `SingleVariant` | 只有一个变体时总是返回它 |

#### DecorationEvalTests — 装饰条件评估

| 用例 | 验证内容 |
|------|---------|
| `AllLandCondition` | 全陆地条件 + 全陆地环境 → 匹配 |
| `WaterCondition` | 水面条件 + 水面环境 → 匹配 |
| `AnyCondition` | "any" 条件始终匹配 |
| `MismatchCondition` | 条件不满足 → 不生成装饰 |
| `RotatedCondition` | 瓦片旋转后条件正确旋转映射 |
| `TransformComposition` | slot × variant transform 合成正确 |
| `GroupVariantSelection` | 装饰组变体按 weight 选择 |
| `EmptyGroup` | 引用不存在的 group 不崩溃 |
| `MultipleSlots` | 一个 tile 的多个 slot 各自独立评估 |

### 11.5 运行方式

```bash
# 构建时启用测试
cmake -DURHO3D_TESTING=ON ...

# 运行所有 TileTerrain 测试
ctest -R TileTerrainTests

# 或直接运行可执行文件（支持 gtest 过滤）
./bin/TileTerrainTests
./bin/TileTerrainTests --gtest_filter="TerrainMap*"
./bin/TileTerrainTests --gtest_filter="ConstraintSolver.RaiseSinglePoint"
```

---

## 12. PrefabReference（引擎级 Prefab 实例化）

> 本章描述 UrhoX 引擎新增的通用 Prefab 实例化能力，非 TileTerrain 专属。
> TileSceneGenerator 依赖此能力来引用 Prefab 资源。

### 12.1 背景与动机

旧引擎的 Prefab 支持多层嵌套（EPrefab 引用 EPrefab），但 UrhoX 目前缺少等价能力。
直接展平所有 Prefab 到 Scene XML 会导致：

- 丢失引用链 — 编辑原始 Prefab 无法传播到所有引用处
- 不利于美术工作流 — 无法复用和独立编辑 Prefab 资产
- 文件冗余 — 同一模型数据在 Scene XML 中重复出现

参考 rbfx（Urho3D fork）的 `PrefabReference` 方案，设计 UrhoX 的 PrefabReference 系统。

### 12.2 架构总览

```
┌──────────────────────────────────────────────────┐
│                 引擎 Scene 系统                    │
│                                                    │
│  PrefabResource : Resource                         │
│  ├── 继承 Resource，通过 ResourceCache 加载/缓存    │
│  ├── 内部持有 XMLFile（Prefab 文件的 DOM）           │
│  └── GetRootElement() → const XMLElement&           │
│                                                    │
│  PrefabReference : Component                        │
│  ├── 挂在 Node 上，引用一个 PrefabResource          │
│  ├── SetPrefab(path) → 加载资源 + 实例化子节点树     │
│  ├── Inline() → 展开为普通节点（Unpack）             │
│  └── 实例化的子节点标记 temporary                    │
│                                                    │
│  【未来扩展 - 本次不实现】                           │
│  ├── 属性覆盖: per-attribute override (Unity 风格)  │
│  ├── NodePrefab: 类型化中间数据层 (Variant-based)   │
│  └── CommitChanges: 从实例推回修改到资源文件          │
└──────────────────────────────────────────────────┘
```

### 12.3 PrefabResource — 资源类

```cpp
namespace Urho3D
{

/// Prefab resource that holds a node tree template as XML DOM.
/// Loaded via ResourceCache, supports hot-reload.
class URHO3D_API PrefabResource : public Resource
{
    URHO3D_OBJECT(PrefabResource, Resource);

public:
    explicit PrefabResource(Context* context);

    /// Register object factory.
    static void RegisterObject(Context* context);

    /// Load resource from stream (XML format).
    bool BeginLoad(Deserializer& source) override;
    /// Finish loading (no post-processing needed).
    bool EndLoad() override;
    /// Save resource to stream.
    bool Save(Serializer& dest) const override;

    /// Get the root <node> element of the prefab.
    const XMLElement& GetRootElement() const;

    /// Get the underlying XMLFile.
    XMLFile* GetXMLFile() const { return xmlFile_; }

private:
    /// Parsed XML DOM of the prefab file.
    SharedPtr<XMLFile> xmlFile_;
};

} // namespace Urho3D
```

**Prefab 文件格式**：复用 UrhoX Scene XML 格式的子集，根元素为 `<node>`

```xml
<!-- Prefabs/Tiles/me_tiles_hope/ground_flat.xml -->
<node>
    <attribute name="Name" value="ground_flat" />
    <component type="StaticModel">
        <attribute name="Model" value="Model;Tiles/me_tiles_hope/Models/ground_flat.mdl" />
        <attribute name="Material" value="Material;Tiles/me_tiles_hope/Materials/ground.xml" />
    </component>
</node>
```

**嵌套 Prefab 文件**：子节点中可包含 PrefabReference 组件

```xml
<!-- Prefabs/Tiles/me_tiles_hope/castle_tower.xml -->
<node>
    <attribute name="Name" value="castle_tower" />
    <component type="StaticModel">
        <attribute name="Model" value="Model;Models/tower_base.mdl" />
    </component>

    <!-- 嵌套引用另一个 prefab -->
    <node>
        <attribute name="Name" value="flag" />
        <attribute name="Position" value="0 5 0" />
        <component type="PrefabReference">
            <attribute name="Prefab"
                value="PrefabResource;Prefabs/Decorations/flag_red.xml" />
        </component>
    </node>
</node>
```

### 12.4 PrefabReference — 实例化组件

```cpp
namespace Urho3D
{

/// Component that instantiates a PrefabResource as child nodes.
/// Supports nested prefabs (prefab referencing prefab).
class URHO3D_API PrefabReference : public Component
{
    URHO3D_OBJECT(PrefabReference, Component);

public:
    explicit PrefabReference(Context* context);

    /// Register object factory and attributes.
    static void RegisterObject(Context* context);

    /// Set prefab resource by resource ref. Triggers re-instantiation.
    void SetPrefabAttr(const ResourceRef& value);
    /// Get prefab resource ref (for serialization).
    ResourceRef GetPrefabAttr() const;

    /// Set prefab by resource path. Loads via ResourceCache.
    void SetPrefab(const String& resourcePath);
    /// Get current prefab resource.
    PrefabResource* GetPrefab() const { return prefab_; }

    /// Inline (Unpack): convert temporary instance nodes to persistent nodes,
    /// then remove this PrefabReference component.
    /// After Inline(), the node tree becomes independent of the prefab resource.
    void Inline();

protected:
    /// Handle node being assigned (trigger instantiation if prefab is set).
    void OnNodeSet(Node* node) override;

private:
    /// Referenced prefab resource.
    SharedPtr<PrefabResource> prefab_;

    /// Instantiate the prefab: load XML into child nodes, mark as temporary.
    void Instantiate();
    /// Remove previously instantiated temporary child nodes.
    void ClearInstance();
};

} // namespace Urho3D
```

### 12.5 实例化流程

```
SetPrefab("Prefabs/Tiles/me_tiles_hope/ground_flat.xml")
  │
  ├─ 1. ResourceCache::GetResource<PrefabResource>(path)
  │     → 加载并缓存 XMLFile
  │
  ├─ 2. ClearInstance()
  │     → 删除之前实例化的 temporary 子节点
  │
  ├─ 3. Instantiate()
  │     → node_->LoadXML(prefab_->GetRootElement())
  │     → 将加载出的子节点标记为 temporary
  │     → 子节点中的 PrefabReference 组件自动触发各自的 Instantiate()（递归嵌套）
  │
  └─ 完成：owner node 下出现 prefab 定义的完整子树
```

**嵌套实例化时序**（Prefab A 引用 Prefab B）：

```
Scene 加载
  → Node "tower" 加载
    → PrefabReference(castle_tower.xml).Instantiate()
      → 创建 StaticModel(tower_base) + 子节点 "flag"
        → 子节点 "flag" 上有 PrefabReference(flag_red.xml)
          → PrefabReference(flag_red.xml).Instantiate()  ← 递归
            → 创建 flag 的 StaticModel + 子节点...
```

### 12.6 Inline（Unpack）操作

```
调用前:
  Node "tower"
    ├─ [Component] PrefabReference → castle_tower.xml
    ├─ [temporary] StaticModel(tower_base)
    └─ [temporary] Node "flag"
        ├─ [Component] PrefabReference → flag_red.xml
        └─ [temporary] StaticModel(flag_mesh)

PrefabReference("tower").Inline() 后:
  Node "tower"
    ├─ StaticModel(tower_base)        ← temporary → persistent
    └─ Node "flag"                    ← temporary → persistent
        ├─ [Component] PrefabReference → flag_red.xml  ← 嵌套 PrefabReference 保留
        └─ [temporary] StaticModel(flag_mesh)

PrefabReference("flag").Inline() 后:     ← 逐层展开
  Node "tower"
    ├─ StaticModel(tower_base)
    └─ Node "flag"
        └─ StaticModel(flag_mesh)      ← 完全展平，无 PrefabReference
```

**Inline 是逐层的**（同 Unity 的 Unpack Prefab），不会递归展开嵌套。
如需完全展平，循环调用直到没有 PrefabReference 为止。

### 12.7 场景序列化

**保存场景时**：PrefabReference 只序列化 prefab 路径，不保存 temporary 子节点

```xml
<!-- 保存的 Scene XML — 紧凑 -->
<node>
    <attribute name="Name" value="tower" />
    <attribute name="Position" value="10 0 5" />
    <component type="PrefabReference">
        <attribute name="Prefab" value="PrefabResource;Prefabs/castle_tower.xml" />
    </component>
    <!-- temporary 子节点不写入 XML -->
</node>
```

**加载场景时**：PrefabReference 组件初始化自动触发 Instantiate()

```
Scene::LoadXML()
  → 创建 Node "tower"
  → 创建 PrefabReference 组件，反序列化 Prefab 属性
  → OnNodeSet() / SetPrefabAttr() 触发 Instantiate()
  → temporary 子树在运行时重建
```

### 12.8 temporary 节点标记

实例化产生的子节点需要与手动添加的节点区分：

- **temporary 节点**：由 PrefabReference 实例化创建，场景保存时跳过
- **persistent 节点**：用户手动添加或 Inline 后的节点，场景保存时写入

Urho3D 的 `Node` 已有 `SetTemporary(bool)` / `IsTemporary()` 方法，直接复用。

```cpp
// Instantiate 时
void PrefabReference::Instantiate()
{
    // ... LoadXML 创建子节点 ...

    // 标记所有新创建的直接子节点为 temporary
    for (unsigned i = startIndex; i < node_->GetNumChildren(); ++i)
        node_->GetChild(i)->SetTemporary(true);
}
```

### 12.9 扩展预留

本次不实现，但架构上预留以下扩展点：

**属性覆盖（Unity-style per-attribute override）**：

```cpp
// 未来在 PrefabReference 中添加
// Vector<AttributeOverride> overrides_;
//
// struct AttributeOverride
// {
//     String nodePath;         // 目标节点路径: "." / "Child" / "Child/GrandChild"
//     String componentType;    // 组件类型: "StaticModel", "Light", 或空(=节点属性)
//     int componentIndex;      // 同类型多组件时的索引
//     String attributeName;    // 属性名: "Position", "Model", etc.
//     Variant value;           // 覆盖值
// };
//
// Instantiate 流程变为:
// 1. LoadXML → 创建完整子树
// 2. 遍历 overrides_ → 逐个定位并覆盖属性值
// 3. 场景保存时序列化 overrides_
```

**NodePrefab 类型化中间层**（用于 diff 生成）：

```cpp
// 未来引入，替代直接使用 XMLFile
// struct NodePrefab
// {
//     Vector<AttributeEntry> attributes;       // Variant-based
//     Vector<ComponentPrefab> components;
//     Vector<NodePrefab> children;              // 递归
// };
//
// PrefabResource 内部从 XMLFile → NodePrefab（解析时需 Context 属性注册表）
// 对比 NodePrefab vs live Node → 自动生成 overrides
```

### 12.10 代码位置

```
engine/Source/Urho3D/Scene/
├── PrefabResource.h       # Prefab 资源类
├── PrefabResource.cpp
├── PrefabReference.h        # Prefab 实例化组件
└── PrefabReference.cpp
```

注册位置：`Scene` 子系统初始化时注册 `PrefabResource` 和 `PrefabReference`

---

## 附录

### A. 坐标系对照

| 属性 | 旧引擎 | UrhoX |
|------|--------|-------|
| 上方向 | Z-up | Y-up |
| 单位 | cm | m |
| 手性 | 左手 | 左手 |
| 转换公式 | `(x,y,z)` | `(y,z,x) × 0.01` |

### B. 旧格式 → 新格式字段映射

| 旧字段 | 新字段 | 说明 |
|--------|--------|------|
| `TileKey::h_[4]` | `key.heights[4]` | 语义不变 |
| `TileKey::mark_[4]` | `key.edgeMarks[4]` | 重命名，避免与 PointMark 混淆 |
| `TileKey::destruction_[4]` | `key.destruction[4]` | 语义不变 |
| `TileGrid (TG_Land/TG_Water)` | `PointMark (PM_LAND/PM_WATER)` | 重命名 |
| `ProxyData::condition` | `DecoSlotDef::condition` | 结构化为 BL/BR/TR/TL |
| `ProxyData::prefabGroup_` | `DecoSlotDef::group` | 引用方式不变 |
| `TileSet::tileMap_` | `TileSetMatcher::index_` | 数据结构重设计 |
| `EPrefab (嵌套)` | `TilePrefabRef.prefab (Prefab 引用)` | 通过 PrefabReference 保留引用链 |

### C. 文件清单

| 文件 | 职责 |
|------|------|
| `Lib/Data/TerrainTypes.h` | 枚举和常量 |
| `Lib/Data/TerrainPoint.h` | 顶点结构 |
| `Lib/Data/TerrainEdge.h` | 边结构 |
| `Lib/Data/TerrainGrid.h` | 格子结构 |
| `Lib/Data/TerrainMap.h/cpp` | 地形网格 + 裸读写操作 |
| `Lib/Data/TerrainSerializer.h/cpp` | JSON 序列化 |
| `Lib/Operator/TerrainOperator.h/cpp` | 带约束的地形修改操作 |
| `Lib/Operator/ConstraintSolver.h/cpp` | SPFA 约束求解器 |
| `Lib/TileSet/TileSetConfig.h/cpp` | TileSet 配置数据 |
| `Lib/TileSet/TileKey.h/cpp` | 匹配键 + 归一化 |
| `Lib/TileSet/TileSetMatcher.h/cpp` | 匹配引擎 |
| `Lib/Generator/TileSceneGenerator.h/cpp` | 场景组装 |
| `Lib/Generator/DecorationEvaluator.h/cpp` | 装饰评估 |
| `CLI/TileTerrainCLI.cpp` | 命令行入口 |
| `Tests/TileTerrain/*.cpp` | Google Test 单元测试（位于 `engine/Tests/TileTerrain/`） |
| `Source/Urho3D/Scene/PrefabResource.h/cpp` | Prefab 资源（持有 XMLFile，引擎级） |
| `Source/Urho3D/Scene/PrefabReference.h/cpp` | Prefab 实例化组件（引擎级） |

---

*创建日期: 2026-02-28*
*基于旧引擎 TileEditorModule 的核心地形算法迁移设计*
