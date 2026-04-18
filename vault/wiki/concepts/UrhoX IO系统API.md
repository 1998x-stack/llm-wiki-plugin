---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["UrhoX", "Lua", "IO", "文件系统", "游戏引擎", "游戏开发"]
aliases: [UrhoX文件IO, UrhoX FileSystem, UrhoX File API]
relates_to: [UrhoX引擎, UrhoX Lua开发准则, UrhoX全局子系统, UrhoX序列化系统API, UrhoX数据格式API]
supersedes: null
---
# UrhoX IO系统API

## 概述
[[UrhoX引擎|UrhoX Lua]] IO 系统提供文件读写、虚拟文件系统（VFS）打包、内存缓冲区、命名管道等能力，核心类均继承自 Object 或 Deserializer/Serializer 接口。

## 关键内容

### File — 文件读写
`File : Object` 支持普通文件和 PackageFile 内资源的读写，以 `FileMode`（`FILE_READ` / `FILE_WRITE` / `FILE_READWRITE`）控制模式。

常用操作：
```lua
local f = File("data/config.bin", FILE_READ)
local value = f:ReadInt()
f:Close()

local out = File("output.txt", FILE_WRITE)
out:WriteLine("hello world")
out:Close()
```

关键方法：`Open`、`Close`、`Flush`、`Seek`/`SeekRelative`、`Read`（返回 VectorBuffer）、`IsEof`、`IsPackaged`。

属性（均只读）：`mode`、`open`、`packaged`、`name`、`checksum`、`position`、`size`、`eof`。

### FileSystem — 文件系统操作
`FileSystem : Object` 暴露为全局子系统 `fileSystem`，提供目录管理、文件操作、系统命令执行等功能。

```lua
-- 检查文件是否存在
if fileSystem:FileExists("saves/slot1.dat") then ... end

-- 创建目录
fileSystem:CreateDir("saves/")

-- 扫描目录
local files = fileSystem:ScanDir("assets/", "*.png", SCAN_FILES, false)
```

常用方法：`FileExists`、`DirExists`、`CreateDir`、`Copy`、`Rename`、`Delete`、`ScanDir`、`GetCurrentDir`、`GetProgramDir`、`GetUserDocumentsDir`、`GetAppPreferencesDir`、`SystemCommand`/`SystemRun`（同步执行外部命令）。

> ⚠️ 引擎沙箱限制：不能用标准 Lua `io` 库，必须用 `File` 和 `FileSystem`。相对路径以沙箱工作目录为根。

### VectorBuffer — 内存缓冲区
`VectorBuffer` 同时实现 Serializer 和 Deserializer，用于在内存中构建或解析二进制数据块，可与 File 互转：

```lua
local buf = VectorBuffer()
buf:WriteInt(42)
buf:WriteString("test")
-- 重置游标
buf:Seek(0)
local n = buf:ReadInt()  -- 42
```

### NamedPipe — 命名管道
`NamedPipe : Object` 支持进程间通信（IPC），以服务端/客户端模式打开：

```lua
local pipe = NamedPipe("mypipe", true)  -- isServer=true
if pipe:IsOpen() then
    pipe:WriteString("data")
end
```

属性：`name`、`open`、`eof`（均只读）。

### PackageFile — VFS 打包资源
`PackageFile : Object` 表示引擎打包格式（`.pak`），用于将多个文件打包为单一资源包，支持压缩。

```lua
local pkg = PackageFile("data.pak")
if pkg:Exists("textures/hero.png") then
    local entry = pkg:GetEntry("textures/hero.png")
    -- entry.offset, entry.size, entry.checksum
end
```

属性：`name`、`numFiles`、`totalSize`、`totalDataSize`、`checksum`、`compressed`。

`PackageEntry` 为轻量值类型，包含 `offset`、`size`、`checksum`。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/io.md]] — UrhoX Lua API 官方文档

## 相关
- [[UrhoX引擎]] — relates_to
- [[UrhoX Lua开发准则]] — relates_to
- [[UrhoX全局子系统]] — relates_to
- [[UrhoX序列化系统API]] — relates_to
- [[UrhoX数据格式API]] — relates_to
