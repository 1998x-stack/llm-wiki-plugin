---
type: entity
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具与框架, 游戏, Lua编程]
aliases: [MoonSharp Lua, NLua, Unity Lua]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.9
  - target: "[[Lua C API 绑定层]]"
    type: relates_to
    confidence: 0.7
  - target: "[[游戏引擎架构]]"
    type: implements
    confidence: 0.75
supersedes: null
entity_type: tool
---

# MoonSharp

## 概述
MoonSharp 是纯 C# 实现的 Lua 解释器，用于在 Unity 等 .NET 环境中嵌入 Lua 脚本，通过 `[MoonSharpUserData]` 特性自动将 C# 类型暴露给 Lua，无需手写 C API 绑定。

## 关键内容

1. **纯 C# 实现**：MoonSharp 不依赖原生 Lua C 库，完全用 C# 编写，可在 Unity IL2[[C++|CPP]] 等受限环境运行，无平台适配问题。

2. **`[MoonSharpUserData]` 特性**：标记 C# 类后，`UserData.RegisterType<T>()` 将其注册为 Lua 可用类型。Lua 侧可调用所有公开方法和属性，方法名映射保持不变。

3. **脚本对象模型**：`Script` 类是 Lua 状态机对象，`Script.Globals["name"] = value` 向 Lua 注入全局变量。`DoString(code)` 执行脚本，`Globals.Get("func")` 获取 Lua 函数引用，`script.Call(func, args)` 调用。

4. **函数引用缓存**：可将 `DynValue`（Lua 函数的 C# 表示）缓存，避免每帧查全局表。`DynValue.Nil` 检查函数是否存在。

5. **Unity 集成模式**：通常在 `MonoBehaviour.Start()` 初始化 `Script`，在 `Update()` 调用 Lua `update` 函数，通过代理类（EntityProxy 等）将 GameObject 能力暴露给 Lua，实现 AI 行为脚本化。

6. **与 [[MoonSharp与NLua|NLua]] 对比**：[[MoonSharp与NLua|NLua]] 是另一种 Unity Lua 方案，基于原生 Lua C 库的 .NET 绑定（需平台原生库）；MoonSharp 纯 C# 更安全但性能略低。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，Unity via MoonSharp/NLua 集成模式与代码示例分析

## 相关
- [[Lua脚本宿主模式]] — MoonSharp 是 Unity C# 项目嵌入 Lua 的主流方案之一
- [[Lua C API 绑定层]] — MoonSharp 用 C# 层模拟了 C API 的对象桥功能
- [[游戏引擎架构]] — 代表 "C# 引擎 + Lua 解释" 的双语言架构模式
