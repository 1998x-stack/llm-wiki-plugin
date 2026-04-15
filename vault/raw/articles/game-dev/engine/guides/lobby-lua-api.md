---
summary: "AI-coding-friendly Lobby Lua API reference for multiplayer lobby functionality"
last_updated: "2026-04-02"
---

# Lobby Lua API

AI Coding 友好的大厅 Lua API 文档。

## 目录

- [快速开始](#快速开始)
- [API 概览](#api-概览)
- [协议与格式要求](#协议与格式要求)
- [用户信息 API](#用户信息)
- [房间操作 API](#房间操作)
- [游戏 API](#游戏)
- [匹配 API](#匹配)
- [事件系统](#事件系统)
- [完整示例](#完整示例)
- [错误处理](#错误处理)

---

## 快速开始

```lua
-- 检查在线状态
if lobby:IsOnline() then
    -- 创建房间（必须包含 map_name 和 mode_id）
    local roomData = cmsg_pack.pack({
        map_name = "p_ogma",
        mode_id = "pvp"
    })
    lobby:CreateRoom({
        maxPlayers = 4,
        roomData = roomData
    })
end

-- 订阅服务器响应事件
SubscribeToEvent("LobbyResponse", function(eventType, eventData)
    local success = eventData["Success"]:GetBool()
    if success then
        print("操作成功！")
    end
end)
```

---

## API 概览

| 方法 | 说明 | 协议 |
|------|------|------|
| `GetMyUserId()` | 获取当前用户ID | - |
| `GetMyLoginId()` | 获取当前登录ID | - |
| `IsOnline()` | 是否已连接服务器 | - |
| `IsInLobby()` | 是否在大厅中 | - |
| `IsInGame()` | 是否在游戏中 | - |
| `IsGuestUser()` | 是否游客登录 | - |
| `CreateRoom(options)` | 创建房间 | `REQUEST_TEAM_CREATE` (0x3001) |
| `JoinRoom(options)` | 加入房间 | `REQUEST_TEAM_APPLY_JOIN` (0x300B) |
| `LeaveRoom()` | 离开房间 | `REQUEST_TEAM_LEAVE` (0x3005) |
| `GetRoomList(options)` | 获取房间列表 | `REQUEST_TEAM_LIST` (0x3013) |
| `GetRoomInfo(roomId)` | 获取房间信息 | `REQUEST_TEAM_INFO` (0x3015) |
| `StartGame(options)` | 开始游戏 | `REQUEST_MATCH_START` (0x3080) |
| `FindMatch(options)` | 开始匹配 | `REQUEST_MATCH_START` (0x3080) |
| `CancelMatch()` | 取消匹配 | `REQUEST_MATCH_CANCEL` (0x3081) |

---

## 协议与格式要求

### ⚠️ 重要：字段格式说明

| 字段 | 格式 | 使用场景 | 示例 |
|------|------|----------|------|
| `roomData` | **MsgPack** | CreateRoom | `cmsg_pack.pack({map_name="xxx", mode_id="xxx"})` |
| `matchInfo` | **JSON 字符串** | StartGame/FindMatch | `'{"mode":"pvp","immediately_start":true}'` |
| `modeArgs` | **JSON 字符串** | StartGame/FindMatch | `'{"difficulty":"hard"}'` |

### roomData 必填字段

创建房间时，`roomData` **必须包含**以下字段，否则服务器会报错：

```lua
{
    map_name = "地图名称",  -- 必填！
    mode_id = "游戏模式"    -- 必填！注意是 mode_id 不是 mode
}
```

### matchInfo 格式

开始游戏/匹配时，`matchInfo` 必须是 **JSON 字符串**（不是 MsgPack！）：

```lua
-- ✅ 正确
local matchInfo = '{"mode":"pvp","immediately_start":true}'

-- ❌ 错误（会导致服务器 JSON 解析失败）
local matchInfo = cmsg_pack.pack({mode = "pvp"})
```

---

## 用户信息

### lobby:GetMyUserId()

获取当前登录用户的ID。

```lua
local userId = lobby:GetMyUserId()
print("我的用户ID:", userId)
```

### lobby:GetMyLoginId()

获取当前登录会话ID。

```lua
local loginId = lobby:GetMyLoginId()
print("登录ID:", loginId)
```

### lobby:IsOnline()

检查是否已连接到服务器。

```lua
if lobby:IsOnline() then
    print("已连接")
end
```

### lobby:IsInLobby()

检查是否在大厅中（未进入游戏）。

```lua
if lobby:IsInLobby() then
    print("在大厅中，可以创建或加入房间")
end
```

### lobby:IsInGame()

检查是否在游戏中。

```lua
if lobby:IsInGame() then
    print("游戏进行中")
end
```

### lobby:IsGuestUser()

检查是否为游客登录。

```lua
if lobby:IsGuestUser() then
    print("当前为游客模式")
end
```

---

## 房间操作

### lobby:CreateRoom(options)

创建一个新房间。使用 `REQUEST_TEAM_CREATE` (0x3001) 协议。

**参数 options:**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| maxPlayers | number | 4 | 最大玩家数 |
| roomData | string | "" | 房间自定义数据（**MsgPack 编码**） |
| isPrivate | boolean | false | 是否私密房间 |
| password | string | "" | 房间密码 |

**roomData 必填字段:**

```lua
{
    map_name = "p_ogma",  -- 必填！地图名称
    mode_id = "pvp"       -- 必填！游戏模式ID
}
```

**示例:**

```lua
-- 创建4人公开房间
local roomData = cmsg_pack.pack({
    map_name = "p_ogma",
    mode_id = "pvp"
})
local requestId = lobby:CreateRoom({
    maxPlayers = 4,
    roomData = roomData
})

-- 创建私密房间
local roomData = cmsg_pack.pack({
    map_name = "arena",
    mode_id = "1v1"
})
lobby:CreateRoom({
    maxPlayers = 2,
    isPrivate = true,
    password = "123456",
    roomData = roomData
})

-- 简化调用（只指定人数，roomData为空）
-- ⚠️ 注意：简化调用时 roomData 为空，可能导致服务器报错！
lobby:CreateRoom(4)
```

### lobby:JoinRoom(options)

加入指定房间。使用 `REQUEST_TEAM_APPLY_JOIN` (0x300B) 协议。

**参数 options:**

| 字段 | 类型 | 说明 |
|------|------|------|
| roomId | number | 房间ID（必填） |
| ownerId | number | 房主用户ID（可选） |
| password | string | 密码（可选） |

**示例:**

```lua
-- 加入房间
lobby:JoinRoom({ roomId = 12345 })

-- 加入私密房间
lobby:JoinRoom({
    roomId = 12345,
    password = "123456"
})

-- 简化调用
lobby:JoinRoom(12345)  -- 直接传房间ID
```

### lobby:LeaveRoom()

离开当前房间。使用 `REQUEST_TEAM_LEAVE` (0x3005) 协议。

```lua
local requestId = lobby:LeaveRoom()
```

### lobby:GetRoomList(options)

获取可用房间列表。使用 `REQUEST_TEAM_LIST` (0x3013) 协议。

**参数 options:**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| mapName | string | "" | 按地图名过滤 |
| modes | table | {} | 按模式过滤 |
| limit | number | 10 | 返回数量限制 |
| includePrivate | boolean | false | 是否包含私密房间 |

**示例:**

```lua
-- 获取所有房间
lobby:GetRoomList({})

-- 获取指定地图的房间
lobby:GetRoomList({
    mapName = "p_ogma",
    limit = 20
})
```

### lobby:GetRoomInfo(roomId)

获取指定房间的详细信息。使用 `REQUEST_TEAM_INFO` (0x3015) 协议。

```lua
lobby:GetRoomInfo(12345)
```

---

## 游戏

### lobby:StartGame(options)

开始游戏。使用 `REQUEST_MATCH_START` (0x3080) 协议。

> ⚠️ 注意：之前的 `REQUEST_TEAM_START_GAME` (0x3086) 协议已废弃，服务器不支持！

**参数 options:**

| 字段 | 类型 | 说明 |
|------|------|------|
| mapName | string | 地图名称（必填） |
| matchInfo | string | 匹配信息（**JSON 字符串**，必填） |
| modeArgs | string | 模式参数（JSON 字符串，可选） |
| players | table | 组队玩家ID列表（可选） |
| regions | table | 区域列表（可选） |
| tag | string | 环境标签（可选） |

**matchInfo 格式（JSON 字符串）:**

```lua
'{"mode":"pvp","immediately_start":true}'
```

**示例:**

```lua
-- 完整参数
local requestId = lobby:StartGame({
    mapName = "p_ogma",
    matchInfo = '{"mode":"pvp","immediately_start":true}',
    modeArgs = '{"difficulty":"hard"}',
    regions = {"cn-east", "cn-north"}
})

-- 简化调用（只传地图名）
lobby:StartGame("p_ogma")
```

---

## 匹配

### lobby:FindMatch(options)

开始自动匹配。使用 `REQUEST_MATCH_START` (0x3080) 协议。

**参数 options:**

| 字段 | 类型 | 说明 |
|------|------|------|
| mapName | string | 地图名称（必填） |
| matchInfo | string | 匹配信息（**JSON 字符串**） |
| modeArgs | string | 模式参数（可选） |
| players | table | 组队玩家ID列表（可选） |
| regions | table | 区域列表（可选） |
| tag | string | 环境标签（可选） |

**示例:**

```lua
-- 单人匹配
lobby:FindMatch({
    mapName = "p_ogma",
    matchInfo = '{"mode":"pvp"}'
})

-- 组队匹配
lobby:FindMatch({
    mapName = "p_ogma",
    players = {userId1, userId2},
    matchInfo = '{"skill":1500}'
})

-- 简化调用
lobby:FindMatch("p_ogma")
```

### lobby:CancelMatch()

取消正在进行的匹配。使用 `REQUEST_MATCH_CANCEL` (0x3081) 协议。

```lua
lobby:CancelMatch()
```

---

## 事件系统

### 订阅响应事件

所有异步操作的结果通过 `LobbyResponse` 事件返回：

```lua
SubscribeToEvent("LobbyResponse", "HandleLobbyResponse")

function HandleLobbyResponse(eventType, eventData)
    local respType = eventData["Type"]:GetInt()
    local requestId = eventData["RequestId"]:GetInt()
    local success = eventData["Success"]:GetBool()
    local errorCode = eventData["ErrorCode"]:GetInt()
    local data = eventData["Data"]:GetString()
    
    if success then
        print("操作成功! RequestId:", requestId)
    else
        print("操作失败! ErrorCode:", errorCode)
    end
end
```

### 响应类型常量

| 类型值 | 名称 | 说明 |
|--------|------|------|
| 1 | CREATE_ROOM | 创建房间响应 |
| 2 | JOIN_ROOM | 加入房间响应 |
| 3 | LEAVE_ROOM | 离开房间响应 |
| 4 | START_GAME | 开始游戏响应 |
| 5 | ROOM_LIST | 房间列表响应 |

### 响应数据

| 字段 | 类型 | 说明 |
|------|------|------|
| Type | int | 响应类型（见上表） |
| RequestId | int | 请求ID |
| Success | bool | 是否成功 |
| ErrorCode | int | 错误码（失败时） |
| Data | string | 额外数据（如房间ID） |

---

## 完整示例

```lua
-- ============================================
-- 游戏大厅完整流程示例
-- ============================================

-- 响应类型常量
local ResponseType = {
    CREATE_ROOM = 1,
    JOIN_ROOM = 2,
    LEAVE_ROOM = 3,
    START_GAME = 4,
    ROOM_LIST = 5,
}

local currentRoomId = nil

-- 处理服务器响应
function HandleLobbyResponse(eventType, eventData)
    local respType = eventData["Type"]:GetInt()
    local success = eventData["Success"]:GetBool()
    local errorCode = eventData["ErrorCode"]:GetInt()
    local data = eventData["Data"]:GetString()
    
    if respType == ResponseType.CREATE_ROOM then
        if success then
            currentRoomId = tonumber(data)
            print("房间创建成功! 房间ID:", currentRoomId)
        else
            print("房间创建失败! 错误码:", errorCode)
        end
    elseif respType == ResponseType.START_GAME then
        if success then
            print("游戏开始!")
        else
            print("开始游戏失败! 错误码:", errorCode)
        end
    end
end

-- 初始化
function Start()
    -- 订阅事件
    SubscribeToEvent("LobbyResponse", "HandleLobbyResponse")
    
    -- 检查连接
    if not lobby:IsOnline() then
        print("未连接到服务器")
        return
    end
    
    print("当前用户ID:", lobby:GetMyUserId())
end

-- 创建房间
function CreateRoom()
    local roomData = cmsg_pack.pack({
        map_name = "p_ogma",
        mode_id = "pvp"
    })
    
    local requestId = lobby:CreateRoom({
        maxPlayers = 4,
        roomData = roomData,
        isPrivate = false
    })
    
    print("创建房间请求已发送, RequestId:", requestId)
end

-- 开始游戏（房主调用）
function StartGame()
    if not currentRoomId then
        print("请先创建或加入房间")
        return
    end
    
    local requestId = lobby:StartGame({
        mapName = "p_ogma",
        matchInfo = '{"mode":"pvp","immediately_start":true}',
        regions = {"cn-east"}
    })
    
    print("开始游戏请求已发送, RequestId:", requestId)
end

-- 快速匹配
function QuickMatch()
    lobby:FindMatch({
        mapName = "p_ogma",
        matchInfo = '{"mode":"pvp"}'
    })
end
```

---

## 错误处理

### 返回值说明

所有异步操作返回 `requestId`：
- `requestId > 0`: 请求已发送，等待服务器响应
- `requestId == -1`: 请求失败（未连接或参数错误）

```lua
local requestId = lobby:CreateRoom({...})
if requestId == -1 then
    print("请求发送失败，请检查连接状态")
else
    print("请求已发送，等待响应...")
end
```

### 常见错误

| 错误现象 | 原因 | 解决方案 |
|----------|------|----------|
| `TypeError: Cannot read properties of undefined` | `roomData` 缺少必填字段 | 确保包含 `map_name` 和 `mode_id` |
| `is not valid JSON` | `matchInfo` 使用了 MsgPack 格式 | 改用 JSON 字符串 |
| 字段名不匹配 | 使用了 `mode` 而不是 `mode_id` | 检查字段名 |
| 请求无响应 | 未正确设置 `deviceType` 或 `GameFlag` | 检查登录流程 |

---

## 协议参考

### 已支持的协议

| 协议名 | 协议号 | Lua API |
|--------|--------|---------|
| REQUEST_TEAM_CREATE | 0x3001 | `CreateRoom()` |
| REQUEST_TEAM_LEAVE | 0x3005 | `LeaveRoom()` |
| REQUEST_TEAM_APPLY_JOIN | 0x300B | `JoinRoom()` |
| REQUEST_TEAM_LIST | 0x3013 | `GetRoomList()` |
| REQUEST_TEAM_INFO | 0x3015 | `GetRoomInfo()` |
| REQUEST_MATCH_START | 0x3080 | `StartGame()` / `FindMatch()` |
| REQUEST_MATCH_CANCEL | 0x3081 | `CancelMatch()` |

### 已废弃的协议

| 协议名 | 协议号 | 说明 |
|--------|--------|------|
| REQUEST_TEAM_START_GAME | 0x3086 | ❌ 服务器不支持，请使用 `REQUEST_MATCH_START` |

---

## 更新日志

- **2025-12-19**: 
  - `StartGame()` 改用 `REQUEST_MATCH_START` 协议
  - 删除 `REQUEST_TEAM_START_GAME` 相关代码
  - 添加事件系统支持
  - 明确 `matchInfo` 必须是 JSON 格式，`roomData` 必须是 MsgPack 格式
  - 添加 `mode_id` 字段要求（不是 `mode`）

