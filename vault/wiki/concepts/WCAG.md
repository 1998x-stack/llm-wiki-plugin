---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [无障碍, WCAG, 前端开发]
aliases: ["Web Content Accessibility Guidelines", "WCAG 2.1"]
relates_to: []
supersedes: null
---

# WCAG

## 概述
Web Content Accessibility Guidelines（网页内容无障碍指南），是国际公认的无障碍标准，旨在确保网页内容对所有人（包括残障人士）都可访问。

## 关键内容

1. **级别分类**：
   - Level A：基础无障碍要求，最低标准
   - Level AA：中等级别，广泛采用的标准
   - Level AAA：高级别，最高标准

2. **核心原则 (POUR)**：
   - Perceivable（可感知）：信息和用户界面组件必须能被感知
   - Operable（可操作）：界面组件和导航必须可操作
   - Understandable（可理解）：信息和UI操作必须可理解
   - Robust（可靠）：内容必须足够健壮以兼容多种用户代理

3. **关键技术要求**：
   - 颜色对比度：正文≥4.5:1，大文字≥3:1
   - 焦点状态：所有交互元素必须有可见的focus ring
   - 键盘导航：所有功能可通过键盘完成
   - ARIA标签：适当的语义化标记

4. **在[[AI辅助开发]]中的应用**：现代AI工具如[[AccessLint]]可自动检查WCAG合规性

## 来源
- [[06_bencium_ux_designer_and_accesslint.md]] — AccessLint和无障碍设计相关内容

## 相关
- [[AccessLint]] — relates_to
- [[无障碍设计]] — relates_to
- [[前端开发]] — relates_to
- [[bencium UX Designer]] — relates_to