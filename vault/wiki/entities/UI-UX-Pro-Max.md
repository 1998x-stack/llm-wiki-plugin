---
type: entity
title: "UI UX Pro Max"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 7
tags:
  - 工具
  - AI
  - 设计
  - UI
  - Skill
aliases:
  - UUPM
  - ui-ux-pro-max-skill
  - UI UX Pro Max Skill
relates_to:
  - target: "[[Claude-Code]]"
    type: related_to
    confidence: 0.9
  - target: "[[AI设计推理层]]"
    type: implements
    confidence: 0.95
  - target: "[[结构化UI风格知识库]]"
    type: implements
    confidence: 0.9
  - target: "[[行业设计反模式系统]]"
    type: implements
    confidence: 0.9
  - target: "[[行业色彩情绪映射]]"
    type: implements
    confidence: 0.9
  - target: "[[工程化UX规则体系]]"
    type: implements
    confidence: 0.9
  - target: "[[技术栈感知设计规则]]"
    type: implements
    confidence: 0.9
  - target: "[[Master-Overrides设计系统持久化]]"
    type: implements
    confidence: 0.95
supersedes: null
---

# UI UX Pro Max

## 概述

UI UX Pro Max（UUPM）是 GitHub 上 53k+ Stars 的开源 AI 设计技能包，专为 Claude Code、Cursor、Windsurf 等 AI 编程助手设计，作为「[[AI设计推理层|设计推理层]]」让 AI 在生成 UI 代码前先完成专业设计决策。

## 关键内容

### 核心数字

| 模块 | 规模 |
|------|------|
| UI 风格库 | 67 种（极简主义到 Cyberpunk） |
| 色彩体系 | 161 套（与 161 种产品类型一一对应） |
| 字体配对 | 57 组（含 [[Google]] Fonts 直链） |
| UX 准则 | 99 条（最佳实践 + 反模式 + 可访问性） |
| 行业推理规则 | 161 条（v2.0 核心） |
| 图表类型 | 25 种 |
| 支持技术栈 | 15 个（React/Vue/SwiftUI/Flutter 等） |

### 三层架构

```
Layer 3：AI 助手集成层（Claude Code / Cursor / Windsurf 等）
           ↓ 调用
Layer 2：推理引擎层（search.py + design_system.py）
         BM25 + Regex 混合检索
         5 路并行域搜索（产品→风格→颜色→字体→落地页）
         161 条行业推理规则（JSON 条件判断）
           ↓ 查询
Layer 1：知识数据库层（CSV 文件集，~564KB）
         styles.csv / colors.csv / typography.csv
         products.csv / ux-guidelines.csv / charts.csv
```

### 核心工作流（5 路并行搜索）

用户请求 → 5 路并行匹配（产品类型 / UI 风格 / 色彩方案 / 落地页模式 / 字体配对）→ 推理引擎整合 → 输出完整设计系统（Pattern + Style + Colors + Typography + 反模式警告）

### 与传统设计资源的本质区别

传统设计资源是**静态文档/模板库**，UUPM 是**动态推理引擎**：按产品类型自动定制、自动检测反模式、技术栈感知、AI 对话自动触发。

### 项目背景

- **作者**：NextLevelBuilder（越南开发者 @viettranx）
- **诞生**：2024 年 12 月（v1.0.0 由 Claude Code 协同生成）
- **当前版本**：v2.5.0（2026 年 3 月）
- **支持平台**：18 个 AI 助手
- **语言**：Python 78.2% + JavaScript 11.6% + TypeScript 6.7%

### 安装方式

```bash
# Claude Marketplace
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

# CLI（推荐）
npm install -g uipro-cli
uipro init --ai claude

# 全局安装（跨项目）
uipro init --ai claude --global   # 安装到 ~/.claude/skills/
```

## 来源

- [[raw/articles/ai-tools/claude-skills/blog-01-overview.md]]
- [[raw/articles/ai-tools/claude-skills/blog-02-styles.md]]
- [[raw/articles/ai-tools/claude-skills/blog-03-design-system-generator.md]]
- [[raw/articles/ai-tools/claude-skills/blog-04-colors-typography.md]]
- [[raw/articles/ai-tools/claude-skills/blog-05-ux-charts.md]]
- [[raw/articles/ai-tools/claude-skills/blog-06-stacks-search.md]]
- [[raw/articles/ai-tools/claude-skills/blog-07-persistence.md]]

## 相关

- [[AI设计推理层]] — UUPM 实现的核心设计模式
- [[结构化UI风格知识库]] — styles.csv 的知识架构
- [[行业设计反模式系统]] — 161 条推理规则的负样本库
- [[行业色彩情绪映射]] — 161 套色板的情绪逻辑
- [[工程化UX规则体系]] — 99 条 UX 规则的工程化
- [[技术栈感知设计规则]] — 15 个技术栈专项指南
- [[Master-Overrides设计系统持久化]] — 解决 AI 设计失忆症
- [[Claude-Code]] — 主要集成平台之一
