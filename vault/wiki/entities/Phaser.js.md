---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["工具", "游戏引擎", "前端", "工具与框架"]
aliases: [Phaser, Phaser.js Framework]
relates_to:
  - target: "[[Codex CLI]]"
    type: uses
    confidence: 0.7
  - target: "[[Codex多Agent调度]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Phaser.js

开源 HTML5 游戏框架，用于在浏览器中快速开发 2D 游戏。支持 Canvas 和 WebGL 双渲染后端，内置物理引擎、动画系统、输入处理和场景管理。

## 概述
Phaser.js 是一个轻量级、高性能的 HTML5 游戏框架，专为跨平台 2D 游戏开发设计，支持桌面和移动端浏览器。

## 关键内容

1. **双渲染后端**：自动在 Canvas 2D 和 WebGL 之间切换，开发者无需手动选择，低性能设备回退到 Canvas。
2. **场景系统**：游戏按场景（Scene）组织，支持场景间的切换、数据传递和并行运行，天然适合模块化开发。
3. **物理引擎集成**：内置 Arcade Physics、Impact Physics 和 Matter.js 三种物理引擎，从简单碰撞到复杂刚体模拟均可覆盖。
4. **输入系统**：统一的键盘、鼠标、触摸输入抽象层，自动适配不同平台。
5. **资源预加载**：内置 Loader 系统支持图片、音频、精灵表、JSON 等资源的批量预加载和进度回调。

## 在 Codex 多 Agent 场景中的角色

在 [[OpenAI]] DevDay 2025 展示中，7 个 [[Codex CLI]] 实例并行开发 7 款不同的 Phaser.js 小游戏——每个 Agent 独立负责一款游戏的迭代开发，开发者仅做审批和方向把控。这体现了 [[Codex多Agent调度|多 Agent 调度]]对开发者带宽的杠杆化：将"写代码"升级为"审批 + 方向把控"。

## 来源
- [[raw/articles/ai-tools/codex/07_codex_multi_agent.md]] — Codex CLI 深度解析 Vol.7：Multi-Agent 并行编码的调度与协同

## 相关
- [[Codex CLI]] — 在 DevDay 2025 案例中用于并行开发 Phaser.js 游戏 (relates_to)
- [[Codex多Agent调度]] — 7 Agent 并行开发场景的调度机制 (relates_to)
- [[HTML]] — Phaser.js 运行于 HTML5 环境 (uses)
