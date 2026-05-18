---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [tech-stack, ui-framework, terminal, AI设计]
aliases: ["Ink", "React Ink"]
relates_to:
  - target: "[[React]]"
    type: extends
  - target: "[[Claude Code]]"
    type: used_by
  - target: "[[TypeScript]]"
    type: compatible_with
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Ink

## 概述
[[React]] Ink 是用于构建命令行界面(CLI)应用程序的 [[React]] 渲染器，允许使用 [[React]] 组件来创建声明式终端 UI。

## 关键内容
1. **功能特性**：提供了一套预构建组件，用于创建终端用户界面，如文本、输入框、列表、表格等。

2. **应用场景**：常用于开发终端应用程序，特别是在 AI 代理系统如 [[Claude Code]] 中，用来构建动态、响应式的终端界面。

3. **主要优势**：使用 [[React]] 的编程模型来构建终端界面，允许开发者利用 [[React]] 生态系统的知识和组件模式来构建 CLI 应用。

## 来源
- [[01_system_overview.md]] — Claude Code 系统总览

## 相关
- [[React]] — extends
- [[Claude Code]] — used_by
- [[TypeScript]] — compatible_with

## 指令