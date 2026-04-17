---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 性能优化, 游戏开发, Lua编程]
aliases: [LuaJIT编译器, Lua JIT, LuaJIT FFI]
relates_to:
  - target: "[[Lua C API 绑定层]]"
    type: extends
    confidence: 0.88
  - target: "[[Lua脚本宿主模式]]"
    type: relates_to
    confidence: 0.8
  - target: "Luau"
    type: relates_to
    confidence: 0.6
supersedes: null
---

# LuaJIT

## 概述
LuaJIT 是 Lua 5.1 的即时编译实现，通过追踪 JIT 将热路径编译为原生机器码，并提供 FFI 库直接调用 C 函数（声明即用，无需手写绑定），性能可接近原生 C。

## 关键内容

### 架构
LuaJIT 包含两个执行层：
- **字节码解释器**：处理冷路径代码，与标准 Lua 兼容
- **Tracing JIT**：识别热路径（循环等），记录执行踪迹并编译为 x86/x64 原生机器码

### FFI 库（外部函数接口）
LuaJIT 的杀手级特性。用 `ffi.cdef...` 声明 C 结构体和函数签名，直接调用原生 C 函数，无需 `lua_pushXXX` / `lua_toXXX` 的手工绑定代码：
- `ffi.new("Vec3", {...})` — 创建栈上 C 值类型（无 GC 压力）
- `ffi.C.function_name(...)` — 调用已声明的 C 函数
- `ffi.new("Type[N]")` — 分配 C 数组，直接内存操作

FFI 调用速度接近 C 直接调用，远快于通过 Lua 栈的标准 C API 绑定。

### 性能最佳实践
- **局部化全局访问**：`local math_sin = math.sin`，避免每次访问全局表
- **预分配表**：`for i=1,N do t[i]=0 end` 避免动态扩展哈希
- **避免热路径闭包**：排序比较函数应定义为模块级 local 函数，不要每次调用时创建匿名函数
- **字符串拼接用 table.concat**：避免大量 `..` 操作产生中间字符串
- **整数运算优先**：LuaJIT 整数比浮点快，位操作用 `bit` 库

### 与标准 Lua 的差异
LuaJIT 基于 Lua **5.1** 标准（不是 5.4），不支持 5.2+ 的 `_ENV`、5.4 的整数类型和分代 GC 等特性。使用 LuaJIT 需注意 API 兼容性。

### 应用场景
适合性能敏感的大型游戏引擎（需要高频 Lua-C 交互）和需要零成本 C 库访问的场景；在 iOS 等禁止 JIT 的平台需回退到解释模式。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，第6节 LuaJIT 架构、FFI 示例与性能最佳实践

## 相关
- [[Lua C API 绑定层]] — LuaJIT FFI 是传统 C API 绑定层的高性能替代方案
- [[Lua脚本宿主模式]] — LuaJIT 作为 VM 层选型，影响整个绑定层策略
- Luau — Roblox 定制 Lua 方言，有类似的 Native codegen 方向
