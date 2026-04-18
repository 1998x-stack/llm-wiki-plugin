---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["claude-code", "skill", "frontend", "react", "shadcn", "工具与框架"]
aliases: ["web-artifacts-builder", "web-artifacts-builder Skill"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[frontend-design Skill]]"
    type: relates_to
  - target: "[[Anthropic]]"
    type: created_by
---

# web-artifacts-builder Skill

## 概述
[[Anthropic]] 官方 Skill，用于构建复杂 React Artifacts，支持状态管理、路由和 shadcn/ui 组件，通过 Parcel + html-inline 将应用打包为单个 HTML 文件。

## 关键内容

1. **技术栈**：
   - React 18
   - [[TypeScript]] (strict)
   - Vite（开发服务器）
   - Parcel（打包）
   - Tailwind CSS 3.4.1
   - shadcn/ui（40+ 组件）
   - html-inline（资源内联）

2. **适用场景**：
   - ✅ 多组件 + 状态管理 + 路由
   - ✅ 复杂 [[TypeScript]] 类型系统
   - ✅ 40+ shadcn/ui 组件
   - ✅ 输出单个可分享 HTML 文件
   - ❌ 简单单文件 HTML/JSX（用 [[frontend-design Skill]]）

3. **五步工作流**：
   - **Step 1**：初始化（`init-artifact.sh`）
   - **Step 2**：开发 Artifact
   - **Step 3**：Bundle（`bundle-artifact.sh`）
   - **Step 4**：分享（`present_files`）
   - **Step 5**：可选测试

4. **为什么用 Parcel 而非 Vite build**：
   - Vite 输出多文件，需服务器托管
   - Parcel + html-inline = 单文件 HTML（500KB ~ 3MB）

5. **Anti-AI-Slop 警告**：
   - 避免过度居中布局
   - 避免紫色渐变
   - 避免统一圆角
   - 避免 Inter 字体

6. **限制**：
   - Node 18 需降级 Vite
   - Bundle 较大（1-3MB）
   - 无 SSR 支持
   - 外部 API 调用需配合 [[Anthropic]] API

## 来源
- [[03_web_artifacts_builder_skill]] — web-artifacts-builder Skill 解析
- GitHub: anthropics/skills

## 相关
- [[Claude Code]] — uses
- [[frontend-design Skill]] — relates_to
- [[Anthropic]] — created_by
- [[shadcn/ui]] — uses
