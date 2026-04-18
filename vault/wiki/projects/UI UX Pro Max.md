---
type: project
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [claude-code, skill, design-system, ui, ux]
aliases: ["UI UX Pro Max", "UUPM", "ui-ux-pro-max"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
---

# UI UX Pro Max

## 概述
专为 AI 编程助手设计的「设计智能技能包」（53k+ Stars），让 AI 在生成 UI 代码前先经过专业设计决策过程，解决 AI 生成界面颜色随意、字体凑合、布局平庸的问题。

## 关键内容

1. **核心规模**：
   - UI 风格库：67 种（极简到 Cyberpunk）
   - 色彩体系：161 套（与 161 种产品类型对应）
   - 字体配对：57 组（含 Google Fonts 直链）
   - UX 准则：99 条
   - 推理规则：161 条
   - 图表类型：25 种
   - 技术栈：15 个（React/Vue/SwiftUI/Flutter）

2. **三层架构**：
   - **Layer 3**：AI 助手集成层（Claude Code/Cursor/Windsurf）
   - **Layer 2**：推理引擎层（BM25 + Regex 混合检索）
   - **Layer 1**：知识数据库层（CSV 文件集）

3. **数据源**：
   - products.csv：161 种产品类型
   - styles.csv：67 种 UI 风格
   - colors.csv：161 套色彩方案
   - typography.csv：57 组字体配对
   - ux-guidelines.csv：99 条 UX 准则
   - ui-reasoning.csv：161 条行业推理规则

## 来源
- [[blog-01-overview]] — UI UX Pro Max 总览

## 相关
- [[Claude Code]] — uses
- [[Agent Skills]] — implements
- [[frontend-design Skill]] — compares_to
