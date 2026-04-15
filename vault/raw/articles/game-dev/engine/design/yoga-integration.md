---
summary: "Facebook Yoga flexbox layout engine integration guide for UrhoX UI system"
related_paths:
  - engine/Source/Urho3D/UI/**
last_updated: "2025-12-31"
---

# Yoga Flexbox 布局库集成指南

**版本**: Facebook Yoga (from GitHub)
**集成日期**: 2025-12-31
**维护者**: Claude

---

## 概述

Yoga 是 Facebook 开源的跨平台 Flexbox 布局引擎，用于在 UrhoX 中提供现代化的 UI 布局能力。本文档记录 Yoga 集成到 UrhoX 的完整过程，包括 C++ 标准降级、平台适配和 Lua 绑定。

---

## 目录

- [C++20 到 C++17 降级](#c20-到-c17-降级)
- [CMake 配置](#cmake-配置)
- [Android 平台链接](#android-平台链接)
- [Lua 绑定](#lua-绑定)
- [修改文件清单](#修改文件清单)

---

## C++20 到 C++17 降级

### 背景

Yoga 库原生使用 C++20 标准，但 UrhoX 需要支持 Android NDK 21.3.6528147（Clang 9），该版本仅支持 C++17。因此需要将 Yoga 降级到 C++17。

### C++20 特性及替代方案

| C++20 特性 | 替代方案 | 修改文件 |
|-----------|---------|---------|
| `concept` / `<concepts>` | `std::enable_if` + type traits | `YogaEnums.h` |
| `std::bit_width` | 自定义 `detail::bit_width_impl` | `YogaEnums.h` |
| `std::bit_cast` | `memcpy` 实现的 polyfill | `StyleValuePool.h` |
| `auto` 函数参数 | 显式模板参数 | `Comparison.h` |
| `[[likely]]` / `[[unlikely]]` | 移除 | 多个文件 |
| 位域默认成员初始化器 | 构造函数初始化列表 | `LayoutResults.h`, `Style.h`, `Node.h` |
| 指定初始化器 `{.member=}` | 传统聚合初始化 | `Node.cpp`, `FlexLine.cpp` |
| `std::input_iterator` concept | 移除 static_assert | `LayoutableChildren.h` |
| 自动生成 `operator!=` | 手动实现 | `StyleSizeLength.h`, `StyleLength.h`, `CachedMeasurement.h` |

### 详细修改

#### 1. CMake 标准设置

**文件**: `3rd/yoga/cmake/project-defaults.cmake`

```cmake
# 修改前
set(CMAKE_CXX_STANDARD 20)

# 修改后
set(CMAKE_CXX_STANDARD 17)
```

#### 2. Concepts 替换为 Type Traits

**文件**: `3rd/yoga/yoga/enums/YogaEnums.h`

```cpp
// 修改前 (C++20)
#include <concepts>

template <typename EnumT>
concept Enumeration = std::is_enum_v<EnumT>;

template <Enumeration EnumT>
constexpr auto to_underlying(EnumT e) noexcept {
  return static_cast<std::underlying_type_t<EnumT>>(e);
}

// 修改后 (C++17)
#include <type_traits>

template <typename EnumT>
struct is_enumeration : std::is_enum<EnumT> {};

template <typename EnumT>
inline constexpr bool is_enumeration_v = is_enumeration<EnumT>::value;

template <typename EnumT, typename = std::enable_if_t<is_enumeration_v<EnumT>>>
constexpr auto to_underlying(EnumT e) noexcept {
  return static_cast<std::underlying_type_t<EnumT>>(e);
}
```

#### 3. std::bit_width Polyfill

**文件**: `3rd/yoga/yoga/enums/YogaEnums.h`

```cpp
// 修改前 (C++20)
#include <bit>
constexpr size_t ordinalCount = std::bit_width(ordinal(lastValue));

// 修改后 (C++17)
namespace detail {
template <typename T>
constexpr int bit_width_impl(T value) noexcept {
  int width = 0;
  while (value > 0) {
    value >>= 1;
    ++width;
  }
  return width;
}
}

constexpr size_t ordinalCount =
    static_cast<size_t>(detail::bit_width_impl(ordinal(lastValue)));
```

#### 4. std::bit_cast Polyfill

**文件**: `3rd/yoga/yoga/style/StyleValuePool.h`

```cpp
// 修改前 (C++20)
#include <bit>
return std::bit_cast<SmallValue>(repr);

// 修改后 (C++17)
#include <cstring>

namespace detail {
template <typename To, typename From>
To bit_cast(const From& src) noexcept {
  static_assert(sizeof(To) == sizeof(From), "Size mismatch");
  To dst;
  std::memcpy(&dst, &src, sizeof(To));
  return dst;
}
}

return detail::bit_cast<SmallValue>(repr);
```

#### 5. Auto 函数参数替换

**文件**: `3rd/yoga/yoga/numeric/Comparison.h`

```cpp
// 修改前 (C++20)
constexpr bool inexactEquals(const auto& a, const auto& b) {
  return a == b;
}

// 修改后 (C++17)
template <typename T, typename U>
constexpr bool inexactEquals(const T& a, const U& b) {
  return a == b;
}
```

#### 6. 位域构造函数

**文件**: `3rd/yoga/yoga/node/LayoutResults.h`

```cpp
// 修改前 (C++20) - 位域默认初始化
struct LayoutResults {
  uint32_t direction : 2 = 0;
  uint32_t hadOverflow : 1 = 0;
  // ...
};

// 修改后 (C++17) - 构造函数初始化
struct LayoutResults {
  uint32_t direction : 2;
  uint32_t hadOverflow : 1;
  // ...

  LayoutResults()
      : direction(0)
      , hadOverflow(0)
      // ...
  {}
};
```

#### 7. 指定初始化器替换

**文件**: `3rd/yoga/yoga/algorithm/FlexLine.cpp`

```cpp
// 修改前 (C++20)
FlexItem item = {
    .node = child,
    .mainAxisSize = 0.0f,
    // ...
};

// 修改后 (C++17)
FlexItem item;
item.node = child;
item.mainAxisSize = 0.0f;
// ...
```

#### 8. 移除 std::input_iterator

**文件**: `3rd/yoga/yoga/node/LayoutableChildren.h`

```cpp
// 修改前 (C++20)
#include <iterator>
static_assert(std::input_iterator<Iterator>);

// 修改后 (C++17)
// 移除 #include <iterator>
// 移除 static_assert
```

#### 9. 添加 operator!=

**文件**: `3rd/yoga/yoga/style/StyleSizeLength.h`, `StyleLength.h`, `node/CachedMeasurement.h`

```cpp
// 修改前 (C++20) - 自动生成 operator!=
bool operator==(const StyleLength& other) const { ... }
// operator!= 由编译器自动生成

// 修改后 (C++17) - 手动实现
bool operator==(const StyleLength& other) const { ... }

bool operator!=(const StyleLength& other) const {
  return !(*this == other);
}
```

---

## CMake 配置

### 添加 Yoga 子目录

**文件**: `3rd/CMakeLists.txt`

```cmake
# Yoga layout library
add_subdirectory(yoga/yoga)
set_target_properties(yogacore PROPERTIES FOLDER "ThirdParty")
```

### 引擎 Include 路径

**文件**: `engine/Source/Urho3D/CMakeLists.txt`

```cmake
# Yoga layout library
list (APPEND INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/../../../3rd/yoga)
```

### 引擎链接

**文件**: `engine/Source/Urho3D/CMakeLists.txt`

```cmake
target_link_libraries(${TARGET_NAME} yogacore)
```

---

## Android 平台链接

### 问题

Android 构建时，某些第三方库（如 `lua54`, `7z`, `yogacore`）不会被合并到 `libUrho3D.a`，也不会被 Gradle 自动复制，需要在 `UrhoXRuntime` 中显式链接。

### 解决方案

**文件**: `engine/Source/Tools/UrhoXRuntime/CMakeLists.txt`

```cmake
# On Android, lua54, 7z, and yogacore are built separately (not merged into libUrho3D.a)
# and not copied by Gradle. Link them explicitly here.
if (ANDROID)
    target_link_libraries (${TARGET_NAME} ${LUA_LIB_NAME})
    target_link_libraries (${TARGET_NAME} 7z)
    target_link_libraries (${TARGET_NAME} yogacore)
endif ()
```

### 验证

构建 Android 时，检查链接输出是否包含 `libyogacore.a`。

---

## Lua 绑定

### 文件结构

```
engine/Source/Urho3D/LuaScript/pkgs/UI/
├── YogaEnums.pkg      # 枚举定义
└── YogaLayout.pkg     # 主要 API 绑定
```

### API 命名约定

- Lua 函数使用 `YG` 前缀大写：`YGNodeNew()`, `YGNodeStyleSetWidth()`
- 枚举保持原命名：`YGFlexDirectionRow`, `YGJustifyCenter`
- 与 Yoga 原生 C API 命名一致

### 主要 API

**节点管理**:
- `YGNodeNew()` - 创建节点
- `YGNodeFree()` / `YGNodeFreeRecursive()` - 释放节点
- `YGNodeInsertChild()` / `YGNodeRemoveChild()` - 子节点管理

**布局计算**:
- `YGNodeCalculateLayout(node, width, height, direction)`

**布局结果**:
- `YGNodeLayoutGetLeft/Top/Right/Bottom/Width/Height()`

**样式设置**:
- `YGNodeStyleSetFlexDirection/JustifyContent/AlignItems/...`
- `YGNodeStyleSetWidth/Height/...` (含 Percent/Auto 变体)
- `YGNodeStyleSetMargin/Padding/...`

### 使用示例

```lua
-- 创建布局树
local root = YGNodeNew()
YGNodeStyleSetWidth(root, 800)
YGNodeStyleSetHeight(root, 600)
YGNodeStyleSetFlexDirection(root, YGFlexDirectionRow)
YGNodeStyleSetJustifyContent(root, YGJustifySpaceEvenly)

local child1 = YGNodeNew()
YGNodeStyleSetWidth(child1, 100)
YGNodeStyleSetHeight(child1, 100)
YGNodeInsertChild(root, child1, 0)

-- 计算布局
YGNodeCalculateLayout(root, 800, 600, YGDirectionLTR)

-- 获取结果并渲染
local x = YGNodeLayoutGetLeft(child1)
local y = YGNodeLayoutGetTop(child1)
local w = YGNodeLayoutGetWidth(child1)
local h = YGNodeLayoutGetHeight(child1)

nvgBeginPath(ctx)
nvgRect(ctx, x, y, w, h)
nvgFill(ctx)

-- 清理
YGNodeFreeRecursive(root)
```

---

## 引用计数与内存管理

### 背景

Yoga 的 `YGNodeRef` 原本是裸指针，导出到 Lua 时存在野指针风险：
- Lua GC 无法感知 C++ 对象的生命周期
- 用户可能在对象释放后继续使用
- 父子节点关系导致生命周期复杂

### 解决方案

为 Yoga Node 添加引用计数支持，与 Lua GC 配合实现安全的内存管理。

### 实现原理

#### 1. C++ 引用计数

在 `yoga::Node` 类中添加引用计数：

```cpp
// Node.h
class Node {
private:
    int refCount_ = 1;  // 初始引用计数为 1

public:
    void addRef() { ++refCount_; }
    void release();  // 减少引用，计数为 0 时删除
    int refCount() const { return refCount_; }
};
```

#### 2. 父子关系引用

- **InsertChild**: 父节点持有子节点引用 (+1)
- **RemoveChild**: 父节点释放子节点引用 (-1)
- **SetChildren**: 释放旧子节点引用，增加新子节点引用

```cpp
// Node.cpp
void Node::insertChild(Node* child, size_t index) {
    child->addRef();  // Parent holds reference
    children_.insert(..., child);
}

bool Node::removeChild(Node* child) {
    children_.erase(...);
    child->release();  // Release parent's reference
    return true;
}
```

#### 3. Lua 绑定集成

**创建节点 (YGNodeNew)**:
```
YGNodeNew() 返回 refCount = 1
└─ 表示 Lua 持有的引用，无需额外 AddRef
```

**获取子节点 (YGNodeGetChild)**:
```
第一次 push 到 Lua → AddRef (+1)
后续访问 → 返回已存在的 userdata
```

**释放节点 (YGNodeFree)**:
```
1. Invalidate userdata (设置内部指针为 nil)
2. 从 ubox 表移除
3. RemoveFromParent (如果有父节点，-1)
4. Release (-1，可能触发删除)
```

**GC 回收 (__gc)**:
```
Lua 回收 userdata 时调用
└─ YGNodeRelease (-1，可能触发删除)
```

### 引用计数规则

| 操作 | 引用计数变化 |
|------|-------------|
| `YGNodeNew()` | = 1 (Lua 持有) |
| `InsertChild(parent, child)` | child +1 (parent 持有) |
| `RemoveChild(parent, child)` | child -1 |
| `YGNodeGetChild()` 首次 push | +1 (Lua 持有) |
| `YGNodeGetChild()` 非首次 | 无变化 (复用 userdata) |
| `YGNodeFree()` | -1 (Lua 释放) |
| `__gc` | -1 (Lua 释放) |

### YGNodeFreeRecursive 防护

#### 问题

当 Lua 中的子节点 userdata 已被 GC 时，调用 `YGNodeFreeRecursive(root)` 会出现问题：

```
原流程：
1. child refCount = 1 (仅 Parent 持有，Lua 已 GC)
2. YGNodeRemoveChild(root, child) → release → refCount = 0 → delete!
3. YGNodeFreeRecursive(child) → 访问已删除的 child → crash!
```

#### 解决方案

在 `YGNodeRemoveChild` 前 `addRef` 保护子节点：

```cpp
// YGNode.cpp - YGNodeFreeRecursive
child->addRef();           // 临时 +1，防止被提前 delete
YGNodeRemoveChild(root, child);  // release parent 引用
YGNodeFreeRecursive(child);      // 递归（YGNodeFree 会 release 临时引用）
```

#### 引用计数流程

**场景：Lua 已 GC 子节点**
```
child refCount = 1 (Parent)
  → addRef → 2
  → YGNodeRemoveChild → 1 (临时)
  → YGNodeFreeRecursive → YGNodeFree → release → 0 → delete ✓
```

**场景：Lua 未 GC 子节点**
```
child refCount = 2 (Lua + Parent)
  → ToluaInvalidateYGNodeRecursive release Lua 引用 → 1 (Parent)
  → addRef → 2
  → YGNodeRemoveChild → 1 (临时)
  → YGNodeFreeRecursive → YGNodeFree → release → 0 → delete ✓
```

#### Lua 绑定层配合

```cpp
// YogaLayout.pkg - tolua_UILuaAPI_YGNodeFreeRecursive00
if (node) {
    // 对子节点：invalidate + release Lua 引用
    for (size_t i = 0; i < childCount; ++i) {
        ToluaInvalidateYGNodeRecursive(tolua_S, child);
    }
    // 对 root：只 invalidate，不 release（YGNodeFree 会 release）
    ToluaInvalidateYGNode(tolua_S, node);
    // 释放整棵树
    YGNodeFreeRecursive(node);
}
```

### 使用注意事项

1. **避免双重释放**: 调用 `YGNodeFree()` 后不要再访问该节点
2. **FreeRecursive**: 会递归释放所有子节点，不需要单独释放子节点
3. **GC 自动清理**: 如果不调用 `Free`，Lua GC 会在合适时机自动释放

### C API 扩展

```c
// 增加引用计数
YG_EXPORT void YGNodeAddRef(YGNodeRef node);

// 减少引用计数（可能触发删除）
YG_EXPORT void YGNodeRelease(YGNodeRef node);

// 获取当前引用计数
YG_EXPORT int YGNodeGetRefCount(YGNodeConstRef node);
```

---

## 修改文件清单

### Yoga 库 C++17 降级

| 文件 | 修改内容 |
|------|---------|
| `3rd/yoga/cmake/project-defaults.cmake` | CMAKE_CXX_STANDARD 20 → 17 |
| `3rd/yoga/yoga/enums/YogaEnums.h` | concepts → type traits, bit_width polyfill |
| `3rd/yoga/yoga/numeric/Comparison.h` | auto 参数 → 模板 |
| `3rd/yoga/yoga/style/StyleValuePool.h` | bit_cast polyfill |
| `3rd/yoga/yoga/style/StyleSizeLength.h` | 添加 operator!= |
| `3rd/yoga/yoga/style/StyleLength.h` | 添加 operator!= |
| `3rd/yoga/yoga/node/CachedMeasurement.h` | 添加 operator!= |
| `3rd/yoga/yoga/node/LayoutResults.h` | 位域构造函数 |
| `3rd/yoga/yoga/node/Node.h` | 位域构造函数, 引用计数成员和方法 |
| `3rd/yoga/yoga/node/Node.cpp` | 指定初始化器替换, 引用计数实现 |
| `3rd/yoga/yoga/style/Style.h` | 位域构造函数 |
| `3rd/yoga/yoga/algorithm/FlexLine.cpp` | 指定初始化器替换 |
| `3rd/yoga/yoga/node/LayoutableChildren.h` | 移除 std::input_iterator |

### Yoga 引用计数扩展

| 文件 | 修改内容 |
|------|---------|
| `3rd/yoga/yoga/node/Node.h` | 添加 refCount_, addRef(), release(), refCount() |
| `3rd/yoga/yoga/node/Node.cpp` | 实现 release(), 修改 insertChild/removeChild/replaceChild/setChildren/clearChildren |
| `3rd/yoga/yoga/YGNode.h` | 添加 YGNodeAddRef, YGNodeRelease, YGNodeGetRefCount 声明 |
| `3rd/yoga/yoga/YGNode.cpp` | 实现 YGNodeAddRef, YGNodeRelease, YGNodeGetRefCount, 修改 YGNodeFree, YGNodeFreeRecursive addRef 防护 |

### CMake 配置

| 文件 | 修改内容 |
|------|---------|
| `3rd/CMakeLists.txt` | 添加 yoga 子目录 |
| `engine/Source/Urho3D/CMakeLists.txt` | include 路径 + 链接 yogacore |
| `engine/Source/Tools/UrhoXRuntime/CMakeLists.txt` | Android 显式链接 yogacore |
| `engine/CMake/Modules/UrhoCommon.cmake` | C++ 标准 11 → 17 |

### Lua 绑定

| 文件 | 修改内容 |
|------|---------|
| `engine/Source/Urho3D/LuaScript/pkgs/UI/YogaEnums.pkg` | 枚举定义 |
| `engine/Source/Urho3D/LuaScript/pkgs/UI/YogaLayout.pkg` | API 绑定, 引用计数与 GC 支持, ToluaInvalidateYGNode 返回 bool, YGNodeFreeRecursive Lua 绑定配合 |
| `engine/Source/Urho3D/LuaScript/pkgs/UILuaAPI.pkg` | 引入 Yoga pkg 文件 |

### 示例

| 文件 | 说明 |
|------|------|
| `engine/bin/Data/LuaScripts/60_YogaLayout_NanoVG.lua` | Yoga + NanoVG 综合示例 (16 个 Demo) |

---

## 已知限制

1. **C++17 polyfill**: `bit_width` 和 `bit_cast` 使用简单实现，性能可能略低于 C++20 原生版本
2. **Android NDK**: 需要 NDK 21+ (Clang 9+)
3. **-Werror**: Yoga 库启用了 `-Werror`，任何警告都会导致编译失败

---

## 故障排除

### Android 链接失败

**症状**: `undefined reference to 'YGNodeNew'` 等

**解决**: 确保 `UrhoXRuntime/CMakeLists.txt` 中有:
```cmake
if (ANDROID)
    target_link_libraries (${TARGET_NAME} yogacore)
endif ()
```

### C++17 编译错误

**症状**: `error: 'concept' does not name a type`

**解决**: 确保 `project-defaults.cmake` 中 `CMAKE_CXX_STANDARD` 设为 17

### 移动端触摸不响应

**症状**: 示例中按钮点击无反应

**解决**: 示例已添加 `TouchBegin/TouchEnd/TouchMove` 事件处理，确保使用最新版本

---

**创建日期**: 2025-12-31
**最后更新**: 2026-01-01 (修复 YGNodeFreeRecursive 子节点提前释放问题)
