---
summary: "UrhoXServer headless game server runtime designed for Linux server deployment"
last_updated: "2026-04-02"
---

# UrhoXServer - 无头游戏服务器

UrhoXServer 是 UrhoX 引擎的无头（headless）游戏服务器运行时，专为 Linux 服务器部署设计。

## 特性

- ✅ **无头模式**：无图形界面，不依赖 GPU
- ✅ **动态加载游戏**：通过 `-game_url` 参数加载不同的游戏
- ✅ **资源热更新**：复用 Bootstrap 系统，支持 CDN 资源下载
- ✅ **跨平台**：支持 Windows 和 Linux
- ✅ **配置灵活**：支持命令行参数和 JSON 配置文件

## 编译

### 启用服务器构建

在 CMake 配置时添加 `-DURHO3D_HEADLESS=ON` 选项：

```bash
# Linux
cmake -DURHO3D_HEADLESS=ON -DURHO3D_LUA=ON -DURHO3D_NETWORK=ON ..

# Windows (Visual Studio)
cmake -G "Visual Studio 17 2022" -DURHO3D_HEADLESS=ON -DURHO3D_LUA=ON -DURHO3D_NETWORK=ON ..
```

### 必需的构建选项

| 选项 | 说明 |
|------|------|
| `URHO3D_HEADLESS=ON` | 启用无头模式（独立游戏服务器，保留完整多线程支持） |
| `URHO3D_LUA=ON` | 启用 Lua 脚本支持 |
| `URHO3D_NETWORK=ON` | 启用网络功能 |

> **注意**: 不要使用 `URHO3D_SERVER=ON`，那是为嵌入式环境设计的，会跳过多线程检查。

## 使用方法

### 基本用法

```bash
# 标准启动（两个必需参数都由编排服务传入）
./UrhoXServer -game_url=https://games.example.com/my-game -port=7777

# 带服务器名称（用于日志区分）
./UrhoXServer -game_url=https://games.example.com/my-game -port=7777 -name=Server-01

# 多协议支持：同时启用 KCP 和 WebSocket
./UrhoXServer -game_url=https://games.example.com/my-game -port=7777 -ws_port=8080
```

### 命令行参数

| 参数 | 说明 | 来源 | 必需 |
|------|------|------|------|
| `-game_url=<url>` | 游戏资源 URL | 编排服务传入 | ✅ |
| `-port=<num>` | KCP 协议监听端口（主端口） | 编排服务传入 | ✅ |
| `-ws_port=<num>` | WebSocket 端口（用于网页客户端） | 可选 | ❌ |
| `-name=<name>` | 服务器名称（日志标识） | 可选 | ❌ |
| `-config=<file>` | 可选配置文件（调试用） | 可选 | ❌ |
| `-fps=<num>` | 服务器帧率限制，0 表示不限（默认：60） | 可选 | ❌ |
| `-idle_timeout=<sec>` | 空闲超时时间（秒），0 表示禁用（默认：300） | 可选 | ❌ |
| `-initial_wait=<sec>` | 初始等待玩家时间（秒），0 表示无限（默认：600） | 可选 | ❌ |
| `-help` | 显示帮助信息 | - | ❌ |

### 多协议支持

UrhoXServer 支持同时监听多种网络协议，让不同类型的客户端连接到同一服务器：

| 协议 | 端口参数 | 说明 | 适用客户端 |
|------|----------|------|-----------|
| KCP | `-port` | 主协议，可靠 UDP | PC/手机原生客户端 |
| WebSocket | `-ws_port` | 可选，TCP 基础 | 网页客户端 |

```bash
# Docker 多协议部署示例
docker run -p 7777:7777/udp -p 8080:8080/tcp urhox-server \
    -game_url=https://... -port=7777 -ws_port=8080

# Kubernetes 配置示例
args:
  - "-game_url=$(GAME_URL)"
  - "-port=$(KCP_PORT)"
  - "-ws_port=$(WS_PORT)"
```

### 设计原则

```
┌─────────────────────────────────────────────────────────────┐
│                    参数来源分离                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  编排服务传入（运行时决定）：                                  │
│  ├── game_url    ← 决定运行哪个游戏                          │
│  ├── port        ← KCP 协议端口（主端口）                     │
│  └── ws_port     ← WebSocket 端口（可选，用于网页客户端）      │
│                                                             │
│  游戏包内 settings.json（游戏定义）：                          │
│  ├── max_players ← 游戏支持的最大玩家数                       │
│  ├── server_fps  ← 服务器帧率（默认 60）                       │
│  ├── tick_rate   ← 游戏逻辑 Tick 频率                         │
│  └── 其他游戏配置                                             │
│                                                             │
│  可选配置文件（调试用）：                                      │
│  └── name        ← 服务器名称                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **设计理念**：
> - `game_url` 和 `port` 由编排服务传入，同一镜像可运行任意游戏
> - 游戏相关配置（max_players 等）在游戏包内定义
> - 服务器运行时本身几乎不需要配置

### 可选配置文件（仅用于调试）

```json
{
    "name": "GameServer-01",
    "log_level": "info"
}
```

## 自动退出保护机制

UrhoXServer 内置多层保护机制，确保服务器资源能被正确回收：

### 退出触发条件

| 机制 | 超时时间 | 触发条件 | 行为 |
|------|---------|---------|------|
| KCP 连接超时 | 10s | 单个客户端无响应 | 断开该连接 |
| 空闲超时 | 300s (可配置) | 所有玩家离开 | 服务器退出 |
| 初始等待超时 | 600s (可配置) | 启动后无人连接 | 服务器退出 |
| 游戏结束 | 5s | 脚本调用 ServerGameEnded | 服务器退出 |
| 玩家主动退出 | 即时 | 客户端发送 PlayerLeaving | 断开该连接 |

### 事件

服务器支持以下事件用于优雅退出：

| 事件名 | 类型 | 方向 | 说明 |
|--------|------|------|------|
| `PlayerLeaving` | 远程 | 客户端 -> 服务器 | 玩家主动点击退出按钮 |
| `ServerGameEnded` | 本地 | 脚本 -> 服务器 | 游戏逻辑结束，触发服务器关闭 |
| `ServerShuttingDown` | 远程 | 服务器 -> 客户端 | 服务器即将关闭 |

> **安全说明**：
> - `PlayerLeaving`：安全。服务器通过 `P_CONNECTION` 自动识别发送者，客户端无法伪装成其他玩家。
> - `ServerGameEnded`：安全。本地事件，只能由服务器端 Lua 脚本触发。客户端调用无效（不会发送到服务器）。

### 客户端 Lua 脚本示例

```lua
-- 【客户端 Lua 脚本】玩家点击退出按钮时调用
-- 通过 SendRemoteEvent 通知服务器玩家主动退出（区别于断线等异常情况）
function OnQuitButtonClicked()
    local serverConnection = network:GetServerConnection()
    if serverConnection then
        local eventData = VariantMap()
        eventData["Reason"] = "Player quit via menu"
        serverConnection:SendRemoteEvent("PlayerLeaving", true, eventData)
    end
    network:Disconnect()
end
```

### 服务器 Lua 脚本示例

```lua
-- 【服务器端 Lua 脚本】游戏结束时调用
-- ServerGameEnded 是服务器专用的本地事件
-- 客户端调用此事件无效（不会发送到服务器）
function OnGameOver(winner)
    print("[Server] Game over! Winner: " .. winner)
    
    local eventData = VariantMap()
    eventData["Reason"] = "Game finished, winner: " .. winner
    
    -- 触发服务器游戏结束事件（本地事件）
    -- 服务器会广播 ServerShuttingDown 给客户端，然后 5 秒后关闭
    SendEvent("ServerGameEnded", eventData)
end
```

### 配置示例

```yaml
# Kubernetes Deployment
containers:
- name: urhox-server
  args:
    - "-game_url=$(GAME_URL)"
    - "-port=7777"
    - "-idle_timeout=300"      # 5 分钟无人自动退出
    - "-initial_wait=600"      # 启动后最多等 10 分钟
```

## 游戏脚本集成

### 服务器入口函数

UrhoXServer 会按以下顺序查找并调用入口函数：

1. `StartServer()` - 服务器专用入口（优先）
2. `Start()` - 通用入口（回退）

### 示例游戏脚本

```lua
-- Scripts/main.lua

-- 服务器专用入口
function StartServer()
    print("[Server] Starting game server...")
    
    -- 初始化游戏逻辑
    InitGameWorld()
    
    -- 设置服务器事件处理
    SubscribeToEvent("ClientConnected", "HandleClientConnected")
    SubscribeToEvent("ClientDisconnected", "HandleClientDisconnected")
end

-- 客户端入口（服务器模式下不会调用）
function Start()
    print("[Client] Starting game client...")
    -- 客户端初始化逻辑
end

function HandleClientConnected(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    print("[Server] Client connected: " .. connection:GetAddress())
end

function HandleClientDisconnected(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    print("[Server] Client disconnected: " .. connection:GetAddress())
end
```

## 架构设计

```
UrhoXServer
├── ServerBootstrapManager     # 服务器专用启动管理器（无 UI）
│   ├── LoadVersionStep        # 加载版本信息
│   ├── LoadProjectManifestStep # 加载项目清单
│   ├── LoadSourceManifestsStep # 加载依赖源清单
│   ├── DownloadInitialPackageStep # 首次启动整包下载
│   ├── InitializeResourceRouterStep # 初始化资源路由
│   └── CleanupStep            # 清理废弃缓存
├── Network                    # 网络服务器
│   ├── KCP Transport          # KCP 传输层（默认）
│   └── WebSocket Transport    # WebSocket 传输层
└── LuaScript                  # Lua 脚本引擎
```

### 与 UrhoXRuntime 的区别

| 特性 | UrhoXRuntime | UrhoXServer |
|------|-------------|-------------|
| 渲染 | ✅ 有 | ❌ 无（headless） |
| UI | ✅ 有 | ❌ 无 |
| 音频 | ✅ 有 | ❌ 无 |
| 登录系统 | ✅ 有 | ❌ 无 |
| 网络角色 | 客户端 | 服务器 |
| 目标平台 | 全平台 | Windows/Linux |
| 入口函数 | `Start()` | `StartServer()` |

## 部署

### Kubernetes 部署

```yaml
# game-server-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: game-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: urhox-server
        image: urhox-server:latest
        command: ["./UrhoXServer"]
        args:
          - "-game_url=$(GAME_URL)"      # 由编排服务注入
          - "-config=/etc/urhox/server.json"
        env:
          - name: GAME_URL
            valueFrom:
              configMapKeyRef:
                name: game-config
                key: game_url
        ports:
          - containerPort: 7777
            protocol: UDP
        volumeMounts:
          - name: config
            mountPath: /etc/urhox
      volumes:
        - name: config
          configMap:
            name: server-config
```

### Docker Compose 部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  game-server:
    image: urhox-server:latest
    command:
      - "-game_url=${GAME_URL}"        # 从环境变量传入
      - "-config=/etc/urhox/server.json"
    ports:
      - "7777:7777/udp"
    volumes:
      - ./server-config.json:/etc/urhox/server.json:ro
    environment:
      - GAME_URL=https://games.example.com/my-game
```

启动不同游戏：

```bash
# 启动游戏 A
GAME_URL=https://games.example.com/game-a docker-compose up -d

# 启动游戏 B
GAME_URL=https://games.example.com/game-b docker-compose up -d
```

### Linux 系统服务（模板服务）

使用 systemd 模板服务，可以用同一个服务文件启动不同游戏：

```ini
# /etc/systemd/system/urhox-server@.service
[Unit]
Description=UrhoX Game Server (%i)
After=network.target

[Service]
Type=simple
User=gameserver
WorkingDirectory=/opt/urhox-server
# %i 是实例名，即 game_url
ExecStart=/opt/urhox-server/UrhoXServer -game_url=%i -config=/etc/urhox/server.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动不同游戏：

```bash
# 启动游戏 A
sudo systemctl start urhox-server@https://games.example.com/game-a

# 启动游戏 B  
sudo systemctl start urhox-server@https://games.example.com/game-b

# 查看状态
sudo systemctl status urhox-server@https://games.example.com/game-a
```

### Docker 镜像

```dockerfile
FROM ubuntu:22.04

# 安装依赖
RUN apt-get update && apt-get install -y \
    libssl3 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 复制服务器文件
COPY UrhoXServer /opt/server/
COPY Data /opt/server/Data/
COPY CoreData /opt/server/CoreData/
COPY server-config.json /etc/urhox/server.json

WORKDIR /opt/server

# 暴露端口
EXPOSE 7777/udp

# 入口点 - game_url 必须由编排服务传入
ENTRYPOINT ["./UrhoXServer", "-config=/etc/urhox/server.json"]
# 默认参数（可被覆盖）
CMD ["-game_url="]
```

构建并运行：

```bash
# 构建镜像
docker build -t urhox-server .

# 运行不同游戏（game_url 由 docker run 传入）
docker run -d -p 7777:7777/udp urhox-server \
    -game_url=https://games.example.com/game-a

docker run -d -p 7778:7777/udp urhox-server \
    -game_url=https://games.example.com/game-b
```

## 日志

服务器日志输出到：
- 控制台（stdout）
- 文件：`logs/server/UrhoXServer.log`

日志格式：

```
[2025-01-15 10:30:00] [INFO] ========================================
[2025-01-15 10:30:00] [INFO]   UrhoX Server Starting...
[2025-01-15 10:30:00] [INFO]   Game URL: https://games.example.com/my-game
[2025-01-15 10:30:00] [INFO]   Port: 7777
[2025-01-15 10:30:00] [INFO] ========================================
[2025-01-15 10:30:00] [INFO] [ServerBootstrap]   0% - Checking version...
[2025-01-15 10:30:01] [INFO] [ServerBootstrap]  20% - Loading manifest...
[2025-01-15 10:30:02] [INFO] [ServerBootstrap]  50% - Downloading package...
[2025-01-15 10:30:10] [INFO] [ServerBootstrap] 100% - Ready
[2025-01-15 10:30:10] [INFO] [UrhoXServer] Network server started on port 7777
[2025-01-15 10:30:10] [INFO] [UrhoXServer] Called StartServer()
```

## 测试

### 编译测试

在 CMake 配置时启用测试选项：

```bash
cmake -DURHO3D_HEADLESS=ON -DURHO3D_TESTING=ON ..
cmake --build . --target ServerTests
```

### 运行测试

```bash
# 方式 1: 直接运行
./bin/ServerTests

# 方式 2: 使用 CTest
ctest -R ServerTests -V

# 方式 3: 使用测试脚本 (Linux)
cd Tests/Server
./run_tests.sh ../../build

# 方式 3: 使用测试脚本 (Windows)
cd Tests\Server
run_tests.bat ..\..\build
```

### 测试内容

| 测试文件 | 说明 |
|---------|------|
| `CommandLineParserTests.cpp` | 命令行参数解析测试 |
| `ServerBootstrapTests.cpp` | ServerBootstrapManager 单元测试 |
| `MockBootstrapTests.cpp` | Bootstrap Pipeline 模拟测试 |

### 集成测试

使用 Lua 脚本进行集成测试：

```bash
# 需要提供测试用的 game_url
./UrhoXServer -game_url=<test_game_url> -port=7777
```

测试脚本位置：`Data/LuaScripts/Tests/ServerIntegrationTest.lua`

测试内容：
- ✅ `StartServer()` 函数被正确调用
- ✅ 无头模式验证（无 Graphics 子系统）
- ✅ 网络子系统可用
- ✅ 资源系统可用

### CI 集成

GitHub Actions 示例：

```yaml
name: Server Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      
      - name: Build with Headless Server Support
        run: |
          mkdir build && cd build
          cmake -DURHO3D_HEADLESS=ON -DURHO3D_TESTING=ON ..
          cmake --build . --target ServerTests
      
      - name: Run Tests
        run: |
          cd build
          ctest -R ServerTests -V --output-on-failure
```

## 故障排除

### 常见问题

**Q: 服务器启动失败，提示 "Network subsystem not available"**

A: 确保编译时启用了 `URHO3D_NETWORK=ON`

**Q: Bootstrap 下载失败**

A: 检查网络连接和 `game_url` 是否正确，服务器会自动重试

**Q: 脚本执行失败**

A: 确保游戏脚本中有 `StartServer()` 或 `Start()` 函数

## 更新日志

### v1.0.0 (2025-01-15)
- 初始版本
- 支持无头模式运行
- 支持 `-game_url` 动态加载游戏
- 支持 JSON 配置文件
- 集成 ServerBootstrapManager（无 UI 依赖）

