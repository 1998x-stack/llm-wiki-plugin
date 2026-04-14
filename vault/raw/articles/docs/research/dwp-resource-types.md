---
summary: "DWP resource type catalog: supported types, unsupported types, and preload strategies"
last_updated: "2026-03-04"
---

# 边玩边下（DWP）资源类型与预加载策略

本文档描述 UrhoX 边玩边下系统（Download While Playing, DWP）支持的资源类型、不支持的类型、以及预加载策略。

---

## 概述

边玩边下的核心思路：**游戏启动时只下载必要资源，其余资源在运行时按需下载**。

对于支持 DWP 的资源类型，`GetResource` 会立即返回一个**占位资源**（placeholder），后台异步下载真实资源，下载完成后自动热替换。对于不支持 DWP 的类型，文件不存在时 `GetResource` 返回 nil 并进入负缓存。

---

## DWP 支持的资源类型

> 源码：`engine/Source/Urho3D/Resource/DownloadWhilePlayingManager.cpp:9-22`

| 资源类型 | 占位资源 | 说明 |
|---------|---------|------|
| `Font` | `Lite.ttf` | 文字可渲染，下载后字体热替换 |
| `Texture2D` | `Lite16x16.png` | 16x16 像素小图，视觉上为纯色块 |
| `Texture3D` | `Lite16x16.png` | 同上 |
| `TextureCube` | `Lite16x16.png` | 天空盒等会短暂显示纯色 |
| `Texture2DArray` | `Lite16x16.png` | 同上 |
| `Image` | `Lite128x128.png` | 128x128，用于运行时图片处理 |
| ~~`Model`~~ | ~~`Lite.mdl`~~ | ~~占位模型~~ → **已移入 blocking**（BoneAttachment 绑点时序问题） |
| `Animation` | `Lite.ani` | 占位动画，角色短暂 T-pose |
| `LogicalAnimation` | `Lite.ani` | 状态机动画，同上 |
| `Sound` | `Lite.ogg` | 静音占位，下载后有声 |

**DWP 工作流程**（`ResourceCache.cpp:1811-1894`）：

```
GetResource(type, name)
  │
  ├─ 本地文件存在？ → 正常加载
  │
  ├─ IsTypeSupport(type) && ResourceContains(name)？
  │   ├─ YES → 返回占位资源 + 后台高优先级下载
  │   │         下载完成 → BackgroundLoader 热替换
  │   │
  │   └─ NO → 进入负缓存，返回 nil（⚠️ 陷阱！）
```

---

## 不支持 DWP 的资源类型

以下类型**没有占位资源**，文件不存在时 `GetResource` 直接返回 nil：

| 资源类型 | 影响 | 预加载必要性 |
|---------|------|------------|
| `JSONFile` | 配置文件读取失败 | **高** — 通常是游戏配置、关卡数据 |
| `XMLFile` | Scene/Prefab/UI 加载失败 | **高** — 场景和预制体依赖 |
| `Material` | 材质丢失，物体渲染异常 | **中** — DWP 类型的 Model 热替换时会重新加载 |
| `Technique` | 渲染管线配置丢失 | **中** — 通常随 Material 一起引用 |
| `ParticleEffect` | 粒子效果不显示 | **低** — 非关键视觉 |
| `LuaFile` | 脚本执行失败 | **最高** — 已强制预加载（`.lua`） |
| `BinaryFile` | 二进制数据读取失败 | **按需** — 取决于用途 |
| `Shader` / `ShaderVariation` | 渲染异常 | **引擎层面已处理** |

### 负缓存陷阱

**问题**：非 DWP 类型调用 `GetResource()` 时文件不存在 → 被加入 `nullResource` 负缓存 → 即使后续下载完成，再次 `GetResource()` 仍返回 nil。

**解决方案**（已实现）：
```lua
-- 方式 1: ReleaseResource 释放后重新加载（推荐）
cache:ReleaseResource("JSONFile", "uuid://xxx", true)
local json = cache:GetResource("JSONFile", "uuid://xxx")

-- 方式 2: 清除所有负缓存
cache:ClearNullResources()

-- 方式 3: 使用 GetResourceAsync 自动处理（推荐 AI 使用）
cache:GetResourceAsync("JSONFile", "uuid://xxx", function(resource)
    -- 内部自动 download → release → reload
end)
```

**兜底设计**：详见 [dwp-render-blocking-preload-design.md](../design/dwp-render-blocking-preload-design.md) — 配置资源两层兜底策略（自动预加载 + 运行时阻塞下载）。

---

## 预加载策略

> 源码：`game/src/Game/Bootstrap/Manifest/ManifestResolver.cpp` (`GetPreloadFiles` / `CollectExplicitPreloadFiles` / `CollectBlockingPreloadFiles`)

### 当前预加载规则

| 优先级 | 规则 | 条件 | 说明 |
|-------|------|------|------|
| **P0** | 入口文件 | `manifest.entry` | 入口脚本强制预加载 |
| **P0** | 引擎资源 | `source == "engine-res"` | 非 WASM 平台，引擎内置资源全量预加载 |
| **P1** | 显式预加载 | `preload == true` 或 `groups ∩ preloadGroups` | CollectExplicitPreloadFiles + 完整引用链 BFS |
| **P1** | 阻塞类型兜底 | `IsRenderBlockingExt(ext)` | CollectBlockingPreloadFiles：从项目资源出发遍历引用链，阻塞扩展名加入预加载 |

**阻塞扩展名**（`RenderBlockingTypes.json`）：
`.lua` `.json` `.xml` `.material` `.prefab` `.effect` `.fsm` `.blendspace` `.cube` `.mdl`

### WASM 特殊处理

- 引擎资源（`source == "engine*"`）已打包在 `.data` 文件中，**跳过预加载**
- 其他资源走标准预加载流程

---

## RenderBlocking 资源兜底方案

> 详细设计见 → **[dwp-render-blocking-preload-design.md](../design/dwp-render-blocking-preload-design.md)**

对齐 H5 浏览器 Critical Rendering Path 模型：

- **CollectExplicitPreloadFiles**: 显式预加载（preload 标记 / preload_groups 匹配）+ 完整引用链 BFS
- **CollectBlockingPreloadFiles**: 从项目资源出发遍历引用链，自动发现阻塞扩展名资源，启动时预加载

两个函数独立运行，通过共享去重集合协作。阻塞类型由 `RenderBlockingTypes.json` 数据驱动，AI/用户无需感知 DWP。

---

## 优化建议：减少必要预加载量

### 当前瓶颈

必要预加载项 = **引擎资源** + **显式预加载（preload_groups）** + **阻塞类型兜底（blocking_exts）**

阻塞类型（.lua, .json, .xml, .material, .prefab, .mdl 等）通常占预加载量的大部分。

### 可优化方向

#### 1. 脚本按需加载（长期）

当前所有 `.lua` 都强制预加载。如果 Lua `require` 机制支持异步加载或占位，可以：
- 只预加载入口脚本及其直接依赖
- 其他脚本在 `require` 时触发下载

**约束**：Lua `require` 是同步的，需要引擎侧改造或协程化。

#### 2. Material/Technique 纳入 DWP

Material 是连接 Model 和 Texture 的桥梁。当前 Model 有 DWP 占位但 Material 没有，导致：
- 模型占位显示时材质加载失败（如果材质文件未预加载）
- 模型热替换后可能因材质缺失而渲染异常

**建议**：为 Material 和 Technique 添加 DWP 占位（空白材质/默认 Technique），让模型的材质引用链完整。

#### 3. 利用 `preload` 字段替代硬编码

当前 `.lua` 和 `.mdl`（服务端）是硬编码预加载。建议：
- 构建工具自动为入口脚本及其依赖链设置 `preload: true`
- 运行时只看 `preload` 字段，不再硬编码扩展名
- 好处：非关键脚本（如纯 UI 装饰逻辑）可以不预加载

#### 4. 利用 GetResRefs 精确预加载

不再按扩展名/分组粗粒度预加载，而是从入口资源出发，递归收集依赖链中的非 DWP 类型资源：

```lua
-- AI 编写的精确预加载逻辑
local entry = "uuid://main-scene"
local allRefs = cache:GetResRefs(entry, true)  -- 含自身的完整依赖树

local toPreload = {}
for _, ref in ipairs(allRefs) do
    local info = cache:GetResInfo(ref)
    if info then
        -- 非 DWP 支持类型 且 本地不存在 → 需要预加载
        local nonDwpExts = {".json", ".xml", ".lua", ".material", ".technique"}
        for _, ext in ipairs(nonDwpExts) do
            if info.ext == ext and not cache:Exists(ref) then
                table.insert(toPreload, ref)
                break
            end
        end
    end
end

-- 批量下载非 DWP 资源
if #toPreload > 0 then
    GetDownloadManager():DownloadResources(toPreload, function(success, failedPaths)
        if success then
            print("All critical resources ready")
        end
    end)
end
```

---

## API 速查

### 查询

```lua
local cache = GetCache()

cache:GetResInfo(uri)              -- → {uuid, fsPath, size, source, ext} | nil
cache:GetResRefs(uri)              -- → {uri1, uri2, ...}（不含自身）
cache:GetResRefs(uri, true)        -- → {uri1, uri2, ...}（含自身）
cache:GetResVirtualPath(uri)       -- → "Textures/hero.png"
cache:GetResUuid(uri)              -- → "uuid://B_J0gVyL..."
cache:Exists(uri)                  -- → bool
```

### 下载

```lua
local dm = GetDownloadManager()

dm:DownloadResource(uri, onComplete)            -- 单个资源
dm:DownloadResources(uris, onComplete, onProgress) -- 批量
dm:CancelResourceTask(uri)                      -- 取消
dm:GetResourceTaskState(uri)                    -- 查询状态
```

### 负缓存管理

```lua
cache:ReleaseResource("JSONFile", "uuid://xxx", true)  -- 释放资源（含负缓存），下次 GetResource 重新加载
cache:ClearNullResources()                              -- 清除全部负缓存
```

### 异步加载

```lua
-- Callback 模式
cache:GetResourceAsync("JSONFile", "uuid://xxx", function(resource)
    -- 自动处理: download → release null-cache → load
end)

-- Coroutine 模式（在 coroutine.start 内）
local json = cache:GetResourceAsync("JSONFile", "uuid://xxx")
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `engine/Source/Urho3D/Resource/DownloadWhilePlayingManager.h/.cpp` | DWP 管理器，类型→占位资源映射 |
| `engine/Source/Urho3D/Resource/ResourceCache.cpp:1811-1894` | DWP 集成点，占位→热替换流程 |
| `game/src/Game/Bootstrap/Manifest/ManifestResolver.cpp:577-618` | 预加载判定逻辑 |
| `game/src/Game/Bootstrap/Steps/LoadPreloadResourcesStep.cpp` | 启动时预加载执行 |
| `game/src/Game/Bootstrap/Manifest/ManifestLuaAPI.cpp` | Lua 查询 API |

---

*最后更新: 2026-03-04（预加载规则更新为 Explicit+Blocking 双收集，.mdl 加入 blocking）*
