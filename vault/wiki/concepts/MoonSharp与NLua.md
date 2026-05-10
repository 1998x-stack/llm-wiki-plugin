---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, Unity, C#, Lua编程]
aliases: [MoonSharp, NLua, Unity Lua集成, C# Lua桥]
relates_to:
  - target: "[[Lua C API 绑定层]]"
    type: extends
    confidence: 0.85
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.9
  - target: "[[游戏引擎架构]]"
    type: relates_to
    confidence: 0.75
supersedes: null
---
# MoonSharp 与 NLua

## 概述
[[MoonSharp]] 和 NLua 是两种在 Unity（及任意 .NET 项目）中嵌入 Lua 脚本的主流桥接库，前者为纯 C# 实现，后者基于原生 Lua C 库，两者均提供 C# 对象注入、函数互调和返回值获取机制。

## 关键内容

### MoonSharp：纯 C# Lua 解释器
[[MoonSharp]] 是完全用 C# 实现的 Lua 5.2 解释器，无原生 DLL 依赖，适合 IL2CPP/AOT 平台（iOS 等）。

**对象注册流程**：
1. 在 C# 类上[[标注]] `[MoonSharpUserData]`，通过 `UserData.RegisterAssembly()` 批量注册
2. `script.Globals["key"] = obj` 将 C# 对象注入 Lua 全局变量
3. 静态类通过 `UserData.Create(typeof(SomeClass))` 包装后注入

**调用机制**：
- `script.DoString(code)` / `script.DoFile(path)` 执行 Lua 代码
- `DynValue fn = script.Globals.Get("update"); script.Call(fn, arg)` 调用 Lua 函数
- `DynValue result = script.DoString("return 1+2"); float val = (float)result.Number` 获取返回值

**类型系统**：DynValue 是 [[MoonSharp]] 的通用值容器，通过 `.Number`、`.String`、`.Table`、`.Function` 等属性读取具体类型。

### NLua：原生 Lua C 库绑定
NLua 基于 KeraLua 封装原生 Lua 5.4（通过 P/Invoke），性能接近原生但需平台原生 DLL。

```csharp
var lua = new Lua();
lua["myObj"] = new MyClass();                            // 注入对象
lua.RegisterFunction("log", typeof(Debug).GetMethod("Log", ...));  // 注册函数
lua.DoString("myObj:Method()");                          // 执行
var result = lua["my_variable"];                         // 读取全局变量
var table = lua.GetTable("my_table");                    // 读取表
```

### 方案对比

| 维度 | [[MoonSharp]] | NLua |
|------|-----------|------|
| 实现方式 | 纯 C# Lua 解释器 | 原生 Lua C 库 P/Invoke |
| AOT/IL2CPP 兼容 | 好（无原生依赖） | 需平台 native DLL |
| 性能 | 略低于原生 | 接近原生 Lua |
| API 风格 | DynValue 类型系统，强类型感 | 动态类型，接近原始 [[Lua C API 绑定层|Lua C API]] |
| 适用场景 | Unity iOS/IL2CPP、跨平台 .NET | Windows/Android 性能优先场景 |

### 与 xLua/tolua 的区别
[[MoonSharp]]/NLua 是**通用 .NET Lua 桥**，适合任意 .NET 项目。xLua/[[Lua脚本宿主模式|tolua]]# 是**Unity 专用桥**，深度集成 Unity 组件生命周期、MonoBehaviour 和 IL2CPP 热补丁机制，工程化程度更高。

## 来源
- [[engine-integration]] — 游戏引擎集成参考文档，Unity MoonSharp/NLua 集成示例代码段

## 相关
- [[Lua C API 绑定层]] — NLua 通过 KeraLua 封装 C API；MoonSharp 则完全绕过 C API
- [[Lua脚本宿主模式]] — MoonSharp/NLua 是 .NET 宿主环境下的 Lua 嵌入方案
- [[游戏引擎架构]] — Unity + Lua 脚本通过此类桥实现 Scripting 层
