---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发]
aliases: [Lua热更新, Lua运行时重载, hot reload]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: extends
    confidence: 0.9
  - target: "[[Lua模块系统]]"
    type: depends_on
    confidence: 0.88
  - target: "[[游戏引擎架构]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Lua 热重载

## 概述
Lua 热重载是在游戏运行时无需重启即可重新加载脚本模块的技术，通过监控文件修改时间戳、清除 `package.loaded` 缓存并重新 `require` 实现，显著缩短调试迭代周期。

## 关键内容

### 核心机制
Lua 的模块缓存存储在 `package.loaded` 表中。热重载的步骤：
1. 监控文件系统时间戳（通过 `stat` 或 fswatch 等工具）
2. 发现文件变更后，将 `package.loaded[module_name]` 置为 `nil` 清除缓存
3. 重新调用 `require(module_name)` 执行新版本代码
4. 可选：触发模块重载事件，通知其他系统更新引用

### 实现模式
- **轮询检查**：在游戏更新循环中每秒调用一次检查函数（仅调试模式启用），避免性能开销
- **文件时间戳比较**：记录每个模块路径的上次修改时间 `mtime`，发现变更时触发重载
- **事件通知**：重载成功后通过 EventBus 广播 `"module_reloaded"` 事件，让系统重新绑定回调

### 已知限制与陷阱
- **闭包捕获问题**：已运行中的闭包仍引用旧模块的 upvalue，重载后新模块代码与旧闭包共存
- **metatable 更新不完整**：userdata 对象绑定的 metatable 可能未更新为新版本方法表
- **状态迁移**：模块全局状态（如 `local count = 0`）在重载后重置，运行时累积状态丢失
- **仅调试模式**：生产环境应禁用热重载，避免安全风险和性能开销

### 与热更新（Hot Patch）的区别
热重载是整体重载模块文件，适合开发调试；xLua 等框架的热更新（Hotfix）是方法级补丁注入，可在生产环境无缝替换函数实现，无需重启。

## 来源
- [[lua-gameengine-deep-research]] — 深度研究报告，第5.1节热重载系统实现原理与代码示例

## 相关
- [[Lua脚本宿主模式]] — 热重载是第5层业务框架层的热更新策略
- [[Lua模块系统]] — `package.loaded` 缓存机制是热重载的操作对象
- [[游戏引擎架构]] — 热重载提升 Scripting 层的开发迭代速度
