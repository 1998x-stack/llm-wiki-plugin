---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [css, styling, framework, AI工程]
aliases: ["Tailwind CSS", "Tailwind", "Tailwind v4"]
relates_to:
  - target: "[[React]]"
    type: integrates_with
  - target: "[[shadcn/ui]]"
    type: integrates_with
  - target: "[[jezweb/claude-skills]]"
    type: used_by
  - target: "[[Tailwind CSS]]"
    type: supersedes
supersedes: null
entity_type: tool
---

# Tailwind CSS v4

## 概述
[[Tailwind CSS]] v4是现代化的实用优先CSS框架的重大版本，引入了破坏性变更的架构调整。

## 关键内容

1. **主要变更**：
   - [[Configuration|配置]]文件：移除了 `tailwind.config.ts`，改为在CSS中直接[[Configuration|配置]]
   - Vite插件：使用 `@tailwindcss/vite` 插件替代PostCSS方式
   - 动画库：`tailwindcss-animate` 替换为 `tw-animate-css`（v4专用）
   - 主题扩展：使用 `@theme inline { --color-*: }` 替代 `extend: { colors: {...} }`
   - CSS导入：使用 `@import "tailwindcss"` 替代 `@tailwind base; @tailwind components`

2. **强制四步架构模式**：
   - Step 1: 导入基础 (`@import "tailwindcss"`, `@import "tw-animate-css"`)
   - Step 2: 定义CSS变量（在`:root`中，非`@layer base`）
   - Step 3: 映射到Tailwind utility类（使用`@theme inline`）
   - Step 4: 应用基础样式（使用`@layer base`）

3. **常见问题**：
   - CSS变量未加`hsl()`包装导致颜色不渲染
   - `tw-animate-css`缺失导致shadcn动画失效
   - `@theme inline`的dark mode切换失效（已知Bug）

## 来源
- [[jezweb/claude-skills]] — 前端插件工程
- [[04_jezweb_claude_skills_frontend]] — Tailwind v4 主题工程详解

## 相关
- [[shadcn/ui]] — UI组件库
- [[Frontend Plugin]] — 前端插件体系
- [[React 19]] — 前端框架
- [[Tailwind CSS]] — 前身版本
