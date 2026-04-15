---
type: concept
title: "工程化 UX 规则体系"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [UI, UX, 设计, AI, 规则系统, 可访问性]
aliases:
  - 可机器执行的UX规则
  - UX规则工程化
  - structured UX guidelines
relates_to:
  - target: "[[UI-UX-Pro-Max]]"
    type: part_of
    confidence: 0.95
  - target: "[[行业设计反模式系统]]"
    type: related_to
    confidence: 0.9
  - target: "[[AI设计推理层]]"
    type: related_to
    confidence: 0.85
supersedes: null
---

# 工程化 UX 规则体系

## 概述

工程化 UX 规则体系是将隐性设计经验编码为**带优先级标签、唯一 ID、可机器检索和自动验证的结构化规则**的方法：使 AI 能直接执行 UX 规则检查而不只是「知道一些原则」。

## 关键内容

### 核心设计决策

**规则必须可机器执行**。每条规则包含：

```
id              → 唯一引用名（hover-state-required）
category        → 分类（交互/可访问性/性能/布局...）
priority        → P0/P1/P2 三级优先级
description     → 详细描述
anti_pattern    → 对应错误模式
platform        → 适用平台（web/mobile/all）
stack_notes     → 技术栈相关注记
```

### P0/P1/P2 三级优先级框架

| 级别 | 含义 | 示例规则 |
|------|------|---------|
| **P0**（必须遵守）| 违反造成严重可用性或合规风险 | 对比度 ≥ 4.5:1、focus 状态可见、可点击元素有 cursor:pointer |
| **P1**（强烈建议）| 违反降低体验质量 | hover 150-300ms 过渡、表单 blur 即时验证 |
| **P2**（酌情处理）| 上下文依赖，有时可例外 | 拇指区域优化、图表数据导出 |

### 99 条规则分类全景

| 分类 | 代表规则 |
|------|---------|
| 交互状态 | hover-state-required、cursor-pointer-required、disabled-state-clarity |
| 可访问性 | contrast-minimum（4.5:1）、focus-visible-required、color-not-sole-indicator |
| 触控/移动端 | touch-target-minimum（44×44px）、safe-area-inset |
| 布局/响应式 | responsive-breakpoints（375/768/1024/1440px）、CLS 防止 |
| 动画/性能 | animation-duration（150-300ms）、GPU 加速（transform/opacity） |
| 表单/输入 | inline-validation、placeholder-not-label、error-message-proximity |
| 图标使用 | no-emoji-as-icon（用 SVG）、icon-style-consistency |
| 平台适配 | dark-mode-pairing、elevation-consistent |

### P0 自动验收清单

每次代码生成后自动输出：

```
PRE-DELIVERY CHECKLIST（P0 必过项）:
  [ ] cursor-pointer-required  — 所有可点击元素有 cursor:pointer
  [ ] contrast-minimum         — 对比度 ≥ 4.5:1
  [ ] hover-state-required     — 所有交互元素有 hover 状态
  [ ] no-emoji-as-icon         — 无 emoji 图标（用 SVG）
  [ ] focus-visible-required   — 焦点状态可见
  [ ] prefers-reduced-motion   — 动画有降级处理
  [ ] responsive-breakpoints   — 测试 375/768/1024/1440px
```

### 图表类型结构化推荐

同样思路应用于图表选择（25 种图表，按数据类型 + 展示目的推荐）：

| 类型 | 代表图表 | 关键反模式 |
|------|---------|-----------|
| 比较 | Bar Chart（≤12类别）、Radar | Grouped Bar 超过 3 系列 |
| 趋势 | Line Chart、Sparkline | 数据点 < 5 时用折线（应用柱状）|
| 分布 | Histogram、Scatter Plot | — |
| 构成 | [[Pi-Agent|Pi]]e（< 5 片）、Treemap | [[Pi-Agent|Pi]]e ≥ 6 片难以分辨 |
| 关系 | Sankey、Network Graph | — |

**核心图表规则**：Y 轴必须从 0 开始（截断是视觉欺骗）；颜色编码必须有图例且不能仅靠颜色区分。

### 知识工程价值

将 UX「感觉对」的隐性经验转化为可检索的规则系统，使 AI 能：
1. **检索**：按 category/priority/platform 过滤规则
2. **验证**：对照 P0 清单检查生成代码
3. **引用**：生成代码时引用具体规则 ID 作为注释

## 来源

- [[raw/articles/ai-tools/claude-skills/blog-05-ux-charts.md]]

## 相关

- [[UI-UX-Pro-Max]] — 实现平台（ux-guidelines.csv + charts.csv）
- [[行业设计反模式系统]] — 规则化设计禁忌的同类模式
- [[结构化UI风格知识库]] — 同为隐性设计知识的结构化编码
