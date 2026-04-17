---
type: concept
status: active
confidence: 0.87
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, 安全, Lua编程]
aliases: [Lua沙盒, Lua安全执行, Lua sandbox]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: extends
    confidence: 0.88
  - target: "[[Lua C API 绑定层]]"
    type: depends_on
    confidence: 0.8
  - target: "[[Roblox]]"
    type: relates_to
    confidence: 0.85
supersedes: null
---

# Lua 沙盒系统

## 概述
Lua 沙盒系统通过白名单环境表（`_ENV` 替换）限制脚本可访问的全局函数，配合指令计数钩子防止无限循环，用于安全执行用户自定义脚本（Mod 系统、关卡脚本、玩家脚本等）。

## 关键内容

### 核心原理
Lua 5.2+ 通过 `_ENV` 机制实现沙盒：用 `load(code, name, "t", env)` 将脚本加载到自定义环境表 `env` 中执行，脚本只能访问 `env` 中存在的函数和变量，无法访问全局表中的其他内容。

### 白名单设计
允许访问的安全函数集合（SAFE_ENV）通常包含：
- **数学库**：`math.abs/ceil/floor/max/min/sqrt/sin/cos/tan/pi/random`
- **字符串库**：`string.format/len/sub/find/gmatch/gsub/upper/lower`
- **表操作**：`table.insert/remove/sort/concat/unpack`
- **基础函数**：`ipairs/pairs/tostring/tonumber/type/error/pcall/xpcall/setmetatable`

明确禁止的危险库：`io`（文件访问）、`os`（系统调用）、`require`（任意模块加载）、`dofile/loadfile`（执行任意文件）、`debug`（绕过保护）。

### 指令计数限制
通过 `debug.sethook(fn, "c", N)` 设置指令钩子，每执行 N 条指令触发一次回调，计数超过阈值时抛出错误，防止用户脚本死循环挂死游戏进程。

### 游戏 API 注入
沙盒环境可选择性注入受控的游戏 API：
```lua
Sandbox.create({
    Entity = {create=..., destroy=...},  -- 受限 Entity API
    Audio  = {play=...},                 -- 只开放 play，不开放 stopAll
})
```

### 应用场景
- **Mod 系统**：允许玩家编写游戏模组（[[Roblox]]、Minecraft 式 Mod）
- **关卡脚本**：关卡设计师编写触发逻辑，不需要完整引擎权限
- **AI 行为树**：限定范围的行为脚本，防止 AI 调用不该调用的接口

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，第5.2节沙盒执行环境实现原理与代码示例

## 相关
- [[Lua脚本宿主模式]] — 沙盒是第1层 VM 层的安全配置
- [[Lua C API 绑定层]] — 沙盒通过 C 侧控制注册哪些函数到 env
- [[Roblox]] — Roblox 对用户脚本实施严格沙盒是其平台安全核心
