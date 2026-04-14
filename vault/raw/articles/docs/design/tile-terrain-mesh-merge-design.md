---
summary: "Tile terrain runtime mesh merging + WorldPartition streaming + HLOD to reduce draw calls to ~100 for 4km x 4km maps"
related_paths:
  - engine/Source/Urho3D/TileTerrain/**
  - engine/Source/Urho3D/Graphics/HLOD/**
last_updated: "2026-04-02"
---

# Tile Terrain 地形网格合并与 WorldPartition 集成方案

## Context

当前 TileSceneGenerator 为每个 2.56m 格子生成独立的 Tile 节点（PrefabReference → StaticModel），每个 tile = 1 draw call。对于 4km×4km 地图（~244 万格子），即使 200m 可视范围内也有数千个 draw call，移动端 CPU 瓶颈严重。

**目标**：通过地形网格运行时合并 + WorldPartition 流式加载 + HLOD 多级代理，将地形 draw call 控制在 ~100 以内，支持 4km×4km 超大地图。

---

## 一、整体架构

```
离线构建阶段（TileSceneGenerator / TileTerrainCLI）
├─ 地形 tile 匹配 → 确定每格子的 MDL 路径 + 变换
├─ 装饰物 HISM 分组 → 按 (model, material) 聚合 transforms
├─ WorldPartition cell 划分 → 输出 cell 场景数据 + 资源清单
└─ L1 HLOD proxy 生成 → MeshMerger + MeshSimplifier（离线简化）

运行时阶段
├─ WorldPartition 距离驱动加载/卸载 cell
├─ TileTerrain + TileTerrainChunk 运行时合并 sub-chunk 内 tile mesh
├─ IB-based LOD 切换（LOD0/LOD1 + 边界 stitching）
└─ HISM 装饰物层级剔除渲染
```

---

## 二、地形网格合并

### 2.1 层级结构

```
WorldPartition Cell (256m)        ← 流式加载单元
  └─ Sub-chunk (16×16 tile ≈ 41m) ← 渲染单元（合并后的单个 mesh）
       └─ Tile (2.56m)            ← 源数据，不直接渲染
```

- Cell 大小：256m（可配置），16×16 = 256 L0 cell 覆盖 4km
- Sub-chunk 大小：16×16 tile = 40.96m（可配置，默认 16）
- 每 cell 约 6×6 = 36 个 sub-chunk

### 2.2 运行时合并流程

**选择运行时合并（而非离线）的原因**：零包体增加——tile MDL 是共享资源，离线合并会把共享数据展开到每个 chunk，导致包体膨胀。

**合并流程**：

1. WorldPartition 检测 cell 进入 loadingRange → 开始异步加载资源
2. Cell 所有资源加载完成 → LOADED 状态
3. TileTerrainChunk 合并初始化：
   a. 从 ResourceCache 获取已加载的 tile Model 资源（共享，无额外加载）
   b. 遍历 sub-chunk 内所有 tile entry，提取 VB 数据
   c. 将顶点变换到 sub-chunk 局部坐标系
   d. 拼接所有 tile 的 VB（顶点追加）
   e. 预生成 17 个 IB 变体（LOD0×16 stitching + LOD1×1），详见 §2.5
   f. 创建运行时 VertexBuffer + IndexBuffer → Geometry → 可渲染
4. Cell ACTIVATED → 合并后的 sub-chunk 可见

**后台线程**：步骤 b-e（读取顶点 + 变换 + 拼接 + 生成 IB）在后台线程执行，只有步骤 f（创建 GPU 资源）在主线程。每个 sub-chunk ~6,400 顶点，合并耗时 ~2-5ms。

### 2.3 Tile Mesh 实际拓扑分析

通过 `TileTerrainCLI analyze-mesh` 对所有 7 套 basemesh tileset 的 MDL 文件进行边缘顶点分析，发现 tile mesh 分为三类：

#### 2.3.1 三类 Tile Mesh

| 类型 | 示例 | 顶点 | 三角形 | BBox (XZ) | 边缘顶点 |
|------|------|------|--------|-----------|---------|
| **平面 tile** | `tile_g_0_0_0_0` | 25 | 32 | **2.560 × 2.560**（满格） | 每边 5 个等距 |
| **斜坡地面（角落）** | `tile_g_0_1_0_0` | 12 | 13 | **0.880 × 0.880**（局部） | 不规则 |
| **斜坡地面（边缘）** | `tile_g_1_1_0_0_a` | 15 | 16 | **2.560 × 0.880**（半格） | 部分边 5 顶点 |
| **3D 斜坡墙面** | `tile_0_0_128_128` | 56 | 84 | **2.560 × 1.955** + Y 高度 | 完全不规则 |

**关键发现**：

1. **只有平面 tile（heights=[0,0,0,0]）是完整的 2.56m 5×5 规则网格**。所有 tileset 中只有 `tile_g_0_0_0_0`（地面）和 `tile_w_0_0_0_0`（水面）满足此条件。

2. **斜坡 tile_g 不是完整 tile**——它们只覆盖格子的一部分（角落约 0.88m 或半边），Y 高度为 0（平面）。一个斜坡格子的渲染由**局部地面 mesh + 独立的 3D 斜坡墙面 mesh** 组合而成。

3. **3D 斜坡墙面**（如 `tile_0_0_128_128`）有 Y 高度，顶点分布完全不规则，边缘顶点数从 1 到 8 不等。

4. **跨 tileset 一致**：所有 7 套 basemesh（hope, chinoiserie, DS, dg, snow, temple, ts）均遵循此模式。

分析数据摘要（使用 `TileTerrainCLI analyze-mesh` 工具获取）：

```
me_basemesh_hope:         Total: 169  Regular(5x5): 5   Irregular: 164
me_basemesh_chinoiserie:  Total: 96   Regular(5x5): 5   Irregular: 91
me_basemesh_DS:           Total: 82   Regular(5x5): 5   Irregular: 77
me_basemesh_ts:           Total: 87   Regular(5x5): 2   Irregular: 85
me_basemesh_temple:       Total: 51   Regular(5x5): 2   Irregular: 49
me_basemesh_dg:           Total: 58   Regular(5x5): 2   Irregular: 56
me_basemesh_snow:         Total: 14   Regular(5x5): 2   Irregular: 12
```

#### 2.3.2 LOD 策略：分类处理

基于实际 mesh 拓扑，采用**分类 LOD 策略**：

| Tile 类型 | 合并方式 | LOD 策略 | 原因 |
|-----------|---------|---------|------|
| 平面 tile（25V, 5×5 grid） | VB 拼接 + IB 模板 | **IB-based LOD0/LOD1** | 规则网格，IB 模板完美适用 |
| 斜坡 tile_g（局部 mesh） | VB+IB 直接拼接 | **始终 LOD0** | 不规则、局部覆盖，无法模板化 |
| 3D 斜坡墙面 | VB+IB 直接拼接 | **始终 LOD0** | 完全不规则拓扑 |

**性能影响极小**：在典型大地图中，平面格子占绝对多数。例如 100×100 的台地，只有边缘 ~400 格子有斜坡，内部 10000 格子全是可 LOD 的平面 tile。对于 4km×4km 地图，斜坡格子占比通常 <5%。

### 2.4 IB-based LOD（仅平面 Tile）

**适用对象**：heights=[0,0,0,0] 的平面 tile（`tile_g_0_0_0_0` / `tile_w_0_0_0_0`），25 顶点，每边 5 个等距顶点。

**LOD 级别**：

| 级别 | 每边顶点 | 网格 | 每 tile 顶点 | 每 tile 三角形 |
|------|---------|------|------------|--------------|
| LOD0 | 5 | 4×4 | 25 | 32 |
| LOD1 | 3 | 2×2 | 25（VB 不变） | 8 |

**核心思路**：VB 始终包含 LOD0 的全部 25 个顶点（不变），通过不同的 IB 实现 LOD 切换。

LOD1 的 3 个边界顶点是 LOD0 的 5 个边界顶点的子集（位置 0、2、4）：

```
LOD0: ●─●─●─●─●  (5 个边界顶点)
LOD1: ●───●───●    (3 个，是 LOD0 的子集)
```

**边界 Stitching**：相邻 sub-chunk LOD 不同时，高 LOD 侧的边缘 tile 使用过渡 IB，将 5 个边界顶点用扇形三角形连接到邻居的 3 个顶点，消除 T-junction：

```
Sub-chunk A (LOD0)      Sub-chunk B (LOD1)
●─●─●─●─●              ●───●───●
内部: 4×4 IB    过渡边: 扇形 IB     内部: 2×2 IB
```

**注意**：stitching 仅应用于 sub-chunk 边界处的**平面 tile**。如果边界处恰好是斜坡 tile，该 tile 始终保持 LOD0，无需 stitching。

**预计算索引模板**：

由于平面 tile mesh 是规则 5×5 网格，可预计算所有 IB 模板：

- `LOD0_Interior`：完整 4×4 网格，32 三角形
- `LOD1_Interior`：稀疏 2×2 网格，8 三角形
- `LOD0_Transition_{Edge}`：4 条边各一个过渡模板（LOD0 侧面向 LOD1 邻居）
- 组合数：每 tile 4 条边 × 是否过渡 = 有限的几种模板

### 2.5 预生成 IB 变体 + DrawRange 切换（参考 Terrain/TerrainPatch）

参考引擎现有 `Terrain.h` / `TerrainPatch.h` 的 LOD stitching 实现，采用**预生成所有 IB 变体 + 运行时 DrawRange 切换**的方案，实现零运行时 IB 重建开销。

#### 2.5.1 设计原理

引擎 Terrain 系统的核心思路：

1. **初始化时预生成所有 IB 变体**：每个 LOD 级别 × 4 条边的 stitching 组合（NSWE 4 bit = 16 种），所有变体打包到同一个 IndexBuffer
2. **drawRanges 索引**：`drawRanges_[index] = {start, count}` 记录每个变体在 IB 中的位置
3. **每帧零开销切换**：根据当前 LOD + 邻居 LOD 计算 `drawRangeIndex`，调用 `SetDrawRange()` 即可
4. **LOD 约束**：相邻 patch LOD 差 ≤ 1（`GetCorrectedLodLevel()`），确保 stitching 只需处理差 1 的情况

#### 2.5.2 映射到 Tile Terrain Sub-chunk

**IB 变体数**：

```
LOD0: 16 种 stitching 组合（N/S/W/E 各边是否需要 stitch）
LOD1: 1 种（最粗级别，无需 stitch）
总计: 17 个 IB 变体
```

**Streaming 加载时一次性生成**：

```
TileTerrainChunk 初始化（cell LOADED 时）:

1. 合并 VB（静态，永不变化）
   ├─ 平面 tile 顶点（25V × N_flat）
   └─ 斜坡 tile 顶点（各自顶点数 × N_slope）

2. 生成 17 个 IB 变体，连续存储在单个 IndexBuffer 中
   ├─ [0..15]  LOD0 × 16 种 stitching 组合
   │   ├─ 内部平面 tile: LOD0 模板索引
   │   ├─ 边界平面 tile: 根据 stitchFlags 选 LOD0 或过渡模板
   │   └─ 所有斜坡 tile: 原始索引（17 个变体中完全相同）
   └─ [16]     LOD1（最粗，无 stitch）
       ├─ 平面 tile: LOD1 模板索引
       └─ 斜坡 tile: 原始索引（同上）

3. 记录 drawRanges_[17] = {start, count}
```

**每帧 LOD 选择**（参考 `Terrain::UpdatePatchLod()`）：

```cpp
void TileTerrainChunk::UpdateLod()
{
    unsigned lodLevel = GetCorrectedLodLevel(distanceLodLevel_);
    unsigned drawRangeIndex = lodLevel << 4u;

    if (lodLevel < NUM_LOD_LEVELS - 1)
    {
        // 检查 4 个邻居 sub-chunk 的 LOD
        if (north_ && north_->GetLodLevel() > lodLevel)
            drawRangeIndex |= STITCH_NORTH;
        if (south_ && south_->GetLodLevel() > lodLevel)
            drawRangeIndex |= STITCH_SOUTH;
        if (west_ && west_->GetLodLevel() > lodLevel)
            drawRangeIndex |= STITCH_WEST;
        if (east_ && east_->GetLodLevel() > lodLevel)
            drawRangeIndex |= STITCH_EAST;
    }

    geometry_->SetDrawRange(TRIANGLE_LIST,
                            drawRanges_[drawRangeIndex].first_,
                            drawRanges_[drawRangeIndex].second_);
}
```

**LOD 约束**（参考 `TerrainPatch::GetCorrectedLodLevel()`）：

```cpp
unsigned TileTerrainChunk::GetCorrectedLodLevel(unsigned lodLevel)
{
    // 相邻 sub-chunk LOD 差 ≤ 1
    if (north_) lodLevel = Min(lodLevel, north_->GetLodLevel() + 1);
    if (south_) lodLevel = Min(lodLevel, south_->GetLodLevel() + 1);
    if (west_)  lodLevel = Min(lodLevel, west_->GetLodLevel() + 1);
    if (east_)  lodLevel = Min(lodLevel, east_->GetLodLevel() + 1);
    return lodLevel;
}
```

#### 2.5.3 IB 变体生成算法

对每个变体 `(lodLevel, stitchFlags)` 生成索引序列：

```
for each tile in sub-chunk:
    if tile.isFlat:
        if tile 是内部 tile（非边界）:
            追加 LOD{lodLevel}_Interior 模板索引 + tile.baseVertex
        else:
            // 边界 tile，检查该边是否需要 stitch
            追加对应模板索引（Interior / Transition_{Edge}）+ tile.baseVertex
    else:
        // 斜坡 tile，所有变体中索引相同
        追加 tile.originalIndices（已含 baseVertex 偏移）
```

由于斜坡 tile 数量少（<5%），它们在 17 个变体中被重复存储的内存开销可忽略。

#### 2.5.4 内存估算

以 16×16 sub-chunk 为例：
- 平面 tile LOD0：256 × 32 三角形 × 3 索引 = 24,576 indices
- 平面 tile LOD1：256 × 8 三角形 × 3 索引 = 6,144 indices
- 斜坡 tile（假设 5%）：~13 tile × ~50 indices = ~650 indices
- 单个 IB 变体：~25,000 indices × 2 bytes = ~50 KB
- 17 个变体总计：~850 KB

对比单个 L0 cell（36 sub-chunk）：~30 MB IB 数据。可优化：实际多数变体差异仅在边界 tile，可通过共享内部索引段减少内存。

#### 2.5.5 优势总结

| 方面 | 说明 |
|------|------|
| **运行时开销** | 零 IB 重建，每帧只做 DrawRange 指针切换 |
| **一致性** | 与引擎 Terrain 系统设计模式完全一致 |
| **正确性** | LOD 约束 + 预计算 stitching，保证无缝 |
| **生成时机** | Streaming 加载完成时（后台线程），不影响帧率 |

### 2.6 LOD 选择策略

- 每个 sub-chunk 根据到 camera 的距离选择基础 LOD 级别
- `GetCorrectedLodLevel()` 约束相邻 sub-chunk LOD 差 ≤ 1
- 相邻 sub-chunk LOD 不同 → 通过预生成的 stitching IB 变体自动处理
- 距离阈值可配置（如 <200m: LOD0, >=200m: LOD1）
- 斜坡 tile 不参与 LOD 简化，但其索引自然包含在所有 IB 变体中

### 2.7 组件架构：TileTerrain + TileTerrainChunk

参考引擎现有 `Terrain`（Component）+ `TerrainPatch`（Drawable）的设计模式，地形合并系统由两个类组成：

#### 2.7.1 类关系

```
TileTerrain (Component)                    ← 管理者，挂在世界/cell 根节点
  │
  ├─ 拥有所有 TileTerrainChunk 的引用
  ├─ 管理跨 sub-chunk 邻居关系（包括跨 cell 边界）
  ├─ 驱动每帧 LOD 更新
  └─ 响应 WorldPartition cell 状态回调
  │
  └─ TileTerrainChunk (Drawable)           ← 渲染单元，每 sub-chunk 一个
       ├─ 继承自 Drawable → 自带 Octree 剔除、距离排序
       ├─ 拥有合并后的 VB + 共享 IB（17 个 DrawRange 变体）
       ├─ UpdateBatches() → 提交 SourceBatch 给渲染管线
       └─ 邻居指针（north_/south_/west_/east_）
```

#### 2.7.2 TileTerrain（Component）

**职责**：全局协调者，不直接参与渲染。

```cpp
class TileTerrain : public Component
{
    URHO3D_OBJECT(TileTerrain, Component);

public:
    // --- 属性 ---
    /// 共享 terrain 材质（ID+Weight shader）
    SharedPtr<Material> material_;
    /// 所有活跃的 TileTerrainChunk，按 (cellCoord, subChunkCoord) 索引
    HashMap<IntVector2, WeakPtr<TileTerrainChunk>> chunks_;

    // --- WorldPartition 回调 ---
    /// Cell LOADED → 创建该 cell 内的所有 TileTerrainChunk 节点
    void OnCellLoaded(WorldPartitionCell* cell);
    /// Cell UNLOADED → 销毁该 cell 内的所有 TileTerrainChunk 节点
    void OnCellUnloaded(WorldPartitionCell* cell);

    // --- 邻居管理 ---
    /// 注册新 chunk 并建立与现有 chunk 的邻居关系
    void RegisterChunk(TileTerrainChunk* chunk);
    /// 注销 chunk 并清理邻居指针
    void UnregisterChunk(TileTerrainChunk* chunk);

    // --- 每帧更新 ---
    /// 遍历所有 chunk，计算距离 LOD + 约束 + 更新 DrawRange
    void UpdateLod(Camera* camera);
};
```

**关键设计**：

- **邻居管理**：chunk 注册时，通过坐标查找四方向邻居并双向建立指针。chunk 注销时清理。**跨 cell 边界**的邻居同样通过全局坐标索引自然关联。
- **LOD 更新驱动**：每帧由 TileTerrain 统一遍历所有 chunk，而非每个 chunk 独立更新。这确保 LOD 约束的一致性（Terrain 也是如此：`Terrain::Update()` → `UpdatePatchLod()` 遍历全部 patch）。
- **材质共享**：所有 TileTerrainChunk 使用同一个 Material 实例（ID+Weight shader），由 TileTerrain 持有和管理。

#### 2.7.3 TileTerrainChunk（Drawable）

**职责**：单个 sub-chunk 的渲染单元，类比 `TerrainPatch`。

```cpp
class TileTerrainChunk : public Drawable
{
    URHO3D_OBJECT(TileTerrainChunk, Drawable);

public:
    // --- 数据 ---
    /// Sub-chunk 全局坐标（用于邻居查找和索引）
    IntVector2 coord_;
    /// 合并后的 VertexBuffer（静态，永不变化）
    SharedPtr<VertexBuffer> vertexBuffer_;
    /// 合并后的 IndexBuffer（包含 17 个 IB 变体）
    SharedPtr<IndexBuffer> indexBuffer_;
    /// 17 个 DrawRange 的 (start, count) 对
    Pair<unsigned, unsigned> drawRanges_[17];
    /// 当前使用的 Geometry
    SharedPtr<Geometry> geometry_;

    /// 邻居指针（由 TileTerrain 管理）
    WeakPtr<TileTerrainChunk> north_;
    WeakPtr<TileTerrainChunk> south_;
    WeakPtr<TileTerrainChunk> west_;
    WeakPtr<TileTerrainChunk> east_;

    /// 当前基于距离的 LOD 级别
    unsigned distanceLodLevel_ = 0;
    /// 经过邻居约束后的实际 LOD 级别
    unsigned lodLevel_ = 0;

    // --- 初始化（Streaming 阶段） ---
    /// 从 tile entry 列表合并 VB + 生成 IB 变体
    /// 可在后台线程执行（CPU 数据准备），完成后主线程创建 GPU 资源
    void BuildMesh(const Vector<TileEntry>& entries);

    // --- Drawable 接口 ---
    void UpdateBatches(const FrameInfo& frame) override;
    void UpdateGeometry(const FrameInfo& frame) override;

    // --- LOD ---
    unsigned GetLodLevel() const { return lodLevel_; }
    unsigned GetCorrectedLodLevel(unsigned lodLevel);
    /// 由 TileTerrain::UpdateLod() 调用
    void SetDistanceLodLevel(unsigned level);
    /// 根据 lodLevel_ + 邻居 LOD 计算 drawRangeIndex，调用 SetDrawRange()
    void UpdateDrawRange();
};
```

**关键设计**：

- **继承 Drawable**：自动获得 Octree 插入/移除、视锥剔除、UpdateBatches 渲染提交。无需手动管理可见性——引擎的 Octree 和 View 系统自动处理。
- **BuildMesh 后台线程化**：CPU 侧数据准备（VB 拼接 + IB 变体生成）可在 WorkQueue 后台线程执行。完成后在主线程调用 `vertexBuffer_->SetData()` / `indexBuffer_->SetData()` 上传 GPU。
- **UpdateBatches**：每帧由引擎 View 调用，设置 `batches_[0]` 的 geometry、material、worldTransform。几乎零开销——Geometry 对象已创建好，只需 `SetDrawRange()` 切换 LOD。

#### 2.7.4 生命周期与 WorldPartition 集成

```
WorldPartition Cell 状态变化
│
├─ LOADING → LOADED
│  TileTerrain::OnCellLoaded():
│  1. 读取 terrain_entries.json
│  2. 为每个 sub-chunk 创建子节点 + TileTerrainChunk 组件
│  3. TileTerrainChunk::BuildMesh()（后台线程）
│  4. BuildMesh 完成 → TileTerrain::RegisterChunk()（建立邻居关系）
│  5. Cell 切换到 ACTIVATED
│
├─ ACTIVATED（运行中）
│  每帧 TileTerrain::UpdateLod():
│  1. 遍历所有 chunk，按距离计算 distanceLodLevel_
│  2. GetCorrectedLodLevel() 约束邻居差 ≤ 1
│  3. lodLevel_ 变化 → chunk.UpdateDrawRange()
│
└─ ACTIVATED → UNLOADED
   TileTerrain::OnCellUnloaded():
   1. 对每个 chunk: TileTerrain::UnregisterChunk()（清理邻居指针）
   2. 销毁 chunk 节点（GPU 资源自动释放）
```

#### 2.7.5 跨 Cell 邻居关系

```
Cell A (ACTIVATED)          Cell B (ACTIVATED)
┌─────────────────┐         ┌─────────────────┐
│  chunk(5,0) ←────邻居────→ chunk(0,0)       │
│  chunk(5,1) ←────邻居────→ chunk(0,1)       │
│  ...            │         │  ...            │
└─────────────────┘         └─────────────────┘
```

当 Cell B 加载时，其边界 chunk 注册到 TileTerrain 的全局 HashMap，自动发现 Cell A 中已注册的邻居 chunk 并建立双向指针。当 Cell A 卸载时，边界 chunk 注销，Cell B 中对应的邻居指针被清空（WeakPtr 自动失效或显式清理）。

**边界 LOD 过渡**：Cell 边界处 chunk 的 LOD 约束与 cell 内部完全一致——`GetCorrectedLodLevel()` 不区分邻居来自同一 cell 还是不同 cell。

---

## 三、地形材质：ID+Weight 方案

参考三角洲行动（Delta Force）GDC 分享的 ID+Weight 地形材质方案。

### 3.1 核心架构：几何与材质分离

地形的**几何形状**和**纹理外观**由两套独立数据决定：

| 层 | 数据来源 | 决定什么 |
|----|---------|---------|
| **Tileset** | 瓦片匹配算法 | 网格形状（平面/斜坡/墙面） |
| **权重图（WeightMap）** | 纹理笔刷绘制 | 每顶点的纹理 layer ID + 混合权重 |

所有 tileset 共用**同一个** ID+Weight 地形材质（同一 Material 实例、同一 Shader），不同地表外观的差异完全编码在顶点数据中。

### 3.2 地形纹理权重图（TerrainWeightMap）

权重图是一张 2D 网格，分辨率与地形顶点网格对齐（每个平面 tile 是 4×4 grid，相邻 tile 共享边界，所以网格间距 = tileSize / 4 = 0.64m）。

**数据结构**：

```cpp
struct TerrainWeightMap
{
    unsigned width_;                    // 网格宽度（= terrain tile 列数 × 4 + 1）
    unsigned height_;                   // 网格高度（= terrain tile 行数 × 4 + 1）
    float gridSpacing_;                 // 采样间距（= tileSize / 4 = 0.64m）
    Vector2 origin_;                    // 左下角世界坐标

    PODVector<unsigned char> bottomID_; // 每采样点的底层 layer ID (0~31)
    PODVector<unsigned char> topID_;    // 每采样点的上层 layer ID (0~31)
    PODVector<float> weight_;           // 每采样点的混合权重 (0~1)
};
```

**初始状态**：默认 layer ID = 0（基础地面纹理），weight = 0。

### 3.3 纹理笔刷（TerrainOperator）

纹理笔刷是 `TileTerrainLib` 中 `TerrainOperator` 的一个方法，用于在权重图上绘制纹理：

```cpp
/// 在世界坐标 (x, z) 位置、radius 圆内刷上 layerID，混合强度 strength。
/// 受影响的采样点：将 topID 设为 layerID，weight 按距离衰减混合 strength。
/// 内部执行 ≤3 约束检查：绘制后扫描影响区域的三角形，
/// 如果某三角形超过 3 种 unique layer ID 则回退该采样点。
void PaintTexture(TerrainWeightMap& map,
                  float x, float z, float radius,
                  unsigned char layerID, float strength);
```

**笔刷逻辑**：

```
for each sample point (sx, sz) in weightMap within radius of (x, z):
    dist = distance((sx, sz), (x, z))
    if dist > radius: skip
    falloff = 1.0 - (dist / radius)  // 线性衰减，可换平滑曲线
    newWeight = lerp(current.weight, strength, falloff)

    // 更新采样点
    if current.bottomID == current.topID:
        // 当前为纯色，将新 layer 设为 topID
        current.topID = layerID
        current.weight = newWeight
    else if current.topID == layerID:
        // 已在混合同一 layer，增强权重
        current.weight = max(current.weight, newWeight)
    else:
        // 已在混合不同 layer，替换 top layer
        // 先将当前混合结果"烘入" bottomID
        if current.weight > 0.5:
            current.bottomID = current.topID
        current.topID = layerID
        current.weight = newWeight

// ≤3 约束验证 pass
for each triangle touching affected samples:
    collect unique IDs from 3 vertices' (bottomID, topID)
    if uniqueCount > 3:
        revert the most recent change on the offending vertex
```

**CLI 命令**：

```bash
TileTerrainCLI.exe paint-texture \
  --weightmap terrain_weights.bin \
  --pos 100.0,200.0 \
  --radius 5.0 \
  --layer 3 \
  --strength 0.8 \
  --output terrain_weights.bin
```

### 3.4 合并时的材质赋值

网格合并时，每个顶点从权重图中读取最近的采样点的 (bottomID, topID, weight)：

```
合并 sub-chunk 时:
  for each vertex in merged VB:
      worldPos = subChunkTransform * vertex.position
      // 在权重图中找最近采样点
      gx = round((worldPos.x - origin.x) / gridSpacing)
      gz = round((worldPos.z - origin.z) / gridSpacing)
      clamp(gx, 0, width-1)
      clamp(gz, 0, height-1)
      idx = gz * width + gx
      vertex.bottomLayerID = weightMap.bottomID[idx]
      vertex.topLayerID = weightMap.topID[idx]
      vertex.weight = weightMap.weight[idx]
```

**关键**：材质赋值与 tile 边界无关。焊接后的边界顶点和内部顶点一视同仁，都从权重图采样。

### 3.5 顶点数据存储

每个顶点存储 3 个材质相关值：

| 数据 | 说明 | 存储位置 |
|------|------|---------|
| Bottom Layer ID | 底层材质 ID (0~31) | Vertex Color R 或 UV2.x |
| Top Layer ID | 上层材质 ID (0~31) | Vertex Color G 或 UV2.y |
| Weight | Top layer 混合权重 (0~1) | Vertex Color B 或 UV2.z |

### 3.6 Shader 混合

- 每三角形最多 3 种材质（笔刷工具保证 ≤3 约束）
- Shader 从 3 个顶点的 6 个 ID 中提取 min/mid/max 三个核心 ID
- 只做 3 次纹理采样，恒定 shader 开销
- 使用高度混合（height-based blending）实现自然过渡

### 3.7 纹理管理

- **Texture2DArray**：全项目支持 32 种地表材质
- **动态加载**：运行时只加载当前可视区域用到的 ~8 种纹理
- 空闲 slot 按需填充/卸载

### 3.8 对网格合并的影响

**完全兼容**：
- 所有 tileset 使用**同一个 ID+Weight terrain shader**（同一 Material 实例）
- 不同地表外观完全编码在**顶点数据**中（来自权重图）
- 合并时顶点焊接 + 从权重图采样 → 材质信息自然注入
- **1 个 sub-chunk = 1 draw call**

### 3.9 顶点焊接

合并 sub-chunk 时，相邻 tile 的边界顶点必须焊接以保证法线连续：

```
焊接流程:
  1. 遍历所有顶点对，如果 distance(posA, posB) < epsilon (0.001m)
     → 视为同一顶点，合并为一个
  2. 更新所有引用这两个顶点的索引
  3. 焊接后重新计算受影响顶点的法线（面积加权平均）
  4. 从权重图采样材质 ID（焊接前后位置不变，采样结果一致）
```

**4-corner 极端情况**：如果焊接点处的三角形超过 3 种 unique layer ID（仅在 4 种不同纹理交汇处可能发生，极罕见），将该顶点拆回独立顶点。单点法线不连续的视觉影响可忽略。

### 3.10 远距离优化（可选）

- 近处：ID+Weight 实时混合（高精度）
- 远处：烘焙到 Virtual Texture 缓存（省带宽）
- 低端设备：回退到单层 splatmap

---

## 四、装饰物 HISM 离线分组

### 4.1 原理

将相同 (model, material) 的装饰物聚合为一个 HISMComponent，GPU instancing 渲染。

### 4.2 离线处理流程（TileSceneGenerator）

1. 对每个 cell 内的装饰物，解析 prefab XML 获取实际 Model/Material 路径
2. 按 (modelPath, materialPath) 分组
3. 每组输出一个 HISMComponent 节点：
   - Model + Material 属性
   - Instance transforms 列表（序列化为 Instance Data 属性）
4. 复杂装饰物（多节点/多组件）保持 PrefabReference 不变

### 4.3 运行时

- HISMComponent 加载后自动构建 BVH cluster tree
- O(log N) 层级视锥剔除
- 相同 model+material 的所有实例 = 1 draw call

---

## 五、WorldPartition 集成

### 5.1 输出格式

TileSceneGenerator 输出 WorldPartition 目录结构：

```
output_dir/
├─ world_partition.json          # Grid 配置 + Cell 列表
├─ terrain.json                  # 原始 TerrainMap 数据（保留）
└─ cells/
   ├─ L0/
   │  ├─ Cell_0_0/
   │  │  ├─ scene.xml            # TileTerrainChunk + HISM 节点
   │  │  └─ terrain_entries.json # tile entry 列表（MDL路径+变换）
   │  ├─ Cell_0_1/
   │  │  └─ ...
   │  └─ ...
   └─ L1/
      ├─ Cell_0_0/
      │  └─ scene.xml            # HLOD proxy StaticModel
      └─ ...
```

### 5.2 world_partition.json

```json
{
  "grids": [
    {
      "level": 0,
      "cellSize": 256.0,
      "loadingRange": 768.0,
      "unloadMargin": 64.0
    },
    {
      "level": 1,
      "cellSize": 256.0,
      "loadingRange": 3000.0,
      "unloadMargin": 128.0
    }
  ],
  "subChunkSize": 16,
  "tileSize": 2.56,
  "cells": [
    {
      "gridLevel": 0,
      "coord": [0, 0],
      "bounds": {"min": [0, 0, 0], "max": [256, 50, 256]},
      "sceneDataPath": "cells/L0/Cell_0_0/scene.xml",
      "terrainEntriesPath": "cells/L0/Cell_0_0/terrain_entries.json",
      "resources": [
        {"type": "Model", "name": "Environment/Legacy/Tiles/.../m.mdl"}
      ]
    }
  ]
}
```

### 5.3 Cell 场景 XML（L0）

```xml
<scene>
  <component type="Octree" />

  <!-- TileTerrain 全局管理器（挂在 cell 根节点或 world 节点上） -->
  <component type="TileTerrain">
    <attribute name="Material" value="Material;Terrain/TerrainMaterial.material" />
  </component>

  <!-- 地形 sub-chunk（Drawable，由 TileTerrain 管理） -->
  <node name="TileTerrainChunk_0_0">
    <component type="TileTerrainChunk">
      <attribute name="Sub Chunk Coord" value="0 0" />
    </component>
  </node>
  <node name="TileTerrainChunk_1_0">
    ...
  </node>

  <!-- 装饰物 HISM -->
  <node name="Deco_tree_oak">
    <component type="HISMComponent">
      <attribute name="Model" value="Model;path/to/tree.mdl" />
      <attribute name="Material" value="Material;path/to/tree.material" />
      <attribute name="Instance Data" value="... packed transforms ..." />
    </component>
  </node>
</scene>
```

### 5.4 terrain_entries.json（每 cell 的 tile 数据）

```json
{
  "subChunks": [
    {
      "coord": [0, 0],
      "tiles": [
        {
          "model": "Environment/Legacy/Tiles/.../m.mdl",
          "position": [0, 0, 0],
          "rotation": [0, -0.707, 0, 0.707]
        }
      ]
    }
  ],
  "weightMapPath": "terrain_weights.bin"
}
```

注意：材质 layer ID 和权重不存储在 tile entry 中，而是来自独立的**地形纹理权重图**（见 §3.2）。合并时从权重图按顶点世界坐标采样。

### 5.5 三态生命周期

```
UNLOADED → LOADING → LOADED → ACTIVATED
                              ↑
                    TileTerrainChunk 在此阶段执行合并
                    合并完成后 cell 才切换到 ACTIVATED
```

---

## 六、L1 HLOD 离线生成

### 6.1 目的

L0 之外（768m+）的地形用简化 proxy mesh 替代，减少远景顶点数和 draw call。

### 6.2 生成流程

1. 对每个 L1 cell 覆盖的 L0 区域：
   a. 加载所有 tile MDL，合并为完整 mesh（同运行时合并逻辑）
   b. 调用 MeshSimplifier 简化到目标比例（如 5%-10%）
   c. **锁定 cell 边界顶点**不参与简化（防止接缝）
   d. 输出简化后的 proxy MDL + 材质
2. 将 proxy 写入 L1 cell 场景 XML（StaticModel）

### 6.3 边界顶点锁定

- 计算 cell AABB 边界
- 标记 x/z 坐标在边界上的顶点为 pinned
- MeshSimplifier QEM 跳过 pinned 顶点
- 保证相邻 L1 cell 的边界完全对齐

### 6.4 L1 ↔ L0 切换

WorldPartition Phase 2 原子切换：
- 所有源 L0 cell ACTIVATED → L1 保持 LOADED（隐藏）
- 所有源 L0 cell 非 ACTIVATED → L1 ACTIVATED（显示 proxy）
- 同帧完成，无空洞无重叠

---

## 七、性能估算（4km×4km 地图）

### 7.1 基础参数

| 参数 | 值 |
|------|-----|
| 地图 | 4000m × 4000m |
| Tile | 2.56m，每 tile ~25 顶点 (LOD0) / ~9 顶点 (LOD1) |
| Sub-chunk | 16×16 tile = 40.96m |
| L0 Cell | 256m，~36 sub-chunk/cell |
| L0 Cell 总数 | 16×16 = 256 |
| L0 loadingRange | 768m，加载 ~28 cell |

### 7.2 Draw Call

| Layer | DC 估算 |
|-------|---------|
| L0 sub-chunk（视锥内） | 18 - 70 |
| L1 HLOD proxy | 20 - 50 |
| L2 HLOD proxy | 5 - 15 |
| 装饰物 HISM | 30 - 50 |
| **总计** | **73 - 185** |

移动端（200m 渲染距离）：~70-100 DC。

### 7.3 每帧提交顶点

| Layer | 顶点数 |
|-------|--------|
| L0 sub-chunk (LOD0, 近处 ~18) | ~115K |
| L0 sub-chunk (LOD1, 远处 ~18) | ~41K |
| L1 HLOD proxy (~20, 简化到 2%) | ~80K |
| L2 HLOD proxy (~10) | ~20K |
| **合计** | **~256K** |

占移动端全场景预算（1-3M）的 ~10-17%。

### 7.4 内存占用

| 项目 | 大小 |
|------|------|
| 共享 tile MDL 资源 | ~1.5 MB |
| 1 个 sub-chunk 合并 VB | ~200 KB |
| 1 个 L0 cell（36 sub-chunk） | ~7.2 MB |
| 28 个已加载 L0 cell | **~200 MB GPU** |
| L1 proxy | ~36 MB |

如内存过高，可缩小 L0 loadingRange（768→512m）降低到 ~120MB。

---

## 八、接缝处理总结

| 场景 | 方案 |
|------|------|
| L0 相邻 sub-chunk 同 LOD | 无缝（共享边界顶点） |
| L0 相邻 sub-chunk 不同 LOD | IB stitching（过渡扇形三角形，消除 T-junction） |
| L0 ↔ L1 HLOD | L1 生成时锁定边界顶点 |
| L1 ↔ L2 HLOD | 同上，级联锁定 |

---

## 九、关键调优参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| subChunkSize | 16 | Sub-chunk 边长（tile 数） |
| L0 cellSize | 256m | WorldPartition L0 cell 大小 |
| L0 loadingRange | 768m | L0 加载距离 |
| L1 loadingRange | 3000m | L1 加载距离 |
| LOD0→LOD1 距离 | 200m | Sub-chunk LOD 切换阈值 |
| L1 简化比例 | 5% | HLOD proxy 简化目标 |
| 最大纹理层数 | 32 | ID+Weight 支持的材质层数 |
| 动态纹理数组大小 | 8 | 运行时同时加载的纹理层数 |

---

## 十、实现阶段划分

### Phase 1：地形运行时合并（核心）
- 新建 `TileTerrain`（Component）+ `TileTerrainChunk`（Drawable）
- TileSceneGenerator 输出 WorldPartition cell 数据
- 运行时 VB 合并 + 预生成 IB 变体
- 基础 LOD0/LOD1 切换 + DrawRange stitching

### Phase 2：装饰物 HISM
- TileSceneGenerator 装饰物分组逻辑
- 解析 prefab XML 获取 Model/Material 路径
- 输出 HISMComponent 节点

### Phase 3：L1 HLOD 生成
- 离线 HLOD 构建工具（基于 HLODBuildLib）
- MeshSimplifier 边界顶点锁定
- WorldPartition L0 ↔ L1 原子切换

### Phase 4：ID+Weight 地形材质
- 新 terrain shader（ID+Weight 混合）
- Texture2DArray 动态管理
- TerrainWeightMap 数据结构 + 序列化
- TerrainOperator::PaintTexture 笔刷方法（含 ≤3 约束）
- 合并时从权重图采样注入顶点 (bottomID, topID, weight)
- CLI `paint-texture` 命令

### Phase 5：优化与调优
- 后台线程合并
- LOD 距离自适应
- 内存预算管理
- 移动端 fallback

---

## 十一、涉及的关键文件

| 文件 | 改动 |
|------|------|
| `TileSceneGenerator.h/cpp` | 重构：输出 WorldPartition cell 数据 |
| **新建** `TileTerrain.h/cpp` | 全局管理组件（邻居关系、LOD 更新、WorldPartition 回调） |
| **新建** `TileTerrainChunk.h/cpp` | 每 sub-chunk 的 Drawable（VB/IB 合并、DrawRange LOD） |
| **新建** `TileTerrainDefs.h` | IB 模板预计算 + 共享常量定义 |
| `WorldPartition.h/cpp` | 集成 terrain cell 加载回调 |
| `HISMComponent.h/cpp` | 已有，装饰物直接使用 |
| `HLODBuildLib/MeshMerger` | 已有，L1 proxy 生成复用 |
| `HLODBuildLib/MeshSimplifier` | 已有，L1 proxy 简化复用，需加边界锁定 |
| `TileTerrainCLI.cpp` | 新增 `generate-wp`、`analyze-mesh`、`paint-texture` 命令 |
| **新建** `Analyzer/TileMeshAnalyzer.h/cpp` | MDL 顶点读取 + 边缘分析工具（已实现） |
| **新建** `TerrainWeightMap.h/cpp` | 权重图数据结构 + 序列化 + 采样 |
| **新建** `TerrainOperator.h/cpp`（扩展） | PaintTexture 笔刷 + ≤3 约束检查 |
| `TileSetConfig.h` | TileDef 加 modelPath/materialPath（解析后的直接路径） |
| **新建** `Terrain/TerrainMaterial.material` | ID+Weight terrain shader 材质 |
| `generate_test_terrain.py` | 适配 WorldPartition 输出 |

---

## 十二、验证方案

```bash
# 0. 分析 tile mesh 边缘拓扑（已实现）
TileTerrainCLI.exe analyze-mesh --dir "C:/Workspace/SCE/UrhoXRes/Environment/Legacy/deco/Tiles/me_basemesh_hope/ground"
# 输出每个 MDL 的边缘顶点数、是否规则、BBox 尺寸等

# 1. 构建
cmake --build build_agent --target TileTerrainCLI --config Release

# 2. 转换 tileset（同前）
TileTerrainCLI.exe convert --input ".../me_tiles_field" --output "..." --res-base "..."

# 3. 生成 WorldPartition 数据
TileTerrainCLI.exe generate-wp \
  --input terrain.json \
  --tileset-dir ".../TileSets" \
  --output-dir C:/tmp/terrain_wp \
  --cell-size 256 \
  --sub-chunk-size 16

# 4. 验证输出结构
ls C:/tmp/terrain_wp/cells/L0/
cat C:/tmp/terrain_wp/world_partition.json

# 5. 运行时加载测试（ScenePreview 或 UrhoXRuntime）
# 检查：地形渲染正确、draw call 数量、LOD 切换、无接缝

# 6. 性能测试
# 移动端：检查 DC < 100、GPU 顶点 < 300K、内存 < 200MB
```
