---
summary: "Lua game script file sandbox isolation ensuring per-project savedata directory confinement"
related_paths:
  - engine/Source/Urho3D/LuaScript/**
last_updated: "2026-04-02"
---

# Lua 游戏脚本文件沙箱隔离 — 设计文档

## 目标

UrhoX 是 AIGC 游戏引擎，不同作者的项目运行在同一引擎上。需要实现**项目隔离**：每个项目的文件读写自动限定在各自 `savedata` 目录下，防止项目间数据泄漏/篡改。

## 架构（三文件拆分）

```
EnginePreview.lua
  └─ loadIsolation()
       ├─ Server: require Isolation_Server  ──→ require Isolation_Common
       └─ Client: require Isolation_Client  ──→ require Isolation_Common
```

### 隔离分三层

- **Common** (`Isolation_Common.lua`): 共享规则（globals 移除、os 清理、SystemCommand 移除、Log:Open 屏蔽、NamedPipe 移除）+ helper 函数导出
- **Client** (`Isolation_Client.lua`): 路径重定向到 savedata（File/FileSystem/Image/C++ 写入 API）
- **Server** (`Isolation_Server.lua`): 完全屏蔽所有文件系统访问

## VM 类型识别 (`GetLuaEnvironment()`)

- LuaScript 构造函数注册 `GetLuaEnvironment()` 全局函数（upvalue 闭包，只读）
- 返回整数：0=Runtime, 1=HostSandbox, 2=Editor
- **只有 Runtime (0) 是 game VM**，HostSandbox/Editor 都不是
- 旧二进制没有此函数: server 不隔离，client 保守隔离

### 加载时机

- EnginePreview.lua 末尾加载，在 stub 文件创建之后、游戏脚本之前
- 用 pcall 包裹，加载失败不影响游戏运行

### loadIsolation 逻辑

```lua
local function isGameVM()
    if not GetLuaEnvironment then return nil end
    return GetLuaEnvironment() == LUA_ENV_RUNTIME
end

local function loadIsolation()
    local vm = isGameVM()
    if IsServerMode() then
        if vm then  -- server: 只在确认是 game VM 时隔离
            require('Isolation_Server')
        end
    else
        if vm ~= false then  -- client: game VM 或旧二进制(nil)都隔离
            require('Isolation_Client')
        end
    end
end
```

## Savedata 根目录解析（优先级链）

1. `__SAVEDATA_ROOT__`（C++ 注入）
2. `GetProjectRoot("settings.json")` — 从资源文件系统路径推导项目下载根目录
3. `GetProjectRoot("main.lua")` — 兜底（入口脚本必定存在）
4. `GetUserDocumentsDir()/temp/savedata/<ProjectId>/` — 最终 fallback

### GetProjectRoot 原理

```
cache:GetFile(name) → file:GetName() 得相对路径
  → cache:GetResourceFileName(relative) 得绝对路径
    → match("^(.+)/assets/") 截取项目根
```

- 路径示例: `.../bin/update/tapcode-sce.spark.xd.com/src/p_ssla/savedata/<userId>/`
- 天然受平台项目删除操作管理
- 必须在 block GetResourceFileName/File:GetName 之前调用

### 二级目录（per-user 隔离）

```
SAVEUSERDATA_ROOT = SAVEDATA_ROOT .. userId .. "/"
```

## 隔离覆盖范围

### Common (Isolation_Common.lua) — 加载时自动执行

- **危险全局移除**: io, debug, loadfile, dofile, PackageFile, NamedPipe = nil; package.loaded.io/debug = nil
- **package 清理**: loadlib = nil, cpath = "", C module searchers (loaders[3]/[4]) 移除
- **os 清理**: 只保留 clock/time/date/difftime
- **FileSystem**: SystemCommand/SystemRun/SystemCommandAsync/SystemRunAsync/SystemOpen 移除
- **Log:Open**: 屏蔽（防止日志重定向到任意文件）
- **导出**: Warn, ClassName, BlockMethod, BlockProperty, RemoveMethods

### Client (Isolation_Client.lua)

- **File**: Open/new/new_local/__call 的路径自动解析到 savedata；GetName/name 剥离 SAVEDATA_ROOT 前缀
- **FileSystem**: CreateDir/Delete/Copy/Rename/FileExists/DirExists/ScanDir/GetLastModifiedTime/SetLastModifiedTime 限定 savedata; SetCurrentDir 阻止; 路径 getter（GetProgramDir 等）屏蔽
- **Image**: SavePNG/BMP/TGA/JPG/DDS/WEBP 路径限定 savedata
- **C++ 直接写入 API**: Scene:Save/SaveXML/SaveJSON, JSONFile:Save, XMLFile:Save, Resource:Save, UIElement:SaveXML, Input:SaveGestures/SaveGesture, Graphics:BeginDumpShaders — 路径重定向到 savedata
- **ResourceCache/DownloadManager**: GetResourceDirs/GetResourceFileName/GetDefaultDirectory 屏蔽

### Server (Isolation_Server.lua)

- File/FileSystem/Image 完全屏蔽（返回 false/nil）
- C++ 直接写入 API 完全屏蔽（同上列表）
- FileSystem 路径 getter 完全屏蔽
- ResourceCache/DownloadManager getter 完全屏蔽

### C++ 读取 API — 不处理

Scene:Load/LoadXML 等读取方法在 C++ 中通过 `File(context, path, FILE_READ)` 读取，对于相对路径会搜索 resource directories。wrapping 到 savedata 会破坏正常资源加载，且读取风险低（数据进引擎对象，脚本无法提取原始字节）。

## tolua++ 覆盖机制

### 核心发现

- `tolua_cclass` 将 registry metatable 同时赋给全局类表和实例 metatable → `FileSystem == getmetatable(fileSystem)` 成立
- `rawset(ClassTable, methodName, luaFunc)` 等价于 `rawset(getmetatable(instance), methodName, luaFunc)` — 方法覆盖正确
- `class_index_event` 的 `.get` 表只调 C 函数（`lua_iscfunction` 检查）→ Lua 函数替换 `.get` 条目无效，必须置 nil
- 需要 Lua getter 的属性（如 `file.name`）→ wrap `__index` 拦截 key，class_index_event 内部用 rawget 不会递归

### 四种覆盖模式

| 模式 | helper 函数 | 用途 |
|------|------------|------|
| 路径重定向（单路径） | `WrapPathMethod` | FileSystem/Image/C++ 写入 API |
| 路径重定向（双路径） | `WrapDualPathMethod` | Copy/Rename |
| 方法屏蔽 + 属性清除 | `BlockMethod` | getter 屏蔽、危险方法屏蔽 |
| 方法移除 | `RemoveMethods` | SystemCommand 等直接置 nil |

## 路径安全检测

### 空字节注入防护 (ResolvePath)

- Lua 字符串允许嵌入 `\0`，但 C++ `const char*` 在 `\0` 处截断
- 攻击示例：`"..\0x"` → Lua 检查通过，C++ 截断为 `".."` → 逃逸到父目录
- **ResolvePath 开头检测 `\0` 并拒绝**，在所有其他检查之前

### 路径穿越检测 (ContainsTraversal)

- 只检测 `..` 作为路径组件（`../`, `/../`, `/..`）
- `file..txt` 等合法文件名不受影响

## C++ 方法重载注意

- WrapPathMethod 必须检查 `type(path) ~= "string"` 直通非 string 参数
- 原因：Scene:SaveXML 等有重载（接受 String fileName 或 Serializer& dest）
- 不检查会把 File/Serializer userdata 当路径处理导致崩溃

## WASM 平台文件系统行为

### 双层文件系统架构

| 层 | 技术 | 持久化 | 场景 |
|---|------|--------|------|
| **EMSCRIPTEN_WX** | `window.CE.file` JS API | 取决于宿主 | TapCode/微信小游戏 |
| **Fallback** | Emscripten MEMFS（内存） | 无，刷新即丢 | 普通浏览器 |

- `File.cpp` 先尝试 WXFileHandler，失败回退 MEMFS
- 隔离层在 WASM 下行为与 native 一致（IsAbsolutePath 检测 `/` 前缀）
- Savedata 在 MEMFS 中创建，刷新页面后丢失；EMSCRIPTEN_WX 模式下可能提供宿主级持久化

## 设计原则

- **绝对路径一律拒绝** — 用户不可能知道 SAVEDATA_ROOT，所有路径无脑拼接前缀
- **日志不加 TAG** — 系统自带 VM topic 路由
- **VM 类型是 per lua_State 属性** — 绝不是进程全局静态变量
- **路径穿越检测是必要的** — 防止 `savedata/../../etc/passwd` 逃逸
- **require("io") 防护** — 光 `io = nil` 不够，还需 `package.loaded.io = nil` 防止 require 复活

## 命名规范

- 所有函数（包括 local helper）使用 **PascalCase**，与 Urho3D C++ 风格一致
- 导出 key: `M.Warn`, `M.ClassName`, `M.BlockMethod`, `M.BlockProperty`, `M.RemoveMethods`
- `ClassName()` 使用 `tolua.type(class)` 自动提取类名
- WrapPathMethod/WrapDualPathMethod 内部调用 `ClassName(class)` 生成 tag

## 日志

- 使用 `log:Write(LOG_WARNING, msg)` 而非 `log:Error`（Log 类无 Error 方法）
- 不加 TAG 前缀，日志系统自带 VM topic 路由

## 关键文件

| 文件 | 作用 |
|------|------|
| `engine/bin/Data/LuaScripts/Utilities/Previews/Isolation_Common.lua` | 共享隔离规则 + helper 函数 |
| `engine/bin/Data/LuaScripts/Utilities/Previews/Isolation_Client.lua` | Client 模式沙箱（路径重定向） |
| `engine/bin/Data/LuaScripts/Utilities/Previews/Isolation_Server.lua` | Server 模式完全屏蔽 |
| `engine/bin/Data/LuaScripts/Utilities/EnginePreview.lua` | 加载入口（末尾） |
| `engine/bin/Data/LuaScripts/Tests/test_isolation.lua` | 测试用例 |
| `engine/Source/Urho3D/LuaScript/LuaScript.cpp` | 注册 `GetLuaEnvironment()` |

## TODO

- [ ] Savedata 目录大小限制（防止恶意脚本写满磁盘）
  - 需要在写入时检查目录总大小，超过阈值拒绝写入
  - 阈值待定（建议 50MB~100MB，可配置）
- [ ] ToluaPushVector\<String\> 模板特化在 Linux 服务端未生效
  - **现象**: `cache:GetResourceDirs()` / `fileSystem:ScanDir()` 在 Linux 服务端报 `tolua_pushusertype: unknown type 'String'`，客户端正常
  - **根因**: `ToluaUtils.h:209` 的特化前向声明被 `#ifdef _WIN32` 包裹，Linux 构建看不到声明，编译器在生成的绑定代码中实例化泛型模板而非使用 `ToluaUtils.cpp` 中的特化版本
  - **修复**: 去掉 `#ifdef _WIN32` 守卫，让所有平台都能看到 `ToluaPushVector<String>` 等特化声明
  - **影响**: 沙箱隔离后此 API 被拦截/屏蔽，不影响隔离功能；但未隔离的引擎内部代码（如 HostSandbox）可能触发
