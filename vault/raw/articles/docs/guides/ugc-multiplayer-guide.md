---
summary: "UGC multiplayer game development guide for creators, covering server-managed networking without self-hosting"
last_updated: "2026-01-18"
---

# UGC 联网游戏开发指南

> **面向**: UGC 创作者  
> **目标**: 教你如何创建联网多人游戏，无需自己部署服务器  
> **难度**: ⭐⭐⭐ 中级

---

## 一、快速开始

### 1.1 最简单的联网游戏

创建一个 2 人对战游戏只需 3 步：

#### 步骤 1: 添加 settings.json

在项目的 `assets/` 目录下创建 `settings.json`:

```json
{
  "max_players": 2
}
```

#### 步骤 2: 编写服务器脚本

创建 `main.lua`:

```lua
-- 服务器入口函数
function StartServer()
    print("Server started! Max players: " .. SERVER_MAX_PLAYERS)
    
    -- 创建场景
    scene_ = Scene()
    scene_:CreateComponent("Octree")
    
    -- 订阅玩家连接事件
    SubscribeToEvent("ClientConnected", "OnPlayerJoin")
    SubscribeToEvent("ClientDisconnected", "OnPlayerLeave")
end

-- 玩家加入
function OnPlayerJoin(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    print("Player joined: " .. connection:GetAddress())
    
    -- 创建玩家实体
    local playerNode = scene_:CreateChild("Player")
    playerNode:SetPosition(Vector3(math.random(-10, 10), 0, math.random(-10, 10)))
end

-- 玩家离开
function OnPlayerLeave(eventType, eventData)
    print("Player left")
end
```

#### 步骤 3: 发布

点击"发布"按钮，系统会自动：
- ✅ 验证你的脚本
- ✅ 上传到 CDN
- ✅ 部署服务器

玩家匹配后会自动连接到官方托管的游戏服务器！

---

## 二、配置详解

### 2.1 settings.json 配置

#### 简化格式（推荐新手）

```json
{
  "max_players": 4
}
```

#### 完整格式（高级配置）

```json
{
  "name": "我的多人游戏",
  "entry": "main.lua",
  "version": "1.0.0",
  
  "multiplayer": {
    "enabled": true,
    "max_players": 8,
    "mode": "server_authoritative",
    "server_tick_rate": 20
  },
  
  "preload": [
    "Scripts/",
    "Data/"
  ]
}
```

**配置说明**:

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `multiplayer.enabled` | bool | false | 是否启用多人游戏 |
| `multiplayer.max_players` | int | 4 | 最大玩家数（1-100） |
| `multiplayer.mode` | string | "server_authoritative" | 模式：服务器权威/P2P |
| `multiplayer.server_tick_rate` | int | 20 | 服务器更新频率（Hz） |

> **注意**：网络协议由平台统一控制（KCP + WebSocket），游戏开发者无需配置。

---

## 三、服务器端脚本

### 3.1 入口函数

服务器脚本有两种入口函数：

#### 方式 1: 专用入口（推荐）

```lua
function StartServer()
    -- 只在服务器端运行
    print("This is server!")
    InitServerGame()
end

function Start()
    -- 只在客户端运行
    print("This is client!")
    InitClientGame()
end
```

#### 方式 2: 通用入口

```lua
function Start()
    if engine:IsHeadless() then
        -- 服务器模式
        print("Running as server")
        InitServerGame()
    else
        -- 客户端模式
        print("Running as client")
        InitClientGame()
    end
end
```

### 3.2 服务器全局变量

服务器启动时会自动设置以下全局变量：

| 变量 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `SERVER_MAX_PLAYERS` | number | 最大玩家数 | 4 |
| `SERVER_MULTIPLAYER` | boolean | 是否多人模式 | true |
| `SERVER_TICK_RATE` | number | 更新频率 | 20 |
| `SERVER_MODE` | string | 多人模式 | "server_authoritative" |
| `SERVER_SESSION_ID` | number | 会话 ID | 7596617... |
| `SERVER_PORT` | number | KCP 端口 | 7000 |
| `SERVER_WS_PORT` | number | WebSocket 端口 | 8000 |
| `SERVER_NAME` | string | 服务器名称 | "session_12345" |
| `SERVER_REGISTERED_PLAYERS` | number | 已注册玩家数 | 4 |

**使用示例**:

```lua
function StartServer()
    print("Starting session: " .. SERVER_SESSION_ID)
    print("Waiting for " .. SERVER_MAX_PLAYERS .. " players...")
    
    -- 根据玩家数初始化游戏
    if SERVER_MAX_PLAYERS <= 4 then
        InitSmallMap()
    else
        InitLargeMap()
    end
end
```

---

## 四、网络同步

### 4.1 玩家连接管理

```lua
-- 玩家列表
local players = {}

function OnPlayerJoin(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    
    -- 创建玩家
    local playerId = #players + 1
    local player = {
        id = playerId,
        connection = connection,
        node = scene_:CreateChild("Player" .. playerId),
    }
    
    players[connection] = player
    
    -- 广播新玩家加入
    BroadcastPlayerJoined(player)
    
    -- 同步当前游戏状态给新玩家
    SyncGameStateToPlayer(connection)
end

function OnPlayerLeave(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    local player = players[connection]
    
    if player then
        -- 销毁玩家实体（使用 Dispose 确保网络同步）
        player.node:Dispose()
        players[connection] = nil
        
        -- 广播玩家离开
        BroadcastPlayerLeft(player)
    end
end
```

### 4.2 发送远程事件

```lua
-- 发送给单个玩家
function SendToPlayer(connection, eventName, data)
    local eventData = VariantMap()
    for k, v in pairs(data) do
        eventData[k] = Variant(v)
    end
    connection:SendRemoteEvent(eventName, true, eventData)
end

-- 广播给所有玩家
function BroadcastToAll(eventName, data)
    local eventData = VariantMap()
    for k, v in pairs(data) do
        eventData[k] = Variant(v)
    end
    network:BroadcastRemoteEvent(eventName, true, eventData)
end

-- 示例：广播游戏状态
function BroadcastGameState()
    BroadcastToAll("GameStateUpdate", {
        time = gameTime,
        score = gameScore,
    })
end
```

### 4.3 接收客户端事件

```lua
function StartServer()
    -- 注册远程事件
    network:RegisterRemoteEvent("PlayerMove")
    network:RegisterRemoteEvent("PlayerAttack")
    
    -- 订阅事件
    SubscribeToEvent("PlayerMove", "OnPlayerMove")
    SubscribeToEvent("PlayerAttack", "OnPlayerAttack")
end

function OnPlayerMove(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    local x = eventData["X"]:GetFloat()
    local z = eventData["Z"]:GetFloat()
    
    -- 更新玩家位置（服务器权威）
    local player = players[connection]
    if player then
        player.node:SetPosition(Vector3(x, 0, z))
        
        -- 广播给其他玩家
        BroadcastToAll("PlayerMoved", {
            playerId = player.id,
            x = x,
            z = z,
        })
    end
end
```

### 4.4 客户端连接（重要）

客户端使用 `lobby:ConnectToGameServer()` API 安全连接到游戏服务器。这个 API 会自动处理服务器地址、协议选择和身份认证。

#### 连接流程

```lua
-- 1. 订阅必要事件
function Start()
    scene_ = Scene()
    scene_:CreateComponent("Octree")
    
    -- 监听游戏开始通知
    SubscribeToEvent("NotifyGameStartEvent", "OnGameStart")
    
    -- 监听连接状态
    SubscribeToEvent("ServerConnected", "OnConnected")
    SubscribeToEvent("ServerDisconnected", "OnDisconnected")
    
    -- 注册远程事件
    network:RegisterRemoteEvent("GameState")
    SubscribeToEvent("GameState", "OnGameState")
end

-- 2. 收到游戏开始通知后连接
function OnGameStart(eventType, eventData)
    if eventData["Success"]:GetBool() then
        -- 使用安全连接 API（不暴露服务器地址）
        lobby:ConnectToGameServer(scene_)
    else
        local errorCode = eventData["ErrorCode"]:GetInt()
        print("游戏开始失败: " .. errorCode)
    end
end

-- 3. 连接成功后的处理
function OnConnected(eventType, eventData)
    print("已连接到游戏服务器!")
    -- 现在可以发送/接收远程事件
end
```

#### 发送事件到服务器

```lua
-- 使用引擎原生 API
local eventData = VariantMap()
eventData["X"] = Variant(10.5)
eventData["Action"] = Variant("move")

local connection = network:GetServerConnection()
if connection then
    connection:SendRemoteEvent("PlayerMove", true, eventData)
end
```

#### 接收服务器事件

```lua
-- 注册 + 订阅
network:RegisterRemoteEvent("GameState")
SubscribeToEvent("GameState", "OnGameState")

function OnGameState(eventType, eventData)
    local score = eventData["Score"]:GetInt()
    local time = eventData["Time"]:GetFloat()
    -- 更新 UI...
end
```

#### 辅助工具（可选）

使用 `NetworkUtils` 模块简化代码：

```lua
local NetworkUtils = require("urhox-libs.Network.NetworkUtils")

-- 简化事件注册
NetworkUtils.OnRemoteEvent("GameState", "OnGameState")

-- 简化发送
NetworkUtils.SendToServer("PlayerMove", {
    x = 10.5,
    y = 0,
    action = "move"
})
```

#### API 参考

| 函数 | 说明 |
|------|------|
| `lobby:ConnectToGameServer(scene)` | 连接到游戏服务器（安全封装） |
| `lobby:HasGameServerInfo()` | 检查是否有有效的服务器信息 |
| `lobby:GetMyUserId()` | 获取当前用户 ID |
| `network:GetServerConnection()` | 获取服务器连接对象 |
| `connection:SendRemoteEvent(name, reliable, data)` | 发送远程事件 |
| `network:RegisterRemoteEvent(name)` | 注册远程事件 |
| `network:Disconnect()` | 断开连接 |

---

## 五、完整示例：2v2 对战游戏

### 5.1 服务器脚本

```lua
-- ============================================
-- 2v2 对战游戏服务器脚本
-- ============================================

local players = {}
local teams = { {}, {} }  -- 两个队伍
local gameStarted = false

function StartServer()
    print("=== 2v2 Battle Server ===")
    print("Max players: " .. SERVER_MAX_PLAYERS)
    
    -- 创建场景
    scene_ = Scene()
    scene_:CreateComponent("Octree")
    scene_:CreateComponent("PhysicsWorld")
    
    -- 订阅事件
    SubscribeToEvent("ClientConnected", "OnPlayerJoin")
    SubscribeToEvent("ClientDisconnected", "OnPlayerLeave")
    SubscribeToEvent("Update", "OnUpdate")
    
    -- 注册远程事件
    network:RegisterRemoteEvent("PlayerReady")
    network:RegisterRemoteEvent("PlayerAction")
    SubscribeToEvent("PlayerReady", "OnPlayerReady")
    SubscribeToEvent("PlayerAction", "OnPlayerAction")
    
    print("Server ready, waiting for players...")
end

function OnPlayerJoin(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    
    -- 检查是否已满
    local playerCount = GetTotalPlayers()
    if playerCount >= SERVER_MAX_PLAYERS then
        print("Server full, rejecting player")
        connection:Disconnect()
        return
    end
    
    -- 创建玩家
    local playerId = playerCount + 1
    local teamId = ((playerId - 1) % 2) + 1  -- 交替分配队伍
    
    local player = {
        id = playerId,
        teamId = teamId,
        connection = connection,
        ready = false,
        node = scene_:CreateChild("Player" .. playerId),
    }
    
    -- 设置初始位置
    local spawnPos = GetTeamSpawnPoint(teamId, #teams[teamId] + 1)
    player.node:SetPosition(spawnPos)
    
    players[connection] = player
    table.insert(teams[teamId], player)
    
    print("Player " .. playerId .. " joined Team " .. teamId)
    
    -- 发送欢迎消息
    SendToPlayer(connection, "Welcome", {
        playerId = playerId,
        teamId = teamId,
        maxPlayers = SERVER_MAX_PLAYERS,
    })
    
    -- 广播新玩家加入
    BroadcastToAll("PlayerJoined", {
        playerId = playerId,
        teamId = teamId,
    })
end

function OnPlayerLeave(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    local player = players[connection]
    
    if player then
        print("Player " .. player.id .. " left")
        
        -- 从队伍移除
        for i, p in ipairs(teams[player.teamId]) do
            if p.id == player.id then
                table.remove(teams[player.teamId], i)
                break
            end
        end
        
        -- 销毁实体
        player.node:Remove()
        players[connection] = nil
        
        -- 广播
        BroadcastToAll("PlayerLeft", { playerId = player.id })
        
        -- 检查是否需要结束游戏
        if GetTotalPlayers() == 0 then
            print("All players left, shutting down...")
            engine:Exit()
        end
    end
end

function OnPlayerReady(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    local player = players[connection]
    
    if player then
        player.ready = true
        print("Player " .. player.id .. " is ready")
        
        -- 检查是否所有人都准备好
        if AllPlayersReady() then
            StartGame()
        end
    end
end

function AllPlayersReady()
    local totalPlayers = GetTotalPlayers()
    if totalPlayers < SERVER_MAX_PLAYERS then
        return false
    end
    
    for _, player in pairs(players) do
        if not player.ready then
            return false
        end
    end
    
    return true
end

function StartGame()
    gameStarted = true
    print("Game starting!")
    
    BroadcastToAll("GameStart", {
        timestamp = os.time(),
    })
end

function OnUpdate(eventType, eventData)
    if not gameStarted then
        return
    end
    
    local dt = eventData["TimeStep"]:GetFloat()
    
    -- 游戏逻辑更新
    UpdateGame(dt)
end

function UpdateGame(dt)
    -- 在这里实现游戏逻辑
    -- 例如：检测碰撞、更新得分等
end

-- 辅助函数
function GetTeamSpawnPoint(teamId, slotId)
    local offset = (slotId - 1) * 2
    if teamId == 1 then
        return Vector3(-10 + offset, 0, 0)
    else
        return Vector3(10 - offset, 0, 0)
    end
end

function SendToPlayer(connection, eventName, data)
    local eventData = VariantMap()
    for k, v in pairs(data) do
        eventData[k] = Variant(v)
    end
    connection:SendRemoteEvent(eventName, true, eventData)
end

function BroadcastToAll(eventName, data)
    local eventData = VariantMap()
    for k, v in pairs(data) do
        eventData[k] = Variant(v)
    end
    network:BroadcastRemoteEvent(eventName, true, eventData)
end

function GetTotalPlayers()
    local count = 0
    for _ in pairs(players) do
        count = count + 1
    end
    return count
end
```

### 5.2 客户端脚本

```lua
function Start()
    print("Client starting...")
    
    -- 监听游戏开始事件（从 Lobby 发来）
    SubscribeToEvent("NotifyGameStartEvent", "OnGameStart")
end

function OnGameStart(eventType, eventData)
    local success = eventData["Success"]:GetBool()
    if not success then
        print("Game start failed")
        return
    end
    
    -- 获取服务器信息
    local serverIP = eventData["ServerIP"]:GetString()
    local serverPort = eventData["ServerPort"]:GetInt()
    local authKey = eventData["AuthKey"]:GetString()
    
    print("Connecting to server: " .. serverIP .. ":" .. serverPort)
    
    -- 构造身份信息
    local identity = VariantMap()
    identity["user_id"] = GetLobby():GetUserId()
    identity["auth_key"] = authKey
    
    -- 连接游戏服务器
    local network = GetNetwork()
    scene_ = Scene()
    network:ConnectWithTransport(serverIP, serverPort, scene_, TRANSPORT_KCP, identity)
    
    -- 订阅连接事件
    SubscribeToEvent("ServerConnected", "OnServerConnected")
    SubscribeToEvent("ServerDisconnected", "OnServerDisconnected")
    
    -- 注册游戏事件
    network:RegisterRemoteEvent("Welcome")
    network:RegisterRemoteEvent("PlayerJoined")
    network:RegisterRemoteEvent("GameStart")
    
    SubscribeToEvent("Welcome", "OnWelcome")
    SubscribeToEvent("PlayerJoined", "OnPlayerJoined")
    SubscribeToEvent("GameStart", "OnGameStart")
end

function OnServerConnected()
    print("Connected to game server!")
    
    -- 发送准备消息
    local eventData = VariantMap()
    network:GetServerConnection():SendRemoteEvent("PlayerReady", true, eventData)
end

function OnServerDisconnected()
    print("Disconnected from server")
end

function OnWelcome(eventType, eventData)
    local playerId = eventData["playerId"]:GetInt()
    local teamId = eventData["teamId"]:GetInt()
    
    print("I am Player " .. playerId .. " in Team " .. teamId)
end
```

---

## 六、服务器限制

### 6.1 不支持的 API

服务器端**不支持**以下 API（使用会导致发布失败）：

| 分类 | 不支持的 API | 原因 |
|------|--------------|------|
| **UI** | `GetUI()`, `UIElement`, `Button`, `Text` 等 | 服务器无界面 |
| **输入** | `GetInput()`, `GetKeyDown()`, `GetMouseButton()` 等 | 服务器无输入设备 |
| **音频** | `GetAudio()`, `PlaySound()`, `SoundSource` 等 | 服务器不需要音频 |
| **图形** | `GetGraphics()`, `Camera`, `Renderer` 等 | 服务器无图形渲染 |

### 6.2 API 兼容性检查

在发布前，系统会自动检查你的脚本：

```bash
# 检查结果示例
[ERROR] 发现 5 个错误:
  Line 10: 客户端专用 API "GetUI" 在服务器端不可用
  Line 15: 客户端专用 API "GetInput" 在服务器端不可用
```

**修复建议**:
- ✅ 使用 `engine:IsHeadless()` 区分服务器和客户端代码
- ✅ 将 UI 逻辑移到 `Start()` 函数（仅客户端）
- ✅ 将服务器逻辑放在 `StartServer()` 函数

### 6.3 代码分离示例

```lua
-- ❌ 错误：混合代码
function Start()
    CreateUI()          -- 服务器会报错
    StartGameLogic()
end

-- ✅ 正确：分离代码
function StartServer()
    -- 只有服务器逻辑
    StartGameLogic()
end

function Start()
    -- 只有客户端逻辑
    CreateUI()
    ConnectToServer()
end

-- 共享逻辑
function StartGameLogic()
    scene_ = Scene()
    InitGame()
end
```

---

## 七、调试技巧

### 7.1 本地测试

你可以在本地运行服务器测试：

```bash
# Windows
UrhoXServer_d.exe -game_url=https://tapcode-sce.spark.xd.com/src/你的项目ID/ -port=7000

# 查看日志
type logs\server\*.log
```

### 7.2 常见问题

#### Q: 如何知道有多少玩家连接？

```lua
function GetConnectedPlayerCount()
    local count = 0
    for _ in pairs(players) do
        count = count + 1
    end
    return count
end

-- 或使用全局变量
print("Registered players: " .. SERVER_REGISTERED_PLAYERS)
```

#### Q: 如何实现准备系统？

```lua
local readyPlayers = {}

function OnPlayerReady(eventType, eventData)
    local connection = eventData["Connection"]:GetPtr("Connection")
    readyPlayers[connection] = true
    
    -- 检查是否所有人都准备好
    local totalReady = 0
    for _ in pairs(readyPlayers) do
        totalReady = totalReady + 1
    end
    
    if totalReady == SERVER_MAX_PLAYERS then
        StartGame()
    end
end
```

#### Q: 如何结束游戏？

```lua
function OnGameOver(winnerTeamId)
    -- 广播游戏结束
    BroadcastToAll("GameOver", {
        winner = winnerTeamId,
    })
    
    -- 5 秒后关闭服务器
    DelayedExecute(5.0, function()
        engine:Exit()
    end)
end
```

---

## 八、最佳实践

### 8.1 性能优化

#### 1. 限制广播频率

```lua
local lastBroadcastTime = 0
local BROADCAST_INTERVAL = 0.05  -- 50ms = 20 Hz

function OnUpdate(eventType, eventData)
    local time = eventData["TimeStep"]:GetFloat()
    lastBroadcastTime = lastBroadcastTime + time
    
    if lastBroadcastTime >= BROADCAST_INTERVAL then
        BroadcastGameState()
        lastBroadcastTime = 0
    end
end
```

#### 2. 只同步变化

```lua
local lastState = {}

function BroadcastGameState()
    local currentState = GetGameState()
    
    -- 只广播变化的数据
    local changes = {}
    for k, v in pairs(currentState) do
        if lastState[k] ~= v then
            changes[k] = v
        end
    end
    
    if next(changes) then
        BroadcastToAll("StateUpdate", changes)
        lastState = currentState
    end
end
```

### 8.2 错误处理

```lua
function OnPlayerAction(eventType, eventData)
    -- 验证连接
    local connection = eventData["Connection"]:GetPtr("Connection")
    if not connection then
        return
    end
    
    -- 验证玩家存在
    local player = players[connection]
    if not player then
        print("Warning: Action from unknown player")
        return
    end
    
    -- 验证游戏状态
    if not gameStarted then
        print("Warning: Action before game start")
        return
    end
    
    -- 处理动作
    ProcessPlayerAction(player, eventData)
end
```

### 8.3 安全建议

#### 1. 不要使用系统命令

```lua
-- ❌ 危险！
os.execute("rm -rf /")
io.popen("cat /etc/passwd")
```

#### 2. 验证客户端数据

```lua
function OnPlayerMove(eventType, eventData)
    local x = eventData["X"]:GetFloat()
    local z = eventData["Z"]:GetFloat()
    
    -- 验证范围（防止作弊）
    if math.abs(x) > 100 or math.abs(z) > 100 then
        print("Invalid position from client")
        return
    end
    
    -- 应用移动
    UpdatePlayerPosition(x, z)
end
```

#### 3. 服务器权威验证

```lua
-- ❌ 错误：直接信任客户端
function OnClientScore(eventType, eventData)
    local score = eventData["Score"]:GetInt()
    UpdateScore(score)  -- 客户端可以作弊！
end

-- ✅ 正确：服务器验证
function OnPlayerKill(eventType, eventData)
    local killerConn = eventData["Connection"]:GetPtr("Connection")
    local targetId = eventData["TargetId"]:GetInt()
    
    -- 服务器验证击杀是否有效
    if ValidateKill(killerConn, targetId) then
        AddScore(killerConn, 100)  -- 服务器计算得分
    end
end
```

---

## 九、常见错误

### 错误 1: 使用了 UI API

```lua
-- ❌ 错误
function StartServer()
    local ui = GetUI()  -- 服务器没有 UI！
end

-- ✅ 正确
function StartServer()
    print("Server started")  -- 使用日志输出
end
```

### 错误 2: 没有处理玩家断线

```lua
-- ❌ 错误：玩家离开后游戏永远不结束
function OnPlayerLeave()
    -- 什么都不做
end

-- ✅ 正确：检查是否需要结束游戏
function OnPlayerLeave()
    if GetConnectedPlayerCount() == 0 then
        engine:Exit()  -- 所有人都走了，结束游戏
    end
end
```

### 错误 3: 忘记注册远程事件

```lua
-- ❌ 错误：直接订阅（不会触发）
function StartServer()
    SubscribeToEvent("PlayerMove", "OnPlayerMove")
end

-- ✅ 正确：先注册再订阅
function StartServer()
    network:RegisterRemoteEvent("PlayerMove")  -- 必须先注册
    SubscribeToEvent("PlayerMove", "OnPlayerMove")
end
```

---

## 十、进阶主题

### 10.1 帧同步 vs 状态同步

#### 状态同步（推荐）

- 服务器定期广播游戏状态
- 客户端根据状态渲染
- 适合大部分游戏

```lua
function BroadcastGameState()
    local state = {
        players = SerializePlayers(),
        time = gameTime,
        score = teamScores,
    }
    BroadcastToAll("StateUpdate", state)
end
```

#### 帧同步（高级）

- 服务器广播玩家输入
- 所有客户端模拟相同逻辑
- 适合 RTS、MOBA

### 10.2 延迟补偿

```lua
-- 服务器时间戳
local serverTime = 0

function OnUpdate(eventType, eventData)
    serverTime = serverTime + eventData["TimeStep"]:GetFloat()
end

-- 广播时附带时间戳
function BroadcastWithTimestamp(eventName, data)
    data.serverTime = serverTime
    BroadcastToAll(eventName, data)
end
```

---

## 十一、发布清单

发布前请确认：

- [ ] `settings.json` 已配置 `max_players`
- [ ] 服务器脚本有 `StartServer()` 或 `Start()` 函数
- [ ] 没有使用客户端专用 API（UI、Input、Audio、Graphics）
- [ ] 已通过本地测试
- [ ] 客户端脚本能正确连接服务器
- [ ] 处理了玩家连接/断开事件
- [ ] 所有玩家离开时正确关闭服务器

---

## 十二、参考资料

### 12.1 API 文档

- 网络 API: `network:BroadcastRemoteEvent()`, `connection:SendRemoteEvent()`
- Lobby API: `lobby:ConnectToGameServer()`, `lobby:GetMyUserId()`
- 场景 API: `Scene()`, `CreateChild()`, `CreateComponent()`
- 事件 API: `SubscribeToEvent()`, `SendEvent()`
- 辅助工具: `NetworkUtils.lua` (`urhox-libs.Network.NetworkUtils`)

### 12.2 示例项目

- **SimpleChat**: `LuaScripts/Multiplayer/SimpleChat.lua` - 最简单的联网聊天示例
- **BattleGame**: `LuaScripts/Multiplayer/BattleGame_Client.lua` + `BattleGame_Server.lua` - 完整对战游戏
- 简单对战: `examples/multiplayer/simple_battle/`
- 合作游戏: `examples/multiplayer/coop_game/`
- 大逃杀: `examples/multiplayer/battle_royale/`

### 12.3 工具

- API 兼容性检查器: `tools/validators/server_api_validator.py`
- 本地服务器测试: `UrhoXServer_d.exe`

---

*指南版本: 1.0*  
*创建日期: 2026-01-18*  
*适用版本: UrhoX 2.0+*

