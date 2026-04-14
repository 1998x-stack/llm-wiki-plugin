# UrhoX 项目构建流程

本文档详细描述 UrhoX 项目从创建到发布的完整构建流程。

---

## 📋 目录

- [概述](#概述)
- [文件结构](#文件结构)
- [配置文件说明](#配置文件说明)
- [资源来源机制](#资源来源机制)
- [资源分组机制](#资源分组机制)
- [前后端分离机制](#前后端分离机制)
- [构建产物说明](#构建产物说明)
- [构建流程](#构建流程)
- [工具命令参考](#工具命令参考)

---

## 概述

### 流程总览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        项目构建流程                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [开发阶段]                    [构建阶段]              [部署阶段]        │
│                                                                         │
│  ┌──────────────┐           ┌──────────────┐        ┌──────────────┐   │
│  │ 创建项目      │           │ 项目构建      │        │ 项目上传      │   │
│  │              │ ────────▶ │              │ ─────▶ │              │   │
│  │ 配置项目      │           │ 生成构建产物  │        │ CDN 部署      │   │
│  └──────────────┘           └──────────────┘        └──────────────┘   │
│         │                          │                       │           │
│         ▼                          ▼                       ▼           │
│  ┌──────────────┐           ┌──────────────┐        ┌──────────────┐   │
│  │ 源配置文件    │           │ 构建产物      │        │ CDN 文件      │   │
│  │              │           │              │        │              │   │
│  │ project.json │           │ version.json │        │ version.json │   │
│  │ resources.json           │ game.json    │        │ game.json    │   │
│  │ settings.json            │ manifest*.json        │ manifest*.json   │
│  │ *.meta       │           │ assets/      │        │ assets/      │   │
│  └──────────────┘           └──────────────┘        └──────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 核心特性

| 特性 | 说明 |
|------|------|
| **前后端分离** | client/server 各自独立的 manifest，资源共用 |
| **内容寻址** | 资源文件名包含 hash：`{uuid}-{hash}.{ext}` |
| **manifest 版本化** | manifest 文件名包含 hash：`manifest-{hash}.json` / `manifest-server-{hash}.json` |
| **多版本共存** | 不同版本可同时部署，资源可跨版本复用 |

### 输入/输出关系

| 源文件 | 构建产物 | 说明 |
|--------|----------|------|
| `project.json` | `game.json` | 项目信息 |
| `resources.json` | `manifest-{hash}.json` | 资源清单（client/server 各一份） |
| `settings.json` | `manifest-{hash}.json` | sources 合并到清单 |
| `*.meta` (uuid, group, c_or_s) | `manifest-{hash}.json` | 提取到清单 |
| 资源文件 | `{uuid}-{hash}.{ext}` | 内容寻址命名 |
| - | `version.json` | 版本索引（指向 manifest） |

---

## 文件结构

### 开发时目录结构

```
MyGame/
├── project.json                              # 项目信息
├── resources.json                            # 资源配置
├── settings.json                             # 构建/运行时设置
├── Assets/
│   ├── Scripts/
│   │   ├── main.lua
│   │   ├── main.lua.meta                     # meta 文件（JSON 格式）
│   │   └── ...
│   ├── Levels/
│   ├── Textures/
│   └── ...
└── Build/                                    # 构建输出
    ├── assets/                               # 资源文件（跨版本共用）
    │   └── {uuid}-{hash}.{ext}
    └── 1.2.5/
        ├── version.json                      # 版本索引
        ├── project.json                      # 项目信息
        ├── manifest-{hash}.json              # 资源清单（client/server 各一份）
        └── assets.7z                         # 整包资源（首次启动下载）
```

### CDN 部署结构

```
CDN/
├── project/{project_id}/
│   ├── assets/                               # 资源文件（跨版本共用）
│   │   └── {uuid}-{hash}.{ext}
│   ├── latest/                               # 最新版本（软链接或复制）
│   │   └── version.json
│   └── {version}/
│       ├── version.json
│       ├── project.json
│       ├── manifest-{hash}.json
│       └── assets.7z                         # 可选，首次启动下载
├── official/                                 # 官方公共资源
│   └── {uuid}-{hash}.{ext}
└── community/{author_id}/                    # 社区作者资源
    └── {uuid}-{hash}.{ext}
```

---

## 配置文件说明

### 1. project.json（项目信息）

```jsonc
{
  "id": "studio_game_001",
  "name": "太空射击游戏",
  
  // 版本号：支持 {x} 自增占位符
  // - "1.0.0" - 固定版本
  // - "1.0.{x}" - 每次构建自动递增（从 latest.json 读取上次版本）
  "version": "1.0.{x}",
  
  // 入口资源（可选，优先于 resources.json 中的 entry）
  // 适合 AIGC 项目，AI 需要频繁修改入口
  "entry": "main.lua",
  
  "author": {
    "name": "游戏工作室",
    "id": "studio_001"
  },
  
  "description": {
    "short": "一款精彩的太空射击游戏",
    "long": "在浩瀚的宇宙中，驾驶你的战机..."
  }
}
```

> **entry 优先级**：`project.json` 中的 entry 优先于 `resources.json`。

### 2. resources.json（资源配置）

```jsonc
{
  // 入口资源（使用 uuid:// 协议）
  "entry": "uuid://C3y7ubiP8nQLJmOepTuuvfqU",
  
  // 预加载分组
  "preload_groups": ["core", "ui", "level_1"],
  
  // 资源别名（Alias → 引用）
  // UUID 引用统一使用 uuid:// 协议（本地/官方/社区资源皆可）
  // 虚拟路径引用使用源协议（official://path、pub-xxx://path）
  "aliases": {
    "main-script": "uuid://C3y7ubiP8nQLJmOepTuuvfqU",
    "official-font": "uuid://L1g5cjQX6vYTRuWmxBceDoZd",
    "official-logo": "official://Textures/logo.png",
    "pixel-pack": "pub-pixel_master://sprites/tileset.png"
  },
  
  // 资源分组（路径相对于 asset_dirs）
  "groups": {
    "core": ["**/*.lua"],
    "default": ["**"]
  }
}
```

> **引用规范**：
> - `uuid://xxx` - 任何 UUID 资源（本地/官方/社区）
> - `alias://xxx` - 别名引用（运行时使用，构建配置不支持）
> - `{source}://path` - 源协议（official、pub-xxx 等任意名称）
> - ⚠️ `official://uuid`、`pub-xxx://uuid` 格式**不再支持**

#### 分片配置

`resources.json` 支持拆分为多个文件，便于模块化管理：

```
MyGame/
├── resources.json           # 主配置
├── resources-aliases.json   # 别名配置（可选）
├── resources-ui.json        # UI 分组配置（可选）
└── resources-levels.json    # 关卡分组配置（可选）
```

**合并规则**：
- 文件名格式：`resources-*.json` 或 `resources-*.jsonc`
- 加载顺序：先加载 `resources.json`，再按文件名字母序加载分片文件
- 覆盖策略：**后者字段覆盖前者**（整个字段替换，不做深度合并）

**示例**：

```jsonc
// resources.json - 主配置
{
  "entry": "uuid://xxx",
  "groups": { "default": ["**"] }
}

// resources-aliases.json - 别名分片
{
  "aliases": {
    "main-script": "uuid://xxx",
    "ui-manager": "uuid://yyy"
  }
}
```

### 3. settings.json（设置配置）

```jsonc
{
  // 资源来源配置
  "sources": {
    "engine": {
      "tag": "1.x.x",
      "base_url": "https://cdn.example.com/engine/"
    },
    "official": {
      "tag": "latest",
      "base_url": "https://cdn.example.com/official/"
    },
    "project": {
      "base_url": "assets/"
    },
    "pub-pixel_master": {
      "base_url": "https://cdn.example.com/community/pixel_master/"
    }
  },
  
  // 构建配置
  "build": {
    "generate_fs_path": true,
    "output_dir": "dist",
    
    // 资源检索根目录列表
    "asset_dirs": ["assets", "scripts"],

    // 资源忽略规则（完整路径，相对于项目根目录）
    "asset_ignores": [
      "assets/Editor/**",
      "assets/Temp/**"
    ],
    
    // 版本标签配置（用于生成 {tag}.json 指向特定版本）
    "tags": {
      "latest": "auto",      // auto = 当前构建版本
      "stable": "1.0.0"      // 固定版本
    }
  }
}
```

**tags 配置说明**：

| 值 | 说明 | 示例 |
|----|------|------|
| `"auto"` | 指向当前构建版本 | `latest.json` → `1.0.5` |
| `"1.0.0"` | 固定指向指定版本 | `stable.json` → `1.0.0` |
| `"1.x.x"` | 匹配模式（主版本锁定） | 用于大版本分支 |

构建时会在 `dist/` 目录生成对应的 `{tag}.json` 文件，上传时一并上传到 CDN 根目录。

> **平台特化**：使用 `@platform` 后缀覆盖字段，如 `"output_dir@android": "dist/android"`

### 4. 资产 Meta 文件

Meta 文件为 JSON 格式，后缀 `.meta`：

```json
{
  "uuid": "C3y7ubiP8nQLJmOepTuuvfqU",
  "group": "ui",
  "c_or_s": "cs"
}
```

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `uuid` | 资源唯一标识符（24 字符 Base64，必须） | - |
| `group` | 资源分组，支持字符串或数组（可选） | - |
| `c_or_s` | 前后端标识（可选） | `c` |

---

## 资源来源机制

### 引用协议规范

| 协议格式 | 示例 | 说明 |
|----------|------|------|
| `uuid://` | `uuid://C3y7ubiP8nQLJmOepTuuvfqU` | 任何 UUID 资源（本地/官方/社区） |
| `official://path` | `official://Fonts/NotoSans.ttf` | 官方资源（虚拟路径） |
| `pub-xxx://path` | `pub-john://sprites/logo.png` | 社区资源（虚拟路径） |

> ⚠️ **注意**：`official://uuid`、`pub-xxx://uuid` 格式**不再支持**，所有 UUID 引用统一使用 `uuid://`

### 来源配置

| source 名称 | 需要配置 | 说明 |
|-------------|----------|------|
| `project` | ❌ | 项目本地资源（默认 `base_url: "assets/"`） |
| `official` | ❌ | 平台官方资源（平台内置） |
| `pub-xxx` | ✅ | 社区作者资源，需在 `settings.sources` 中配置 |

### URL 拼接规则

```
# 有 tag 时（推荐）
{base_url}/{tag}.json → 获取版本信息 → {base_url}assets/{uuid}-{hash}.{ext}

# 有 version 时（精确锁定）
{base_url}{version}/version.json → {base_url}assets/{uuid}-{hash}.{ext}

# 无 tag/version 时
{base_url}assets/{uuid}-{hash}.{ext}
```

> **注意**: `assets/` 目录在 `base_url` 根目录下（与版本号同级），因为资源使用内容寻址命名，可跨版本复用。

---

## 资源分组机制

### 分组配置

```jsonc
{
  "groups": {
    "core": ["**/*.lua", "uuid://C3y7ubiP8nQLJmOepTuuvfqU"],
    "ui": ["UI/**"],
    "default": ["**"]
  }
}
```

- **格式**: 每个 group 是路径模式数组（相对于 `asset_dirs`）
- **支持的模式**:
  - `**/*.lua` - glob 模式匹配
  - `uuid://xxx` - UUID 引用
  - `{source}://path` - 源协议引用
- **常见模式**:
  - `"**"` - 匹配所有文件
  - `"Fonts/**"` - 匹配子目录
  - `"**/*.lua"` - 匹配特定扩展名

### 多 Group 支持

资源可属于多个 group，来源合并：

1. `resources.json` 中 groups 模式匹配该资源
2. 资源 meta 文件中的 `group` 字段

### 预加载判断

```
预加载 = 资源的任一 group ∈ preload_groups
```

---

## 前后端分离机制

### c_or_s 字段

| 值 | client manifest | server manifest | 说明 |
|----|-----------------|-----------------|------|
| `c` | ✅ | ❌ | 仅客户端（**缺省值**） |
| `s` | ❌ | ✅ | 仅服务端 |
| `cs` | ✅ | ✅ | 前后端通用 |

### 构建后效果

- **manifest 分离**：client 和 server 各自有独立的 manifest（通过文件名区分）
- **无需 c_or_s 字段**：manifest 中不再包含 c_or_s，因为已按端分离
- **资源共用**：client 和 server 共用一个 assets 目录（内容寻址保证无重复）

### 典型场景

| 资源类型 | c_or_s | 说明 |
|----------|--------|------|
| UI 贴图 | `c` | 仅客户端展示 |
| 音效/音乐 | `c` | 仅客户端播放 |
| 游戏逻辑脚本 | `cs` | 前后端都需要 |
| 服务端配置 | `s` | 仅服务端使用 |
| 数据校验脚本 | `s` | 仅服务端校验 |

---

## 构建产物说明

### 1. version.json（版本索引）

```json
{
  "format": 1,
  "version": "1.2.5",
  "build": 100,
  "client": "a1b2c3d4",
  "server": "e5f6g7h8"
}
```

| 字段 | 说明 |
|------|------|
| `format` | 配置格式版本（解析方式版本） |
| `client` | 客户端 manifest hash |
| `server` | 服务端 manifest hash |

manifest 路径统一为 `manifest-{hash}.json`，client/server 的 hash 不同，文件名自然不同。

**用途**：
- 客户端/服务端通过 hash 拼接 manifest 路径
- 数据库只需存储 version.json 即可追溯所有版本
- `format` 字段用于未来配置结构变化时的兼容处理

### 2. game.json（项目信息）

从 `project.json` 转换，按目标平台输出不同格式。

### 3. manifest-{hash}.json（资源清单）

```jsonc
{
  "manifest_version": "2.0",
  "target": "client",           // client 或 server
  "project": { "id": "...", "name": "...", "version": "..." },
  "engine": { "version": "...", "base_url": "..." },
  "sources": { ... },
  "entry": "uuid://C3y7ubiP8nQLJmOepTuuvfqU",
  "preload_groups": ["core", "ui"],
  "files": [
    {
      "uuid": "C3y7ubiP8nQLJmOepTuuvfqU",
      "hash": "a1b2c3d4",
      "ext": ".lua",
      "size": 2048,
      "groups": ["core"],
      "alias": "main-script",
      "fs_path": "Scripts/main.lua",
      "refs": ["D4z8vcjQ9oRMKnPfqUvwxhsW", "E5a9wdkR0pSNLoQgrVxyzitX"]
    }
  ],
  "metadata": {
    "total_files": 16,
    "total_size": 1048576,
    "preload_files": 8,
    "preload_size": 524288,
    "groups": { ... }
  }
}
```

**说明**：
- `uuid` 可从 `path` 解析（格式 `{uuid}-{hash}.{ext}`），无需单独字段
- manifest 中不再包含 `c_or_s` 字段（已按前后端分离）
- `refs` 字段包含该资源直接引用的其他资源 UUID（一级引用，**仅本地资源**）
- `entry` 使用 `uuid://xxx` 标准格式

### 4. 资源文件命名

```
{uuid}-{hash}.{ext}
例：C3y7ubiP8nQLJmOepTuuvfqU-a1b2c3d4.lua
```

**优点**：
- **CDN 缓存友好**：相同内容永远相同文件名
- **多版本复用**：不同版本的相同资源可共享
- **版本切换成本低**：只需下载变更的资源

### 5. 多平台纹理压缩

使用 `--platform all` 构建时，纹理会为所有目标平台生成压缩版本：

| 平台 | 压缩格式 |
|------|----------|
| iOS | ASTC 6x6 |
| Android | ASTC 6x6 |
| Windows | BC7 |

**manifest 平台特化字段**：

```json
{
  "uuid": "ABC123...",
  "ext": ".png",
  "hash": "a1b2c3d4",
  "size": 12345,
  "hash@ios": "a1b2c3d4",
  "hash@android": "a1b2c3d4",
  "hash@windows": "c3d4e5f6",
  "size@ios": 12345,
  "size@android": 12345,
  "size@windows": 8765
}
```

- `hash` / `size`：默认值（iOS/Android ASTC 共用）
- `hash@{platform}` / `size@{platform}`：平台特化值

**运行时平台选择**（已实现于 `ManifestData.cpp`）：

| 平台 | GetAssetPlatform() | 使用字段 |
|------|-------------------|----------|
| iOS/tvOS/macOS | `"ios"` | `hash@ios` |
| Android | `"android"` | `hash@android` |
| Windows | `"windows"` | `hash@windows` |
| Web (BC7 支持) | `"windows"` | `hash@windows` |
| Web (ASTC 支持) | `"android"` | `hash@android` |
| Web (其他) | `""` | `hash` (默认) |

**内容寻址去重**：iOS 和 Android 使用相同压缩格式（ASTC），hash 相同时只存储一份文件。

### 6. 纹理配置 XML 内嵌

纹理的 XML 配置文件（如 `Textures/UI.xml`）会被内嵌到 KTX 文件的元数据区域：

**处理流程**：
1. 压缩纹理时，清理 XML 中的构建配置（`<platform>` / `<compress>` 标签）
2. 将清理后的 XML 内嵌到 KTX 元数据（key = "Config"）
3. 从 manifest 中移除该 XML 配置文件
4. 从纹理资源的 `refs` 中移除对该 XML 的引用

**优点**：
- **减少文件数量**：manifest 更精简，减少 HTTP 请求
- **原子加载**：纹理和配置一起加载，无需额外请求
- **运行时透明**：引擎自动从 KTX 元数据读取配置

**运行时配置来源优先级**（已实现于 `Texture.cpp`）：
1. KTX 元数据中的嵌入配置（key = "Config"）
2. 同名 XML 文件（回退，兼容旧格式）
3. 默认配置文件（`EngineRes/Textures/Default.xml`）

**支持的纹理类型**：
- `Texture2D` - 2D 纹理 ✅
- `TextureCube` - 立方体贴图（单文件 KTX/DDS）✅
- `Texture2DArray` - 纹理数组（单文件 KTX/DDS）✅
- `Texture3D` - 3D 纹理（不支持压缩，无需嵌入配置）

> 详细实现见 Native_Runtime_MultiPlatform_TODO

---

## 构建流程

```bash
python tools/project-tools/project_builder.py --project ./MyGame --version 1.2.5
```

### Pipeline 架构

构建流程采用 Pipeline/Step 架构，详见 [project-builder.md](./project-builder.md)：

```
BuildPipeline
├── InitBuildDirStep        # 初始化构建目录
├── LoadConfigStep          # 加载配置文件
├── LoadRemoteSourcesStep   # 加载远端资源
├── ScanLocalResourcesStep  # 扫描本地资源
├── ParseAliasesStep        # 解析别名映射
├── AssignGroupsStep        # 分配资源分组
├── ExpandRefsStep          # 展开资源引用
├── AssetsCookingStep       # 资产烘焙（纹理压缩等）
├── GenerateManifestsStep   # 生成构建产物
├── CopyAssetsStep          # 复制资产文件
└── PrintStatsStep          # 输出统计信息
```

### 构建产物

```
{output_dir}/
├── {version}/
│   ├── version.json              # 版本索引（含 client/server hash）
│   ├── project.json              # 项目信息
│   └── manifest-{hash}.json      # 资源清单（client/server 各一份）
└── assets/
    └── {uuid}-{hash}.{ext}       # 资源文件（跨版本共用）
```

---

## 工具命令参考

```bash
# 生成/补充 meta 文件
python tools/project-tools/meta_generator.py --project ./MyGame

# 完整构建
python tools/project-tools/project_builder.py --project ./MyGame --version 1.2.5

# 指定构建号
python tools/project-tools/project_builder.py --project ./MyGame --version 1.2.5 --build 100

# 指定平台（启用纹理压缩）
python tools/project-tools/project_builder.py --project ./MyGame --platform web

# 多平台构建（生成所有平台的压缩纹理）
python tools/project-tools/project_builder.py --project ./MyGame --platform all

# 只生成 manifest（不复制资源）
python tools/project-tools/project_builder.py --project ./MyGame --no-copy

# 跳过 assets.7z 整包生成
python tools/project-tools/project_builder.py --project ./MyGame --no-7z

# 保留临时目录（调试纹理压缩）
python tools/project-tools/project_builder.py --project ./MyGame --platform web --keep-temp

# 禁用纹理压缩（仅生成 mipmap）
python tools/project-tools/project_builder.py --project ./MyGame --platform web --no-compress

# 调试模式
python tools/project-tools/project_builder.py --project ./MyGame --debug

# 上传到 CDN（基于 manifest 精准上传）
python tools/project-tools/project_uploader.py --project . --host <cdn_host> --token <token>
```

### 上传策略（project_uploader.py）

基于 manifest 的精准上传，只上传构建产物中真正需要的文件：

| 目录层级 | 上传策略 |
|---------|---------|
| `{version}/` | 无脑上传所有文件（version.json、manifest、engine-*.json 等）|
| `assets/` | 精准上传：只上传 manifest 中引用的资源文件 |
| 根目录 `dist/` | 固定文件 + tags 配置的 `{tag}.json` |

**根目录上传的文件**：
- `latest.json` - 最新版本索引
- `project.json` - 项目信息
- `assets.7z` - 整包下载（如有）
- `{major}.x.x.json` - 主版本索引（如 `1.x.x.json`）
- `{tag}.json` - 来自 `settings.json` 中 `build.tags` 配置（如 `stable.json`）

---

## 运行时资源引用

### 引用格式

运行时使用 fs_path（虚拟路径）引用资源：

```lua
-- 使用 fs_path 引用资源
cache:GetResource("Font", "Fonts/MiSans-Regular.ttf")
cache:GetResource("Model", "Models/Box.mdl")
cache:GetResource("Material", "Materials/Stone.xml")
cache:GetResource("Texture2D", "Textures/UI.png")
```

> **说明**：运行时通过 manifest 中的 `fs_path` 字段将虚拟路径映射到实际的 `{uuid}-{hash}.{ext}` 文件。

### 关键设计决策

| 决策 | 说明 |
|------|------|
| **内容寻址** | 文件名包含 hash，相同内容 = 相同文件名 |
| **manifest 版本化** | 通过 version.json 索引 manifest |
| **前后端分离** | 各自独立的 manifest 和 assets 目录 |

详见 [resource-uuid-design.md](./resource-uuid-design.md) 中的"开发调试策略"章节。

---

## 多版本部署优势

1. **版本隔离**：每个版本独立目录，互不干扰
2. **资源复用**：相同 hash 的资源可跨版本共享
3. **快速回滚**：修改 latest 指向即可
4. **A/B 测试**：同时部署多个版本
5. **缓存友好**：资源文件可设置长期缓存

---

## 相关文件

### JSON Schema（配置校验）

| Schema 文件 | 说明 |
|-------------|------|
| `tools/project-tools/schemas/project.schema.json` | project.json 校验 |
| `tools/project-tools/schemas/resources.schema.json` | resources.json 校验 |
| `tools/project-tools/schemas/settings.schema.json` | settings.json 校验 |
| `tools/project-tools/schemas/manifest.schema.json` | manifest.json 校验 |
| `tools/project-tools/schemas/meta.schema.json` | *.meta 校验 |
| `tools/project-tools/schemas/version.schema.json` | version.json 校验 |

### 文档

| 文档 | 说明 |
|------|------|
| [meta-application-design.md](./meta-application-design.md) | Meta 应用设计 |
| [resource-uuid-design.md](./resource-uuid-design.md) | UUID 设计说明 |
| [project-builder.md](./project-builder.md) | 构建工具实现指南 |

---

*最后更新: 2026-01-11*

<!--
更新日志:
- 2026-01-11: 补充运行时实现状态（manifest 平台选择、纹理配置加载已完成）
- 2026-01-10: 新增多平台纹理压缩和纹理配置 XML 内嵌说明（构建产物章节）
- 2026-01-09: 重命名为 README.md；更新相关文件为 JSON Schema；修正运行时资源引用 API
- 2025-12-19: 新增 resources.json 分片配置支持（resources-*.json）
- 2025-12-17: 新增 tags 配置说明；更新上传策略（精准上传机制）
-->
