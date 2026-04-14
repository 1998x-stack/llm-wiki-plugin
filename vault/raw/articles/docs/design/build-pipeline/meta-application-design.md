---
summary: "Meta file classification, processing strategies, and application in the build pipeline"
related_paths:
  - tools/generators/**
last_updated: "2025-12-12"
---

# Meta 文件应用设计

本文档描述 UrhoX 项目中 Meta 文件的分类、处理策略以及在构建流程中的应用。

---

## 📋 目录

- [概述](#概述)
- [核心设计原则](#核心设计原则)
- [文件分类与职责](#文件分类与职责)
- [目录结构示例](#目录结构示例)
- [构建流程中的处理](#构建流程中的处理)
- [边玩边下优化](#边玩边下优化)
- [长期演进方案](#长期演进方案)

---

## 概述

### 背景

UrhoX 引入 UUID 系统后，每个资源都需要承载 UUID 等元信息。为保持清晰和一致性，采用 **Meta 文件完全独立** 的设计。

### 核心设计决策

| 决策 | 说明 |
|------|------|
| **Meta 文件独立** | `.meta` 只存放元数据，不混入引擎配置文件 |
| **引擎配置保持原样** | Urho 的 `.xml` 配置文件不添加 uuid/group 等字段 |
| **构建时统一剔除** | 所有 `.meta` 文件在构建时提取信息后丢弃 |

---

## 核心设计原则

### 分离原则

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        文件职责分离                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────┐                                                │
│  │ .meta 文件           │ ← 纯元数据                                     │
│  │ (player.png.meta)   │   uuid, group, c_or_s                         │
│  └─────────────────────┘                                                │
│           ↕ 完全独立，互不干扰                                           │
│  ┌─────────────────────┐                                                │
│  │ .xml 配置文件        │ ← 纯运行时配置                                 │
│  │ (player.xml)        │   srgb, filter, address, mipmap               │
│  └─────────────────────┘                                                │
│           ↕ 完全独立，互不干扰                                           │
│  ┌─────────────────────┐                                                │
│  │ 引擎格式文件         │ ← 纯数据                                       │
│  │ (enemy.prefab)      │   节点、组件、属性等                            │
│  └─────────────────────┘                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 设计优势

| 优势 | 说明 |
|------|------|
| **职责单一** | 每种文件只做一件事，易于理解和维护 |
| **构建简单** | 统一规则：剔除所有 `.meta`，保留其他 |
| **引擎无侵入** | 不需要修改 Urho 现有的配置解析逻辑 |
| **Git 友好** | `.meta` 文件小且稳定，变更易追踪 |

---

## 文件分类与职责

### 三类文件，三种职责

| 文件类型 | 命名规范 | 职责 | 构建后处理 |
|---------|---------|------|-----------|
| **Meta 文件** | `资源名.meta` | 元数据（uuid、group、c_or_s） | ❌ 剔除，信息合并到 manifest |
| **配置文件** | `资源名.xml` | 运行时配置（srgb、filter） | ✅ 保留（短期）/ 内嵌（长期） |
| **资源文件** | `资源名.ext` | 实际数据 | ✅ 重命名为 `uuid.ext` |

### Meta 文件（`.meta`）

**职责**：只存放元数据，构建后完全丢弃

**命名规范**：`资源文件名.meta`（如 `player.png.meta`）

> **文件夹 Meta**：当前不需要。UrhoX 使用 UUID 引用资源，完全独立于路径，文件夹移动/重命名不影响引用。如需批量配置（如整个文件夹设为同一 group），可在 `settings.jsonc` 中使用路径规则。

| 字段 | 说明 | 构建后去向 |
|------|------|-----------|
| `uuid` | 资源唯一标识符 | → manifest.files[].uuid |
| `group` | 资源分组 | → manifest.files[].groups |
| `c_or_s` | 前后端标识 | → manifest.files[].c_or_s |

**格式**（JSON）：

```json
{
  "uuid": "Wjyfex0KT2watjVfL4xKfg0c",
  "group": ["ui", "level_1"],
  "c_or_s": "c"
}
```

### 配置文件（`.xml`）

**职责**：Urho 引擎运行时配置，**不包含任何 meta 字段**

```xml
<!-- player.xml - 纯运行时配置，无 uuid/group 等字段 -->
<texture>
    <srgb>true</srgb>
    <filter>trilinear</filter>
    <address>wrap</address>
</texture>
```

#### 同名配置文件关联问题

Urho 通过同名机制关联资源和配置：`AAA.png` + `AAA.xml`

构建后两者 UUID 不同，关联丢失：
```
AAA.png  →  uuid1-{hash1}.png
AAA.xml  →  uuid2-{hash2}.xml   ❌ 无法通过同名查找
```

**短期解决方案**（✅ 已实现）：在 meta 中直接记录配置文件的 UUID

1. `meta_generator.py` 在为主资源（如 `.png`）生成 meta 时，检测是否存在同名配置文件（`.xml` 或 `.json`）
2. 如果存在，先确保配置文件有 meta（没有则生成），然后在主资源 meta 中记录 `config: "配置文件UUID"`
3. `project_builder.py` 构建时，将 `config` 字段写入 manifest
4. 运行时可直接通过 UUID 加载配置文件，无需依赖路径替换

> **注意**：同时支持 `.xml` 和 `.json` 配置文件，检测优先级为 `.xml` > `.json`

```json
// AAA.png.meta
{
  "uuid": "uuid1",
  "config": "uuid2"  // AAA.xml 或 AAA.json 的 UUID
}

// manifest 中
{
  "uuid": "uuid1",
  "hash": "...",
  "ext": ".png",
  "config": "uuid2"  // 运行时直接加载
}
```

**长期方案**：KTX2 等格式内嵌配置（见[长期演进方案](#长期演进方案)）

### 引擎格式文件

**职责**：存放实际数据，**不包含任何 meta 字段**

```xml
<!-- enemy.prefab - 纯数据，无 uuid/group 等字段 -->
<node>
    <component type="StaticModel">
        <attribute name="Model" value="Models/Enemy.mdl"/>
    </component>
</node>
```

### XML 路径引用替换

`path_replacer.py` 支持扫描和替换 XML 文件中的资源路径引用，将老路径替换为 `uuid://` 格式。

**支持的引用格式**：

| 格式 | 示例 | 说明 |
|------|------|------|
| 属性 name/path/Name | `<texture name="Textures/UI.png"/>` | 材质、LOD 等配置 |
| attribute value | `<attribute name="Model" value="Model;Models/Box.mdl"/>` | 场景/预制体资源引用 |
| variant ResourceRef | `<variant type="ResourceRef" value="Image;Textures/UI.png"/>` | UI Style 资源引用 |

**替换后示例**：

```xml
<!-- 替换前 -->
<attribute name="Model" value="Model;Models/Box.mdl"/>

<!-- 替换后 -->
<attribute name="Model" value="Model;uuid://C3y7ubiP8nQLJmOepTuuvfqU"/>
```

---

## 目录结构示例

### 开发时目录结构

```
Assets/
├── Textures/
│   ├── player.png              ← 原始图片
│   ├── player.xml              ← Urho 运行时配置（srgb、filter）
│   └── player.png.meta         ← 纯元数据（uuid、group）
│
├── Audio/
│   ├── bgm.ogg                 ← 原始音频
│   ├── bgm.xml                 ← Urho 运行时配置（loop、stream）
│   └── bgm.ogg.meta            ← 纯元数据
│
├── Prefabs/
│   ├── enemy.prefab            ← 引擎格式（纯数据）
│   └── enemy.prefab.meta       ← 纯元数据
│
├── Scenes/
│   ├── level_1.xml             ← 场景数据
│   └── level_1.xml.meta        ← 纯元数据
│
└── Scripts/
    ├── main.lua                ← 脚本文件
    └── main.lua.meta           ← 纯元数据
```

### 构建后目录结构

```
Build/{version}/
├── manifest.json               ← 所有 meta 信息合并于此
└── assets/
    ├── Wjyfex0KT2watjVfL4xKfg0c.png    ← 贴图（重命名）
    ├── Wjyfex0KT2watjVfL4xKfg0c.xml    ← 贴图配置（短期保留）
    ├── Xk2mPqR9sT4vWxYz3bABcd.ogg      ← 音频
    ├── Xk2mPqR9sT4vWxYz3bABcd.xml      ← 音频配置
    ├── 7fXk2mPqR9sT4vWxYz3bAB.prefab   ← Prefab
    ├── 8gYl3nQs0U5xXyZa4cCDef.xml      ← 场景
    └── 9hZm4oRt1V6yYzAb5dDEfg.lua      ← 脚本
    
    # 注意：所有 .meta 文件都被剔除了！
```

---

## 构建流程中的处理

### 构建规则

```
┌─────────────────────────────────────────────────────────────────────┐
│                    构建时文件处理规则                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  输入文件              处理方式              输出                    │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  *.meta          →    提取信息到 manifest   →    ❌ 不输出          │
│                                                                     │
│  *.png/jpg/...   →    重命名为 uuid.ext     →    ✅ uuid.ext       │
│                       如有同名 .xml 配置         强制生成 fs_path   │
│                                                                     │
│  配置.xml        →    重命名为 uuid.xml     →    ✅ uuid.xml       │
│  (同名资源存在)       强制生成 fs_path           （短期方案）        │
│                                                                     │
│  *.prefab        →    重命名为 uuid.prefab  →    ✅ uuid.prefab    │
│  *.scene.xml     →    重命名为 uuid.xml     →    ✅ uuid.xml       │
│  *.lua           →    重命名为 uuid.lua     →    ✅ uuid.lua       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**同名配置文件处理**：当资源存在同名 `.xml` 配置文件时，两者都必须生成 `fs_path`，以便运行时通过路径关联。

### 构建流程

```
1. 扫描资源目录
   └── 收集所有 *.meta 文件

2. 提取 meta 信息
   ├── uuid → manifest.files[].uuid
   ├── group → manifest.files[].groups
   └── c_or_s → manifest.files[].c_or_s

3. 处理资源文件
   ├── 资源文件 → 重命名为 {uuid}.{ext}
   └── 配置文件（如有） → 重命名为 {uuid}.xml

4. 生成构建产物
   ├── manifest.json
   └── assets/{uuid}.{ext}

5. 清理
   └── 所有 *.meta 文件不输出
```

### Manifest 结构

```jsonc
{
  "manifest_version": "2.0",
  "project": { "id": "game_001", "version": "1.2.5" },
  
  "files": [
    {
      // 基础信息（从 .meta 提取）
      "uuid": "Wjyfex0KT2watjVfL4xKfg0c",
      "path": "Wjyfex0KT2watjVfL4xKfg0c.png",
      "fs_path": "Textures/player.png",
      "type": "Texture2D",
      
      // 元数据（从 .meta 提取）
      "groups": ["ui", "level_1"],
      "c_or_s": "c",
      
      // 文件信息
      "hash": "a1b2c3d4",
      "size": 10240,
      
      // 是否有独立的运行时配置文件
      "has_config": true   // 表示存在 uuid.xml 配置文件
    },
    {
      // Prefab 没有独立配置文件
      "uuid": "7fXk2mPqR9sT4vWxYz3bAB",
      "path": "7fXk2mPqR9sT4vWxYz3bAB.prefab",
      "type": "Prefab",
      "groups": ["level_1"],
      "has_config": false
    }
  ]
}
```

---

## 边玩边下优化

### 下载优先级

```
1. manifest.json          (~50KB)   ← 最高优先级，包含所有元数据
2. 预加载资源              (~2MB)    ← preload_groups 中的资源
   └── 资源文件 + 配置文件（如有）
3. 当前关卡资源            (按需)    ← 边玩边下
4. 其余资源               (后台)    ← 后台下载
```

### 关键优化点

| 优化 | 说明 |
|------|------|
| **manifest 预加载** | 包含所有 meta 信息，一次下载，全局可用 |
| **配置文件小** | `.xml` 配置文件通常 < 1KB，下载开销小 |
| **长期消除配置文件** | KTX2 内嵌配置后，无需额外下载 |

---

## 长期演进方案

### 演进路径

```
┌─────────────────────────────────────────────────────────────────────┐
│                    配置文件演进路径                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  阶段 1（当前）                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│  player.png + player.xml + player.png.meta                          │
│  （三个文件）                                                        │
│                                                                     │
│                            ↓                                        │
│                                                                     │
│  阶段 2（短期目标）                                                  │
│  ─────────────────────────────────────────────────────────────────  │
│  uuid.png + uuid.xml                                                │
│  （两个文件，meta 已合并到 manifest）                                │
│                                                                     │
│                            ↓                                        │
│                                                                     │
│  阶段 3（长期目标）                                                  │
│  ─────────────────────────────────────────────────────────────────  │
│  uuid.ktx2                                                          │
│  （一个文件，配置内嵌）                                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### KTX2 格式（贴图长期方案）

> **TODO**: 实现 KTX2 支持，将纹理配置（srgb、filter、address 等）内嵌到 KTX2 文件的 Key-Value Data 区域，彻底消除同名 .xml 配置文件的依赖。

KTX2 是 Khronos 推出的现代纹理容器格式，支持配置内嵌：

```
uuid.ktx2
┌──────────────────────────────────────┐
│ KTX2 Header                          │
├──────────────────────────────────────┤
│ Key-Value Data                       │ ← 运行时配置内嵌
│ {                                    │
│   "srgb": true,                      │
│   "filter": "trilinear"              │
│ }                                    │
├──────────────────────────────────────┤
│ Mipmap Level 0 (ASTC/ETC2/BC)        │ ← GPU 压缩格式
│ Mipmap Level 1                       │
│ ...                                  │
└──────────────────────────────────────┘
```

**优势**：
- 一个文件 = 图片数据 + 运行时配置
- 支持 GPU 压缩格式（ASTC/ETC2/BC）
- 行业标准，工具链成熟

### 各资源类型长期方案

| 资源类型 | 短期方案 | 长期方案 |
|---------|---------|---------|
| **贴图** | `uuid.png` + `uuid.xml` | `uuid.ktx2`（配置内嵌） |
| **音频** | `uuid.ogg` + `uuid.xml` | `uuid.ogg`（配置合并到 manifest） |
| **模型** | `uuid.mdl` | `uuid.mdl` 或 glTF 2.0 |
| **Prefab** | `uuid.prefab` | `uuid.prefab`（配置在文件内部） |
| **场景** | `uuid.xml` | `uuid.xml`（配置在文件内部） |
| **脚本** | `uuid.lua` | `uuid.lua`（无需配置） |

---

## 总结

### 核心要点

1. **Meta 文件完全独立**：`.meta` 只存元数据，不混入任何其他文件
2. **引擎配置保持原样**：`.xml` 配置文件不添加 uuid/group 等字段
3. **构建时统一剔除**：所有 `.meta` → 提取信息到 manifest → 丢弃
4. **运行时配置短期保留**：`.xml` 配置文件随资源一起下载
5. **长期内嵌优化**：KTX2 等格式内嵌配置，减少文件数量

### UUID 引用规范

配置文件中引用 UUID 资源时，统一使用 `uuid://` 协议：

```jsonc
{
  // ✅ 正确 - 使用 uuid:// 协议
  "entry": "uuid://C3y7ubiP8nQLJmOepTuuvfqU",
  "config": "uuid://D4z8vcjQ9oRMKnPfqUvwxhsW",
  
  // ❌ 不再支持
  // "entry": "C3y7ubiP8nQLJmOepTuuvfqU",
  // "font": "official://L1g5cjQX6vYTRuWmxBceDoZd"
}
```

> **例外**：`.meta` 文件中的 `uuid` 字段值本身就是 UUID，无需协议前缀。

### 文件对照表

| 开发时 | 构建后 | 说明 |
|--------|--------|------|
| `player.png` | `uuid.png` | 资源重命名 |
| `player.xml` | `uuid.xml` | 配置重命名（短期保留） |
| `player.png.meta` | ❌ | 剔除，信息在 manifest |
| `enemy.prefab` | `uuid.prefab` | 引擎格式重命名 |
| `enemy.prefab.meta` | ❌ | 剔除，信息在 manifest |

---

## 相关文档

- [INDEX.md](./INDEX.md) - 完整构建流程
- [resource-uuid-design.md](./resource-uuid-design.md) - UUID 设计

---

*最后更新: 2025-12-12*
