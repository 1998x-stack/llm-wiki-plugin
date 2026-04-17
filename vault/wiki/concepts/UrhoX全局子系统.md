---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, Lua, 游戏引擎, API]
aliases: [全局单例, UrhoX全局对象, global subsystems]
relates_to: [UrhoX引擎, UrhoX Lua开发准则, UrhoX音频系统API]
supersedes: null
---
# UrhoX全局子系统

## 概述
[[UrhoX引擎|UrhoX Lua]] API 在全局作用域预注册了18个只读单例对象，覆盖音频、渲染、输入、网络等核心功能，无需声明即可在任意脚本中直接访问。

## 关键内容

### 18个全局单例

| 变量名 | 类型 | 职责 |
|--------|------|------|
| `audio` | Audio* | 音频系统（播放/暂停/音量） |
| `cache` | ResourceCache* | 资源加载与缓存 |
| `console` | Console* | 控制台输入输出 |
| `context` | Context* | 引擎上下文（系统注册中心） |
| `database` | Database* | 数据库访问 |
| `debugHud` | DebugHud* | 调试信息显示（FPS、内存等） |
| `engine` | Engine* | [[UrhoX引擎生命周期API|引擎生命周期]]管理 |
| `eventHandler` | EventHandler* | 当前事件处理器 |
| `eventSender` | EventSender* | 当前事件发送者 |
| `fileSystem` | FileSystem* | 文件系统操作 |
| `graphics` | Graphics* | 图形设备与分辨率查询 |
| `input` | Input* | 键盘/鼠标/触摸输入 |
| `localization` | [[Localization]]* | 多语言本地化 |
| `log` | Log* | 日志系统 |
| `network` | Network* | 网络连接 |
| `renderer` | [[Renderer渲染器|Renderer]]* | 渲染管线与视口 |
| `time` | Time* | 时间与帧率 |
| `ui` | UI* | 原生UI系统（已废弃，见[[UrhoX Lua开发准则]]） |

### 访问方式

每个全局对象同时提供直接变量访问和 Get 函数两种形式：

```lua
-- 直接访问（推荐）
local w = graphics:GetWidth()

-- 等价的函数形式
local w = GetGraphics():GetWidth()
```

### 常用模式

```lua
-- 获取分辨率（SetMode已禁用）
local physW, physH = graphics:GetWidth(), graphics:GetHeight()
local dpr = graphics:GetDPR()

-- 资源加载
local tex = cache:GetResource("Texture2D", "Textures/player.png")

-- 日志输出
log:Write(LOG_INFO, "message")

-- 时间步
-- 通过 Update 事件的 eventData 获取，而非 time 直接调用
```

### 全局变量系统

引擎还提供跨脚本共享的 Variant 键值存储：

```lua
SetGlobalVar("score", Variant(100))
local v = GetGlobalVar("score"):GetInt()
local all = GetGlobalVars()  -- 返回 VariantMap
```

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/globals.md]] — UrhoX Lua API Global Scope 文档

## 相关
- [[UrhoX引擎]] — relates_to，全局子系统是引擎暴露给 Lua 层的接口
- [[UrhoX Lua开发准则]] — relates_to，开发准则规定了分辨率获取、UI系统选择等全局对象使用规范
- [[UrhoX音频系统API]] — relates_to，`audio` 全局对象的详细 API
