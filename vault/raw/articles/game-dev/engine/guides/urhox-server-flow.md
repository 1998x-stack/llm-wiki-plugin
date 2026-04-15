---
summary: "UrhoXServer startup, game loading, and main loop flow diagrams"
last_updated: "2026-04-02"
---

# UrhoXServer 流程图

## 1. 服务器启动流程

```
┌─────────────────────────────────────────────────────────────┐
│                        Setup()                              │
│  ParseCommandLine() → 解析 -game_url / -port / -config 等  │
│  验证必需参数（game_url 或 script + port）                   │
│  配置引擎参数（无头模式、无音频、资源路径、日志）              │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                        Start()                              │
│                                                             │
│  1. SetRuntimeMode(SERVER)                                  │
│  2. 设置帧率（默认 60fps）                                   │
│  3. LoadServerConfig()                                      │
│     ├─ session_id, redis_uri, dev_mode                      │
│     └─ players[] → playerAuthInfos_ (userId → AuthInfo)     │
│  4. ParseModeArgs()                                         │
│     └─ 提取 project_version, tapmaker_env, middle_game_key  │
│                                                             │
│  ┌─ [URHO3D_REDIS] ────────────────────────────────────┐    │
│  │  5. InitRedisClient() → 连接 Redis                  │    │
│  │  6. StartOrchestratorChannel()                       │    │
│  │     └─ 订阅 orch_to_urhox:{session_id}              │    │
│  │  7. StartScoreArchiveChannel()                       │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                             │
│  8. SubscribeToEvent(E_UPDATE)                              │
│  9. StartNetworkServer()                                    │
│     ├─ 绑定 KCP 端口                                       │
│     ├─ 绑定 WebSocket 端口（可选）                           │
│     └─ 订阅网络事件 + 远程事件                               │
│ 10. SetupScriptSystem() → 初始化 Lua                        │
│                                                             │
│  ┌─ [-script 本地模式] ──┐  ┌─ [-game_url 生产模式] ──┐     │
│  │  PrepareDevDebug()    │  │  StartBootstrap()       │     │
│  │  LoadGameSettings()   │  │    ↓ (异步下载)         │     │
│  │  RunGameScript()      │  │  OnBootstrapComplete()  │     │
│  │  serverReady_ = true  │  │  LoadGameSettings()     │     │
│  │  BroadcastServerReady │  │  RunGameScript()        │     │
│  └───────────────────────┘  │  serverReady_ = true    │     │
│                             │  BroadcastServerReady    │     │
│                             └─────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           ▼
                   HandleUpdate() 主循环
```

## 2. 玩家加入流程

### 2.1 playerAuthInfos_ 数据来源

```
┌──────────────────────────────────┐
│     playerAuthInfos_ 填充方式    │
├──────────────────────────────────┤
│                                  │
│  方式 A: 启动时从 config.json    │
│  LoadServerConfig()              │
│    └─ players[] 数组             │
│       └─ { user_id, auth_key,    │
│            user_name, nick_name }│
│                                  │
│  方式 B: 运行时 Orchestrator     │
│  Redis orch_to_urhox:{sid}       │
│    └─ { type: "add_user",        │
│         user_id, auth_key }      │
│    └─ DrainOrchestratorAddUsers()│
│       (每帧从队列取出加入 map)   │
│                                  │
└──────────────────────────────────┘
```

### 2.2 中途局 can_register_user 流程

```
  Orchestrator                    UrhoXServer
      │                               │
      │  can_register_user             │
      │  { user_id, request_id,        │
      │    reply_key }                 │
      ├──────────────────────────────→ │
      │                               │ EvaluateAllowMidGameRegister()
      │                               │   ├─ 已在局内? → "already_in_game"
      │                               │   ├─ 房间满?   → "room_full"
      │                               │   └─ 通过      → allowed=true
      │      LPUSH reply_key           │
      │  { request_id, allowed,        │
      │    reason }                    │
      │ ←─────────────────────────────┤
      │                               │
      │  add_user (if allowed)         │
      │  { user_id, auth_key }         │
      ├──────────────────────────────→ │
      │                               │ pendingAddUsers_ 队列
      │                               │   ↓ (下一帧 DrainOrchestratorAddUsers)
      │                               │ playerAuthInfos_[userId] = info
      │                               │
```

### 2.3 客户端连接认证流程

```
  Client                          UrhoXServer
    │                                 │
    │  Connect(port, identity)        │
    │  identity = { user_id,          │
    │               auth_key }        │
    ├────────────────────────────────→│
    │                                 │ HandleClientConnected()
    │                                 │   hadPlayersConnected_ = true
    │                                 │   取消空闲计时器
    │                                 │   如果 serverReady_ → SendServerReady()
    │                                 │
    │                                 │ HandleClientIdentity()
    │                                 │   │
    │                                 │   ├─ playerAuthInfos_ 为空?
    │                                 │   │   ├─ devMode_ → 自动分配 userId, 允许
    │                                 │   │   └─ 生产模式 → 拒绝 ❌
    │                                 │   │
    │                                 │   ├─ ValidateAuthKey()
    │                                 │   │   ├─ userId 不存在 → 拒绝 ❌
    │                                 │   │   ├─ authKey 不匹配 → 拒绝 ❌
    │                                 │   │   │  (tag=test 时跳过 key 比较)
    │                                 │   │   └─ 验证通过 ✓
    │                                 │   │
    │                                 │   ├─ 检查重复连接（同 userId）
    │                                 │   │   └─ 向旧连接发送 KickedByServer
    │                                 │   │      { Reason: "DuplicateLogin" }
    │                                 │   │
    │                                 │   ├─ 注入 nick_name 到 identity
    │  IdentityUpdated               │   ├─ 发送 IdentityUpdated 事件
    │ ←───────────────────────────────┤   │
    │                                 │   ├─ 清除断线重连超时记录
    │                                 │   └─ ALLOW = true ✓
    │                                 │
```

## 3. 玩家退出流程

### 3.1 主动退出 (PlayerLeaving)

```
  Client                          UrhoXServer
    │                                 │
    │  SendRemoteEvent                │
    │  ("PlayerLeaving",              │
    │   { Reason: "..." })            │
    ├────────────────────────────────→│
    │                                 │ HandlePlayerLeaving()
    │                                 │   └─ connection->Disconnect()
    │                                 │        ↓
    │                                 │ HandleClientDisconnected()
    │                                 │   └─ 记录断线重连超时
    │                                 │      disconnectedUserExpiry_[userId]
    │                                 │        = serverUptime_ + 60s
    │                                 │
```

### 3.2 异常断线 + 重连超时

```
  Client                          UrhoXServer
    │                                 │
    │  ── 网络断开 ──                 │
    │                                 │ HandleClientDisconnected()
    │                                 │   └─ disconnectedUserExpiry_[userId]
    │                                 │        = serverUptime_ + 60s
    │                                 │
    │                                 │ HandleUpdate() 每帧检查:
    │                                 │   if serverUptime_ >= expiry
    │                                 │     └─ 从 disconnectedUserExpiry_ 移除
    │                                 │
    │  60s 内重连 ──────────────────→ │ HandleClientIdentity()
    │                                 │   └─ 清除 disconnectedUserExpiry_
    │                                 │      允许连接 ✓
    │                                 │
```

### 3.3 Orchestrator 通知放弃重连 (user_give_up_reconnect)

```
  Lobby           Orchestrator         UrhoXServer
    │                  │                     │
    │ 玩家放弃重连     │                     │
    ├─────────────────→│                     │
    │                  │  Redis PUBLISH       │
    │                  │  orch_to_urhox:{sid} │
    │                  │  { type:             │
    │                  │   "user_give_up_     │
    │                  │    reconnect",       │
    │                  │   user_id }          │
    │                  ├────────────────────→ │
    │                  │                     │ OrchestratorChannel::OnMessage()
    │                  │                     │   └─ pendingGiveUpUserIds_ 队列
    │                  │                     │
    │                  │                     │ HandleUpdate() (下一帧):
    │                  │                     │   DrainGiveUpUserIds()
    │                  │                     │     │
    │                  │                     │     ├─ 清除 disconnectedUserExpiry_
    │                  │                     │     │
    │                  │                     │     ├─ SendKickAndScheduleDisconnect()
    │                  │                     │     │   ├─ 查找该 userId 的在线连接
    │                  │                     │     │   ├─ 发送 KickedByServer
    │                  │                     │     │   │  { Reason: "GiveUpReconnect" }
    │                  │                     │     │   └─ 加入 pendingKicks_ 队列
    │                  │                     │     │      (2s 后断开)
    │                  │                     │     │
    │                  │                     │     └─ playerAuthInfos_.Erase(userId)
    │                  │                     │        日志: remaining=N
    │                  │                     │
    │                  │                     │ ProcessPendingKicks() (2s 后):
    │                  │                     │   └─ connection->Disconnect()
    │                  │                     │
```

### 3.4 重复登录踢人

```
  Client A (旧)    Client B (新)      UrhoXServer
    │                  │                   │
    │  已连接 userId=X │                   │
    │                  │ Connect(userId=X) │
    │                  ├─────────────────→ │
    │                  │                   │ HandleClientIdentity()
    │                  │                   │   ValidateAuthKey() ✓
    │                  │                   │   检测到 Client A 同 userId
    │  KickedByServer  │                   │
    │  { Reason:       │                   │
    │   "DuplicateLogin" }                 │
    │ ←────────────────────────────────────┤
    │                  │                   │   允许 Client B 连接 ✓
    │                  │                   │
```

## 4. 服务器退出流程

```
┌──────────────────────────────────────────────────────────────┐
│                    服务器退出触发条件                          │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 条件 1: Auth 列表清空 (5s)                          │     │
│  │                                                     │     │
│  │ 触发: playerAuthInfos_ 变为空                       │     │
│  │ 前提: !devMode_ && serverReady_                     │     │
│  │       && middleGameKey_.Empty() (非中途局)           │     │
│  │ 延迟: AUTH_EMPTY_SHUTDOWN_DELAY = 5s                │     │
│  │ 取消: add_user 补充新用户时自动取消                  │     │
│  │ 日志: "Auth list empty ... shutting down in 5s"     │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 条件 2: 游戏结束 (5s)                               │     │
│  │                                                     │     │
│  │ 触发: Lua 脚本 SendEvent("ServerGameEnded")         │     │
│  │ 处理: HandleGameEnded()                             │     │
│  │       → 广播 ServerShuttingDown 给所有客户端         │     │
│  │       → gameEndedPending_ = true                    │     │
│  │ 延迟: GAME_ENDED_SHUTDOWN_DELAY = 5s                │     │
│  │ 日志: "Game ended countdown finished, shutting down" │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 条件 3: 空闲超时 (默认 300s)                        │     │
│  │                                                     │     │
│  │ 触发: 曾有玩家连接 → 所有玩家断开 → 持续无人        │     │
│  │ 状态机: EvaluateIdleTimeout()                       │     │
│  │   Continue → EnterIdle → ExitIdleTimeout            │     │
│  │                ↑                                    │     │
│  │           CancelIdle (有人重连)                      │     │
│  │ 延迟: idleTimeoutSeconds_ (默认 300s)               │     │
│  │ 日志: "Idle timeout reached, shutting down"         │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 条件 4: 初始等待超时 (默认 600s)                    │     │
│  │                                                     │     │
│  │ 触发: 服务器启动后从未有玩家连接                     │     │
│  │ 延迟: initialWaitTimeout_ (默认 600s)               │     │
│  │ 日志: "No players connected within Ns, shutting down"│     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                       engine_->Exit()                        │
│                           ↓                                  │
│                        Stop()                                │
│                                                              │
│  1. serverScore_.Reset()           ── 停止云变量系统          │
│  2. StopScoreArchiveChannel()      ── 停止积分通道            │
│  3. StopOrchestratorChannel()      ── 停止编排通道            │
│  4. Lua Stop() 回调                ── 通知脚本清理            │
│  5. ShutdownRedisClient()          ── 关闭 Redis 连接         │
│  6. network->StopServer()          ── 停止网络服务器          │
│  7. 日志: "Shutdown complete"                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 5. HandleUpdate 主循环总览

```
HandleUpdate() — 每帧执行
│
├─ serverUptime_ += timeStep
│
├─ [REDIS] DrainOrchestratorAddUsers()
│     └─ add_user → playerAuthInfos_
│
├─ [REDIS] DrainGiveUpUserIds()
│     └─ user_give_up_reconnect
│        ├─ SendKickAndScheduleDisconnect()
│        └─ playerAuthInfos_.Erase()
│
├─ 断线重连超时检查
│     └─ serverUptime_ >= expiry → 从 disconnectedUserExpiry_ 移除
│
├─ ProcessPendingKicks()
│     └─ 2s 到期 → connection->Disconnect()
│
├─ Auth 列表清空检查 (非 devMode, 非中途局)
│     └─ 空 → 5s 倒计时 → Exit
│     └─ 非空 → 取消倒计时
│
├─ ServerScore::FlushPendingCallbacks()
│
├─ 游戏结束倒计时
│     └─ gameEndedPending_ → 5s → Exit
│
├─ CheckIdleTimeout()
│     ├─ EnterIdle / CancelIdle
│     ├─ ExitIdleTimeout (300s)
│     └─ ExitInitialTimeout (600s)
│
└─ 进度广播 (serverReady_ 之前)
      └─ BroadcastServerProgress() (每 1s)
```
