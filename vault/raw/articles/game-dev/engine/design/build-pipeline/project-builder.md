---
summary: "Implementation guide for project_builder.py covering input/output and build steps"
related_paths:
  - tools/generators/**
last_updated: "2026-01-11"
---

# Project Builder 实现指南

本文档为 `project_builder.py` 的实现指南。

---

## 输入/输出

### 输入文件

| 文件 | 必须 | 说明 |
|------|------|------|
| `project.json` | ✅ | 项目信息（id, name, version, author, **entry**），version 支持 `{x}` 自增占位符 |
| `resources.json` | ✅ | 资源配置（entry, aliases, groups, preload_groups） |
| `settings.json` | ❌ | 设置配置（sources, build, engine） |
| `*.meta` | ✅ | 资源元数据（uuid, group, c_or_s），JSON 格式 |

> **entry 优先级**：`project.json` 中的 entry 优先于 `resources.json`，方便 AIGC 项目频繁修改入口。

### 输出产物

| 文件 | 说明 |
|------|------|
| `version.json` | 版本索引（包含 client/server manifest hash） |
| `project.json` | 项目信息（从源 project.json 转换） |
| `manifest-{hash}.json` | 资源清单（client/server 各一份，hash 不同） |
| `assets/{uuid}-{hash}.{ext}` | 资源文件（跨版本共用） |

### 输出目录结构

```
Build/
├── assets.7z                       # 整包下载（首次启动用，可选）
├── assets/                         # 资源文件（跨版本共用）
│   └── {uuid}-{hash}.{ext}
└── {version}/
    ├── version.json                # 版本索引
    ├── project.json                # 项目信息
    └── manifest-{hash}.json        # 资源清单（client/server 各一份）
```

> **说明**：
> - `assets/` 目录在 Build 根目录下，相同内容的资源只存一份，跨版本共用
> - `assets.7z` 整包也在 Build 根目录，供首次启动时一次性下载所有资源

---

## 核心设计

### 前后端分离

构建时根据 `c_or_s` 字段将资源分配到不同的 manifest：

| c_or_s | client manifest | server manifest |
|--------|-----------------|-----------------|
| `c`（缺省） | ✅ | ❌ |
| `s` | ❌ | ✅ |
| `cs` | ✅ | ✅ |

**优点**：
- manifest 中无需 `c_or_s` 字段
- 客户端/服务端各自只加载需要的资源
- 减少不必要的信息泄露

### 内容寻址（Content Addressable）

资源文件名包含内容 hash：

```
{uuid}-{hash}.{ext}
例：C3y7ubiP8nQLJmOepTuuvfqU-a1b2c3d4.lua
```

**优点**：
- **CDN 缓存友好**：相同内容永远相同文件名，可设置长期缓存
- **多版本共存**：不同版本的相同资源可复用
- **版本切换成本低**：只需下载变更的资源

### manifest 版本化

manifest 文件名也包含内容 hash：

```
manifest-{hash}.json
例：manifest-a1b2c3d4.json
```

通过 `version.json` 索引：

```json
{
  "format": 1,
  "version": "1.2.5",
  "build": 100,
  "client": "a1b2c3d4",
  "server": "e5f6g7h8"
}
```

manifest 路径统一为 `manifest-{hash}.json`，client/server 的 hash 不同，文件名自然不同。

**优点**：
- **同时部署多版本**：不同版本的 manifest 可并存
- **原子切换**：只需更新 version.json 即可切换版本
- **数据库简化**：只需存储 version.json 即可追溯所有版本

---

## Pipeline 架构

项目构建采用 **Pipeline + Step** 架构，每个 Step 专注于单一职责：

```
┌───────────────────────────────────────────────────────────────────────┐
│                          BuildPipeline                                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐               │
│  │ InitBuildDir │ → │ LoadConfig   │ → │LoadRemoteSrc │               │
│  └──────────────┘   └──────────────┘   └──────────────┘               │
│                                               │                         │
│                                               ▼                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐               │
│  │ScanLocalRes  │ → │ ParseAliases │ → │ AssignGroups │               │
│  └──────────────┘   └──────────────┘   └──────────────┘               │
│                                               │                         │
│                                               ▼                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐               │
│  │ ExpandRefs   │ → │AssetsCooking │ → │GenManifests  │               │
│  └──────────────┘   └──────────────┘   └──────────────┘               │
│                                               │                         │
│                                               ▼                         │
│  ┌──────────────┐   ┌──────────────┐                                   │
│  │ CopyAssets   │ → │ PrintStats   │                                   │
│  └──────────────┘   └──────────────┘                                   │
│                                                                         │
└───────────────────────────────────────────────────────────────────────┘
```

### Step 生命周期

每个 Step 实现 `BuildStep` 基类，包含：

```python
class BuildStep(ABC):
    @property
    def name(self) -> str:
        """步骤名称"""

    def validate(self, ctx: BuildContext) -> bool:
        """前置条件检查（可选）"""

    @abstractmethod
    def execute(self, ctx: BuildContext) -> bool:
        """执行步骤逻辑"""

    def cleanup(self, ctx: BuildContext):
        """清理（失败时逆序调用）"""
```

### BuildContext

`BuildContext` 是跨 Step 共享的上下文，包含：

| 属性 | 说明 |
|------|------|
| `config` | 构建配置（`BuildConfig`） |
| `options` | 命令行选项（`BuildOptions`） |
| `uuid_to_resource` | UUID → 资源信息映射 |
| `alias_to_info` | 别名 → 资源信息映射 |
| `meta_cache` | Meta 缓存（懒加载） |
| `stats` | 构建统计 |

---

## 构建流程

### 阶段 1：加载配置

1. 读取 `project.json` → 提取 id, name, version, author
2. 读取 `resources.json` → 提取 entry, aliases, groups, preload_groups
3. 读取 `settings.json`（可选） → 提取 sources, build, engine
4. **解析版本号自增占位符**（如有）

> **注意**：配置文件顶层字段直接读取，无额外嵌套层。

#### 版本号自增 `{x}` 占位符

`project.json` 中的 `version` 字段支持 `{x}` 自增占位符：

```jsonc
{
  "version": "1.0.{x}"  // 每次构建自动 +1
}
```

**解析规则**：
- `{x}` 表示自增占位符，每次构建 +1
- 从 `{output_dir}/latest.json` 读取上次构建的版本号
- 如果 `latest.json` 存在且前缀匹配，从中提取数字并 +1
- 如果 `latest.json` 不存在或前缀不匹配，从 0 开始

**示例**：

| 模板 | 上次版本 | 本次版本 |
|------|----------|----------|
| `1.0.{x}` | `1.0.5` | `1.0.6` |
| `1.0.{x}` | (无) | `1.0.0` |
| `1.{x}.0` | `1.3.0` | `1.4.0` |
| `2.0.{x}` | `1.0.5` | `2.0.0` (前缀不匹配，从 0 开始) |

### 阶段 1.5：加载远端资源

对于 `settings.json` 中配置的远端 sources（非 `project`），下载其 manifest 并导入到 meta_cache：

1. 遍历 `settings.sources` 中的每个远端来源
2. 获取 `base_url` 和 `tag`（默认 `latest`）
3. 下载 `{base_url}/{tag}.json` 或 `{base_url}/{tag}/version.json`
4. 从 version.json 获取 manifest hash
5. 下载 `{base_url}/{version}/manifest-{hash}.json`
6. 将 manifest 中的 files 导入到 meta_cache

**导入后的效果**：
- 远端资源可通过 UUID 查询
- 支持 `source://**` 通配符匹配
- 支持 `source://path` 精确路径匹配
- 统一使用 `uuid_to_resource` 管理本地和远端资源

**缓存机制**：
- meta_cache 使用 `PersistentMetaCache`，缓存文件位于 `.build/meta-cache.json`
- 远端资源的 meta 信息会被持久化，避免重复下载

### 阶段 2：扫描资源

1. 遍历 `settings.build.asset_dirs`（支持字符串或对象格式）
   - 字符串格式：`"Assets"` → `{ path: "Assets", prefix: "Assets" }`
   - 对象格式：`{ "path": "engine/bin/Data", "prefix": "Data" }`
2. 应用 `settings.build.asset_ignores` 规则（glob 模式）过滤忽略的文件/目录
3. 为每个资源文件查找对应的 `.meta` 文件（JSON 格式）
4. 从 `.meta` 提取：uuid, group, c_or_s
5. 计算文件 hash（CRC32，8 字符 hex）
6. 构建资源索引：`uuid → ResourceInfo`

**c_or_s 默认值**：如果 meta 中未指定 `c_or_s`，默认为 `c`（仅客户端）。

**asset_ignores 规则**：
- 格式：`{prefix}/{relative_path}`，如 `Data/Fonts/DejaVu`
- 支持 glob 通配符：`*`、`**`、`?`、`[seq]`
- 示例：`CoreData/Shaders`、`Data/UI/Editor*.xml`、`Res/**/*.dds`

### 阶段 3：解析别名

遍历 `aliases`，解析每个别名：

| 格式 | 说明 |
|------|------|
| `uuid://C3y7ubiP8nQL...` | UUID 资源（本地/官方/社区皆可） |
| `official://path/to/file` | 官方资源（虚拟路径） |
| `pub-john://path/to/file` | 社区资源（虚拟路径） |

> **重要变更**：
> - 所有 UUID 引用统一使用 `uuid://` 协议
> - `official://uuid`、`pub-xxx://uuid` 格式**不再支持**
> - 源协议（`official://`、`pub-xxx://`）仅用于虚拟路径引用

生成：`alias → { uuid/path, source }`

> **规则**：alias 与 uuid 是一对一关系。若同一 uuid 有多个 alias，manifest 中只保留第一个。

### 阶段 4：分配分组

为每个资源确定所属 groups（合并多个来源）：

1. **groups 模式匹配** → 加入该组
2. **meta.group** 配置 → 加入该组
3. 以上都没有 → 加入 `default` 组

> **⚠️ 重要**：groups 匹配的是 **`fs_path`（相对路径）**，相对于 `asset_dirs` 根目录

#### 条目格式（优先级判定）

| 优先级 | 判定条件 | 类型 | 示例 |
|--------|----------|------|------|
| 1 | `uuid://` 开头 | UUID 资源 | `uuid://C3y7ubiP8nQLJmOepTuuvfqU` |
| 2 | `{source}://` 开头 | 源协议 | `official://**`、`official://Textures/UI.png` |
| 3 | 含 `*` | glob 模式 | `**/*.lua` |
| 4 | 其他 | 本地路径 | `Textures/bg.png` |

> **重要变更**：
> - 裸 UUID（无协议前缀）**不再被识别**为资源引用
> - 所有 UUID 引用必须使用 `uuid://` 协议
> - `official://uuid`、`pub-xxx://uuid` 格式**不再支持**

#### 协议格式解析

| 协议 | 格式 | 说明 |
|------|------|------|
| `uuid://` | `uuid://{uuid}` | UUID 资源引用（本地/官方/社区均可） |
| `{source}://**` | `{source}://**` | 远端来源通配符（引用该来源的所有资源） |
| `{source}://path` | `{source}://{path}` | 远端来源具体路径 |

**示例**：

```jsonc
{
  "groups": {
    "official": [
      "official://**",                       // 通配符：引用所有官方资源
      "official://Textures/UI.png",          // 具体路径
      "uuid://C3y7ubiP8nQLJmOepTuuvfqU"      // UUID（无论本地/远端）
    ],
    "core": ["**/*.lua"],
    "default": ["**"]
  }
}
```

**注意**：远端资源必须先在 `settings.json` 的 `sources` 中配置，构建时会自动下载其 manifest。

### 阶段 4.5：资产烘焙（AssetsCookingStep）

资产烘焙步骤负责纹理压缩和配置内嵌：

#### 多平台纹理压缩

使用 `--platform all` 时，纹理会为所有目标平台生成压缩版本：

| 平台 | 压缩格式 | 说明 |
|------|----------|------|
| iOS | ASTC 6x6 | 移动端高质量压缩 |
| Android | ASTC 6x6 | 与 iOS 共用（相同 hash） |
| Windows | BC7 | 桌面端压缩格式 |

**处理流程**：

1. 收集所有纹理资源（`.png`, `.jpg`, `.jpeg`, `.tga`）
2. 计算源文件 hash，生成缓存键：`{uuid}_{src_hash}`
3. 调用 AssetsCooking 批量压缩（`-ExeFunc=TextureCompressBatchCached`）
4. 解析压缩结果，更新资源的 `platform_hashes` 和 `platform_sizes`

**缓存机制**：

```
.build/cooking_cache/
├── {uuid}_{src_hash}_ASTC_6X6_medium.ktx  # iOS/Android 共用
└── {uuid}_{src_hash}_BC7_medium.ktx       # Windows
```

- 按压缩配置去重（iOS/Android 使用相同 ASTC 格式，共用缓存）
- 源文件 hash 变化时自动重新压缩

#### 纹理配置 XML 内嵌

纹理的同名 XML 配置文件会被内嵌到 KTX 元数据区域：

**内嵌流程**：

1. 检测同名 XML 配置文件（如 `Textures/UI.png` → `Textures/UI.xml`）
2. 清理构建配置标签（`<platform>` / `<compress>`），保留运行时配置
3. 将清理后的 XML 嵌入 KTX 文件的元数据（key = "Config"）
4. 返回 `config_embedded=true` 通知 Python 端

**Python 端处理**：

1. 收集所有 `config_embedded=true` 的纹理
2. 从 `uuid_to_resource` 移除对应的 XML 配置资源
3. 从纹理资源的 `refs` 中移除对该 XML 的引用
4. manifest 中不再包含这些 XML 文件

**manifest 平台特化字段**：

```json
{
  "uuid": "Ho4Viejpf2BG...",
  "ext": ".png",
  "hash": "ed806f60",
  "size": 20629,
  "hash@windows": "412140a3",
  "size@windows": 43829,
  "fs_path": "Textures/UI.png"
}
```

- `hash` / `size`：默认值（iOS 压缩结果）
- `hash@{platform}` / `size@{platform}`：平台特化值
- **无 refs**：XML 配置已内嵌，不再作为独立资源引用

#### 运行时配置读取

引擎加载纹理时的配置来源优先级：

1. **KTX 元数据**：从 `imageGetMetadata(container, "Config")` 读取嵌入配置
2. **同名 XML 文件**：通过 refs 查找，兼容旧格式

### 阶段 5：生成产物

#### version.json

```json
{
  "format": 1,
  "version": "1.2.5",
  "build": 100,
  "client": "a1b2c3d4",
  "server": "e5f6g7h8",
  "generated_at": "2025-12-12T10:30:00Z"
}
```

| 字段 | 说明 |
|------|------|
| `format` | 配置格式版本，未来结构变化时递增 |
| `version` | 项目语义化版本号 |
| `build` | 构建号（单调递增） |
| `client` | 客户端 manifest hash（CRC32） |
| `server` | 服务端 manifest hash（CRC32） |
| `generated_at` | 构建时间（ISO 8601 UTC） |

> **注意**：`manifest.json` 中**不包含** `generated_at` 字段，以避免每次构建导致 CRC 变化。

#### project.json

- 从源 project.json 提取并格式化
- 包含 project_id、name、version、author 等信息

#### manifest-{hash}.json

```json
{
  "format": 1,
  "target": "client",
  "project_id": "p_a2sf",
  "sources": {
    "engine": { "version": "1.2.3", "base_url": "https://cdn.example.com/engine" },
    "project": { "base_url": "assets/" },
    "official": { "version": "1.0.0", "base_url": "https://cdn.example.com/official" }
  },
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
      "refs": ["D4z8vcjQ9oRMKnPfqUvwxhsW"]
    }
  ],
  "metadata": { ... }
}
```

**files 结构**：
- 本地资源：`uuid + hash + ext + size`（省略 source = project）
- 远端资源：`uuid + ext + source`（**无 hash**，版本由远端 manifest 决定）
- `refs`：一级 UUID 引用列表（**仅本地资源**，远端资源的 refs 由其 manifest 负责）
- `fs_path`：原始虚拟路径，用于运行时路径映射

**本地资源示例**：
```json
{
  "uuid": "C3y7ubiP8nQLJmOepTuuvfqU",
  "hash": "a1b2c3d4",
  "ext": ".lua",
  "size": 2048,
  "groups": ["core"],
  "fs_path": "Scripts/main.lua",
  "refs": ["D4z8vcjQ9oRMKnPfqUvwxhsW"]
}
```

**远端资源示例**：
```json
{
  "uuid": "D4z8vcjQ9oRMKnPfqUvwxhsW",
  "ext": ".png",
  "source": "official-res",
  "groups": ["textures"],
  "fs_path": "Textures/UI.png"
}
```

> **注意**：远端资源不包含 `refs` 字段，其引用关系由远端来源的 manifest 负责。

> **重要**：远端资源不包含 `hash` 和 `size` 字段，因为其版本由远端来源的 manifest 决定，而非本项目固定。运行时需从远端 source 的 manifest 获取具体版本信息。

**sources 结构**：
- 每个 source 支持 `version`（可选）和 `base_url`（字符串或数组）
- 有 version 时拼接：`{base_url}/{version}/{path}`
- 无 version 时直接：`{base_url}/{path}`
- `base_url` 支持数组用于 fallback/负载均衡

**注意**：manifest 中不再包含 `c_or_s` 字段，因为已经按前后端分离。

#### 资源文件

- 复制资源文件到 `assets/` 目录
- 重命名为 `{uuid}-{hash}.{ext}`
- **不复制** `.meta` 文件
- 相同内容的资源只复制一次（基于 hash）

---

## 技术规范

### UUID 格式

- 24 字符 URL-safe Base64（无填充）
- 由 `uuid_generator.py` 生成
- 详见 [resource-uuid-design.md](./resource-uuid-design.md)

### Hash 计算

| 场景 | 算法 | 格式 |
|------|------|------|
| 文件内容 hash | CRC32 | 8 字符 hex（如 `a1b2c3d4`） |
| manifest hash | CRC32 | 8 字符 hex |

> **说明**：使用 CRC32 而非 SHA256，与 `gen_agent_project_manifest.py` 保持一致，计算更快。

### 文件命名

| 文件类型 | 命名格式 | 示例 |
|----------|----------|------|
| 资源文件 | `{uuid}-{hash}.{ext}` | `C3y7ubiP8nQLJmOepTuuvfqU-a1b2c3d4.lua` |
| manifest | `manifest-{hash}.json` | `manifest-a1b2c3d4.json` |

### 远端资源处理

远端资源（`official-res://**`、`official-res://path`）的处理流程：

1. **构建时**：下载远端 manifest 并导入到 meta_cache
2. **分组时**：根据 `source://**` 或 `source://path` 匹配远端资源
3. **输出时**：远端资源只记录 uuid、ext、source、fsPath，**不输出 hash**

**设计理由**：
- 远端资源的版本由其 source 的 manifest 决定
- 项目 manifest 只记录"我需要这个资源"，不锁定具体版本
- 运行时从远端 source 获取具体版本信息

> **UUID 资源**：使用 `uuid://` 协议引用的资源，统一通过 meta_cache 查询，自动处理本地/远端资源。

---

## 命令行接口

```
python project_builder.py --project ./MyGame [options]

必需：
  --project PATH              项目目录

可选：
  --version VER               指定版本号（覆盖 project.json）
  --build NUM                 指定构建号
  --output PATH               输出目录（默认 Build/{version}）
  --platform PLATFORM         目标平台（web, android, ios, windows, all）
  --asset-cooking-path PATH   AssetsCooking 可执行文件路径
  --no-copy                   不复制资源文件，只生成 manifest
  --7z                        强制生成 assets.7z 整包
  --no-7z                     强制不生成 assets.7z（默认：文件数>=50时自动生成）
  --keep-temp                 保留临时目录（用于调试纹理压缩）
  --debug                     调试模式（详细日志）
```

### 平台特化

使用 `--platform` 参数指定目标平台时，`settings.json` 中带有 `@platform` 后缀的字段会覆盖默认值：

```jsonc
{
  "build": {
    "output_dir": "dist",
    "output_dir@android": "dist/android",
    "output_dir@ios": "dist/ios"
  }
}
```

---

## 依赖模块

### 核心模块

| 模块 | 说明 |
|------|------|
| `project_builder.py` | 主入口，解析命令行参数，调用 Pipeline |
| `build_pipeline.py` | Pipeline 框架，定义 `BuildStep` 基类和 `BuildPipeline` 执行器 |
| `build_context.py` | 构建上下文，跨 Step 共享状态（资源索引、配置、统计等） |
| `build_types.py` | 数据类型定义（`ResourceInfo`, `BuildConfig`, `AssetDir` 等） |
| `build_utils.py` | 工具函数（`load_jsonc`, `resolve_platform_config`, `match_glob_pattern` 等） |

### Pipeline Steps（构建步骤）

| Step | 说明 |
|------|------|
| `InitBuildDirStep` | 初始化构建目录 |
| `LoadConfigStep` | 加载配置文件（project.json, resources.json, settings.json），处理 `{x}` 版本号自增和 `@platform` 特化 |
| `LoadRemoteSourcesStep` | 加载远端资源 manifest（从 CDN 下载） |
| `ScanLocalResourcesStep` | 扫描本地资源目录，读取 meta 文件，应用 ignore 规则 |
| `ParseAliasesStep` | 解析别名配置（aliases） |
| `AssignGroupsStep` | 分配资源分组（groups 模式匹配） |
| `ExpandRefsStep` | 展开引用（递归收集间接依赖，入口文件强制 cs） |
| `AssetsCookingStep` | 资产烘焙（纹理压缩/mipmap 生成），更新 hash/size，内嵌 XML 配置 |
| `GenerateManifestsStep` | 生成 manifest（client/server 分离）、version.json、tags |
| `CopyAssetsStep` | 复制资源文件（优先从 cooking 临时目录）、生成 assets.7z |
| `PrintStatsStep` | 输出构建统计信息 |

### 辅助模块

| 模块 | 说明 |
|------|------|
| `uuid_generator.py` | UUID 生成 |
| `meta_generator.py` | Meta 文件生成，集成 path_replacer 进行路径替换 |
| `meta_cache.py` | Meta 缓存，支持路径/UUID 双向索引，扫描文件的 UUID 引用，**支持远端资源导入** |
| `path_replacer.py` | XML 路径替换，支持 attribute value 和 variant 格式 |
| `path_scanner.py` | 路径扫描器，从 XML/JSON 中扫描资源路径引用 |
| `uuid_decoder.py` | UUID 解码 |
| `asset_cooking.py` | 纹理压缩封装（调用 AssetsCooking 可执行文件） |

### meta_cache.py 功能

**扫描支持**：`SCANNABLE_EXTENSIONS` 定义了哪些文件会被扫描 UUID 引用：

```python
SCANNABLE_EXTENSIONS = {
    '.xml', '.json', '.jsonc',      # 配置文件
    '.lua', '.ts',                   # 脚本
    '.scene', '.prefab', '.pfb',     # 场景/预制体
    '.material', '.mat', '.effect',  # 材质/效果
    '.anim', '.animation',           # 动画
    '.ui', '.layout',                # UI
    '.config', '.cfg', '.settings',  # 配置
    '.manifest', '.state',           # 其他
}
```

**远端资源支持**：

```python
# 导入远端 manifest
cache.import_remote_manifest("official-res", manifest_data)

# 按来源获取资源
resources = cache.get_resources_by_source("official-res")

# 根据 UUID 获取 meta（统一查询本地和远端）
meta = cache.get_meta_by_uuid(uuid)

# 根据远端路径获取 UUID
uuid = cache.get_remote_uuid_by_path("official-res", "Textures/UI.png")
```

**持久化缓存**（`PersistentMetaCache`）：
- 缓存文件：`.build/meta-cache.json`
- 内容包括：本地资源 meta、远端资源 meta、UUID 索引
- 加速后续构建，避免重复下载远端 manifest

### meta_generator.py 忽略规则

`IGNORE_EXTENSIONS` 定义了不生成 meta 的文件类型（如脚本、文档、构建配置等）。

> **注意**：`.sh` 不在忽略列表中，因为可能是 shader 文件。

---

## 实现优先级

### P0：最小可用 ✅

1. 加载三个配置文件
2. 扫描资源目录，读取 meta（JSON 格式）
3. 生成 manifest.json（基础字段）
4. 复制资源文件

### P1：完整功能 ✅

1. 别名解析（source 前缀）
2. 分组分配（paths + files + meta）
3. 生成 version.json 和 game.json
4. 统计信息（metadata）
5. fs_path 可选生成（读取 settings.build.generate_fs_path）
6. **前后端分离**（client/server manifest）
7. **内容寻址**（hash 命名）

### P2：增强功能

1. 引用分析（递归收集）
2. 增量构建
3. 资源压缩/优化
4. 外部资源 hash/size 获取（从远程 manifest）

---

## CDN 部署结构

```
CDN/
├── project/{project_id}/
│   ├── assets.7z                         # 整包下载（首次启动用）
│   ├── assets/                           # 资源文件（跨版本共用）
│   │   └── {uuid}-{hash}.{ext}
│   ├── latest.json                       # 最新版本索引
│   └── {version}/
│       ├── version.json
│       ├── project.json
│       └── manifest-{hash}.json
├── official/                             # 官方公共资源
│   ├── assets.7z
│   ├── assets/
│   │   └── {uuid}-{hash}.{ext}
│   └── ...
└── community/{author_id}/                # 社区作者资源
    └── {uuid}-{hash}.{ext}
```

### 多版本部署优势

1. **版本隔离**：每个版本独立目录，互不干扰
2. **资源复用**：相同 hash 的资源可跨版本共享（CDN 层面）
3. **快速回滚**：修改 latest 指向即可
4. **A/B 测试**：同时部署多个版本
5. **缓存友好**：资源文件可设置长期缓存（内容不变 = 文件名不变）

---

## 相关文档

- [README.md](./README.md) - 整体流程
- [meta-application-design.md](./meta-application-design.md) - Meta 文件设计
- [resource-uuid-design.md](./resource-uuid-design.md) - UUID 设计
- Native_Runtime_MultiPlatform_TODO - 运行时多平台纹理支持实现

---

## 已知问题与注意事项

> 本节记录当前架构中的已知问题和潜在踩坑点，供后续开发参考。

### 1. `meta_cache.get_fs_path_by_uuid()` 是死代码

**问题**：`_uuid_to_fs_path` 映射永远为空，该方法始终返回 `None`。

**原因**：重构时将 `asset_dirs` 移入 `BuildConfig`，删除了原本在 `BuildContext` 构造时调用的 `scan_directory()`，导致 `_uuid_to_fs_path` 不再被填充。

**当前绕过方案**：`build_context.ensure_resource_registered()` 中改用 `relative_to(asset_path)` 直接计算 fs_path。见 `build_context.py:391-394` 的注释。

**后续选项**：
- 保持现状（推荐，避免与 `ScanLocalResourcesStep` 重复）
- 或在某个 Step 中调用 `scan_directory()` 填充映射

---

### 2. `CompositeStep.validate()` 只验证第一个子步骤

**问题**：`build_pipeline.py` 中的 `CompositeStep.validate()` 只调用第一个子步骤的 `validate()`，后续子步骤的前置条件不会被检查。

**当前影响**：无（当前未使用 `CompositeStep`）

**建议修复**：
```python
def validate(self, ctx: BuildContext) -> bool:
    return all(step.validate(ctx) for step in self._steps)
```

---

### 3. 统计逻辑分散在多个位置

**现状**：`ctx.stats` 的更新分散在多个 Step 和 `BuildContext` 方法中：

| 统计项 | 更新位置 |
|--------|----------|
| `resources_found` | `ScanLocalResourcesStep`, `AssignGroupsStep`, `BuildContext.ensure_resource_registered()` |
| `client_resources` / `server_resources` | 同上 + `ExpandRefsStep`（修正 c→cs） |

**注意**：有去重保护（`uuid in uuid_to_resource`），不会重复统计。但维护时需注意各处的统计职责。

---

*最后更新: 2026-01-11*

<!--
更新日志:
- 2026-01-11: 更新相关文档链接，添加 Native_Runtime_MultiPlatform_TODO.md
- 2026-01-10: 新增多平台纹理压缩（--platform all）和纹理配置 XML 内嵌说明
- 2026-01-09: 新增 AssetsCookingStep，修复 cooking 在 manifest 生成后执行的 bug；更新 Pipeline 架构图
- 2026-01-09: 新增 Pipeline 架构说明；更新依赖模块列表（Pipeline Steps）；新增已知问题与注意事项
- 2025-12-17: 初始版本
-->
