# UrhoX 游戏项目工作流指南（手动版）

本文件夹包含 UrhoX 具体游戏项目的完整工作流工具，支持创建、构建、上传和测试。

---

## 文件结构

```
project-workflow-manual/
├── README.md              # 本文档
├── create_project.bat     # 创建项目
├── build_project.bat      # 构建项目
└── upload_project.bat     # 上传项目
```

---

## 快速开始（3 步完成）

双击运行 bat 文件即可进入交互模式：

1. **创建项目** - 双击 `create_project.bat`
2. **构建项目** - 双击 `build_project.bat`，输入项目目录
3. **上传项目** - 双击 `upload_project.bat`，输入项目目录

或命令行运行：
```batch
create_project.bat
build_project.bat <项目目录>
upload_project.bat <项目目录>
```

完成后访问远端测试：
```
https://tapcode-sce.spark.xd.com/src/web/index.html?game_url=https://tapcode-sce.spark.xd.com/src/<project_id>/
```

---

## 工具说明

### 1. create_project.bat - 创建项目

```batch
REM 交互式创建（推荐新手）
create_project.bat

REM 命令行创建
create_project.bat my_game --author test_user

REM 指定入口脚本
create_project.bat my_game --author test_user --entry game.lua
```

**功能**：
- 从 `tapcode-agent-project` 模板复制创建项目
- 自动填写 `project_id`、`author_id`
- 生成入口脚本文件
- 显示后续构建和上传命令

---

### 2. build_project.bat - 构建项目

```batch
REM 基本构建
build_project.bat my_game

REM 调试模式（详细输出）
build_project.bat my_game --debug
```

**功能**：
- 生成资源 UUID 和 hash
- 创建 manifest 清单文件
- 输出到项目的 `dist/` 目录

**构建产物**：
```
dist/
├── latest.json              # 指向最新版本
├── project.json             # 项目信息
├── assets/                  # 资源文件（UUID-hash 命名）
└── 1.0.0/                   # 版本目录
    ├── version.json
    └── manifest-{hash}.json
```

---

### 3. upload_project.bat - 上传项目

```batch
REM 预览上传（不实际上传）
upload_project.bat my_game --dry-run

REM 正式上传
upload_project.bat my_game
```

**功能**：
- 上传 `dist/` 中的构建产物到 OSS
- 自动显示远端测试 URL

---

## 远端测试

上传成功后，通过以下 URL 测试：

```
https://tapcode-sce.spark.xd.com/src/web/index.html?game_url=https://tapcode-sce.spark.xd.com/src/<project_id>/
```

**URL 参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `game_url` | 项目 CDN 地址（必填） | `?game_url=https://tapcode-sce.spark.xd.com/src/my_game/` |

---

## 官方项目

以下是 UrhoX 官方维护的项目及模板，位于 `tools/project-tools/` 目录下：

### 项目模板

| 项目目录 | 说明 |
|----------|------|
| [`tapcode-agent-project/`](../../tools/project-tools/tapcode-agent-project/) | 新项目模板，`create_project.bat` 基于此模板创建项目 |

### 引擎发布（使用 project 载体上传）

| 项目目录 | project_id | 说明 |
|----------|------------|------|
| [`engine-project/`](../../tools/project-tools/engine-project/) | `engine` | WASM 引擎本体 |
| [`engine-res-project/`](../../tools/project-tools/engine-res-project/) | `engine-res` | 引擎内置资源 |

### 示例项目

| 项目目录 | project_id | 说明 |
|----------|------------|------|
| [`welcome-project/`](../../tools/project-tools/welcome-project/) | `welcome` | 欢迎演示项目，入口脚本 `LuaScripts/main.lua` |

---

## 测试项目 URL

以下是常用的测试项目远端访问链接：

### 官方项目

| 项目 | 测试 URL |
|------|----------|
| welcome | https://tapcode-sce.spark.xd.com/src/web/index.html?game_url=https://tapcode-sce.spark.xd.com/src/welcome/ |

### 测试项目

| 项目 | 测试 URL |
|------|----------|
| p_test | https://tapcode-sce.spark.xd.com/src/web/index.html?game_url=https://tapcode-sce.spark.xd.com/src/p_test/ |
| flag_test | https://tapcode-sce.spark.xd.com/src/web/index.html?game_url=https://tapcode-sce.spark.xd.com/src/flag_test/ |

---

## 项目结构

创建的项目结构如下：

```
my_game/
├── .project/                # 配置目录
│   ├── project.json         # 项目信息（必填）
│   ├── settings.json        # 构建配置
│   ├── resources.json       # 资源配置
│   └── resources-aliases.json
├── assets/                  # 资源目录（贴图、模型等）
├── scripts/                 # Lua 脚本目录
└── dist/                    # 构建产物（自动生成）
```

### project.json 配置

```json
{
  "project_id": "my_game",
  "name": "My Game",
  "author": {
    "id": "developer_001",
    "name": "Your Name"
  },
  "entry": "LuaScripts/main.lua",
  "version": "1.0.{x}"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `project_id` | ✅ | 项目唯一标识，用于远端 URL |
| `name` | ✅ | 项目显示名称 |
| `author.id` | ✅ | 作者 ID，用于 UUID 生成 |
| `entry` | ✅ | 入口 Lua 脚本 |
| `version` | ✅ | 版本号，`{x}` 自动递增 |

---

## 完整流程示例

```batch
REM Step 1: 创建项目
create_project.bat hello_world --author test_user

REM Step 2: 进入项目目录，编辑 scripts/LuaScripts/main.lua
REM function Start()
REM     print("Hello World!")
REM end

REM Step 3: 构建
build_project.bat G:\Workspace\SCE\NE\UrhoX-Replica\tools\project-tools\hello_world

REM Step 4: 预览上传
upload_project.bat G:\Workspace\SCE\NE\UrhoX-Replica\tools\project-tools\hello_world --dry-run

REM Step 5: 正式上传
upload_project.bat G:\Workspace\SCE\NE\UrhoX-Replica\tools\project-tools\hello_world

REM Step 6: 远端测试
REM 浏览器访问：https://tapcode-sce.spark.xd.com/src/web/index.html?game_url=https://tapcode-sce.spark.xd.com/src/hello_world/
```

---

## 常见问题

### Q: 构建报错 "project_id 未设置"
A: 编辑 `.project/project.json`，填写 `project_id` 字段

### Q: 上传后访问 404
A: 检查 URL 中的 `project` 参数是否与 `project_id` 一致

### Q: 版本号没有递增
A: 确保 `version` 字段包含 `{x}` 占位符，如 `"1.0.{x}"`

### Q: 资源加载失败
A: 检查 `settings.json` 中的 `asset_dirs` 配置是否正确

---

## Python 命令参考

如需直接使用 Python 脚本：

```bash
# 创建项目
python tools/project-tools/project_creator.py [project_name] --author <author_id>

# 构建
python tools/project-tools/project_builder.py --project <dir> [--debug]

# 上传
python tools/project-tools/project_uploader.py --project <dir> --host publisher-alpha.spark.xd.com --im_vip [--dry-run] [--full]
```

---

## 相关文档

- [project-tools/README.md](../../tools/project-tools/README.md) - 工具集详细说明
- [project-build-pipeline](../project-build-pipeline/) - 构建管线设计

---

*最后更新: 2025-12-22*
