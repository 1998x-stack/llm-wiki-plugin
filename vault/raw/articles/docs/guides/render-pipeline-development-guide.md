---
summary: "Render pipeline development conventions, shader standards, and best practices for UrhoX engine"
last_updated: "2026-02-14"
---

# UrhoX 渲染管线开发指南

本文档记录 UrhoX 引擎渲染管线开发的规范、约定和最佳实践。

---

## 目录

1. [管线总览](#1-管线总览)
2. [Shader 开发规范](#2-shader-开发规范)
3. [Shader 精度规范（关键陷阱）](#3-shader-精度规范关键陷阱)
4. [SAMPLER 命名规范](#4-sampler-命名规范)
5. [Uniform 使用规范](#5-uniform-使用规范)
6. [BGFX Shader 语法注意事项](#6-bgfx-shader-语法注意事项)
7. [RenderPath 配置](#7-renderpath-配置)
8. [Execution 机制（C++ → Shader 参数传递）](#8-execution-机制c--shader-参数传递)
9. [深度缓冲使用规范](#9-深度缓冲使用规范)
10. [屏幕空间效果架构](#10-屏幕空间效果架构)
11. [各效果详解](#11-各效果详解)
12. [矩阵约定与坐标系](#12-矩阵约定与坐标系)
13. [开发哲学](#13-开发哲学)
14. [目录结构](#14-目录结构)
15. [常见问题](#15-常见问题)

---

## 1. 管线总览

CEMapDeferred.xml 定义了完整的延迟渲染管线，分为 10 个阶段：

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Pre-Z Pass          深度预渲染                                │
│ 2. GBuffer Pass        几何属性写入 (A:Normal, B:PBR, C:Albedo, D:Emissive) │
│ 3. HiZ Generation      层级深度缓冲 (5 级 mip, Closest + Farthest)         │
│ 3.5 Motion Vector      运动向量生成 (深度重投影)                  │
│ 4. SSAO (GTAO)         半分辨率 GTAO → Temporal → Bilateral Upsample      │
│ 5. Deferred Lighting    延迟光照 → SceneLighting + EnvSpecular (分离输出)  │
│ 6. SSR                  屏幕空间反射 (Trace → Temporal → Upscale → Composite) │
│ 7. Alpha Pass           半透明物体 (postopaque → alpha → postalpha)          │
│    + CopyDepth          深度拷贝 (解决读写冲突)                    │
│    + Water/Volumetric   水面 + 体积光 (采样 depth_buffer)          │
│ 8. TAA                  时域抗锯齿 → viewport                     │
│ 9. Special Effects      编辑器叠加 (高亮, 描边)                    │
│ 10. Post Process        Bloom, Tonemapping 等后处理                │
└─────────────────────────────────────────────────────────────────┘
```

### 关键 RenderTarget

| RT 名称 | 格式 | 尺寸 | 用途 |
|---------|------|------|------|
| `depth` | readabledepth | 1:1 | 可读深度缓冲，贯穿全管线 |
| `GBufferA~D` | rgba | 1:1 | 几何属性 (法线/PBR/Albedo/Emissive) |
| `ClosestHiZ` | r32f, 5 mip | 1:1 | MIN 深度层级纹理 (最近表面) |
| `FarthestHiZ` | r32f, 5 mip | 1:1 | MAX 深度层级纹理 (最远表面) |
| `SSAOBuffer` | r8 | 1/2 | AO 计算结果 (半分辨率) |
| `SSAOBlurred` | r8 | 1/2 | AO 中间结果 / temporal 输出 |
| `SSAOHistory` | r8, persistent | 1/2 | AO 历史帧 (temporal filter) |
| `SSAOUpscaled` | r8 | 1:1 | AO 双边上采样结果 (全分辨率) |
| `SceneLighting` | rgba16f | 1:1 | 直接光 + IBL Diffuse + Emissive |
| `EnvSpecular` | rgba16f | 1:1 | IBL Specular only (SSR fallback) |
| `MotionVector` | rg16f | 1:1 | 逐像素运动向量 |
| `SSRBuffer` | rgba16f | 1/2 | SSR trace 原始结果 |
| `SSRFiltered` | rgba16f | 1/2 | SSR 时域降噪结果 |
| `SSRHistory` | rgba16f, persistent | 1/2 | SSR 历史帧 |
| `SSRUpscaled` | rgba16f | 1:1 | SSR 双边上采样结果 |
| `depth_buffer` | r32f | 1:1 | 深度拷贝 (避免读写冲突) |
| `SceneColor` | rgba16f | 1:1 | HDR 场景色 (SSR合成 + alpha) |
| `TAAHistory` | rgba16f, persistent | 1:1 | TAA 历史帧 |

### 分离光照（Split Lighting）

延迟光照使用 `SPLIT_LIGHTING` 宏分离输出：
- **SceneLighting** = 直接光全部 + IBL Diffuse + Emissive
- **EnvSpecular** = IBL Specular only

SSR Composite 阶段用 SSR 结果 **替换**（非叠加）EnvSpecular，实现能量守恒：
```
FinalColor = SceneLighting + lerp(EnvSpecular, SSR, ssrConfidence)
```

---

## 2. Shader 开发规范

### 2.1 文件命名

- **使用大写驼峰命名**：`HiZInit.glsl`, `SSAOBlur.glsl`, `SSRHiZTrace.glsl`
- **不要使用** `fs_xxx.glsl` / `vs_xxx.glsl` 分离命名

### 2.2 函数命名

- **所有函数使用 PascalCase**：`ReconstructViewPos`, `CalculateEdgeFade`, `ImportanceSampleGGX`
- **注意引擎冲突**：`samplers.sh` 已定义 `DecodeNormal(vec3)` 和 `DecodeNormal(vec4)`，因此自定义版本命名为 `DecodeGBufferNormal` 避免冲突

### 2.3 VS/PS 合并写法

所有后处理 Shader 应将 VS 和 PS 写在同一个文件中，使用条件编译区分：

```glsl
#include "varying_quad.def.sc"
#include "urho3d_compatibility.sh"

#ifdef COMPILEVS
    $input a_position
    $output vTexCoord, vScreenPos
#endif
#ifdef COMPILEPS
    $input vTexCoord, vScreenPos
#endif

#include "Common/common.sh"
#include "uniforms.sh"
#include "samplers.sh"
#include "transform.sh"
#include "screen_pos.sh"

void VS()
{
    hmat4 modelMatrix = iModelMatrix;
    hvec3 worldPos = GetWorldPos(modelMatrix);
    gl_Position = GetClipPos(worldPos);
    vTexCoord = GetQuadTexCoord(gl_Position);
    vScreenPos = GetScreenPosPreDiv(gl_Position);
}

#ifdef COMPILEPS

// PS-only samplers and uniforms here

void PS()
{
    // ...
}

#endif
```

### 2.4 标准头文件

后处理 Shader 必须 include 以下标准头文件：

| 头文件 | 用途 |
|--------|------|
| `varying_quad.def.sc` | 全屏 quad 的 varying 定义 |
| `urho3d_compatibility.sh` | 引擎兼容性宏 |
| `Common/common.sh` | 通用工具函数 |
| `uniforms.sh` | 引擎 uniform 定义 |
| `samplers.sh` | 预定义采样器 |
| `transform.sh` | 变换函数 |
| `screen_pos.sh` | 屏幕坐标函数 |

屏幕空间效果额外 include：

| 头文件 | 用途 |
|--------|------|
| `ScreenSpace/ScreenSpaceCommon.sh` | `ReconstructViewPos`, `DecodeGBufferNormal`, `InterleavedGradientNoise` |
| `ScreenSpace/SSR/SSRCommon.sh` | SSR 专用：`CalculateEdgeFade`, `ImportanceSampleGGX`, `TangentToWorld` |
| `ScreenSpace/SSAO/GTAOCommon.sh` | GTAO 专用：`XeGTAO_FastACos`, XeGTAO 常量 |

### 2.5 标准接口函数

使用引擎提供的标准接口，不要自己实现：

| 函数 | 用途 |
|------|------|
| `GetWorldPos(modelMatrix)` | 获取世界坐标 |
| `GetClipPos(worldPos)` | 世界坐标转裁剪坐标 |
| `GetQuadTexCoord(gl_Position)` | 获取全屏 quad 的 UV |
| `GetScreenPosPreDiv(gl_Position)` | 获取屏幕坐标 |
| `LinearizeDepth(rawDepth, near, far)` | 引擎提供的深度线性化，处理 GL/D3D 差异 |

---

## 3. Shader 精度规范（关键陷阱）

### 3.1 精度约定（反直觉！）

UrhoX 的 BGFX shader 精度约定与常规**相反**：

| 写法 | 实际精度 | 说明 |
|------|---------|------|
| `float`, `vec2`, `vec3`, `vec4`, `mat4` | **HALF (fp16)** | 默认类型 = 半精度 |
| `hfloat`, `hvec2`, `hvec3`, `hvec4`, `hmat4` | **FULL (fp32)** | h 前缀 = 全精度 |

**这是最常见的 bug 来源！**

### 3.2 必须使用全精度 (hfloat/hvec*) 的场景

- **深度值** — fp16 无法表示深度差异，产生量化条纹
- **矩阵运算** — 视图投影矩阵必须 `hmat4`
- **位置重建** — `ReconstructViewPos` 的返回值和中间计算
- **HiZ 采样** — R32F 深度值必须用 `hfloat` 存储
- **运动向量** — 亚像素级精度需要 fp32

### 3.3 hvec* 初始化语法

**必须使用 `_init()` 函数**，不能用构造器语法：

```glsl
// ✅ 正确
hvec2 v = hvec2_init(1.0, 2.0);
hvec3 n = hvec3_init(x, y, z);
hvec4 p = hvec4_init(pos.x, pos.y, pos.z, 1.0);

// ❌ 错误 — 不支持构造器语法
hvec2 v = hvec2(1.0, 2.0);      // 编译错误
hvec4 p = hvec4(pos.xyz, 1.0);  // 编译错误
```

### 3.4 splat 函数

```glsl
// 半精度 splat
vec2 v = vec2_splat(0.0);
vec3 n = vec3_splat(1.0);

// 全精度没有 splat，用 _init()
hvec2 v = hvec2_init(0.0, 0.0);
```

---

## 4. SAMPLER 命名规范

### 4.1 核心规则

**引擎通过变量名的后缀数字来确定 register 绑定！**

```glsl
// 正确：后缀数字 0 表示绑定到 register 0
SAMPLER2D(u_Depth0, 0);

// 正确：后缀数字 1 表示绑定到 register 1
SAMPLER2D(u_Normal1, 1);

// 错误：没有数字后缀，引擎无法正确解析 register
SAMPLER2D(u_Depth, 0);  // 不要这样写
```

### 4.2 命名格式

```
u_<语义名><register数字>
```

示例：
- `u_Depth0` - 深度缓冲，register 0
- `u_Normal1` - 法线缓冲，register 1
- `u_GBufferB2` - GBuffer B，register 2
- `u_ClosestHiZ3` - ClosestHiZ 纹理，register 3

### 4.3 与 RenderPath 对应

Shader 中的 register 数字必须与 RenderPath XML 中的 `texture unit` 匹配：

```xml
<!-- RenderPath -->
<command type="quad" vs="ScreenSpace/SSAO/GTAO" ps="ScreenSpace/SSAO/GTAO">
    <texture unit="0" name="GBufferA" />
    <texture unit="1" name="ClosestHiZ" />
</command>
```

```glsl
// Shader
SAMPLER2D(u_Normal0, 0);     // 对应 unit="0"
SAMPLER2D(u_ClosestHiZ1, 1); // 对应 unit="1"
```

---

## 5. Uniform 使用规范

### 5.1 cGBufferInvSize

`cGBufferInvSize` 是引擎自动设置的 uniform，表示**当前 output RT 的 inverse size**。

```glsl
uniform vec2 u_GBufferInvSize;
#define cGBufferInvSize u_GBufferInvSize
```

**关键点：**
- 它是 `vec2`，只有 `.xy` 分量
- 值为 `(1.0/outputWidth, 1.0/outputHeight)`
- 引擎在每个 quad pass 时根据 output RT 尺寸自动设置

### 5.2 Downsample 时的 TexelSize 计算

对于 downsample pass（output 是 input 的 1/2 尺寸）：

```glsl
// cGBufferInvSize 是 output RT 的 invSize
// Input 纹理是 output 的 2 倍大
// 所以 input 的 texelSize = cGBufferInvSize * 0.5
vec2 inputTexelSize = cGBufferInvSize * 0.5;
```

### 5.3 Per-RenderTarget InvSize

引擎会为每个 render target 自动设置专门的 InvSize uniform：

```glsl
// 格式：c<RenderTargetName>InvSize
uniform vec2 u_ClosestHiZInvSize;
#define cClosestHiZInvSize u_ClosestHiZInvSize
```

### 5.4 RenderPath Parameter → Shader Uniform

RenderPath XML 中的 `<parameter>` 自动映射为 shader uniform，加 `u_` 前缀：

```xml
<parameter name="AORadius" value="0.5" />
<parameter name="MaxSteps" value="64" />
<parameter name="SSRIntensity" value="1.0" />
```

```glsl
uniform hfloat u_AORadius;      // XML name="AORadius"
uniform hfloat u_MaxSteps;      // XML name="MaxSteps"
uniform hfloat u_SSRIntensity;  // XML name="SSRIntensity"
```

### 5.5 已定义的 Uniform

以下 uniform 已在引擎头文件中定义，不要重复声明：
- `u_viewTexel` - 在 `bgfx_shader.sh` 中
- `u_invProj` / `cInvProj` - 在 `uniforms.sh` 中
- `u_GBufferInvSize` / `cGBufferInvSize` - 在 `uniforms.sh` 中
- `u_view` / `cView` - 在 `uniforms.sh` 中
- `u_proj` / `cProj` - 在 `uniforms.sh` 中

---

## 6. BGFX Shader 语法注意事项

### 6.1 vec 构造函数

BGFX 不支持 `vec2(scalar)` 语法，必须使用 `vec2_splat()`：

```glsl
// 错误
vec2 v = vec2(0.0);

// 正确
vec2 v = vec2_splat(0.0);
```

同理：`vec3_splat()`, `vec4_splat()`

### 6.2 数组初始化

使用花括号初始化，不要使用 `float[N](...)` 语法：

```glsl
// 错误
const float weights[5] = float[5](0.227, 0.194, 0.121, 0.054, 0.016);

// 正确
float weights[5];
weights[0] = 0.227;
weights[1] = 0.194;
weights[2] = 0.121;
weights[3] = 0.054;
weights[4] = 0.016;
```

### 6.3 UV Y-Flip 约定

D3D11 和 GL 的 UV 方向不同，需要条件翻转：

```glsl
// D3D11: UV.y=0 是顶部, GL: UV.y=0 是底部
#if !BGFX_SHADER_LANGUAGE_GLSL
    uv.y = 1.0 - uv.y;    // D3D 翻转
#endif
```

**常见错误**：`#if BGFX_SHADER_LANGUAGE_GLSL` → 这是反的，会翻转 GL 而不是 D3D！

### 6.4 矩阵乘法顺序

UrhoX 使用**行向量约定** — 向量在左，矩阵在右：

```glsl
// 正确：向量在左
hvec4 viewPos = mul(clipPos, cInvProj);
hvec4 clipPos = mul(hvec4_init(worldPos, 1.0), cViewProj);

// 错误：向量在右（列向量约定）
hvec4 viewPos = mul(cInvProj, clipPos);
```

参考 `transform.sh` 中的写法：`mul(mul(hvec4_init(worldPos, 1.0), u_view), u_proj)`

---

## 7. RenderPath 配置

### 7.1 Quad Pass 配置

```xml
<command type="quad" tag="mytag" vs="Path/ShaderName" ps="Path/ShaderName">
    <texture unit="0" name="input_texture" />
    <output index="0" name="output_rt" />
    <parameter name="MyParam" value="1.0" />
</command>
```

- `vs` 和 `ps` 指向同一个文件（VS/PS 合并写法）
- `texture unit` 数字对应 Shader 中 SAMPLER 的 register
- `output index` 对应 `gl_FragData[index]` 或 MRT 输出
- `tag` 用于标识 pass，便于调试

### 7.2 RenderTarget 定义

```xml
<rendertarget name="MyBuffer" sizedivisor="1 1" format="rgba16f" />
```

常用格式：

| 格式 | 用途 |
|------|------|
| `rgba` / `rgba16f` | 颜色缓冲 |
| `r32f` | 单通道浮点（深度/HiZ） |
| `rg16f` | 双通道（motion vector） |
| `r8` | 单通道 8 位（AO） |
| `readabledepth` | 可读硬件深度（屏幕空间效果） |

特殊属性：
- `persistent="true"` — 跨帧保留内容（用于历史缓冲：`TAAHistory`, `SSRHistory`）
- `miplevels="5"` — 创建 mipmapped 纹理（用于 HiZ）
- `sizedivisor="2 2"` — 半分辨率

### 7.3 纹理过滤

RenderTarget 默认 **point sampling**。需要 bilinear 时在 `<texture>` 标签加 `filter="true"`：

```xml
<!-- Point sampling（默认）— 用于 HiZ cell 查询 -->
<texture unit="3" name="ClosestHiZ" />

<!-- Point sampling — GTAO 全分辨率采样 HiZ (深度不能插值) -->
<texture unit="1" name="ClosestHiZ" />

<!-- Bilinear filtering — 用于历史帧采样 -->
<texture unit="1" name="TAAHistory" filter="true" />
```

### 7.4 lightvolumes 命令的纹理槽位限制

**重要**：`type="lightvolumes"` 命令会**自动覆盖** slot 5 绑定 IBL specular cubemap！

```xml
<!-- ❌ 错误：slot 5 会被 IBL specular cubemap 覆盖 -->
<command type="lightvolumes" ...>
    <texture unit="5" name="SSAOBlurred" />  <!-- 被覆盖为 cubemap! -->
</command>

<!-- ✅ 正确：使用 slot 14 (TU_AOMAP) -->
<command type="lightvolumes" ...>
    <texture unit="14" name="SSAOBlurred" />  <!-- TU_AOMAP -->
</command>
```

**纹理槽位参考**：

| Slot | 常量 | Desktop | OpenGL ES |
|------|------|---------|-----------|
| 0-3 | - | 安全 | 安全 |
| 4 | TU_ENVIRONMENT | 安全 | **被覆盖** |
| 5 | TU_ENVSPECULAR | **被覆盖** | **被覆盖** |
| 14 | TU_AOMAP | 安全 | 安全 |

### 7.5 GFX 命令

控制引擎渲染状态：

```xml
<!-- 关闭自动深度模板（quad pass 不需要） -->
<command type="gfx" autoGenDepthStencil="false" />

<!-- 恢复自动深度模板（scene pass 需要） -->
<command type="gfx" autoGenDepthStencil="true" />

<!-- 绑定 SSAO Buffer 到引擎管线 (全分辨率上采样后的结果) -->
<command type="gfx" bindSSAOBuffer="SSAOUpscaled" />
```

### 7.6 disableDepthStencilRT

当需要采样 `depth` 同时不使用深度测试时，有两种方式：

**方式一：单个 command 级别**

在 `<command>` 标签上设置 `disableDepthStencilRT="true"`，仅对当前 command 生效：

```xml
<command type="quad" tag="CopyDepth" vs="ScreenSpace/CopyTexture" ps="ScreenSpace/CopyTexture"
         disableDepthStencilRT="true">
    <texture unit="0" name="depth" />
    <output index="0" name="depth_buffer" />
</command>
```

**方式二：批量关闭（推荐连续多个 quad pass 时使用）**

通过 `<command type="gfx" autoGenDepthStencil="false" />` 关闭自动深度模板绑定，之后所有 command 都不再自动绑定 depth stencil RT，相当于全局 `disableDepthStencilRT`：

```xml
<!-- 关闭：之后的所有 command 都不绑定深度模板 -->
<command type="gfx" autoGenDepthStencil="false" />

<!-- 这些 quad pass 都不需要深度模板 -->
<command type="quad" tag="HiZ Init" ...> ... </command>
<command type="quad" tag="GTAO" ...> ... </command>
<command type="quad" tag="SSR Trace" ...> ... </command>

<!-- 恢复：后续 scene pass 需要深度测试 -->
<command type="gfx" autoGenDepthStencil="true" />

<!-- 这个 scene pass 需要深度模板 -->
<command type="scenepass" pass="alpha" depthstencil="depth" ...> ... </command>
```

**注意**：关闭后**必须记得恢复** `autoGenDepthStencil="true"`，否则后续需要深度测试的 scene pass 会工作异常。

---

## 8. Execution 机制（C++ → Shader 参数传递）

### 8.1 基本概念

某些 shader 参数无法在 XML 中静态设置（如帧索引、抖动偏移、矩阵等），需要 C++ 在运行时动态设置。RenderPath 通过 `<execution>` 标签调用 C++ 函数：

```xml
<command type="quad" ...>
    <execution name="ApplyMotionVectorParameters" />
</command>
```

### 8.2 C++ 端实现

在 `View.h` 声明函数：

```cpp
void ApplyMotionVectorParameters(ptrint command);
```

在 `View.cpp` 注册属性并实现：

```cpp
// 属性注册（在 RegisterObject 中）
URHO3D_ACCESSOR_ATTRIBUTE("ApplyMotionVectorParameters",
    ReflectionPropertyPlaceholderPtrGetter, ApplyMotionVectorParameters,
    ptrint, 0, AM_EDIT);

// 函数实现
void View::ApplyMotionVectorParameters(ptrint commandPtrInt)
{
    // 通过 graphics_->SetShaderParameter() 设置 uniform
    Matrix4 invViewProj = (camera_->GetGPUProjection() * camera_->GetView()).Inverse();
    graphics_->SetShaderParameter(StringHash("InvViewProj"), invViewProj);
    graphics_->SetShaderParameter(StringHash("PrevViewProj"), prevViewProj_);
}
```

### 8.3 现有 Execution 函数

| XML name | 用途 | 设置的 Uniform |
|----------|------|---------------|
| `ApplyMotionVectorParameters` | 运动向量生成 | `u_InvViewProj`, `u_PrevViewProj` |
| `ApplySSRTraceParameters` | SSR trace | `u_FrameIndex`, `u_ScreenSize` |
| `ApplySSRTemporalParameters` | SSR 时域降噪 | `u_JitterOffset`, `u_SSRTexelSize` |
| `ApplyTAAResolveParameters` | TAA 解析 | `u_JitterOffset` |

### 8.4 自定义矩阵 vs bgfx 内置矩阵

**关键**：bgfx 内置的组合矩阵（`u_viewProj`, `u_invViewProj`）**不可用**！

原因：
1. bgfx 内部（bx 库）使用**行向量约定**，与 Urho3D 的**列向量约定**不一致
2. `hmat4` 精度损失

解决方案：通过 Execution 传递自定义矩阵：

```cpp
// ✅ 正确：自定义矩阵，列向量约定
Matrix4 viewProj = camera_->GetGPUProjection() * camera_->GetView();
graphics_->SetShaderParameter(StringHash("PrevViewProj"), prevViewProj);

// ❌ 错误：bgfx 内置，行向量约定，精度损失
// shader 中直接用 u_viewProj → 结果错误
```

单独矩阵是安全的（仅转置，无组合）：`u_view` / `cView`, `u_proj` / `cProj`, `u_invProj` / `cInvProj`

---

## 9. 深度缓冲使用规范

### 9.1 可读深度

**`linkDepth="xxx"` 创建的深度是不可读的！** 必须使用 `<rendertarget format="readabledepth">`：

```xml
<!-- ✅ 正确：使用 readabledepth 格式 -->
<rendertarget name="depth" sizedivisor="1 1" format="readabledepth" />
<command type="scenepass" pass="depth" depthstencil="depth" />
<command type="quad" ...>
    <texture unit="0" name="depth" />  <!-- 可以正常读取 -->
</command>
```

### 9.2 深度读写冲突（Depth Read-Write Hazard）

**问题**：某些 pass 需要同时使用深度进行深度测试（`depthstencil="depth"`）和在 shader 中采样深度。这会导致未定义行为。

**解决方案**：拷贝深度到 R32F 纹理，shader 采样拷贝版本：

```xml
<!-- 拷贝深度到 R32F（在需要的 pass 之前） -->
<command type="quad" tag="CopyDepth" vs="ScreenSpace/CopyTexture" ps="ScreenSpace/CopyTexture"
         disableDepthStencilRT="true">
    <texture unit="0" name="depth" />
    <output index="0" name="depth_buffer" />
</command>

<!-- singlelayerwater：深度测试用 depth，shader 采样用 depth_buffer -->
<command type="scenepass" pass="singlelayerwater" depthstencil="depth">
    <texture unit="3" name="depth_buffer" />  <!-- 采样拷贝版本 -->
    <output index="0" name="SceneColor" />
</command>
```

**受影响的 pass**：`singlelayerwater`, `volumetriclight`

---

## 10. 屏幕空间效果架构

### 10.1 共享工具库

```
ScreenSpaceCommon.sh (所有屏幕空间效果共用)
├── ReconstructViewPos(uv, depth)      — UV+深度 → 视空间位置
├── DecodeGBufferNormal(encoded)        — 解码 GBuffer 法线
└── InterleavedGradientNoise(screenPos) — IGN 噪声（Jimenez 2014）

SSRCommon.sh (SSR 专用)
├── CalculateEdgeFade(uv)              — 屏幕边缘衰减
├── CalculateRoughnessFade(r, maxR)    — 粗糙度衰减
├── SsrSpatialHash(screenPos)          — 空间哈希噪声
├── ImportanceSampleGGX(xi, roughness) — GGX 重要性采样
└── TangentToWorld(H, N)              — 切线空间 → 世界空间

GTAOCommon.sh (GTAO 专用)
├── XeGTAO_FastACos(x)                — 快速 acos 近似
├── XeGTAO_HilbertIndex(x, y)        — Hilbert 空间填充曲线索引
├── XeGTAO_SpatioTemporalNoise(x,y,t)— Hilbert + R2 准随机噪声
└── XeGTAO 常量定义 (RADIUS_MULTIPLIER, FALLOFF_RANGE, etc.)
```

### 10.2 Pre-multiplied Alpha 约定

SSR 使用 pre-multiplied alpha 输出格式：

```glsl
// SSR Trace 输出
gl_FragColor = hvec4_init(color.r * confidence, color.g * confidence, color.b * confidence, confidence);
```

- RGB = 反射颜色 × 置信度
- A = 置信度（0 = 无命中/使用 IBL 降级, 1 = 完美命中）
- 优势：时域滤波可以对 4 个通道统一处理

### 10.3 通用纹理拷贝 Shader

`ScreenSpace/CopyTexture.glsl` 是通用的纹理拷贝 shader，用于：
- SSR 历史帧拷贝
- TAA 历史帧拷贝
- 深度拷贝（`depth` → `depth_buffer`）

```glsl
SAMPLER2D(u_Source0, 0);
void PS() { gl_FragColor = texture2D(u_Source0, vTexCoord); }
```

---

## 11. 各效果详解

### 11.1 HiZ 系统

**目的**：为 GTAO 和 SSR 提供层级深度缓冲，支持 `texture2DLod` 在不同 mip 级别采样。

**结构**：
- `ClosestHiZ`（MIN depth）：每个 cell 的最近表面深度 → 用于 SSR ray march
- `FarthestHiZ`（MAX depth）：每个 cell 的最远表面深度 → 预留
- 5 级 mip（0-4），R32F 格式

**生成流程**：
由于 bgfx 不支持同纹理不同 mip 的读写，使用独立 RT 链：

```
depth → HiZInit → ClosestHiZ_Mip0 / FarthestHiZ_Mip0
  → HiZDownsample → Mip1 → Mip2 → Mip3 → Mip4
  → HiZCopy × 5 → ClosestHiZ (mip 0~4) / FarthestHiZ (mip 0~4)
```

**采样方式**：
```glsl
// Point sampling — 用于 HiZ cell traversal（精确 cell 值）
hfloat z = texture2DLod(u_ClosestHiZ, uv, hfloat(mipLevel)).r;

// Bilinear — 用于 GTAO 平滑采样（XML 中 filter="true"）
```

**精度注意**：HiZ 值必须用 `hfloat`（fp32），fp16 会产生量化条纹。

### 11.2 GTAO（XeGTAO 忠实移植）

**参考实现**：Intel XeGTAO (GameTechDev/XeGTAO, MIT License) — `XeGTAO.hlsli`

**核心特性**：
- Per-slice projected normal angle（论文 lines 8-15）
- 完整可见性积分：`IntegrateArc(h, n) = (cosN + 2h·sinN - cos(2h-n)) / 4`
- 距离衰减通过 `mix(lowHorizonCos, shc, weight)` — 非角度缩放
- 功率分布采样：`s²` 聚焦中心附近（捕捉小缝隙）
- 屏幕空间像素半径：`effectRadius / viewZ * proj[0][0] * 0.5 / texelSize.x`

**噪声源**：Hilbert 空间填充曲线 + R2 准随机序列（XeGTAO 原版）
- Hilbert 曲线将 2D 像素映射到 64×64 块内 1D 索引，消除 IGN 的方向性周期条纹
- R2 广义黄金比例常数提供 2D 准随机抖动
- temporal 偏移 `288 × frameIndex` 实现跨帧变化

**质量参数**：3 slices × 3 steps（XeGTAO "High"），可选 Low(1×2) / Medium(2×2) / Ultra(9×3)

**默认参数**：
- `AORadius = 0.5`（× XeGTAO 乘数 1.457）
- `AOIntensity = 2.2`（FinalValuePower）

**半分辨率管线**（匹配 UE4/UE5 `r.GTAO.Downsample=1`）：
```
GTAO (半分辨率) → [Spatial Denoise (可选, enabled=false)]
  → Temporal Filter (MV 重投影 + 邻域 clamp + 10% blend)
    → Copy → History
      → Bilateral Upsample (深度感知 Gaussian 衰减)
        → SSAOUpscaled (全分辨率)
```

- **Spatial Denoise** (`GTAODenoise.glsl`): XeGTAO 原版坡度感知边缘检测 + 非可分离 3×3 核，默认关闭（temporal 已足够）
- **Temporal Filter** (`GTAOTemporal.glsl`): 独立于主 TAA，单通道 LDR 无需 HDR weighting
- **Bilateral Upsample** (`GTAOBilateralUpscale.glsl`): 深度感知 4-tap，防止 AO 跨深度边界渗透

**纹理采样**：
- ClosestHiZ: **point sampling**（深度不能双线性插值）
- SSAOHistory: **bilinear**（temporal 重投影落在亚像素位置）
- MotionVector: **bilinear**（半分辨率采样全分辨率 MV）

### 11.3 Motion Vector

**方法**：深度重投影

```
当前帧 UV + depth → cInvViewProj → worldPos → cPrevViewProj → prevUV
MotionVector = currentUV - prevUV
```

**自定义矩阵**：通过 `ApplyMotionVectorParameters` Execution 传递 `u_InvViewProj` 和 `u_PrevViewProj`（不使用 bgfx 内置）。

**输出**：RG16F，R = 水平运动，G = 垂直运动。

### 11.4 SSR 管线

SSR 采用 4 阶段管线：

```
SSR Trace (半分辨率) → SSR Temporal (降噪) → SSR Copy (历史) → SSR Upscale (全分辨率) → SSR Composite
```

#### 11.4.1 SSR Trace

两种 trace 方法（XML 中 `enabled` 互斥切换）：

**Linear Trace** (`SSRLinearTrace.glsl`):
- 逐像素线性 march（最多 64 步）+ 二分精化（8 步）
- 简单可靠，短距离效果好

**HiZ Trace** (`SSRHiZTrace.glsl`):
- AMD FidelityFX SSSR 的 cell traversal 算法
- `HIZ_MIP_BIAS=1` 适配半分辨率
- 相同迭代次数能覆盖更长光线距离

两者共同特性：
- **GGX 重要性采样**：每像素每帧 1 根光线，通过时域累积收敛
- **IGN 噪声**：两个独立的 IGN 评估（交换坐标 + 不同时域偏移）
- **Pre-multiplied alpha 输出**：`vec4(color * confidence, confidence)`
- **NdotV grazing fade**：`saturate(NdotV * 4.0)`，NdotV < 0.25 时衰减

#### 11.4.2 SSR Temporal Denoise（UE4 SSRTemporalAAPS）

**完全匹配 UE4 PostProcessTemporalCommon.usf 的 SSR 配置**：

| UE4 Flag | 值 | 含义 |
|----------|---|------|
| AA_FILTERED | 1 | BH 3×3 空间滤波 |
| AA_LOWPASS | 1 | 宽 BH (scale×0.25) 作为 AABB clamp 目标 |
| AA_ROUND | 1 | mu±sigma 方差边界（8 样本，排除右下角） |
| AA_AABB | 1 | Ray-AABB clamp，**仅 RGB**（alpha 不修改） |
| AA_ALPHA | 0 | Alpha 作为数据，与 color 一同滤波 |
| AA_TONE | 1 | HDR 感知权重 `HdrWeight4 = 1/(Luma4+4)` |
| AA_LERP | 8 | 固定 12.5% blend |
| AA_CROSS | 0 | 直接运动向量采样（无深度膨胀） |

#### 11.4.3 SSR Bilateral Upscale

半分辨率 → 全分辨率，深度 + 法线边缘感知上采样。

#### 11.4.4 SSR Composite

反射层级系统，能量守恒：

```glsl
finalReflection = envSpecular * (1 - ssrAlpha) + ssrResult.rgb * intensity;
finalColor = sceneLighting + finalReflection;
```

SSR **替换** IBL Specular（非叠加），通过 pre-multiplied alpha 混合。

### 11.5 TAA（UE4 MainTemporalAAPS 忠实移植）

**参考实现**：UE4 PostProcessTemporalCommon.usf, AA_YCOCG=1 路径

**核心配置**：

| UE4 Flag | 值 | 含义 |
|----------|---|------|
| AA_FILTERED | 1 | BH 加权 plus-pattern 空间滤波 |
| AA_YCOCG | 1 | YCoCg 颜色空间 |
| AA_BICUBIC | 1 | Catmull-Rom 双三次历史采样（锐度来源） |
| AA_TONE | 1 | HDR 感知权重 `1/(Y+1)` |
| AA_AABB | 0 | 简单 component-wise clamp |
| AA_ROUND | 0 | Plus-pattern min/max（非 mu±sigma） |
| AA_CROSS | 2 | X-pattern 运动膨胀 2px |
| AA_LOWPASS | 0 | 无宽 lowpass |
| AA_ALPHA | 0 | Alpha 不做 AA |
| Blend | 0.04 | 固定 4% 新帧 |

**锐度来源**：Catmull-Rom 双三次历史采样的负 lobes 自然产生高通增强。**无显式锐化步骤**。

**TAA 抖动**：
- C++ `View::Render()` 应用 Halton(2,3) 序列，8 帧循环
- 偏移 = `(halton - 0.5) / screenSize` → ±0.5 像素抖动
- `u_JitterOffset` 传递给 TAAResolve 用于 BH kernel 重新居中

**管线位置**：所有场景渲染之后，Bloom/Tonemapping 之前。

**SSR + TAA 关系**：SSR 有独立的时域滤波（SSRTemporal），在 TAA 之前运行。SSR Temporal = 降噪，Main TAA = 边缘抗锯齿。两者解决不同问题。

---

## 12. 矩阵约定与坐标系

### 12.1 左手视空间

- `Vector3::FORWARD = (0, 0, 1)` — Z 正方向朝屏幕内
- 投影矩阵：`m32_ = 1.0` → `w_clip = z_view`
- 线性深度比较：`rayZ > sceneZ` 表示光线在表面后方

### 12.2 矩阵乘法约定

| 上下文 | 约定 | 示例 |
|--------|------|------|
| Shader (GLSL) | 行向量 | `mul(vec, mat)` |
| C++ (Urho3D Matrix4) | 列向量 | `Proj * View` |
| bgfx 内部 (bx) | 行向量 | `view * proj` — 不要混用！ |

C++ 的 `SetShaderParameter` 传递行主序数据，GLSL 读取列主序 → 隐式转置。
效果：`mul(v, M_glsl)` ≡ `M_cpp * v`（列向量），所以 C++ 用 `Proj * View` 是正确的。

### 12.3 ViewProj 矩阵

```cpp
// ✅ 正确：Urho3D 列向量约定
Matrix4 viewProj = camera_->GetGPUProjection() * camera_->GetView();

// ❌ 错误：行向量约定
Matrix4 viewProj = camera_->GetView() * camera_->GetGPUProjection();
```

---

## 13. 开发哲学

### 13.1 永远不要自创算法

屏幕空间效果的实现**必须**基于已验证的参考实现，逐行对照移植：

| 效果 | 参考实现 |
|------|---------|
| GTAO | Intel XeGTAO (`XeGTAO.hlsli`) |
| SSR HiZ Trace | AMD FidelityFX SSSR (`ffx_sssr.h`) |
| SSR Temporal | UE4 `PostProcessTemporalCommon.usf` (SSR config) |
| TAA | UE4 `PostProcessTemporalCommon.usf` (Main TAA, AA_YCOCG=1) |

**教训**：自创 GTAO 曾同时存在 3 个 bug（采样半径错误 + 初始视角错误 + 可见性公式错误），XeGTAO 移植首次编译即正确。自创 TAA 锐化（unsharp mask）效果不如 UE4 原生的 Catmull-Rom 双三次采样。

### 13.2 全精度优先

所有屏幕空间效果默认使用 `hfloat`/`hvec*`（fp32）。只有确认 fp16 不会产生 artifact 的场景才降级。

---

## 14. 目录结构

```
Res/Shaders/BLGL/ScreenSpace/
├── ScreenSpaceCommon.sh          # 共享函数（ReconstructViewPos, DecodeGBufferNormal, IGN）
├── CopyTexture.glsl              # 通用纹理拷贝（SSR/TAA 历史 + 深度拷贝）
├── HiZ/
│   ├── HiZInit.glsl              # Mip0 初始化（depth → Closest/Farthest）
│   ├── HiZDownsample.glsl        # Mip chain 降采样（min/max）
│   └── HiZCopy.glsl              # 拷贝到 mipmapped 纹理
├── SSAO/
│   ├── GTAO.glsl                 # XeGTAO 主 pass (Hilbert+R2 noise, 3×3 High)
│   ├── GTAODenoise.glsl          # XeGTAO 空间降噪 (可选, 默认关闭)
│   ├── GTAOTemporal.glsl         # 时域降噪 (MV 重投影 + 邻域 clamp)
│   ├── GTAOBilateralUpscale.glsl # 双边上采样 (半分辨率→全分辨率)
│   ├── SSAOBlur.glsl             # 旧版双边模糊 (已弃用)
│   └── GTAOCommon.sh             # XeGTAO 函数 + Hilbert 曲线 + R2 常量
├── SSR/
│   ├── SSRLinearTrace.glsl       # 线性 march trace
│   ├── SSRHiZTrace.glsl          # HiZ 加速 trace (FidelityFX SSSR)
│   ├── SSRTemporal.glsl          # 时域降噪 (UE4 SSRTemporalAAPS)
│   ├── SSRBilateralUpscale.glsl  # 双边上采样（半分辨率 → 全分辨率）
│   ├── SSRComposite.glsl         # 反射合成（SSR + IBL fallback）
│   └── SSRCommon.sh              # SSR 共享函数（GGX, edge fade）
├── TAA/
│   └── TAAResolve.glsl           # TAA 解析 (UE4 MainTemporalAAPS)
└── MotionVector/
    └── MotionVector.glsl         # 运动向量生成（深度重投影）
```

---

## 15. 常见问题

### Q: Shader 编译报 "redefinition" 错误
A: 检查是否重复声明了 `uniforms.sh` 或 `bgfx_shader.sh` 中已定义的 uniform。特别注意 `DecodeNormal` 已在 `samplers.sh` 中定义，自定义版本需改名（如 `DecodeGBufferNormal`）。

### Q: 纹理采样结果全黑
A: 检查 SAMPLER 变量名的数字后缀是否与 RenderPath 中的 `texture unit` 匹配。

### Q: cGBufferInvSize.zw 报错
A: `cGBufferInvSize` 是 `vec2`，只有 `.xy`，没有 `.zw`。

### Q: Downsample 采样位置不对
A: 记住 `cGBufferInvSize` 是 output RT 的 invSize，如果 input 是 output 的 2 倍大，input 的 texelSize = `cGBufferInvSize * 0.5`。

### Q: 深度纹理采样结果全黑或全 1
A: 检查是否使用了 `linkDepth="depth_buffer"`。`linkDepth` 创建的深度缓冲是**不可读**的，必须使用 `<rendertarget format="readabledepth">` 定义可读深度。

### Q: HiZ/GTAO/SSR 出现水平条纹
A: 几乎一定是精度问题。检查深度相关变量是否使用了 `hfloat`/`hvec*`（fp32）。`float`/`vec*` 是 fp16，无法表示 R32F 深度差异。

### Q: TAA 结果模糊
A: 检查是否使用了 Catmull-Rom 双三次历史采样。这是 UE4 TAA 锐度的唯一来源。不要使用简单 bilinear 采样历史帧，也不要添加 unsharp mask 之类的自创锐化。

### Q: 运动向量在静止场景非零
A: 检查 `u_InvViewProj` 和 `u_PrevViewProj` 是否使用了自定义矩阵（通过 Execution），而不是 bgfx 内置的 `u_viewProj`/`u_invViewProj`。bgfx 内置矩阵约定不同，会导致错误。

### Q: SSR 边缘出现条纹/光晕
A: 检查 SSR Temporal 的 AABB clamp 是否只修改了 RGB（alpha 不动）。如果 alpha 也被 clamp，会在 SSR 边界产生硬切割 → 条纹。

### Q: singlelayerwater / volumetriclight 采样深度异常
A: 这两个 pass 的 `depthstencil="depth"` 和 shader 采样深度冲突。确保 shader 采样 `depth_buffer`（R32F 拷贝），而不是 `depth`。

---

*最后更新: 2026-02-14*
