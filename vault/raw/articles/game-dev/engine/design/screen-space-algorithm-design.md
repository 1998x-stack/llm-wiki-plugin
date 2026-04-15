---
summary: "Screen space algorithms design: HiZ, SSAO (XeGTAO), SSR (GGX + HiZ), and Motion Vector"
related_paths:
  - engine/Source/Urho3D/Graphics/**
last_updated: "2026-02-14"
---

# 屏幕空间算法设计文档

## 概述

本文档描述 UrhoX 引擎屏幕空间算法的设计方案与实现状态，包括：

1. **HiZ (Hierarchical-Z)** - 双 RT 版本，生成 ClosestHiZ 和 FarthestHiZ
2. **SSAO (Screen Space Ambient Occlusion)** - XeGTAO 忠实移植，复用 HiZ 加速
3. **SSR (Screen Space Reflections)** - GGX 重要性采样 + HiZ/Linear Tracing + UE4 Temporal Denoise
4. **Motion Vector** - 深度重投影运动向量
5. **TAA (Temporal Anti-Aliasing)** - UE4 MainTemporalAAPS 忠实移植

基于延迟渲染管线（CEMapDeferred.xml），GBuffer 数据可直接复用。

> **编码规范**: 所有 shader 代码和详细开发约定见 [render-pipeline-development-guide.md](../guides/render-pipeline-development-guide.md)。

---

## 反射层级系统（Reflection Hierarchy）

### 设计理念

在 PBR 渲染中，反射是 Specular BRDF 的一部分。为了保证**能量守恒**，SSR 不能简单叠加到场景颜色上，而应该**替换** IBL（Image-Based Lighting）反射。

主流引擎（Unity HDRP、Unreal Engine、Frostbite）都采用**反射层级系统**：

```
┌─────────────────────────────────────────────────────┐
│                  Reflection Hierarchy               │
├─────────────────────────────────────────────────────┤
│  Level 1: SSR (屏幕空间，最准确但覆盖有限)          │
│     ↓ fallback (当 SSR 失败时)                      │
│  Level 2: Reflection Probe (局部反射探针)           │
│     ↓ fallback (当无探针时)                         │
│  Level 3: Sky/Global IBL (全局环境反射)             │
└─────────────────────────────────────────────────────┘
```

### 为什么不能简单叠加

```glsl
// ❌ 错误做法：简单叠加会导致双重反射，破坏能量守恒
hvec3 finalColor = sceneColor + ssrReflection;

// ✅ 正确做法：SSR 替换 IBL 反射（pre-multiplied alpha blend）
hvec3 finalReflection = envSpecular * (1.0 - ssrAlpha) + ssrResult.rgb * intensity;
hvec3 finalColor = sceneLighting + finalReflection;
```

### Chicken-and-Egg 问题

```
SSR 需要：场景颜色（作为反射源）
Lighting 需要：SSR 结果（作为 Specular 项）
→ 互相依赖，无法在同一个 Pass 解决
```

**解决方案**：Lighting Pass 分离输出（SPLIT_LIGHTING），SSR 后处理时替换 Specular。

### 当前实现

Deferred Lighting 使用 `SPLIT_LIGHTING` psdefine 分离输出：

| RT 名称 | 内容 | 用途 |
|---------|------|------|
| **SceneLighting** | direct_all + IBL_diffuse + emissive | 场景颜色基础 |
| **EnvSpecular** | IBL_specular only | SSR 的 fallback |

SSR Composite 阶段用 pre-multiplied alpha 替换 EnvSpecular：

```glsl
// Pre-multiplied alpha composite
hvec3 finalReflection = envSpecular * (1.0 - ssrAlpha) + ssrResult.rgb * u_SSRIntensity;
hvec3 finalColor = sceneLighting + finalReflection;
```

---

## 第一部分：引擎层修改 - 支持渲染到指定 Mip Level

### 1.1 修改文件清单

| 文件 | 修改内容 |
|------|---------|
| `BgfxGraphicsImpl.h` | `BgfxRenderSurfaceGroupKey`: uint16→uint32, ToHash 函数 |
| `Graphics.h` | 添加 `renderTargetMips_[]`, 修改 `SetRenderTarget` 签名 |
| `BgfxGraphics.cpp` | `SetRenderTarget` 实现, PrepareDraw 中 rsgk 和 attachment |
| `RenderPath.h` | 新增 `RenderPathOutput` 结构体, 修改 `outputs_` 类型 |
| `RenderPath.cpp` | 解析 XML 的 `mip` 属性 |
| `View.cpp` | `SetRenderTargets` 传递 mip |

> 详细的 C++ 代码变更见 git 历史。此处仅记录关键设计决策。

### 1.2 关键设计决策

**BgfxRenderSurfaceGroupKey**：高 16 位存 mip level，低 16 位存 texture handle，用于 FrameBuffer 缓存 key。

**RenderPathOutput**：扩展 `outputs_` 从 `Vector<Pair<String, CubeMapFace>>` 为包含 `mip_` 字段的结构体。

**RenderPath XML 用法**：

```xml
<!-- 定义带 mipmap 的 RT -->
<rendertarget name="ClosestHiZ" sizedivisor="1 1" format="r32f" miplevels="5" />

<!-- 输出到指定 mip level -->
<command type="quad" ...>
    <output index="0" name="ClosestHiZ" mip="1" />
</command>
```

### 1.3 收益

- HiZ RT 数量从独立 RT 链减少为 2 个 mipmapped RT
- Sampler 绑定大幅减少（HiZ 只需 2 个采样器 + `texture2DLod`）
- Shader 代码更简洁（无需分支选择不同采样器）

---

## 第二部分：RenderPath 配置

### 2.1 GBuffer 结构

| Buffer | 内容 | 用途 |
|--------|------|------|
| GBufferA | Normal (encoded) | SSAO、SSR 方向计算 |
| GBufferB | Metallic, Specular, Roughness, ShadingModelID | SSR 粗糙度衰减 |
| GBufferC | BaseColor | Lighting |
| GBufferD | Emissive | Lighting |
| depth | readabledepth | 所有屏幕空间算法 |

### 2.2 RenderTarget 定义

```xml
<!-- 可读深度 -->
<rendertarget name="depth" sizedivisor="1 1" format="readabledepth" />

<!-- GBuffer -->
<rendertarget name="GBufferA" sizedivisor="1 1" format="rgba" />
<rendertarget name="GBufferB" sizedivisor="1 1" format="rgba" />
<rendertarget name="GBufferC" sizedivisor="1 1" format="rgba" />
<rendertarget name="GBufferD" sizedivisor="1 1" format="rgba" />

<!-- HiZ 独立 RT (降采样链) + mipmapped 纹理 -->
<rendertarget name="ClosestHiZ_Mip0~4" ... format="r32f" />
<rendertarget name="FarthestHiZ_Mip0~4" ... format="r32f" />
<rendertarget name="ClosestHiZ" sizedivisor="1 1" format="r32f" miplevels="5" />
<rendertarget name="FarthestHiZ" sizedivisor="1 1" format="r32f" miplevels="5" />

<!-- SSAO (半分辨率 + temporal filter + bilateral upsample, 匹配 UE4/UE5) -->
<rendertarget name="SSAOBuffer" sizedivisor="2 2" format="r8" />
<rendertarget name="SSAOBlurred" sizedivisor="2 2" format="r8" />
<rendertarget name="SSAOHistory" sizedivisor="2 2" format="r8" persistent="true" />
<rendertarget name="SSAOUpscaled" sizedivisor="1 1" format="r8" />

<!-- Split Lighting -->
<rendertarget name="SceneLighting" sizedivisor="1 1" format="rgba16f" />
<rendertarget name="EnvSpecular" sizedivisor="1 1" format="rgba16f" />

<!-- Motion Vector -->
<rendertarget name="MotionVector" sizedivisor="1 1" format="rg16f" />

<!-- SSR (半分辨率) -->
<rendertarget name="SSRBuffer" sizedivisor="2 2" format="rgba16f" />
<rendertarget name="SSRFiltered" sizedivisor="2 2" format="rgba16f" />
<rendertarget name="SSRHistory" sizedivisor="2 2" format="rgba16f" persistent="true" />
<rendertarget name="SSRUpscaled" sizedivisor="1 1" format="rgba16f" />

<!-- Depth copy (避免读写冲突) -->
<rendertarget name="depth_buffer" sizedivisor="1 1" format="r32f" />

<!-- TAA -->
<rendertarget name="SceneColor" sizedivisor="1 1" format="rgba16f" />
<rendertarget name="TAAHistory" sizedivisor="1 1" format="rgba16f" persistent="true" />
```

### 2.3 完整渲染流程

见 `Res/EngineRes/RenderPaths/CEMapDeferred.xml`，10 阶段管线：

```
1. Pre-Z Pass → depth
2. GBuffer Pass → GBufferA~D
3. HiZ Generation → ClosestHiZ/FarthestHiZ (5 mip each)
3.5. Motion Vector → MotionVector
4. GTAO (半分辨率) → Temporal Filter → Bilateral Upsample → SSAOUpscaled
5. Deferred Lighting (SPLIT_LIGHTING) → SceneLighting + EnvSpecular
6. SSR Trace → SSRBuffer → SSR Temporal → SSRHistory → SSR Upscale → SSR Composite → SceneColor
7. Alpha Pass → SceneColor + CopyDepth → depth_buffer → Water/Volumetric
8. TAA Resolve → viewport → TAAHistory
9. Special Effects (editor overlays)
10. Post Process (Bloom, Tonemapping)
```

---

## 第三部分：算法设计

### 3.1 HiZ 系统

**目的**：为 GTAO 和 SSR 提供层级深度缓冲。

**结构**：
- `ClosestHiZ`（MIN depth）：最近表面 → SSR ray march
- `FarthestHiZ`（MAX depth）：最远表面 → 预留
- 5 级 mip（0-4），R32F

**生成流程**（独立 RT 链 + 拷贝到 mipmapped 纹理）：

```
depth → HiZInit → ClosestHiZ_Mip0 / FarthestHiZ_Mip0
  → HiZDownsample × 4 → Mip1 → Mip2 → Mip3 → Mip4
  → HiZCopy × 5 → ClosestHiZ (mip 0~4) / FarthestHiZ (mip 0~4)
```

独立 RT 链的原因：bgfx 不支持同纹理不同 mip 的同时读写。

**精度要求**：所有 HiZ 值必须用 `hfloat`（fp32）。`float`（fp16）无法表示 R32F 深度差异，会产生量化条纹。

### 3.2 GTAO（XeGTAO 忠实移植）

**参考实现**：Intel XeGTAO (GameTechDev/XeGTAO, MIT License) — `XeGTAO.hlsli`

> **设计原则**：不自创算法。之前自创的 GTAO 同时存在 3 个 bug（采样半径错误 + 初始视角错误 + 可见性公式错误），XeGTAO 移植首次编译即正确。

**核心算法 (XeGTAO_MainPass)**：

1. **Slice loop**（3 slices，覆盖 [0, PI)）
2. **Per-slice projected normal**（论文 lines 8-15）：
   - `orthoDirectionVec = directionVec - dot(directionVec, viewVec) * viewVec`
   - `axisVec = normalize(cross(orthoDirectionVec, viewVec))`
   - `projectedNormalVec = viewspaceNormal - axisVec * dot(viewspaceNormal, axisVec)`
   - `n = signNorm * FastACos(cosNorm)`
3. **Horizon search**（3 steps per direction）：
   - 功率分布采样：`s = (step/total)²` 聚焦中心附近
   - MIP 级别选择：`log2(sampleOffset) - 3.3`
   - 距离衰减通过 `mix(lowHorizonCos, shc, weight)` — **非角度缩放**
4. **Visibility integral**：`IntegrateArc(h, n) = (cosN + 2h·sinN - cos(2h-n)) / 4`

**噪声源**：Hilbert 空间填充曲线 + R2 准随机序列（XeGTAO 原版）
- Hilbert 曲线将 2D 像素坐标映射到 64×64 块内的 1D 索引，相邻像素索引差异大
- R2 序列提供 2D 准随机抖动 + temporal 变化（288×frameIndex 偏移）
- 消除了 IGN 噪声的方向性周期导致的斜条纹 artifact

**质量档位**（slices × steps）：
| 档位 | Slices | Steps | 说明 |
|------|--------|-------|------|
| Low | 1 | 2 | 最低质量 |
| Medium | 2 | 2 | 中等质量 |
| High | 3 | 3 | **推荐**，需要 temporal 降噪 |
| Ultra | 9 | 3 | 单帧无噪点，无需 temporal |

**默认参数**：AORadius=0.5 (×1.457), AOIntensity=2.2 (FinalValuePower)

**半分辨率管线**（匹配 UE4/UE5 默认做法）：
```
GTAO (半分辨率) → [Spatial Denoise (可选, 默认关闭)]
  → Temporal Filter (motion vector 重投影 + 邻域 clamp)
    → Copy to History
      → Bilateral Upsample (深度感知, 半分辨率→全分辨率)
```

- **Spatial Denoise** (`GTAODenoise.glsl`): XeGTAO 原版 2-pass 边缘感知空间滤波，默认 `enabled="false"`（temporal filter 已足够，匹配 UE4 `r.GTAO.SpatialFilter=0`）
- **Temporal Filter** (`GTAOTemporal.glsl`): motion vector 重投影 + plus-pattern 邻域 min/max clamp + 固定 10% blend，独立于主 TAA
- **Bilateral Upsample** (`GTAOBilateralUpscale.glsl`): 4-tap 深度感知上采样（Gaussian 衰减），防止 AO 跨深度边界渗透

### 3.3 Motion Vector

**方法**：深度重投影（适用于静态场景或相机运动为主的场景）

```
当前帧 UV + depth → u_InvViewProj → worldPos → u_PrevViewProj → prevUV
MotionVector = currentUV - prevUV
```

**关键**：
1. 必须使用自定义矩阵（通过 Execution 传递），不能用 bgfx 内置的 `u_viewProj`/`u_invViewProj`（约定不同）。
2. Motion Vector pass 运行时 camera 处于 **unjittered** 状态（`jitter="false"`），`InvViewProj` 和 `PrevViewProj` 都是 unjittered 的，输出纯物体运动向量，不包含 TAA jitter 差异。

```cpp
// C++ (View.cpp, ApplyMotionVectorParameters)
// 此时 camera 已被 ApplyCommandJitter() 恢复为 unjittered
Matrix4 invViewProj = (camera_->GetGPUProjection() * camera_->GetView()).Inverse();
graphics_->SetShaderParameter(StringHash("InvViewProj"), invViewProj);
// prevViewProj_ 在 FinalizeTAAJitter() 中以 unjittered 状态保存
graphics_->SetShaderParameter(StringHash("PrevViewProj"), prevViewProj_);
```

### 3.4 SSR 管线

SSR 采用 5 阶段管线，半分辨率 trace + 全分辨率合成：

```
SSR Trace (半分辨率)
  → SSR Temporal Denoise (半分辨率)
    → SSR Copy (历史帧)
      → SSR Bilateral Upscale (全分辨率)
        → SSR Composite (与 IBL 合成)
```

#### 3.4.1 SSR Trace — GGX 重要性采样

两种 trace 方法（XML 中 `enabled` 互斥切换）：

| 方法 | 算法 | 优势 |
|------|------|------|
| **Linear Trace** | 逐像素线性 march (64步) + 二分精化 (8步) | 简单可靠 |
| **HiZ Trace** | AMD FidelityFX SSSR cell traversal + mip bias | 覆盖更远距离 |

**共同特性**：
- **Stochastic GGX importance sampling**：每像素每帧 1 根光线
- **IGN 噪声**：两个独立 IGN 评估（交换坐标 + 不同时域偏移）
- **Pre-multiplied alpha 输出**：`vec4(color * confidence, confidence)`
- **NdotV grazing fade**：`saturate(NdotV * 4.0)`
- **MIN_SSR_ROUGHNESS = 0.014**（UE4 值）

#### 3.4.2 SSR HiZ Trace — 半分辨率 FidelityFX 改造

SSR 在半分辨率下运行（`sizedivisor="2 2"`），但 FidelityFX SSSR 设计在全分辨率运行。

**核心思路：Mip Bias**

关键观察：**HiZ mip 1 的分辨率 = 全分辨率 / 2 = SSR 半分辨率**。

给所有 HiZ 采样加 `HIZ_MIP_BIAS = 1`，等价于让 FidelityFX 在半分辨率网格上运行：

| 原版 FidelityFX（全分辨率） | 半分辨率改造（mip bias +1） |
|---|---|
| mostDetailedMip = 0 → 采样 mip 0 | mostDetailedMip = 0 → 采样 mip **1** = SSR 分辨率 |
| mostDetailedMip = 1 → 采样 mip 1 | mostDetailedMip = 1 → 采样 mip **2** |
| screenSize = 全分辨率 | screenSize = `1/cGBufferInvSize`（= SSR 分辨率）|

算法逻辑**完全保持原版 FidelityFX 不变**（`InitialAdvanceRay`, `AdvanceRay`, `HierarchicalRaymarch`），唯一改动是 HiZ 采样时 mip +1。

**不需要 depth bias**：FidelityFX 通过 `mostDetailedMip = 1`（min-depth of 2×2）提供间隙。

#### 3.4.3 SSR Temporal Denoise — UE4 SSRTemporalAAPS

**参考实现**：UE4 PostProcessTemporalCommon.usf SSR 配置

完全匹配 UE4 的 flag 配置：

| UE4 Flag | 值 | 含义 |
|----------|---|------|
| AA_FILTERED | 1 | Blackman-Harris 3×3 空间滤波，jitter-recentered |
| AA_LOWPASS | 1 | 宽 BH (scale×0.25=0.375) 作为 AABB clamp 目标 |
| AA_ROUND | 1 | mu±sigma 方差边界（8 样本，排除右下角） |
| AA_AABB | 1 | Ray-AABB clamp，**仅 RGB**（alpha 不修改） |
| AA_ALPHA | 0 | Alpha 作为数据，与 color 一同滤波（不单独 clamp） |
| AA_TONE | 1 | HDR 感知权重 `HdrWeight4 = 1/(Luma4+4)` |
| AA_LERP | 8 | 固定 12.5% blend |
| AA_CROSS | 0 | 直接运动向量采样（无深度膨胀） |

**关键细节**：
- BH kernel scale = 1.5（SSR Sharpness=1.0 → `1.0 + 1.0 * 0.5 = 1.5`）
- AABB clamp 只修改 `.rgb`，`.a` 不动 → 避免 alpha 硬切割导致条纹
- Luma4 = `g*2 + r + b`，HdrWeight = `1/(Luma4+4)`
- 逆权重 = `4/(1-Luma4)`，clamp 分母到 1/32

#### 3.4.4 SSR Bilateral Upscale

半分辨率 → 全分辨率。使用深度 + 法线双边权重，4 个最近邻加权插值。避免反射跨越深度/法线边界时产生渗色。

#### 3.4.5 SSR Composite

反射层级系统合成。使用 pre-multiplied alpha blend：

```glsl
hvec3 finalReflection = envSpecular * (1.0 - ssrAlpha) + ssrResult.rgb * u_SSRIntensity;
hvec3 finalColor = sceneLighting + finalReflection;
```

SSR **替换** IBL Specular（非叠加），保证能量守恒。

### 3.5 TAA（UE4 MainTemporalAAPS 忠实移植）

**参考实现**：UE4 PostProcessTemporalCommon.usf, AA_YCOCG=1 路径（raysjoshua 版 AA_FILTERED=1）

> TAA 与 SSR Temporal 是**独立的两个时域滤波器**，解决不同问题：
> - SSR Temporal = 降噪（消除 stochastic importance sampling 噪声）
> - Main TAA = 边缘抗锯齿（消除几何锯齿）

**核心配置**：

| UE4 Flag | 值 | 含义 |
|----------|---|------|
| AA_FILTERED | 1 | BH 加权 plus-pattern 空间滤波（jitter-recentered） |
| AA_YCOCG | 1 | YCoCg 颜色空间 |
| AA_BICUBIC | 1 | Catmull-Rom 双三次历史采样（**锐度唯一来源**） |
| AA_TONE | 1 | HDR 感知权重 `1/(Y+1)` 在 YCoCg luminance 上 |
| AA_AABB | 1 | 但 AA_YCOCG 路径下实际为简单 component-wise clamp |
| AA_CROSS | 2 | X-pattern 运动膨胀 2px（4 对角 + 中心） |
| AA_LOWPASS | 0 | 无宽 lowpass |
| AA_ALPHA | 0 | Alpha 不做 AA |
| Blend | 0.04 | 固定 4% 新帧（AA_TONE=1 时硬编码） |

> **UE4 版本差异**：raysjoshua 版 `AA_FILTERED=1`（BH 空间滤波），chendi-YU 版 `AA_FILTERED=0`（仅中心像素）。我们使用 `AA_FILTERED=1`，实测效果更好。

**算法流程**：
1. X-pattern motion dilation（2px 对角采样，最近深度选运动向量）
2. Plus-pattern 采样（5 taps）→ RGB → YCoCg → HDR weight
3. BH 加权空间滤波（jitter-recentered，scale=1.0）
4. Plus min/max 邻域边界
5. Catmull-Rom 双三次历史采样（5-tap optimized，**负 lobes = 锐度**）
6. YCoCg component-wise clamp
7. Fixed 0.04 blend
8. Karis 逆 HDR weight → YCoCg → RGB

**锐度来源**：Catmull-Rom 双三次历史采样的负 lobes 自然产生高通增强。**无显式锐化步骤**。

#### 3.5.1 Per-Command Jitter 机制

TAA 需要每帧以不同的亚像素偏移光栅化几何体（提供亚像素信息），但后处理 pass 必须使用稳定的 UV（否则画面抖动）。UE4 通过 `DrawRectangle` 函数让后处理 quad 绕过 camera projection 实现 unjittered UV。UrhoX 的 fullscreen quad UV 来自 `GetQuadTexCoord(gl_Position)`（从 clip position 推导），无法绕过 camera，因此采用 **per-command jitter** 方案：在 XML command 上标记 `jitter="true"`，只有标记的 command 才会应用 camera projection offset。

**C++ 实现**（`View.cpp`）：

```
InitTAAJitter()          ← Render() 开头，计算 Halton(2,3) 偏移，不立即应用
  ↓
ExecuteRenderPathCommands()
  ├─ ApplyCommandJitter(cmd)  ← 每个 command 前，根据 bUseJitter 设置/清除 projection offset
  │    ├─ jitter=true:  camera->SetProjectionOffset(original + jitterOffset)
  │    └─ jitter=false: camera->SetProjectionOffset(original)
  │    └─ ClearParameterSource(SP_CAMERA)  ← 强制下一个 batch 重新上传 camera uniforms
  └─ switch (command.type_) → 执行渲染
  ↓
FinalizeTAAJitter()      ← Render() 结尾
  ├─ 恢复 camera offset 到 original
  ├─ 保存 UNJITTERED prevViewProj（供下帧 Motion Vector 使用）
  └─ ++taaFrameIndex_
```

**Jitter 计算**：

```
Halton(2,3) 序列，8 帧循环，1-based index
taaJitterPixels_ = (haltonX - 0.5, haltonY - 0.5)     // ±0.5 像素
taaJitterOffset_ = taaJitterPixels_ / viewSize          // projection offset 空间
Camera::SetProjectionOffset → projection_.m02_ = offset.x * 2.0  // NDC 空间
```

**哪些 Command 需要 jitter**：

| Command | jitter | 原因 |
|---------|--------|------|
| depth (scenepass) | ✅ | 深度预渲染，TAA 亚像素采样核心 |
| deferred (scenepass) | ✅ | GBuffer 渲染，几何体光栅化 |
| lightvolumes | ✅ | 延迟光照，需要匹配 jittered GBuffer |
| GTAO (quad) | ✅ | 读取 jittered depth 做投影重建，cInvProj 必须匹配 |
| SSR Trace (quad) | ✅ | 同上，ray origin 从 jittered depth 重建 |
| postopaque / alpha / postalpha (scenepass) | ✅ | 几何体渲染 |
| singlelayerwater / volumetriclight | ✅ | 场景效果，受益于 TAA |
| Motion Vector (quad) | ❌ | 使用 unjittered InvViewProj + unjittered PrevViewProj，输出纯运动向量 |
| HiZ Init/Downsample (quad) | ❌ | 纯纹理处理，不涉及 camera |
| SSAO Blur (quad) | ❌ | 纯纹理处理 |
| SSR Temporal/Copy/Composite (quad) | ❌ | 纯纹理处理 |
| TAA Resolve (quad) | ❌ | **必须 unjittered UV**，jitter 信息通过 `u_JitterOffset` uniform 传递给 BH 滤波器 |
| Bloom / Tonemap (quad) | ❌ | 纯后处理 |

**Motion Vector 与 Jitter 的关系**：

Motion Vector pass 运行时 camera 处于 **unjittered** 状态：
- `InvViewProj` = 当前帧 unjittered ViewProj 的逆
- `PrevViewProj` = 上一帧 `FinalizeTAAJitter()` 保存的 unjittered ViewProj
- 输出的运动向量 = 纯物体运动，不包含 jitter 差异
- TAA Resolve 的 `historyUV = uv - motionVec` 直接使用，无需 jitter 补偿

**TAA Resolve 与 Jitter 的关系**：

TAA Resolve 运行时 UV 是 unjittered（画面稳定），但需要知道当前帧的 jitter 位置来正确加权当前帧的贡献：
- C++ `ApplyTAAResolveParameters()` 传递 `u_JitterOffset = taaJitterPixels_`（±0.5 像素空间）
- Shader 中 BH 空间滤波器以 jitter 位置为中心重新加权 5 个邻域样本
- 效果：在 pixel center 处对当前帧做亚像素插值，模拟 jitter 位置的采样值

> **关键陷阱**：`RenderPath.cpp` 中 `CMD_SCENEPASS` 的 `switch case` 有独立的 `break;`，而 `jitter` 属性解析在 `CMD_QUAD`/`CMD_LIGHTVOLUMES`/`CMD_VOLUMETRIC_LIGHT` 的 fallthrough 分支中。必须在 `CMD_SCENEPASS` case 内单独添加 jitter 解析，否则几何体永远不会收到 jitter。

### 3.6 深度读写冲突解决

**问题**：`singlelayerwater` 和 `volumetriclight` 需要同时用 `depth` 做深度测试（`depthstencil`）和在 shader 中采样深度 → 未定义行为。

**解决方案**：在这些 pass 之前，拷贝 `depth` 到 `depth_buffer`（R32F），shader 采样拷贝版本：

```xml
<!-- CopyDepth 在 water/volumetric 之前 -->
<command type="quad" tag="CopyDepth" vs="ScreenSpace/CopyTexture" ps="ScreenSpace/CopyTexture"
         disableDepthStencilRT="true">
    <texture unit="0" name="depth" />
    <output index="0" name="depth_buffer" />
</command>

<!-- singlelayerwater: depthstencil=depth (深度测试), texture unit 3=depth_buffer (采样) -->
<command type="scenepass" pass="singlelayerwater" depthstencil="depth">
    <texture unit="3" name="depth_buffer" />
    <output index="0" name="SceneColor" />
</command>
```

### 3.7 Lighting Shader 分离输出

为了支持反射层级系统，延迟光照 Shader 使用 `SPLIT_LIGHTING` psdefine 分离输出。

**当前 Shader 调用链**：

```
StandardPBRDeferred.glsl (入口)
    ├── MetallicPBR() / MetallicPBR_Split()  ← MetallicWorkflow.glsl
    │       └── Standard_BRDF() / Standard_BRDF_Split()  ← StandardBRDF.sh
    │               └── Disney_BRDF() / Disney_BRDF_Split()  ← DisneyBRDF.glsl
    │                       ├── GetLightingColor() → directDiffuse + directSpecular
    │                       └── GI_Indirect()       → indirectDiffuse + indirectSpecular (IBL)
    └── LambertBRDF()  ← lambert.sh (无 Specular)
```

**分离输出**：

| MRT 输出 | 内容组成 | 说明 |
|----------|---------|------|
| **gl_FragData[0]** (SceneLighting) | emissive + directDiffuse + directSpecular + indirectDiffuse | 场景的全部光照（除 IBL Specular） |
| **gl_FragData[1]** (EnvSpecular) | indirectSpecular (IBL) | SSR 的 fallback |

`SPLIT_LIGHTING` 宏控制，不启用时保持原有单一输出行为，向后兼容。

---

## 第四部分：注意事项

### 4.1 REVERSED_Z

UrhoX 当前 **REVERSED_Z 未定义**，所有 `#ifdef REVERSED_Z` 路径是死代码。

标准 Z（0=近, 1=远）：
- Closest depth = **min** value
- Farthest depth = **max** value

### 4.2 性能预算

| 效果 | 分辨率 | 采样数 | 备注 |
|------|--------|--------|------|
| HiZ 生成 | 全分辨率 | 5 init + 4×4 downsample + 5 copy = 14 pass | 但都很轻量 |
| GTAO | 半分辨率 | 3 slices × 3 steps × 2 directions = 18 采样 | + temporal + bilateral upsample |
| SSR Trace | 半分辨率 | 最多 64 步 march | 每像素 1 根光线 |
| SSR Temporal | 半分辨率 | 9 tap 邻域 + 2×9 BH 权重 | 固定开销 |
| SSR Upscale | 全分辨率 | 4 tap 双边 | 轻量 |
| TAA Resolve | 全分辨率 | 5 tap 邻域 + 5 tap 双三次 + 5 tap 深度 | 固定开销 |

### 4.3 Texture Slot 限制

`type="lightvolumes"` 命令自动覆盖 slot 5（IBL specular cubemap）。AO 使用 slot 14（TU_AOMAP）避免冲突。

### 4.4 实现状态

**引擎层修改** — 全部完成

- [x] `BgfxGraphicsImpl.h` - uint32 RenderSurfaceGroupKey
- [x] `Graphics.h` - `renderTargetMips_[]` + `SetRenderTarget` mip 参数
- [x] `BgfxGraphics.cpp` - mip level 支持
- [x] `RenderPath.h/cpp` - `mip` 属性解析 + `miplevels` RT 属性
- [x] `View.cpp` - 传递 mip 到 Graphics 层
- [x] `Renderer.h/cpp` - `GetScreenBuffer` numLevels 参数

**Shader 实现** — 全部完成

- [x] HiZ: `HiZInit.glsl`, `HiZDownsample.glsl`, `HiZCopy.glsl`
- [x] GTAO: `GTAO.glsl`, `GTAODenoise.glsl`, `GTAOTemporal.glsl`, `GTAOBilateralUpscale.glsl`, `GTAOCommon.sh` (XeGTAO faithful port, Hilbert+R2 noise)
- [x] SSR: `SSRLinearTrace.glsl`, `SSRHiZTrace.glsl` (FidelityFX SSSR), `SSRTemporal.glsl` (UE4 SSRTemporalAAPS), `SSRBilateralUpscale.glsl`, `SSRComposite.glsl`
- [x] SSR Common: `SSRCommon.sh`, `ScreenSpaceCommon.sh`
- [x] Motion Vector: `MotionVector.glsl`
- [x] TAA: `TAAResolve.glsl` (UE4 MainTemporalAAPS faithful port)
- [x] 通用工具: `CopyTexture.glsl`

**Lighting Shader 修改** — 全部完成

- [x] `DisneyBRDF.glsl` - `Disney_BRDF_Split()` 函数
- [x] `MetallicWorkflow.glsl` - `MetallicPBR_Split()` 函数
- [x] `StandardBRDF.sh` - `Standard_BRDF_Split()` 宏选择
- [x] `StandardPBRDeferred.glsl` - `SPLIT_LIGHTING` 分支

**C++ Execution 机制** — 全部完成

- [x] `ApplyMotionVectorParameters` - `u_InvViewProj`, `u_PrevViewProj`
- [x] `ApplySSRTraceParameters` - `u_FrameIndex`, `u_ScreenSize`
- [x] `ApplySSRTemporalParameters` - `u_JitterOffset`, `u_SSRTexelSize`
- [x] `ApplyTAAResolveParameters` - `u_JitterOffset`
- [x] TAA jitter (Halton 2,3) via `Camera::SetProjectionOffset`
- [x] `prevViewProj_` 存储上一帧 ViewProj 矩阵

**待实现**

- [ ] SSPR (Screen Space Planar Reflections) — 可选
- [ ] Per-object Motion Vector（需要引擎层支持上一帧 Model 矩阵）

---

## 目录结构

```
Res/Shaders/BLGL/ScreenSpace/
├── ScreenSpaceCommon.sh          # 共享函数（ReconstructViewPos, DecodeGBufferNormal, IGN）
├── CopyTexture.glsl              # 通用纹理拷贝
├── HiZ/
│   ├── HiZInit.glsl              # depth → Mip0 (MRT: closest, farthest)
│   ├── HiZDownsample.glsl        # Mip(n-1) → Mip(n) (MRT: min/max)
│   └── HiZCopy.glsl              # 独立 RT → mipmapped 纹理
├── SSAO/
│   ├── GTAO.glsl                 # XeGTAO 主 pass (3 slices × 3 steps, Hilbert+R2 noise)
│   ├── GTAODenoise.glsl          # XeGTAO 空间降噪 (可选, 默认关闭)
│   ├── GTAOTemporal.glsl         # 时域降噪 (motion vector 重投影)
│   ├── GTAOBilateralUpscale.glsl # 双边上采样 (半分辨率→全分辨率)
│   ├── SSAOBlur.glsl             # 旧版双边模糊 (已弃用)
│   └── GTAOCommon.sh             # XeGTAO 共享函数、常量、Hilbert 曲线
├── SSR/
│   ├── SSRLinearTrace.glsl       # 线性 march trace + GGX importance sampling
│   ├── SSRHiZTrace.glsl          # FidelityFX SSSR cell traversal + mip bias
│   ├── SSRTemporal.glsl          # UE4 SSRTemporalAAPS temporal denoise
│   ├── SSRBilateralUpscale.glsl  # 深度+法线感知双边上采样
│   ├── SSRComposite.glsl         # 反射层级合成（SSR + IBL fallback）
│   └── SSRCommon.sh              # GGX importance sampling, edge fade
├── TAA/
│   └── TAAResolve.glsl           # UE4 MainTemporalAAPS (AA_YCOCG=1)
└── MotionVector/
    └── MotionVector.glsl         # 深度重投影运动向量
```

---

## 更新记录

| 日期 | 内容 |
|------|------|
| 2026-02-05 | 初版设计文档 |
| 2026-02-05 | 添加反射层级系统（Reflection Hierarchy）设计 |
| 2026-02-05 | 添加 Lighting Shader 分离输出方案 |
| 2026-02-05 | 添加 SSR Temporal Filter 方案 |
| 2026-02-06 | 实现引擎 Mipmap RT 支持 |
| 2026-02-06 | 添加 SSR HiZ Trace 半分辨率 FidelityFX 改造方案 |
| 2026-02-06 | 全面更新：同步实际实现状态，更新算法为 XeGTAO/UE4/FidelityFX 忠实移植，添加 TAA 设计，添加深度读写冲突解决方案，更新 TODO 为实际完成状态 |
| 2026-02-14 | GTAO 重大更新：Hilbert+R2 噪声源替代 IGN、半分辨率管线、temporal filter、bilateral upsample、XeGTAO spatial denoise (可选) |
