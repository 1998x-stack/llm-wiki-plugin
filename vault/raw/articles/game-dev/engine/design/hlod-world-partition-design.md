---
summary: "Hierarchical LOD + World Partition design for large-scale scene rendering with proxy mesh merging and cell streaming"
related_paths:
  - engine/Source/Urho3D/Graphics/HLOD/**
  - engine/Source/Urho3D/Graphics/**
last_updated: "2026-04-02"
---

# HLOD + World Partition 设计方案

## Context

UrhoX 当前的 LOD 系统是 **per-geometry 多级 LOD**（`StaticModel::geometries_[G][L]`），通过距离阈值选择 LOD 级别。这对单个模型有效，但在大规模场景中（数千个物体），即使所有物体都切到最低 LOD，仍然有数千个 draw call。

**HLOD（Hierarchical Level of Detail）** 的核心思想：在远距离将**一组物体**合并为一个**代理网格（Proxy Mesh）**，用 1 个 draw call 替代 N 个。结合 **World Partition** 的 Cell 流式加载，可实现超大世界的高效渲染和内存管理。

### 目标

- 远距离：数百个物体 → 1 个合并 proxy → 1 draw call
- 材质 atlas：无 SRP Batcher，必须合并纹理 → 单材质 → 单 draw call
- 可扩展聚类：接口化设计，Grid-based 优先，后续扩展 K-means / 手动分组
- World Partition：Cell 流式加载/卸载，与 HLOD 层级联动
- 多级 HLOD：Level 1（物体→proxy），Level 2（proxy→更大 proxy），...
- 构建工具：独立静态库，UrhoXEditor 引用
- 植被实例化：HISM（层级实例化静态网格）组件，O(log N) 层级剔除替代逐物体 Octree 剔除

---

## 一、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    UrhoXEditor                          │
│  ┌──────────────┐  ┌────────────────┐  ┌─────────────┐ │
│  │ HLODBuilder  │  │ WorldPartition │  │ ShaderTools  │ │
│  │    Panel     │  │    Panel       │  │   Panel      │ │
│  └──────┬───────┘  └───────┬────────┘  └─────────────┘ │
│         │                  │                            │
├─────────┼──────────────────┼────────────────────────────┤
│         ▼                  ▼           Library Layer     │
│  ┌──────────────────────────────────┐                   │
│  │         HLODBuildLib             │ ← 独立静态库      │
│  │  ┌──────────┐ ┌───────────────┐  │                   │
│  │  │Clustering│ │  MeshMerger   │  │                   │
│  │  │ Strategy │ │ + AtlasBuilder│  │                   │
│  │  └──────────┘ └───────────────┘  │                   │
│  │  ┌──────────┐ ┌───────────────┐  │                   │
│  │  │ Hierarchy│ │  ProxyModel   │  │                   │
│  │  │ Builder  │ │  Generator    │  │                   │
│  │  └──────────┘ └───────────────┘  │                   │
│  └──────────────────────────────────┘                   │
│         │ 依赖                                          │
│  ┌──────┴───────┐  ┌───────────────┐                    │
│  │MeshSimplifier│  │   Urho3D      │                    │
│  └──────────────┘  └───────────────┘                    │
├─────────────────────────────────────────────────────────┤
│                  Runtime (Urho3D 引擎)                   │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ StaticModel   │  │WorldPartition│  │   Octree     │ │
│  │ (proxy mesh)  │  │  Component   │  │  (existing)  │ │
│  └───────────────┘  └──────────────┘  └──────────────┘ │
│  ┌───────────────┐                                     │
│  │HISMComponent  │  ← 植被实例化渲染（层级剔除）        │
│  │(ClusterTree)  │                                     │
│  └───────────────┘                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 二、World Partition — 多级 Grid 流式加载（参考 UE5）

### 2.1 四叉树式多级 Grid

每个 HLOD Layer 拥有**独立的 Runtime Grid**，CellSize 逐级递增（类似四叉树）。**每一级只替代上一级**，形成 parent-child 链：

```
Grid Level 0 (Actor Grid):    cellSize = 256m   loadingRange = 768m    → 原始物体
Grid Level 1 (HLOD Layer 0):  cellSize = 256m   loadingRange = 3000m   → 替代 L0（合并 Cell 内物体）
Grid Level 2 (HLOD Layer 1):  cellSize = 512m   loadingRange = 8000m   → 替代 L1（合并 4 个 L1 proxy）
Grid Level 3 (HLOD Layer 2):  cellSize = 1024m  loadingRange = ∞       → 替代 L2（Always Loaded）

替代链（每级只替代上一级，不跨级）：
  原始物体 ←→ HLOD L1 ←→ HLOD L2 ←→ HLOD L3
```

```
Camera 近距离（< 768m）：L0 显示原始物体
┌──┬──┬──┬──┐
│  │  │  │  │  256m cells, 独立物体
├──┼──┼──┼──┤
│  │  │  │  │
└──┴──┴──┴──┘

中距离（768m ~ 3000m）：L1 显示 HLOD proxy
┌──┬──┬──┬──┐
│  │  │  │  │  256m cells, L1 HLOD proxy（每个 Cell 一个 proxy）
├──┼──┼──┼──┤
│  │  │  │  │
└──┴──┴──┴──┘

远距离（3000m ~ 8000m）：L2 显示更大的 HLOD proxy
┌─────┬─────┐
│     │     │  512m cells, L2 HLOD proxy（4 个 L1 Cell → 1 个 proxy）
├─────┼─────┤
│     │     │
└─────┴─────┘

超远距离（> 8000m）：L3 显示最粗糙的 HLOD proxy
┌───────────┐
│           │  1024m cells, L3 HLOD proxy
│           │
└───────────┘
```

### 2.2 三态模型 + 状态驱动可见性（参考 UE5）

#### Cell 三态

与 UE5 World Partition 一致，Cell 有三个状态（而非传统的二态加载/卸载）：

| 状态 | 说明 | UrhoX 对应 |
|---|---|---|
| **UNLOADED** | 不在内存 | 无资源、无 Node |
| **LOADED** | 在内存，但**不可见** | 资源已加载，Node 已实例化，但**未添加到 Scene** |
| **ACTIVATED** | 在内存且**可见** | Node 已添加到 Scene，Drawable 注册到 Octree |

LOADED 状态的意义：Cell 在内存中待命，可以**零延迟**切换到 ACTIVATED。这是实现无缝过渡的关键。

#### Loading Range 故意重叠

**不同 Grid 的 Loading Range 故意重叠**（不是互斥的）。HLOD Cell 在其 loadingRange 内被预加载到 LOADED 状态（在内存中但不可见），等待激活：

```
距离 →
|←─── L0 Actor loadingRange (768m) ───→|
|←──────────── L1 HLOD loadingRange (3000m) ──────────────→|
                                       |←── L2 HLOD loadingRange (8000m) ──→|

         重叠区域（L0 + L1 都在内存中）
|←─────────────────────────────────────→|
  L0 ACTIVATED（可见）
  L1 LOADED（在内存但隐藏，等待 L0 退出后接管）
```

#### 可见性 = 源 Cell 状态的反转

HLOD Cell 的可见性**不由距离决定**，而由其**源 Cell 的激活状态**决定：

```
HLOD L1 Cell 的源 Cell = 其覆盖区域内的所有 L0 Cell

所有源 L0 Cell 都 ACTIVATED → L1 Cell 保持 LOADED（隐藏）
所有源 L0 Cell 都非 ACTIVATED → L1 Cell ACTIVATED（显示 proxy）

同理，HLOD L2 Cell 的源 Cell = 覆盖区域内的所有 L1 Cell
```

**原子切换**：同一帧内完成 "源 Cell 全部 Activate + HLOD Cell Deactivate"（反向同理），无空洞、无重叠。

#### 仅基于距离，不考虑相机视锥

与 UE5 World Partition 一致：
- 玩家可能随时转身，按视锥加载会导致转身时看到空白
- 异步加载有延迟，视锥优化收益小但风险高
- 距离环保证 360° 都有数据就绪

可选优化：在 loading queue 中，朝向 Camera 方向的 Cell 提高加载优先级（不影响加载/卸载决策，只影响排队顺序）。

### 2.3 四角问题与 LoadingRange 约束

当 CellSize 递增时（如 L2 = 512m 覆盖 4 个 L1 = 256m Cell），Camera 靠近 L2 Cell 的一角时，L2 HLOD 需要隐藏，4 个 L1 Cell 全部需要 ACTIVATED。

**问题**：如果 L1 的 LoadingRange 不够大，远处角落的 L1 Cell 可能不在范围内 → 空洞。

**约束：每级的 LoadingRange >= 上一级 CellSize × √2**

```
L2 CellSize = 512m → 需要 L1 LoadingRange >= 512 × √2 ≈ 724m
L1 LoadingRange = 3000m >> 724m ✓

→ 当 Camera 靠近 L2 Cell 的任意角落时
  所有 4 个 L1 Cell 都在 L1 的 loadingRange 内
  → L1 Cell 全部 LOADED → 可以全部 ACTIVATED
  → L2 Cell 安全 Deactivate，无空洞
```

**验证公式**：Camera 在 L(N+1) Cell 的最近角，最远角的 L(N) Cell 距离 ≈ L(N+1).cellSize × √2。只要 L(N).loadingRange >= L(N+1).cellSize × √2，所有子 Cell 都在范围内。

典型配置验证：

| 层级 | CellSize | LoadingRange | 上级 CellSize × √2 | 满足？ |
|---|---|---|---|---|
| L0 Actor | 256m | 768m | — | — |
| L1 HLOD | 256m | 3000m | L1 同 CellSize，无四角问题 | ✓ |
| L2 HLOD | 512m | 8000m | 512 × √2 = 724m < 3000m | ✓ |
| L3 HLOD | 1024m | ∞ | 1024 × √2 = 1448m < 8000m | ✓ |

### 2.4 LoadingRange 配置指南

#### 距离度量方式

UrhoX 的 `CellDistance` 使用 **Camera 到 Cell AABB 最近边界的距离**（见 2.6 节）。

注意：UE5 可能使用到 Cell 中心的距离（社区分析，未经官方确认）。我们选择边界距离是因为：大 Cell（如 1024m）用中心距离会导致 Camera 已到 Cell 边界但距中心仍 512m，加载过晚。边界距离确保 Cell 大小不影响加载时机。

若使用中心距离，LoadingRange 需额外加上 `cellSize / 2` 才能等效覆盖。

#### 硬约束

```
L(N).loadingRange >= L(N+1).cellSize × √2
```

否则四角空洞（见 2.3 节）。实际值应远大于下限，为异步加载留出余量。

#### 配置因素

| 因素 | 影响 |
|---|---|
| 可视距离 | 玩家需要看多远 → 决定最外层 HLOD 的 range |
| 内存预算 | 同时在内存的 Cell 数 ≈ π × (range / cellSize)²，range 越大内存越高 |
| 加载速度 | range 越大 → Cell 预加载越早 → Camera 快速移动也不会出现空洞 |
| Cell 密度 | Cell 内物体越多 → 加载耗时越长 → 需要更大的 range 提前加载 |

#### 业界典型配置（参考 UE5）

**小型开放世界**（城镇、岛屿，~2km²）：

| 层级 | CellSize | LoadingRange | 说明 |
|---|---|---|---|
| L0 Actor | 128m | 384m | 近距离独立物体 |
| L1 HLOD | 128m | 1024m | 合并 Cell 内物体 |
| L2 HLOD | 256m | 2048m | 合并 4 个 L1 proxy |
| L3 HLOD | 512m | Always Loaded | 最远距离 |

**中型开放世界**（大地图，~16km²）：

| 层级 | CellSize | LoadingRange | 说明 |
|---|---|---|---|
| L0 Actor | 256m | 768m | 近距离独立物体 |
| L1 HLOD | 256m | 3000m | 合并 Cell 内物体 |
| L2 HLOD | 512m | 8000m | 合并 4 个 L1 proxy |
| L3 HLOD | 1024m | Always Loaded | 最远距离 |

**大型开放世界**（超大地图，~64km²，参考 UE5 CitySample）：

| 层级 | CellSize | LoadingRange | 说明 |
|---|---|---|---|
| L0 Actor | 512m | 1536m | 近距离独立物体 |
| L1 HLOD | 512m | 4096m | 合并 Cell 内物体 |
| L2 HLOD | 1024m | 16000m | 合并 4 个 L1 proxy |
| L3 HLOD | 2048m | Always Loaded | 最远距离 |

**经验公式**：

```
L0:  loadingRange ≈ cellSize × 3
L1:  loadingRange ≈ cellSize × 12
L2:  loadingRange ≈ cellSize × 16
L3:  Always Loaded（或 loadingRange = 视距上限）
```

**配置建议**：
- HLOD CellSize 应为 Actor CellSize 的整数倍（1×、2×、4×），确保 Cell 边界对齐
- Runtime Grid 不超过 3~4 级（UE5 官方建议），更多层级带来的管理开销抵消收益
- 先用保守配置（大 range）确保无空洞，再逐步缩小 range 优化内存

### 2.5 数据结构

```cpp
// engine/Source/Urho3D/Scene/WorldPartition.h

/// 资源引用（type + name），用于 BackgroundLoad 和定向释放
struct ResourceRef
{
    StringHash type_;               // Model::GetTypeStatic() 等
    String name_;                   // 资源路径，如 "WorldData/L0/Cell_3_5/building.mdl"
};

/// 统一的 Cell 结构，适用于所有 Grid Level
/// Level 0 Cell 包含独立物体，Level 1+ Cell 包含 HLOD proxy
struct WorldCell : public Delegate_ResourceAsyncLoading
{
    IntVector2 coord_;              // Cell grid 坐标
    BoundingBox worldBounds_;       // 世界空间 AABB
    unsigned gridLevel_;            // 所属 Grid Level（0=Actor, 1+=HLOD）

    // --- 序列化数据（构建时写入 Cell 描述文件）---
    String sceneDataPath_;          // Node 树/proxy 描述文件路径
    Vector<ResourceRef> resources_; // 该 Cell 依赖的全部资源清单

    // --- 运行时状态 ---
    SharedPtr<Node> rootNode_;      // LOADED 后实例化的 Node（未添加到 Scene）

    /// 已加载资源的 SharedPtr 持有列表
    /// 双重职责：
    ///   1. 加载期间：防止资源被其他 Cell 的卸载释放（保护引用）
    ///   2. 卸载时：提供精确的资源列表，用于从 ResourceCache 定向释放
    Vector<SharedPtr<Resource>> loadedResources_;

    enum CellState
    {
        UNLOADED,       // 不在内存
        LOADING,        // 异步加载资源中
        LOADED,         // 资源就绪，Node 已实例化，但不可见（未添加到 Scene）
        ACTIVATED,      // Node 已添加到 Scene，可见
        CANCELLING      // 加载中被要求卸载，等待剩余回调完成后释放
    };
    CellState state_ = UNLOADED;
    volatile unsigned totalResourceCount_ = 0;
    unsigned currentLoadingResCount_ = 0;

    WorldPartitionComponent* owner_ = nullptr;

    // ─── Delegate_ResourceAsyncLoading 实现（见 4.3 节）───
    void Invoke(Resource* resource, AsyncLoadState state, AsyncLoadError error) override;
    void Release() override {}
};

/// 一个 Grid Level 的配置和 Cell 集合
struct StreamingGrid
{
    unsigned level_;                // 0=Actor Grid, 1+=HLOD Layer
    float cellSize_;                // 该 Grid 的 Cell 大小
    float loadingRange_;            // 加载距离（Cell 在此范围内 → 至少 LOADED）
    float unloadMargin_;            // 卸载边距，防止频繁切换
    HashMap<uint64, WorldCell> cells_;  // PackCoord(x,y) → Cell

    /// 非 UNLOADED 状态的 Cell 列表（LOADING/RESOURCES_READY/LOADED/ACTIVATED/CANCELLING）
    /// 由 BeginLoad(add) 和 →UNLOADED 转换(remove) 维护。
    /// 对于大世界远小于 cells_.Size()（只包含加载范围内的 Cell）。
    PODVector<WorldCell*> activeCells_;
};

class URHO3D_API WorldPartitionComponent : public Component
{
    URHO3D_OBJECT(WorldPartitionComponent, Component);
public:
    /// 添加一个 Grid Level（Level 0 = Actor Grid, Level 1+ = HLOD Layer）
    void AddGridLevel(unsigned level, float cellSize, float loadingRange);

    void Update(const FrameInfo& frame);

    /// 同时加载上限（LOADING 状态的 Cell 数量）。0 = 不限制。
    /// 防止相机快速移动时大量并发 IO。参考 UE5 wp.Runtime.MaxLoadingStreamingCells。
    void SetMaxLoadingCells(unsigned maxCells) { maxLoadingCells_ = maxCells; }
    unsigned GetMaxLoadingCells() const { return maxLoadingCells_; }

private:
    Vector<StreamingGrid> grids_;   // 按 level 排序
    Vector3 cameraPos_;             // 缓存当前帧 Camera 位置，供 Phase 2 使用
    unsigned maxLoadingCells_ = 0;  // 0 = 不限制

    // --- Phase 1: 内存管理（距离驱动，只管 UNLOADED ↔ LOADED）---
    void UpdateGridLoading(StreamingGrid& grid, const Vector3& cameraPos);
    void BeginLoad(WorldCell* cell);
    void CancelLoading(WorldCell* cell);
    void FinishLoad(WorldCell* cell);       // → LOADED（在内存，不可见）
    void Unload(WorldCell* cell);           // LOADED → UNLOADED（不可见时才允许卸载）
    void ReleaseCellResources(WorldCell* cell);
    void RemoveFromActiveCells(WorldCell* cell);  // 从 activeCells_ 移除（swap-erase O(1)）

    // --- Phase 2: 可见性切换（状态驱动，分组原子操作）---
    void UpdateVisibility();
    void ActivateCell(WorldCell* cell);     // LOADED → ACTIVATED
    void DeactivateCell(WorldCell* cell);   // ACTIVATED → LOADED

    // --- 源 Cell / 父 HLOD 查询 ---
    void GetSourceCells(const WorldCell& hlodCell, PODVector<WorldCell*>& result);
    bool AllSourceCellsActivated(const WorldCell& hlodCell);
    bool AllSourceCellsNotActivated(const WorldCell& hlodCell);
    bool HasParentHLOD(const WorldCell& cell);           // Cell 是否被上级 HLOD 覆盖（结构性查询）
    bool HasActivatedParentHLOD(const WorldCell& cell);  // 任何祖先级 HLOD 是否已 ACTIVATED
    bool HasAnyActivatedDescendant(const WorldCell& cell);  // 任何后代级是否有 ACTIVATED Cell
};
```

**统一 Cell 结构**：所有 Grid Level 使用相同的 `WorldCell`，区别仅在于 `gridLevel_` 和 Cell 内容（L0 是独立物体，L1+ 是 proxy）。加载/卸载/取消逻辑完全一致。

### 2.6 Cell 坐标与辅助函数

```cpp
IntVector2 WorldToCell(const Vector3& worldPos, float cellSize)
{
    return IntVector2(
        (int)Floor(worldPos.x_ / cellSize),
        (int)Floor(worldPos.z_ / cellSize)
    );
}

uint64 PackCellCoord(int x, int y)
{
    return ((uint64)(unsigned)x << 32) | (unsigned)y;
}

/// Camera 到 Cell AABB 最近边界的 3D 距离
/// Camera 在 Cell 内部 → 返回 0
/// Camera 在 Cell 外部 → 返回到最近边/角的距离
///
///          ┌─────────┐
///          │  Cell    │
///     ★────┤         │   CellDistance = Camera 到最近表面的距离
///   Camera  │         │
///          └─────────┘
///
/// 为什么用边界距离而非中心距离：
///   大 Cell（如 1024m）的中心距离很大，即使 Camera 在 Cell 边界旁，
///   中心距离仍 ~512m，导致加载过晚。边界距离确保 Cell 越大不会导致加载越晚。
///
/// 为什么用 3D 距离而非 XZ 平面距离：
///   山地/高低差场景中，Camera 高度差会影响实际可视距离。
///   3D 距离确保在高处俯瞰时不会加载过多地面 Cell。
float CellDistance(const Vector3& cameraPos, const BoundingBox& cellBounds)
{
    // 3D 点到 AABB 的最短距离
    float dx = Max(cellBounds.min_.x_ - cameraPos.x_, Max(0.0f, cameraPos.x_ - cellBounds.max_.x_));
    float dy = Max(cellBounds.min_.y_ - cameraPos.y_, Max(0.0f, cameraPos.y_ - cellBounds.max_.y_));
    float dz = Max(cellBounds.min_.z_ - cameraPos.z_, Max(0.0f, cameraPos.z_ - cellBounds.max_.z_));
    return Sqrt(dx * dx + dy * dy + dz * dz);
}

/// 查找 HLOD Cell 覆盖区域内的所有下一级 Cell（源 Cell）
void WorldPartitionComponent::GetSourceCells(const WorldCell& hlodCell, PODVector<WorldCell*>& result)
{
    unsigned srcLevel = hlodCell.gridLevel_ - 1;
    StreamingGrid& srcGrid = grids_[srcLevel];
    float srcCellSize = srcGrid.cellSize_;

    IntVector2 minCoord = WorldToCell(hlodCell.worldBounds_.min_, srcCellSize);
    IntVector2 maxCoord = WorldToCell(
        hlodCell.worldBounds_.max_ - Vector3(0.01f, 0, 0.01f), srcCellSize);

    for (int x = minCoord.x_; x <= maxCoord.x_; ++x)
        for (int y = minCoord.y_; y <= maxCoord.y_; ++y)
        {
            auto it = srcGrid.cells_.Find(PackCellCoord(x, y));
            if (it != srcGrid.cells_.End())
                result.Push(&it->second_);
        }
}

/// 检查 L0 Cell 是否有上级 HLOD Cell 覆盖
/// 用于判断没有 HLOD 的 L0 Cell（世界边缘、或未构建 HLOD 的区域）
/// 这些 Cell 不走分组切换，可直接自动激活
bool WorldPartitionComponent::HasParentHLOD(const WorldCell& cell)
{
    if (cell.gridLevel_ + 1 >= grids_.Size())
        return false;
    StreamingGrid& parentGrid = grids_[cell.gridLevel_ + 1];
    IntVector2 parentCoord = WorldToCell(cell.worldBounds_.Center(), parentGrid.cellSize_);
    return parentGrid.cells_.Contains(PackCellCoord(parentCoord.x_, parentCoord.y_));
}
```

### 2.7 流式加载 Update 逻辑

Update 分两个阶段：先做距离驱动的内存管理，再做状态驱动的可见性切换。

**核心原则**：
- **Phase 1（距离驱动）只管 UNLOADED ↔ LOADED，永远不碰 ACTIVATED 状态的 Cell**
- **Phase 2（状态驱动）管 LOADED ↔ ACTIVATED，所有可见性切换都是分组原子操作**

这样分离的原因：HLOD proxy 覆盖多个源 Cell 区域，如果逐个激活/卸载源 Cell，必然产生重叠（proxy + 真实物体同时可见）或空洞（既没有 proxy 也没有真实物体）。

**性能优化（参考 UE5）**：
- Phase 1 加载：**从相机位置做空间查询** → O(radius²/cellSize²)，不遍历全部 Cell
- Phase 1 卸载 + Phase 2：**只遍历 activeCells_**（非 UNLOADED 的 Cell 子集）
- 复杂度与**世界大小无关**，仅与加载范围相关

```cpp
void WorldPartitionComponent::Update(const FrameInfo& frame)
{
    Vector3 cameraPos = frame.camera_->GetNode()->GetWorldPosition();
    cameraPos_ = cameraPos;  // 缓存供 Phase 2 使用

    // Phase 1: 每个 Grid 独立做内存管理（距离驱动）
    for (auto& grid : grids_)
        UpdateGridLoading(grid, cameraPos);

    // Phase 2: 统一做可见性切换（状态驱动，分组原子操作）
    UpdateVisibility();
}
```

#### Phase 1: 距离驱动的内存管理（Streaming Source 空间查询）

两遍结构：
- **Pass 1**：从 cameraPos ± loadingRange 计算 Cell 坐标范围，只查询该范围内的 Cell → 加载 UNLOADED Cell
- **Pass 2**：遍历 `activeCells_`（非 UNLOADED 子集）→ 延迟实例化 + 卸载超出范围的 Cell

**关键：Phase 1 只卸载 LOADED（不可见）的 Cell，不碰 ACTIVATED（可见）的 Cell。**

```cpp
void WorldPartitionComponent::UpdateGridLoading(StreamingGrid& grid, const Vector3& cameraPos)
{
    bool alwaysLoaded = (grid.loadingRange_ < 0.0f);

    // ═══ Pass 1: 加载新 Cell — 从相机位置做空间查询 ═══
    // 不遍历全部 Cell，只遍历 loadingRange 内的坐标范围。O(radius²/cellSize²)。
    if (!alwaysLoaded)
    {
        // 统计当前 LOADING 数量，受 maxLoadingCells_ 限流
        unsigned currentLoading = 0;
        if (maxLoadingCells_ > 0)
            for (auto* c : grid.activeCells_)
                if (c->state_ == WorldCell::LOADING)
                    ++currentLoading;

        float range = grid.loadingRange_;
        Vector3 rangeVec(range, 0, range);
        IntVector2 minCoord = WorldToCell(cameraPos - rangeVec, grid.cellSize_);
        IntVector2 maxCoord = WorldToCell(cameraPos + rangeVec, grid.cellSize_);

        for (int x = minCoord.x_; x <= maxCoord.x_; ++x)
            for (int y = minCoord.y_; y <= maxCoord.y_; ++y)
            {
                if (maxLoadingCells_ > 0 && currentLoading >= maxLoadingCells_)
                    goto loadingDone;

                auto it = grid.cells_.Find(PackCellCoord(x, y));
                if (it == grid.cells_.End()) continue;
                WorldCell& cell = it->second_;
                if (cell.state_ != WorldCell::UNLOADED) continue;
                if (CellDistance(cameraPos, cell.worldBounds_) < range)
                {
                    BeginLoad(&cell);   // → LOADING, 加入 activeCells_
                    ++currentLoading;
                }
            }
        loadingDone:;
    }
    else
    {
        // alwaysLoaded: 加载所有 UNLOADED Cell（通常数量少）
        for (auto& pair : grid.cells_)
            if (pair.second_.state_ == WorldCell::UNLOADED)
                BeginLoad(&pair.second_);
    }

    // ═══ Pass 2: 处理 active cells — 延迟实例化 + 卸载 ═══
    // 只遍历 activeCells_（非 UNLOADED 子集），比遍历全部 cells_ 小得多。
    for (unsigned i = 0; i < grid.activeCells_.Size(); )
    {
        WorldCell* cell = grid.activeCells_[i];
        if (cell->state_ == WorldCell::CANCELLING) { ++i; continue; }

        // 延迟实例化：资源就绪后同步实例化 Node
        if (cell->state_ == WorldCell::RESOURCES_READY)
            FinishLoad(cell);

        if (!alwaysLoaded)
        {
            float dist = CellDistance(cameraPos, cell->worldBounds_);
            if (dist >= grid.loadingRange_ + grid.unloadMargin_)
            {
                // ★ 只卸载不可见的 Cell（LOADED），不碰可见的（ACTIVATED）
                if (cell->state_ == WorldCell::LOADED || cell->state_ == WorldCell::RESOURCES_READY)
                {
                    Unload(cell);       // → UNLOADED, swap-erase 从 activeCells_ 移除
                    continue;           // 不递增 i，swap 后的元素现在在 i 位置
                }
                else if (cell->state_ == WorldCell::LOADING)
                {
                    CancelLoading(cell);
                    if (cell->state_ == WorldCell::UNLOADED)
                        continue;       // 已从 activeCells_ 移除
                }
                // ACTIVATED → 不处理！等 Phase 2 通过分组原子切换处理
            }
        }
        ++i;
    }
}
```

**activeCells_ 维护规则**（3 个转换点）：

| 转换 | 位置 | 操作 |
|------|------|------|
| UNLOADED → LOADING | `BeginLoad()` 末尾 | `activeCells_.Push(cell)` |
| → UNLOADED | `Unload()` 内 | `RemoveFromActiveCells(cell)`（swap-erase） |
| CANCELLING → UNLOADED | `WorldCell::Invoke()` 回调 | `RemoveFromActiveCells(cell)` |

**16km 世界性能对比**（L0=256m, loadingRange=768m）：

| 操作 | 遍历全部 cells_ | 空间查询 + activeCells_ |
|------|-----------------|------------------------|
| Pass 1 加载 | 4096 cells | ~36 坐标查询 |
| Pass 2 卸载 | 4096 cells | ~200 active cells |
| 总计 | **~5400/帧** | **~600/帧** |

**为什么不能在 Phase 1 直接卸载 ACTIVATED Cell？**

考虑 L1 HLOD（512m）覆盖 4 个 L0 Cell（256m）的场景。Camera 远离时，4 个 L0 Cell 依次超出 loadingRange：

```
旧方案（Bug）：
  T1: L0 Cell A 超出 range → Phase 1 直接 Unload → UNLOADED（消失！）
      L0 Cell B/C/D 仍在 range → ACTIVATED
      L1 检查: Cell B 仍 ACTIVATED → L1 不能激活
      → Cell A 区域空洞！

修正方案：
  T1: L0 Cell A 超出 range → Phase 1 跳过（ACTIVATED 不处理）
      Phase 2 检查: Cell A 超出 range → 触发整组切换
      → 同帧: 4 个 L0 全部 DeactivateCell + L1 ActivateCell
      → 无空洞
```

#### Phase 2: 状态驱动的可见性切换（分组原子操作）

**从高层级到低层级处理**（先处理 HLOD，再处理 Actor）。所有可见性切换都是分组操作——同一个 HLOD Cell 的所有源 Cell 同时激活或同时隐藏。

**只遍历 activeCells_**，不遍历全部 cells_。UNLOADED 的 HLOD Cell 无需参与可见性判断。

**多层级防重叠机制**：
- `HasActivatedParentHLOD()` — 祖先级 HLOD 已激活时，低层级不自激活（防 L2+L1 同时亮）
- `HasAnyActivatedDescendant()` — 后代级有 Cell 激活时，高层级不自激活（防相机后退时 L2 抢先于 L1）
- 两个检查配合 highest-to-lowest 处理顺序，保证**任何时刻只有一个层级可见**

```cpp
void WorldPartitionComponent::UpdateVisibility()
{
    // 从高层级到低层级处理（L2 先于 L1 先于 L0）
    for (int i = grids_.Size() - 1; i >= 0; --i)
    {
        StreamingGrid& grid = grids_[i];
        if (grid.level_ == 0)
            continue;  // L0 不在这里自主激活，由上级 HLOD 的原子切换驱动

        StreamingGrid* srcGrid = GetGrid(grid.level_ - 1);

        // 只遍历 active（非 UNLOADED）的 HLOD Cell
        for (unsigned c = 0; c < grid.activeCells_.Size(); ++c)
        {
            WorldCell& hlodCell = *grid.activeCells_[c];
            PODVector<WorldCell*> sourceCells;
            GetSourceCells(hlodCell, sourceCells);

            if (hlodCell.state_ == WorldCell::ACTIVATED)
            {
                // ═══ Camera 靠近：L(N) → L(N-1) 过渡 ═══
                // 条件：所有源 Cell 都在内存（LOADED 或 ACTIVATED）
                //       且都在源 Grid 的 switchBackRange 内
                // → 整组原子切换：激活全部源 Cell（跳过已激活的）+ 隐藏 HLOD
                //
                // 源 Cell 可能已经是 ACTIVATED（由低层级过渡先激活），这是合法的。
                float switchBackRange = srcGrid->loadingRange_ - srcGrid->unloadMargin_;
                bool allSourcesReady = !sourceCells.Empty();
                for (auto* src : sourceCells)
                {
                    CellState st = src->state_;
                    if (st != WorldCell::LOADED && st != WorldCell::ACTIVATED)
                    { allSourcesReady = false; break; }
                    if (CellDistance(cameraPos_, src->worldBounds_) >= switchBackRange)
                    { allSourcesReady = false; break; }
                }

                if (allSourcesReady)
                {
                    for (auto* src : sourceCells)
                        if (src->state_ != WorldCell::ACTIVATED)
                            ActivateCell(src);
                    DeactivateCell(&hlodCell);   // → LOADED
                }
            }
            else if (hlodCell.state_ == WorldCell::LOADED)
            {
                // ═══ Camera 远离：L(N-1) → L(N) 过渡 ═══
                // 条件：任一源 Cell 超出其 loadingRange
                //       且所有源 Cell 都是 ACTIVATED
                // → 整组原子切换：隐藏全部源 Cell + 激活 HLOD
                bool anySourceBeyondRange = false;
                bool allSourcesActivated = true;
                for (auto* src : sourceCells)
                {
                    if (src->state_ != WorldCell::ACTIVATED)
                        allSourcesActivated = false;
                    if (CellDistance(cameraPos_, src->worldBounds_) >= srcGrid->loadingRange_)
                        anySourceBeyondRange = true;
                }

                if (anySourceBeyondRange && allSourcesActivated)
                {
                    for (auto* src : sourceCells)
                        DeactivateCell(src);     // → LOADED
                    ActivateCell(&hlodCell);
                }

                // ═══ 初始 / 远距离激活 ═══
                // 条件：所有后代级都没有 ACTIVATED Cell（区域完全无覆盖）
                //       且没有祖先级 HLOD 已 ACTIVATED（防止多层重叠）
                // → 激活此 HLOD 覆盖该区域
                //
                // 为什么检查所有后代而非仅直接源：
                //   相机后退时，L2 先处理，此时 L0 可能还是 ACTIVATED。
                //   只检查 L1（直接源）看不到 L0 的激活状态 → L2 误激活。
                if (!HasAnyActivatedDescendant(hlodCell)
                    && !HasActivatedParentHLOD(hlodCell))
                {
                    ActivateCell(&hlodCell);
                }
            }
        }
    }

    // L0 Cell 如果没有上级 HLOD 覆盖 → 自动激活
    // （世界边缘、或未构建 HLOD 的区域）
    if (!grids_.Empty() && grids_[0].level_ == 0)
    {
        StreamingGrid& actorGrid = grids_[0];
        for (unsigned c = 0; c < actorGrid.activeCells_.Size(); ++c)
        {
            WorldCell& cell = *actorGrid.activeCells_[c];
            if (cell.state_ == WorldCell::LOADED && !HasParentHLOD(cell))
                ActivateCell(&cell);
        }
    }
}
```

**为什么 L0 Cell 不能逐个自动激活？**

考虑 L1 HLOD（256m proxy）覆盖 4 个 L0 Cell。Camera 靠近时，4 个 L0 Cell 异步加载，完成时间不同：

```
旧方案（Bug）：
  T1: L1 ACTIVATED（显示 proxy）
      L0 Cell A → LOADED → 自动 ACTIVATED（真实物体出现）
      L0 Cell B/C/D → 还在 LOADING
      → Cell A 区域: proxy + 真实物体同时渲染 → Z-Fighting 闪烁！

修正方案：
  T1: L1 ACTIVATED（显示 proxy）
      L0 Cell A → LOADED（不可见，等待兄弟）
      L0 Cell B/C/D → LOADING
  T2: L0 Cell B → LOADED（不可见，等待兄弟）
  T3: L0 Cell C, D → LOADED（全部就绪）
      → Phase 2 检查: 全部 LOADED → 同帧原子切换
      → 4 个 L0 全部 ActivateCell + L1 DeactivateCell
      → 无闪烁、无重叠
```

**HLOD 级联切换（首次加载）**：

游戏启动时，从最高级 HLOD 向下级联切换：

```
T0: L3 Always Loaded → ACTIVATED（最粗粒度 proxy）
    L2 cells 开始加载
T1: L2 cells 全部 LOADED → 原子切换: L2 ACTIVATED + L3 DEACTIVATED
    L1 cells 开始加载
T2: L1 cells 全部 LOADED → 原子切换: L1 ACTIVATED + L2 DEACTIVATED
    L0 cells 开始加载
T3: L0 cells 全部 LOADED → 原子切换: L0 ACTIVATED + L1 DEACTIVATED
    → 玩家看到: L3 proxy → L2 proxy → L1 proxy → 真实物体（逐步细化）
```

**原子切换保证**：所有可见性切换都发生在 `UpdateVisibility()` 同一帧内。不存在"部分源 Cell 可见 + HLOD 也可见"的多帧重叠，也不存在"源 Cell 卸载 + HLOD 未激活"的空洞。

**多层级防重叠机制**：

3+ 层 HLOD 时，仅靠"直接源 Cell 未激活"不足以防止重叠。例如 L0 ACTIVATED → 相机后退 → 同一帧内 L2 和 L1 都尝试自激活 → 双层重叠。

解决方案：两个辅助查询 + highest-to-lowest 处理顺序配合工作：

| 查询 | 作用 | 场景 |
|------|------|------|
| `HasActivatedParentHLOD(cell)` | 祖先级已激活 → 不自激活 | L2 已激活时，L1 不自激活 |
| `HasAnyActivatedDescendant(cell)` | 后代级有激活 → 不自激活 | L0 仍激活时，L2 不抢先激活 |

处理顺序保证：L2 先处理完毕 → L1 处理时能看到 L2 的状态。同一帧内不会出现多层同时激活。

### 2.8 边界：World Partition 与植被实例化

#### World Partition 只管「场景物体」

World Partition Cell 流式管理的对象是**独立的场景物体**（建筑、道具、石头等），每个物体是一个 Node + StaticModel Drawable，通过 Octree 逐个做 Frustum Culling。

一个 128m Cell 内的场景物体通常是**几十~几百个**，CPU Octree 剔除完全能承受。

#### 密集植被不走 World Partition

密集植被（草、灌木、树木）的特征：
- **数量极大**：一块 128m 的森林可能有数千~数万株植被
- **几何相同**：同类植被共享 Mesh + Material，仅 Transform 不同
- **渲染距离短**：草 40-50m，灌木 60-80m，树 100-200m

如果每株植被都是独立 Drawable 走 Octree 剔除 → **O(N) per-frame 剔除**，完全不可接受。

#### 业界解决方案

UE5 采用两套独立系统：

| 类型 | 系统 | 流式方式 | 渲染方式 | CPU 剔除复杂度 |
|---|---|---|---|---|
| 场景物体 | World Partition Actor Grid | Cell 距离驱动 | StaticModel（逐物体） | O(N) 但 N 小 |
| 放置植被（树） | World Partition + HISM | 跟随 Cell 流式 | HISM（GPU Instancing + Cluster Tree） | O(log N) |
| 地表覆盖（草） | Landscape Grass（独立系统） | 独立距离驱动 | HISM（GPU Instancing + Cluster Tree） | O(log N) |

**核心**：植被使用 **HISM（Hierarchical Instanced Static Mesh）** 渲染 —— 一个组件管理上千个实例，内部通过 Cluster Tree 做 O(log N) 层级剔除，只需 1 个 draw call。

#### UrhoX 的方案

```
┌─────────────────────────────────────────────────────┐
│              World Partition Cell 流式               │
│  管理「场景物体」的加载/卸载                          │
│  每个 Cell 内物体数 = 建筑、石头、道具等              │
│  通常几十~几百个，CPU Octree 剔除完全能承受           │
├─────────────────────────────────────────────────────┤
│              植被实例化系统（HISM）                   │
│                                                     │
│  ┌─────────────────┐  ┌─────────────────┐           │
│  │ 放置植被（树木）  │  │ 地表覆盖（草丛） │           │
│  │ 跟随 Cell 流式   │  │ 独立距离流式     │           │
│  │ 距离: 100-200m  │  │ 距离: 40-50m    │           │
│  │ HISM 渲染       │  │ HISM 渲染       │           │
│  │ Cluster Tree    │  │ Cluster Tree    │           │
│  └─────────────────┘  └─────────────────┘           │
│                                                     │
│  1 个 HISM = 1 个 Drawable = 1~few draw call        │
│  内部 Cluster Tree 做 O(log N) 层级剔除              │
└─────────────────────────────────────────────────────┘
```

详细设计见 **第十节：植被实例化渲染系统（HISM）**。

---

## 三、HLOD 离线构建管线

### 3.1 可扩展聚类接口

```cpp
// engine/Source/Tools/HLODBuildLib/Clustering/IClusteringStrategy.h

struct ClusterInput
{
    struct ObjectInfo
    {
        unsigned nodeID;            // 场景 Node ID
        BoundingBox worldBounds;    // 世界空间 AABB
        Vector3 worldCenter;        // 质心
        unsigned triangleCount;     // 三角形数
        unsigned materialHash;      // 材质哈希（用于优先合并同材质）
    };
    PODVector<ObjectInfo> objects;
    BoundingBox worldBounds;        // 整个区域的 AABB
};

struct Cluster
{
    PODVector<unsigned> objectIndices;  // 引用 ClusterInput::objects 的索引
    BoundingBox bounds;                // Cluster 的 AABB
};

struct ClusterOutput
{
    Vector<Cluster> clusters;
};

class IClusteringStrategy : public RefCounted
{
public:
    virtual ~IClusteringStrategy() = default;
    virtual String GetName() const = 0;
    virtual ClusterOutput Execute(const ClusterInput& input) = 0;
};
```

### 3.2 Grid-Based 聚类（首选实现）

```cpp
// engine/Source/Tools/HLODBuildLib/Clustering/GridClustering.h

class GridClustering : public IClusteringStrategy
{
public:
    String GetName() const override { return "Grid"; }

    void SetGridSize(float size) { gridSize_ = size; }
    void SetMaxObjectsPerCluster(unsigned max) { maxObjects_ = max; }

    ClusterOutput Execute(const ClusterInput& input) override;

private:
    float gridSize_ = 64.0f;       // 聚类网格大小
    unsigned maxObjects_ = 256;     // 最多物体数（避免 proxy 过大）
};
```

**Grid 聚类算法**:
1. 按 gridSize_ 将世界空间划分为网格
2. 将每个 object 分配到其 worldCenter 所在的 grid cell
3. 过滤掉 objectCount < minObjects_ 的 cell
4. 如果 cell 内物体 > maxObjects_，递归细分（halfSize）
5. 每个 grid cell 输出一个 Cluster

### 3.3 材质烘焙（GPU Render-to-Texture）

由于 UrhoX **没有 SRP Batcher**，多材质的多个物体即使合并了 mesh，仍然是多个 draw call。必须将所有材质参数烘焙为 atlas 纹理 → 单材质 → 单 draw call。

#### 3.3.1 原理：UV 空间延迟渲染

利用引擎现有的延迟渲染管线，将材质参数烘焙到 atlas 纹理。核心思想：

- **顶点变换**：用 UV 坐标替代世界坐标作为屏幕位置
- **TBN = 单位矩阵**：使 shader 输出切线空间法线原值（而非世界空间法线）
- **MRT 输出**：一次 draw call 同时输出所有材质通道

```
普通延迟渲染:  worldPos → MVP → 屏幕坐标 → EncodeGBufferPBR → GBuffer MRT
材质烘焙:     UV coord → NDC          → EncodeGBufferBake → Atlas MRT
```

#### 3.3.2 Bake 专用 GBuffer 宏

现有 `EncodeGBufferPBR`（`Res/Shaders/BLGL/screen_pos.sh`）会对法线做 `EncodeNormal()` 编码压缩，不适合 bake。需要替代宏直接输出原始参数值：

```glsl
// Bake 专用宏：按 PBRLitSolid 输入纹理通道格式存储
// 运行时 proxy 材质直接采样这些 atlas 纹理，uniform 设为中性值（1.0）
//
// 参考 PBRLitSolid.glsl 的采样方式:
//   sDiffMap      → baseColor = cMatDiffColor * texture2D(sDiffMap)
//   sSpecMap      → roughness = .r * cTextureRoughnessFactor
//                    metallic  = .g * cTextureMetallicFactor
//                    occlusion = .b
//   sNormalMap    → nn = DecodeNormal(texture2D(sNormalMap))
//   sEmissiveMap  → emissive = cMatEmissiveColor * texture2D(sEmissiveMap)

#define EncodeGBufferBake(diffuseColor, metallic, specular, roughness, normalDirection, emissiveColor) \
    gl_FragData[0].rgb = diffuseColor;                        \
    gl_FragData[1].r   = roughness;                           \
    gl_FragData[1].g   = metallic;                            \
    gl_FragData[1].b   = 1.0;                                \
    gl_FragData[2].rgb = EncodeNormalStore(normalDirection);   \
    gl_FragData[3].rgb = emissiveColor;
// MRT 输出 → 对应运行时纹理:
// RT0.rgb → atlas_diffuse   (sDiffMap)      已包含 cMatDiffColor 等 uniform 乘算
// RT1.rgb → atlas_spec      (sSpecMap)      R=roughness, G=metallic, B=occlusion
// RT2.rgb → atlas_normal    (sNormalMap)    需 EncodeNormalStore 编码，运行时 DecodeNormal 读回
// RT3.rgb → atlas_emissive  (sEmissiveMap)  已包含 cMatEmissiveColor 乘算
```

**运行时 proxy 材质 uniform（全部设为中性值）**:
```
cMatDiffColor = (1, 1, 1, 1)
cTextureRoughnessFactor = 1.0
cTextureMetallicFactor = 1.0
cMatEmissiveColor = (1, 1, 1)
cMatSpecColor = (1, 1, 1)    // specular 已 bake 进 roughness/metallic
```

**关键设计点**：
1. MRT 通道按 PBRLitSolid 的**输入纹理格式**存储（非 GBuffer 编码格式）
2. Shader 执行所有 uniform 乘算、混合后输出最终值 → atlas 纹理包含完整材质效果
3. 法线使用 `EncodeNormalStore`（`DecodeNormal` 的逆操作），确保运行时 `DecodeNormal` 能正确读回
4. 不同材质的 sSpecMap 通道含义一致（R=rough, G=metal, B=occ），天然兼容

#### 3.3.3 Bake 顶点构造

```cpp
// 对每个 mesh 的每个顶点，构造 bake 用的顶点数据：
struct BakeVertex
{
    // Position = UV 映射到 NDC（atlas 子区域）
    float position[3];  // (atlasU * 2 - 1, -(atlasV * 2 - 1), 0)

    // TBN = 单位矩阵 → shader 输出切线空间法线原值
    float tangent[4];   // (1, 0, 0, 1)
    float normal[3];    // (0, 0, 1)

    // UV = 原始 UV → 供材质正确采样纹理
    float uv[2];        // 原始 mesh UV
};
```

**为什么 TBN = 单位矩阵？**

shader 中法线计算：`worldNormal = T * normalMap.x + B * normalMap.y + N * normalMap.z`

TBN = identity 时：`output = normalMap.xyz`（切线空间法线原值）

运行时 Merged Mesh 保留原始几何 → 原始 TBN 不变 → 采样 atlas 法线 → 经真实 TBN 变换 → 正确世界法线。

#### 3.3.4 完整 Bake 流程

```
Step 1: UV Atlas 布局
  对 cluster 中每个 mesh 的每个 geometry 分配 atlas 子区域
  Bin Packing（Skyline 算法），每个 geometry 记录 AtlasRect { u0, v0, u1, v1 }

Step 2: 构造 Bake 顶点
  遍历每个 geometry 的每个顶点：
    position = UV 重映射到 atlas NDC 空间
    tangent = (1, 0, 0, 1), normal = (0, 0, 1)
    uv = 原始 UV

Step 3: GPU Render（一次 draw per material）
  创建 atlas 大小的 MRT（4 个 RenderTarget）
  对每个 mesh，绑定其原始材质（走 DEFERRED 路径，但用 EncodeGBufferBake）
  Draw call → MRT 同时写入所有通道

Step 4: ReadBack（MRT 通道对应运行时纹理 slot）
  RT0 → atlas_diffuse.png   （sDiffMap，已含 cMatDiffColor 等乘算）
  RT1 → atlas_spec.png      （sSpecMap，R=roughness, G=metallic, B=occlusion）
  RT2 → atlas_normal.png    （sNormalMap，EncodeNormalStore 编码的切线空间法线）
  RT3 → atlas_emissive.png  （sEmissiveMap，已含 cMatEmissiveColor 乘算）

Step 5: 合并 VB/IB
  将所有 mesh 的顶点数据合并为一个 VertexBuffer
  将所有 mesh 的索引数据合并为一个 IndexBuffer（index 加偏移）
  顶点 position 用 worldTransform 变换到世界空间
  顶点 UV 重映射到 atlas 子区域

Step 6: 生成 Proxy Material
  创建 Material:
    technique = PBRLitSolid (DEFERRED + DIFFMAP + METALLIC + NORMALMAP + EMISSIVEMAP)
    sDiffMap     = atlas_diffuse
    sSpecMap     = atlas_spec
    sNormalMap   = atlas_normal
    sEmissiveMap = atlas_emissive
  Uniform 全部中性值（值已 bake 进纹理）:
    cMatDiffColor = (1,1,1,1)
    cTextureRoughnessFactor = 1.0
    cTextureMetallicFactor = 1.0
    cMatEmissiveColor = (1,1,1)
    cTintColor.a = 0.0  （禁用 tint blend）
```

#### 3.3.5 多 Part 物体处理

一个 StaticModel 可能有多个 geometry（`geometries_[0..N]`），每个用不同材质。

处理方式：每个 geometry 作为独立的 bake 单元，各自分配 atlas 区域、各自绑定材质渲染。最终全部合并为单 geometry、单材质。

```cpp
for (Node* node : clusterNodes)
{
    StaticModel* sm = node->GetComponent<StaticModel>();
    for (unsigned g = 0; g < sm->GetNumGeometries(); ++g)
    {
        BakeEntry entry;
        entry.model = sm->GetModel();
        entry.geometryIndex = g;
        entry.worldTransform = node->GetWorldTransform();
        entry.material = sm->GetMaterial(g);  // 每个 part 独立材质
        bakeEntries.Push(entry);
    }
}
```

#### 3.3.6 Opaque / AlphaMask 分组

每个 cluster 按材质类型分成两组，各自生成独立 proxy：

| Proxy | 包含物体 | Technique | 说明 |
|---|---|---|---|
| Opaque Proxy | 不透明物体 | PBRLitSolid（无 ALPHAMASK） | 无 alpha test 开销 |
| AlphaMask Proxy | AlphaTest 物体 | PBRLitSolid + ALPHAMASK | atlas_diffuse.a 保留 alpha |
| — | Alpha Blend 物体 | 不参与合并 | 需 forward 透明 pass + 排序 |

每 cluster 最多 2 个 draw call（Opaque + AlphaMask），比原来 N 个物体仍大幅减少。

分组判断依据：材质 technique 是否包含 `ALPHAMASK` 或 `ALPHA` 宏定义。

#### 3.3.7 限制

- **Alpha Blend 物体**：不参与合并，保留原始材质独立渲染
- **世界坐标采样材质**（triplanar mapping 等）：UV 空间渲染结果不正确，需排除
- **动态效果材质**（Dissolve、Stealth 等）：bake 只保留静态快照，动态效果丢失
- **Atlas 精度**：atlas 分辨率有限，每个物体分到的纹素密度随物体数量增加而降低

### 3.4 Proxy Model 简化

合并后的 mesh 可能三角形数很高，需要用 MeshSimplifier 简化。

```cpp
// engine/Source/Tools/HLODBuildLib/ProxyGenerator.h

struct ProxySettings
{
    float targetTriangleRatio = 0.1f;   // 目标三角形比率（相对合并后总量）
    float maxError = 0.01f;             // QEM 最大允许误差
    unsigned atlasSize = 4096;          // Atlas 分辨率
    unsigned atlasPadding = 2;
    bool preserveUV = true;             // 简化时保持 UV 属性
};

struct ProxyOutput
{
    SharedPtr<Model> model;
    SharedPtr<Material> material;
    SharedPtr<Image> atlasDiffuse;      // RT0 → sDiffMap
    SharedPtr<Image> atlasSpec;         // RT1 → sSpecMap (R=rough, G=metal, B=occ)
    SharedPtr<Image> atlasNormal;       // RT2 → sNormalMap (EncodeNormalStore)
    SharedPtr<Image> atlasEmissive;     // RT3 → sEmissiveMap
};

class ProxyGenerator
{
public:
    /// 从一组场景物体生成 HLOD proxy
    bool Generate(
        const Vector<Node*>& sourceNodes,   // 需要合并的场景 Node
        const ProxySettings& settings,
        ProxyOutput& output
    );

private:
    // 1. 收集每个 Node 的每个 geometry + material
    // 2. UV Atlas 布局（Bin Packing）
    // 3. GPU Bake（EncodeGBufferBake → MRT 输出 4 张 atlas）
    // 4. 合并 VB/IB（世界空间位置 + atlas UV）
    // 5. MeshSimplifier::Simplify() → 简化
    // 6. 生成 PBR Material（4 张 atlas 纹理，uniform 默认值）
};
```

**复用现有 MeshSimplifier**（`engine/Source/Tools/MeshSimplifier/`）：
```cpp
IMeshSimplifier* simplifier = new MeshSimplifier(
    vertices, indices, attributeWeights, partIDs, boneInfluences);
simplifier->SetPreserveVolume(true);
simplifier->SetOffsets(normalOffset, tangentOffset, colorOffset, uvOffset, 0);
simplifier->Simplify(
    0,                          // targetNumVertices (0 = 不限)
    targetTriangleCount,        // targetNumTriangles
    settings.maxError,          // targetError
    0, 0, 0                     // limits (0 = 不限)
);
simplifier->Compact();
```

### 3.5 植被（HISM）与 HLOD Proxy 的关系

#### 构建时：植被不参与 HLOD Proxy 合并

`HierarchyBuilder::Build()` 内部通过 `VegetationCollector::CollectAndPartition()` 将场景节点分为两组：

| 节点类型 | 判定条件 | 构建流程 |
|---|---|---|
| **普通物体**（建筑、石头等） | 无 `HISMGroup` 变量 | → 聚类 → Mesh 合并 → Proxy 简化 → L1/L2 proxy |
| **植被**（树木、灌木等） | 有 `HISMGroup` 变量 | → 收集 transform → 存入 `result.vegetation_` → **不进入 proxy 管线** |

```
场景节点 ──→ VegetationCollector::CollectAndPartition()
              │
              ├─ 有 HISMGroup → vegGroups（植被组）──→ L0 Cell 中生成 HISMComponent
              │                                       L1/L2 中无对应，被 proxy 整体替代
              │
              └─ 无 HISMGroup → sourceNodes ──→ Clustering → MeshMerger → Proxy
```

#### 运行时：远距离植被被 HLOD Proxy 替代

| 距离 | L0 植被 HISM | HLOD Proxy |
|---|---|---|
| 近距离（L0 ACTIVATED） | 可见，HISM 实例化渲染 | 不可见 |
| 中距离（L1 ACTIVATED） | 不可见（L0 DEACTIVATED） | L1 proxy 替代整个区域（含植被位置） |
| 远距离（L2 ACTIVATED） | 不可见 | L2 proxy 替代更大区域 |

植被在远距离不需要单独表示 —— HLOD proxy 已经从整体视觉上覆盖了该区域。

#### 与 UE5 的对比

UE5 提供更灵活的 HLOD 植被策略：

| 策略 | 说明 | 适用场景 |
|---|---|---|
| **默认排除**（Default） | 植被不参与 HLOD 生成（需显式开启） | 大多数项目 |
| **Instancing Layer** | 远处保持实例化，减少实例数量 | 需要远距离仍能辨识单棵树 |
| **Merged Mesh** | 合并为单个 mesh | 极远距离 |
| **Approximated Mesh** | Nanite 自动简化 | Nanite 树木 |

UrhoX 当前采用与 UE5 默认行为一致的方案（植被不参与 HLOD proxy 合并）。
未来可扩展 Instancing HLOD Layer，在 L1/L2 中保留降采样的 HISM 实例。

### 3.6 多级 HLOD 层级构建

```
Level 0: 原始场景物体（不做处理）
Level 1: 聚类 → 每 cluster 生成 1 个 proxy（~10:1 简化）
Level 2: 将 Level 1 的 proxy 再聚类 → 更大的 proxy（~5:1 简化）
Level N: 递归，直到整个 Cell 只剩 1 个 proxy
```

```cpp
// engine/Source/Tools/HLODBuildLib/HierarchyBuilder.h

struct HLODBuildSettings
{
    unsigned numLevels = 2;                 // HLOD 层级数
    SharedPtr<IClusteringStrategy> clusteringStrategy;  // 聚类策略
    Vector<ProxySettings> levelSettings;    // 每层的 proxy 设置

    // 每层的聚类网格大小（递增）
    // Level 1: 64m, Level 2: 256m, Level 3: 1024m ...
    Vector<float> clusterGridSizes;
};

struct HLODBuildResult
{
    struct ProxyInfo
    {
        unsigned level;
        SharedPtr<Model> model;
        SharedPtr<Material> material;
        SharedPtr<Image> atlas;
        BoundingBox bounds;
        float switchDistance;               // 切换到此 proxy 的最小距离
        Vector<unsigned> sourceNodeIDs;     // 此 proxy 代表的原始 Node
    };
    Vector<ProxyInfo> proxies;
};

class HierarchyBuilder
{
public:
    bool Build(
        Scene* scene,                       // 源场景
        const BoundingBox& regionBounds,    // 构建区域（= Cell bounds）
        const HLODBuildSettings& settings,
        HLODBuildResult& result
    );

    void SetProgressCallback(void (*func)(float progress, const String& stage));

private:
    // Level 1: 从场景收集 StaticModel Node → 聚类 → 逐 cluster 生成 proxy
    // Level 2: 将 Level 1 的 proxy 当作输入 → 更大粒度聚类 → 生成更大 proxy
    // ...递归
};
```

### 3.7 切换距离计算

复用引擎已有的 LOD 距离公式（`engine/Source/Tools/MeshSimplifier/LODGroup.h`）：

```cpp
// 已有函数
float CalculateViewDistance(float maxDeviation, float pixelError);
// viewDistance = (maxDeviation * 640) / max(pixelError, 1)

// HLOD proxy 的切换距离 = 基于 cluster 包围盒大小 + 简化误差
float ComputeHLODSwitchDistance(const BoundingBox& clusterBounds, float simplifyError)
{
    float radius = clusterBounds.Size().Length() * 0.5f;
    // 在 proxy 的几何偏差占屏幕 < 2px 时切换
    float pixelError = 2.0f;
    return CalculateViewDistance(simplifyError, pixelError);
}
```

---

## 四、HLOD 运行时系统

### 4.1 设计原则

- **三态 Cell 模型**：UNLOADED → LOADED（在内存不可见）→ ACTIVATED（可见），参考 UE5
- **Phase 1（距离驱动）只管内存**：UNLOADED ↔ LOADED，**永远不碰 ACTIVATED Cell**
- **Phase 2（状态驱动）管可见性**：LOADED ↔ ACTIVATED，**所有可见性切换都是分组原子操作**
- **Loading Range 重叠**：HLOD 预加载到 LOADED 状态待命，切换时零延迟
- 不引入 HLODComponent，proxy 直接使用 **StaticModel**
- 异步回调参考 `InstanceManager.h/cpp` 中 `AsyncLoadingBlock` 的 `Delegate_ResourceAsyncLoading` 用法

### 4.2 Cell 状态机

所有 Grid Level 的 Cell 共用同一状态机：

```
                BeginLoad()           FinishLoad()          ActivateCell()
  UNLOADED ─────────────→ LOADING ──────────────→ LOADED ──────────────→ ACTIVATED
     ↑                      │                       │ ↑                     │
     │               CancelLoading()           Unload() DeactivateCell()   │
     │                      ↓                       │                       │
     ←──── CANCELLING ←─────┘                       │                       │
     │   (回调全部完成                                │                       │
     │    → UNLOADED)                               │                       │
     ←──────────────────────────────────────────────┘                       │
                                                                            │
     注意：ACTIVATED 没有直接到 UNLOADED 的路径！                              │
     必须先 DeactivateCell → LOADED，再由 Phase 1 Unload → UNLOADED           │
```

关键路径：
- **加载**：UNLOADED → LOADING → LOADED（在内存但不可见，Node 已实例化）
- **激活**：LOADED → ACTIVATED（Node 添加到 Scene，零开销，由 Phase 2 分组触发）
- **隐藏**：ACTIVATED → LOADED（Node 从 Scene 移除，保留在内存，由 Phase 2 分组触发）
- **卸载**：LOADED → UNLOADED（释放资源，仅在 LOADED 状态时 Phase 1 允许卸载）
- **禁止**：ACTIVATED → UNLOADED（~~直接卸载可见 Cell~~，会导致空洞）

### 4.3 核心流程

#### 4.3.1 WorldCell 的 Delegate 实现

每个 WorldCell 实现 `Delegate_ResourceAsyncLoading` 接口，自身就是回调对象：

```cpp
void WorldCell::Invoke(Resource* resource, AsyncLoadState state, AsyncLoadError error)
{
    if (state == ASYNC_QUEUED || error == AsyncLoadError::IN_LOADING_QUEUE)
    {
        ++totalResourceCount_;
        return;
    }

    if (state == ASYNC_DONE)
    {
        if (error == AsyncLoadError::NONE && resource)
            loadedResources_.Push(SharedPtr<Resource>(resource));

        ++currentLoadingResCount_;

        if (currentLoadingResCount_ == totalResourceCount_)
        {
            if (state_ == CANCELLING)
            {
                owner_->ReleaseCellResources(this);
                state_ = UNLOADED;
            }
            else if (state_ == LOADING)
                owner_->FinishLoad(this);
        }
    }
}
```

#### 4.3.2 加载发起

```cpp
void WorldPartitionComponent::BeginLoad(WorldCell* cell)
{
    cell->state_ = WorldCell::LOADING;
    cell->totalResourceCount_ = 0;
    cell->currentLoadingResCount_ = 0;
    cell->loadedResources_.Clear();

    auto* cache = GetSubsystem<ResourceCache>();
    for (const auto& res : cell->resources_)
        cache->BackgroundLoadResource(res.type_, res.name_, false, nullptr, cell);
}
```

#### 4.3.3 取消加载

```cpp
void WorldPartitionComponent::CancelLoading(WorldCell* cell)
{
    auto* cache = GetSubsystem<ResourceCache>();
    for (const auto& res : cell->resources_)
        cache->RemoveBackgroundLoadResourceDelegate(res.type_, res.name_, cell);

    if (cell->currentLoadingResCount_ == cell->totalResourceCount_)
    {
        ReleaseCellResources(cell);
        cell->state_ = WorldCell::UNLOADED;
    }
    else
    {
        cell->state_ = WorldCell::CANCELLING;
    }
}
```

#### 4.3.4 组装 → LOADED（在内存但不可见）

```cpp
void WorldPartitionComponent::FinishLoad(WorldCell* cell)
{
    // 从 Cell 描述文件同步实例化 Node 树（所有资源已在 cache，无 I/O）
    // 注意：只实例化，不添加到 Scene → 不可见
    cell->rootNode_ = InstantiateCellScene(cell->sceneDataPath_);
    cell->state_ = WorldCell::LOADED;
    // 可见性由 UpdateVisibility() 在同一帧内决定
}
```

#### 4.3.5 激活 / 隐藏（可见性切换）

```cpp
void WorldPartitionComponent::ActivateCell(WorldCell* cell)
{
    // LOADED → ACTIVATED：将 Node 添加到 Scene → Drawable 注册到 Octree → 可见
    GetScene()->GetChild("WorldRoot")->AddChild(cell->rootNode_);
    cell->state_ = WorldCell::ACTIVATED;
}

void WorldPartitionComponent::DeactivateCell(WorldCell* cell)
{
    // ACTIVATED → LOADED：从 Scene 移除 → Octree 注销 → 不可见，但保留在内存
    if (cell->rootNode_)
        cell->rootNode_->Remove();
    cell->state_ = WorldCell::LOADED;
}
```

**ActivateCell / DeactivateCell 的开销极低**：只是 Scene 树操作 + Octree 注册/注销，无 I/O、无资源加载。因此可在同一帧内对多个 Cell 做原子切换。

#### 4.3.6 卸载与资源释放

```cpp
void WorldPartitionComponent::Unload(WorldCell* cell)
{
    if (cell->state_ == WorldCell::LOADING)
    {
        CancelLoading(cell);
        return;
    }

    // ★ 断言：Unload 只允许在 LOADED（不可见）状态调用
    // ACTIVATED Cell 必须先通过 Phase 2 的 DeactivateCell → LOADED，才能被 Unload
    // 直接 Unload ACTIVATED Cell 会导致空洞（HLOD 可能还没接管该区域）
    assert(cell->state_ == WorldCell::LOADED);

    // 释放 Node
    cell->rootNode_.Reset();
    ReleaseCellResources(cell);
    cell->state_ = WorldCell::UNLOADED;
}

void WorldPartitionComponent::ReleaseCellResources(WorldCell* cell)
{
    auto* cache = GetSubsystem<ResourceCache>();
    cache->ReleaseResourcesFast(cell->loadedResources_);
    cell->loadedResources_.Clear();
    cell->totalResourceCount_ = 0;
    cell->currentLoadingResCount_ = 0;
}
```

### 4.4 ResourceCache 资源释放

**问题**：`node->Remove()` + `SharedPtr::Reset()` 只销毁 Node 树和组件，但 Model、Material、Texture2D 等资源仍被 `ResourceCache` 的 `SharedPtr<Resource>` 持有，不会释放内存。

**ResourceCache 的存储结构**：
```cpp
// ResourceCache 内部
HashMap<StringHash/*type*/, ResourceGroup> resourceGroups_;
struct ResourceGroup {
    unsigned long long memoryBudget_;       // 内存预算（0=无限制）
    HashMap<StringHash/*nameHash*/, SharedPtr<Resource>> resources_;  // 缓存的资源
};
```

**释放策略：`loadedResources_` 双重职责 + 内存预算兜底**

`WorldCell::loadedResources_`（`Vector<SharedPtr<Resource>>`）承担两个职责：

| 阶段 | 职责 | 说明 |
|---|---|---|
| 加载期间 | 保护引用 | 防止资源被其他 Cell 的卸载从 cache 中释放 |
| 卸载时 | 提供精确的资源列表 | 按列表定向从 cache 释放，无需遍历 Node 树或全量扫描 |

**卸载四步流程**（`ReleaseCellResources`）：

```
Step 1: node->Remove() + Reset()    → 组件析构，释放 Component 对资源的 SharedPtr
Step 2: 从 loadedResources_ 收集 type/name
Step 3: loadedResources_.Clear()     → 释放 Cell 持有的 SharedPtr → 专属资源 RefCount 降到 1
Step 4: cache->ReleaseResource()     → RefCount==1 的资源从 cache 移除，共享资源(>1)跳过
```

语义上等价于 UE5 GC："卸载后，回收没有任何人使用的资源"。但 UrhoX 的优势是**按清单定向释放**，复杂度 O(M)（M=Cell 资源数，几十~几百），不需要 UE5 那样的全量 GC 遍历。

**共享资源安全保障**：
- Cell A 和 Cell B 共享 `Textures/brick.png`
- Cell A 卸载 → Step 3 释放 Cell A 的 SharedPtr → RefCount 从 3 降到 2（cache + Cell B）
- Step 4 调用 `ReleaseResource(force=false)` → RefCount != 1 → 跳过，不释放
- Cell B 卸载 → RefCount 降到 1 → 释放

**内存预算作为安全兜底**：
```cpp
auto* cache = GetSubsystem<ResourceCache>();
cache->SetMemoryBudget(Model::GetTypeStatic(), 256 * 1024 * 1024);      // 256MB
cache->SetMemoryBudget(Texture2D::GetTypeStatic(), 512 * 1024 * 1024);  // 512MB
cache->SetMemoryBudget(Material::GetTypeStatic(), 64 * 1024 * 1024);    // 64MB
// 超出预算时 ResourceCache 自动按 LRU 淘汰最久未使用的资源
```

### 4.5 与 Octree 的集成

- `node->Remove()` 自动从 Octree 移除所有 Drawable
- 新 Node 添加到 Scene 后自动通过 `Drawable::OnSceneSet()` → `AddToOctree()` 注册
- proxy 的 `worldBoundingBox_` 覆盖整个 cluster 区域，确保不被错误剔除
- 全部操作在主线程，无线程安全问题

---

## 五、库目录结构

```
engine/Source/Tools/HLODBuildLib/
├── CMakeLists.txt
├── HLODBuildLib.h              // 公共头文件（汇总 include）
├── Clustering/
│   ├── IClusteringStrategy.h   // 聚类接口
│   ├── GridClustering.h        // Grid 聚类实现
│   └── GridClustering.cpp
├── MeshMerger.h                // Mesh 合并（VB/IB 拼接 + UV 重映射）
├── MeshMerger.cpp
├── MaterialBaker.h             // GPU Render-to-Texture 材质烘焙
├── MaterialBaker.cpp
├── AtlasBuilder.h              // UV Atlas 布局（Bin Packing）
├── AtlasBuilder.cpp
├── ProxyGenerator.h            // Proxy 生成（bake + 合并 + 简化）
├── ProxyGenerator.cpp
├── HierarchyBuilder.h          // 多级 HLOD 构建
└── HierarchyBuilder.cpp

Res/Shaders/BLGL/
└── screen_pos.sh               // 新增 EncodeGBufferBake 宏
```

### CMakeLists.txt

```cmake
# engine/Source/Tools/HLODBuildLib/CMakeLists.txt
if (NOT URHO3D_TOOLS OR WEB OR IOS OR ANDROID)
    return ()
endif ()

set (TARGET_NAME HLODBuildLib)

define_source_files (RECURSE GROUP)
setup_library (STATIC)

target_link_libraries (${TARGET_NAME} PUBLIC MeshSimplifier)
set_target_properties (${TARGET_NAME} PROPERTIES FOLDER "Tools")
```

UrhoXEditor 的 CMakeLists.txt 添加链接：
```cmake
target_link_libraries (${TARGET_NAME} ... HLODBuildLib)
```

### 运行时文件

```
engine/Source/Urho3D/Scene/WorldPartition.h
engine/Source/Urho3D/Scene/WorldPartition.cpp
```

---

## 六、HLOD 数据序列化格式

### 世界描述文件（WorldPartition.json）

描述所有 Grid Level 的配置：

```json
{
    "grids": [
        { "level": 0, "cellSize": 256, "loadingRange": 768,  "comment": "Actor Grid" },
        { "level": 1, "cellSize": 256, "loadingRange": 3000, "comment": "HLOD L1" },
        { "level": 2, "cellSize": 512, "loadingRange": 8000, "comment": "HLOD L2" },
        { "level": 3, "cellSize": 1024, "loadingRange": -1,  "comment": "HLOD L3 Always Loaded" }
    ]
}
```

注意：
- `loadingRange = -1` 表示 Always Loaded（始终在内存中）
- Loading Range 之间是**重叠**的，不是互斥的
- 配置参考 2.4 节 LoadingRange 配置指南
- 距离单位为米，度量方式为 Camera 到 Cell AABB 最近边界的距离

### Cell 描述文件（每个 Grid Level 独立目录）

所有 Grid Level 的 Cell 使用统一格式，区别仅在于内容（L0=独立物体，L1+=proxy）：

```
WorldData/
├── L0/                         # Actor Grid (256m cells)
│   ├── Cell_3_5.json
│   ├── Cell_3_5/
│   │   ├── scene.xml           # Node 树
│   │   ├── building_A.mdl
│   │   └── building_A.xml
│   └── ...
├── L1/                         # HLOD Layer 0 (256m cells)
│   ├── Cell_1_2.json
│   ├── Cell_1_2/
│   │   ├── scene.xml           # proxy Node
│   │   ├── proxy_opaque.mdl
│   │   ├── proxy_opaque.xml
│   │   └── proxy_opaque_diffuse.png
│   └── ...
└── L2/                         # HLOD Layer 1 (512m cells)
    └── ...
```

**Cell JSON 格式**（所有 Level 统一）：

```json
{
    "gridLevel": 0,
    "cellCoord": [3, 5],
    "worldBounds": { "min": [384, -100, 640], "max": [512, 200, 768] },
    "sceneData": "WorldData/L0/Cell_3_5/scene.xml",
    "resources": [
        { "type": "Model",     "name": "WorldData/L0/Cell_3_5/building_A.mdl" },
        { "type": "Material",  "name": "WorldData/L0/Cell_3_5/building_A.xml" },
        { "type": "Texture2D", "name": "Textures/Shared/brick_diffuse.png" },
        { "type": "Texture2D", "name": "Textures/Shared/brick_normal.png" }
    ]
}
```

L1 Cell（HLOD proxy）的 JSON 格式完全一致，只是内容不同：

```json
{
    "gridLevel": 1,
    "cellCoord": [1, 2],
    "worldBounds": { "min": [256, -100, 512], "max": [512, 200, 768] },
    "sceneData": "WorldData/L1/Cell_1_2/scene.xml",
    "resources": [
        { "type": "Model",     "name": "WorldData/L1/Cell_1_2/proxy_opaque.mdl" },
        { "type": "Material",  "name": "WorldData/L1/Cell_1_2/proxy_opaque.xml" },
        { "type": "Texture2D", "name": "WorldData/L1/Cell_1_2/proxy_opaque_diffuse.png" },
        { "type": "Texture2D", "name": "WorldData/L1/Cell_1_2/proxy_opaque_spec.png" },
        { "type": "Texture2D", "name": "WorldData/L1/Cell_1_2/proxy_opaque_normal.png" },
        { "type": "Texture2D", "name": "WorldData/L1/Cell_1_2/proxy_opaque_emissive.png" }
    ]
}
```

共享资源（如 `Textures/Shared/brick_diffuse.png`）可出现在多个 Cell 的 `resources` 列表中。卸载时 `ReleaseResourcesFast` 只释放 RefCount=1 的资源，共享资源安全。

---

## 七、UrhoX 引擎关键集成点

### 已有系统（复用）

| 能力 | 类 | 方法 | 文件 |
|---|---|---|---|
| Per-geometry LOD 数组 | `Model` | `geometries_[G][L]` | `Graphics/Model.h` |
| Per-Geometry 距离阈值 | `Geometry` | `SetLodDistance(float)` | `Graphics/Geometry.h` |
| 运行时 LOD 选择 | `StaticModel` | `CalculateLodLevels(int)` | `Graphics/StaticModel.cpp` |
| LOD 距离缩放 | `Camera` | `GetLodDistance(dist, scale, bias)` | `Graphics/Camera.h` |
| 空间查询 | `Octree` | `GetDrawables(OctreeQuery&)` | `Graphics/Octree.h` |
| Frustum 查询 | `FrustumOctreeQuery` | `TestOctant()` + `TestDrawables()` | `Graphics/OctreeQuery.h` |
| Drawable 注册 | `Drawable` | `OnSceneSet()` → `AddToOctree()` | `Graphics/Drawable.cpp` |
| 异步资源加载 | `ResourceCache` | `BackgroundLoadResource<T>(name)` | `Resource/ResourceCache.h` |
| Mesh 简化 | `MeshSimplifier` | `Simplify(targetVerts, targetTris, ...)` | `Tools/MeshSimplifier/` |
| LOD 屏幕尺寸公式 | 自由函数 | `ComputeLODAutoScreenSize()` | `Tools/MeshSimplifier/LODGroup.h` |
| 视距公式 | 自由函数 | `CalculateViewDistance(deviation, pixelError)` | `Tools/MeshSimplifier/LODGroup.h` |
| GPU Instanced Draw | `Geometry` | `DrawInstanced()` | `Graphics/Geometry.h` |
| Instance Transform 传递 | Shader | `iTexCoord4/5/6` = Matrix3x4 per instance | `Shaders/BLGL/transform.sh` |
| Batch 自动合组 | `BatchGroup` | 相同 Geometry+Material 合为 Instanced Draw | `Graphics/Batch.h` |
| Per-Instance 自定义数据 | `InstanceDataSetter` | 支持 per-instance float4 数据 | `Graphics/InstanceDataSetter.h` |
| 基础实例化合批 | `StaticModelGroup` | CPU 管理实例 Node，无层级剔除 | `Graphics/StaticModelGroup.h` |

### LOD 距离公式参考

```cpp
// StaticModel::UpdateBatches() 中:
float scale = worldBoundingBox.Size().DotProduct(DOT_SCALE);
float lodDistance = camera->GetLodDistance(distance, scale, lodBias);

// CalculateLodLevels() 中:
// 遍历 LOD 级别，找到第一个 lodDistance <= geometry->GetLodDistance() 的级别

// LODGroup.h 中:
// viewDistance = (maxDeviation * 640) / max(pixelError, 1)
```

---

---

## 十、植被实例化渲染系统（HISM）

### 10.1 问题与动机

传统方式：每株植被 = 1 个 Node + 1 个 StaticModel → 1 个 Drawable → Octree 逐个 Frustum Cull。

```
1000 棵树 → 1000 个 Drawable → CPU 每帧 1000 次包围盒测试 → 1000 个 draw call
```

HISM 方式：1000 棵树 → 1 个 HISMComponent → 内部 Cluster Tree 层级剔除 → 1~few draw call。

```
1000 棵树 → 1 个 HISMComponent
  → Cluster Tree: ~10 次包围盒测试（O(log N)）确定可见集
  → GPU Instancing: 可见实例一次 DrawIndexedInstanced
  → 每种 LOD 1 个 draw call
```

### 10.2 UrhoX 现有实例化能力

UrhoX 已有**完整的 GPU Instancing 基础设施**，可直接复用：

| 能力 | 类/文件 | 说明 |
|---|---|---|
| GPU Instance Draw | `Geometry::DrawInstanced()` | 已实现 DrawIndexedInstanced |
| Instance Transform | `iTexCoord4/5/6` (shader) | 3×float4 = Matrix3x4 per instance |
| Batch 自动合组 | `BatchGroup` + `BatchGroupKey` | 相同 Geometry+Material 自动合为 Instanced Draw |
| Per-Instance 数据 | `InstanceDataSetter` | 支持自定义 per-instance float4 数据 |
| 基础合批 | `StaticModelGroup` | CPU 管理实例 Node，共享 Geometry，但**无层级剔除** |
| Shader 支持 | `#ifdef INSTANCED` | Transform.glsl/hlsl 已处理 instance matrix |

**StaticModelGroup 的局限**：
- 无 Cluster Tree → 遍历所有实例做可见性判断 → O(N)
- 无 per-cluster LOD → 整个 Group 只有一个 LOD
- 无 per-instance distance culling → 远处实例仍然 draw
- 单 Geometry 限制 → 不支持多 LOD Model

**HISM 需要在此基础上增加**：
1. Cluster Tree（BVH 变种）→ O(log N) 层级剔除
2. Per-Cluster LOD 选择 → 不同距离不同模型精度
3. 动态可见实例列表 → 每帧只提交可见实例
4. Distance Culling → 超过 maxDistance 的实例不渲染

### 10.3 HISMComponent 设计

```cpp
// engine/Source/Urho3D/Graphics/HISMComponent.h

/// Cluster Tree 节点（固定大小，缓存友好）
struct HISMClusterNode
{
    BoundingBox bounds_;            // 该节点覆盖的所有实例的 AABB
    unsigned firstChild_;           // 分支节点: clusters_ 中第一个子节点索引
                                    // 叶节点: instances_ 中第一个实例索引
    unsigned short childCount_;     // 分支节点: 子节点数; 叶节点: 实例数
    bool isLeaf_;
};

/// 单个 LOD 级别的 Model
struct HISMLODLevel
{
    SharedPtr<Model> model_;        // 该 LOD 的 Model
    float maxDistance_;              // 超过此距离切到下一 LOD（0 = 最高精度，无限远 = 最低精度）
};

class URHO3D_API HISMComponent : public Drawable
{
    URHO3D_OBJECT(HISMComponent, Drawable);
public:
    explicit HISMComponent(Context* context);

    // ─── 配置 ───
    /// 设置实例共享的 Material
    void SetMaterial(Material* material);
    /// 设置 LOD Model 列表（从高精度到低精度）
    void SetNumLODLevels(unsigned num);
    void SetLODModel(unsigned level, Model* model);
    void SetLODMaxDistance(unsigned level, float distance);

    /// 最大渲染距离（超过完全不渲染）
    void SetCullDistance(float distance) { cullDistance_ = distance; }

    // ─── 实例管理 ───
    /// 批量设置所有实例（构建后调用 BuildClusterTree）
    void SetInstanceTransforms(const PODVector<Matrix3x4>& transforms);
    /// 单个增删（标记脏，需 Rebuild）
    unsigned AddInstance(const Matrix3x4& transform);
    void RemoveInstance(unsigned index);
    void SetInstanceTransform(unsigned index, const Matrix3x4& transform);
    unsigned GetNumInstances() const { return instanceTransforms_.Size(); }

    /// 构建 Cluster Tree（实例变更后调用）
    void BuildClusterTree();

    // ─── Drawable Override ───
    void UpdateBatches(const FrameInfo& frame) override;
    void UpdateGeometry(const FrameInfo& frame) override;
    unsigned GetNumOccluderTriangles() override { return 0; }

    static void RegisterObject(Context* context);

private:
    // ─── 实例数据 ───
    PODVector<Matrix3x4> instanceTransforms_;  // 所有实例的世界变换
    SharedPtr<Material> material_;
    Vector<HISMLODLevel> lodLevels_;           // LOD 0 = 最高精度
    float cullDistance_ = 200.0f;

    // ─── Cluster Tree ───
    Vector<HISMClusterNode> clusterNodes_;     // 紧凑数组存储
    PODVector<unsigned> leafInstanceIndices_;   // 叶节点引用的实例索引
    unsigned rootNodeIndex_ = 0;
    bool clusterTreeDirty_ = true;

    // ─── 每帧剔除结果 ───
    struct LODBatch
    {
        unsigned lodLevel;
        PODVector<unsigned> instanceIndices;   // 该 LOD 的可见实例索引
    };
    Vector<LODBatch> frameLODBatches_;

    // ─── 构建方法 ───
    void BuildClusterRecursive(
        unsigned* sortedIndices, unsigned count,
        unsigned depth, unsigned maxInstancesPerLeaf);
    BoundingBox ComputeInstancesBounds(
        const unsigned* indices, unsigned count) const;

    // ─── 每帧剔除方法 ───
    void CullClusterTree(const FrameInfo& frame);
    void CullRecursive(
        unsigned nodeIndex,
        const Frustum& frustum,
        const Vector3& cameraPos);
};
```

### 10.4 Cluster Tree 构建

离线（或加载时）构建，采用**自顶向下空间中值分割**（类似 BVH）：

```
输入: N 个实例的 Transform + BoundingBox

BuildClusterTree():
  1. 计算所有实例的总 AABB → root node
  2. 递归分割:
     if (count <= maxInstancesPerLeaf)  // 默认 64
         创建叶节点, 存储实例索引列表
     else
         选择最长轴（X 或 Z）
         按该轴的实例中心坐标排序
         从中间分割为两半
         递归构建左子树 + 右子树
         创建分支节点

复杂度: O(N log N)  （排序主导）
空间: O(N) 节点数   （二叉树，叶节点 ~N/64 个）
```

```cpp
void HISMComponent::BuildClusterTree()
{
    unsigned count = instanceTransforms_.Size();
    if (count == 0)
        return;

    clusterNodes_.Clear();
    leafInstanceIndices_.Clear();

    // 初始化排序索引
    PODVector<unsigned> sortedIndices(count);
    for (unsigned i = 0; i < count; ++i)
        sortedIndices[i] = i;

    // 递归构建
    rootNodeIndex_ = 0;
    BuildClusterRecursive(sortedIndices.Buffer(), count, 0, 64);

    // 更新 Drawable 的 worldBoundingBox_（Octree 用）
    worldBoundingBox_ = clusterNodes_[rootNodeIndex_].bounds_;
    clusterTreeDirty_ = false;
}

void HISMComponent::BuildClusterRecursive(
    unsigned* indices, unsigned count,
    unsigned depth, unsigned maxPerLeaf)
{
    unsigned nodeIndex = clusterNodes_.Size();
    clusterNodes_.Resize(nodeIndex + 1);
    HISMClusterNode& node = clusterNodes_[nodeIndex];

    node.bounds_ = ComputeInstancesBounds(indices, count);

    if (count <= maxPerLeaf)
    {
        // 叶节点
        node.isLeaf_ = true;
        node.firstChild_ = leafInstanceIndices_.Size();
        node.childCount_ = (unsigned short)count;
        for (unsigned i = 0; i < count; ++i)
            leafInstanceIndices_.Push(indices[i]);
        return;
    }

    // 选择最长轴分割
    Vector3 size = node.bounds_.Size();
    int splitAxis = (size.x_ >= size.z_) ? 0 : 2;  // XZ 平面

    // 按该轴排序
    Sort(indices, indices + count, [&](unsigned a, unsigned b)
    {
        Vector3 ca = instanceTransforms_[a].Translation();
        Vector3 cb = instanceTransforms_[b].Translation();
        return (splitAxis == 0) ? (ca.x_ < cb.x_) : (ca.z_ < cb.z_);
    });

    unsigned mid = count / 2;
    node.isLeaf_ = false;
    node.firstChild_ = clusterNodes_.Size();  // 下一个待分配的索引
    node.childCount_ = 2;

    BuildClusterRecursive(indices, mid, depth + 1, maxPerLeaf);
    BuildClusterRecursive(indices + mid, count - mid, depth + 1, maxPerLeaf);
}
```

**Cluster 粒度选择**：

| maxInstancesPerLeaf | 树深度(10000实例) | 剔除精度 | 构建时间 |
|---|---|---|---|
| 32 | ~9 层 | 高（粒度细） | 较慢 |
| **64** | ~8 层 | **推荐平衡** | 中等 |
| 128 | ~7 层 | 低（粒度粗） | 快 |

### 10.5 运行时层级剔除

每帧 `UpdateBatches()` 中执行：

```cpp
void HISMComponent::UpdateBatches(const FrameInfo& frame)
{
    if (clusterNodes_.Empty())
        return;

    // 1. 层级剔除 → 填充 frameLODBatches_
    CullClusterTree(frame);

    // 2. 为每个 LOD 创建 BatchGroup
    distance_ = frame.camera_->GetDistance(GetWorldBoundingBox().Center());
    for (auto& lodBatch : frameLODBatches_)
    {
        if (lodBatch.instanceIndices.Empty())
            continue;

        Geometry* geometry = lodLevels_[lodBatch.lodLevel].model_->GetGeometry(0, 0);
        // 通过引擎现有 BatchGroup 机制提交 Instanced Draw
        // BatchGroup 按 (geometry, material, pass) 分组
        // 可见实例的 Transform 写入 instance buffer
    }
}
```

```cpp
void HISMComponent::CullClusterTree(const FrameInfo& frame)
{
    // 清空上一帧结果
    frameLODBatches_.Resize(lodLevels_.Size());
    for (auto& batch : frameLODBatches_)
        batch.instanceIndices.Clear();

    const Frustum& frustum = frame.camera_->GetFrustum();
    Vector3 cameraPos = frame.camera_->GetNode()->GetWorldPosition();

    CullRecursive(rootNodeIndex_, frustum, cameraPos);
}

void HISMComponent::CullRecursive(
    unsigned nodeIndex,
    const Frustum& frustum,
    const Vector3& cameraPos)
{
    const HISMClusterNode& node = clusterNodes_[nodeIndex];

    // 1. Frustum Culling: 整个 cluster 是否在视锥内
    Intersection result = frustum.IsInside(node.bounds_);
    if (result == OUTSIDE)
        return;  // 整个分支裁掉

    // 2. Distance Culling: 整个 cluster 是否超过最大渲染距离
    float clusterDist = node.bounds_.DistanceToPoint(cameraPos);
    if (clusterDist > cullDistance_)
        return;  // 整个分支裁掉

    if (node.isLeaf_)
    {
        // 叶节点: 确定 LOD 级别，添加实例
        unsigned lodLevel = 0;
        for (unsigned i = 0; i < lodLevels_.Size() - 1; ++i)
        {
            if (clusterDist > lodLevels_[i].maxDistance_)
                lodLevel = i + 1;
        }

        if (result == INSIDE)
        {
            // 整个 cluster 完全在视锥内，无需逐实例测试
            for (unsigned i = 0; i < node.childCount_; ++i)
            {
                unsigned instIdx = leafInstanceIndices_[node.firstChild_ + i];
                frameLODBatches_[lodLevel].instanceIndices.Push(instIdx);
            }
        }
        else  // INTERSECTS
        {
            // Cluster 与视锥相交，逐实例测试
            for (unsigned i = 0; i < node.childCount_; ++i)
            {
                unsigned instIdx = leafInstanceIndices_[node.firstChild_ + i];
                // 简化: 用实例位置做点测试（不精确但极快）
                Vector3 pos = instanceTransforms_[instIdx].Translation();
                if (frustum.IsInsideFast(BoundingBox(pos, pos)))  // 或 sphere test
                    frameLODBatches_[lodLevel].instanceIndices.Push(instIdx);
            }
        }
    }
    else
    {
        // 分支节点: 递归子节点
        for (unsigned i = 0; i < node.childCount_; ++i)
            CullRecursive(node.firstChild_ + i, frustum, cameraPos);
    }
}
```

**性能分析**（10000 棵树，maxPerLeaf=64）：

```
Cluster 节点数: ~312 (= 10000/64 叶 + ~156 内部)
最坏 Frustum test: ~312 次 BoundingBox 测试
典型（60° FOV）: ~80 次（大部分分支整体 OUTSIDE 被裁掉）

对比逐物体: 10000 次 → ~80 次 = 125x 加速
```

### 10.6 与 World Partition 的集成

#### 放置植被（树木、大灌木）

跟随 World Partition Cell 流式，但渲染通过 HISM：

```
离线构建时:
  对每个 L0 Cell:
    收集 Cell 内所有树木 Node → 按树种分组
    每种树 → 1 个 HISMComponent 描述文件（transforms + LOD models）

运行时:
  Cell ACTIVATED → 实例化 HISMComponent → BuildClusterTree → 注册 Octree
  Cell LOADED    → HISMComponent 移出 Scene
  Cell UNLOADED  → 释放

Cell 描述文件 (scene.xml) 中:
  <node>
    <component type="HISMComponent">
      <attribute name="Material" value="Materials/TreeOak.xml" />
      <attribute name="LOD Models" value="Models/TreeOak_LOD0.mdl;Models/TreeOak_LOD1.mdl;Models/TreeOak_LOD2.mdl" />
      <attribute name="LOD Distances" value="50;100;200" />
      <attribute name="Cull Distance" value="200" />
      <attribute name="Instance Transforms" value="..." />  <!-- 二进制或引用外部文件 -->
    </component>
  </node>
```

**一个 128m Cell 的树木 draw call**：
- 假设 3 种树，每种 ~100 棵 → 3 个 HISMComponent → 3~9 draw call（每种树每 LOD 1 个）
- 对比原来 300 个独立 StaticModel → 300 draw call
- **减少 30~100 倍 draw call**

#### 地表覆盖（草丛）—— 独立流式

地表草丛**不走 World Partition Cell**，有独立的距离驱动系统：

```
草丛特点:
  - 渲染距离极短 (40-50m)
  - 密度极高 (每 m² 数株)
  - Camera 快速移动时频繁创建/销毁

方案:
  - 按 Landscape Subsection（如 32m × 32m）管理
  - 每个 Subsection 一个 HISMComponent
  - Camera 移动 → 新 Subsection 进入 50m 范围 → 创建 HISM + BuildClusterTree
  - 旧 Subsection 离开范围 → 销毁 HISM
  - 与 World Partition 完全独立
```

这部分作为未来扩展，当前版本优先实现 World Partition + HLOD + 树木 HISM。

### 10.7 LOD 配置参考

| 植被类型 | LOD 0 距离 | LOD 1 距离 | LOD 2 距离 | Cull 距离 | 每实例三角形(LOD0) |
|---|---|---|---|---|---|
| 草 | 15m | 30m | — | 50m | 48-114 |
| 小灌木 | 30m | 60m | — | 80m | 200-500 |
| 中型树 | 50m | 100m | 150m | 200m | 1000-3000 |
| 大型景观树 | 80m | 150m | 250m | 350m | 2000-5000 |

**参考**：原神移动端整帧控制在 50-85 万三角形，草 48-114 三角形/株，GPU Instancing 每 draw call 32 组。

### 10.8 文件结构

```
engine/Source/Urho3D/Graphics/
├── HISMComponent.h             // HISM 组件（Cluster Tree + GPU Instancing）
└── HISMComponent.cpp
```

不需要独立库，直接放在引擎 Graphics 模块中（与 StaticModel、StaticModelGroup 同级）。

---

## 十一、分阶段实现计划

### Phase 1: 基础框架（HLODBuildLib 骨架 + Grid 聚类）
- 创建 `HLODBuildLib/` 目录和 CMakeLists.txt
- 实现 `IClusteringStrategy` 接口
- 实现 `GridClustering`
- 单元测试：输入一组 BoundingBox → 输出 Cluster 分组

### Phase 2: 材质烘焙 + Mesh 合并
- 实现 `AtlasBuilder`（Bin Packing）
- 实现 `MaterialBaker`（GPU Render-to-Texture，EncodeGBufferBake）
- 实现 `MeshMerger`（VB/IB 合并 + UV 重映射 + 世界空间变换）
- 测试：合并 N 个 StaticModel → 1 个 Model + 4 张 Atlas

### Phase 3: 多级 HLOD 构建
- 实现 `ProxyGenerator`（bake + 合并 + 简化）
- 实现 `HierarchyBuilder`（多级独立 Grid 构建）
  - Level 0 Grid: 原始物体按 cellSize 划分
  - Level 1 Grid: 将 L0 Cell 内物体生成 proxy，按更大 cellSize 划分
  - Level N Grid: 将 L(N-1) 的 proxy 再聚合
- 输出每个 Grid Level 的 Cell 描述文件 + 资源

### Phase 4: 运行时 WorldPartitionComponent
- 实现 `WorldPartitionComponent`（多级 StreamingGrid + 统一 WorldCell）
- 三态 Cell 状态机（UNLOADED → LOADING → LOADED → ACTIVATED, CANCELLING）
  - **ACTIVATED → UNLOADED 路径禁止**：必须先 DeactivateCell → LOADED，再 Unload → UNLOADED
- Phase 1: 距离驱动**内存管理**（Loading Range 重叠，**只管 UNLOADED ↔ LOADED，不碰 ACTIVATED**）
- Phase 2: 状态驱动**可见性切换**（**分组原子操作**，同一 HLOD Cell 的所有源 Cell 同时激活/隐藏）
  - Camera 靠近: 所有源 Cell LOADED → 原子切换（激活全部源 Cell + 隐藏 HLOD）
  - Camera 远离: 任一源 Cell 超出 range → 原子切换（隐藏全部源 Cell + 激活 HLOD）
  - 无 HLOD 覆盖的 L0 Cell: 自动激活（HasParentHLOD 判断）
- `Delegate_ResourceAsyncLoading` 回调（参考 InstanceManager）
- 加载中取消（CANCELLING 状态 + RemoveBackgroundLoadResourceDelegate）
- ResourceCache 定向释放（loadedResources_ + ReleaseResourcesFast）

### Phase 5: HISM 植被实例化
- 实现 `HISMComponent`（继承 Drawable）
- Cluster Tree 构建（自顶向下空间中值分割）
- 运行时层级 Frustum Culling（O(log N)）
- Per-Cluster LOD 选择
- 与引擎 BatchGroup 系统集成（GPU Instanced Draw）
- 与 World Partition Cell 集成（树木跟随 Cell 流式）
- 测试：10000 棵树 → 验证 draw call 减少、CPU 剔除时间

### Phase 6: Editor 集成
- UrhoXEditor 中添加 HLOD Build Panel
- 多级 Grid 配置界面（每级 cellSize / loadingRange）
- 聚类策略选择、参数调整、Atlas 大小等
- HISM 植被刷（导入植被分布 → 生成 HISM 描述）
- 构建进度显示 + 构建结果预览

---

## 十二、验证方案

1. **Grid 聚类测试**: 构造 100 个随机分布的 BoundingBox → 验证 cluster 分组合理
2. **Atlas 构建测试**: 合并 10 种不同纹理 → 验证 atlas 无重叠、UV 映射正确
3. **Mesh 合并测试**: 合并 5 个 StaticModel → 验证顶点/索引正确、世界空间位置正确
4. **Proxy 简化测试**: 合并后 mesh 简化到 10% → 验证外形可接受
5. **多级 Grid 构建测试**: 构建 L0/L1/L2 Grid → 验证每级 Cell 覆盖正确、proxy 递归聚合正确
6. **三态切换测试**: Cell LOADED（不可见）→ ACTIVATED（可见）→ LOADED → 验证 Node 正确添加/移除 Scene
7. **靠近原子切换测试**: Camera 靠近 → 4 个 L0 Cell 异步加载完成时间不同 → 验证全部 LOADED 前 L1 proxy 持续显示，全部 LOADED 后同帧原子切换（无重叠闪烁）
8. **远离原子切换测试**: Camera 远离 → 任一 L0 Cell 超出 loadingRange → 验证整组 L0 同帧 DeactivateCell + L1 ActivateCell（无空洞）
9. **Phase 1 不碰 ACTIVATED 测试**: L0 Cell 超出 loadingRange 但仍 ACTIVATED → 验证 Phase 1 不卸载它（由 Phase 2 处理）
10. **四角覆盖测试**: Camera 靠近 L2 Cell 一角 → 验证 4 个 L1 Cell 全部 LOADED + ACTIVATED → L2 安全 Deactivate
11. **级联切换测试**: 游戏启动 → L3 ACTIVATED → L2 全部 LOADED → 原子切换 → L1 全部 LOADED → 原子切换 → L0 全部 LOADED → 原子切换 → 验证逐步细化无闪烁
12. **加载取消测试**: Camera 快速移动 → 验证 CANCELLING 状态正确处理，无资源泄漏
13. **共享资源测试**: 多 Cell 共享纹理 → 验证卸载不会误释放
14. **LoadingRange 约束验证**: 验证每级 LoadingRange >= 上级 CellSize × √2
15. **Draw call 稳定性**: 任意视距下统计 ACTIVATED Cell 数和 draw call → 验证数量恒定
16. **HISM Cluster Tree 构建测试**: 10000 个实例 → 验证树结构正确、叶节点大小合理
17. **HISM 层级剔除测试**: 正面/背面/侧面视角 → 验证可见实例数合理、无漏剔除
18. **HISM LOD 切换测试**: Camera 前进/后退 → 验证 LOD 平滑切换、无闪烁
19. **HISM Draw Call 测试**: 10000 棵树 3 种树种 → 验证 draw call = 树种数 × LOD 数（~9），非 10000
20. **HISM + World Partition 集成测试**: Cell 加载/卸载 → 验证 HISM 实例正确创建/销毁

---

*Created: 2026-02-27*
