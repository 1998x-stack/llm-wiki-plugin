---
summary: "Download-While-Playing RenderBlocking resource preload design, auto-classifying resources like browser Critical Rendering Path"
related_paths:
  - engine/Source/Urho3D/Resource/**
last_updated: "2026-03-04"
---

# 边玩边下：RenderBlocking 资源预加载兜底设计

> 对齐目标：**H5 浏览器的 Critical Rendering Path**
>
> 浏览器不需要开发者标记"这个 CSS 要预加载"——它按资源类型自动判定。
> DWP 应做同样的事：**按类型自动兜底，开发者/AI 零感知**。

## ⭐ 核心三要点

> **1. 边玩边下作为默认兜底**
>
> DWP 是引擎默认行为，AI/开发者零感知零配置。阻塞类型（材质、配置等）由 Layer 1 自动预加载，媒体类型（纹理、模型等）由 DWP 占位+热替换兜底。排查并封堵所有边界问题（负缓存、服务端模式、blocking 类型遗漏等）。

> **2. AI 可控阶段下载**
>
> 将资源查询、下载、加载 API 统一收敛到 `cache` 一个对象上。AI 只需面对一个主体即可完成：查引用（`GetResRefs`）、查元信息（`GetResInfo`）、查状态（`GetDownloadState`）、触发下载（`DownloadResource` / `DownloadResources`）、取消下载（`CancelDownload`）。降低认知负担，让 AI 写出正确的分阶段加载代码。

> **3. 非 DWP 类型的兜底**
>
> 对没有占位符的资源类型（JSONFile、XMLFile、BinaryFile 等），提供 `GetResourceAsync` 封装「下载 → 清负缓存 → 加载」的完整流程，支持 callback 和 coroutine 两种调用风格。避免 AI 踩入「GetResource 返回 nil → 负缓存中毒 → 下载后仍 nil」的陷阱。

---

## H5 浏览器模型

```
浏览器加载页面
  │
  ├─ HTML → 增量解析 DOM
  │
  ├─ CSS (render-blocking)
  │   └─ 阻塞渲染，直到 CSSOM 构建完成
  │      不显示 FOUC（Flash of Unstyled Content）
  │
  ├─ JS (<head>, parser-blocking)
  │   └─ 阻塞 DOM 解析，除非 defer/async
  │
  ├─ Images / Video / Audio (non-blocking)
  │   └─ 占位 → 渐进加载，不阻塞渲染
  │
  └─ Fonts (semi-blocking)
      └─ FOUT/FOIT 降级策略
```

**核心设计**：

1. **Preload Scanner** — 浏览器自动从 HTML 中发现 CSS/JS 依赖，提前开始下载
2. **Render-Blocking** — 即使 preload scanner 没发现，CSS 仍然阻塞渲染
3. **两层保障** — scanner 是主动优化，blocking 是被动安全网

---

## DWP 对齐映射

| H5 概念 | DWP 对应 | 资源类型 |
|---------|---------|---------|
| **CSS / Critical JS** = render-blocking | **阻塞资源** = 场景不可缺 | Material, Technique, JSONFile, XMLFile, Prefab, Effect, FSM, BlendSpace, ColorLUT, Model |
| **Images / Video / Audio** = non-blocking + placeholder | **媒体资源** = 占位 + 热替换 | Texture2D/3D/Cube/Array, Image, Animation, Sound, Font |
| **Preload Scanner** = 自动发现依赖 | **运行时依赖链预加载** | GetResRefs 运行时递归 |
| **`<script defer>`** = 延迟加载 | **GetResourceAsync** = 异步加载 | AI 可控的延迟加载 |

---

## 构建时 vs 运行时职责划分

### 为什么不能只靠构建时

远端资源（engine-res, official-res）可以独立热更新，构建时只能拿到**当时版本**的 refs 快照。
远端资源的引用关系可能随版本更新而变化，构建时的依赖链可能已过时。

**所有资源都有 UUID 和虚拟路径，运行时统一通过 URI（`uuid://{uuid}`、虚拟路径）访问。**

### 职责划分

| 职责 | 构建时 | 运行时 |
|------|--------|--------|
| 项目本地资源扫描 | ✅ 扫描、提取 refs、分组、打包 | 加载 manifest |
| 本地资源 refs | ✅ 递归遍历完整依赖链 | — |
| 远端资源 refs | ⚠️ **只取一层**（快照，可能过时） | ✅ **用最新 manifest 实时计算** |
| 预加载集合判定 | ⚠️ 按 group 初筛（旧方案 preload_groups，兼容但不再扩展） | ✅ **路径A: preload_groups 远端深度补齐 ∪ 路径B: manifest 非 DWP 扫描** |
| DWP 类型判定 | 不涉及 | ✅ IsTypeSupport 判定媒体/配置 |
| 下载执行 | 不涉及 | ✅ 预加载 + DWP + 按需 |

**核心原则**：构建时做能做的事（本地资源 refs 递归提取、远端 refs 取一层、group 分配），运行时做必须做的事（最新 refs 计算、预加载判定）。

> ⚠️ **构建时远端 refs 只取一层**：远端资源可独立热更新，深层 refs 随时可能变化，构建时快照不可靠。只取一层确保 manifest 包含项目直接依赖的远端资源，更深的依赖由运行时用最新 manifest 递归。
>
> **存量兼容**：存量项目通过 `preload_groups` 配置了全量预加载，构建时砍掉深层远端条目后，由运行时 `CollectPreloadGroupRefs` 补回（见 Layer 1）。

### 构建管线已有基础

> 源码：`tools/project-tools/`

| 构建步骤 | 作用 | 与预加载的关系 |
|---------|------|--------------|
| `ScanLocalResourcesStep` | 扫描项目本地资源 | 本地资源入库 |
| `ParseAliasesStep` | 解析 alias 映射 | alias:// → uuid:// |
| `AssignGroupsStep` | 按配置分配 group（glob/路径/uuid） | 决定资源分组 |
| `ExpandRefsStep` | **BFS 递归展开 refs，生成 `{group}#refs` 派生分组** | 依赖链传导 |
| `GenerateManifestsStep` | 生成 manifest JSON | 输出 groups + 条件输出 refs |

**refs 提取规则**（`meta_cache._scan_file_refs()`）：

| 模式 | 提取方式 | 覆盖 |
|------|---------|------|
| `uuid://xxx` | 正则匹配所有文本文件 | ✅ 全覆盖 |
| `alias://xxx` | 正则匹配 | ✅ |
| 裸 24 字符 base64 UUID | .lua/.ts 中引号内匹配 | ✅ |
| 路径字符串 `"Models/hero.mdl"` | 需 meta 中 `path_refs: true` | ⚠️ 默认关闭 |

**已有 group 与预加载传导**：

```
preload_groups: [default, #engine-res, #config, #blocking,
                 default#refs, #engine-res#refs, #config#refs]

传导链（改造后，远端只一层）：
  main.lua (in #blocking+default, 本地)
    → refs → scene.xml (远端) → 获得 default#refs → 在 manifest 中 ✅
      → refs → hero.material (远端的远端) → 不在 manifest 中 ❌
        → 由运行时路径 A/B 补齐

旧行为：ExpandRefsStep 无限深度 BFS → hero.material 也在 manifest 中
新行为：ExpandRefsStep 远端只一层 → hero.material 由运行时发现
```

**构建时覆盖的（目标状态，步骤 5 改造后）**：
- ✅ 本地资源递归 refs — 完整依赖链（不变）
- ✅ 远端资源一层 refs — 确保直接依赖在 manifest 中（从无限深度改为一层）
- ✅ group 分配 — `#engine-res`, `#blocking`, `#config`，`default` 等
- ✅ 一层远端资源获得 `{group}#refs` 派生分组（preload_groups 仍可命中，`#blocking` 除外）

**构建时覆盖不了的（由运行时补齐）**：
- ❌ 远端资源的深层 refs — 远端热更后依赖关系可能变
- ❌ 运行时动态引用 — Lua 代码中用虚拟路径或动态拼接的 URI
- ❌ 非 DWP 类型自动预加载 — 需运行时 `CollectBlockingRefs` 扫描 manifest

---

## 阻塞资源配置：RenderBlockingTypes.json

### 为什么不硬编码在 C++

- C++ 引擎代码不可热更，新增阻塞类型需要发版
- 不同项目可能有不同的阻塞类型需求
- 数据驱动更灵活，运行时 Lua 也能查询

### 配置文件

**位置**：`engine/bin/Data/Strings/RenderBlockingTypes.json`（引擎随包资源 + 热更资源）

```json
{
    "blocking_exts": [".lua", ".json", ".xml", ".material", ".prefab", ".effect", ".fsm", ".blendspace", ".cube", ".mdl"]
}
```

> 这些扩展名没有 DWP 占位资源，运行时缺失会导致功能异常（渲染缺材质、场景加载失败等）。

### C++ 存储

阻塞扩展名集合存放在 `DownloadWhilePlayingManager`，作为资源可用性分类的唯一入口：

```cpp
// DownloadWhilePlayingManager.h
class DownloadWhilePlayingManager : public Object
{
    // ... existing DWP placeholder methods ...

    /// 从 JSON 配置加载阻塞资源扩展名
    void LoadRenderBlockingExts(const JSONFile* json);

    /// 检查扩展名是否为阻塞类型（无 DWP 占位，必须预加载）
    bool IsRenderBlockingExt(const String& ext) const;

private:
    HashSet<String> renderBlockingExts_;
};
```

**`IsExtSupported` 与 `IsRenderBlockingExt` 的关系**：

| 方法 | 含义 | 数据来源 | 用途 |
|------|------|---------|------|
| `IsExtSupported(ext)` | 该扩展名有 DWP 占位 | C++ 硬编码 | 运行时 DWP 占位判定 |
| `IsRenderBlockingExt(ext)` | 该扩展名缺失会阻塞渲染/功能 | JSON 配置 | 预加载判定 |

两者不是简单互补：有些扩展名既不是 DWP 也不是 blocking（如 `.bin`、`.dat`）。

### 加载时序

`RenderBlockingTypes.json` 是引擎资源（随包 + 热更），需要通过 `DownloadResource` 下载最新版：

```
LoadSourceManifestsStep      ← 远端 manifest 加载完毕
DownloadInitialPackageStep
LoadPreloadResourcesStep     ← ★ 改造点
  │
  ├─ 1. 下载 Strings/RenderBlockingTypes.json（通过 DownloadManager）
  ├─ 2. 解析并调用 dwpMgr->LoadRenderBlockingExts(json)
  └─ 3. 执行 GetPreloadFiles()（使用已加载的 blocking_exts）
```

不新建 Step，在 `LoadPreloadResourcesStep` 内部先下载配置再分析。

---

## Layer 1：运行时预加载

> 对应 H5：浏览器的 preload scanner 自动发现依赖

### 设计：两个独立收集函数

`IsFilePreloadNeeded` 已废弃，预加载判定拆为两个独立函数，通过共享去重集合 `added` 协作：

| 函数 | 目的 | 根节点 | 遍历行为 | 加入条件 |
|------|------|--------|---------|---------|
| **CollectExplicitPreloadFiles** | 存量兼容（逐步废弃） | `preload=true` 或 `preload_groups` 匹配 | 自身 + 完整引用链 | **全部加入** |
| **CollectBlockingPreloadFiles** | 阻塞类型自动兜底 | 所有项目资源 | 完整引用链 | **仅阻塞扩展名** |

两个函数结构完全一致：先收集根节点，再统一遍历引用链。区别仅在根节点筛选条件和加入结果的判定条件。

**阻塞扩展名来源**：
- 基础列表：`RenderBlockingTypes.json` 配置
- 动态插入：服务端模式下追加 `.mdl`（物理碰撞依赖，当前需求）
- `.mdl` 临时加入 JSON 配置（客户端动态绑点时序问题，待解决后从 JSON 移除）

### Bootstrap 流程

```
Bootstrap 启动流程
  │
  ├─ LoadProjectManifestStep  — 加载项目 manifest
  ├─ LoadSourceManifestsStep  — 加载远端 manifest（最新版）
  │
  ├─ LoadPreloadResourcesStep — ★ 预加载
  │   │
  │   ├─ LoadRenderBlockingConfig()
  │   │   └─ DownloadResource("Strings/RenderBlockingTypes.json")
  │   │   └─ dwpMgr->LoadRenderBlockingExts(json)
  │   │       └─ 解析 blocking_exts 数组
  │   │       └─ 服务端模式追加 .mdl（物理碰撞依赖）
  │   │
  │   └─ DownloadResourceFiles()
  │       ├─ GetPreloadFiles(results)
  │       │   ├─ 入口文件
  │       │   ├─ 引擎资源（WASM 跳过，其他平台全量预加载自身）
  │       │   ├─ CollectExplicitPreloadFiles — 显式预加载
  │       │   └─ CollectBlockingPreloadFiles — 阻塞预加载
  │       │
  │       └─ 检查本地是否存在 → 下载缺失的
  │
  └─ 启动游戏代码（所有阻塞资源已就绪）
```

### 效果示例

#### 存量项目（配了 preload_groups）

```
preload_groups: [default, #blocking, default#refs]

manifest（构建时远端只一层）：
  ├─ main.lua          (本地, default+#blocking) → preload_groups 匹配 ✅
  ├─ remote_prefab     (远端, default#refs)      → preload_groups 匹配 ✅
  └─ (深层远端不在 manifest 中)

CollectExplicitPreloadFiles:
  根节点: main.lua, remote_prefab
  遍历 remote_prefab 的 refs → 全部加入：
    → remote_material   ✅
      → remote_technique ✅
      → remote_texture   ✅

效果：与原来的全量预加载等价 ✅
```

#### 新项目（不配 preload_groups）

```
manifest：
  ├─ main.lua          (本地)
  ├─ remote_model      (远端)
  └─ ...

CollectExplicitPreloadFiles: 无根节点（没有 preload/preload_groups）→ 跳过

CollectBlockingPreloadFiles:
  根节点: 所有项目资源（main.lua, ...）
  遍历引用链：
    main.lua (.lua)            → IsRenderBlockingExt ✅ → 加入
    remote_model (.mdl)        → IsRenderBlockingExt ✅ → 加入（动态绑点时序需要）
    remote_material (.material)→ IsRenderBlockingExt ✅ → 加入
    remote_technique (.xml)    → IsRenderBlockingExt ✅ → 加入
    remote_texture (.png)      → 不是 blocking → 跳过（DWP 兜底）

效果：阻塞资源 + 模型全部预加载，纹理/动画/声音等媒体资源 DWP 兜底 ✅
```

### 关键优势

1. **存量完全兼容** — CollectExplicitPreloadFiles 完整引用链，等价于原来的全量预加载
2. **新项目零配置** — CollectBlockingPreloadFiles 自动兜底，AI/开发者零感知
3. **两函数独立** — 显式预加载未来废弃时直接删除 CollectExplicitPreloadFiles，不影响阻塞预加载
4. **数据驱动** — 阻塞类型从 JSON 配置加载，可热更，Lua 可查询
5. **manifest 精简** — 构建时远端只一层，深层依赖由运行时补齐

---

## Layer 2：不可行性说明 + 替代方案

### 为什么 H5 的 Render-Blocking 在游戏引擎中不可行

H5 浏览器的 CSS render-blocking 依赖**多线程架构**（网络线程独立于渲染线程）。
游戏引擎（特别是 WASM）的约束：

| 约束 | 影响 |
|------|------|
| WASM 单线程事件循环 | 主线程 spin-wait → async 回调永远不 fire → **死锁** |
| 下载系统纯异步 | 没有 sync download API，也不应该有 |
| 主线程阻塞 = 冻帧 | 即使 native 平台，体验也不可接受 |

**结论**：`GetResource` 内同步阻塞等下载在 WASM 上不可行，Layer 2 作为 universal safety net **放弃**。

### 替代方案：AI 使用 GetResourceAsync

对于 Layer 1 覆盖不到的动态引用场景（运行时拼 URI），AI 使用 `GetResourceAsync`：

```lua
-- 静态引用：Layer 1 自动预加载，GetResource 直接可用
local scene = cache:GetResource("XMLFile", "uuid://scene-uuid")  -- ✅ 已预加载

-- 动态引用：Layer 1 覆盖不到，用 GetResourceAsync
local levelId = getCurrentLevel()
cache:GetResourceAsync("JSONFile", "uuid://" .. levelConfigs[levelId], function(config)
    -- 下载 → 加载 → 回调
end)
```

**类比 H5**：
- 静态 `<link href="style.css">` → 浏览器自动 blocking 加载 → DWP Layer 1 自动预加载
- 动态 `fetch("style.css")` → 开发者自己 `await` → `GetResourceAsync`

---

## 完整 DWP 资源加载流程（含 Layer 1）

```
GetResource(type, name)
  │
  ├─ 本地文件存在？ → 正常加载
  │
  ├─ IsTypeSupport(type) && ResourceContains(name)？
  │   └─ YES → DWP 占位 + 后台热替换               ← 媒体资源
  │
  └─ 都不满足 → nil + 负缓存                        ← 配置资源（文件不在本地）
      │
      └─ 但 Layer 1 保证：manifest 中所有资源及其 refs 中的配置资源
         在 bootstrap 阶段已预加载到本地
         → 此分支对 manifest 覆盖的资源不会触发
```

**对 AI 的契约**：
- manifest 中的资源及其依赖链中的配置资源 → `GetResource` 直接可用，零感知
- 运行时动态引用（运行时拼 URI，不在 manifest 中）→ 用 `GetResourceAsync`，跟 H5 的 `fetch()` + `await` 一样

---

## 实现计划

| 步骤 | 内容 | 位置 | 状态 |
|------|------|------|------|
| **1** | 新增 `RenderBlockingTypes.json` 配置文件 | `engine/bin/Data/Strings/` | ✅ 已完成 |
| **2** | `LoadRenderBlockingExts` / `IsRenderBlockingExt` / `GetRenderBlockingExts` | `DownloadWhilePlayingManager.h/.cpp` | ✅ 已完成 |
| **3** | `LoadPreloadResourcesStep` 先下载配置再分析 | `LoadPreloadResourcesStep.h/.cpp` | ✅ 已完成 |
| **4** | 改造 `GetPreloadFiles` — 拆为 Explicit + Blocking 两函数 | `ManifestResolver.h/.cpp` | ✅ 已完成 |
| **5** | 构建管线：`ExpandRefsStep` + `#blocking` 组 + `trim_remote_refs` | `step_expand_refs.py` / `step_load_config.py` / `step_generate_manifests.py` | ✅ 已完成 |
| **6** | 真实项目验证 + Bug 修复 | 见下方 6.1-6.9 | ✅ 构建验证通过 |
| **7** | 测试验收（全量 + DWP + 回归） | 见下方步骤 7 | 🔄 进行中 |

### 前置依赖

- ✅ `ManifestResolver::GetRefs()` — 已实现
- ✅ `DownloadWhilePlayingManager::IsTypeSupport()` — 已有
- ✅ 远端 manifest 在 bootstrap 早期加载 — 已有
- ⚠️ 远端 manifest 的 refs 字段是否完整 — 需要验证

### 实施顺序

**先引擎后构建**：先部署步骤 1-4（配置 + 统一 BFS），确保运行时能补齐深层 refs，再改构建管线（步骤 5）。
这样存量项目在构建管线更新后，运行时已有兜底，不会出现预加载缺失的窗口期。

> **调用方接口不变**：`LoadPreloadResourcesStep` 只需在调用 `GetPreloadFiles()` 前加载配置，`GetPreloadFiles` 签名不变。

---

## 涉及文件

| 文件 | 改动 | 状态 |
|------|------|------|
| `engine/bin/Data/Strings/RenderBlockingTypes.json` | **新增** 阻塞资源扩展名配置 | ✅ |
| `engine/Source/Urho3D/Resource/DownloadWhilePlayingManager.h/.cpp` | 新增 `LoadRenderBlockingExts` / `IsRenderBlockingExt` / `GetRenderBlockingExts`，移除 `IsExtSupported` / `supportedExts_`，构造函数加默认阻塞列表 | ✅ |
| `game/src/Game/Bootstrap/Steps/LoadPreloadResourcesStep.h/.cpp` | 重构：`LoadRenderBlockingConfig` → `DownloadResourceFiles`，字段从 ctx_ 移入类内 | ✅ |
| `game/src/Game/Bootstrap/Manifest/ManifestResolver.h` | 新增 `CollectExplicitPreloadFiles` / `CollectBlockingPreloadFiles` 声明 | ✅ |
| `game/src/Game/Bootstrap/Manifest/ManifestResolver.cpp` | GetPreloadFiles 拆为两个独立收集函数，废弃 `IsFilePreloadNeeded` | ✅ |
| `tools/project-tools/build_steps/step_expand_refs.py` | 远端资源 BFS 限制为一层 | ✅ |

---

## blocking_exts 完整性验证（2026-03-01）

基于官方资源库 `UrhoX-Res` 全量扫描，对比 DWP 占位类型 + blocking_exts 覆盖情况：

| 扩展名 | 数量 | DWP 占位? | blocking? | 运行时加载? | 结论 |
|--------|------|-----------|-----------|------------|------|
| `.png` | 12269 | Yes (Texture2D/Image) | — | Yes | OK |
| `.tga` | 5012 | Yes (Texture2D/Image) | — | Yes | OK |
| `.effect` | 4998 | — | Yes | Yes | OK |
| `.mdl` | 4240 | ~~Yes (Model)~~ | **→ Yes** | Yes | **补入**（绑点时序问题） |
| `.xml` | 4124 | — | Yes | Yes | OK |
| `.ani` | 1802 | Yes (Animation) | — | Yes | OK |
| `.lodgroup` | 396 | — | — | **No**（编辑器/工具链专用，`LODGroup` 只在 `Tools/MeshSimplifier` 中定义） | N/A |
| `.prefab` | 374 | — | Yes | Yes | OK |
| `.material` | 284 | — | Yes | Yes | OK |
| `.json` | 26 | — | Yes | Yes | OK |
| `.jpg` | 13 | Yes (Texture2D/Image) | — | Yes | OK |
| `.lua` | 3 | — | Yes | Yes | OK |
| **`.cube`** | **3** | **No** | **→ Yes** | **Yes**（`ColorLUT`） | **补入** |
| `.fbx` | 5 | — | — | No（源文件，无运行时加载器） | N/A |
| `.jpeg` | 3 | Yes (Texture2D/Image) | — | Yes | OK |
| `.fsm` | 2 | — | Yes | Yes | OK |
| `.txt` | 2 | — | — | No（工具/元数据文件） | N/A |
| `.simpleeffect` | 1 | — | — | No（废弃格式，引擎无 `CESimpleParticleEffect` 引用） | N/A |
| `.blendspace` | 1 | — | Yes | Yes | OK |

### .cube 分析

`.cube` 是 3D LUT 色彩分级文件（非天空盒 CubeMap），由引擎 `ColorLUT` 类解析（`ColorLUT.cpp`）。

**关键发现**：`ColorGrading` 是 Scene Component，LUT 属性通过 `ResourceRef` 序列化：

```cpp
URHO3D_ACCESSOR_ATTRIBUTE("LUT", GetLUTAttr, SetLUTAttr, ResourceRef, ResourceRef(ColorLUT::GetTypeStatic()), AM_DEFAULT);
```

这意味着 `.cube` 文件**会被场景/Prefab XML 间接引用**，走 refs 依赖链 → 预加载的标准路径。缺失时 `GetResource<ColorLUT>()` 返回 nil，后处理色彩分级失效。

**处理方案**：加入 `blocking_exts`，由 Layer 1 自动预加载。不做 DWP 占位（文件极少，且 identity LUT 的视觉效果等于没有色彩分级，不如直接预加载）。

### 结论

官方资源库全量覆盖。`.cube` 和 `.mdl` 已补入 `RenderBlockingTypes.json`。
`.mdl` 补入原因：DWP 占位模型与骨骼绑点（BoneAttachment）动态绑定存在时序问题，热替换后绑点丢失。

---

## 步骤 6：真实项目验证（2026-03-01）

### 测试项目

| 字段 | 值 |
|------|-----|
| 项目 ID | p_yxna |
| 类型 | 3D 动作联网游戏 |
| Game URL | `https://f802b309-b881-4d43-afb4-c82189e7b585.ipv.taptap-code.org/` |
| 本地文件 | 17 |
| 远端来源 | engine-res (1195), official-res (19895), engine (248) |
| 还原目录 | `tmp/restored_projects/p_yxna@1.0.0/` |

### 6.1 ExpandRefsStep Bug 修复

**发现的 bug**：`step_expand_refs.py` 第 59 行的远端跳过逻辑无效。

BFS 中新发现的远端资源尚未注册到 `uuid_to_resource`（`ensure_resource_registered` 在 BFS 结束后才调用），导致 `ctx.uuid_to_resource.get(uuid)` 返回 `None`，跳过条件 `resource is not None and resource.source != "project"` 永远不触发。代码 fallthrough 到 `meta_cache.get_meta_by_uuid(uuid)` 拿到远端资源的 refs 并继续深层展开。

**修复**：当 `resource` 为 None 时，额外从 `meta_cache` 检查 source 字段：

```python
if resource is None:
    meta_check = ctx.meta_cache.get_meta_by_uuid(uuid)
    if meta_check and meta_check.get('source', 'project') != 'project':
        remote_skipped += 1
        continue
```

### 6.2 构建对比

| 维度 | 文件数 | 说明 |
|------|--------|------|
| CDN（线上） | 1316 | 旧版构建工具产物 |
| 旧版本地构建 | 1326 | 比 CDN 多 10（官方资源库版本更新，新增动画） |
| **新版本地构建** | **1274** | 比旧版少 52（深层依赖被裁剪） |

**裁剪的 52 个文件**：全部是 `official-res` 的深层依赖（材质纹理 `.tga`、材质配置 `.xml` 等），由 prefab → material → texture 链引入。新版 ExpandRefsStep 正确地只保留了第一层远端引用。

**新版多出的 10 个文件**：都是 `.ani` 动画文件，属于 blendspace 直接引用的第一层远端资源，因官方资源库版本更新而新增，符合预期。

### 6.3 FillFrom refs 合并问题（向后兼容）

**发现**：`ManifestFileInfo::FillFrom()` 不合并 `refs` 字段。

项目 manifest 中远端资源一直没有 refs（新旧构建工具都是如此）。运行时先加载项目 manifest（无 refs），再加载源 manifest 时调 `FillFrom`，但 refs 未被合并 → BFS 在第一层远端资源断链。

**影响分析**：

| 组合 | 结果 | 原因 |
|------|------|------|
| 旧构建 + 旧二进制 | ✅ | 深层依赖是 manifest 直接条目，不需要 BFS 追踪 refs |
| 旧构建 + 新二进制 | ✅ | 同上 |
| **新构建 + 旧二进制** | **❌** | manifest 裁掉深层依赖，BFS 需追踪 refs 但断链 |
| 新构建 + 新二进制 | ✅ | FillFrom 合并 refs，BFS 畅通 |

**必须支持新构建 + 旧二进制**（构建工具先于引擎部署），因此修复分两道：

1. **构建工具（必须）**：`step_generate_manifests.py` 远端资源也写入 refs 到 manifest。旧二进制直接从 JSON 读到 refs → BFS 畅通。
2. **引擎（纵深防御）**：`ManifestData.cpp` `FillFrom` 无条件用源 manifest 的 refs 覆盖（`if (!other.refs.Empty()) refs = other.refs;`），因为源 manifest 是运行时最新版本，构建时快照可能已过时。

### 6.4 运行时验证结果（2026-03-02）

测试项目部署到 `p_w5ja`（CDN: `https://tapcode-sce.spark.xd.com/src/p_w5ja/`）。

运行时日志（搜 `DWP-VERIFY`）：

```
[DWP-VERIFY] CollectExplicitPreload: roots=79, traversed=133
[DWP-VERIFY] CollectBlockingPreload: roots=17, traversed=133
ManifestResolver: 预加载 1326 个文件 (manifest 总计 19912)
[DWP-VERIFY] GetPreloadFiles: total=1326, explicit=130, blocking=0
```

| 验证项 | 结果 | 说明 |
|--------|------|------|
| CollectExplicitPreloadFiles BFS 补齐 | ✅ | traversed(133) > roots(79)，54 个深层依赖通过 refs 链发现 |
| CollectBlockingPreloadFiles BFS 链路 | ✅ | traversed(133) > roots(17)，链路畅通 |
| 预加载总量等价 | ✅ | 1326 = 旧版数量（新 manifest 1274 + 运行时补回 52） |
| blocking=0（存量项目预期） | ✅ | 项目配了 preload_groups，explicit 已全覆盖 |

### 6.5 engine-res 孤儿条目错误（已修复）

**问题**: 运行时大量 ERROR 日志 `File uuid=xxx has no source, skipping`，涉及 engine-res 的 UI 组件（Card.lua, Slider.lua, ProgressBar.lua 等）。

**根因分析**:
1. 项目 manifest 中记录了 `source="engine-res"` 的条目，但只有 uuid+source，没有 hash
2. 运行时加载最新 engine-res 源 manifest，对匹配的 UUID 调用 `FillFrom` 填充 hash/size 等
3. 如果某些 UUID 在最新 engine-res manifest 中已不存在（版本迭代移除/重命名），`FillFrom` 不会被调用 → hash 为空
4. `GetPreloadFiles()` 遍历所有 `source=="engine-res"` 条目加入预加载，未检查 hash 有效性
5. hash 为空 → `GetFileName()` 返回空 → `localPath` 为空 → `IsValid()` 返回 false → ERROR 日志

**修复**: `GetPreloadFiles()` 添加 `!file->hash.Empty()` 检查，跳过无法下载的孤儿条目。同时改进 `LoadPreloadResourcesStep` 中的日志描述（`has no valid localPath`）。

**这是预存问题，非本次改动引入。**

### 6.6 BuildFileIndex localPath 未计算（已修复）

**问题**: engine-res 条目在 `FillFrom` 后，后续的 `CalculateLocalPath` / `CalculateDownloadUrl` 仍在操作源 manifest 的条目，而非游戏 manifest 中已存在的条目。

**根因**: `BuildFileIndex` 中 `FillFrom` 将 hash 等字段填到 `exists`（游戏条目），但 `CalculateLocalPath(*target)` 等调用仍用 `file`（源条目）。

**修复**: 引入 `target` 指针模式 — `FillFrom` 后将 `target = exists`，后续所有操作（别名索引、fsPath 索引、路径计算）统一走 `target`：

```cpp
ManifestFileInfo* target = &file;
// ...
if (exists && !isGameManifest) {
    exists->FillFrom(file);
    target = exists;  // 后续操作走已存在的条目
}
// ... 所有后续操作用 *target
```

### 6.7 向后兼容：trim_remote_refs 分阶段策略

**问题**: 6.2 中新构建裁剪了 52 个深层远端依赖，新二进制通过 BFS 补回没问题，但**旧二进制不会补回** → 新构建 + 旧二进制 = 缺失 52 个文件（含 26 个 blocking 类型）。

构建工具先于引擎部署，**必须确保新构建 + 旧二进制不回退**。

**方案**: 分两阶段，通过 `trim_remote_refs` 配置开关控制：

| 阶段 | `trim_remote_refs` | 行为 | 适用期 |
|------|---------------------|------|--------|
| **Phase 1**（当前） | `false`（默认） | BFS 全量展开远端 refs，manifest 包含所有深层依赖 | 旧二进制仍在线 |
| **Phase 2**（未来） | `true` | BFS 在远端资源处停止，只保留一层 refs | 旧二进制全面淘汰后 |

配置方式（`settings.json`）：
```json
{ "build": { "trim_remote_refs": true } }
```

### 6.8 #blocking 组重构（替代 #scripts）

**背景**: 第一期 DWP 工程（commit `13942e82c`）引入了 `#scripts` + `#scripts#refs` 组，将所有脚本及其引用的资源纳入预加载，作为旧二进制兜底。但这导致**所有脚本引用的 DWP 类型资源也被预加载**，DWP 实际无法生效。

**方案**: 用 `#blocking` 组替代 `#scripts` / `#scripts#refs`：

| 维度 | 旧方案 (#scripts) | 新方案 (#blocking) |
|------|-------------------|---------------------|
| 范围 | 脚本 + 脚本引用的一切 | 仅阻塞扩展名的资源 |
| refs 展开 | `#scripts#refs` 展开所有引用 | **不展开** refs（blocking 的 refs 通常是 DWP 类型） |
| 新二进制 | explicit 覆盖了一切，无实际影响 | `CollectExplicitPreloadFiles` **跳过 #blocking**，让 `CollectBlockingPreloadFiles` 运行时兜底 |
| 旧二进制 | 全覆盖但 DWP 不生效 | 按 group 匹配预加载 blocking 类型，DWP 类型不预加载 |

**阻塞扩展名**（来自 `RenderBlockingTypes.json`）：
`.lua` `.json` `.xml` `.material` `.prefab` `.effect` `.fsm` `.blendspace` `.cube` `.mdl`

**构建工具改动**:
- `step_load_config.py`: 移除 `#scripts` 注入，改为 `#blocking` 加入 `preload_groups`
- `step_expand_refs.py`: 新增 `_assign_blocking_group()` 按扩展名分配 `#blocking` 组
- `step_generate_manifests.py`: `#blocking` 不扩展为 `#blocking#refs`

**引擎改动**:
- `CollectExplicitPreloadFiles`: 遍历 groups 时 `if (group == "#blocking") continue;`

### 6.9 构建验证（2026-03-02）

三组构建对比（测试项目 `p_yxna`，`groups: {"default": ["**"]}`）：

| 构建版本 | 文件数 | preload_groups | 说明 |
|----------|--------|----------------|------|
| **旧版 baseline** | 1326 | default, #engine-res, #config, +#refs | 无 #blocking |
| **新版 + default** | 1330 | default, #config, #engine-res, #blocking, +#refs | 多 4 个远端资源（engine-res 版本更新） |
| **新版 - default（DWP 模式）** | 1330 | #config, #engine-res, #blocking, +#refs | 同上，仅 preload_groups 不同 |

#### 新版 + default vs CDN 对比

| 维度 | 结果 |
|------|------|
| 文件差异 | 新版多 10 个 `.ani`（official-res 深层 refs，版本更新） |
| groups 差异 | 858 个文件新增 `#blocking`，16 个项目本地文件新增 `default` + `#blocking` |
| refs 差异 | 108 个文件补齐了 refs（+72 engine-res .xml，+62 official-res） |
| 旧二进制预加载 | CDN=1316, 新版=1330，新版多 14 个（严格超集） |
| 新二进制预加载 | 全量（default 覆盖所有文件，#blocking skip 无实际影响） |

**结论**: 新版 + default 是 CDN 的严格超集，全量预加载模式下无回归。

#### 新版 - default（DWP 模式）预加载模拟

| 二进制 | 预加载数 | 说明 |
|--------|----------|------|
| 旧二进制 | 1249 | 匹配 #blocking + #config + #engine-res + 各自 #refs |
| 新二进制 | ~468 | 跳过 #blocking，仅 #config + #engine-res + #refs |

新二进制预加载少 → 更多资源走 DWP 热替换（纹理、动画、声音等媒体类型）。

---

## 步骤 7：测试验收矩阵

### 测试环境

| 字段 | 值 |
|------|-----|
| 测试项目 ID | `p_w5ja`（从 `p_yxna` 还原） |
| CDN 地址 | `https://tapcode-sce.spark.xd.com/src/p_w5ja/` |
| Game URL | `https://f802b309-b881-4d43-afb4-c82189e7b585.ipv.taptap-code.org/` |
| 构建版本 | build 15（含 #blocking 组，trim_remote_refs=false） |

### 全量预加载（preload_groups 含 default）

| # | 场景 | 验收标准 | 结果 |
|---|------|----------|------|
| **N1** | 新构建 + 新二进制 | ① 无 ERROR 日志 ② DWP-VERIFY: `blocking=0`（default 全覆盖） ③ 游戏正常运行渲染 | ✅ total=1330, explicit=130, blocking=0 |
| **N2** | 新构建 + 旧二进制 | ① 无 ERROR 日志 ② 游戏正常运行渲染（旧二进制无 DWP-VERIFY 日志） | ✅ 无 ERROR，游戏正常 |

**N1 详细验收**:
1. 运行时日志搜 `DWP-VERIFY`，期望输出：
   ```
   [DWP-VERIFY] GetPreloadFiles: total=~1330, explicit=~130, blocking=0
   ```
2. `blocking=0` 说明 `default` 在 preload_groups 中 → explicit 已全覆盖 → `#blocking` skip 无实际影响
3. 无 `has no valid localPath` 相关 ERROR

### DWP 模式（preload_groups 不含 default）

> ⚠️ N3-N5 需要重新构建：修改项目 `settings.json` 清空 `preload_groups`（或移除 `default`），重新构建部署。

| # | 场景 | 验收标准 | 结果 |
|---|------|----------|------|
| **N3** | 新构建 + 新二进制 + DWP | ① DWP-VERIFY: `blocking > 0` ② explicit 明显少于 N1 的 total ③ 游戏能启动运行 ④ 纹理先显示占位符再热替换 | ✅ 资源下载正常，.mdl 加入 blocking 后绑点时序问题解决 |
| **N4** | 新构建 + 旧二进制 + DWP | ① 无崩溃 ② 旧二进制通过 #blocking group 匹配预加载 blocking 类型 ③ 游戏基本可运行 | ✅ |
| **N5** | DWP 热替换视觉验证 | 在 N3 场景下：① 角色/场景纹理从低质量占位 → 高清替换 ② 替换过程无崩溃/闪烁 | ✅ |

**N3 详细验收**:
1. 修改 `settings.json`：`"preload_groups": []`（构建工具会自动加 `#blocking` + `#engine-res` + `#config`）
2. 重新构建部署
3. 运行时日志搜 `DWP-VERIFY`，期望输出：
   ```
   [DWP-VERIFY] GetPreloadFiles: total=<远小于N1>, explicit=<少>, blocking=<大于0>
   ```
4. `blocking > 0` 说明 `CollectBlockingPreloadFiles` 扫描到了非 explicit 的阻塞类型资源

### 回归验证

| # | 场景 | 验收标准 | 结果 |
|---|------|----------|------|
| **R1** | 旧构建 + 新二进制 | ① 游戏正常运行 ② 无新增 ERROR ③ 预加载行为与旧版一致 | ✅ 旧构建无 #blocking，新二进制正常全量预加载 |
| **R2** | 旧构建 + 旧二进制 | ① 游戏正常运行（基线对照） | ✅ 基线对照，行为不变 |

### 收尾事项

- [ ] 移除 `[DWP-VERIFY]` 临时日志（`ManifestResolver.cpp` 中搜 `DWP-VERIFY`）
- [x] 更新此文档中的验收结果列（N1-N5 ✅，R1-R2 ✅）
- [ ] 评估 `step_generate_manifests.py` 中远端资源写 refs 的必要性（trim_remote_refs=false 时冗余）
- [ ] 动态绑点时序问题解决后，从 `RenderBlockingTypes.json` 移除 `.mdl`（服务端 `IsServerMode()` 追加不受影响，物理碰撞当前需求）
- [ ] **负缓存跨 URI 形式失效问题**：`GetResource("T2D", "Textures/hero.png")` 进负缓存（key=`StringHash("Textures/hero.png")`），随后 `DownloadResource("uuid://AAA")` 下载完成后清负缓存，但 `uuid://AAA` 和 `Textures/hero.png` 的 StringHash 不同，清不到。`GetResourceAsync` 已兜底（内部 `ReleaseResource` + 重加载），但 `DownloadResource` + 手动 `GetResource` 的组合路径未兜底。需要设计跨 URI 形式的负缓存清除方案（引擎层 router 解析 or Lua 层双向映射 or 其他方案）

---

## 涉及文件（更新）

| 文件 | 改动 | 状态 |
|------|------|------|
| `engine/bin/Data/Strings/RenderBlockingTypes.json` | 新增阻塞资源扩展名配置（含 `.cube`、`.mdl`） | ✅ |
| `engine/Source/Urho3D/Resource/DownloadWhilePlayingManager.h/.cpp` | LoadRenderBlockingExts / IsRenderBlockingExt / GetRenderBlockingExts，构造函数默认阻塞列表含 `.cube` | ✅ |
| `game/src/Game/Bootstrap/Steps/LoadPreloadResourcesStep.h/.cpp` | 重构：先下载配置再分析；改进日志描述 | ✅ |
| `game/src/Game/Bootstrap/Manifest/ManifestResolver.h` | CollectExplicitPreloadFiles / CollectBlockingPreloadFiles 声明 | ✅ |
| `game/src/Game/Bootstrap/Manifest/ManifestResolver.cpp` | GetPreloadFiles 拆为两个收集函数 + engine-res hash 检查 + BuildFileIndex target 指针 + CollectExplicit 跳过 #blocking + `[DWP-VERIFY]` 临时日志 | ✅ |
| `game/src/Game/Bootstrap/Manifest/ManifestData.cpp` | FillFrom 合并 refs（纵深防御） | ✅ |
| `tools/project-tools/build_types.py` | 新增 `trim_remote_refs` 字段（默认 false） | ✅ |
| `tools/project-tools/build_steps/step_load_config.py` | 移除 #scripts 注入，新增 #blocking 到 preload_groups，读取 trim_remote_refs 配置 | ✅ |
| `tools/project-tools/build_steps/step_expand_refs.py` | trim_remote_refs 条件 BFS + `_assign_blocking_group()` 按扩展名分配 #blocking 组 | ✅ |
| `tools/project-tools/build_steps/step_generate_manifests.py` | 远端资源写入 refs + #blocking 不扩展 #refs | ✅ |
| `engine/Source/Urho3D/Graphics/StaticModel.cpp` | DWP 材质延迟重应用（`materialsAttr_` 保存 + `HandleModelReloadFinished` 重应用） | ✅ |
| `engine/Source/Urho3D/Graphics/AnimatedModel.cpp` | DWP 动画 reload 恢复播放状态 | ✅ |

---

## 相关文档

- [dwp-resource-types.md](../research/dwp-resource-types.md) — DWP 资源类型与预加载策略参考
- DWP_Model_Animation_Fix_Changelog — DWP 模型材质丢失 & 动画 T-pose 修复详细 changelog
- DWP_BoneAttachment_Issue — DWP 骨骼绑定时序问题（.mdl 暂入 blocking 的原因）
- [CLAUDE.md](../../CLAUDE.md) — 项目上下文

---

*最后更新: 2026-03-04（.mdl 加入 blocking + N1-N5/R1-R2 全部通过 + 改名 RenderBlocking + 归档完善）*
