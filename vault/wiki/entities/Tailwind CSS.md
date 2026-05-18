---
type: tool
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [css-framework, styling, frontend, AI工程]
aliases: ["Tailwind CSS", "Tailwind CSS v4", "Tailwind v4"]
relates_to:
  - target: "[[React]]"
    type: uses
  - target: "[[shadcn/ui]]"
    type: uses
  - target: "[[jezweb/claude-skills]]"
    type: uses
  - target: "[[Tailwind CSS v4]]"
    type: supersedes
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Tailwind CSS v4

## 概述
[[Tailwind CSS v4]] 是 CSS 框架的重大更新版本，相比 v3 有显著变化，引入了新的[[Configuration|配置]]方式和主题系统，是现代前端开发的重要工具。

## 关键内容
1. **[[Configuration|配置]]变更**：移除了传统的 `tailwind.config.ts` [[Configuration|配置]]文件，在 CSS 文件中通过 `@theme inline` 进行[[Configuration|配置]]。[[Configuration|配置]]顺序为：导入基础、定义 CSS 变量、映射到工具类、应用基础样式。

2. **关键语法变化**：
   - 导入方式：`@import "tailwindcss"` 替代 `@tailwind base/components/utilities`
   - 主题[[Configuration|配置]]：`@theme inline { --color-*: }` 替代 `extend: { colors: {...} }`
   - Vite 插件：使用 `@tailwindcss/vite` 插件替代 PostCSS 方式

3. **动画支持**：v4 需要专用的 `tw-animate-css` 库替代旧的 `tailwindcss-animate`，以支持 shadcn/ui 动画组件。

4. **CSS 变量模式**：需要使用 `hsl()` 包装器定义颜色变量，如 `--background: hsl(0 0% 100%)`，然后通过 `@theme inline` 映射到工具类。

5. **常见陷阱**：包括遗漏 `tw-animate-css` 导致动画失效、CSS 变量未加 `hsl()` 包装器、dark mode 切换失效等问题。

## 来源
- [[04_jezweb_claude_skills_frontend]] — Tailwind v4 主题工程深度解析

## 相关
- [[React]] — 通常配合使用
- [[shadcn/ui]] — 依赖 Tailwind 主题系统
- [[jezweb/claude-skills]] — 提供 Tailwind 主题构建技能