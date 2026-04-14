---
summary: "TileTerrain multi-texture blending using ID+Weight Control Map approach inspired by Delta Force GDC 2025 and Terrain3D"
related_paths:
  - engine/Source/Urho3D/TileTerrain/**
last_updated: "2026-04-02"
---

# TileTerrain 地形混合材质设计：ID+Weight Control Map 方案

## 一、背景与动机

当前 TileTerrain 系统中，所有 sub-chunk 共享同一个 Material，地表纹理外观单一。需要实现地形多纹理混合，让不同区域（草地、泥土、岩石等）拥有不同的地表外观，并在交界处平滑过渡。

本方案参考三角洲行动（Delta Force）在 GDC 2025 分享的 ID+Weight 地形材质方案，以及 Terrain3D 开源引擎的 Control Map Shader 实现。

### 参考资料

- [Delta Force GDC 2025: Performant High-Quality Terrain and Biome Technology](https://media.gdcvault.com/gdc2025/Slides/Jiao_Hang_Delta+Force+Performant.pdf)
- [GameRes - GDC 2025《三角洲行动》地形技术总结](https://www.gameres.com/911914.html)
- [Terrain3D Shader Design Documentation](https://terrain3d.readthedocs.io/en/latest/docs/shader_design.html)

---

## 二、核心架构：几何与材质分离

地形的**几何形状**和**纹理外观**由两套独立数据决定：

| 层 | 数据来源 | 决定什么 |
|----|---------|---------|
| **Tileset** | 瓦片匹配算法 | 网格形状（平面/斜坡/墙面） |
| **Control Map** | 纹理笔刷绘制 | 每像素的纹理 layer ID + 混合权重 |

所有 tileset 共用**同一个** Terrain Blend Material（同一 Shader），不同地表外观的差异完全编码在 Control Map 纹理中。

---

## 三、为什么不能把 Layer ID 存在顶点属性中

### 3.1 问题

最直觉的方案是：每顶点存储 `(bottomLayerID, topLayerID, blendWeight)`，用 Vertex Color 或 UV2 传入 Shader。

**这是错误的**。原因：GPU 光栅化器会对所有顶点属性做**线性插值**。Layer ID 是离散的整数索引，线性插值会产生无意义的中间值：

```
顶点 A: bottomID = 3 (草地)
顶点 B: bottomID = 7 (岩石)
中间像素: bottomID = 5.0 → 采样到"泥土"纹理层 → 完全错误！
```

这会导致三角形内部出现错误的纹理条带和硬边。

### 3.2 `flat`/`nointerpolation` 也不可行

HLSL 的 `nointerpolation` / GLSL 的 `flat` 修饰符可以禁止插值，但它会让整个三角形使用 provoking vertex 的值，导致**三角形级别的色块**（每个三角形是纯色）。这不是我们想要的平滑过渡效果。

### 3.3 正确方案：Control Map 纹理 + texelFetch

把 ID+Weight 数据存储在一张**纹理**中（Control Map），在 Pixel Shader 中用 `texelFetch()`（无硬件插值的点采样）读取 4 个相邻 texel，然后**手动**进行双线性插值——只插值权重，不插值 ID。

这是 Delta Force 和 Terrain3D 共同采用的方案。

---

## 四、Control Map 数据格式

### 4.1 TerrainWeightMap（CPU 端数据结构）

```cpp
struct TerrainWeightMap
{
    unsigned width_;       // 网格宽度 = terrain tile 列数 × 4 + 1
    unsigned height_;      // 网格高度 = terrain tile 行数 × 4 + 1
    float gridSpacing_;    // 采样间距 = tileSize / 4 = 0.64m
    Vector2 origin_;       // 左下角世界坐标

    PODVector<unsigned char> bottomID_;  // 底层 layer ID (0~31)
    PODVector<unsigned char> topID_;     // 上层 layer ID (0~31)
    PODVector<unsigned char> weight_;    // 混合权重 (0~255, 映射 0.0~1.0)
};
```

- **分辨率**：每个平面 tile 是 4×4 grid，间距 0.64m。对于 768×768 的地图，Control Map 尺寸为 3073×3073。
- **每采样点**：存储 2 个 layer ID + 1 个混合权重（3 bytes）。
- **初始状态**：全部 `bottomID=0, topID=0, weight=0`（纯 layer 0）。
- 底层权重隐式为 `1 - weight/255`，无需额外存储。

### 4.2 GPU 纹理格式

Bake 到 RGBA8 纹理（Control Map Texture）：

| 通道 | 内容 | 范围 |
|------|------|------|
| R | bottomID / 255.0 | 0~31 → 0.0~0.122 |
| G | topID / 255.0 | 0~31 → 0.0~0.122 |
| B | weight / 255.0 | 0~255 → 0.0~1.0 |
| A | 保留 | 0 |

**采样模式**：必须设为 **Nearest/Point**（`filter="nearest"`）。**绝不能**使用 Bilinear，否则硬件会插值 ID 通道。

### 4.3 二进制序列化格式（`.bin`）

```
Offset  Size  Content
0       4     Magic: "TWMB"
4       4     Version: 1
8       4     width (unsigned)
12      4     height (unsigned)
16      4     gridSpacing (float)
20      4     originX (float)
24      4     originZ (float)
28      w*h   bottomID array (1 byte each)
28+w*h  w*h   topID array (1 byte each)
28+2wh  w*h   weight array (1 byte each)
```

---

## 五、Shader 实现

### 5.1 核心思路

1. **VS**：计算世界坐标，传递到 PS
2. **PS**：
   - 用世界坐标计算 Control Map 中的浮点 texel 坐标
   - `texelFetch()` 读取 4 个相邻 texel（无硬件插值）
   - 计算双线性权重因子 `(fx, fy)`
   - 从 8 个 ID（4 texel × 2 ID）中收集 unique ID（最多 3 个）
   - 对每个 unique ID 累加来自 4 个 texel 的权重贡献
   - 采样 Texture2DArray 3 次
   - 归一化混合

### 5.2 PS 核心实现

```glsl
uniform sampler2D sControlMap;          // RGBA8, nearest filter
uniform sampler2DArray sTerrainArray;   // 32 层纹理数组
uniform vec4 cControlMapParams;         // (originX, originZ, 1/gridSpacing, 0)
uniform vec2 cControlMapSize;           // (width, height) in texels
uniform vec2 cDetailTiling;             // 纹理平铺系数

void PS() {
    // ---- 1. texelFetch 4 个相邻 texel ----
    vec2 mapCoord = (worldPos.xz - cControlMapParams.xy) * cControlMapParams.z;
    ivec2 t00 = clamp(ivec2(floor(mapCoord)),     ivec2(0), ivec2(cControlMapSize) - 1);
    ivec2 t10 = clamp(t00 + ivec2(1, 0),          ivec2(0), ivec2(cControlMapSize) - 1);
    ivec2 t01 = clamp(t00 + ivec2(0, 1),          ivec2(0), ivec2(cControlMapSize) - 1);
    ivec2 t11 = clamp(t00 + ivec2(1, 1),          ivec2(0), ivec2(cControlMapSize) - 1);

    vec4 c00 = texelFetch(sControlMap, t00, 0);
    vec4 c10 = texelFetch(sControlMap, t10, 0);
    vec4 c01 = texelFetch(sControlMap, t01, 0);
    vec4 c11 = texelFetch(sControlMap, t11, 0);

    // ---- 2. 解码 ID 和 blend ----
    int b00 = int(c00.r * 255.0 + 0.5), t00 = int(c00.g * 255.0 + 0.5); float blend00 = c00.b;
    int b10 = int(c10.r * 255.0 + 0.5), t10 = int(c10.g * 255.0 + 0.5); float blend10 = c10.b;
    int b01 = int(c01.r * 255.0 + 0.5), t01 = int(c01.g * 255.0 + 0.5); float blend01 = c01.b;
    int b11 = int(c11.r * 255.0 + 0.5), t11 = int(c11.g * 255.0 + 0.5); float blend11 = c11.b;

    // ---- 3. min/mid/max 提取 3 个 unique ID ----
    int id0 = min(min(min(b00,t00), min(b10,t10)), min(min(b01,t01), min(b11,t11)));
    int id2 = max(max(max(b00,t00), max(b10,t10)), max(max(b01,t01), max(b11,t11)));
    int id1 = id0;  // 默认 = min（当只有 ≤2 种 unique 时）
    id1 = (b00 > id0 && b00 < id2) ? b00 : id1;
    id1 = (t00 > id0 && t00 < id2) ? t00 : id1;
    id1 = (b10 > id0 && b10 < id2) ? b10 : id1;
    // 找到一个就够，后续覆盖无害

    // ---- 4. 双线性因子 ----
    vec2 f = fract(mapCoord);
    float bw00 = (1.0 - f.x) * (1.0 - f.y);
    float bw10 = f.x         * (1.0 - f.y);
    float bw01 = (1.0 - f.x) * f.y;
    float bw11 = f.x         * f.y;

    // ---- 5. 优先级独占权重累加 ----
    float w0 = 0.0, w1 = 0.0, w2 = 0.0;

    #define ACCUM(val, weight)                          \
    {                                                   \
        float m0 = float(val == id0);                   \
        float m1 = (1.0 - m0) * float(val == id1);     \
        float m2 = 1.0 - m0 - m1;                      \
        w0 += m0 * weight;                              \
        w1 += m1 * weight;                              \
        w2 += m2 * weight;                              \
    }

    ACCUM(b00, bw00 * (1.0 - blend00))   // texel 00 bottom
    ACCUM(t00, bw00 * blend00)            // texel 00 top
    ACCUM(b10, bw10 * (1.0 - blend10))   // texel 10 bottom
    ACCUM(t10, bw10 * blend10)            // texel 10 top
    ACCUM(b01, bw01 * (1.0 - blend01))   // texel 01 bottom
    ACCUM(t01, bw01 * blend01)            // texel 01 top
    ACCUM(b11, bw11 * (1.0 - blend11))   // texel 11 bottom
    ACCUM(t11, bw11 * blend11)            // texel 11 top

    // ---- 6. 采样 Texture2DArray + 混合 ----
    vec2 detailUV = worldPos.xz * cDetailTiling;
    vec4 color = texture(sTerrainArray, vec3(detailUV, float(id0))) * w0
               + texture(sTerrainArray, vec3(detailUV, float(id1))) * w1
               + texture(sTerrainArray, vec3(detailUV, float(id2))) * w2;

    // 后续：光照计算同 TerrainBlend.glsl
}
```

整个 PS 核心：**4 次 texelFetch + 8 次 ACCUM（纯乘加）+ 3 次 Texture2DArray 采样**。没有 if/else，没有循环。

### 5.3 为什么需要"优先级独占"（关键陷阱）

**问题**：当 unique ID < 3 种时（例如只有 {0, 3}），min/mid/max 会提取出重复的 slot（id0=0, id1=0, id2=3）。如果用 naive 的 `eq()` 累加：

```glsl
// ❌ 错误：val=0 同时匹配 id0 和 id1，权重被计两次
w0 += float(val == id0) * weight;   // val=0 → +weight
w1 += float(val == id1) * weight;   // id1==id0==0 → 也 +weight！
w2 += float(val == id2) * weight;
```

**具体案例**：4 个 texel 只用 2 种 ID（0 和 3），正确混合应为 34% 草 + 66% 土。但 naive eq() 把 ID=0 的权重计了两次，归一化后变成 51% 草 + 49% 土 —— **17% 的绝对误差**。

**修复**：优先级门控，每个 val 只能匹配第一个相等的 slot：

```glsl
// ✓ 正确：slot 0 匹配后，slot 1 被门控关闭
float m0 = float(val == id0);                    // 优先匹配 slot 0
float m1 = (1.0 - m0) * float(val == id1);       // m0==1 时被乘以 0
float m2 = 1.0 - m0 - m1;                        // 剩余归 slot 2
```

| 场景 | id0,id1,id2 | val=0 | val=3 | val=5 |
|------|-------------|-------|-------|-------|
| 3 种 unique | 0, 3, 5 | m0=1,m1=0,m2=0 → w0 | m0=0,m1=1,m2=0 → w1 | m0=0,m1=0,m2=1 → w2 |
| 2 种 unique | 0, 0, 3 | m0=1,m1=**0**(门控),m2=0 → w0 only | m0=0,m1=0,m2=1 → w2 | — |
| 1 种 unique | 3, 3, 3 | — | m0=1,m1=**0**,m2=**0** → w0 only | — |

全部是乘法运算，无分支，GPU 友好。每个 val 恰好进入一个 slot，权重总和恒等于 1.0。

### 5.4 与 Delta Force 方案的对比

Delta Force 的地形是**规则网格**，PS 可以从世界坐标反推当前像素属于哪个三角形，从而 texelFetch 三角形 3 个顶点位置（而非 2×2 方块 4 个点）。这减少了 ID 数量从 8 → 6，采样从 4 → 3。

我们的 TileTerrain 是各种 tile 合并的**不规则 mesh**，PS 无法从世界坐标反推三角形顶点。因此采用 2×2 texelFetch 方案，代价是多 1 次 texelFetch 和稍多的 ALU。

| | Delta Force | 我们的方案 |
|--|-------------|-----------|
| 采样方式 | 3 个三角形顶点 | 4 个相邻 texel（2×2） |
| ID 数量 | 6 个 → ≤3 unique | 8 个 → ≤3 unique |
| texelFetch 次数 | 3 | 4 |
| Texture2DArray 采样 | 3 | 3 |
| 适用 mesh | 规则网格 | 任意 mesh |
| 离线约束范围 | 每三角形 | 每 2×2 texel 方块 |

---

## 六、纹理笔刷（PaintTexture）

### 6.1 接口

```cpp
/// 在世界坐标 (x, z) 位置、radius 圆内刷上 layerID。
/// 受影响的采样点：将 topID 设为 layerID，weight 按距离衰减。
/// 内部执行 ≤3 约束检查。
void PaintTexture(TerrainWeightMap& map,
                  float x, float z, float radius,
                  unsigned char layerID, float strength);
```

### 6.2 笔刷逻辑

```
for each sample point (sx, sz) in weightMap within radius of (x, z):
    dist = distance((sx, sz), (x, z))
    if dist > radius: skip
    falloff = 1.0 - (dist / radius)       // 线性衰减
    newWeight = lerp(current.weight, strength * 255, falloff)

    if current.bottomID == current.topID:
        // 当前为纯色 → 将新 layer 设为 topID
        current.topID = layerID
        current.weight = newWeight
    else if current.topID == layerID:
        // 已在混合同一 layer → 增强权重
        current.weight = max(current.weight, newWeight)
    else:
        // 已在混合不同 layer → 替换
        if current.weight > 128:
            current.bottomID = current.topID  // "烘入"当前 top
        current.topID = layerID
        current.weight = newWeight
```

### 6.3 ≤3 Unique ID 约束

**约束范围**：每个 2×2 texel 方块（因为 Shader 会同时读取 4 个相邻 texel）。

```
≤3 约束验证 pass:
for each 2×2 block in affected area:
    collect all (bottomID, topID) from 4 texels → up to 8 ID values
    unique_ids = deduplicate(8 values)
    if len(unique_ids) > 3:
        // 回退本次修改中权重最小的采样点
        revert weakest change in this block
```

### 6.4 CLI 命令

```bash
# 初始化空权重图
TileTerrainCLI.exe init-weightmap \
  --terrain terrain.json \
  --output terrain_weights.bin

# 刷纹理
TileTerrainCLI.exe paint-texture \
  --weightmap terrain_weights.bin \
  --pos 400,400 --radius 50 --layer 5 --strength 1.0 \
  --output terrain_weights.bin
```

---

## 七、纹理管理

### 7.1 Texture2DArray

- 全项目支持 **32 种地表材质**（5-bit ID 范围）
- 复用老编辑器的 `BaseColor_Terrain.xml`（82 层 KTX 纹理数组，512×512，ASTC4X4 压缩）
- 运行时只加载实际使用的层（按需填充 slot）

### 7.2 Material XML

```xml
<material>
    <technique name="Techniques/TileTerrainBlend.xml" />
    <texture unit="0" name="terrain_control.png" filter="nearest" />
    <texture unit="1" name="BaseColor_Terrain.xml" />
    <parameter name="ControlMapParams" value="originX originZ invGridSpacing 0" />
    <parameter name="ControlMapSize" value="width height" />
    <parameter name="DetailTiling" value="0.39 0.39" />
</material>
```

---

## 八、对现有系统的影响

### 8.1 不需要修改的模块

| 模块 | 原因 |
|------|------|
| TileTerrainDefs.h/cpp | Merge pipeline 不变，VB 仍是 Position+Normal+UV |
| TileTerrainChunk.cpp | VB layout 不变（32 bytes/vertex），IB 生成不变 |
| TileChunkBuildData | 异步构建不变 |
| TileSetMatcher | 瓦片匹配不变 |

### 8.2 需要新增/修改的模块

| 操作 | 路径 | 说明 |
|------|------|------|
| **新建** | `Lib/Data/TerrainWeightMap.h/cpp` | 权重图数据结构 |
| **新建** | `Lib/Data/TerrainWeightMapSerializer.h/cpp` | 二进制序列化 |
| **新建** | `Shaders/GLSL/TileTerrainBlend.glsl` | GLSL shader |
| **新建** | `Shaders/HLSL/TileTerrainBlend.hlsl` | HLSL shader |
| **新建** | `Techniques/TileTerrainBlend.xml` | Technique |
| **新建** | `Materials/TileTerrainBlend.xml` | Material 模板 |
| **修改** | `Lib/Operator/TerrainOperator.h/cpp` | PaintTexture 笔刷 |
| **修改** | `CLI/TileTerrainCLI.cpp` | CLI 命令 |
| **修改** | `Lib/Scene/TileSceneGenerator.cpp` | 生成集成 |

### 8.3 与 Mesh Merge 的兼容性

完全兼容。材质信息不在顶点中，而在全局 Control Map 纹理中。Shader 用世界坐标采样，与网格拓扑无关。顶点焊接、IB 生成、LOD 切换均不受影响。

### 8.4 与 HLOD 的兼容性

L0/L1/L2 所有级别共用同一张 Control Map 纹理和同一个 Material。HLOD proxy mesh 同样用世界坐标采样，自动获得正确的纹理外观。

---

## 九、远距离优化（可选，后续扩展）

- **近处**（0~200m）：ID+Weight 实时混合（3 次 Texture2DArray 采样）
- **远处**（200m+）：逐步过渡到线性混合模式（减少采样次数）
- **超远**（500m+）：烘焙到低分辨率 Virtual Texture 缓存
- **低端设备**：回退到单层 splatmap

---

## 十、实施计划

### Phase A: 数据层
1. TerrainWeightMap 数据结构
2. 二进制序列化
3. Bake 到 Control Map 纹理

### Phase B: 渲染层
4. TileTerrainBlend Shader（GLSL + HLSL）
5. Technique + Material XML
6. 用全 layer 0 验证基础渲染正确

### Phase C: 编辑工具
7. PaintTexture 笔刷 + ≤3 约束
8. CLI init-weightmap / paint-texture 命令

### Phase D: 集成
9. GenerateWorldPartition 集成 Control Map 输出
10. 端到端验证
