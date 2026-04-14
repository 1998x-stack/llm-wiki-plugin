---
summary: "Plan to export full NanoVG C API to Lua with transparent BGFX integration wrapper"
status: in_progress
last_updated: "2026-04-02"
read_when:
  - "modifying NanoVG Lua bindings"
  - "adding new NanoVG API to Lua"
  - "working on NanoVG BGFX integration"
---

# NanoVG Lua API 导出开发计划（透明 Wrapper 方案）

**项目目标**: 将 NanoVG C API 完整导出到 Lua，提供 AI Coding 友好的原生风格接口，同时透明管理 BGFX 集成

**核心理念**: 100% 原生 API 体验 + 零 BGFX 学习成本

**预计工期**: 4-6 个工作日

**优先级**: P1 (高优先级 - AI 编程友好核心组件)

---

## 📋 目录

- [1. 项目概述](#1-项目概述)
- [2. 核心设计：透明 Wrapper](#2-核心设计透明-wrapper)
- [3. 技术方案](#3-技术方案)
- [4. 实施阶段](#4-实施阶段)
- [5. 文件清单](#5-文件清单)
- [6. 详细实施步骤](#6-详细实施步骤)
- [7. 测试计划](#7-测试计划)
- [8. 文档计划](#8-文档计划)
- [9. 风险评估](#9-风险评估)
- [10. 验收标准](#10-验收标准)

---

## 1. 项目概述

### 1.1 项目背景

根据 UrhoX "AI 编程友好" 的核心目标，NanoVG Lua API 需要：
- ✅ 最大化 AI 代码生成准确率
- ✅ 直接使用 NanoVG 官方文档和示例
- ✅ 与现有 1000+ GitHub 项目兼容
- ✅ 自动管理 BGFX 集成，对用户透明

### 1.2 设计原则

1. **100% 原生 API** - 完全保持 `nvgXxx(ctx, ...)` 的命名风格
2. **透明的 BGFX 集成** - 自动管理 ViewId，用户无感知
3. **零学习成本** - AI 和开发者可直接参考官方文档
4. **完整的功能覆盖** - 113 个函数 + 所有枚举和类型

### 1.3 核心创新：智能 Context Wrapper

**关键洞察**：在 Context 层面包装 BGFX 集成，而不是在 API 层面修改。

```lua
-- ✅ 用户视角：完全原生的 NanoVG API
local ctx = nvgCreate(1)  -- 只需要 edgeAntiAlias，不需要 viewId

nvgBeginFrame(ctx, width, height, 1.0)  -- 自动管理 ViewId
nvgBeginPath(ctx)
nvgRect(ctx, 10, 10, 100, 50)
nvgFillColor(ctx, nvgRGBA(255, 0, 0, 255))
nvgFill(ctx)
nvgEndFrame(ctx)
```

**用户完全感觉不到 BGFX 的存在！**

---

## 2. 核心设计：透明 Wrapper

### 2.1 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    Lua 用户代码                          │
│   local ctx = nvgCreate(1)                              │
│   nvgBeginFrame(ctx, width, height, 1.0)                │
│   nvgRect(ctx, 10, 10, 100, 50)                         │
│   nvgEndFrame(ctx)                                      │
└────────────────────┬────────────────────────────────────┘
                     │ 100% 原生 API
                     ↓
┌─────────────────────────────────────────────────────────┐
│              NVGContextWrapper (透明层)                  │
│   ┌─────────────────────────────────────────┐           │
│   │ NVGcontext* nvgContext                  │           │
│   │ WeakPtr<Context> urhoContext            │           │
│   └─────────────────────────────────────────┘           │
│                                                          │
│   nvgCreate() → 创建 wrapper + 原生 context              │
│   nvgBeginFrame() → 自动获取 ViewId + 调用原生          │
│   其他函数 → 直接转发到 nvgContext                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│              BGFX 后端 (nanovg_bgfx.h)                   │
│   nvgCreate(edgeAntiAlias, viewId)                      │
│   nvgSetViewId(ctx, viewId)                             │
│   nvgBeginFrame(ctx, width, height, pixelRatio)         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 NVGContextWrapper 设计

```cpp
/// Wrapper for NVGcontext that automatically manages BGFX integration
/// This wrapper is transparent to Lua users - they just see NVGcontext*
struct NVGContextWrapper
{
    NVGcontext* nvgContext;         // 原生 NanoVG context
    WeakPtr<Context> urhoContext;   // Urho3D context (用于获取 Graphics)

    NVGContextWrapper(NVGcontext* ctx, Context* context);
    ~NVGContextWrapper();
};
```

**关键特性**：
- ✅ 对 Lua 完全透明（userdata）
- ✅ 自动管理生命周期
- ✅ 持有 Urho3D Context 引用（用于获取当前 ViewId）

### 2.3 智能函数包装

#### nvgCreate - 简化签名

```cpp
// 原生 BGFX 版本
NVGcontext* nvgCreate(int edgeAntiAlias, bgfx::ViewId viewId);

// ✅ 透明 Wrapper 版本（用户只需一个参数）
NVGContextWrapper* nvgCreate(int edgeAntiAlias);

// 实现
NVGContextWrapper* nvgCreateUrho(Context* urhoContext, int edgeAntiAlias)
{
    // 初始 ViewId 使用 0，会在 BeginFrame 时自动更新
    NVGcontext* ctx = nvgCreate(edgeAntiAlias, 0);
    return new NVGContextWrapper(ctx, urhoContext);
}
```

#### nvgBeginFrame - 自动管理 ViewId

```cpp
// 原生版本
void nvgBeginFrame(NVGcontext* ctx, float width, float height, float pixelRatio);

// ✅ 透明 Wrapper 版本（自动设置 ViewId）
void nvgBeginFrame(NVGContextWrapper* wrapper, float width, float height, float pixelRatio);

// 实现
void nvgBeginFrameUrho(NVGContextWrapper* wrapper, float w, float h, float ratio)
{
    // ✅ 自动从 Graphics 获取当前 ViewId
    if (Context* ctx = wrapper->urhoContext.Get())
    {
        if (Graphics* graphics = ctx->GetSubsystem<Graphics>())
        {
            auto impl = graphics->GetImpl();
            impl->SetViewName("NanoVG");
            impl->StartView();

            // ✅ 自动设置 ViewId
            nvgSetViewId(wrapper->nvgContext, impl->GetView());
        }
    }

    // 调用原生 nvgBeginFrame
    nvgBeginFrame(wrapper->nvgContext, w, h, ratio);
}
```

#### 其他函数 - 直接转发

```cpp
// ✅ 所有其他函数直接转发，零开销
void nvgBeginPath(NVGContextWrapper* wrapper)
{
    nvgBeginPath(wrapper->nvgContext);
}

void nvgRect(NVGContextWrapper* wrapper, float x, float y, float w, float h)
{
    nvgRect(wrapper->nvgContext, x, y, w, h);
}

// ... 其他 110+ 函数类似
```

---

## 3. 技术方案

### 3.1 使用 tolua++ 绑定系统

UrhoX 使用 tolua++ 作为 Lua 绑定工具，需要创建 `.pkg` 文件。

**工具链**:
```
NVGContextWrapper (C++ 类)
    ↓
NanoVG.pkg (tolua++ 包装)
    ↓
tolua++ 生成器
    ↓
NanoVGLuaAPI.cpp (自动生成的绑定代码)
    ↓
链接到 Lua 虚拟机
```

### 3.2 类型映射策略

| C 类型 | Lua 类型 | 说明 |
|--------|----------|------|
| `NVGContextWrapper*` | `userdata` | 透明的智能指针 |
| `NVGcolor` | `table` | `{r, g, b, a}` |
| `NVGpaint` | `userdata` | 复杂结构体 |
| `float[6]` | `table` | 变换矩阵 `{a, b, c, d, e, f}` |
| `const char*` | `string` | 文本 |
| `int` | `number` | 枚举值 |

### 3.3 内存管理策略

```lua
-- ✅ NVGContextWrapper 生命周期由 C++ 管理
local ctx = nvgCreate(1)
-- ... 使用 ctx
nvgDelete(ctx)  -- 自动释放 wrapper 和 原生 context

-- ✅ NVGcolor 是值类型，自动管理
local color = nvgRGBA(255, 0, 0, 255)

-- ✅ NVGpaint 是值类型（返回值）
local paint = nvgLinearGradient(ctx, 0, 0, 100, 100, c1, c2)
-- 自动析构
```

### 3.4 关键实现细节

#### Context 创建与销毁

```cpp
// engine/Source/Urho3D/UI/NanoVGLuaHelper.h
namespace Urho3D
{

struct NVGContextWrapper
{
    NVGcontext* nvgContext;
    WeakPtr<Context> urhoContext;

    NVGContextWrapper(NVGcontext* ctx, Context* context)
        : nvgContext(ctx), urhoContext(context) {}

    ~NVGContextWrapper()
    {
        if (nvgContext)
        {
            nvgDelete(nvgContext);
            nvgContext = nullptr;
        }
    }
};

// Lua 绑定辅助函数
NVGContextWrapper* nvgCreateUrho(Context* urhoContext, int edgeAntiAlias);
void nvgDeleteUrho(NVGContextWrapper* wrapper);
void nvgBeginFrameUrho(NVGContextWrapper* wrapper, float w, float h, float ratio);
void nvgEndFrameUrho(NVGContextWrapper* wrapper);

}
```

#### Lua 绑定宏

```cpp
// 在 .pkg 文件中
${
// 自动从 Lua 获取 Urho3D Context
static Context* GetUrhoContext(lua_State* L)
{
    lua_getglobal(L, "context");
    Context* context = (Context*)tolua_tousertype(L, -1, nullptr);
    lua_pop(L, 1);
    return context;
}

#define TOLUA_DISABLE_tolua_UILuaAPI_nvgCreate00
static int tolua_UILuaAPI_nvgCreate00(lua_State* tolua_S)
{
    int edgeAntiAlias = (int)tolua_tonumber(tolua_S, 1, 1);
    Context* context = GetUrhoContext(tolua_S);

    NVGContextWrapper* wrapper = nvgCreateUrho(context, edgeAntiAlias);
    tolua_pushusertype(tolua_S, wrapper, "NVGContextWrapper");
    return 1;
}

// 所有其他函数从 wrapper 提取 nvgContext 并转发
#define TOLUA_DISABLE_tolua_UILuaAPI_nvgRect00
static int tolua_UILuaAPI_nvgRect00(lua_State* tolua_S)
{
    NVGContextWrapper* wrapper = (NVGContextWrapper*)tolua_tousertype(tolua_S, 1, nullptr);
    float x = (float)tolua_tonumber(tolua_S, 2, 0);
    float y = (float)tolua_tonumber(tolua_S, 3, 0);
    float w = (float)tolua_tonumber(tolua_S, 4, 0);
    float h = (float)tolua_tonumber(tolua_S, 5, 0);

    if (wrapper && wrapper->nvgContext)
        nvgRect(wrapper->nvgContext, x, y, w, h);

    return 0;
}
$}
```

---

## 4. 实施阶段

### Phase 1: 核心框架搭建 (1 天)

**目标**: 建立透明 Wrapper 基础设施

**任务**:
- [x] 创建 `NanoVGLuaHelper.h/cpp`（NVGContextWrapper 定义）
- [x] 实现 `nvgCreateUrho()` / `nvgDeleteUrho()`
- [x] 实现 `nvgBeginFrameUrho()` / `nvgEndFrameUrho()`
- [x] 创建 `NanoVG.pkg` 基础文件
- [x] 验证 tolua++ 生成流程

**验收**: 可以在 Lua 中创建 context 并绘制一个矩形

---

### Phase 2: 核心绘制 API (1.5 天)

**目标**: 实现 80% 的常用绘制功能

#### P0 - 必须（Day 1）
1. **枚举定义** (NanoVGEnums.pkg)
   - 所有 NVG 枚举导出

2. **颜色工具** (7 个函数)
   - `nvgRGBA`, `nvgRGBf`, `nvgHSL`, `nvgLerpRGBA` 等

3. **状态管理** (3 个函数)
   - `nvgSave`, `nvgRestore`, `nvgReset`

4. **路径操作** (15 个函数)
   - `nvgBeginPath`, `nvgMoveTo`, `nvgLineTo`, `nvgClosePath`
   - `nvgRect`, `nvgRoundedRect`, `nvgCircle`, `nvgEllipse`
   - `nvgArc`, `nvgBezierTo`, `nvgQuadTo`
   - `nvgFill`, `nvgStroke`

5. **基本样式** (5 个函数)
   - `nvgFillColor`, `nvgStrokeColor`
   - `nvgStrokeWidth`, `nvgLineCap`, `nvgLineJoin`

#### P1 - 重要（Day 2）
6. **渐变与图案** (4 个函数)
   - `nvgLinearGradient`, `nvgBoxGradient`, `nvgRadialGradient`
   - `nvgImagePattern`

7. **变换** (8 个函数)
   - `nvgResetTransform`, `nvgTransform`, `nvgTranslate`
   - `nvgRotate`, `nvgScale`, `nvgSkewX`, `nvgSkewY`
   - `nvgCurrentTransform`

**验收**: 可以绘制带渐变的复杂形状

---

### Phase 3: 文本与图像 API (1 天)

**目标**: 完整的文本和图像渲染功能

#### 文本 API (19 个函数)
- 字体加载: `nvgCreateFont`, `nvgCreateFontMem`, `nvgFindFont`
- 字体样式: `nvgFontSize`, `nvgFontFace`, `nvgFontBlur`, `nvgTextAlign`
- 文本渲染: `nvgText`, `nvgTextBox`, `nvgTextBounds`, `nvgTextMetrics`
- 高级功能: `nvgTextGlyphPositions`, `nvgTextBreakLines`

#### 图像 API (4 个函数)
- `nvgCreateImageRGBA`, `nvgUpdateImage`, `nvgImageSize`, `nvgDeleteImage`

**验收**: 可以加载字体并渲染文本，加载图像并绘制

---

### Phase 4: 高级工具函数 (0.5 天)

**目标**: 完整的 API 覆盖

#### 变换工具函数 (12 个)
- `nvgTransformIdentity`, `nvgTransformTranslate`, `nvgTransformScale`
- `nvgTransformRotate`, `nvgTransformSkewX`, `nvgTransformSkewY`
- `nvgTransformMultiply`, `nvgTransformPremultiply`, `nvgTransformInverse`
- `nvgTransformPoint`, `nvgDegToRad`, `nvgRadToDeg`

#### 其他功能
- 裁剪: `nvgScissor`, `nvgIntersectScissor`, `nvgResetScissor`
- 混合模式: `nvgGlobalCompositeOperation`, `nvgGlobalCompositeBlendFunc`
- 抗锯齿: `nvgShapeAntiAlias`
- 透明度: `nvgGlobalAlpha`

**验收**: 所有 113 个函数全部导出

---

### Phase 5: 测试与文档 (1-2 天)

**目标**: 确保质量和可用性

#### 测试内容
- 单元测试 (30 个测试用例)
- 集成测试 (3 个完整示例)
- AI 代码生成测试 (ChatGPT/Claude 生成测试)
- 性能测试（Lua vs C++ 开销）

#### 文档内容
- API 参考文档
- Lua 使用指南
- 迁移指南（从官方 C 示例）
- 最佳实践

**验收**: 所有测试通过，文档完整

---

## 5. 文件清单

### 5.1 需要创建的文件

```
engine/Source/Urho3D/UI/
├── NanoVGLuaHelper.h               # NVGContextWrapper 定义 (NEW)
└── NanoVGLuaHelper.cpp             # 智能包装函数实现 (NEW)

engine/Source/Urho3D/LuaScript/pkgs/UI/
├── NanoVG.pkg                      # 主绑定文件 (NEW)
├── NanoVGEnums.pkg                 # 枚举定义 (NEW)
└── NanoVGTypes.pkg                 # 类型定义 (NEW)

engine/Source/Urho3D/LuaScript/pkgs/
└── UILuaAPI.pkg                    # 修改：添加 NanoVG.pkg 引用

engine/Bin/Data/LuaScripts/
└── Examples/
    ├── 51_NanoVGBasic.lua          # 基础示例 (NEW)
    ├── 52_NanoVGText.lua           # 文本示例 (NEW)
    └── 53_NanoVGDashboard.lua      # 复杂示例 (NEW)

docs/
├── NanoVG_Lua_API.md               # API 文档 (NEW)
└── NanoVG_Lua_Migration.md         # 迁移指南 (NEW)
```

### 5.2 需要修改的文件

```
engine/Source/Urho3D/LuaScript/pkgs/UILuaAPI.pkg
  + $pfile "UI/NanoVGEnums.pkg"
  + $pfile "UI/NanoVGTypes.pkg"
  + $pfile "UI/NanoVG.pkg"

engine/Source/Urho3D/CMakeLists.txt
  + add_library(... NanoVGLuaHelper.h NanoVGLuaHelper.cpp)
```

---

## 6. 详细实施步骤

### Step 1: 创建 NVGContextWrapper

**文件**: `engine/Source/Urho3D/UI/NanoVGLuaHelper.h`

```cpp
#pragma once

#include "../Core/Object.h"
#include <nanovg.h>

namespace Urho3D
{

/// Transparent wrapper for NVGcontext with automatic BGFX integration
/// Users see this as NVGcontext* in Lua, but it automatically manages ViewId
struct URHO3D_API NVGContextWrapper
{
    NVGcontext* nvgContext;
    WeakPtr<Context> urhoContext;

    NVGContextWrapper(NVGcontext* ctx, Context* context);
    ~NVGContextWrapper();
};

/// Create NanoVG context with automatic BGFX integration
/// @param urhoContext Urho3D context (for Graphics subsystem access)
/// @param edgeAntiAlias Enable edge anti-aliasing (0 or 1)
/// @return Wrapped NanoVG context
URHO3D_API NVGContextWrapper* nvgCreateUrho(Context* urhoContext, int edgeAntiAlias);

/// Delete NanoVG context
URHO3D_API void nvgDeleteUrho(NVGContextWrapper* wrapper);

/// Begin frame with automatic ViewId management
URHO3D_API void nvgBeginFrameUrho(NVGContextWrapper* wrapper, float windowWidth, float windowHeight, float devicePixelRatio);

/// End frame
URHO3D_API void nvgEndFrameUrho(NVGContextWrapper* wrapper);

/// Cancel frame
URHO3D_API void nvgCancelFrameUrho(NVGContextWrapper* wrapper);

}
```

**文件**: `engine/Source/Urho3D/UI/NanoVGLuaHelper.cpp`

```cpp
#include "../Precompiled.h"
#include "NanoVGLuaHelper.h"
#include "../Graphics/Graphics.h"
#include "../IO/Log.h"

#ifdef URHO3D_BGFX
#include "../Graphics/Bgfx/BgfxGraphicsImpl.h"
#include <nanovg_bgfx.h>
#endif

namespace Urho3D
{

NVGContextWrapper::NVGContextWrapper(NVGcontext* ctx, Context* context)
    : nvgContext(ctx)
    , urhoContext(context)
{
}

NVGContextWrapper::~NVGContextWrapper()
{
    if (nvgContext)
    {
        nvgDelete(nvgContext);
        nvgContext = nullptr;
    }
}

NVGContextWrapper* nvgCreateUrho(Context* urhoContext, int edgeAntiAlias)
{
    if (!urhoContext)
    {
        URHO3D_LOGERROR("nvgCreateUrho: urhoContext is null");
        return nullptr;
    }

#ifdef URHO3D_BGFX
    // Create native NanoVG context (BGFX version)
    // Initial ViewId is 0, will be updated in BeginFrame
    NVGcontext* ctx = nvgCreate(edgeAntiAlias, 0);

    if (!ctx)
    {
        URHO3D_LOGERROR("nvgCreate failed");
        return nullptr;
    }

    return new NVGContextWrapper(ctx, urhoContext);
#else
    URHO3D_LOGERROR("nvgCreateUrho: BGFX backend not enabled");
    return nullptr;
#endif
}

void nvgDeleteUrho(NVGContextWrapper* wrapper)
{
    delete wrapper;
}

void nvgBeginFrameUrho(NVGContextWrapper* wrapper, float windowWidth, float windowHeight, float devicePixelRatio)
{
    if (!wrapper || !wrapper->nvgContext)
        return;

#ifdef URHO3D_BGFX
    // Automatically get current ViewId from Graphics subsystem
    if (Context* context = wrapper->urhoContext.Get())
    {
        if (Graphics* graphics = context->GetSubsystem<Graphics>())
        {
            auto impl = graphics->GetImpl();
            impl->SetViewName("NanoVG");
            impl->StartView();

            // Automatically set ViewId
            bgfx::ViewId viewId = impl->GetView();
            nvgSetViewId(wrapper->nvgContext, viewId);

            // Platform-specific optimizations
#ifdef __ANDROID__
            bgfx::setViewClear(viewId, BGFX_CLEAR_DISCARD_DEPTH | BGFX_CLEAR_DISCARD_STENCIL);
#endif
        }
    }
#endif // URHO3D_BGFX

    // Call native nvgBeginFrame
    nvgBeginFrame(wrapper->nvgContext, windowWidth, windowHeight, devicePixelRatio);
}

void nvgEndFrameUrho(NVGContextWrapper* wrapper)
{
    if (!wrapper || !wrapper->nvgContext)
        return;

    nvgEndFrame(wrapper->nvgContext);

#if defined(URHO3D_BGFX) && defined(__ANDROID__)
    if (Context* context = wrapper->urhoContext.Get())
    {
        if (Graphics* graphics = context->GetSubsystem<Graphics>())
        {
            auto impl = graphics->GetImpl();
            bgfx::setViewClear(impl->GetView(), BGFX_CLEAR_DISCARD_DEPTH | BGFX_CLEAR_DISCARD_STENCIL);
        }
    }
#endif
}

void nvgCancelFrameUrho(NVGContextWrapper* wrapper)
{
    if (wrapper && wrapper->nvgContext)
    {
        nvgCancelFrame(wrapper->nvgContext);
    }
}

} // namespace Urho3D
```

---

### Step 2: 创建枚举定义文件

**文件**: `engine/Source/Urho3D/LuaScript/pkgs/UI/NanoVGEnums.pkg`

```cpp
// NanoVGEnums.pkg
$#include <nanovg.h>

// Winding direction
enum NVGwinding {
    NVG_CCW = 1,
    NVG_CW = 2,
};

// Solidity
enum NVGsolidity {
    NVG_SOLID = 1,
    NVG_HOLE = 2,
};

// Line cap style
enum NVGlineCap {
    NVG_BUTT,
    NVG_ROUND,
    NVG_SQUARE,
    NVG_BEVEL,
    NVG_MITER,
};

// Text alignment
enum NVGalign {
    NVG_ALIGN_LEFT = 1<<0,
    NVG_ALIGN_CENTER = 1<<1,
    NVG_ALIGN_RIGHT = 1<<2,
    NVG_ALIGN_TOP = 1<<3,
    NVG_ALIGN_MIDDLE = 1<<4,
    NVG_ALIGN_BOTTOM = 1<<5,
    NVG_ALIGN_BASELINE = 1<<6,
};

// Blend factors
enum NVGblendFactor {
    NVG_ZERO = 1<<0,
    NVG_ONE = 1<<1,
    NVG_SRC_COLOR = 1<<2,
    NVG_ONE_MINUS_SRC_COLOR = 1<<3,
    NVG_DST_COLOR = 1<<4,
    NVG_ONE_MINUS_DST_COLOR = 1<<5,
    NVG_SRC_ALPHA = 1<<6,
    NVG_ONE_MINUS_SRC_ALPHA = 1<<7,
    NVG_DST_ALPHA = 1<<8,
    NVG_ONE_MINUS_DST_ALPHA = 1<<9,
    NVG_SRC_ALPHA_SATURATE = 1<<10,
};

// Composite operations
enum NVGcompositeOperation {
    NVG_SOURCE_OVER,
    NVG_SOURCE_IN,
    NVG_SOURCE_OUT,
    NVG_ATOP,
    NVG_DESTINATION_OVER,
    NVG_DESTINATION_IN,
    NVG_DESTINATION_OUT,
    NVG_DESTINATION_ATOP,
    NVG_LIGHTER,
    NVG_COPY,
    NVG_XOR,
};

// Image flags
enum NVGimageFlags {
    NVG_IMAGE_GENERATE_MIPMAPS = 1<<0,
    NVG_IMAGE_REPEATX = 1<<1,
    NVG_IMAGE_REPEATY = 1<<2,
    NVG_IMAGE_FLIPY = 1<<3,
    NVG_IMAGE_PREMULTIPLIED = 1<<4,
    NVG_IMAGE_NEAREST = 1<<5,
};
```

---

### Step 3: 创建主 API 绑定文件

**文件**: `engine/Source/Urho3D/LuaScript/pkgs/UI/NanoVG.pkg`

```cpp
// NanoVG.pkg - Transparent wrapper for native NanoVG API
$#include "UI/NanoVGLuaHelper.h"
$#include <nanovg.h>

$using namespace Urho3D;

// Forward declarations
struct NVGContextWrapper;

//
// Context management (transparent BGFX integration)
//

/// Create NanoVG context (automatically manages BGFX ViewId)
/// @param edgeAntiAlias Enable edge anti-aliasing (0=off, 1=on)
/// @return NanoVG context
tolua_outside NVGContextWrapper* nvgCreate @ nvgCreate(int edgeAntiAlias);

/// Delete NanoVG context
/// @param ctx NanoVG context
tolua_outside void nvgDelete @ nvgDelete(NVGContextWrapper* ctx);

//
// Frame control (automatic ViewId management)
//

/// Begin drawing a new frame (automatically sets ViewId from Graphics subsystem)
/// @param ctx NanoVG context
/// @param windowWidth Window width
/// @param windowHeight Window height
/// @param devicePixelRatio Device pixel ratio (usually 1.0)
tolua_outside void nvgBeginFrame @ nvgBeginFrame(NVGContextWrapper* ctx, float windowWidth, float windowHeight, float devicePixelRatio);

/// Cancel drawing the current frame
/// @param ctx NanoVG context
tolua_outside void nvgCancelFrame @ nvgCancelFrame(NVGContextWrapper* ctx);

/// End drawing flushing remaining render state
/// @param ctx NanoVG context
tolua_outside void nvgEndFrame @ nvgEndFrame(NVGContextWrapper* ctx);

//
// Color utils (native API)
//

/// Create color from RGBA values (0-255)
NVGcolor nvgRGBA(unsigned char r, unsigned char g, unsigned char b, unsigned char a);

/// Create color from RGB float values (0.0-1.0)
NVGcolor nvgRGBf(float r, float g, float b);

/// Create color from RGBA float values (0.0-1.0)
NVGcolor nvgRGBAf(float r, float g, float b, float a);

/// Linearly interpolate between two colors
NVGcolor nvgLerpRGBA(NVGcolor c0, NVGcolor c1, float u);

/// Create color from HSL (0.0-1.0)
NVGcolor nvgHSL(float h, float s, float l);

/// Create color from HSLA
NVGcolor nvgHSLA(float h, float s, float l, unsigned char a);

//
// State handling
//

void nvgSave(NVGContextWrapper* ctx);
void nvgRestore(NVGContextWrapper* ctx);
void nvgReset(NVGContextWrapper* ctx);

//
// Render styles
//

void nvgShapeAntiAlias(NVGContextWrapper* ctx, int enabled);
void nvgStrokeColor(NVGContextWrapper* ctx, NVGcolor color);
void nvgStrokePaint(NVGContextWrapper* ctx, NVGpaint paint);
void nvgFillColor(NVGContextWrapper* ctx, NVGcolor color);
void nvgFillPaint(NVGContextWrapper* ctx, NVGpaint paint);
void nvgMiterLimit(NVGContextWrapper* ctx, float limit);
void nvgStrokeWidth(NVGContextWrapper* ctx, float size);
void nvgLineCap(NVGContextWrapper* ctx, int cap);
void nvgLineJoin(NVGContextWrapper* ctx, int join);
void nvgGlobalAlpha(NVGContextWrapper* ctx, float alpha);

//
// Transforms
//

void nvgResetTransform(NVGContextWrapper* ctx);
void nvgTransform(NVGContextWrapper* ctx, float a, float b, float c, float d, float e, float f);
void nvgTranslate(NVGContextWrapper* ctx, float x, float y);
void nvgRotate(NVGContextWrapper* ctx, float angle);
void nvgSkewX(NVGContextWrapper* ctx, float angle);
void nvgSkewY(NVGContextWrapper* ctx, float angle);
void nvgScale(NVGContextWrapper* ctx, float x, float y);

// Transform helper functions (static, no context needed)
void nvgTransformIdentity(float* dst);
void nvgTransformTranslate(float* dst, float tx, float ty);
void nvgTransformScale(float* dst, float sx, float sy);
void nvgTransformRotate(float* dst, float a);
void nvgTransformSkewX(float* dst, float a);
void nvgTransformSkewY(float* dst, float a);
void nvgTransformMultiply(float* dst, const float* src);
void nvgTransformPremultiply(float* dst, const float* src);
int nvgTransformInverse(float* dst, const float* src);
void nvgTransformPoint(float* dstx, float* dsty, const float* xform, float srcx, float srcy);
float nvgDegToRad(float deg);
float nvgRadToDeg(float rad);

//
// Images
//

int nvgCreateImageRGBA(NVGContextWrapper* ctx, int w, int h, int imageFlags, const unsigned char* data);
void nvgUpdateImage(NVGContextWrapper* ctx, int image, const unsigned char* data);
void nvgImageSize(NVGContextWrapper* ctx, int image, int* w, int* h);
void nvgDeleteImage(NVGContextWrapper* ctx, int image);

//
// Paints
//

NVGpaint nvgLinearGradient(NVGContextWrapper* ctx, float sx, float sy, float ex, float ey, NVGcolor icol, NVGcolor ocol);
NVGpaint nvgBoxGradient(NVGContextWrapper* ctx, float x, float y, float w, float h, float r, float f, NVGcolor icol, NVGcolor ocol);
NVGpaint nvgRadialGradient(NVGContextWrapper* ctx, float cx, float cy, float inr, float outr, NVGcolor icol, NVGcolor ocol);
NVGpaint nvgImagePattern(NVGContextWrapper* ctx, float ox, float oy, float ex, float ey, float angle, int image, float alpha);

//
// Scissoring
//

void nvgScissor(NVGContextWrapper* ctx, float x, float y, float w, float h);
void nvgIntersectScissor(NVGContextWrapper* ctx, float x, float y, float w, float h);
void nvgResetScissor(NVGContextWrapper* ctx);

//
// Paths
//

void nvgBeginPath(NVGContextWrapper* ctx);
void nvgMoveTo(NVGContextWrapper* ctx, float x, float y);
void nvgLineTo(NVGContextWrapper* ctx, float x, float y);
void nvgBezierTo(NVGContextWrapper* ctx, float c1x, float c1y, float c2x, float c2y, float x, float y);
void nvgQuadTo(NVGContextWrapper* ctx, float cx, float cy, float x, float y);
void nvgArcTo(NVGContextWrapper* ctx, float x1, float y1, float x2, float y2, float radius);
void nvgClosePath(NVGContextWrapper* ctx);
void nvgPathWinding(NVGContextWrapper* ctx, int dir);
void nvgArc(NVGContextWrapper* ctx, float cx, float cy, float r, float a0, float a1, int dir);
void nvgRect(NVGContextWrapper* ctx, float x, float y, float w, float h);
void nvgRoundedRect(NVGContextWrapper* ctx, float x, float y, float w, float h, float r);
void nvgRoundedRectVarying(NVGContextWrapper* ctx, float x, float y, float w, float h, float radTopLeft, float radTopRight, float radBottomRight, float radBottomLeft);
void nvgEllipse(NVGContextWrapper* ctx, float cx, float cy, float rx, float ry);
void nvgCircle(NVGContextWrapper* ctx, float cx, float cy, float r);
void nvgFill(NVGContextWrapper* ctx);
void nvgStroke(NVGContextWrapper* ctx);

//
// Text
//

int nvgCreateFont(NVGContextWrapper* ctx, const char* name, const char* filename);
int nvgCreateFontMem(NVGContextWrapper* ctx, const char* name, unsigned char* data, int ndata, int freeData);
int nvgFindFont(NVGContextWrapper* ctx, const char* name);
int nvgAddFallbackFontId(NVGContextWrapper* ctx, int baseFont, int fallbackFont);
int nvgAddFallbackFont(NVGContextWrapper* ctx, const char* baseFont, const char* fallbackFont);
void nvgFontSize(NVGContextWrapper* ctx, float size);
void nvgFontBlur(NVGContextWrapper* ctx, float blur);
void nvgTextLetterSpacing(NVGContextWrapper* ctx, float spacing);
void nvgTextLineHeight(NVGContextWrapper* ctx, float lineHeight);
void nvgTextAlign(NVGContextWrapper* ctx, int align);
void nvgFontFaceId(NVGContextWrapper* ctx, int font);
void nvgFontFace(NVGContextWrapper* ctx, const char* font);
float nvgText(NVGContextWrapper* ctx, float x, float y, const char* string, const char* end);
void nvgTextBox(NVGContextWrapper* ctx, float x, float y, float breakRowWidth, const char* string, const char* end);
float nvgTextBounds(NVGContextWrapper* ctx, float x, float y, const char* string, const char* end, float* bounds);
void nvgTextBoxBounds(NVGContextWrapper* ctx, float x, float y, float breakRowWidth, const char* string, const char* end, float* bounds);
int nvgTextGlyphPositions(NVGContextWrapper* ctx, float x, float y, const char* string, const char* end, NVGglyphPosition* positions, int maxPositions);
void nvgTextMetrics(NVGContextWrapper* ctx, float* ascender, float* descender, float* lineh);
int nvgTextBreakLines(NVGContextWrapper* ctx, const char* string, const char* end, float breakRowWidth, NVGtextRow* rows, int maxRows);

${
// Lua binding helper functions

// Get Urho3D Context from Lua global
static Context* GetUrhoContext(lua_State* L)
{
    lua_getglobal(L, "context");
    Context* context = (Context*)tolua_tousertype(L, -1, nullptr);
    lua_pop(L, 1);
    return context;
}

// nvgCreate wrapper
#define TOLUA_DISABLE_tolua_UILuaAPI_nvgCreate00
static int tolua_UILuaAPI_nvgCreate00(lua_State* tolua_S)
{
    int edgeAntiAlias = (int)tolua_tonumber(tolua_S, 1, 1);
    Context* context = GetUrhoContext(tolua_S);

    if (!context)
    {
        tolua_error(tolua_S, "nvgCreate: Urho3D Context not found", nullptr);
        return 0;
    }

    NVGContextWrapper* wrapper = nvgCreateUrho(context, edgeAntiAlias);
    tolua_pushusertype(tolua_S, wrapper, "NVGContextWrapper");
    return 1;
}

// nvgDelete wrapper
#define TOLUA_DISABLE_tolua_UILuaAPI_nvgDelete00
static int tolua_UILuaAPI_nvgDelete00(lua_State* tolua_S)
{
    NVGContextWrapper* wrapper = (NVGContextWrapper*)tolua_tousertype(tolua_S, 1, nullptr);
    nvgDeleteUrho(wrapper);
    return 0;
}

// nvgBeginFrame wrapper
#define TOLUA_DISABLE_tolua_UILuaAPI_nvgBeginFrame00
static int tolua_UILuaAPI_nvgBeginFrame00(lua_State* tolua_S)
{
    NVGContextWrapper* wrapper = (NVGContextWrapper*)tolua_tousertype(tolua_S, 1, nullptr);
    float width = (float)tolua_tonumber(tolua_S, 2, 0);
    float height = (float)tolua_tonumber(tolua_S, 3, 0);
    float pixelRatio = (float)tolua_tonumber(tolua_S, 4, 1.0);

    nvgBeginFrameUrho(wrapper, width, height, pixelRatio);
    return 0;
}

// nvgCancelFrame wrapper
#define TOLUA_DISABLE_tolua_UILuaAPI_nvgCancelFrame00
static int tolua_UILuaAPI_nvgCancelFrame00(lua_State* tolua_S)
{
    NVGContextWrapper* wrapper = (NVGContextWrapper*)tolua_tousertype(tolua_S, 1, nullptr);
    nvgCancelFrameUrho(wrapper);
    return 0;
}

// nvgEndFrame wrapper
#define TOLUA_DISABLE_tolua_UILuaAPI_nvgEndFrame00
static int tolua_UILuaAPI_nvgEndFrame00(lua_State* tolua_S)
{
    NVGContextWrapper* wrapper = (NVGContextWrapper*)tolua_tousertype(tolua_S, 1, nullptr);
    nvgEndFrameUrho(wrapper);
    return 0;
}

// All other functions: auto-forward from wrapper to nvgContext
// (tolua++ will generate these automatically)

$}
```

---

## 7. 测试计划

### 7.1 单元测试

创建 `Tests/NanoVGLuaTest.lua`:

```lua
-- Test 1: Context creation (transparent wrapper)
function TestContextCreation()
    local ctx = nvgCreate(1)
    assert(ctx ~= nil, "Context creation failed")
    nvgDelete(ctx)
    print("✓ Context creation test passed")
end

-- Test 2: Native API style
function TestNativeAPIStyle()
    local ctx = nvgCreate(1)

    -- Should work like native NanoVG
    nvgBeginPath(ctx)
    nvgRect(ctx, 0, 0, 100, 100)
    nvgFillColor(ctx, nvgRGBA(255, 0, 0, 255))
    nvgFill(ctx)

    nvgDelete(ctx)
    print("✓ Native API style test passed")
end

-- Test 3: Automatic ViewId management
function TestAutoViewId()
    local ctx = nvgCreate(1)

    -- BeginFrame should automatically set ViewId
    nvgBeginFrame(ctx, 1024, 768, 1.0)
    nvgEndFrame(ctx)

    nvgDelete(ctx)
    print("✓ Auto ViewId test passed")
end

-- Run all tests
function RunTests()
    TestContextCreation()
    TestNativeAPIStyle()
    TestAutoViewId()
    print("\n✓✓✓ All tests passed! ✓✓✓")
end
```

### 7.2 AI 代码生成测试

使用以下 prompt 测试 AI 生成代码：

```
Prompt: "用 NanoVG Lua API 绘制一个仪表盘"

Expected: AI 生成的代码应该直接可用，无需修改
```

---

## 8. 文档计划

### 8.1 API 参考文档

**文件**: `docs/NanoVG_Lua_API.md`

**重点强调**:
- ✅ 100% 原生 NanoVG API
- ✅ 自动管理 BGFX ViewId
- ✅ 直接参考官方文档

---

## 9. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| tolua++ 不支持 struct 包装 | 低 | 中 | 已验证可行 |
| ViewId 获取失败 | 低 | 高 | 添加错误检查和日志 |
| 性能开销 | 低 | 中 | BeginFrame 只查询一次 |

---

## 10. 验收标准

### 10.1 功能完整性

- [ ] 所有 113 个 NanoVG 函数已导出
- [ ] nvgCreate 只需一个参数（edgeAntiAlias）
- [ ] nvgBeginFrame 自动管理 ViewId
- [ ] 所有其他函数保持原生 API 风格

### 10.2 质量标准

- [ ] AI 代码生成测试通过率 > 95%
- [ ] 用户无需理解 BGFX 概念
- [ ] 官方 NanoVG 示例可直接翻译

### 10.3 性能标准

- [ ] Wrapper 开销 < 1% (只在 BeginFrame 查询 ViewId)
- [ ] 其他函数直接转发，零开销

---

## 附录 A: 使用示例对比

### ❌ 传统方案（需要管理 ViewId）

```lua
local ctx = nvgCreate(1, viewId)  -- 需要 viewId
nvgSetViewId(ctx, newViewId)  -- 需要手动切换
```

### ✅ 透明 Wrapper 方案（推荐）

```lua
local ctx = nvgCreate(1)  -- 不需要 viewId
nvgBeginFrame(ctx, width, height, 1.0)  -- 自动管理
```

---

**计划制定完成时间**: 2025-10-28 (Updated)
**计划版本**: v2.0 (Transparent Wrapper)
**计划状态**: 待审核
