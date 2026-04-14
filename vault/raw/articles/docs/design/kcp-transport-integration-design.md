---
summary: "Integration design for ACGame::KCPNetwork with the Urho3D::ITransport interface"
related_paths:
  - engine/Source/Urho3D/Network/**
last_updated: "2025-01-01"
---

# KCP Transport Integration Design

## Overview

This document describes how to integrate the existing mature `ACGame::KCPNetwork` implementation with the new `Urho3D::ITransport` interface.

## Current State Analysis

### Two KCP Implementations

| Feature | `ACGame::KCPNetwork` | `Urho3D::KCPTransport` |
|---------|---------------------|------------------------|
| Location | `game/src/Game/Network/UDP/` | `engine/Source/Urho3D/Network/Transport/` |
| Purpose | Game-specific, production-ready | Engine generic interface |
| FEC Support | Yes (Forward Error Correction) | No |
| Compression | Yes (ZCompressAdapter) | No |
| Threading | Dedicated update thread | Single-threaded polling |
| Handshake | Custom (CE1SYN/CE1SYNACK) | Standard (SYN/SYNACK/ACK) |
| Ping | ICMP + Connection ping | None |
| Pause/Resume | Yes | No |
| Replace Connection | Yes | No |
| Message Encoding | Protobuf | Raw bytes |
| Statistics | Comprehensive | Basic |

### Interface Comparison

**ACGame::Network Interface:**
```cpp
class Network {
    virtual void Connect(const char* ip, unsigned short port) = 0;
    virtual void Disconnect() = 0;
    virtual void WaitForDisconnect(int waitMSec) = 0;
    virtual bool IsActive() = 0;
    virtual Connection* GetConnection() = 0;
};

class Connection {
    virtual void SendMessage(const void* data, unsigned size,
                            PacketReliability reliability, char channel) = 0;
    virtual void Pause(bool isLoading) = 0;
    virtual void Resume(bool isLoading) = 0;
    virtual int GetLastPing() const = 0;
    // ... more ping methods
};

class Callback {
    virtual void OnConnected(Connection*) = 0;
    virtual void OnDisconnected(Connection*) = 0;
    virtual void OnReceiveMessage(Connection*, const void* data, unsigned size) = 0;
    virtual void OnErrorCatch(FantasyNetworkError error, const char* msg) = 0;
};
```

**Urho3D::ITransport Interface:**
```cpp
class ITransport {
    virtual bool StartServer(unsigned maxConnections, unsigned short port) = 0;
    virtual bool StartClient() = 0;
    virtual void Shutdown() = 0;
    virtual bool Connect(const NetworkAddress& address, const String& password) = 0;
    virtual void Disconnect(const NetworkAddress& address, int waitMSec) = 0;
    virtual void DisconnectAll(int waitMSec) = 0;
    virtual bool Send(const NetworkAddress& address, const unsigned char* data,
                     unsigned size, TransportReliability reliability, unsigned char channel) = 0;
    virtual bool Broadcast(const unsigned char* data, unsigned size,
                          TransportReliability reliability, unsigned char channel) = 0;
    virtual void Poll(Vector<TransportEvent>& events) = 0;
    virtual bool IsActive() const = 0;
    virtual bool IsServer() const = 0;
    // ...
};
```

## Design Decision: Adapter vs Refactor

### Option A: Adapter Pattern (Recommended)

Create an adapter that wraps `ACGame::KCPNetwork` to implement `ITransport`.

**Pros:**
- No changes to existing, tested `KCPNetwork` code
- Reuse all production-proven features (FEC, compression, threading)
- Gradual migration path
- Low risk

**Cons:**
- Additional layer of indirection
- Some interface impedance mismatch
- Game-specific dependencies need abstraction

### Option B: Refactor KCPNetwork to Engine

Move core `KCPNetwork` to engine, make game-specific parts pluggable.

**Pros:**
- Clean separation of concerns
- Single implementation to maintain
- Native `ITransport` conformance

**Cons:**
- High risk: changes to production code
- Complex dependency management (protobuf, compression)
- Significant engineering effort

### Recommendation: Option A with Gradual Migration

1. **Phase 1**: Create `KCPNetworkAdapter` that wraps `ACGame::KCPNetwork`
2. **Phase 2**: Extract core KCP logic to engine (optional, based on Phase 1 results)

## Phase 1: Adapter Implementation

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Network Class (Engine)                    │
│            ConnectWithTransport(TRANSPORT_KCP)             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    ITransport Interface                     │
│    StartClient(), Connect(), Send(), Poll(), etc.          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  KCPNetworkAdapter                          │
│   Implements ITransport, wraps ACGame::KCPNetwork           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  - Translates ITransport calls to KCPNetwork API    │   │
│  │  - Implements ACGame::Callback for events           │   │
│  │  - Converts events to TransportEvent                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   ACGame::KCPNetwork                        │
│   Production KCP with FEC, compression, threading           │
└─────────────────────────────────────────────────────────────┘
```

### Key Implementation Details

#### 1. Client-Only Support

`ACGame::KCPNetwork` is designed for client-only use (connects to game server). The adapter will:
- Return `false` from `StartServer()`
- Implement `StartClient()` + `Connect()` for client mode

#### 2. Single Connection Model

`KCPNetwork` supports only one connection at a time. The adapter will:
- Track current connection address
- Validate address in `Send()` and `Disconnect()`

#### 3. Event Translation

```cpp
// ACGame events → TransportEvent mapping
KCPEventType::CONNECTED      → TRANSPORT_EVENT_CONNECTED
KCPEventType::DISCONNECTED   → TRANSPORT_EVENT_DISCONNECTED
KCPEventType::CONNECTION_ERROR → TRANSPORT_EVENT_CONNECT_FAILED
KCPEventType::DATA           → TRANSPORT_EVENT_DATA
```

#### 4. Reliability Mapping

```cpp
// TransportReliability → PacketReliability
TRANSPORT_UNRELIABLE          → UNRELIABLE
TRANSPORT_UNRELIABLE_SEQUENCED → UNRELIABLE_SEQUENCED
TRANSPORT_RELIABLE            → RELIABLE
TRANSPORT_RELIABLE_ORDERED    → RELIABLE_ORDERED (default)
```

### Proposed Interface

```cpp
// engine/Source/Urho3D/Network/Transport/KCPNetworkAdapter.h

#pragma once

#include "Transport.h"
#include <functional>

namespace ACGame {
    class KCPNetwork;
    class Callback;
}

namespace Urho3D {

class Context;

/// Configuration for KCP network adapter
struct KCPAdapterConfig
{
    /// FEC data shards (0 = disabled)
    unsigned char fecDataShards_ = 0;
    /// FEC parity shards (0 = disabled)
    unsigned char fecParityShards_ = 0;
    /// Use stream mode
    bool streamMode_ = false;
    /// Connection timeout in seconds
    float timeoutSeconds_ = 3.0f;
};

/// Adapter that wraps ACGame::KCPNetwork to implement ITransport
/// This allows reusing the production KCP implementation with the Transport API
class URHO3D_API KCPNetworkAdapter : public ITransport
{
public:
    /// Factory function type for creating KCPNetwork instances
    /// This allows the game layer to provide the actual KCPNetwork implementation
    using KCPNetworkFactory = std::function<ACGame::KCPNetwork*(Context*, ACGame::Callback*)>;

    /// Construct with factory function
    KCPNetworkAdapter(Context* context, KCPNetworkFactory factory = nullptr);
    /// Destruct
    ~KCPNetworkAdapter() override;

    /// Set configuration (must be called before Connect)
    void SetConfig(const KCPAdapterConfig& config);

    /// Set factory function for creating KCPNetwork
    void SetFactory(KCPNetworkFactory factory);

    // ITransport implementation
    bool StartServer(unsigned maxConnections, unsigned short port) override;
    bool StartClient() override;
    void Shutdown() override;

    bool Connect(const NetworkAddress& address, const String& password = String::EMPTY) override;
    void Disconnect(const NetworkAddress& address, int waitMSec = 0) override;
    void DisconnectAll(int waitMSec = 0) override;

    bool Send(const NetworkAddress& address, const unsigned char* data, unsigned size,
             TransportReliability reliability = TRANSPORT_RELIABLE_ORDERED,
             unsigned char channel = 0) override;
    bool Broadcast(const unsigned char* data, unsigned size,
                  TransportReliability reliability = TRANSPORT_RELIABLE_ORDERED,
                  unsigned char channel = 0) override;

    void Poll(Vector<TransportEvent>& events) override;

    bool IsActive() const override;
    bool IsServer() const override { return false; } // Client-only

    TransportStats GetStats(const NetworkAddress& address) const override;
    Vector<NetworkAddress> GetConnections() const override;

    TransportProtocol GetProtocol() const override { return TRANSPORT_KCP; }

    void SetPassword(const String& password) override;
    void SetNetworkSimulation(int latencyMs, float packetLoss) override;
    void BanAddress(const String& address) override;

    NetworkAddress GetLocalAddress() const override;

    // KCP-specific methods exposed through adapter
    /// Pause sending (for background/loading states)
    void Pause(bool isLoading = false);
    /// Resume sending
    void Resume(bool isLoading = false);
    /// Get ping statistics
    int GetLastPing() const;
    int GetAveragePing() const;
    int GetLowestPing() const;

private:
    class CallbackAdapter;

    /// Urho3D context
    Context* context_;
    /// Factory function
    KCPNetworkFactory factory_;
    /// Wrapped KCPNetwork instance
    ACGame::KCPNetwork* kcpNetwork_;
    /// Callback adapter
    CallbackAdapter* callbackAdapter_;
    /// Configuration
    KCPAdapterConfig config_;
    /// Current connection address
    NetworkAddress currentAddress_;
    /// Client started flag
    bool clientStarted_;
    /// Pending events from callback
    Vector<TransportEvent> pendingEvents_;
    /// Mutex for thread safety
    mutable Mutex mutex_;
};

}
```

### Game Layer Integration

The game layer needs to register the factory function:

```cpp
// game/src/Game/Network/KCPTransportBridge.cpp

#include <Urho3D/Network/Transport/KCPNetworkAdapter.h>
#include "UDP/KCPNetwork.h"

namespace ACGame {

void RegisterKCPTransportBridge(Urho3D::Context* context)
{
    // Register factory function with TransportFactory
    Urho3D::TransportFactory::RegisterKCPFactory([context](Urho3D::Context* ctx, void* callbackPtr)
    {
        auto* callback = static_cast<ACGame::Callback*>(callbackPtr);
        // Use default FEC settings from game config
        return Network::CreateKCPNetwork(ctx, callback,
            GameConfig::GetFECDataShards(),
            GameConfig::GetFECParityShards(),
            GameConfig::UseStreamMode());
    });
}

}
```

## Build System Changes

### CMakeLists.txt Updates

```cmake
# engine/Source/Urho3D/Network/Transport/CMakeLists.txt

if (URHO3D_KCP)
    # Option 1: Use simple KCPTransport (current)
    set (KCP_TRANSPORT_SOURCES
        KCPTransport.cpp
        KCPTransport.h
    )

    # Option 2: Use KCPNetworkAdapter (for game integration)
    if (URHO3D_KCP_USE_ADAPTER)
        set (KCP_TRANSPORT_SOURCES
            KCPNetworkAdapter.cpp
            KCPNetworkAdapter.h
        )
        add_definitions(-DURHO3D_KCP_USE_ADAPTER)
    endif()

    list (APPEND TRANSPORT_SOURCES ${KCP_TRANSPORT_SOURCES})
endif()
```

### Build Options

| Option | Description |
|--------|-------------|
| `URHO3D_KCP=1` | Enable KCP transport support |
| `URHO3D_KCP_USE_ADAPTER=1` | Use adapter with ACGame::KCPNetwork (for game builds) |

## Usage Examples

### Lua Script Usage

```lua
-- The API remains unchanged from user perspective
network:ConnectWithTransport("192.168.1.100", 8888, scene, TRANSPORT_KCP)

-- Events work as before
SubscribeToEvent("ServerConnected", HandleServerConnected)
SubscribeToEvent("ClientConnected", HandleClientConnected)
```

### C++ Usage (Engine Side)

```cpp
// Connecting with KCP
NetworkAddress address("192.168.1.100", 8888, TRANSPORT_KCP);
SharedPtr<ITransport> transport = TransportFactory::Create(TRANSPORT_KCP);

if (transport->StartClient())
{
    transport->Connect(address);
}

// In update loop
Vector<TransportEvent> events;
transport->Poll(events);

for (const auto& event : events)
{
    switch (event.type_)
    {
    case TRANSPORT_EVENT_CONNECTED:
        // Handle connection
        break;
    case TRANSPORT_EVENT_DATA:
        // Handle received data
        break;
    }
}
```

### C++ Usage (Game Side with Full Features)

```cpp
// Access KCP-specific features through adapter
auto* adapter = dynamic_cast<KCPNetworkAdapter*>(transport.Get());
if (adapter)
{
    // Use FEC and compression (configured at creation)
    adapter->Pause(true);  // For loading screen
    // ... loading ...
    adapter->Resume(true);

    // Get ping stats
    int ping = adapter->GetLastPing();
}
```

## Migration Path

### Step 1: Initial Integration (Current Task)

1. Create `KCPNetworkAdapter` in engine
2. Modify `TransportFactory` to support factory registration
3. Register adapter in game initialization
4. Test with `TransportTest.lua`

### Step 2: Feature Parity (Optional)

1. Add FEC support to engine `KCPTransport`
2. Add compression support
3. Add threading support

### Step 3: Consolidation (Future)

1. Move core KCP logic to engine
2. Make game-specific features (protobuf) pluggable
3. Deprecate game-layer `KCPNetwork`

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Thread safety issues | Use mutex in adapter, minimize shared state |
| Callback timing | Buffer events, process in Poll() |
| Memory management | Use SharedPtr/raw ptr boundary carefully |
| Build complexity | Clear CMake option documentation |

## Conclusion

The adapter approach provides a low-risk way to leverage the mature `ACGame::KCPNetwork` implementation while conforming to the new `ITransport` interface. This enables:

1. **Immediate Value**: Use production KCP features in Transport API
2. **Backward Compatibility**: Existing game code unchanged
3. **Gradual Evolution**: Option to refactor later based on experience

## Files to Create/Modify

**New Files:**
- `engine/Source/Urho3D/Network/Transport/KCPNetworkAdapter.h`
- `engine/Source/Urho3D/Network/Transport/KCPNetworkAdapter.cpp`
- `game/src/Game/Network/KCPTransportBridge.h`
- `game/src/Game/Network/KCPTransportBridge.cpp`

**Modified Files:**
- `engine/Source/Urho3D/Network/Transport/Transport.h` - Add factory registration
- `engine/Source/Urho3D/Network/Transport/Transport.cpp` - Implement registration
- `engine/Source/Urho3D/CMakeLists.txt` - Add `URHO3D_KCP_USE_ADAPTER` option
- `tools/generators/gen_vs_agent.bat` - Add adapter option for game builds

---

## Implementation Status

### Completed Files

**Engine Layer:**
- `engine/Source/Urho3D/Network/Transport/Transport.h` - Added `SetKCPFactory()` for factory registration
- `engine/Source/Urho3D/Network/Transport/Transport.cpp` - Implemented factory registration, changed to `__EMSCRIPTEN__` macro
- `engine/Source/Urho3D/Network/Transport/KCPNetworkAdapter.h` - Adapter interface definition
- `engine/Source/Urho3D/Network/Transport/KCPNetworkAdapter.cpp` - Full adapter implementation

**Game Layer:**
- `game/src/Game/Network/KCPTransportBridge.h` - Bridge registration interface
- `game/src/Game/Network/KCPTransportBridge.cpp` - Bridge implementation

### Key Changes

1. **Macro Change**: Removed `URHO3D_KCP`, now using `__EMSCRIPTEN__` consistently with `ACGame::KCPNetwork`

2. **Factory Pattern**: `TransportFactory::SetKCPFactory()` allows game layer to override default `KCPTransport`

3. **Callback Adapter**: `KCPNetworkAdapter::CallbackAdapter` translates `ACGame::Callback` events to `TransportEvent`

### Usage Example

```cpp
// In game initialization (before network operations)
#include "Game/Network/KCPTransportBridge.h"

void GameApplication::Setup()
{
    // Register ACGame::KCPNetwork as KCP transport
    ACGame::RegisterKCPTransportBridge(context_);
}

// Now engine Network class can use KCP
network->ConnectWithTransport(host, port, scene, TRANSPORT_KCP);
```

---

*Document Version: 1.1*
*Created: 2025-01-XX*
*Updated: 2025-01-XX*
*Status: Implemented*
