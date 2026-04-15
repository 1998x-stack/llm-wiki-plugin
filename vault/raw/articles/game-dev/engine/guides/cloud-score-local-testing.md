---
summary: "How to locally test clientCloud cloud variables and leaderboard API on Windows"
last_updated: "2026-04-02"
---

# 云变量/排行榜本地测试

本文档介绍如何在 **Windows 本地** 测试 `clientCloud` 云变量和排行榜 API。

## 背景：为什么需要传入项目 ID？

`clientCloud` API 底层通过 `Score::GetMapName()` 获取当前项目的 **Game ID**（即项目 ID），用来标识云端数据所属的"地图/项目"。数据的存取链路为：

```
clientCloud:SetInt("score", 100)
    → Score::GetMapName()          -- 获取项目 ID
    → CEGlobal::GetGameID()        -- 底层实现
        → 非 Tapcode 环境: AppArgs::GetArgsValue("game")  -- 从命令行参数 -game= 获取
        → Tapcode 环境:    从 JS 接口或命令行参数获取
    → 发送到云端 Entrance 服务
```

**如果不传入 `-game=` 参数，`GetGameID()` 返回空字符串，云端无法识别数据归属，所有存取操作都会失败。**

## 启动方式

在命令行中通过 `-game=<项目ID>` 传入一个合法的项目 ID：

```bash
UrhoXRuntime.exe <你的脚本>.lua -game=<项目ID>
```

**项目 ID** 即 `.project/project.json` 中的 `project_id` 字段（由 SCE 平台分配的唯一标识）。

**示例**:
```bash
# 使用一个已有的项目 ID
UrhoXRuntime.exe 100_LeaderboardMultiFieldTest.lua -game=p_abc123def456

# 或使用已部署项目的 game_url 作为标识（Tapcode 环境）
UrhoXRuntime.exe 100_LeaderboardMultiFieldTest.lua -game=fcb07ed0-854a-4c5a-9b32-9449e150c2a7
```

## 前置条件

云变量/排行榜正常工作需要以下条件全部满足：

| 条件 | 说明 | 如何满足 |
|------|------|---------|
| **项目 ID** | 标识数据所属的项目 | 命令行 `-game=<项目ID>` |
| **用户 ID** | 标识数据所属的玩家 | 需要登录流程（Entrance 连接） |
| **网络连接** | Score 底层通过 Entrance 通信 | 需要连接到 Entrance 服务 |

> ⚠️ **仅传入 `-game=` 不足以让排行榜完全工作**，还需要有效的登录和网络连接。
> 最可靠的方式是使用 **Tapcode 本地调试流程**（通过 `-tapcode_dir` + `-game_url` 启动），
> 这样 `project_id`、`userId`、网络连接都会自动就绪。

## 常见问题

| 症状 | 原因 | 解决方案 |
|------|------|---------|
| 回调不触发 / error 回调报错 | 未传入 `-game=` | 添加 `-game=<项目ID>` 参数 |
| `clientCloud.mapName` 为空 | 同上 | 同上 |
| `clientCloud.userId` 为 0 | 未完成登录 | 通过 Tapcode 调试流程启动（包含登录） |
| 写入成功但排行榜读不到数据 | 不同的 `-game=` 值 | 确保每次启动使用相同的项目 ID |

## 验证方法

在 Lua 脚本中打印确认：

```lua
print("mapName:", clientCloud.mapName)   -- 应输出你传入的 -game= 值
print("userId:", clientCloud.userId)     -- 应输出有效的用户 ID (非 0)
```
