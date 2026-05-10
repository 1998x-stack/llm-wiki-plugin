---
type: company
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [frontend, hosting, react, nextjs, ai-tools]
aliases: ["Vercel", "Vercel Labs"]
relates_to:
  - target: "[[Next.js]]"
    type: created
  - target: "[[Claude Code]]"
    type: relates_to
---

# Vercel

## 概述
前端部署平台，[[Next.js]] 创造者，[[Agent Skills]] 规范的早期采用者和主要推动者，通过 [[Vercel Agent Skills|vercel-labs/agent-skills]] 提供 [[React]]/[[Next.js]] 性能与架构的官方 [[Agent Skills|Skills]]。

## 关键内容

1. **核心产品**：
   - **[[Next.js]]**：[[React]] 框架
   - **Vercel Platform**：前端部署与托管
   - **Turbopack**：Rust 编写的打包工具

2. **[[Agent Skills]] 贡献**：
   - **[[Vercel Agent Skills|vercel-labs/agent-skills]]**：[[React]]/[[Next.js]] 性能与架构 [[Agent Skills|Skills]]（19k+ Stars）
   - **vercel-labs/skills**：`npx skills` CLI 工具（社区标准）
   - **[[React Best Practices Skill|react-best-practices]]**：70+ 条 [[React]] 性能优化规则

3. **核心 [[Agent Skills|Skills]]**：
   - `react-best-practices`：[[React]]/[[Next.js]] 性能优化（CRITICAL → LOW 四级优先级）
   - `composition-patterns`：[[React]] 组合模式
   - `web-design-guidelines`：Web UI 设计规范
   - `react-native-skills`：[[React]] Native + Expo

4. **安装方式**：
   ```bash
   npx skills add vercel-labs/agent-skills
   npx skills add vercel-labs/agent-skills --skill react-best-practices
   ```

5. **规则分类（[[React Best Practices Skill|react-best-practices]]）**：
   - Async 模式（并行请求、延迟 await）
   - Bundle 优化（动态导入、Tree Shaking）
   - 渲染模式（SSG、SSR、Streaming）
   - [[React]] 优化（memo、useCallback、useMemo）
   - 状态管理（Server State、Form State）
   - CSS 优化（CSS-in-JS、[[Tailwind CSS v4|Tailwind]]）
   - 图片优化（next/image、WebP/AVIF）
   - 数据获取（SWR、[[React]] Query）

## 来源
- [[05_vercel_agent_skills_react]] — Vercel Agent Skills React 系列

## 相关
- [[Next.js]] — created
- [[React]] — relates_to
- [[Claude Code]] — relates_to
- [[Agent Skills]] — implements
