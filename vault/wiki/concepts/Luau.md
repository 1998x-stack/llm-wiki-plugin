---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [技术, Lua, 编程语言, 游戏开发]
aliases: [Luau类型系统, Roblox Lua, 类型化Lua]
relates_to:
  - target: "[[Roblox]]"
    type: implements
    confidence: 0.98
  - target: "[[LuaJIT]]"
    type: relates_to
    confidence: 0.55
  - target: "[[Lua C API 绑定层]]"
    type: extends
    confidence: 0.7
  - target: "[[Roblox API]]"
    type: relates_to
    confidence: 0.9
supersedes: null
---

# Luau

## 概述
Luau 是 [[Roblox]] 对 Lua 5.1 的方言扩展，增加了渐进式可选静态类型系统、泛型、联合类型，并通过本地字节码编译和 Native codegen（实验性）提升运行时性能，同时维持与 Lua 5.1 的语法兼容。

## 关键内容

### 类型系统
Luau 引入可选静态类型注解，类型检查在编辑器阶段（[[Roblox|Roblox Studio]]）运行，运行时仍为动态类型：
- **基础注解**：`local x: number = 42`、`local name: string`、`local b: boolean`
- **可选类型**：`local maybe: string?` 等价于 `string | nil`
- **函数类型**：`local fn: (number, string) -> boolean`
- **联合/字面量类型**：`type State = "idle" | "run" | "jump" | "dead"`
- **泛型**：`type Array<T> = {[number]: T}`；`type Dict<K, V> = {[K]: V}`；支持泛型函数 `function first<T>(arr: {T}): T?`
- **交叉类型（组合）**：`type NamedEntity = Named & Positioned`
- **类型断言**：`local x = getValue() :: string`
- **typeof 检测**：[[Roblox]] 用 `typeof()` 而非 `type()`，因 `type(Vector3.new()) == "userdata"` 而 `typeof(Vector3.new()) == "Vector3"`
- **嵌套结构体**：支持多层嵌套 table 类型定义，如 `PlayerData` 含 `stats: { kills: number, deaths: number }`

### 性能特性
- **Vector3 内建值类型**：`Vector3` 等引擎类型是值类型（value type），不产生 GC 压力
- **本地字节码编译**：脚本在首次执行前编译为字节码，非纯解释执行
- **Native codegen**（实验性）：热函数可编译为机器码，性能接近 [[LuaJIT]]
- **类型注解加速**：有类型注解的数字运算比无注解快约 2–3x（编译器可做更多优化）
- **buffer 库**：`buffer.create(N)` / `buffer.writei32` / `buffer.readi32`，高性能二进制数据，Luau 特有
- **table.freeze**：冻结只读表，允许编译器进一步优化常量访问
- **task 库替代 wait()**：`task.spawn` / `task.defer` / `task.delay` / `task.cancel`，帧调度更精确

### 与标准 Lua 的关系
Luau 基于 Lua **5.1** 扩展，语法层面向下兼容。主要新增：类型注解语法、`continue` 语句、bit32 库内建、CompileOptions 控制等。不支持 Lua 5.2+ 的 `goto`、5.4 的整数类型等特性。

### 应用范围
Luau 目前主要在 [[Roblox]] 平台使用，但 Luau 已开源（luau-lang.o[[ripgrep|rg]]），可作为独立 Lua 运行时嵌入其他引擎。其类型系统设计对 Lua 生态的演进有参考价值。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，第8节 Luau 类型系统、性能特性与 Roblox 应用场景分析
- [[luau-types]] — Luau 类型系统与 Roblox API 参考，含完整类型注解语法、性能技巧示例

## 相关
- [[Roblox]] — Luau 的诞生背景和主要运行平台
- [[LuaJIT]] — 另一条 Lua 性能提升路线（追踪 JIT vs Luau Native codegen）
- [[Lua C API 绑定层]] — Luau 有自己的 C API 扩展机制（luau_push* 系列）
- [[Roblox API]] — Roblox 平台 API（Instance、TweenService、Raycast、RunService 等）
