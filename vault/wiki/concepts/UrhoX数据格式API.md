---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["UrhoX", "Lua", "XML", "JSON", "数据格式", "游戏引擎", "游戏开发"]
aliases: [UrhoX XMLFile, UrhoX JSONFile, UrhoX XML JSON API]
relates_to: [UrhoX引擎, UrhoX IO系统API, UrhoX序列化系统API, UrhoX全局子系统]
supersedes: null
---
# UrhoX数据格式API

## 概述
[[UrhoX引擎|UrhoX]] 提供 XML 和 JSON 两套结构化数据格式支持，均继承自 Resource，可通过资源缓存加载，也支持字符串直接解析和文件保存。

## 关键内容

### XMLFile — XML 资源
`XMLFile : Resource` 代表一个 XML 文档，支持从字符串解析、DOM 操作和文件保存。

```lua
-- 从文件加载
local xml = cache:GetResource("XMLFile", "config.xml")

-- 从字符串解析
local xml2 = XMLFile()
xml2:FromString("<root><item name='a'/></root>")

-- 获取根元素
local root = xml:GetRoot("root")

-- 保存
xml:Save("output.xml", "\t")
```

关键方法：`FromString`、`CreateRoot`、`GetOrCreateRoot`、`GetRoot`、`ToString`、`Patch`（XML patch 机制）、`Save`。

### XMLElement — XML 元素操作
`XMLElement` 是轻量值类型（非指针），表示 XML DOM 节点，支持完整的子树遍历和属性读写。

常用操作：
```lua
local item = root:CreateChild("item")
item:SetAttribute("name", "sword")
item:SetInt("damage", 50)
item:SetBool("magic", true)
item:SetVector3("pos", Vector3(1, 2, 3))

-- 遍历子元素
local child = root:GetChild("item")
while child:NotNull() do
    local name = child:GetAttribute("name")
    child = child:GetNext("item")
end
```

支持的类型读写：`Bool`、`Float`、`Double`、`Int`/`UInt`/`Int64`/`UInt64`、`IntRect`、`IntVector2/3`、`Rect`、`Quaternion`、`Vector2/3/4`、`[[矩阵|Matrix]]3/3x4/4`、`Color`、`String`、`[[Hal Varian|Varian]]t`、`ResourceRef`/`ResourceRefList`。

属性（只读）：`null`、`name`、`parent`、`value`、`numAttributes`、`file`。
常量：`XMLElement.EMPTY`（空元素，用于判断是否有效）。

> ⚠️ `IsNull()` / `NotNull()` 用于检查元素是否有效；遍历到末尾时 `GetNext()` 返回空元素。

### JSONFile — JSON 资源
`JSONFile : Resource` 代表一个 JSON 文档。

```lua
local jf = JSONFile()
jf:FromString('{"score": 100, "name": "player1"}')
local root = jf:GetRoot()  -- 返回 JSONValue
local score = root:Get("score"):GetInt()
jf:Save("save.json", "\t")
```

方法：`FromString`、`ToString`、`GetRoot`、`Save`。

### JSONValue — JSON 节点
`JSONValue` 是 JSON 树中的任意节点，支持类型检查、基本类型读写和数组/对象操作。

```lua
local val = JSONValue()
val:SetInt(42)
print(val:IsNumber(), val:GetInt())   -- true   42

-- 数组操作
local arr = JSONValue()
arr:SetArray({})
arr:Push(JSONValue(1.0))
arr:Push(JSONValue("hello"))
print(arr:Size())   -- 2

-- 对象操作
local obj = JSONValue()
obj:SetObject({})
obj:Set("key", JSONValue(true))
print(obj:Contains("key"))   -- true
obj:Erase("key")
```

类型检查：`IsNull`、`IsBool`、`IsNumber`、`IsString`、`IsArray`、`IsObject`。
类型读取：`GetBool`、`GetInt`、`GetUInt`、`GetFloat`、`GetDouble`、`GetString`、`GetArray`、`GetObject`。
类型写入：`SetBool`、`SetInt`、`SetUint`、`SetFloat`、`SetDouble`、`SetString`、`SetArray`、`SetObject`。
Variant 互转：`Set[[Hal Varian|Varian]]t`/`Get[[Hal Varian|Varian]]t`、`Set[[Hal Varian|Varian]]tMap`/`Get[[Hal Varian|Varian]]tMap`。
常量：`JSONValue.EMPTY`、`JSONValue.emptyArray`、`JSONValue.emptyObject`。

> ⚠️ 引擎提供 `File`+JSON 的原生路径，但对于复杂 JSON 操作推荐优先使用 `[[cjson]]`（见 `engine-docs/recipes/json.md`），性能更好且 API 更简洁。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/io.md]] — UrhoX Lua API 官方文档

## 相关
- [[UrhoX引擎]] — relates_to
- [[UrhoX IO系统API]] — relates_to
- [[UrhoX序列化系统API]] — relates_to
- [[UrhoX全局子系统]] — relates_to
