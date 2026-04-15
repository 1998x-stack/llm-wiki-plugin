---
summary: "Manual workflow for querying UrhoX project version info and resource files"
last_updated: "2025-12-26"
---

# 项目资源手动查询流程

本文档描述如何手动查询 UrhoX 项目的版本信息和资源文件。

---

## 快速开始（直接贴脚本）

```bash
# 查看帮助
python tools/project-tools/resource_query.py --help

# 通过 UUID 查询
python tools/project-tools/resource_query.py uuid://BuCGwRfcPuyhFwFmDcylLE_Y

# 通过路径查询（支持部分匹配）
python tools/project-tools/resource_query.py --path "Vehicles/Car01/Car01.prefab"

# 指定项目
python tools/project-tools/resource_query.py --path "version.json" --project engine

# 指定版本（tag 或版本号）
python tools/project-tools/resource_query.py --path "version.json" --project engine --tag stable
python tools/project-tools/resource_query.py --path "version.json" --project engine --tag 1.1.5

# 查询版本信息
python tools/project-tools/resource_query.py --version --project engine

# 查询依赖链
python tools/project-tools/resource_query.py uuid://BuCGwRfcPuyhFwFmDcylLE_Y --refs

# 下载资源
python tools/project-tools/resource_query.py uuid://BuCGwRfcPuyhFwFmDcylLE_Y --download
```

---

## URL 结构规范

### Base URL 格式

```
https://tapcode-sce.spark.xd.com/src/{project_id}/
```

### 官方项目 ID

| Project ID | 说明 |
|------------|------|
| `engine` | 引擎运行时 (WASM/Native) |
| `engine-res` | 引擎内置资源 |
| `official-res` | 官方公共资源库 |

### 引用协议

| 协议 | 说明 | 示例 |
|------|------|------|
| `uuid://xxx` | UUID 资源引用 | `uuid://BuCGwRfcPuyhFwFmDcylLE_Y` |
| `{source}://path` | 源协议路径引用 | `official://Textures/logo.png` |

> `{source}://` 映射到 `settings.sources[{source}].base_url`

---

## 三层查询架构

```
[Layer 1] 版本索引
    {base_url}/latest.json
              ↓
    { version, client, server }
              ↓
[Layer 2] 资源清单
    {base_url}/{version}/manifest-{client}.json
              ↓
    { files: [{ uuid, hash, ext, fs_path, refs, ... }] }
              ↓
[Layer 3] 具体资源
    {base_url}/assets/{uuid}-{hash}.{ext}
```

---

## 查询步骤

### Step 1: 获取版本信息

| 场景 | URL |
|------|-----|
| 最新版本 | `{base_url}/latest.json` |
| 稳定版本 | `{base_url}/stable.json` |
| 指定 tag | `{base_url}/{tag}.json` |
| 指定版本 | `{base_url}/{version}/version.json` |

**返回格式**:
```json
{
  "version": "1.1.5",
  "client": "ab651f76",
  "server": "90393d60"
}
```

### Step 2: 获取资源清单 (Manifest)

根据 Step 1 的 `client` 或 `server` hash 拼接：

```
{base_url}/{version}/manifest-{hash}.json
```

**Manifest 文件结构**:
```json
{
  "entry": "uuid://xxx",
  "files": [
    {
      "uuid": "BuCGwRfcPuyhFwFmDcylLE_Y",
      "hash": "4064f2da",
      "ext": ".prefab",
      "size": 8413,
      "groups": ["official-prefabs"],
      "fs_path": "Vehicles/Car01/Car01.prefab",
      "refs": ["EI1iubludiM_3nrWdtaBaQ_k", "..."]
    }
  ]
}
```

### Step 3: 获取具体资源

根据 `uuid`、`hash`、`ext` 拼接资源 URL：

```
{base_url}/assets/{uuid}-{hash}.{ext}
```

---

## 完整示例：查询跑车预制体

**目标**: 查询 `uuid://BuCGwRfcPuyhFwFmDcylLE_Y`

### Step 1: 获取版本

```
GET https://tapcode-sce.spark.xd.com/src/official-res/latest.json

Response:
{
  "version": "1.1.5",
  "client": "ab651f76",
  "server": "90393d60"
}
```

### Step 2: 查询 Manifest

```
GET https://tapcode-sce.spark.xd.com/src/official-res/1.1.5/manifest-ab651f76.json

在 files[] 中查找 uuid = "BuCGwRfcPuyhFwFmDcylLE_Y"

Result:
{
  "uuid": "BuCGwRfcPuyhFwFmDcylLE_Y",
  "ext": ".prefab",
  "hash": "4064f2da",
  "size": 8413,
  "groups": ["official-prefabs"],
  "fs_path": "Vehicles/Car01/Car01.prefab",
  "refs": [
    "EI1iubludiM_3nrWdtaBaQ_k",  // Car01_Body.mdl
    "AKheOQ3zlh2tWjNDZbX8rsCX",  // 材质
    // ... 共 15 个依赖
  ]
}
```

### Step 3: 下载资源

```
GET https://tapcode-sce.spark.xd.com/src/official-res/assets/BuCGwRfcPuyhFwFmDcylLE_Y-4064f2da.prefab

Content-Length: 8413
```

### 流程图

```
uuid://BuCGwRfcPuyhFwFmDcylLE_Y
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: GET .../src/official-res/latest.json                │
│         → version: "1.1.5", client: "ab651f76"              │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: GET .../src/official-res/1.1.5/manifest-ab651f76.json│
│         → 查找 uuid = "BuCGwRfcPuyhFwFmDcylLE_Y"            │
│         → hash: "4064f2da", ext: ".prefab"                  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 资源 URL                                             │
│ https://tapcode-sce.spark.xd.com/src/official-res/assets/   │
│         BuCGwRfcPuyhFwFmDcylLE_Y-4064f2da.prefab            │
└─────────────────────────────────────────────────────────────┘
```

---

## 示例：查询引擎构建详情

**目标**: 查询引擎的 commit hash、分支、构建时间

### Step 1: 获取版本

```
GET https://tapcode-sce.spark.xd.com/src/engine/latest.json

Response:
{
  "version": "1.1.7",
  "client": "b1f70dfa",
  "server": "d82dd32d"
}
```

### Step 2: 从 Manifest 找 version.json

```
GET https://tapcode-sce.spark.xd.com/src/engine/1.1.7/manifest-b1f70dfa.json

在 files[] 中查找 fs_path = "version.json"

Result:
{
  "uuid": "AdIkSQ_H0joILNj_fg1tJzWa",
  "hash": "dc85d4af",
  "ext": ".json",
  ...
}
```

### Step 3: 获取构建详情

```
GET https://tapcode-sce.spark.xd.com/src/engine/assets/AdIkSQ_H0joILNj_fg1tJzWa-dc85d4af.json

Response:
{
  "timestamp": "2025-12-26T07:40:10.864420",
  "binary_hash": "fb300de3",
  "commit_hash": "bc99595e",
  "branch": "main"
}
```

### 使用脚本

```bash
# 查询引擎版本
python tools/project-tools/resource_query.py --version --project engine

# 查询 version.json 资源
python tools/project-tools/resource_query.py --path "version.json" --project engine
```

---

## 快速参考

### URL 模板

| 查询目标 | URL |
|---------|-----|
| 最新版本 | `https://tapcode-sce.spark.xd.com/src/{project_id}/latest.json` |
| 稳定版本 | `https://tapcode-sce.spark.xd.com/src/{project_id}/stable.json` |
| Client Manifest | `https://tapcode-sce.spark.xd.com/src/{project_id}/{version}/manifest-{client}.json` |
| Server Manifest | `https://tapcode-sce.spark.xd.com/src/{project_id}/{version}/manifest-{server}.json` |
| 具体资源 | `https://tapcode-sce.spark.xd.com/src/{project_id}/assets/{uuid}-{hash}.{ext}` |

### Manifest 字段说明

| 字段 | 说明 |
|------|------|
| `uuid` | 资源唯一标识 (24 字符 Base64) |
| `hash` | 内容哈希 (8 字符) |
| `ext` | 文件扩展名 |
| `size` | 文件大小 (bytes) |
| `groups` | 资源分组 |
| `fs_path` | 原始文件路径 |
| `refs` | 依赖资源 UUID 列表 |
| `alias` | 资源别名 (可选) |

---

## 相关文档

- [INDEX.md](../design/build-pipeline/INDEX.md) - 项目构建流程
- [resource-uuid-design.md](../design/build-pipeline/resource-uuid-design.md) - UUID 设计说明

---

*最后更新: 2025-12-26*
