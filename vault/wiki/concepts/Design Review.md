---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [design, quality, review]
aliases: ["设计质量审查"]
relates_to: []
supersedes: null
---

# Design Review

## 概述
Design Review是一种系统性的界面质量检查方法，用于对建成的界面进行评估，并输出带优先级的改进建议报告。

## 关键内容

1. **审查维度**（按优先级排序）：
   - 🔴 Critical（必须修复）：对比度不足（< WCAG AA标准4.5:1）、交互元素缺少focus状态、移动端点击目标< 44px
   - 🟡 High（强烈建议）：字体选择是否有个性、颜色是否使用语义token、空状态/加载状态/错误状态是否完整、动效是否尊重prefers-reduced-motion
   - 🟢 Medium（建议改善）：间距系统是否一致、组件是否可复用、是否有记忆锚点

2. **输出格式**：
   - 包含Critical Issues、High Priority Issues、Medium Priority Issues的分级报告
   - 每个问题都提供具体的修复建议

3. **实施方法**：
   - 在界面建设完成后进行系统性质量检查
   - 重点关注用户体验和可访问性
   - 通过明确的检查清单确保全面覆盖

## 来源
- [[jezweb/claude-skills]] — 前端插件工程
- [[]] —

## 相关
- [[Frontend Plugin]] — 前端插件体系
- [[Tailwind CSS v4]] — CSS框架
- [[shadcn/ui]] — UI组件库
