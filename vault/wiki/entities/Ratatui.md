---
type: entity
status: active
confidence: 0.7
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [技术, 工具, Rust, TUI]
aliases: [Ratatui Framework]
relates_to:
  - target: "[[Codex TUI]]"
    type: uses
    confidence: 0.95
  - target: "[[Rust]]"
    type: depends_on
    confidence: 0.95
  - target: "[[Codex CLI]]"
    type: uses
    confidence: 0.9
supersedes: null
---

# Ratatui

Rust 生态中最活跃的**终端用户界面（TUI）框架**，基于 crossterm 后端，提供声明式 widget 组件和事件驱动渲染能力。

## 概述

Ratatui 是 Rust 的 TUI 渲染引擎，为 [[Codex CLI]] 等现代终端应用提供全屏 alternate screen 渲染、语法高亮 diff 展示、以及事件驱动的 UI 状态管理能力。

## 关键特性

1. **声明式 Widget 系统**：通过 Rust 类型系统构建终端 UI 组件（Paragraph、List、Table、Gauge 等），编译期保证布局正确性
2. **Alternate Screen 支持**：原生支持终端 alternate buffer 模式，进入时清屏、退出时恢复 shell 状态，不污染 history
3. **事件驱动架构**：与 crossterm 事件系统集成，处理键盘输入、鼠标事件、终端 resize 信号
4. **零运行时开销**：纯 Rust 实现，无 GC 抖动，帧渲染延迟可预测
5. **主题与样式系统**：支持终端 256 色 / True Color，可[[Configuration|配置]]配色方案

## 在 Codex CLI 中的角色

Ratatui 是 [[Codex TUI]] 的渲染层底座，负责：
- 全屏 Alternate Screen 模式渲染
- 语法高亮的 diff 预览展示
- [[Approval Gate UI|Approval Gate]] 弹窗 UI
- Composer 输入框与 Draft History 面板
- 多 Agent 状态面板的并发渲染

## 来源

- [[raw/articles/ai-tools/codex/02_codex_tui_component.md]] — Codex CLI 深度解析 Vol.2：TUI 交互式终端的设计哲学

## 相关

- [[Codex TUI]] — uses
- [[Rust]] — depends_on
- [[Codex CLI]] — uses
