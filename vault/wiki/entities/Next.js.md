---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["web框架", "前端", "全栈", "React", "工具与框架"]
aliases: ["Next.js Framework", "NextJS", "Next"]
relates_to:
  - target: "[[TypeScript]]"
    type: uses
    confidence: 0.9
  - target: "[[React]]"
    type: depends_on
    confidence: 0.95
  - target: "[[Prisma]]"
    type: compares_to
    confidence: 0.6
supersedes: null
---

# Next.js

## 概述
[[Vercel]] 开发的基于 [[React]] 的全栈 Web 框架，支持[[服务]]端渲染（SSR）、静态生成（SSG）和 App [[网关与路由器|Router]] 架构。

## 关键内容

1. **App [[网关与路由器|Router]] 架构**：基于文件系统的路由，使用 `app/` 目录组织页面。支持路由组（如 `(auth)/`、`(dashboard)/`）用于逻辑分组而不影响 URL 路径，API 路由通过 `api/` 子目录定义。

2. **Server Components 优先**：App [[网关与路由器|Router]] 中默认使用 Server Components，可直接使用 `async/await` 获取数据，无需 `useEffect` 或客户端数据获取库。仅在有交互需求时通过 `'use client'` 指令标记 Client Components。

3. **Route Handlers**：API 路由使用标准的 `GET`、`POST` 等导出函数处理 HTTP 请求，返回 `Response.json()` 对象，支持完整的[[错误处理]]和状态码控制。

4. **与 [[Prisma]] 集成**：常搭配 [[Prisma|Prisma ORM]] 使用，通过 `npx prisma migrate dev` 管理数据库迁移，`npx prisma studio` 提供 GUI 数据浏览，`npx prisma db seed` 导入测试数据。

5. **在 [[Ralph Loop]] 中的角色**：作为 [[项目约定手册|AGENTS.md]] 模板中推荐的默认技术栈，配合 [[TypeScript]]、[[Prisma]] 和 [[PostgreSQL]] 构成全栈开发基线。

## 来源
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — Ralph Loop 项目约定模板

## 相关
- [[TypeScript]] — uses（默认开发语言）
- [[Prisma]] — compares_to（常搭配使用的 ORM）
- [[React]] — depends_on（底层 UI 框架）
- [[Vercel]] — part_of（开发与维护方）
