---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [layout-engine, ui-framework, yoga-layout]
aliases: ["Yoga", "Yoga Layout", "Yoga（Meta 开源）"]
relates_to:
  - target: "[[Meta]]"
    type: developed_by
  - target: "[[Claude Code]]"
    type: used_by
  - target: "[[React]]"
    type: integrates_with
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Yoga

## 概述
Yoga 是 Meta 开源的布局引擎，实现了 Flexbox 布局[[算法]]，支持约束布局，能够适配任意终端宽度。

## 关键内容
1. **核心功能**：Yoga 是一个跨平台的布局引擎，实现了 W3C 的 Flexbox 标准，允许开发者使用相同的布局[[算法]]在不同平台上创建一致的用户界面。

2. **应用场景**：在 [[Claude Code]] 中用作布局引擎，帮助实现声明式终端 UI，使其能够适应各种终端宽度。

3. **技术特点**：
   - 高性能：优化了[[计算]]效率，能快速[[计算]]复杂布局
   - 跨平台：可在多种[[操作系统]]和设备上运行
   - Flexbox 标准：遵循 W3C 的 Flexbox 规范
   - 约束布局：支持基于约束条件的布局[[计算]]

## 来源
- [[01_system_overview.md]] — Claude Code 系统总览

## 相关
- [[Meta]] — developed_by
- [[Claude Code]] — used_by
- [[React]] — integrates_with

## 指令