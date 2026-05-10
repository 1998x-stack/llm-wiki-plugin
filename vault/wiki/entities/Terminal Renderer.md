---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [terminal-ui, rendering, optimization]
aliases: ["Terminal Rendering Engine", "CLI UI"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends
-->

# Terminal Renderer

## 概述
[[Claude Code]] 的自定义终端 UI 渲染引擎，基于 Ink 框架构建的高度优化渲染层。

## 关键内容

1. **核心技术架构**：
   - 基于 Ink（[[Ink Framework|React 终端 UI]] 框架）的自定义渲染层
   - 使用 Int32Array 作为 ASCII 字符池，每个 Int32 同时编码字符码和样式元数据
   - 采用位掩码样式编码节省内存，避免对象分配
   - 借鉴游戏引擎 ECS（Entity-Component-System）思想优化性能

2. **性能优化技术**：
   - 渲染补丁优化器（Optimizer）：[[计算]]最小变更补丁，而非重新渲染整个屏幕
   - 相比朴素实现在 Token 流式传输期间减少约 50x 的 stringWidth 函数调用
   - 自蒸发行宽缓存（self-evicting line-width cache）避免重复[[计算]]
   - 光标移动合并优化，消除不必要的 hide/show 对

3. **工程应用**：
   - 屏幕缓冲管理通过 ink/screen.ts 实现
   - 渲染补丁优化通过 ink/optimizer.ts 实现
   - 在逐 Token 实时流式输出场景下显著提升性能

## 来源
- [[Claude Code 源码泄露深度解析（七）：终端渲染引擎与彩蛋——BUDDY、ULTRAPLAN 与 VOICE_MODE]] — 终端 UI：React + Ink 的工程奇迹

## 相关
- [[Ink]] — depends_on
- [[Claude Code]] — part_of