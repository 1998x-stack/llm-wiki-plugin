---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["数据库", "关系型数据库", "开源", "工具与框架"]
aliases: ["Postgres", "PostgreSQL Database"]
relates_to:
  - target: "[[Prisma]]"
    type: uses
    confidence: 0.85
  - target: "[[Next.js]]"
    type: uses
    confidence: 0.7
  - target: "[[SQLite]]"
    type: compares_to
    confidence: 0.6
supersedes: null
---

# PostgreSQL

## 概述
开源对象关系型数据库管理系统，以 ACID 合规性、扩展性和对复杂查询的支持著称，是现代 Web 应用的首选关系数据库之一。

## 关键内容

1. **连接池管理**：在 Agent 驱动的开发环境中，必须设置 connection pool timeout，否则长时间无操作后连接会断开。典型连接串格式：`postgresql://localhost:5432/[project]_dev`。

2. **与 [[Prisma]] 配合**：通过 `DATABASE_URL` 环境变量配置连接，[[Prisma]] 的 `migrate dev` 命令执行前需确保数据库可访问。迁移文件由 [[Prisma]] 自动生成并管理。

3. **在 [[Ralph Loop]] 中的角色**：AGENTS.md 模板中作为默认数据库选择，配合 [[Prisma]] ORM 和 [[Next.js]] 构成全栈开发基线。环境变量存储在 `.env.local` 中（gitignored）。

4. **开发工作流**：
   - 本地开发：`postgresql://localhost:5432/[project]_dev`
   - 通过 [[Prisma]] Studio GUI 浏览和编辑数据
   - 迁移通过 schema.prisma 变更驱动，非手动 SQL

## 来源
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — Ralph Loop 项目约定模板

## 相关
- [[Prisma]] — uses（ORM 层）
- [[Next.js]] — uses（应用框架层）
- [[SQLite]] — compares_to（轻量替代方案）
