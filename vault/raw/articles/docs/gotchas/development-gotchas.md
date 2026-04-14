---
summary: "Development gotchas and counter-intuitive rules for UrhoX engine code to avoid repeated pitfalls"
related_paths:
  - engine/Source/**
last_updated: "2026-03-03"
---

# UrhoX 开发陷阱与特殊规则

**目标**: 记录在开发 UrhoX 引擎代码时遇到的特殊坑点、与常识冲突的规则，避免重复踩坑。

**维护规则**: 每次遇到编译错误、意外行为、或与常识不符的规则时，必须更新此文档。

**最后更新**: 2026-03-03

---

## 📋 目录

- [Include 路径规则](#include-路径规则)
- [ImGui 兼容性](#imgui-兼容性)
- [日志系统](#日志系统)
- [CMake 构建系统](#cmake-构建系统)
- [类型系统](#类型系统)
- [平台相关](#平台相关)
- [BGFX Shader 系统](#bgfx-shader-系统)
- [RenderPath 配置](#renderpath-配置)
- [UI 系统](./ui-system-gotchas.md) ⭐ **独立文档**
- [tolua++ 绑定系统](#tolua-绑定系统)
- [UI 控件架构](#ui-控件架构)
- [C++ 标准库](#c-标准库)
- [Lua 脚本](#lua-脚本)
- [性能相关](#性能相关)
- [WebAssembly / 移动平台](#webassembly--移动平台)
- [资源系统](#资源系统)
- [Redis / hiredis](#redis--hiredis)
- [nanopb / Proto](#nanopb--proto)

---

## Include 路径规则

### 🔴 第三方库头文件必须使用完整路径

**错误示例**:
```cpp
#include <nanovg_bgfx.h>  // ❌ 编译失败: file not found
```

**正确示例**:
```cpp
#include <nanovg/nanovg.h>       // ✅ 必须包含目录前缀
#include <nanovg/nanovg_bgfx.h>  // ✅ 必须包含目录前缀
```

**原因**:
- Urho3D 的 include 路径配置为 `ThirdParty/nanovg/` 作为根目录
- 所有 NanoVG 头文件必须使用 `nanovg/` 前缀

**受影响的库**:
- NanoVG: `<nanovg/nanovg.h>`
- BGFX: `<bgfx/bgfx.h>`
- 其他第三方库需要检查 CMakeLists.txt 中的 include_directories 配置

**参考代码**: `engine/Source/Urho3D/UI/NanoVG.cpp:10`

---

### 🔴 必须同时包含 nanovg.h 和 nanovg_bgfx.h

**错误示例**:
```cpp
#include <nanovg/nanovg_bgfx.h>  // ❌ 只包含 BGFX 版本
// 编译失败: nvgBeginFrame/nvgEndFrame 未声明
```

**正确示例**:
```cpp
#include <nanovg/nanovg.h>       // ✅ 基础 API 声明
#include <nanovg/nanovg_bgfx.h>  // ✅ BGFX 扩展
```

**原因**:
- `nanovg.h` 包含核心 API 声明（nvgBeginFrame, nvgRect 等）
- `nanovg_bgfx.h` 只包含 BGFX 特定函数（nvgCreate, nvgSetViewId 等）
- 必须同时包含才能使用完整功能

**触发场景**:
- 使用 `nvgCreate()` 创建 context（需要 nanovg_bgfx.h）
- 调用 `nvgBeginFrame()` 绘制（需要 nanovg.h）

**文件**: `engine/Source/Urho3D/UI/NanoVGLuaHelper.cpp`

---

## ImGui 兼容性

### 🔴 ImGui::BeginDisabled/EndDisabled 不可用

**错误示例**:
```cpp
// ❌ 编译失败: 'BeginDisabled': 找不到标识符
ImGui::BeginDisabled(isDisabled);
if (ImGui::Button("Click Me"))
{
    // ...
}
ImGui::EndDisabled();
```

**正确示例**:
```cpp
// ✅ 使用 PushStyleVar 模拟禁用效果
if (isDisabled)
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, ImGui::GetStyle().Alpha * 0.5f);

if (ImGui::Button("Click Me") && !isDisabled)
{
    // 只在非禁用状态下响应点击
}

if (isDisabled)
    ImGui::PopStyleVar();
```

**原因**:
- `ImGui::BeginDisabled()` / `ImGui::EndDisabled()` 是 ImGui 1.86+ 版本才添加的函数
- UrhoX 使用的是 bgfx 捆绑的旧版 ImGui（位于 `ThirdParty/bgfx-all/bgfx/examples/common/imgui/`）
- 该版本不包含这些较新的 API

**替代方案**:

1. **视觉禁用 + 逻辑检查**（推荐）:
```cpp
bool canClick = !importing && !files.Empty();
if (!canClick)
    ImGui::PushStyleVar(ImGuiStyleVar_Alpha, ImGui::GetStyle().Alpha * 0.5f);
if (ImGui::Button("Start") && canClick)
{
    DoSomething();
}
if (!canClick)
    ImGui::PopStyleVar();
```

2. **条件渲染**（简单场景）:
```cpp
if (!isDisabled)
{
    if (ImGui::Button("Click Me"))
        DoSomething();
}
else
{
    ImGui::TextDisabled("Click Me");  // 显示禁用文本
}
```

**ImGui 版本差异**:

| 功能 | bgfx 捆绑版本 | ImGui 1.86+ |
|------|---------------|-------------|
| `BeginDisabled()` | ❌ | ✅ |
| `EndDisabled()` | ❌ | ✅ |
| `PushStyleVar(Alpha)` | ✅ | ✅ |
| `IsItemDisabled()` | ❌ | ✅ |

**触发场景**:
- 在 UrhoXEditor 工具中使用 ImGui 创建 UI
- 需要禁用按钮或控件时
- 从网上复制 ImGui 示例代码时

**参考**:
- `engine/Source/ThirdParty/bgfx-all/bgfx/examples/common/imgui/imgui.h`
- `engine/Source/Tools/UrhoXEditor/ModelImporter.cpp`
- `engine/Source/Tools/UrhoXEditor/ResourceBrowser.cpp`

**发现时间**: 2025-12-17
**发现者**: Claude (编译错误，多次重复)

---

### 🔴 ImGui 右键菜单 (BeginPopupContextItem) 的正确使用

**问题现象**:
- 右键菜单不弹出
- 空白区域右键无反应
- `BeginPopupContextWindow()` 覆盖了项目的右键菜单

**错误示例 1**: 使用字符串 ID 导致冲突
```cpp
// ❌ 多个项目使用相同的字符串 ID 会冲突
for (int i = 0; i < items.Size(); ++i)
{
    ImGui::Selectable(items[i].name.CString());
    if (ImGui::BeginPopupContextItem("ItemMenu"))  // ❌ 所有项目共用同一 ID
    {
        // ...
        ImGui::EndPopup();
    }
}
```

**正确示例 1**: 使用 PushID + 无参数的 BeginPopupContextItem
```cpp
// ✅ 使用 PushID 确保每个项目有唯一 ID
for (int i = 0; i < items.Size(); ++i)
{
    ImGui::PushID(i);  // ✅ 为每个项目创建唯一 ID 上下文
    ImGui::Selectable(items[i].name.CString());
    if (ImGui::BeginPopupContextItem())  // ✅ 不传参数，使用 LastItemId
    {
        // ...
        ImGui::EndPopup();
    }
    ImGui::PopID();
}
```

**错误示例 2**: 使用 BeginPopupContextWindow 覆盖项目菜单
```cpp
// ❌ BeginPopupContextWindow 会捕获整个窗口的右键，覆盖项目菜单
for (int i = 0; i < items.Size(); ++i)
{
    RenderItem(items[i]);  // 项目有自己的 BeginPopupContextItem
}

// ❌ 这会覆盖上面项目的右键菜单！
if (ImGui::BeginPopupContextWindow())
{
    // ...
    ImGui::EndPopup();
}
```

**正确示例 2**: 空白区域右键使用手动检测
```cpp
for (int i = 0; i < items.Size(); ++i)
{
    RenderItem(items[i]);  // 项目有自己的 BeginPopupContextItem
}

// ✅ 手动检测：窗口悬停 + 无项目悬停 + 右键释放
if (ImGui::IsWindowHovered(ImGuiHoveredFlags_AllowWhenBlockedByPopup) &&
    !ImGui::IsAnyItemHovered() &&
    ImGui::IsMouseReleased(1))
{
    ImGui::OpenPopup("BlankAreaPopup");
}

if (ImGui::BeginPopup("BlankAreaPopup"))
{
    // ...
    ImGui::EndPopup();
}
```

**错误示例 3**: InvisibleButton 不响应右键
```cpp
// ❌ InvisibleButton 在某些情况下不触发 BeginPopupContextItem
ImGui::InvisibleButton("##area", size);
if (ImGui::BeginPopupContextItem())  // ❌ 可能不工作
{
    // ...
}
```

**正确示例 3**: 空目录使用 Selectable 代替
```cpp
// ✅ 使用 Selectable 并隐藏选中效果
ImGui::PushID("EmptyArea");
ImGui::PushStyleColor(ImGuiCol_Header, ImVec4(0, 0, 0, 0));
ImGui::PushStyleColor(ImGuiCol_HeaderHovered, ImVec4(0, 0, 0, 0));
ImGui::PushStyleColor(ImGuiCol_HeaderActive, ImVec4(0, 0, 0, 0));
ImGui::Selectable("No resources found", false, 0, availSize);  // ✅ Selectable 可以响应右键
ImGui::PopStyleColor(3);

if (ImGui::BeginPopupContextItem())  // ✅ 工作正常
{
    // ...
    ImGui::EndPopup();
}
ImGui::PopID();
```

**关键规则总结**:

| 场景 | 正确做法 |
|------|----------|
| 列表中的项目右键 | `PushID(index)` + `BeginPopupContextItem()` (无参数) |
| 空白区域右键（无项目时） | `Selectable` + `BeginPopupContextItem()` |
| 空白区域右键（有项目时） | `IsWindowHovered() + !IsAnyItemHovered() + IsMouseReleased(1)` + `OpenPopup()` |
| 避免覆盖项目菜单 | **不要**使用 `BeginPopupContextWindow()` |

**BeginPopupContextItem 工作原理**:
```cpp
// 源码 imgui.cpp:7833-7844
bool ImGui::BeginPopupContextItem(const char* str_id, ImGuiPopupFlags popup_flags)
{
    ImGuiID id = str_id ? window->GetID(str_id) : window->DC.LastItemId;
    // ↑ 如果不传 str_id，使用上一个控件的 ID
    if (IsMouseReleased(mouse_button) && IsItemHovered(...))
        OpenPopupEx(id, popup_flags);
    return BeginPopupEx(id, ...);
}
```

**触发场景**:
- ResourceBrowser 资源项目右键菜单
- 文件列表、树形视图的右键操作
- 空白区域的右键菜单

**参考**:
- `engine/Source/Tools/UrhoXEditor/ResourceBrowser.cpp:521, 549, 800-817`
- `engine/Source/ThirdParty/bgfx-all/bgfx/3rdparty/dear-imgui/imgui.cpp:7833`

**发现时间**: 2025-12-18
**发现者**: Claude (多次尝试右键菜单不生效)

---

## 日志系统

### 🔴 URHO3D_LOGDEBUG/LOGTRACE 不支持格式化参数

**错误示例**:
```cpp
URHO3D_LOGDEBUG("Value: {}", value);  // ❌ 编译失败: too many arguments to macro
URHO3D_LOGTRACE("Size: {}x{}", width, height);  // ❌ 不支持
```

**正确示例**:

**方式 1: 使用 URHO3D_LOGDEBUGF（推荐）**:
```cpp
URHO3D_LOGDEBUGF("Value: %d", value);  // ✅ printf 风格
URHO3D_LOGTRACEF("Size: %dx%d", width, height);  // ✅
```

**方式 2: 使用字符串拼接**:
```cpp
URHO3D_LOGDEBUG("Value: " + String(value));  // ✅
```

**方式 3: 简化日志**:
```cpp
URHO3D_LOGDEBUG("Operation completed");  // ✅ 不带参数
```

**原因**:
- `URHO3D_LOGDEBUG(message)` 宏定义为: `Urho3D::Log::Write(LOG_DEBUG, message + LOGDETAIL)`
- 只接受一个参数（字符串）
- 不支持类似 fmt/spdlog 的 `{}` 格式化语法

**宏定义位置**: `engine/Source/Urho3D/IO/Log.h:203`

**可用的日志宏**:
```cpp
// 简单日志（字符串参数）
URHO3D_LOGERROR(message)
URHO3D_LOGWARNING(message)
URHO3D_LOGINFO(message)
URHO3D_LOGDEBUG(message)
URHO3D_LOGTRACE(message)

// 格式化日志（printf 风格）
URHO3D_LOGERRORF(format, ...)
URHO3D_LOGWARNINGF(format, ...)
URHO3D_LOGINFOF(format, ...)
URHO3D_LOGDEBUGF(format, ...)
URHO3D_LOGTRACEF(format, ...)
```

**触发场景**:
- 任何需要输出变量值的日志
- 调试信息包含数字、字符串参数

**文件**: `engine/Source/Urho3D/UI/NanoVGLuaHelper.cpp:74, 113, 169, 194`

---

## CMake 构建系统

### 🟢 新增 .cpp/.h 文件无需修改 CMakeLists.txt

**常识预期**:
```cmake
# 通常需要手动添加源文件
add_library(Urho3D
    UI/NanoVG.cpp
    UI/NanoVGLuaHelper.cpp  # ← 需要手动添加？
)
```

**实际情况**:
```cmake
# ✅ Urho3D 使用 GLOB 自动收集
define_source_files(EXCLUDE_PATTERNS ${EXCLUDE_PATTERNS}
                    GLOB_CPP_PATTERNS *.cpp ${GLOB_OBJC_PATTERN}
                    RECURSE GROUP PCH Precompiled.h)
```

**规则**:
- ✅ 在 `engine/Source/Urho3D/` 下新增 `.cpp` 文件会**自动**被包含
- ✅ 无需修改 CMakeLists.txt
- ✅ 只需确保文件在正确的目录下

**例外情况**:
- 如果文件在 `EXCLUDED_SOURCE_DIRS` 中，需要显式添加
- 平台特定文件（如 `.mm` Objective-C 文件）需要特殊处理

**触发场景**:
- 添加新的模块/功能
- 创建新的源文件

**文件**: `engine/Source/Urho3D/CMakeLists.txt:196`

---

### 🔴 MSVC 静态库链接时 DEBUG_POSTFIX 不生效

**问题现象**:
```
LINK : fatal error LNK1181: 无法打开文件 'FreeType.lib'
```

但实际编译出的文件是 `FreeType_d.lib`（带 `_d` 后缀）。

**原因**:
- `setup_library()` 宏设置了 `CMAKE_DEBUG_POSTFIX _d`
- 第三方库（如 FreeType）输出 `FreeType_d.lib`
- 但原代码使用 `LOCATION` 属性获取库路径，生成 `$(Configuration)/FreeType.lib`
- `STATIC_LIBRARY_FLAGS` 不支持根据配置动态调整后缀

**错误代码** (`engine/Source/Urho3D/CMakeLists.txt`):
```cmake
# ❌ LOCATION 属性不会考虑 DEBUG_POSTFIX
get_target_property (ARCHIVE ${TARGET} LOCATION)
set_property (TARGET ${TARGET_NAME} APPEND_STRING PROPERTY STATIC_LIBRARY_FLAGS " \"${ARCHIVE}\"")
```

**正确代码**:
```cmake
# ✅ 对于 MSVC，使用 target_link_libraries 直接链接 target
# CMake 会自动处理 DEBUG_POSTFIX
elseif (MSVC)
    target_link_libraries (${TARGET_NAME} ${TARGET})
```

**注意**:
- 不能使用 `PRIVATE` 关键字，因为同一 target 的其他 `target_link_libraries` 调用使用了无关键字（plain）形式
- CMake 要求同一 target 的所有 `target_link_libraries` 调用必须统一为 all-keyword 或 all-plain

**触发场景**:
- MSVC 静态库构建 (build_editor)
- Debug 配置编译
- 链接第三方静态库

**参考**:
- `engine/Source/Urho3D/CMakeLists.txt:575-578`
- `engine/CMake/Modules/UrhoCommon.cmake:1837` (CMAKE_DEBUG_POSTFIX 定义)

**发现时间**: 2025-12-10
**发现者**: Claude (编译链接错误)

---

### 🟢 .pkg 文件也是自动收集

**常识预期**:
```cmake
# 需要手动注册 .pkg 文件？
```

**实际情况**:
```cmake
# ✅ 自动收集 LuaScript/pkgs/**/*.pkg
file(GLOB API_PKG_FILES LuaScript/pkgs/*.pkg)
file(GLOB PKG_FILES LuaScript/pkgs/${DIR}/*.pkg)
```

**规则**:
- ✅ 在 `LuaScript/pkgs/UI/` 下创建 `.pkg` 文件会自动被 tolua++ 处理
- ✅ 只需在 `UILuaAPI.pkg` 中添加 `$pfile "UI/NanoVG.pkg"` 引用
- ✅ tolua++ 会自动生成 `UILuaAPI.cpp`

**触发场景**:
- 添加新的 Lua 绑定

**文件**: `engine/Source/Urho3D/CMakeLists.txt:288-300`

---

## 类型系统

### 🟡 指针格式化风格

**观察**:
```cpp
// clang-format 会自动调整指针位置
NVGContextWrapper* wrapper  // 原始代码
NVGContextWrapper *wrapper  // clang-format 后
```

**规则**:
- Urho3D 使用 clang-format 自动格式化
- 指针 `*` 靠近变量名而非类型名
- 不要手动调整，让 clang-format 处理

**触发场景**:
- 提交代码时 clang-format 自动运行
- 手动格式化代码

---

## 平台相关

### 🟢 Android TBR GPU 优化必须手动设置

**规则**:
```cpp
// 更加底层bgfx的写法
#ifdef __ANDROID__
bgfx::setViewClear(viewId, BGFX_CLEAR_DISCARD_DEPTH | BGFX_CLEAR_DISCARD_STENCIL);
#endif
```

```cpp
// 引擎图形层的写法
GetSubsystem<Graphics>()->Invalid(CLEAR_DEPTH | CLEAR_STENCIL);
```

**原因**:
- Android 上使用 TBR (Tile-Based Rendering) GPU
- 必须显式 discard depth/stencil 以节省带宽
- 否则性能会下降

**触发场景**:
- 任何使用 BGFX ViewId 的渲染代码
- BeginFrame/EndFrame/CancelFrame

**参考**: `engine/Source/Urho3D/UI/NanoVG.cpp:115, 132, 162`

---

### 🟢 iOS Metal 需要禁用不必要的 Load/Store

**规则**:
```cpp
// 更加底层bgfx的写法
#ifdef IOS
bgfx::setViewDisableAction(viewId,
    BGFX_DISABLE_LOAD_COLOR | BGFX_DISABLE_LOAD_DEPTH |
    BGFX_DISABLE_LOAD_STENCIL | BGFX_DISABLE_STORE_DEPTH |
    BGFX_DISABLE_STORE_STENCIL);
#endif
```

```cpp
// 引擎图形层的写法
GetSubsystem<Graphics>()->DisableLoad(CLEAR_COLOR | CLEAR_DEPTH | CLEAR_STENCIL);
GetSubsystem<Graphics>()->DisableStore(CLEAR_DEPTH | CLEAR_STENCIL);
```

**原因**:
- iOS Metal 后端需要显式禁用不必要的操作
- 提升性能，避免无效的 framebuffer 操作

**触发场景**:
- 离屏渲染（Framebuffer）
- BeginFrame with framebuffer 参数

**参考**: `engine/Source/Urho3D/UI/NanoVG.cpp:118-120`

---

### 🔴 SSAO Rasterize 版本必须使用平台特定的 UV/视空间转换

**错误示例**:
```cpp
// SSAORasterize.cpp - 统一使用 D3D 约定
// ❌ 错误：尝试在所有平台上使用相同的设置
Vec2Set(uniforms_.ndcToViewMul, tanHalfFOVX * 2.0f, tanHalfFOVY * -2.0f);
Vec2Set(uniforms_.ndcToViewAdd, tanHalfFOVX * -1.0f, tanHalfFOVY * 1.0f);
```

```glsl
// vs_fullscreen.glsl - 统一 UV 计算
// ❌ 错误：所有平台使用相同公式
v_texcoord0 = vec2(
    gl_Position.x / gl_Position.w * 0.5 + 0.5,
    -gl_Position.y / gl_Position.w * 0.5 + 0.5);
```

**正确示例**:
```cpp
// SSAORasterize.cpp - 根据渲染器类型区分
if (bgfx::getRendererType() == bgfx::RendererType::OpenGL)
{
    // OpenGL: UV.y=0 在底部，正 Y 乘数
    Vec2Set(uniforms_.ndcToViewMul, tanHalfFOVX * 2.0f, tanHalfFOVY * 2.0f);
    Vec2Set(uniforms_.ndcToViewAdd, tanHalfFOVX * -1.0f, tanHalfFOVY * -1.0f);
}
else
{
    // D3D: UV.y=0 在顶部，负 Y 乘数
    Vec2Set(uniforms_.ndcToViewMul, tanHalfFOVX * 2.0f, tanHalfFOVY * -2.0f);
    Vec2Set(uniforms_.ndcToViewAdd, tanHalfFOVX * -1.0f, tanHalfFOVY * 1.0f);
}
```

```glsl
// vs_fullscreen.glsl - 平台特定 UV 计算
#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
    // OpenGL: UV.y=0 在底部
    v_texcoord0.y = gl_Position.y / gl_Position.w * 0.5 + 0.5;
#else
    // D3D: UV.y=0 在顶部
    v_texcoord0.y = -gl_Position.y / gl_Position.w * 0.5 + 0.5;
#endif
```

```glsl
// fs_prepare_normals.glsl / fs_generate_ao.glsl - OpenGL pixelSize.y 翻转
vec2 pixelSize = u_viewportPixelSize;
#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
    pixelSize.y = -pixelSize.y;
#endif
```

**原因**:
- OpenGL 和 D3D 的纹理 UV 原点不同：OpenGL 在左下角 (Y=0)，D3D 在左上角 (Y=0)
- `ndcToViewMul/Add` 用于将 UV 转换为视空间位置，必须与 UV 约定匹配
- 如果 UV 约定与乘数/加数不匹配，视空间位置的 Y 坐标会反转
- **症状**：水平地板的法线 Y 分量为 0（朝向侧面）而不是 1（朝上）

**必须同时修改的地方**:
1. **C++ (`SSAORasterize.cpp`)**: `ndcToViewMul/Add` 根据渲染器类型设置
2. **VS (`vs_fullscreen.glsl`)**: UV.y 计算根据平台取反或不取反
3. **FS (`fs_prepare_normals.glsl`)**: `pixelSize.y` 在 OpenGL 上取反
4. **FS (`fs_generate_ao.glsl`)**: `pixelSize.y`、`sampleOffset.y`、`pixTDelta/pixBDelta` 符号

**注意**: 检查 GLSL 平台时必须同时检查两个宏：
```glsl
#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
```

**触发场景**:
- 实现基于栅格化的后处理效果（SSAO、DOF 等）
- 从计算着色器版本移植到片段着色器版本
- 需要从深度图重建视空间位置或法线

**参考**:
- 原版计算着色器: `engine/Source/Urho3D/Graphics/SSAO.cpp:563-572`
- 栅格化版本: `engine/Source/Urho3D/Graphics/SSAORasterize.cpp:166-175`
- 详细文档: `docs/SSAORasterize_Implementation.md`

**发现时间**: 2025-11-26
**发现者**: Claude (法线方向错误调试)

---

## BGFX Shader 系统

### 🔴 varying.def.sc 文件不能包含注释

**错误示例**:
```
// HiZ varying definitions  ❌ 注释会导致解析失败
vec2 v_texcoord0 : TEXCOORD0 = vec2(0.0, 0.0);

vec4 a_position  : POSITION;
vec2 a_texcoord0 : TEXCOORD0;
```

**正确示例**:
```
vec2 v_texcoord0 : TEXCOORD0 = vec2(0.0, 0.0);

vec4 a_position  : POSITION;
vec2 a_texcoord0 : TEXCOORD0;
```

**原因**:
- BGFX 的 shader 编译工具 (`shaderc`) 在处理 `varying.def.sc` 文件时不支持注释
- 引擎的 varying 解析器没有实现注释过滤功能
- 任何 `//` 或 `/* */` 样式的注释都会导致解析失败

**触发场景**:
- 创建新的 shader 目录时添加 `varying.def.sc` 文件
- 想要在 varying 文件中添加文档说明

**替代方案**:
- 在同目录下创建单独的 `README.md` 文件记录 varying 说明
- 或在引用该 varying 的 `.glsl` 文件头部添加注释说明

**受影响的文件**:
- `Res/Shaders/BLGL/**/varying.def.sc`
- `Res/Shaders/BLGL/**/varying_*.def.sc`

**发现时间**: 2026-02-05
**发现者**: Claude (屏幕空间算法实现)

---

## RenderPath 配置

### 🔴 linkDepth 创建的深度缓冲不可读

**错误示例**:
```xml
<!-- RenderPath 配置 -->
<command type="clear" depth="1.0" linkDepth="depth_buffer" />
<command type="scenepass" pass="depth" output="depth_buffer" />

<!-- 尝试在 Shader 中采样 -->
<command type="quad" vs="MyShader" ps="MyShader">
    <texture unit="0" name="depth_buffer" />  <!-- ❌ 采样结果全黑或全1 -->
</command>
```

**正确示例**:
```xml
<!-- 定义可读深度 RT -->
<rendertarget name="depth" sizedivisor="1 1" format="readabledepth" />

<command type="clear" depth="1.0" depthstencil="depth" />
<command type="scenepass" pass="depth" depthstencil="depth" />

<command type="quad" vs="MyShader" ps="MyShader">
    <texture unit="0" name="depth" />  <!-- ✅ 可以正常读取 -->
</command>
```

**原因**:
- `linkDepth="depth_buffer"` 创建的是硬件深度/模板缓冲，仅用于深度测试，**不可被 Shader 采样**
- 要在 Shader 中读取深度，必须使用 `<rendertarget format="readabledepth">` 定义可读深度
- 使用 `depthstencil="..."` 属性代替 `linkDepth` 和 `output`

**关键区别**:
| 属性 | `linkDepth` | `depthstencil` + `readabledepth` |
|------|-------------|----------------------------------|
| 用途 | 仅用于深度测试 | 深度测试 + Shader 采样 |
| 可读性 | 不可读 | 可读 |
| 适用场景 | 简单前向渲染 | 屏幕空间效果（SSAO/SSR/HiZ） |

**触发场景**:
- 实现 HiZ、SSAO、SSR 等需要读取深度的屏幕空间效果
- 从其他引擎移植 RenderPath 配置

**发现时间**: 2026-02-06
**发现者**: Claude (屏幕空间算法实现)

---

### 🔴 lightvolumes 命令会覆盖 slot 5 的纹理绑定

**错误示例**:
```xml
<command type="lightvolumes" psdefines="AMBIENT ...">
    <texture unit="5" name="SSAOBuffer" />  <!-- ❌ 被 IBL specular cubemap 覆盖！ -->
</command>
```

**正确示例**:
```xml
<command type="lightvolumes" psdefines="AMBIENT ...">
    <texture unit="4" name="depth" />       <!-- ✅ Desktop 上安全 -->
    <texture unit="14" name="SSAOBuffer" /> <!-- ✅ TU_AOMAP -->
</command>
```

**原因**:
- 引擎的 `Batch.cpp` 在渲染时会**自动绑定** IBL specular cubemap 到 slot 5
- Slot 5 (TU_ENVSPECULAR): 始终被覆盖
- Slot 4 (TU_ENVIRONMENT): **仅在 OpenGL ES 上被覆盖**，Desktop 不受影响

**D3D11 错误信息**:
```
D3D11 ERROR: DEVICE_DRAW_VIEW_DIMENSION_MISMATCH
The Shader Resource View dimension declared in the shader code (TEXTURE2D)
does not match the view type bound to slot 5 (TEXTURECUBE)
```

**槽位安全性**:
| Slot | Desktop | OpenGL ES |
|------|---------|-----------|
| 0-4 | 安全 | 4 被覆盖 |
| 5 | **被覆盖** | **被覆盖** |
| 14 | 安全 | 安全 |

**触发场景**:
- 使用 `type="lightvolumes"`
- 在 slot 5 绑定 2D 纹理

**发现时间**: 2026-02-06
**发现者**: Claude (屏幕空间算法实现)

---

## tolua++ 绑定系统

### 🔴 必须包含完整的头文件路径

**错误示例**:
```cpp
// .pkg 文件
$#include "NanoVGLuaHelper.h"  // ❌ 路径不完整
```

**正确示例**:
```cpp
// .pkg 文件
$#include "UI/NanoVGLuaHelper.h"  // ✅ 相对于 Urho3D/ 的完整路径
```

**原因**:
- tolua++ 从 `engine/Source/Urho3D/LuaScript/pkgs/` 目录运行
- Include 路径必须相对于 `engine/Source/Urho3D/` 根目录

**触发场景**:
- 创建新的 .pkg 文件
- 引用 Urho3D 内部头文件

---

### 🔴 .pkg 文件中第三方库也需要完整路径

**错误示例**:
```cpp
// .pkg 文件
$#include <nanovg.h>  // ❌ 编译失败: file not found
```

**正确示例**:
```cpp
// .pkg 文件
$#include <nanovg/nanovg.h>  // ✅ 必须包含目录前缀
```

**原因**:
- tolua++ 生成的 .cpp 文件会直接使用这些 include 语句
- 第三方库头文件遵循与 C++ 代码相同的 include 路径规则
- 必须使用完整路径（包括目录前缀）

**影响**:
- 编译失败: `fatal error: 'nanovg.h' file not found`
- 即使 C++ 代码可以编译，生成的 Lua 绑定代码也会失败

**触发场景**:
- 在 .pkg 文件中引用第三方库头文件
- tolua++ 生成代码时

**文件**:
- `engine/Source/Urho3D/LuaScript/pkgs/UI/NanoVG.pkg:2`
- `engine/Source/Urho3D/LuaScript/pkgs/UI/NanoVGEnums.pkg:1`
- `engine/Source/Urho3D/LuaScript/pkgs/UI/NanoVGTypes.pkg:1`

**发现时间**: 2025-10-28
**发现者**: Claude (编译错误)

---

### 🟡 Lua 全局变量 `context` 的特殊性

**观察**:
```cpp
// 在 Lua 绑定中获取 Urho3D Context
static Context* GetUrhoContext(lua_State* L)
{
    lua_getglobal(L, "context");  // "context" 是全局变量
    Context* context = (Context*)tolua_tousertype(L, -1, nullptr);
    lua_pop(L, 1);
    return context;
}
```

**规则**:
- Urho3D 在 Lua 环境中自动创建全局变量 `context`
- 可以直接访问获取 Urho3D Context
- 不需要显式传递

**触发场景**:
- 创建需要 Urho3D Context 的对象
- 访问子系统（Graphics, UI, etc.）

**参考**: 其他 .pkg 文件中的 `GetXxx()` 模式

---

### 🔴 tolua++ 无法自动生成复杂参数函数

**错误示例**:
```cpp
// .pkg 文件
// ❌ tolua++ 生成错误代码
tolua_outside void nvgTransformMultiply @ nvgTransformMultiply(float* dst @ [6], const float* src @ [6]);
tolua_outside void nvgTransformPoint @ nvgTransformPoint(float* dstx, float* dsty, const float* xform @ [6], float srcx, float srcy);
tolua_outside int nvgCreateImageRGBA @ nvgCreateImageRGBA(NVGContextWrapper* ctx, int w, int h, int imageFlags, const unsigned char* data);
```

**生成的错误代码**:
```cpp
// 生成的 UILuaAPI.cpp
nvgTransformMultiply(self, &dst, &src);  // ❌ 'self' undeclared (静态函数不需要 self)
nvgCreateImageRGBA(self, ctx, w, h, imageFlags, data);  // ❌ 参数顺序错误
```

**正确做法**: 在 `${}` 块中手动实现

```cpp
// .pkg 文件
// ✅ 移除 tolua_outside 声明，在 ${} 块中手动实现

${
#define TOLUA_DISABLE_tolua_UILuaAPI_nvgTransformMultiply00
static int tolua_UILuaAPI_nvgTransformMultiply00(lua_State* tolua_S)
{
    // 手动从 Lua stack 读取参数
    // 手动调用 C 函数
    // 手动推送返回值
    return 1;
}
$}
```

**tolua++ 无法正确处理的情况**:

1. **多个数组参数**:
   ```cpp
   void func(float* dst @ [6], const float* src @ [6]);  // ❌
   ```

2. **多个输出指针**:
   ```cpp
   void func(float* outX, float* outY, ...);  // ❌
   ```

3. **静态函数（无 context 参数）**:
   ```cpp
   tolua_outside void StaticFunc(float* param);  // ❌ 生成 self 参数
   ```

4. **二进制数据缓冲区**:
   ```cpp
   int func(unsigned char* data, int size);  // ❌
   ```

5. **复杂结构体数组**:
   ```cpp
   int func(NVGglyphPosition* positions, int maxPositions);  // ❌
   ```

**解决方案**:
- 在 `${}` 块中手动编写 Lua C API 代码
- 手动处理参数获取和返回值推送
- 使用 `#define TOLUA_DISABLE_xxx` 禁用自动生成

**影响**:
- 复杂函数需要手动实现（工作量大）
- Phase 1 先实现基础功能，Phase 2 再补充高级功能

**触发场景**:
- 导出带数组参数的函数
- 导出返回多个值的函数
- 导出静态工具函数

**文件**:
- `engine/Source/Urho3D/LuaScript/pkgs/UI/NanoVG.pkg:151-299`
- 生成错误: `build_agent_wasm/Source/Urho3D/LuaScript/generated/UILuaAPI.cpp:4062`

**发现时间**: 2025-10-28
**发现者**: Claude (编译错误)

---

### 🟢 tolua_readonly tolua_property__get_set 是标准语法

**常识预期**:
```lua
// .pkg 文件
tolua_readonly tolua_property__get_set Text* textElement;  // ❌ 这不是冲突吗？
// readonly 和 get_set 同时出现看起来矛盾
```

**实际情况**:
```lua
// .pkg 文件
tolua_readonly tolua_property__get_set Text* textElement;  // ✅ 这是 tolua++ 标准语法！
```

**语义说明**:
- `tolua_property__get_set`: 表示有 getter 和 setter 方法（GetTextElement/SetTextElement）
- `tolua_readonly`: 表示禁止**直接表赋值**
- 组合起来的含义：
  - ✅ `button.textElement` - 通过 GetTextElement() 读取
  - ✅ `button:SetTextElement(text)` - 可以调用 setter
  - ❌ `button.textElement = text` - 禁止直接赋值（触发 readonly 保护）

**实际效果**:
```lua
-- Lua 脚本
local text = button.textElement  -- ✅ 读取，调用 GetTextElement()
-- button.textElement = someText  -- ❌ Lua error: readonly property
```

**代码库中的使用**:
在 UrhoX 代码库中有 **132 处**使用此模式：
- `Graphics/Graphics.pkg` (22处): width, height, fullscreen 等只读属性
- `UI/UIElement.pkg` (8处): screenPosition, numChildren, root 等
- `Graphics/Camera.pkg` (多处): frustum, projection, view 等

**用途场景**:
1. **只读计算属性**: 内部状态派生的值（如 screenPosition = position + parentPosition）
2. **防止误用**: 有 getter/setter 但不希望用户直接赋值（如 textElement 应通过方法控制）
3. **引用返回**: 返回内部对象引用但不允许替换（如 frustum, view matrix）

**触发场景**:
- 为 UI 控件添加内部元素访问器
- 暴露只读的计算属性
- 创建新的 Lua 绑定

**文件**:
- `engine/Source/Urho3D/LuaScript/pkgs/UI/Button.pkg:39`
- `engine/Source/Urho3D/LuaScript/pkgs/Graphics/Graphics.pkg:94-122`

**发现时间**: 2025-11-05
**发现者**: lishuceo (PR #60 反馈)

---

## UI 控件架构

### 🟢 构造函数中创建 internal 子元素是标准模式

**常识预期**:
```cpp
// ❌ 担心构造函数创建子元素会导致 XML 序列化冲突
Button::Button(Context* context) : BorderImage(context)
{
    text_ = CreateChild<Text>("B_Text");  // 这安全吗？
    text_->SetInternal(true);             // XML 加载时会冲突吗？
}
```

**实际情况**:
```cpp
// ✅ 这是 Urho3D UI 控件的标准模式！
Button::Button(Context* context) : BorderImage(context)
{
    text_ = CreateChild<Text>("B_Text");  // ✅ 完全安全
    text_->SetInternal(true);             // ✅ 标记为内部元素
}
```

**Urho3D 引擎中的实现**:

**LineEdit** (`UI/LineEdit.cpp:64-68`):
```cpp
LineEdit::LineEdit(Context* context) : BorderImage(context)
{
    text_ = CreateChild<Text>("LE_Text");
    text_->SetInternal(true);
    cursor_ = CreateChild<BorderImage>("LE_Cursor");
    cursor_->SetInternal(true);
}
```

**ProgressBar** (`UI/ProgressBar.cpp:48-52`):
```cpp
ProgressBar::ProgressBar(Context* context) : BorderImage(context)
{
    knob_ = CreateChild<BorderImage>("S_Knob");
    knob_->SetInternal(true);
    loadingText_ = CreateChild<Text>("S_Text");
    loadingText_->SetInternal(true);
}
```

**ScrollView** (`UI/ScrollView.cpp`):
```cpp
ScrollView::ScrollView(Context* context) : UIElement(context)
{
    scrollPanel_ = CreateChild<UIElement>("SV_ScrollPanel");
    scrollPanel_->SetInternal(true);

    horizontalScrollBar_ = CreateChild<ScrollBar>("SV_HorizontalScrollBar");
    horizontalScrollBar_->SetInternal(true);

    verticalScrollBar_ = CreateChild<ScrollBar>("SV_VerticalScrollBar");
    verticalScrollBar_->SetInternal(true);
}
```

**XML 序列化行为**:
当从 XML 加载 Button 时，Urho3D 序列化系统会：
1. 调用 `Button::Button()` 构造函数（创建 `B_Text` 内部元素）
2. 解析 XML 节点中的属性（如 size, position 等）
3. **检查子元素**: 如果 XML 中有名为 `B_Text` 的子元素：
   - Urho3D 会**找到已存在的 `B_Text`**（通过名称查找）
   - **应用 XML 中的属性**到现有元素（如 fontSize, color 等）
   - **不会创建新元素**，避免冲突
4. 对于 XML 中的其他子元素，正常创建

**SetInternal(true) 的作用**:
- 标记元素为 "内部元素"（引擎控制的子元素）
- XML 序列化时会特殊处理（优先匹配现有 internal 元素）
- 用户可以安全地添加自定义子元素（不同名称）

**使用场景**:
- ✅ Button 的内置 Text
- ✅ LineEdit 的 Text 和 Cursor
- ✅ ProgressBar 的 Knob 和 LoadingText
- ✅ ScrollView 的 ScrollBar 和 ScrollPanel
- ✅ Slider 的 Knob

**规则总结**:
1. ✅ 构造函数中创建内部子元素是 Urho3D 标准模式
2. ✅ 必须调用 `SetInternal(true)` 标记
3. ✅ 使用特殊名称前缀（如 `B_`, `LE_`, `SV_`）避免与用户子元素冲突
4. ✅ XML 加载时 Urho3D 会智能匹配现有 internal 元素

**触发场景**:
- 创建复合 UI 控件
- 为控件添加内置子元素
- 从 XML 加载复杂 UI 布局

**文件**:
- `engine/Source/Urho3D/UI/Button.cpp:54-56`
- `engine/Source/Urho3D/UI/LineEdit.cpp:64-68`
- `engine/Source/Urho3D/UI/ProgressBar.cpp:48-52`
- `engine/Source/Urho3D/UI/ScrollView.cpp:49-60`

**发现时间**: 2025-11-05
**发现者**: lishuceo (PR #60 反馈)

---

## C++ 标准库

### 🟢 static const 类成员可以安全返回引用

**常识预期**:
```cpp
// ❌ 担心返回临时对象的引用导致悬空引用
const String& GetText() const {
    return text_ ? text_->GetText() : String::EMPTY;  // EMPTY 是临时对象吗？
}
```

**实际情况**:
```cpp
// ✅ String::EMPTY 是 static 成员，生命周期贯穿整个程序
// engine/Source/Urho3D/Container/Str.h:589
class String {
    static const String EMPTY;  // ✅ static 类成员
};

// 返回引用完全安全
const String& GetText() const {
    return text_ ? text_->GetText() : String::EMPTY;  // ✅ 安全
}
```

**static const 成员的特性**:
1. **生命周期**: 从程序启动到结束（与全局变量相同）
2. **内存位置**: 位于静态存储区（不在栈上）
3. **线程安全**: 只读访问无需加锁
4. **引用安全**: 可以安全返回引用，永远不会悬空

**类似模式（C++ 标准库）**:
```cpp
// std::string 也有类似的 static 成员
std::string::npos  // static const size_t 成员

// std::vector::max_size() 也返回 static 值的引用
```

**Urho3D 中的其他 static EMPTY 成员**:
```cpp
// Container/Vector.h
template <class T> class Vector {
    static const Vector<T> EMPTY;
};

// Container/HashMap.h
template <class T, class U> class HashMap {
    static const HashMap<T, U> EMPTY;
};

// Scene/Node.h
const Vector<Node*> Node::EMPTY_NODE_VECTOR;
```

**错误的临时对象示例（对比）**:
```cpp
// ❌ 这才是返回临时对象的引用（未定义行为）
const String& GetText() const {
    return String("");  // ❌ 返回临时对象的引用！
    // 临时对象在语句结束后被销毁，引用悬空
}

// ✅ 正确做法：返回 static 成员或按值返回
const String& GetText() const {
    return String::EMPTY;  // ✅ static 成员
}

String GetText() const {
    return String("");  // ✅ 按值返回（RVO 优化）
}
```

**判断依据**:
- ✅ `static const` 成员 → 安全返回引用
- ✅ 全局变量 → 安全返回引用
- ✅ 类成员变量 → 安全返回引用（生命周期与对象绑定）
- ❌ 局部变量 → 不能返回引用（函数返回后销毁）
- ❌ 临时对象 (`String("")`) → 不能返回引用

**触发场景**:
- 返回默认值/空值时
- 实现 getter 方法返回引用
- 需要避免不必要的拷贝

**参考代码**:
```cpp
// Button.cpp:231-234
const String& Button::GetText() const
{
    return text_ ? text_->GetText() : String::EMPTY;  // ✅ 完全安全
}

// 其他类似实现
const Vector3& Node::GetPosition() const
{
    return position_;  // ✅ 成员变量引用
}

const String& Resource::GetName() const
{
    return name_.Empty() ? String::EMPTY : name_;  // ✅ static 或成员
}
```

**文件**:
- `engine/Source/Urho3D/Container/Str.h:589` (String::EMPTY 定义)
- `engine/Source/Urho3D/UI/Button.cpp:231-234` (使用示例)

**发现时间**: 2025-11-05
**发现者**: lishuceo (PR #60 反馈)

---

## Lua 脚本

### 🔴 LuaScriptInstance 二进制序列化与动态属性冲突（待解决）

**问题现象**:
- 使用 `Scene::Save/Load` 二进制序列化场景时，LuaScriptInstance 组件加载失败
- 出现错误的 ScriptObjectType 值（如 "HB" 而非 "Vehicle"）
- 从 XML 文件直接加载同一场景正常工作

**错误流程**:
```cpp
// Play In Editor 模式下
savedSceneData_.Clear();
scene_->Save(savedSceneData_);  // 二进制保存
playScene_->Load(savedSceneData_);  // ❌ 加载失败
```

**正确流程**:
```cpp
// 必须使用 XML 序列化
savedSceneXML_ = new XMLFile(context_);
XMLElement rootElem = savedSceneXML_->CreateRoot("scene");
scene_->SaveXML(rootElem);  // XML 保存
playScene_->LoadXML(savedSceneXML_->GetRoot());  // ✅ 正常工作
```

**根本原因**:

LuaScriptInstance 覆盖了 `GetAttributes()` 返回动态属性列表 `attributeInfos_`：

```cpp
// LuaScriptInstance.h:77
const Vector<AttributeInfo>* GetAttributes() const override { return &attributeInfos_; }
```

**二进制序列化 vs XML 序列化**:

| 方面 | 二进制 `Load()` | XML `LoadXML()` |
|------|----------------|-----------------|
| 循环方式 | `for (i < attributes->Size())` | 遍历 XML 元素 |
| 匹配方式 | 按索引顺序读取 | **按名称匹配** |
| 动态属性影响 | `Size()` 变化会影响循环！ | **不影响** |

**问题发生过程**:
1. **保存时**: Vehicle 脚本对象已存在，`attributeInfos_` = 4个静态属性 + N个动态属性
2. **加载时**: 新创建的 LuaScriptInstance，`attributeInfos_` 只有 4 个静态属性
3. 读取第3个属性 "Script Object Type" = "Vehicle"
4. `SetScriptObjectType("Vehicle")` 被调用，添加动态属性
5. `attributeInfos_.Size()` 从 4 变成 4+N
6. **循环继续**！尝试读取第5个、第6个属性...
7. 但 VectorBuffer 中只有4个静态属性的数据
8. 读取到垃圾数据（如 "HB"）

**临时解决方案**:
Play In Editor 模式使用 XML 序列化代替二进制序列化。

**待解决**: 需要为 LuaScriptInstance 实现自定义的 `Load/Save` 方法，正确处理动态属性。

**触发场景**:
- Play In Editor (PIE) 模式
- 任何需要二进制序列化包含 LuaScriptInstance 组件的场景

**参考**:
- `engine/Source/Urho3D/LuaScript/LuaScriptInstance.h:77` (GetAttributes 覆盖)
- `engine/Source/Urho3D/Scene/Serializable.cpp:293-316` (二进制 Load)
- `engine/Source/Urho3D/Scene/Serializable.cpp:344-417` (XML LoadXML)
- `engine/Source/Tools/UrhoXEditor/UrhoXEditor.cpp:7124-7161` (Play Mode 使用 XML)

**发现时间**: 2025-12-21
**发现者**: Claude (PIE 模式调试)
**状态**: ⚠️ **待解决** - 当前使用 XML 序列化绕过

---

### 🔴 NanoVG 渲染无效 UTF-8 会导致字体系统状态异常

**问题描述**:

NanoVG (fontstash) 的 UTF-8 解码器使用状态机处理多字节字符。当传入无效的 UTF-8 序列时，会导致字体渲染状态异常，影响后续所有文本渲染。

**常见错误 - Lua string.sub 截取 UTF-8 字符**:
```lua
-- ❌ 错误：string.sub 按字节截取，会破坏 UTF-8 序列
local text = "🏷️"
local firstChar = string.sub(text, 1, 1)  -- 返回 "\xF0"（无效 UTF-8）
nvgText(nvg, x, y, firstChar)  -- 传入无效字节，导致状态异常
```

**正确做法**:
```lua
-- ✅ 正确：使用 utf8 库获取完整字符
local text = "🏷️"
local firstChar = text
if utf8 and utf8.offset then
    local endPos = utf8.offset(text, 2)  -- 第二个字符的起始位置
    if endPos then
        firstChar = string.sub(text, 1, endPos - 1)  -- 截取第一个完整字符
    end
end
nvgText(nvg, x, y, firstChar)  -- 传入有效 UTF-8
```

**UTF-8 编码长度参考**:

| 字符类型 | 示例 | 字节数 | `string.sub(s,1,1)` 结果 |
|----------|------|--------|--------------------------|
| ASCII | `"A"` | 1 | `"A"` ✅ |
| 中文 | `"中"` | 3 | `"\xE4"` ❌ 无效 |
| Emoji | `"🏷️"` | 4+ | `"\xF0"` ❌ 无效 |

**技术原因**:

fontstash 使用状态机解码 UTF-8：
```c
// fontstash.h - UTF-8 解码状态机
for (; str != end; ++str) {
    if (fons__decutf8(&utf8state, &codepoint, *str))
        continue;  // 等待后续字节
    glyph = fons__getGlyph(..., codepoint, ...);
}
```

当输入无效 UTF-8 时：
1. UTF-8 状态机卡在"等待后续字节"的中间状态
2. `prevGlyphIndex`（用于 kerning 字距计算）被设置为异常值
3. **状态在帧之间保留**，影响后续渲染
4. 其他文本的 kerning 计算使用了错误的前置字形，导致位置偏移

**症状**:
- 渲染无效 UTF-8 后，其他文本位置偏移
- 停止渲染无效内容后，偏移消失（正常渲染覆盖了异常状态）

**参考**:
- `engine/Source/ThirdParty/bgfx-all/bgfx/examples/common/nanovg/fontstash.h:702-733`

**发现时间**: 2026-01-09

---

### 🔴 Lua 脚本中不能使用 log:Info()

**错误示例**:
```lua
-- Lua 脚本
log:Info("Message")  -- ❌ Runtime error: attempt to call method 'Info' (a nil value)
log:Error("Error")   -- ❌ 同样错误
```

**正确示例**:
```lua
-- Lua 脚本
print("Message")  -- ✅ 使用 print()
```

**原因**:
- Lua 环境中 `log` 对象没有 `Info()`, `Error()` 等方法
- 这些是 C++ 侧的方法，未导出到 Lua
- Lua 应使用标准的 `print()` 函数

**触发场景**:
- 在 Lua 脚本中输出日志信息
- 调试 Lua 代码

**错误信息**:
```
ERROR: Execute Lua function failed: attempt to call method 'Info' (a nil value)
```

**文件**: `engine/bin/Data/LuaScripts/54_NanoVGBasic.lua:26, 43`

**发现时间**: 2025-10-29
**发现者**: 用户（运行时错误）

---

## 性能相关

### 🟡 清理逻辑不应放在热路径

**反面案例** (来自现有代码分析):
```cpp
// engine/Source/Urho3D/UI/NanoVG.cpp:339-354
NVGpaint NanoVG::ImagePattern(...)
{
    ++clearExternalImage_;
    if (clearExternalImage_ > 100)  // ⚠️ 在每次调用时检查
    {
        // 遍历 externalImages_ 清理过期纹理
        // 可能导致性能抖动
    }
}
```

**建议**:
- 清理逻辑应该在 `EndFrame()` 或专门的清理函数中
- 避免在频繁调用的函数（如 ImagePattern）中执行

**触发场景**:
- 资源管理代码
- 缓存清理逻辑

---

## WebAssembly / 移动平台

### 🔴 iOS Safari Web Audio 必须用户交互后才能播放

**问题现象**:
- PC 浏览器 WASM 版本音效正常
- iOS Safari WASM 版本无法播放任何音效
- 控制台可能显示 `AudioContext state: suspended`

**原因**:
- iOS Safari 对 Web Audio API 有严格的自动播放限制
- `AudioContext` 默认处于 `suspended` 状态
- 必须在用户交互事件（触摸/点击）的**同步调用栈**中调用 `resume()`

**引擎层面的处理** (`Audio.cpp:93-112`):
```cpp
// C++ 引擎已有处理，但可能不够可靠
static int TryResumeAudio(void* userdata, SDL_Event* event) {
    switch (event->type) {
    case SDL_FINGERDOWN:
    case SDL_MOUSEBUTTONDOWN:
#ifdef __EMSCRIPTEN__
        EM_ASM({
          if (Module.SDL2.audioContext && !Module.SDL2.audioContext.init) {
            if (Module.SDL2.audioContext.state != 'running') {
                Module.SDL2.audioContext.resume();
            }
            Module.SDL2.audioContext.init = true;
          }
        });
#endif
        break;
    }
    return 1;
}
```

**问题**:
- SDL 事件过滤器的调用时机可能不在用户交互的同步调用栈中
- iOS Safari 比其他浏览器更严格

**解决方案**: 在 HTML 页面添加 JavaScript 层面的音频解锁代码

```javascript
// wasm_player.html / wasm_player_lite.html
(function() {
  var audioUnlocked = false;

  function tryUnlockAudio() {
    if (audioUnlocked) return;

    // 尝试解锁 SDL2 AudioContext
    if (typeof Module !== 'undefined' && Module.SDL2 && Module.SDL2.audioContext) {
      var ctx = Module.SDL2.audioContext;
      if (ctx.state === 'suspended') {
        ctx.resume().then(function() {
          console.log('[Audio] AudioContext resumed');
          audioUnlocked = true;
        });
      } else if (ctx.state === 'running') {
        audioUnlocked = true;
      }
    }
  }

  // 监听用户交互事件
  ['touchstart', 'touchend', 'mousedown', 'click', 'keydown'].forEach(function(event) {
    document.addEventListener(event, function() {
      tryUnlockAudio();
      // 延迟重试，因为 AudioContext 可能在交互后才创建
      setTimeout(tryUnlockAudio, 100);
      setTimeout(tryUnlockAudio, 500);
    }, { passive: true });
  });
})();
```

**修改的文件**:
- `tools/templates/wasm_player.html`
- `tools/templates/wasm_player_lite.html`

**验证方法**:
1. 在 iOS Safari 打开 WASM 页面
2. 点击或触摸屏幕
3. 控制台应显示 `[Audio] AudioContext resumed`
4. 音效应正常播放

**注意事项**:
- 用户**必须**进行交互（点击/触摸）后音频才能播放
- 这是浏览器安全策略，无法绑过
- 建议在游戏开始前添加"点击开始"界面

**触发场景**:
- iOS Safari 上运行 WASM 游戏
- 任何移动端 Safari/Chrome 的 WASM 应用
- 有音效的 Web 游戏

**参考**:
- `engine/Source/Urho3D/Audio/Audio.cpp:93-112` (C++ 端处理)
- `tools/templates/wasm_player.html` (JS 端解锁)
- [Web Audio API Autoplay Policy](https://developer.chrome.com/blog/autoplay/)

**发现时间**: 2025-12-04
**发现者**: 用户 (iOS Safari 无音效)

---

### 🔴 Web/WASM 鼠标滚轮 delta 值比桌面大 100 倍

**问题现象**:
- 桌面平台滚动正常
- Web/WASM 平台滚动非常灵敏，轻轻滚动就跳很远

**原因**:
SDL 在不同平台返回的 wheel delta 值单位不统一：
- **桌面平台**: SDL 返回 ±1（每个滚轮刻度）
- **Web/WASM**: SDL 直接传递浏览器的 `wheelEvent.deltaY`（像素值，通常是 100+）

**SDL Emscripten 源码** (`SDL/src/video/emscripten/SDL_emscriptenevents.c:410`):
```c
// 直接使用浏览器的 deltaY，未做单位转换
SDL_SendMouseWheel(window_data->window, 0, (float)wheelEvent->deltaX, (float)-wheelEvent->deltaY, SDL_MOUSEWHEEL_NORMAL);
```

**解决方案**: 在 Lua 层根据平台调整滚动量

```lua
-- ScrollView.lua
function ScrollView:OnWheel(dx, dy)
    local scrollAmount = 40  -- 桌面: delta=1 × 40 = 40像素/刻度
    if GetPlatform and GetPlatform() == "Web" then
        -- Web: delta≈100 × 0.4 = 40像素/刻度（与桌面一致）
        scrollAmount = 0.4
    end

    if self.props.scrollY then
        self:ScrollBy(0, -dy * scrollAmount)
    end
end
```

**计算方法**:
- 目标：各平台滚动体验一致（约 40 像素/滚轮刻度）
- 桌面：`delta(1) × scrollAmount(40) = 40 像素`
- Web：`delta(100) × scrollAmount(0.4) = 40 像素`
- 公式：`Web_scrollAmount = 桌面_scrollAmount / Web_delta = 40 / 100 = 0.4`

**为什么不在引擎层修复**:
可以在 `Input.cpp` 中统一处理，但需要重新编译引擎：
```cpp
case SDL_MOUSEWHEEL:
    if (!touchEmulation_) {
#ifdef __EMSCRIPTEN__
        int delta = evt.wheel.y > 0 ? 1 : (evt.wheel.y < 0 ? -1 : 0);
        SetMouseWheel(delta);
#else
        SetMouseWheel(evt.wheel.y);
#endif
    }
    break;
```

**触发场景**:
- Web/WASM 应用中的滚动列表
- ScrollView、下拉菜单等需要滚轮的组件

**参考**:
- `engine/Source/Urho3D/Input/Input.cpp:2503-2506` (SDL 事件处理)
- `engine/Source/ThirdParty/SDL/src/video/emscripten/SDL_emscriptenevents.c:407-411` (Emscripten wheel 处理)
- `engine/bin/Data/urhox-libs/UI/Widgets/ScrollView.lua:337-344` (Lua 层修复)

**发现时间**: 2026-01-05
**发现者**: 用户 (Web 滚动太灵敏)

---

### 🔴 Chrome 特定版本 WebGL GPU Instancing 渲染异常

**问题现象**:
- WebGL/WASM 应用中使用 GPU Instancing 渲染的物体三角面完全混乱
- 看起来像是实例矩阵数据错误
- 非实例化渲染正常
- Edge 浏览器正常，Chrome 浏览器异常

**原因**:
Chrome 128.0.6541.235 版本的 ANGLE D3D11 后端存在 WebGL GPU Instancing bug。

**受影响版本**:
- ❌ Chrome 128.0.6541.235 - 有 bug
- ✅ Chrome 128.0.6541.238 - 已修复
- ✅ Edge 144+ - 正常（使用更新的 Chromium 内核）

**解决方案**:
1. **更新浏览器** - 推荐，最简单的解决方案
2. **切换 ANGLE 后端** - 临时方案
   - 打开 `chrome://flags/#use-angle`
   - 尝试切换到 "OpenGL" 或 "D3D11on12"
   - 重启浏览器测试

**排查步骤**:
1. 打开 `chrome://gpu` 查看 ANGLE 配置
2. 对比不同浏览器（Chrome vs Edge）的渲染结果
3. 测试非实例化渲染是否正常
4. 检查浏览器版本号

**注意事项**:
- 这是浏览器/ANGLE 的 bug，不是引擎代码问题
- 如果用户报告 WebGL 实例化渲染异常，首先建议更新浏览器
- Edge 和 Chrome 虽然都基于 Chromium，但版本可能差异很大

**触发场景**:
- WebGL/WASM 应用中使用 GPU Instancing
- 使用 bgfx 的 `glVertexAttribDivisor` 进行实例化渲染
- Chrome 旧版本 + ANGLE D3D11 后端

**发现时间**: 2026-02-04
**发现者**: 开发调试 (WebGL 实例化渲染三角面混乱)

---

## 资源系统

### 🔴 UUID 判定不能依赖固定长度

**错误示例**:
```python
# ❌ 错误：假设 UUID 是 24 字符
def is_uuid(s):
    return len(s) == 24 and is_base64(s)
```

**正确示例**:
```python
# ✅ 正确：只检查字符集，不检查长度
def is_url_safe_base64(s: str) -> bool:
    """URL-safe Base64 字符集：A-Z, a-z, 0-9, -, _"""
    valid_chars = set(string.ascii_letters + string.digits + '-_')
    return all(c in valid_chars for c in s)

def is_uuid(s: str) -> bool:
    # 只含 Base64 字符，无路径特征（无 / \ .）
    if '/' in s or '\\' in s or '.' in s:
        return False
    return is_url_safe_base64(s)
```

**原因**:
- UUID 的生成算法/版本可能变化，长度不固定
- 只依赖字符集判断才能兼容未来变化
- 当前使用 24 字符，但未来可能调整

**判定 UUID 的正确方式**:
1. 只包含 URL-safe Base64 字符（A-Z, a-z, 0-9, -, _）
2. **不包含**路径特征字符（`/`、`\`、`.`）
3. **不检查长度**

**paths 条目优先级判定顺序**:

| 优先级 | 判定条件 | 类型 |
|--------|----------|------|
| 1 | 含 `://` 且非 `http(s)://` | 协议格式 |
| 2 | `http://` 或 `https://` 开头 | 绝对 URL |
| 3 | 在 aliases 中能找到 | 别名 |
| 4 | 含 `/` 或 `\` 或 `.` | 路径/glob |
| 5 | 只含 URL-safe Base64 字符 | UUID |
| 6 | 其他 | 当路径处理 |

**参考**:
- `tools/project-tools/project_builder.py` - `is_url_safe_base64()`, `parse_path_entry()`
- `docs/Project_Build_Pipeline/Project_Builder_Implementation.md`

**发现时间**: 2025-12-08
**发现者**: AI 多次错误假设 24 字符，用户纠正

---

## 待补充的坑点

### 模板

当遇到新的坑点时，按以下格式添加：

```markdown
### 🔴/🟡/🟢 [问题标题]

**错误示例**:
[展示错误代码]

**正确示例**:
[展示正确代码]

**原因**:
[解释为什么会这样]

**触发场景**:
[什么情况下会遇到]

**参考**:
[相关文件和行号]
```

**优先级图例**:
- 🔴 严重（会导致编译失败）
- 🟡 重要（会导致运行时错误或性能问题）
- 🟢 建议（最佳实践）

---

## 快速索引

| 问题 | 严重性 | 关键字 |
|------|--------|--------|
| NanoVG 头文件路径 | 🔴 | `<nanovg/nanovg.h>` |
| ImGui BeginDisabled 不可用 | 🔴 | 使用 `PushStyleVar(Alpha)` 替代 |
| ImGui 右键菜单不生效 | 🔴 | `PushID` + `BeginPopupContextItem()` 无参数；空白区域用手动检测 |
| 日志宏格式化 | 🔴 | `URHO3D_LOGDEBUGF` |
| MSVC DEBUG_POSTFIX 静态库链接 | 🔴 | `target_link_libraries` 代替 `STATIC_LIBRARY_FLAGS` |
| CMake 自动 GLOB | 🟢 | `define_source_files` |
| 指针格式化 | 🟢 | `Type *var` |
| Android TBR 优化 | 🟢 | `BGFX_CLEAR_DISCARD` |
| iOS Metal 优化 | 🟢 | `BGFX_DISABLE_LOAD` |
| tolua++ include 路径 | 🔴 | `$#include "UI/..."` |
| tolua++ 第三方库路径 | 🔴 | `$#include <nanovg/nanovg.h>` |
| tolua++ 复杂参数限制 | 🔴 | 数组/多输出/静态函数需手动实现 |
| Lua log:Info() 不可用 | 🔴 | 使用 `print()` 而非 `log:Info()` |
| LuaScriptInstance 二进制序列化 | 🔴 | 动态属性导致二进制加载失败，使用 XML 序列化 |
| Lua context 全局变量 | 🟡 | `lua_getglobal(L, "context")` |
| 热路径清理 | 🟡 | 避免在频繁调用函数中清理 |
| SSAO Rasterize 平台 UV/视空间 | 🔴 | `ndcToViewMul/Add` 必须与 UV 约定匹配 |
| varying.def.sc 不能有注释 | 🔴 | BGFX varying 解析不支持 `//` 或 `/* */` |
| iOS Safari Web Audio 解锁 | 🔴 | `AudioContext.resume()` 需用户交互 |
| Web/WASM 滚轮 delta 差异 | 🔴 | Web delta 是像素值(~100)，桌面是刻度(±1)，需调整 scrollAmount |
| Chrome WebGL Instancing Bug | 🔴 | Chrome 128.0.6541.235 ANGLE D3D11 实例化渲染异常，更新浏览器解决 |
| nanopb PointerVector `_count` 不可靠 | 🔴 | 解码后用 `.Size()` 而非 `_count`，编码前手动设 `_count` |
| nanopb PointerVector 双重释放 | 🔴 | 不要手动 delete 元素后再 delete 父对象，析构器会自动释放 |

---

## 贡献指南

### 何时添加条目

遇到以下情况时，**必须**更新此文档：

1. ✅ 编译错误（include 路径、宏使用等）
2. ✅ 运行时错误（类型不匹配、未定义行为等）
3. ✅ 性能问题（热路径、内存泄漏等）
4. ✅ 与常识冲突的规则（自动 GLOB、日志宏等）
5. ✅ 平台特定问题（Android, iOS, WASM 等）

### 添加格式

```markdown
### 🔴 [问题简短描述]

**错误示例**:
\`\`\`cpp
// 错误代码
\`\`\`

**正确示例**:
\`\`\`cpp
// 正确代码
\`\`\`

**原因**:
[解释]

**触发场景**:
[什么时候会遇到]

**参考**:
[文件路径:行号]

**发现时间**: YYYY-MM-DD
**发现者**: [名字/AI]
```

---

## 文档维护

### 更新流程

1. **遇到问题** → 记录问题和解决方案
2. **添加条目** → 使用上述格式
3. **更新索引** → 在快速索引表中添加
4. **提交代码** → 与代码修复一起提交文档更新

### Commit Message 模板

```
🐛 fix(xxx): [修复内容]

- [修复说明]
- Update docs/gotchas/development-gotchas.md with discovered issue

Gotcha: [问题简述]
```

---

## Redis / hiredis

### 🔴 hiredis PubSub 双连接要求

- **问题**: hiredis 的 PubSub 模式下，连接进入 subscriber 模式后，只能执行 `SUBSCRIBE`/`UNSUBSCRIBE`/`PING`/`QUIT` 命令。`PUBLISH`/`GET`/`SET`/`HSET` 等命令无法在同一连接上执行。
- **解决**: `RedisClient` 维护两个独立连接：
  - `subCtx`（工作线程）: 专用于 `SUBSCRIBE`，阻塞读取消息
  - `cmdCtx`（主线程）: 用于 `PUBLISH`/`HSET`/`HDEL` 等命令
- **线程安全**: 工作线程**绝不**调用 Urho3D/Lua API，只通过 `ThreadSafeDeque<RedisMessage>` 将消息 push 到主线程，主线程在 `E_BEGINFRAME` 中 drain 并触发回调（与 `HttpClient` 完全一致的模式）。
- **发现时间**: 2026-02-26
- **影响范围**: UrhoXServer Redis PubSub 通信

### 🟢 URHO3D_REDIS 编译选项

- `URHO3D_REDIS` 控制 Redis 支持的编译
- 仅在 Windows/Linux 服务器端可用（`NOT EMSCRIPTEN AND NOT IOS AND NOT ANDROID`）
- hiredis 静态库位于 `3rd/hiredis/`
- Redis 源文件通过显式 GLOB 包含（与 `URHO3D_NETWORK_HTTP` 模式一致）

---

## nanopb / Proto

### 🔴 nanopb PointerVector 的 `_count` 与 `.Size()` 不同步

nanopb 对 proto 中 `repeated` MESSAGE 字段使用 `PointerVector` 存储。`_count` 字段和 `.Size()` 方法**不会自动同步**，这是一个通用陷阱。

**解码陷阱**:
```cpp
CE_PROTO(MyNamespace, MyResponse, res);
CE_DECODE_PROTO(MyNamespace, MyResponse, res, body, bodySize, ok);

// ❌ _count 始终为 0！解码不会更新它
for (pb_size_t i = 0; i < res.items_count; ++i) { ... }  // 永远不执行

// ✅ 使用 .Size() 获取实际解码出的元素数量
for (pb_size_t i = 0; i < res.items.Size(); ++i)
{
    auto* item = static_cast<CEProto_MyNamespace_ItemType*>(res.items.At(i));
}
```

**编码陷阱**:
```cpp
CE_PROTO(MyNamespace, MyRequest, req);
req.items.Push(item1);
req.items.Push(item2);

// ❌ items_count 仍为 0，编码后 repeated 字段为空！
CE_ENCODE_PROTO(MyNamespace, MyRequest, req, buf, bufSize, written, ok);

// ✅ 编码前手动同步 _count
req.items_count = req.items.Size();
CE_ENCODE_PROTO(MyNamespace, MyRequest, req, buf, bufSize, written, ok);
```

**原因**:
- `PointerVector` 是独立的容器，`.Push()` / 解码只操作容器本身
- `_count` 是生成代码中的独立字段，nanopb 编码/解码引擎依赖它来确定元素数量
- 两者之间**没有自动同步机制**

**安全做法**:

| 场景 | 做法 |
|------|------|
| 解码后读取元素 | 用 `.Size()` 而非 `_count` |
| 编码前 | 手动设 `xxx_count = xxx.Size()` |
| 使用 `PROTO_PUSH_REPEATED` 宏 | 宏会同时 `.Push()` 和 `_count += 1`，可以不手动设 |

**触发场景**:
- 任何 proto 定义中有 `repeated MessageType field = N;` 的场景

**发现时间**: 2026-03-03

### 🔴 nanopb PointerVector：不要手动 delete 元素后再 delete 父对象

`PointerVector` 析构函数会自动遍历所有元素并调用注册的 `delete_func_` 释放内存。如果你在 `delete` 父对象之前已经手动 `delete` 了元素指针，就会产生**双重释放 (double-free)**。

```cpp
// 假设 MyRequest 包含 repeated Operation operations = N;
auto* req = NEW_CE_PROTO(MyNamespace, MyRequest);
auto* op = NEW_CE_PROTO(MyNamespace, Operation);
PROTO_PUSH_REPEATED(*req, operations, op);

// ❌ 双重释放！手动 delete + PointerVector 析构器都会释放 op
for (pb_size_t i = 0; i < req->operations.Size(); ++i)
{
    delete static_cast<CEProto_MyNamespace_Operation*>(req->operations.At(i));
}
delete req;  // 💥 ~PointerVector() 再次 delete 同样的指针 → crash

// ✅ 直接 delete 父对象，PointerVector 析构器自动释放所有元素
delete req;  // ~PointerVector() 安全释放所有 Operation
```

**Lua userdata `__gc` 中特别容易犯此错**：
- `NEW_CE_PROTO` 创建的对象放入 Lua userdata
- `__gc` 元方法中清理时，只需 `delete` 顶层对象
- PointerVector 析构会负责释放所有子元素

**发现时间**: 2026-03-03

---

**初始创建**: 2025-10-28
**最后更新**: 2026-03-03
**条目数量**: 26 个
**覆盖领域**: Include 路径、ImGui 兼容性、日志系统、CMake、类型系统、平台优化、tolua++ 绑定、UI 控件架构、C++ 标准库、Lua 脚本、性能、SSAO/后处理、WebAssembly/移动平台、Redis/hiredis、nanopb/Proto
