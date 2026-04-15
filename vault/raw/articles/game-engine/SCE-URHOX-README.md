# MCP SCE UrhoX

基于 `@modelcontextprotocol/sdk` 的 MCP 服务，内置创建项目与调试启动两个工具，可通过 stdio 与 MCP 客户端交互，也能独立作为命令行工具使用。

## 功能架构简介

- `src/index.ts`：MCP 服务入口，同时处理 CLI 模式与 stdio 模式。
- `src/tools/`：工具注册与实现，包含 `create-project`、`start-debug`。
- `src/server/UrhoXHelper.ts`：提供调试用静态资源 HTTP 服务。
- `src/utils/console-logger.ts`：将日志写入工作目录下的 `.sce/mcp-sce-hrhox.log`。

## 安装

```bash
# 项目内安装
npm install sce-urhox-mcp

# 或全局安装（便于在命令行直接调用）
npm install -g sce-urhox-mcp

# 更新(全局更新应添加-g)
npm update sce-urhox-map
```

## 使用

### 方案一：通过 `.mcp.json` 挂载 MCP 服务

在 MCP 客户端的配置中新增：

```json
{
  "mcpServers": {
    "sce-urhox-mcp": {
      "command": "sce-urhox-mcp",
      "args": ["--mcp"]
    }
  }
}
```

客户端启动后即可在工具列表中看到 `create-project` 与 `start-debug`。

### 方案二：命令行模式

默认以 CLI 方式运行，需要作为 MCP 服务时再加上 `--mcp`。

```bash
# 查看帮助
sce-urhox-mcp --help

# 创建项目 - 支持以下两种写法：
# 1. 使用 --path 长选项（推荐使用绝对路径）
sce-urhox-mcp create-project --path "/absolute/path/to/project"

# 2. 直接传位置参数（第一个参数自动映射为 path）
sce-urhox-mcp create-project /absolute/path/to/project

# 启动调试（目录需含 project.sce 与 bin/AgentProject）
sce-urhox-mcp start-debug --path "/absolute/path/to/project"
# 或使用位置参数
sce-urhox-mcp start-debug /absolute/path/to/project

# 自定义调试地址与端口（命令行优先于配置文件）
sce-urhox-mcp start-debug --path "/absolute/path/to/project" --address 0.0.0.0 --port 18080

# 以 MCP 模式运行（提供给其他客户端）
sce-urhox-mcp --mcp
```

**路径参数说明：**
- 支持 `--path "/path"` 或 `--path=/path` 格式
- 支持位置参数：直接传路径作为第一个参数，会自动映射为 `path` 字段
- 相对路径会自动转换为绝对路径
- 支持 `~` 扩展为用户主目录（如 `--path=~/projects/my-app` 或 `~/projects/my-app`）

## 工具概览

- `create-project`：创建新项目目录，拉取 `UrhoXRuntime-wasm.zip` 模板, 根据参数`path`创建项目文件夹。Lua 默认入口为 `{path}/bin/AgentProject/Scripts/main.lua`, 你可以通过修改`bin/AgentProject/commandline.txt`指定。
- `start-debug`：校验项目结构后启动静态资源 HTTP 服务，返回可访问的 `url`、`port`、`host`，并默认开放跨域访问方便前端调试。
- `build`：**[必选]** 官方构建工具，用于构建 SCE/UrhoX 项目。支持 C/S 架构入口点配置和多人游戏配置。

---

## build 工具详解

`build` 是 SCE/UrhoX 项目的官方构建工具，**必须使用此工具进行构建**，不要编写自定义构建脚本。

### 基本参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `scriptsPath` | string | ✅ | 脚本目录路径（相对于 workspace，如 `project-name/scripts`） |

### 入口点配置

所有入口路径均相对于 `scriptsPath`，二选一：

| 配置方式 | 参数 | 描述 |
|----------|------|------|
| **单机游戏** | `entry` | 统一入口（如 `main.lua`） |
| **联网游戏 C/S** | `entry_client` + `entry_server` | 客户端入口 + 服务端入口（如 `client_main.lua`、`server_main.lua`） |

**构建时入口选择：**
- **客户端构建**：`entry_client` → `entry`
- **服务端构建**：`entry_server` → `entry`

### 多人游戏配置

`multiplayer` 参数用于配置网络游戏功能。配置会写入 `.project/settings.json` 的 `@runtime` 字段，并在构建时生成运行时资源。

#### 完整字段列表

| 参数 | 类型 | 描述 | 运行时默认值 |
|------|------|------|------------|
| `enabled` | boolean | 启用多人游戏模式。启用后初始化网络子系统和大厅 | `false` |
| `max_players` | number (2-100) | 最大玩家数上限。实际组队/开房可以少于此数，但不会超过 | `4` |
| `background_match` | boolean | 是否启用后台匹配模式（详见下方说明） | `false` |
| `match_info` | object | 匹配配置（见下表） | - |

#### background_match 后台匹配模式说明

当 `background_match` 设为 `true` 时：
1. 多人游戏进入后**直接加载游戏脚本**
2. 匹配逻辑在**后台自动触发**
3. 匹配成功后会触发 `ServerReady` 事件
4. 通过 `SubscribeToEvent` 订阅该事件来处理匹配成功回调

```lua
-- 示例：订阅 ServerReady 事件
SubscribeToEvent("ServerReady", function()
    -- 匹配成功，可以开始游戏逻辑
end)
```

> ⚠️ **注意**：非后台匹配模式（`background_match = false`）**不需要**处理 `ServerReady` 事件！

#### match_info 字段详解

| 参数 | 类型 | 描述 |
|------|------|------|
| `desc_name` | string | 匹配算法：`free_match`（超时不塞AI）、`free_match_with_ai`（超时后塞入AI） |
| `player_number` | number | 匹配需要凑齐的人数（必须 ≤ `max_players`）。系统等待凑齐后开局；超时后 `free_match_with_ai` 用AI补齐，`free_match` 继续等待 |
| `immediately_start` | boolean | 是否直接匹配开局（秒开模式） |
| `match_timeout` | number | 匹配超时时间（秒）。仅在 `desc_name` 为 `free_match_with_ai` 时生效，超时后会塞入AI |

#### 增量更新机制

**支持增量更新**：多次构建时，只需传入要更新的字段，其他字段会保持不变。

| 场景 | 传入参数 | 行为 |
|------|---------|------|
| 首次配置多人游戏 | 传入所有必要字段 | 创建完整配置 |
| 后续构建不改配置 | 不传 `multiplayer` | 保持现有配置 |
| 只更新部分字段 | 传入要更新的字段 | 增量合并，保留其他字段 |
| 快速切换单/多人 | 只传 `enabled` | 切换模式，保留其他配置 |

**快速测试开关**：单独更新 `enabled` 字段可以快速切换单人/多人模式。开启时会启动前置大厅。

#### 配置示例

**首次配置完整多人游戏：**
```json
{
  "multiplayer": {
    "enabled": true,
    "max_players": 8
  }
}
```

> **注意**：以上所有字段（除 `enabled` 外）如果不指定，运行时会使用默认值。

**配置带匹配功能的多人游戏：**
```json
{
  "multiplayer": {
    "enabled": true,
    "max_players": 20,
    "background_match": true,
    "match_info": {
      "desc_name": "free_match_with_ai",
      "player_number": 4,
      "immediately_start": false,
      "match_timeout": 60
    }
  }
}
```

**只配置普通匹配（不塞AI）：**
```json
{
  "multiplayer": {
    "enabled": true,
    "background_match": true,
    "match_info": {
      "desc_name": "free_match",
      "player_number": 4,
      "immediately_start": false
    }
  }
}
```

**后续只更新玩家数：**
```json
{
  "multiplayer": {
    "max_players": 16
  }
}
```

**快速切换到单人模式测试：**
```json
{
  "multiplayer": {
    "enabled": false
  }
}
```

**切换回多人模式：**
```json
{
  "multiplayer": {
    "enabled": true
  }
}
```

#### 数据流向

```
MCP build 参数                    .project/settings.json
multiplayer: {            →      @runtime: {
  enabled: true,                   multiplayer: {
  max_players: 8,                     enabled: true,
  background_match: true,             max_players: 8,
  match_info: {                       background_match: true,
    desc_name: "...",                 match_info: {
    player_number: 4,                   desc_name: "...",
    immediately_start: false,           player_number: 4,
    match_timeout: 60               immediately_start: false,
  }                                     match_timeout: 60
}                                     }
                                    }
                                  }
        ↓
构建时 step_generate_runtime_config.py 提取 @runtime
        ↓
运行时资源 settings.json (根级 multiplayer 对象)
        ↓
UrhoXServer 读取配置
```

### 完整调用示例

**单人游戏项目：**
```json
{
  "scriptsPath": "scripts",
  "entry": "main.lua"
}
```

**多人游戏项目（C/S 分离入口）：**
```json
{
  "scriptsPath": "scripts",
  "entry_client": "client_main.lua",
  "entry_server": "server_main.lua",
  "multiplayer": {
    "enabled": true,
    "max_players": 8
  }
}
```

**带匹配功能的多人游戏项目：**
```json
{
  "scriptsPath": "scripts",
  "entry_client": "client_main.lua",
  "entry_server": "server_main.lua",
  "multiplayer": {
    "enabled": true,
    "max_players": 20,
    "background_match": true,
    "match_info": {
      "desc_name": "free_match_with_ai",
      "player_number": 4,
      "immediately_start": false,
      "match_timeout": 100000
    }
  }
}
```

### 构建流程

1. **写入配置** - 写入 `entry_client`、`entry_server` 到 project.json（可选），写入 `@runtime.multiplayer` 到 settings.json（可选）
2. **验证入口文件** - 确认 `entry` 存在且包含 `Start()` 函数
3. **验证脚本目录** - 确认 `scriptsPath` 存在
4. **Lua LSP 检查** - 运行语法和类型检查
5. **初始化项目** - 创建 `.project` 目录和必要文件
6. **推导 entry** - 从 `entry` 推导 `entry` 写入 `project.json`
7. **执行构建** - 调用 `project_builder.py` 进行资源打包

---

## UrhoXHelper 配置与跨域

调试 HTTP 服务的地址策略如下：

- **监听地址与端口**：最终绑定在解析出的 `address:port` 上（默认端口 `12345`）。`address` 的决策顺序为：
  1. CLI / MCP 参数中的 `address`
  2. 项目根目录 `debug-config.yaml` 的 `UrhoXHelper.address`
  3. 自动探测到的局域网 IPv4（找不到时回退到 `127.0.0.1`）
- `port` 的优先级同上（CLI / MCP > `debug-config.yaml` > 默认值）。
- **配置文件示例**：

  ```yaml
  UrhoXHelper:
    port: 12346
    address: 192.168.1.50
  ```

  - `port` 支持数值或字符串形式，合法范围 `1-65535`。
  - `address` 接受任意非空字符串；留空则按照上面的优先级自动推算。

所有 HTTP 接口默认开启 CORS，允许任意来源、任意方法和自定义请求头，方便浏览器或其它工具直接访问。

## 上传模式

项目上传到 CDN 支持两种模式：

### ossutil 模式（默认，推荐）
使用阿里云 `ossutil` 命令行工具直接流式上传到 OSS，大幅降低内存占用，适合大型项目（1GB+）。

**优势**：
- 内存占用低（固定 ~28MB，不随项目大小增长）
- 消除因内存不足导致的 SIGKILL
- 支持断点续传

**配置要求**：
- 环境变量 `ALIYUN_OSS_ACCESS_KEY_ID`（已在 docker-compose.yml 中配置）
- 环境变量 `ALIYUN_OSS_ACCESS_KEY_SECRET`（已在 docker-compose.yml 中配置）
- Docker 镜像中已预装 ossutil

### 传统模式
通过 HTTP multipart 方式上传文件到 `upload-map-urhox` API，API 再转存到 OSS。

**禁用 ossutil 模式**：设置环境变量 `DISABLE_OSSUTIL_UPLOAD=true`

---

## 发布流程
先跳转到packages/mcp-sce-urhox `cd packages/mcp-sce-urhox`
1. 更新版本号：`npm version <patch|minor|major>`。
2. 构建产物：`npm run build`。
3. 登录 npm（首次需 `npm login`）：`npm publish --access public`。

