---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [terminal-ui, react, ui-framework]
aliases: ["Ink", "Ink Framework", "React 终端 UI"]
relates_to:
  - target: "[[Claude Code]]"
    type: used_by
  - target: "[[React]]"
    type: extends
  - target: "[[Terminal Renderer Engine]]"
    type: base_framework
supersedes: null
---

# Ink Framework

## 概述
基于 [[React]] 的终端 UI 渲染框架，被 [[Claude Code]] 用于构建终端界面。

## 关键内容

1. **设计理念**：
   - 将 [[React]] 的组件化和 Virtual DOM 技术应用于终端界面开发
   - 支持流式渲染，适合模型逐 Token 输出的场景
   - 提供复杂的 UI 状态管理能力

2. **技术优势**：
   - 高效处理差量更新，适合实时变化的界面
   - 支持组件复用，提高开发效率
   - 复杂 UI 元素可以通过组件形式统一管理

3. **在 [[Claude Code]] 中的应用**：
   - [[Claude Code]] 使用 Ink 作为基础框架构建终端界面
   - 在此基础上开发了高度优化的自定义渲染层

## 来源
- [[07_terminal_renderer_features]] — 

## 相关
- [[Claude Code]] — used_by
- [[React]] — extends
- [[Terminal Renderer Engine]] — base_framework