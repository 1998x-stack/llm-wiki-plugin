---
type: entity
status: active
confidence: 0.87
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具与框架, 游戏, 游戏开发]
aliases: [Roblox Studio, Roblox平台]
relates_to:
  - target: "[[Luau]]"
    type: uses
    confidence: 0.98
  - target: "[[Lua沙盒系统]]"
    type: implements
    confidence: 0.9
  - target: "[[游戏引擎架构]]"
    type: implements
    confidence: 0.8
supersedes: null
entity_type: tool
---

# Roblox

## 概述
Roblox 是面向用户自创游戏的在线游戏平台，使用 [[Luau]]（Lua 5.1 的 Roblox 扩展方言）作为脚本语言，采用严格的服务端/客户端分离架构和 RemoteEvent 通信机制。

## 关键内容

1. **服务端/客户端分离架构**：
   - `ServerScriptService/` — 仅服务端执行，处理权威逻辑
   - `StarterPlayer/StarterPlayerScripts/` — 仅客户端执行，处理 UI 和本地效果
   - `ReplicatedStorage/` — 服务端+客户端共享，存放通用代码和 RemoteEvent
   - `Workspace/` — 3D 场景和游戏对象

2. **RemoteEvent 通信**：客户端与服务端之间通过 RemoteEvent/RemoteFunction 通信。服务端必须验证客户端数据，永远不信任客户端传入的数值（反作弊关键）。`OnServerEvent:Connect(player, ...)` 处理客户端触发，`FireServer(...)` 从客户端发起。

3. **[[Luau]] 类型系统**：在标准 Lua 上新增可选静态类型注解（`local x: number`）、联合类型（`"idle" | "running"`）、泛型（`Array<T>`）等。类型检查在 Studio 编辑阶段运行，运行时仍为动态类型。

4. **安全沙盒**：Roblox 对玩家自编写脚本实施严格沙盒，禁止访问文件系统、网络库等，防止用户脚本滥用平台资源。

5. **实例系统**：游戏对象以 Instance 层级组织，通过 `game:GetService("Players")`、`Instance.new("RemoteEvent")` 等 API 操作，`FindFirstChild`、`WaitForChild` 是常用安全访问模式。

6. **DataStore 持久化**：`DataStoreService:GetDataStore("name")` 获取持久化存储，`SetAsync(key, data)` 写入，`GetAsync(key)` 读取，均需 `pcall` 包裹防错。`UpdateAsync(key, fn)` 提供原子读-改-写操作，是防止并发写入冲突的推荐方式。

7. **RemoteFunction 双向调用**：`RemoteFunction.OnServerInvoke` 设置服务端处理函数，客户端调用 `rf:InvokeServer(data)` 阻塞等待返回值。适合需要确认响应的场景（如购买请求），但阻塞特性需注意超时风险。

8. **RunService 环境检测**：`RunService:IsServer()` / `IsClient()` / `IsStudio()` 在运行时判断当前执行环境，用于编写服务端/客户端通用代码，是防止逻辑错位执行的常用守卫模式。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，分析 Roblox/Luau 架构、RemoteEvent 通信与类型系统

## 相关
- [[Luau]] — Roblox 定制的类型化 Lua 方言
- [[Lua沙盒系统]] — Roblox 对用户脚本实施严格沙盒执行环境
- [[游戏引擎架构]] — Roblox 是 Luau 优先的闭环平台
