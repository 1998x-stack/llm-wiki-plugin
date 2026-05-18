---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, ui, accessibility, design, skills, AI工程]
aliases: ["web-design-guidelines", "Web Design Guidelines", "UI Guidelines", "Vercel Web Interface Guidelines"]
relates_to:
  - target: "[[Vercel Agent Skills]]"
    type: part_of
    confidence: 0.9
  - target: "[[UI Design]]"
    type: implements
    confidence: 0.8
  - target: "[[Accessibility]]"
    type: implements
    confidence: 0.8
supersedes: null
---

# Web Design Guidelines Skill

## 概述
[[Vercel Agent Skills]] 中的 UI 设计规范[[Skills|技能]]，基于 vercel-labs/web-interface-guidelines [[仓库]]，提供 100+ 条设计规范的自动化审查。

## 关键内容

1. **动态更新机制**：[[Skills|技能]]执行时会动态获取最新的规范内容，确保始终使用最新版本

2. **规范覆盖范围**：
   - 无障碍：图片 alt 属性、表单标签关联、正确的 ARIA 使用
   - 焦点管理：可见的 focus ring、合理 tab 顺序、模态框焦点捕获
   - 触摸目标：按钮最小 44×44px 符合 iOS HIG 标准
   - 减弱动效：尊重 `prefers-reduced-motion` 偏好[[Settings|设置]]
   - 语义 HTML：正确使用 `<nav>`, `<main>`, `<article>`, `<aside>`
   - 键盘导航：所有功能支持键盘操作
   - 颜色对比：符合 WCAG AA 标准

3. **与美学层[[Skills|技能]]的互补**：与 [[Anthropic_frontend-design_Skill|Anthropic frontend-design]] [[Skills|技能]]形成层次化防护

## 来源
- [[05_vercel_agent_skills_react.md]] — Vercel Agent Skills React 系列深度解析

## 相关
- [[Vercel Agent Skills]] — part_of
- [[UI Design]] — implements
- [[Accessibility]] — implements