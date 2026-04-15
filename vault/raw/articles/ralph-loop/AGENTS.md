# AGENTS.md — Project Convention Manual

> **Read this at the START of every Ralph session.**  
> This file is maintained by agents. When you discover new patterns, update this file.
> Keep it concise — every token here is token budget spent.

---

## Project Overview

**Project**: [PROJECT_NAME]  
**Tech Stack**: [TECH_STACK]  
**Dev Server**: http://localhost:[PORT]  
**Created**: [DATE]

---

## How to Run

```bash
# Start everything
bash init.sh           # Starts dev server, waits for READY

# Development
npm run dev            # Next.js dev server (if not using init.sh)
npm run build          # Production build
npm run type-check     # TypeScript check only

# Database (if using Prisma)
npx prisma migrate dev # Run migrations
npx prisma studio      # GUI for database
npx prisma db seed     # Seed test data

# Testing
npm test               # Run all tests
npm test -- auth       # Run tests matching "auth"

# Verification
python3 scripts/verify-story.py [story-id]
bash scripts/verify-api.sh [story-id]
```

---

## File Structure

```
src/
├── app/               ← Next.js App Router pages & layouts
│   ├── (auth)/       ← Route group: auth pages
│   ├── (dashboard)/  ← Route group: protected pages
│   └── api/          ← API routes
├── components/        ← Reusable React components
│   ├── ui/           ← Base UI components (Button, Input, etc.)
│   └── features/     ← Feature-specific components
├── lib/               ← Utilities and helpers
├── types/             ← TypeScript type definitions
└── hooks/             ← Custom React hooks

prisma/
├── schema.prisma      ← Database models
└── migrations/        ← Migration history (don't edit manually)
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| React Components | PascalCase | `UserProfile.tsx` |
| Utility Functions | camelCase | `formatDate.ts` |
| API Routes | kebab-case path | `/api/user-profile/route.ts` |
| Database Models | PascalCase singular | `User`, `BlogPost` |
| CSS Classes | Tailwind utilities | `className="flex items-center gap-2"` |
| Test Files | Same name + `.test` | `auth.test.ts` |

---

## Code Conventions

```typescript
// ✅ Correct: Use Server Components by default in App Router
// app/dashboard/page.tsx
export default async function DashboardPage() {
  const data = await fetchData(); // direct async/await
  return <Dashboard data={data} />;
}

// ✅ Correct: Client components only when needed
// components/interactive-button.tsx
'use client';
export function InteractiveButton() { ... }

// ✅ Correct: API routes use Route Handlers
// app/api/users/route.ts
export async function GET(request: Request) { ... }
export async function POST(request: Request) { ... }

// ✅ Correct: Error handling in API routes
export async function POST(request: Request) {
  try {
    const body = await request.json();
    // validate, process...
    return Response.json({ success: true, data: result });
  } catch (error) {
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```

---

## NEVER DO

```
❌ Never delete or modify tests that currently pass
❌ Never set passes: true in prd.json without running the actual verification
❌ Never commit code that fails to build (npm run build must succeed)
❌ Never leave half-implemented features uncomitted (git stash or revert)
❌ Never modify prd.json acceptanceCriteria or descriptions
❌ Never skip the startup ritual in CLAUDE.md
❌ Never hardcode secrets or API keys (use .env.local)
```

---

## Environment Variables

```bash
# .env.local (gitignored, create from .env.example)
DATABASE_URL="postgresql://localhost:5432/[project]_dev"
NEXTAUTH_SECRET="[generate with: openssl rand -base64 32]"
NEXTAUTH_URL="http://localhost:3000"
```

---

## Known Issues & Gotchas

> This section is maintained by Ralph agents. Add here when you discover issues.

<!-- 示例（运行后由 Agent 填充实际内容）:
- PostgreSQL 连接: 必须设置 connection pool timeout，否则长时间无操作后断开
- Next.js 14 App Router: middleware.ts 必须在 src/ 目录外（项目根目录）
- Prisma: 执行 migrate dev 前必须确保 DATABASE_URL 可连接
-->

*(由 Ralph agents 在运行过程中自动填充)*

---

## Learnings from Previous Sessions

> Patterns, discoveries, and optimizations found during development.

*(由 Ralph agents 在运行过程中自动填充)*

---

## Dependency Map

*(PRD 依赖关系图 — 由初始化 Agent 填充)*

```
setup-001 (基础环境)
    ├── auth-001 (注册)
    │       └── auth-002 (登录)
    │               └── auth-003 (登出)
    │               └── profile-001 (查看资料)
    │                       └── profile-002 (编辑资料)
    ├── api-001 (健康检查)
    └── ui-001 (导航栏)
```
