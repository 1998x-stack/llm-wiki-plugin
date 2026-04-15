---
summary: "Transport abstraction layer supporting multiple network protocols (UDP, WebSocket, KCP) with backward-compatible Lua API"
related_paths:
  - engine/Source/Urho3D/Network/**
last_updated: "2024-12-23"
---

# Network Transport Abstraction Layer Design (v2)

## Overview

This document describes the Transport abstraction layer introduced to support multiple network protocols (UDP, WebSocket, KCP) in UrhoX engine.

## Key Design Principle: Backward Compatibility

**The existing Lua API remains completely unchanged.** The Transport layer is an internal implementation detail that enables protocol flexibility without requiring users to learn new APIs.

```lua
-- Lua code remains the same!
network:Connect("192.168.1.100", 8888, scene)  -- Works with UDP (default)
network:StartServer(12345)                      -- Works with UDP (default)

-- New optional methods for explicit protocol selection
network:ConnectWithTransport("192.168.1.100", 8080, scene, TRANSPORT_WEBSOCKET)
network:StartServerWithTransport(8080, TRANSPORT_WEBSOCKET)
```

## Architecture

```
                           User Code (Lua/C++)
                                   |
                    +--------------+--------------+
                    |                             |
             network:Connect()          network:ConnectWithTransport()
             network:StartServer()      network:StartServerWithTransport()
                    |                             |
                    +-------------+---------------+
                                  |
                                  v
                    +---------------------------+
                    |       Network Class       |
                    |   (Internal Transport)    |
                    +---------------------------+
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
        v                         v                         v
+---------------+       +------------------+       +---------------+
| SLikeNet      |       | WebSocket        |       | KCP           |
| Transport     |       | Transport        |       | Transport     |
| (UDP)         |       | (TCP/WS)         |       | (Reliable UDP)|
+---------------+       +------------------+       +---------------+
```

## Core Changes

### Connection Class

The Connection class now supports both SLikeNet (legacy) and Transport layer (new):

```cpp
class Connection
{
public:
    // New constructor for Transport layer
    Connection(Context* context, bool isClient, ITransport* transport, const NetworkAddress& address);

    // Legacy constructor (still supported)
    Connection(Context* context, bool isClient, const SLNet::AddressOrGUID& address, SLNet::RakPeerInterface* peer);

    // New methods
    ITransport* GetTransport() const;
    bool UsesTransport() const;

private:
    SharedPtr<ITransport> transport_;      // New: Transport layer
    NetworkAddress* transportAddress_;      // New: Transport address
    SLNet::AddressOrGUID* address_;        // Legacy: SLikeNet address
    SLNet::RakPeerInterface* peer_;        // Legacy: SLikeNet peer
};
```

### Network Class

The Network class internally manages Transport selection:

```cpp
class Network
{
public:
    // Existing API (unchanged)
    bool Connect(const String& address, unsigned short port, Scene* scene, const VariantMap& identity);
    bool StartServer(unsigned short port);

    // New API for explicit protocol selection
    bool ConnectWithTransport(const String& address, unsigned short port, Scene* scene,
                              TransportProtocol protocol, const VariantMap& identity);
    bool StartServerWithTransport(unsigned short port, TransportProtocol protocol);

    // Query current protocol
    TransportProtocol GetTransportProtocol() const;
    void SetPreferredTransport(TransportProtocol protocol);

private:
    // Auto-select protocol based on platform
    TransportProtocol SelectDefaultTransport() const;

    SharedPtr<ITransport> clientTransport_;
    SharedPtr<ITransport> serverTransport_;
    TransportProtocol transportProtocol_;
    TransportProtocol preferredTransport_;
};
```

## Protocol Auto-Selection

The engine automatically selects the best transport based on platform:

| Platform | Default Transport | Reason |
|----------|------------------|--------|
| WebAssembly | WebSocket | UDP not supported in browser |
| Native (Windows/Linux/macOS/iOS/Android) | UDP (SLikeNet) | Best performance, backward compatible |

### Environment Variable Override

On native platforms, you can override the default transport:

```bash
# Use WebSocket on native platforms
URHO3D_TRANSPORT=websocket ./MyGame

# Use KCP on native platforms
URHO3D_TRANSPORT=kcp ./MyGame
```

## Lua API

### Basic Usage (Unchanged)

```lua
-- Server
network:StartServer(12345)

-- Client
network:Connect("192.168.1.100", 12345, scene)

-- Events work as before
SubscribeToEvent("ServerConnected", "HandleServerConnected")
SubscribeToEvent("ClientConnected", "HandleClientConnected")
SubscribeToEvent("NetworkMessage", "HandleNetworkMessage")
```

### Explicit Protocol Selection (New)

```lua
-- Check protocol support
if TransportFactory.IsSupported(TRANSPORT_WEBSOCKET) then
    -- Start WebSocket server
    network:StartServerWithTransport(8080, TRANSPORT_WEBSOCKET)
end

-- Connect with specific protocol
network:ConnectWithTransport("game.server.com", 8080, scene, TRANSPORT_WEBSOCKET)

-- Query current protocol
local protocol = network:GetTransportProtocol()
```

## Transport Implementations

### SLikeNetTransport (UDP)

- **Protocol**: UDP with reliability built into SLikeNet
- **Use Case**: LAN games, P2P, low-latency multiplayer
- **Platform**: All native platforms
- **Features**:
  - Multiple reliability modes (UNRELIABLE, RELIABLE, RELIABLE_ORDERED)
  - NAT punchthrough support
  - Network simulation (latency, packet loss)

### WebSocketTransport

- **Protocol**: TCP-based WebSocket
- **Use Case**: Web games, cross-firewall communication
- **Platform**: All platforms (client), Native only (server)
- **Features**:
  - Web browser native support
  - SSL/TLS encryption (wss://)
  - Firewall-friendly (port 80/443)

**Limitations**:
- WebSocket server not supported on Web platform (browser limitation)
- All reliability modes map to RELIABLE_ORDERED (TCP semantics)

### KCPTransport

- **Protocol**: KCP over UDP (reliable ARQ)
- **Use Case**: Real-time games, mobile networks with packet loss
- **Platform**: Native platforms only
- **Features**:
  - 30-40% lower latency than TCP in lossy networks
  - Configurable parameters for latency vs bandwidth trade-off
  - Custom congestion control

## Platform Support Matrix

| Transport | Windows | Linux | macOS | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| UDP (SLikeNet) | Yes | Yes | Yes | Yes | Yes | No |
| WebSocket (client) | Yes | Yes | Yes | Yes | Yes | Yes |
| WebSocket (server) | Yes | Yes | Yes | Yes | Yes | No |
| KCP | Yes | Yes | Yes | Yes | Yes | No |

## Migration Guide

### For Existing Code

**No changes required.** Existing code using `network:Connect()` and `network:StartServer()` continues to work with UDP (SLikeNet) as before.

### For New WebSocket/KCP Support

```lua
-- Option 1: Use environment variable (no code changes)
-- Set URHO3D_TRANSPORT=websocket before running

-- Option 2: Use new explicit API
if TransportFactory.IsSupported(TRANSPORT_WEBSOCKET) then
    network:ConnectWithTransport(host, port, scene, TRANSPORT_WEBSOCKET)
end
```

## Files Modified

```
engine/Source/Urho3D/Network/
+-- Connection.h        # Added ITransport* constructor and members
+-- Connection.cpp      # Added Transport support in Send/Disconnect/etc.
+-- Network.h           # Added Transport-related methods and members
+-- Network.cpp         # Added Transport event processing
+-- Transport/          # Transport abstraction layer (existing)
    +-- Transport.h
    +-- Transport.cpp
    +-- SLikeNetTransport.h
    +-- SLikeNetTransport.cpp
    +-- WebSocketTransport.h
    +-- WebSocketTransport.cpp
    +-- KCPTransport.h
    +-- KCPTransport.cpp

engine/Source/Urho3D/LuaScript/pkgs/Network/
+-- Network.pkg         # Added ConnectWithTransport, StartServerWithTransport
+-- Transport.pkg       # Simplified to only expose protocol enums
```

## Testing

Run the test script:

```bash
# Start server with UDP (default)
./Urho3DPlayer -p "LuaScripts/TransportTest.lua"
# Press 1 for UDP, 2 for WebSocket, 3 for KCP

# In another terminal, start client
./Urho3DPlayer -p "LuaScripts/TransportTest.lua"
# Press C to connect
```

## Multi-Protocol Server (多协议服务器监听) ✅ IMPLEMENTED

**目标**: 服务器支持同时监听多种协议（RakNet/UDP、KCP、WebSocket）

**实现状态**: ✅ 已完成 (2024-12)

### C++ API

```cpp
// 方案: 使用 AddServerTransport() 叠加监听

// 首先启动主协议
network->StartServerWithTransport(12345, TRANSPORT_KCP);

// 添加额外协议监听
network->AddServerTransport(8080, TRANSPORT_WEBSOCKET);
network->AddServerTransport(12346, TRANSPORT_SLIKENET);

// 检查特定协议是否运行
bool kcpRunning = network->IsServerTransportRunning(TRANSPORT_KCP);

// 获取所有运行的协议
Vector<TransportProtocol> protocols = network->GetServerTransportProtocols();

// 停止特定协议
network->StopServerTransport(TRANSPORT_WEBSOCKET);

// 停止所有协议
network->StopServer();
```

### Lua API

```lua
-- 启动多协议服务器
network:StartServerWithTransport(12345, TRANSPORT_KCP)
network:AddServerTransport(8080, TRANSPORT_WEBSOCKET)
network:AddServerTransport(12346, TRANSPORT_SLIKENET)

-- 检查特定协议是否运行
if network:IsServerTransportRunning(TRANSPORT_KCP) then
    print("KCP is running")
end

-- 获取所有运行的协议
local protocols = network:GetServerTransportProtocols()
for i = 1, #protocols do
    print("Protocol: " .. protocols[i])
end

-- 停止特定协议
network:StopServerTransport(TRANSPORT_WEBSOCKET)

-- 停止所有协议
network:StopServer()
```

### 实现细节

- **存储结构**: `serverTransports_` 改为 `Vector<SharedPtr<ITransport>>`
- **连接管理**: 所有协议的连接统一存储在 `transportClientConnections_`
- **事件处理**: `ProcessServerTransportEvents()` 遍历所有 Transport
- **广播消息**: `BroadcastMessage()` 和 `BroadcastRemoteEvent()` 向所有 Transport 广播
- **密码设置**: `SetPassword()` 设置到所有 Transport
- **地址禁止**: `BanAddress()` 在所有 Transport 上生效

### 用例

- PC/主机客户端 (UDP/RakNet) + 手机客户端 (KCP) + 网页客户端 (WebSocket) 同服游玩
- 逐步迁移协议时的双协议过渡期
- 为不同客户端类型提供最优传输协议

### 示例脚本

参见 `engine/bin/Data/LuaScripts/MultiProtocolServerDemo.lua`

---

## Future Enhancements

### High Priority

1. **Unified Connection HashMap**: Currently using two separate HashMaps:
   - `clientConnections_` (HashMap<SLNet::AddressOrGUID, Connection>) for SLikeNet
   - `transportClientConnections_` (HashMap<unsigned, Connection>) for Transport
   - Can be unified when mixed protocol server is implemented
   - Consider using `uint64_t` as unified key type for performance

3. **SLikeNetTransport Integration**: Currently `SLikeNetTransport` is not used
   - `Connect()`/`StartServer()` directly call SLikeNet for backward compatibility
   - `ConnectWithTransport(..., TRANSPORT_SLIKENET)` falls back to direct SLikeNet call
   - Future: optionally route all UDP through `SLikeNetTransport` for unified code path

### Medium Priority

4. **QUIC Support**: Modern protocol combining benefits of TCP and UDP
5. **Protocol Auto-negotiation**: Client tries multiple protocols and picks best
6. **Middleware System**: Compression, encryption as pluggable layers
7. **Connection Quality Metrics**: Automatic protocol selection based on network conditions

### Low Priority

8. **Remove `isServer_` flag**: Currently needed to distinguish server mode from NAT peer
   - Can be refactored when `rakPeer_` is fully encapsulated by Transport layer

---

## RakNet Encapsulation Refactoring Plan

### Current Progress (Last Updated: 2024-12-23)

| Phase | 状态 | 说明 |
|-------|------|------|
| Phase 1: 扩展 ITransport 接口 | ✅ 完成 | 添加 GetConnectionId 等方法 |
| Phase 2: 清理 Connection 类 | ✅ 完成 | 添加 connectionId_, userData_, GetNetworkAddress() |
| Phase 3: 重构 Network 类 | ✅ 完成 | 添加 GetConnectionById(), GetConnectionByAddress() |
| Phase 4: IConnectionFactory | ✅ 完成 | **已删除**，改用 MessageHandler/SendFilter 钩子 |
| Phase 5: 更新 Game 层 | ✅ 完成 | UDPNetwork 已迁移到 MessageHandler/SendFilter API |
| Phase 6: 清理 SLikeNetTransport | ✅ 完成 | getter 已标记 deprecated |
| 验证: Transport 事件处理 | ✅ 完成 | 修复 SLikeNetTransport msgID 处理 |
| **Phase A: Connect/StartServer 统一** | ✅ 完成 | 全部改用 Transport 层 |
| **Phase B: 统一连接存储** | ✅ 完成 | 移除 clientConnections_，统一用 transportClientConnections_ |
| **Phase C: Connection 类清理** | ✅ 完成 | SLikeNet 构造函数/成员标记 deprecated |
| Phase D: NAT Punchthrough | ⏳ 待完成 | 可选，后续处理 |

**已完成的工作 (2024-12-22 ~ 2024-12-23)**:
1. Connection 类新增 `connectionId_`, `userData_`, `networkAddress_` 成员
2. Network 类新增 `GetConnectionById()`, `GetConnectionByAddress()` 方法
3. ~~IConnectionFactory 接口标记为 `@deprecated`~~ **已删除 IConnectionFactory 和 ConnectionFactory.h**
4. SLikeNetTransport 公开 getter 标记为 `@deprecated`
5. **关键修复**: SLikeNetTransport::ProcessPacket() 现在正确包含 msgID 在数据中
   - 之前跳过了 packetID，导致 Network::OnTransportMessage() 解析错误
   - 修复后与 WebSocket/KCP Transport 行为一致
6. **新增 Connection 钩子 API** (替代 IConnectionFactory 继承模式):
   - `Connection::SetMessageHandler(handler)` - 自定义消息处理
   - `Connection::SetSendFilter(filter)` - 拦截/缓存发送消息
   - `Connection::GetMessageHandler()` / `GetSendFilter()` - 获取当前处理器
   - 在 `E_SERVERCONNECTED` / `E_CLIENTCONNECTED` 事件中使用
7. **Game 层迁移完成** (game/src/Game/Network/UDP/):
   - `UDPConnectionFactory` 类已删除
   - `UDPConnectionImpl` 重构为 `UDPMessageAdapter`（不再继承 Connection）
   - 在 `CreateConnection()` 中创建 adapter 并设置 handlers

**2024-12-23 重大重构 - 消除 RakNet 残留，统一走 Transport**:

8. **Network::Connect() 和 StartServer() 统一使用 Transport 层**:
   - `Connect()` 现在调用 `ConnectWithTransport(TRANSPORT_SLIKENET)`
   - `StartServer()` 现在调用 `StartServerWithTransport(TRANSPORT_SLIKENET)`
   - 移除了 `ConnectWithTransport()` 对 UDP 回退到老代码的特殊处理
   - 所有协议（UDP/WebSocket/KCP）现在统一通过 Transport 层

9. **统一连接存储**:
   - 移除了所有对 `clientConnections_` (HashMap<SLNet::AddressOrGUID, Connection>) 的遍历
   - 所有客户端连接现在统一存储在 `transportClientConnections_`
   - 更新了 `BroadcastRemoteEvent()`, `SendPackageToClients()`, `GetConnectionById()`, `GetClientConnections()`, `PostUpdate()`, `ConfigureNetworkSimulator()` 等方法

10. **移除死代码/标记 deprecated**:
    - `Network::Update()` 移除了直接的 RakNet 包处理循环
    - `Network::IsServerRunning()` 简化为只检查 Transport 层
    - `HandleIncomingPacket()`, `HandleMessage()`, `NewConnectionEstablished()`, `ClientDisconnected()` 标记为 `@deprecated`
    - `GetConnection(SLNet::AddressOrGUID)` 标记为 `@deprecated`
    - `rakPeer_`, `rakPeerClient_`, `clientConnections_` 成员标记为 `@deprecated`

11. **Connection 类 SLikeNet 残留标记 deprecated**:
    - SLikeNet 构造函数标记为 `@deprecated`
    - `GetAddressOrGUID()`, `SetAddressOrGUID()` 标记为 `@deprecated`
    - `address_`, `peer_` 成员标记为 `@deprecated`

**2024-12-23 默认协议改为 KCP**:
- `Network::Connect()` 默认使用 `TRANSPORT_KCP` 而非 `TRANSPORT_SLIKENET`
- `Network::StartServer()` 默认使用 `TRANSPORT_KCP`
- `SelectDefaultTransport()` 返回 `TRANSPORT_KCP` 作为原生平台默认值
- 仍可通过环境变量 `URHO3D_TRANSPORT=websocket` 或 `URHO3D_TRANSPORT=kcp` 覆盖

**待完成 (Phase D - 可选)**:
- NAT Punchthrough 功能需要移植到 Transport 层（当前仍使用 Network 类的 rakPeer_）

**Game 层迁移指南** (`game/src/Game/Network/UDP/`):

```cpp
// 旧方式 (已删除):
class UDPConnectionFactory : public IConnectionFactory { ... };
class UDPConnectionImpl : public Connection { ... };
network->SetConnectionFactory(factory);

// 新方式:
class UDPMessageAdapter {
public:
    bool HandleMessage(int msgID, MemoryBuffer& msg) {
        if (pause_) { cache...; return true; }
        UncompressMessage(msg.GetData(), msg.GetSize());
        return true;
    }
    bool FilterSend(const unsigned char* data, unsigned size, int rel, char ch) {
        if (pause_) { cache...; return true; }
        return false;
    }
};

// 在 E_SERVERCONNECTED 事件中:
void HandleServerConnected(...) {
    auto* conn = network->GetServerConnection();
    auto* adapter = new UDPMessageAdapter(netContext_);
    conn->SetUserData(adapter);
    conn->SetMessageHandler([adapter](int id, MemoryBuffer& msg) {
        return adapter->HandleMessage(id, msg);
    });
    conn->SetSendFilter([adapter](auto... args) {
        return adapter->FilterSend(args...);
    });
}
```

**下一步计划**:
1. 更新 `game/src/Game/Network/UDP/` 使用新 API
2. Connect()/StartServer() 内部改为调用 Transport 版本（高风险，需充分测试）
3. Phase 2/3 剩余工作 - 移除 SLikeNet 直接成员（需确认无外部依赖后）

---

### Problem Statement

当前 Network 子系统存在**严重的架构缺陷**：RakNet/SLikeNet 类型没有被封装在 Transport 层，而是**直接暴露在 Connection 和 Network 核心类中**。

这违背了 Transport 抽象层的设计初衷：**SLikeNet 应该和 KCP、WebSocket 处于同一抽象级别，完全封装在各自的 Transport 实现中**。

### Current Architecture (Broken)

```
┌─────────────────────────────────────────────────────────────────┐
│                       Connection.h                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ PUBLIC:                                                   │   │
│  │   SLNet::AddressOrGUID* address_     ← 直接暴露 RakNet   │   │
│  │   SLNet::RakPeerInterface* peer_     ← 直接暴露 RakNet   │   │
│  │   GetAddressOrGUID()                 ← 公开 getter       │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │   ITransport* transport_             ← Transport 抽象    │   │
│  │   NetworkAddress* transportAddress_  ← Transport 抽象    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       Network.h                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ PUBLIC:                                                   │   │
│  │   HandleMessage(SLNet::AddressOrGUID&, ...)   ← 暴露     │   │
│  │   NewConnectionEstablished(SLNet::AddressOrGUID&)         │   │
│  │   GetConnection(SLNet::AddressOrGUID&)                    │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ PRIVATE:                                                  │   │
│  │   SLNet::RakPeerInterface* rakPeer_           ← 直接持有  │   │
│  │   SLNet::RakPeerInterface* rakPeerClient_     ← 直接持有  │   │
│  │   HashMap<SLNet::AddressOrGUID, Connection>   ← 直接使用  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

问题：
1. Connection 同时持有两套成员变量（SLikeNet + Transport）
2. Network 直接操作 RakPeerInterface，绕过 Transport 层
3. SLikeNet 类型暴露在公共头文件中
4. IConnectionFactory 强制使用 RakNet 类型
```

### Target Architecture (Correct)

```
┌─────────────────────────────────────────────────────────────────┐
│                       Connection.h                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ONLY Transport abstractions:                              │   │
│  │   ITransport* transport_                                  │   │
│  │   NetworkAddress address_                                 │   │
│  │   uint64_t connectionId_   (unified key for HashMap)      │   │
│  │                                                           │   │
│  │   NO SLikeNet types!                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ uses ITransport interface
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ITransport (abstract)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Send(NetworkAddress, data, reliability)                  │  │
│  │  Poll(events)                                             │  │
│  │  Connect(NetworkAddress)                                  │  │
│  │  Disconnect(NetworkAddress)                               │  │
│  │  GetConnectionId(NetworkAddress) → uint64_t               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
              │                    │                    │
    ┌─────────┴────────┐ ┌────────┴────────┐ ┌────────┴────────┐
    ▼                  ▼ ▼                 ▼ ▼                 ▼
┌──────────────┐ ┌──────────────┐ ┌────────────────────────────┐
│KCPTransport  │ │WebSocket     │ │SLikeNetTransport           │
│              │ │Transport     │ │  ┌──────────────────────┐  │
│ kcp_cb_*     │ │              │ │  │ RakPeerInterface*    │  │  ← 封装
│ ikcp_*       │ │ lws_*        │ │  │ AddressOrGUID        │  │  ← 内部
│              │ │              │ │  │ SystemAddress        │  │
└──────────────┘ └──────────────┘ │  └──────────────────────┘  │
                                  └────────────────────────────┘
```

### Detailed Problem Analysis

#### Problem 1: Connection 持有两套成员

**当前代码** (`Connection.h:343-352`):
```cpp
class Connection {
private:
#ifndef __EMSCRIPTEN__
    // Legacy SLikeNet (不应该在这里!)
    SLNet::AddressOrGUID* address_;
    SLNet::RakPeerInterface* peer_;
#endif
    // Transport layer
    SharedPtr<ITransport> transport_;
    NetworkAddress* transportAddress_;
};
```

**问题**：
- 两套成员变量并存，逻辑复杂
- `address_` 和 `transportAddress_` 语义重复
- `peer_` 应该由 Transport 管理，不是 Connection

#### Problem 2: Network 直接操作 RakPeerInterface

**当前代码** (`Network.h` + `Network.cpp`):
```cpp
class Network {
private:
    SLNet::RakPeerInterface* rakPeer_;        // 服务器端
    SLNet::RakPeerInterface* rakPeerClient_;  // 客户端
    // ...
};

// Network.cpp 中直接调用 RakNet API
bool Network::Connect(...) {
    rakPeerClient_->Connect(address.CString(), port, ...);  // 直接调用!
}
```

**问题**：
- `Network::Connect()` 绕过 Transport 层直接使用 RakNet
- 无法统一切换传输协议
- SLikeNet 代码散落在 Network.cpp 各处

#### Problem 3: IConnectionFactory 强制 RakNet 类型

**当前代码** (`ConnectionFactory.h:18-22`):
```cpp
class IConnectionFactory {
    virtual Connection* Create(Context* ctx, bool isClient,
                              const SLNet::AddressOrGUID& address,      // 被迫使用
                              SLNet::RakPeerInterface* peer) = 0;       // 被迫使用
};
```

**问题**：
- 任何想扩展 Connection 的代码都必须依赖 RakNet
- 与 Transport 设计冲突（Transport 使用 NetworkAddress）

#### Problem 4: 两套并行的连接存储

**当前代码** (`Network.h`):
```cpp
class Network {
private:
    // SLikeNet 连接
    HashMap<SLNet::AddressOrGUID, SharedPtr<Connection>> clientConnections_;
    // Transport 连接
    HashMap<unsigned, SharedPtr<Connection>> transportClientConnections_;
};
```

**问题**：
- 两套 HashMap 维护成本高
- 查询连接时需要判断用哪个 HashMap
- 代码复杂度增加

---

### Refactoring Strategy

#### Core Principle

**SLikeNet 必须完全封装在 `SLikeNetTransport` 内部**，与 KCP/WebSocket 处于同一抽象级别。

所有 Network/Connection 代码只通过 `ITransport` 接口操作，不直接使用任何 RakNet 类型。

---

#### Phase 1: Extend ITransport Interface

**目标**：让 ITransport 提供足够的抽象，使 Connection 和 Network 无需知道底层实现

**新增接口** (`Transport.h`):

```cpp
class ITransport {
public:
    // 现有接口...

    /// Get unique connection ID for a network address
    /// This ID is used as HashMap key, replacing SLNet::AddressOrGUID
    virtual uint64_t GetConnectionId(const NetworkAddress& address) const = 0;

    /// Get network address from connection ID
    virtual NetworkAddress GetAddressFromId(uint64_t connectionId) const = 0;

    /// Internal data access (for Transport implementations only)
    /// Returns opaque pointer that specific Transport can cast
    virtual void* GetInternalData(uint64_t connectionId) const { return nullptr; }
};
```

**SLikeNetTransport 实现**:

```cpp
class SLikeNetTransport : public ITransport {
public:
    uint64_t GetConnectionId(const NetworkAddress& address) const override {
        // 从内部映射查找对应的 AddressOrGUID，返回其 hash
        auto it = addressToGuid_.Find(address);
        return it != addressToGuid_.End() ? HashAddressOrGUID(it->second_) : 0;
    }

    void* GetInternalData(uint64_t connectionId) const override {
        // 返回内部的 AddressOrGUID 指针（仅供内部使用）
        auto it = idToAddress_.Find(connectionId);
        return it != idToAddress_.End() ? &it->second_ : nullptr;
    }

private:
    // 内部维护映射
    HashMap<NetworkAddress, SLNet::AddressOrGUID> addressToGuid_;
    HashMap<uint64_t, SLNet::AddressOrGUID> idToAddress_;
    SLNet::RakPeerInterface* rakPeer_;  // 完全封装在内部
};
```

---

#### Phase 2: Clean Up Connection Class

**目标**：Connection 只依赖 Transport 抽象

**变更** (`Connection.h`):

```cpp
class Connection {
public:
    /// Single constructor - only Transport API
    Connection(Context* context, bool isClient, ITransport* transport, const NetworkAddress& address);

    /// Get network address (replaces GetAddressOrGUID)
    const NetworkAddress& GetAddress() const { return address_; }

    /// Get unique connection ID (for HashMap key)
    uint64_t GetConnectionId() const { return connectionId_; }

    /// Get transport
    ITransport* GetTransport() const { return transport_.Get(); }

    /// User data for extension (replaces inheritance)
    void SetUserData(void* data) { userData_ = data; }
    void* GetUserData() const { return userData_; }

private:
    SharedPtr<ITransport> transport_;
    NetworkAddress address_;
    uint64_t connectionId_;
    void* userData_ = nullptr;

    // NO SLikeNet members!
    // 移除: SLNet::AddressOrGUID* address_;
    // 移除: SLNet::RakPeerInterface* peer_;
};
```

**废弃兼容层** (可选，用于过渡期):

```cpp
#ifndef __EMSCRIPTEN__
// Deprecated compatibility layer - will be removed
[[deprecated("Use GetAddress() instead")]]
inline SLNet::AddressOrGUID GetAddressOrGUID_Compat(Connection* conn) {
    if (auto* slikeNet = dynamic_cast<SLikeNetTransport*>(conn->GetTransport())) {
        return *static_cast<SLNet::AddressOrGUID*>(
            slikeNet->GetInternalData(conn->GetConnectionId()));
    }
    return {};
}
#endif
```

---

#### Phase 3: Refactor Network Class

**目标**：Network 只通过 Transport 接口操作，不直接使用 RakNet

**变更** (`Network.h`):

```cpp
class Network {
public:
    /// Connect using default or preferred transport
    bool Connect(const String& address, unsigned short port, Scene* scene,
                const VariantMap& identity = {});

    /// Get connection by address
    Connection* GetConnection(const NetworkAddress& address) const;

    /// Get connection by ID
    Connection* GetConnectionById(uint64_t connectionId) const;

private:
    /// Single unified connection storage
    HashMap<uint64_t, SharedPtr<Connection>> clientConnections_;

    /// Active transports (server may have multiple)
    Vector<SharedPtr<ITransport>> serverTransports_;
    SharedPtr<ITransport> clientTransport_;

    // 移除: SLNet::RakPeerInterface* rakPeer_;
    // 移除: SLNet::RakPeerInterface* rakPeerClient_;
    // 移除: HashMap<SLNet::AddressOrGUID, SharedPtr<Connection>> clientConnections_;
};
```

**Connect 实现变更** (`Network.cpp`):

```cpp
// Before (直接使用 RakNet)
bool Network::Connect(...) {
    rakPeerClient_ = SLNet::RakPeerInterface::GetInstance();
    rakPeerClient_->Startup(1, &sd, 1);
    rakPeerClient_->Connect(address.CString(), port, password.CString(), ...);
}

// After (通过 Transport)
bool Network::Connect(...) {
    // 使用 TransportFactory 创建合适的 Transport
    clientTransport_ = TransportFactory::Create(preferredProtocol_);
    if (!clientTransport_->StartClient())
        return false;

    NetworkAddress addr(address, port, preferredProtocol_);
    return clientTransport_->Connect(addr, password);
}
```

---

#### Phase 4: Remove IConnectionFactory

**目标**：完全移除 IConnectionFactory，用 UserData + 事件替代

**删除文件**：
- `ConnectionFactory.h`

**Network.cpp 变更**：

```cpp
// Before (使用 Factory)
void Network::NewConnectionEstablished(const SLNet::AddressOrGUID& connection) {
    auto conn = connectFactory_->Create(context_, true, connection, rakPeer_);
    clientConnections_[connection] = conn;
}

// After (直接创建 + 事件通知)
void Network::HandleTransportConnected(const TransportEvent& event) {
    auto conn = new Connection(context_, true, serverTransport_, event.address_);
    uint64_t id = serverTransport_->GetConnectionId(event.address_);
    clientConnections_[id] = conn;

    // Game 层通过事件设置 UserData
    SendEvent(E_CLIENTCONNECTED, "Connection", conn);
}
```

**Game 层迁移**：

```cpp
// Before
class UDPConnectionFactory : public IConnectionFactory { ... };
class UDPConnectionImpl : public Connection { ... };

// After
void UDPNetwork::HandleClientConnected(StringHash, VariantMap& eventData) {
    auto* conn = static_cast<Connection*>(eventData["Connection"].GetPtr());
    conn->SetUserData(netContext_);  // 直接设置，无需继承
}
```

---

#### Phase 5: Update SLikeNetTransport

**目标**：SLikeNetTransport 完全封装 RakNet，提供 ITransport 接口

**当前问题** (`SLikeNetTransport.h:99-102`):

```cpp
// 这些 getter 破坏封装!
SLNet::RakPeerInterface* GetServerPeer() const { return rakPeer_; }
SLNet::RakPeerInterface* GetClientPeer() const { return rakPeerClient_; }
```

**变更**：

```cpp
class SLikeNetTransport : public ITransport {
public:
    // ITransport interface implementation
    bool StartServer(unsigned maxConnections, unsigned short port) override;
    bool StartClient() override;
    bool Connect(const NetworkAddress& address, const String& password) override;
    bool Send(const NetworkAddress& address, const unsigned char* data, ...) override;
    void Poll(Vector<TransportEvent>& events) override;
    uint64_t GetConnectionId(const NetworkAddress& address) const override;

    // 移除公开的 RakNet getter!
    // 如果内部确实需要访问，使用 GetInternalData()

private:
    SLNet::RakPeerInterface* rakPeer_ = nullptr;
    SLNet::RakPeerInterface* rakPeerClient_ = nullptr;

    // 内部地址映射
    HashMap<NetworkAddress, SLNet::AddressOrGUID> addressMap_;
    HashMap<uint64_t, NetworkAddress> idToAddress_;
};
```

---

### Implementation Checklist

#### Phase 1: Extend ITransport (1 day) ✅ COMPLETED (2024-12-22)

- [x] `Transport.h`: 添加 `GetConnectionId()`, `GetAddressFromId()`, `IsValidConnectionId()`
- [x] `SLikeNetTransport`: 实现新接口，内部维护 `idToAddress_` 映射
- [x] `WebSocketTransport`: 实现新接口，连接/断开时更新映射
- [x] `KCPTransport`: 实现新接口，握手完成时添加映射

**已完成的具体修改**:
- `Transport.h:297-312` - 新增接口声明
- `SLikeNetTransport.h:102-105,146-149` - 声明 + 成员变量
- `SLikeNetTransport.cpp:56,132,302,313,325-332,465-481` - 初始化、连接/断开映射、实现
- `WebSocketTransport.h:141-144,189-192` - 声明 + 成员变量
- `WebSocketTransport.cpp:43,89,116-123,214,239,316,346-353,614-632,688,752-760` - 实现
- `KCPTransport.h:143-146,226-229` - 声明 + 成员变量
- `KCPTransport.cpp:145,220,504-522,582-590,721,771` - 实现

#### Phase 2: Clean Up Connection (2 days) ⏳ IN PROGRESS (2024-12-22)

- [x] `Connection.h`: 添加 `connectionId_`, `userData_` 成员
- [x] `Connection.h`: 添加 `GetConnectionId()`, `GetNetworkAddress()`, `SetUserData()`, `GetUserData()`
- [x] `Connection.cpp`: Transport 构造函数初始化 `connectionId_` (从 ITransport::GetConnectionId 获取)
- [x] `Connection.cpp`: SLikeNet 构造函数初始化 `connectionId_`, `userData_`
- [ ] `Connection.h`: 移除 `SLNet::` 成员和 forward declarations (待完成 Phase 3 后)
- [ ] `Connection.h`: 移除 `GetAddressOrGUID()`, 只保留 `GetAddress()` (待完成 Phase 3 后)
- [ ] `Connection.cpp`: 移除 SLikeNet 构造函数 (待完成 Phase 3 后)
- [ ] `Connection.cpp`: 更新 `Send()`, `Disconnect()` 等方法只使用 Transport (待完成 Phase 3 后)

**已完成的具体修改 (2024-12-22)**:
- `Connection.h:177-186` - 添加 `GetConnectionId()`, `GetNetworkAddress()`, `SetUserData()`, `GetUserData()`
- `Connection.h:354-357` - 添加 `connectionId_`, `userData_` 成员变量
- `Connection.cpp:84-109` - Transport 构造函数初始化新成员
- `Connection.cpp:112-130` - SLikeNet 构造函数初始化新成员

#### Phase 3: Refactor Network (3 days) ⏳ PARTIAL (2024-12-22)

- [x] `Network.h`: 添加 `GetConnectionById(uint64_t)` 方法
- [x] `Network.h`: 添加 `GetConnectionByAddress(const NetworkAddress&)` 方法
- [x] `Network.cpp`: 实现 `GetConnectionById()` (遍历所有连接类型)
- [x] `Network.cpp`: 实现 `GetConnectionByAddress()` (查找 Transport 连接)
- [ ] `Network.h`: 移除 `SLNet::RakPeerInterface*` 成员 (风险较高，待后续)
- [ ] `Network.h`: 统一 `clientConnections_` 为 `HashMap<uint64_t, Connection>` (风险较高，待后续)
- [ ] `Network.h`: 移除 RakNet 相关的公开方法 (风险较高，待后续)
- [ ] `Network.cpp`: `Connect()` 改为通过 Transport (待验证 SLikeNetTransport 完整性)
- [ ] `Network.cpp`: `StartServer()` 改为通过 Transport (待验证 SLikeNetTransport 完整性)
- [ ] `Network.cpp`: `Update()` 改为处理 Transport 事件 (已部分支持，需统一)

**已完成的具体修改 (2024-12-22)**:
- `Network.h:152-154` - 添加 `GetConnectionById()`, `GetConnectionByAddress()` 声明
- `Network.cpp:811-861` - 实现 `GetConnectionById()`, `GetConnectionByAddress()`

#### Phase 4: Remove IConnectionFactory (1 day)

- [ ] 删除 `ConnectionFactory.h`
- [ ] `Network.h`: 移除 `connectFactory_` 和 `SetConnectionFactory()`
- [ ] `Network.cpp`: 移除 `DefaultConnectionFactory`
- [ ] `CMakeLists.txt`: 移除 `ConnectionFactory.h`

#### Phase 5: Update Game Layer (1 day)

- [ ] `UDPNetwork.h`: 移除 `UDPConnectionFactory`
- [ ] `UDPNetwork.cpp`: 改用事件 + `SetUserData()`
- [ ] 评估 `UDPConnectionImpl` 是否仍需要（可能可删除）

#### Phase 6: Cleanup SLikeNetTransport (1 day)

- [ ] `SLikeNetTransport.h`: 移除 `GetServerPeer()`, `GetClientPeer()`
- [ ] 确保所有 RakNet 操作通过 ITransport 接口
- [ ] 添加内部地址映射管理

---

### File Changes Summary

| 文件 | 操作 | 变更内容 |
|------|------|---------|
| `Transport.h` | 修改 | 添加 `GetConnectionId()` 等新接口 |
| `Connection.h` | **重写** | 移除所有 SLikeNet 成员和接口 |
| `Connection.cpp` | **重写** | 只使用 Transport API |
| `Network.h` | **重写** | 移除 RakNet 成员，统一连接存储 |
| `Network.cpp` | **重写** | 通过 Transport 操作，处理 Transport 事件 |
| `ConnectionFactory.h` | **删除** | 不再需要 |
| `SLikeNetTransport.h` | 修改 | 实现新接口，移除公开 getter |
| `SLikeNetTransport.cpp` | 修改 | 内部地址映射，完整封装 |
| `WebSocketTransport.cpp` | 修改 | 实现 `GetConnectionId()` |
| `KCPTransport.cpp` | 修改 | 实现 `GetConnectionId()` |
| `UDPNetwork.h` | 修改 | 移除 `UDPConnectionFactory` |
| `UDPNetwork.cpp` | 修改 | 改用事件 + UserData |

---

### Risk Assessment

| 风险 | 级别 | 缓解措施 |
|------|------|---------|
| 大规模重构导致回归 | 🔴 高 | 分阶段实施，每阶段完成后充分测试 |
| SLikeNet 特有功能丢失 | 🟡 中 | 确保 ITransport 接口覆盖所有必要功能 |
| Game 层代码需同步修改 | 🟡 中 | Phase 4-5 同时进行 |
| 性能影响（额外的间接层） | 🟢 低 | 几乎无影响，只是函数调用重定向 |

### Success Criteria

1. ✅ `Connection.h` 中无 `SLNet::` 前缀的任何内容
2. ✅ `Network.h` 中无 `SLNet::` 前缀的任何内容
3. ✅ `ConnectionFactory.h` 被完全删除
4. ✅ Game 层代码不再 `#include` 任何 SLikeNet 头文件
5. ✅ 所有 RakNet 类型仅存在于 `SLikeNetTransport.cpp` 内部
6. ✅ 现有功能正常工作（UDP/WebSocket/KCP 三种协议）
7. ✅ Lua API 保持不变

---

## References

- [KCP Protocol](https://github.com/skywind3000/kcp)
- [libwebsockets](https://libwebsockets.org/)
- [Emscripten WebSocket API](https://emscripten.org/docs/api_reference/websocket.h.html)
- [SLikeNet](https://github.com/SLikeSoft/SLikeNet)
