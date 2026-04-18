---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["ORM", "数据库", "TypeScript", "Node.js", "工具与框架"]
aliases: ["Prisma ORM", "Prisma Client"]
relates_to:
  - target: "[[Next.js]]"
    type: uses
    confidence: 0.8
  - target: "[[TypeScript]]"
    type: uses
    confidence: 0.9
  - target: "[[PostgreSQL]]"
    type: depends_on
    confidence: 0.85
supersedes: null
---

# Prisma

## 概述
[[TypeScript]] 和 Node.js 生态的下一代 ORM，通过声明式 schema 定义数据库模型，提供类型安全的查询 API 和可视化数据管理工具。

## 关键内容

1. **声明式 Schema**：通过 `prisma/schema.prisma` 文件以 DSL 定义数据模型，支持关系定义、枚举类型和默认值配置。模型命名采用 PascalCase 单数形式（如 `User`、`BlogPost`）。

2. **迁移管理**：`npx prisma migrate dev` 执行数据库迁移并同步 schema 状态，迁移历史存储在 `prisma/migrations/` 目录中，不应手动编辑。执行前需确保 `DATABASE_URL` 环境变量可连接。

3. **核心命令**：
   - `prisma migrate dev` — 开发环境迁移
   - `prisma studio` — 启动 GUI 数据浏览器
   - `prisma db seed` — 导入种子测试数据
   - `prisma generate` — 生成类型安全的 Client 代码

4. **环境变量**：通过 `.env.local` 配置 `DATABASE_URL`，支持 [[PostgreSQL]]、MySQL、[[SQLite]] 等数据库。[[PostgreSQL]] 连接需设置 connection pool timeout 防止长时间空闲后断开。

5. **在 [[Ralph Loop]] 中的角色**：AGENTS.md 模板中作为默认数据库层工具，与 [[Next.js]] App [[网关与路由器|Router]] 和 [[TypeScript]] 配合构成全栈开发基线。

## 来源
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — Ralph Loop 项目约定模板

## 相关
- [[Next.js]] — uses（常搭配的全栈框架）
- [[TypeScript]] — uses（原生类型支持）
- [[PostgreSQL]] — depends_on（首选数据库）
