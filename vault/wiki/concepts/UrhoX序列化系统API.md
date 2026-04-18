---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["UrhoX", "Lua", "序列化", "二进制IO", "游戏引擎", "游戏开发"]
aliases: [UrhoX Serializer, UrhoX Deserializer, UrhoX二进制序列化]
relates_to: [UrhoX引擎, UrhoX IO系统API, UrhoX数据格式API, UrhoX全局子系统]
supersedes: null
---
# UrhoX序列化系统API

## 概述
[[UrhoX引擎|UrhoX]] 序列化体系由 `Serializer`（写接口）和 `Deserializer`（读接口）两个抽象基类构成，支持基本类型、数学类型、资源引用和 [[Hal Varian|Varian]]t 等引擎内建类型的二进制序列化。

## 关键内容

### Serializer — 写接口
`Serializer` 定义统一的写方法集，被 `File`、`VectorBuffer`、`NamedPipe` 等具体类实现。

支持写入的类型（返回 `bool`，表示成功与否）：

| 类别 | 方法示例 |
|------|---------|
| 整型 | `WriteInt`、`WriteShort`、`WriteByte`、`WriteUInt`、`WriteInt64` |
| 浮点 | `WriteFloat`、`WriteDouble` |
| 数学类型 | `WriteVector2/3/4`、`WriteQuaternion`、`WriteMatrix3/3x4/4`、`WriteColor`、`WriteRect`、`WriteBoundingBox` |
| 字符串 | `WriteString`、`WriteFileID`、`WriteStringHash`、`WriteLine` |
| 压缩 | `WritePackedVector3(maxAbsCoord)`、`WritePackedQuaternion` |
| 引擎类型 | `WriteResourceRef`、`WriteResourceRefList`、`WriteVariant`、`WriteVariantVector`、`WriteVariantMap` |
| 网络 | `WriteVLE`（可变长编码）、`WriteNetID` |

```lua
-- 将游戏数据写入文件
local f = File("save.dat", FILE_WRITE)
f:WriteInt(level)
f:WriteFloat(health)
f:WriteVector3(playerPos)
f:WriteLine(playerName)
f:Close()
```

### Deserializer — 读接口
`Deserializer` 定义统一的读方法集，与 Serializer 对称。提供游标控制和校验：

```lua
-- 游标控制
deserializer:Seek(0)          -- 跳到绝对位置
deserializer:SeekRelative(4)  -- 相对偏移

-- 检查
local pos = deserializer:GetPosition()  -- 当前位置
local size = deserializer:GetSize()     -- 总大小
local done = deserializer:IsEof()       -- 是否结束
```

属性（只读）：`name`、`checksum`、`position`、`size`、`eof`。

读方法命名规律：`ReadInt`、`ReadFloat`、`ReadVector3`、`ReadString`、`Read[[Hal Varian|Varian]]t` 等，与写方法一一对应。

### 设计模式
- `File` 同时继承 Serializer 和 Deserializer，根据打开模式决定可用操作
- `VectorBuffer` 同样双向实现，常用于构建数据包后写入网络或文件
- 所有读方法按值返回，写方法返回 `bool` 指示成功
- `WriteVLE`/`ReadVLE` 用于网络协议的可变长整数，减少带宽占用
- `WritePackedVector3(maxAbsCoord)` 将 Vector3 量化压缩为 uint32，适合网络同步位置数据

### 完整读写循环示例
```lua
-- 写
local buf = VectorBuffer()
buf:WriteInt(42)
buf:WriteVector3(Vector3(1, 2, 3))
buf:WriteString("item_name")

-- 读（需先重置游标）
buf:Seek(0)
local id = buf:ReadInt()          -- 42
local pos = buf:ReadVector3()     -- (1, 2, 3)
local name = buf:ReadString()     -- "item_name"
```

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/io.md]] — UrhoX Lua API 官方文档

## 相关
- [[UrhoX引擎]] — relates_to
- [[UrhoX IO系统API]] — relates_to
- [[UrhoX数据格式API]] — relates_to
- [[UrhoX全局子系统]] — relates_to
