# GSD 深度解析 · 第二篇
# `.planning/` 上下文文件系统：AI 项目的持久化大脑

> **上一篇**：[第一篇——Context Rot 与 GSD 五大支柱](./01-overview-context-rot.md)

---

## 一、为什么需要外部化的项目记忆？

LLM 没有持久化记忆。每次新会话，Claude 的记忆都从零开始。即使在同一个会话内，随着上下文窗口填满，早期信息也会逐渐"淡出"注意力范围。

传统解决方案：把一切塞进 `CLAUDE.md`。这个方案对简单项目有效，但有三个根本性缺陷：

1. **无差别加载**：无论当前任务是什么，所有信息都被加载，造成 token 浪费和噪声增加
2. **单文件无结构**：随着项目增长，`CLAUDE.md` 变成混乱的信息垃圾场
3. **无版本化需求**：没有 v1/v2/out-of-scope 区分，Claude 总是试图实现所有东西

GSD 的答案是 **`.planning/` 目录**——一个结构化的、按需加载的、多文件的项目外部记忆系统。

---

## 二、`.planning/` 完整目录结构

```
.planning/
├── PROJECT.md              # 项目愿景锚点（每次调用都加载）
├── REQUIREMENTS.md         # 版本化需求边界
├── ROADMAP.md              # 阶段路线图 + 状态追踪
├── STATE.md                # 跨会话工程记忆
├── config.json             # 工作流配置（20+ 参数）
├── MILESTONES.md           # 已完成里程碑存档
├── HANDOFF.json            # 会话切换快照
├── research/               # 项目级领域研究（new-project 时生成）
│   ├── domain.md
│   ├── stack.md
│   └── pitfalls.md
├── seeds/                  # 前瞻性想法（带触发条件）
│   └── SEED-001-realtime-collab.md
├── threads/                # 跨会话轻量知识存储
│   └── tcp-timeout-investigation.md
├── todos/
│   ├── pending/            # 待处理的想法
│   └── done/               # 已完成的 todo
├── debug/                  # 活跃调试会话
│   └── resolved/           # 已解决的调试存档
├── codebase/               # 棕地代码库分析（map-codebase 时生成）
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   └── CONCERNS.md
├── reports/                # 会话报告（session-report 时生成）
└── phases/
    └── 01-user-auth/       # 每个阶段的独立目录
        ├── CONTEXT.md      # 实现偏好（discuss-phase 生成）
        ├── RESEARCH.md     # 领域研究（plan-phase 生成）
        ├── 01-01-PLAN.md   # 原子执行计划（XML）
        ├── 01-02-PLAN.md
        ├── 01-01-SUMMARY.md # 执行存档
        ├── 01-02-SUMMARY.md
        ├── 01-UI-SPEC.md   # UI 设计契约（ui-phase 生成）
        ├── 01-UI-REVIEW.md # 视觉审计结果（ui-review 生成）
        ├── VERIFICATION.md  # 后验证结果
        └── VALIDATION.md   # 测试覆盖合约（Nyquist 层）
```

---

## 三、核心文件逐一深析

### 3.1 PROJECT.md — 项目愿景锚点

**作用**：这是唯一在**所有**命令中都被加载的文件。它是 Claude 理解"这个项目是什么"的基础。

**内容设计原则**：
- 控制在 **2-3 页以内**（GSD 设有大小限制，超出会影响其他信息的注意力权重）
- 只记录 AI 真正需要的信息，不记录人类对话式的"背景故事"
- 包含：项目愿景、核心用户、关键技术选型、非功能性约束、禁止事项

**一个好的 PROJECT.md 示例结构**：

```markdown
## 项目愿景
面向独立开发者的项目管理工具。核心价值：30秒内能描述项目状态。

## 技术栈（锁定，不可更改）
- Runtime: Next.js 14 App Router + TypeScript (strict)
- Database: PostgreSQL via Prisma ORM
- Auth: NextAuth.js v5
- UI: Tailwind CSS + shadcn/ui

## 关键约束
- 所有 API 路由必须有 Zod 验证
- 禁止使用 any 类型
- 错误信息必须用户友好，不暴露内部堆栈

## 明确不做的事
- 不支持团队协作（v1 仅 solo 使用）
- 不支持移动端原生 App
```

**为什么不把所有信息都放这里**：PROJECT.md 越大，每次调用的 token 开销越大，同时它本身的信息密度越低（因为 Claude 需要"找"关键信息）。GSD 的设计哲学是：PROJECT.md 应该是高密度、永远相关的核心契约。

---

### 3.2 REQUIREMENTS.md — 版本化需求边界

**作用**：这是防止 AI 过度实现（Over-engineering）的核心护栏。

**关键设计**：三级需求分类

```markdown
## v1 需求（本里程碑必须实现）
- REQ-001: 用户可以用邮件+密码注册账户
- REQ-002: 用户可以创建和编辑项目
- REQ-003: 每个项目可以有多个阶段，阶段可以设置状态

## v2 需求（下个里程碑考虑）
- REQ-101: 支持 GitHub OAuth 登录
- REQ-102: 项目可以设置截止日期和提醒

## Out of Scope（永远不做，除非明确决策更改）
- 团队协作/多用户项目
- 移动端 App
- AI 自动化功能
```

**为什么 out-of-scope 如此重要**：Claude 天然倾向于"帮你多做一些"。如果没有明确的 out-of-scope 声明，它可能在实现登录功能时顺手加入邀请团队成员的代码。这些未经计划的实现会引入依赖、增加复杂度、破坏计划的原子性。

**需求 ID 的可追溯性**：GSD 的 PLAN.md 会引用 REQ-XXX 编号，plan-checker 的第一个验证维度就是检查计划是否覆盖了本阶段对应的所有 v1 需求。

---

### 3.3 ROADMAP.md — 阶段路线图

**作用**：全局进度追踪，但不是详细规格文档。

**设计原则**：每个阶段只有**一句话描述**，不是完整的功能规格。详细规格留给 PLAN.md。

```markdown
## Milestone v1.0: MVP 用户认证与项目管理

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| 01 | 用户认证系统 | ✅ 完成 | 注册、登录、会话管理 |
| 02 | 项目 CRUD | 🔄 进行中 | 项目创建、编辑、删除 |
| 03 | 阶段管理 | ⏳ 待开始 | 阶段的增删改查 |
| 04 | Dashboard | ⏳ 待开始 | 项目概览与状态展示 |

## 定义完成
- 所有 v1 需求通过 UAT
- 测试覆盖率 > 80%
- 无已知 P0/P1 bug
```

**`/gsd:progress` 读取此文件**，向你展示当前位置和下一步建议。

---

### 3.4 STATE.md — 跨会话工程记忆

**作用**：这是 GSD 实现"会话记忆"的核心机制。每次会话开始时，`/gsd:resume-work` 读取 STATE.md 恢复上下文；每次重要决策或会话结束时，GSD 更新 STATE.md。

**STATE.md 典型内容**：

```markdown
## 当前位置
- 里程碑: v1.0 MVP
- 当前阶段: Phase 02 (项目 CRUD)
- 当前步骤: 已完成 plan-phase，准备执行 execute-phase

## 关键技术决策（已定锁，不再讨论）
- 2024-03-15: 选择 Prisma 而非 Drizzle（团队更熟悉）
- 2024-03-16: 使用 jose 而非 jsonwebtoken（CommonJS 兼容问题）
- 2024-03-18: 不实现软删除（v1 复杂度控制）

## 当前阻塞项
- Vercel 部署 PostgreSQL 连接字符串格式问题（待解决）

## 待讨论事项
- Phase 03 的阶段依赖关系设计（是否允许循环依赖？）

## 上次会话摘要（2024-03-18）
完成了 Phase 01 用户认证，所有 UAT 通过，已创建 PR #3。
Phase 02 计划生成完毕，共 3 个 PLAN 文件，依赖关系：Plan01 和 Plan02 可并行，Plan03 依赖两者。
```

**STATE.md 是 GSD 实现"无遗忘跨会话协作"的关键**。它不是会话历史的完整复制，而是精心提炼的工程状态快照。

---

### 3.5 CONTEXT.md — 单阶段实现偏好

**作用**：捕获你对特定阶段的实现偏好，是 `discuss-phase` 命令的产物。

**为什么需要独立的 CONTEXT.md**？

ROADMAP.md 的阶段描述只有一句话，这远远不够。考虑一个"用户 Dashboard"阶段：

- 布局是单列还是网格？
- 数据更新是轮询还是 WebSocket？
- 空状态时显示引导还是示例数据？
- 是否需要暗色模式？

这些决策不应该由 Claude 自己做——它会做出"合理但不是你想要的"选择。CONTEXT.md 就是在执行前锁定这些决策的机制。

**CONTEXT.md 同时被两个下游步骤读取**：

```
discuss-phase 生成 CONTEXT.md
         │
         ├──→ gsd-phase-researcher 读取
         │    "用户想要卡片式布局" → 研究卡片组件最佳实践
         │    "用户想要实时更新" → 研究 WebSocket vs SSE
         │
         └──→ gsd-planner 读取
              "用户想要卡片式布局" → PLAN 中直接指定组件选型
              "用户不需要暗色模式" → PLAN 不包含主题切换任务
```

这个双向读取是 CONTEXT.md 设计的精妙之处——研究者知道该研究什么，规划者知道什么已经决定了。

---

### 3.6 RESEARCH.md — 阶段专属领域研究

**作用**：4 个并行研究子智能体的研究结论汇总，是 gsd-planner 的核心输入。

**四个研究维度**：

```markdown
## 技术栈研究（gsd-stack-researcher）
当前使用 Next.js 14 App Router，WebSocket 在 App Router 中的支持情况：
- 原生 App Router 不支持 WebSocket（只支持 HTTP streaming）
- 推荐方案：使用 socket.io 配合独立 Node.js 服务，或改用 SSE
- 推荐：采用 SSE（Server-Sent Events），完全兼容 App Router，无需独立进程
- 备选库：EventSource polyfill for IE（如果需要 IE 兼容）

## 功能实现研究（gsd-features-researcher）
SSE 实现最佳实践：
- 使用 Route Handler 中的 ReadableStream
- 客户端用 EventSource API 订阅
- 注意：SSE 只支持服务端→客户端单向推送，适合仪表盘数据刷新场景

## 架构模式研究（gsd-architecture-researcher）
Dashboard 数据层设计建议：
- 使用 React Query (TanStack Query) 管理服务端状态
- SSE 事件触发 React Query 手动 invalidate，而非直接更新 UI 状态
- 这样可以保持数据层的单一真相来源

## 常见陷阱研究（gsd-pitfalls-researcher）
- SSE 连接在 Vercel 上有 10 秒超时限制，需要配置 maxDuration
- Safari 不支持 EventSource 的 withCredentials（跨域 SSE 需要额外处理）
- 避免在每个组件中独立创建 SSE 连接，应使用 Context 共享单一连接
```

**RESEARCH.md 的大小控制**：GSD 要求研究报告精炼，不是完整的技术文档，而是决策相关的关键发现。过长的研究报告会稀释 PLAN 阶段的信号质量。

---

### 3.7 PLAN.md — 原子执行计划

**作用**：执行子智能体的唯一输入。每个 PLAN 文件包含 2-3 个 XML 结构化任务，是执行的最小可信单元。

完整格式见**第五篇**（XML 结构化计划系统），这里只说文件设计原则：

**原子性**：每个 PLAN 文件应该可以在**一个干净的 200k 上下文窗口**内完全执行。如果一个计划需要超过 150 个文件操作，它太大了，应该拆分。

**文件命名**：`{phase}-{plan}-PLAN.md`，例如 `02-01-PLAN.md` 表示第 2 阶段第 1 个计划。

---

### 3.8 SUMMARY.md — 执行存档

**作用**：记录实际发生了什么，形成永久性工程日志。

**SUMMARY.md 典型内容**：

```markdown
## 执行结果
状态：✅ 成功
执行时间：2024-03-18 15:32 - 16:47
Git Commits: abc123f, def456g, hij789k

## 完成的任务
- ✅ Task 1: 用户数据库 Schema + Prisma 迁移
- ✅ Task 2: 密码哈希（bcrypt, rounds=12）
- ✅ Task 3: 登录 API 端点（返回 JWT cookie）

## 关键决策记录
- 选择 bcrypt rounds=12（平衡安全性和登录响应时间）
- JWT expiry 设为 7 天（可通过 env 配置）

## 偏差说明
- 原计划包含邮件验证，但 Resend API 配置问题导致推迟到下一个 Plan
- 已在 STATE.md 记录此偏差，Plan 03 将补充实现

## 影响的文件
- src/lib/auth.ts (新增)
- src/app/api/auth/login/route.ts (新增)
- prisma/schema.prisma (修改)
- prisma/migrations/xxx (新增)
```

---

### 3.9 VALIDATION.md — Nyquist 验证层（v1.26 新增）

**作用**：在计划执行前，将每个需求映射到可运行的自动化测试命令，形成"验证合约"。

**为什么叫 Nyquist 层**？类比奈奎斯特采样定理——为了可靠地"采样"到代码质量信号，需要在编码之前就设计好足够密度的测试覆盖。

```markdown
## 需求-测试映射表

| 需求 ID | 需求描述 | 测试命令 | 覆盖类型 |
|---------|----------|---------|---------|
| REQ-001 | 用户注册成功 | `pnpm test auth/register.test.ts` | 单元测试 |
| REQ-001 | 重复邮件拒绝 | `pnpm test auth/register.test.ts -t "duplicate"` | 单元测试 |
| REQ-002 | 登录返回 cookie | `pnpm test:e2e login.spec.ts` | E2E 测试 |
| REQ-002 | 无效密码返回 401 | `pnpm test:e2e login.spec.ts -g "invalid"` | E2E 测试 |

## Wave 0 任务（必须在实现前完成的测试脚手架）
- [ ] 创建 auth 测试的 Mock Prisma Client
- [ ] 配置 Playwright E2E 测试环境
```

**plan-checker 的第 8 个验证维度**就是检查 VALIDATION.md 是否存在且覆盖了本阶段所有 v1 需求。不通过则计划无法被批准执行。

---

### 3.10 其他重要文件

**HANDOFF.json** — `/gsd:pause-work` 时生成，JSON 格式的精确会话快照：

```json
{
  "timestamp": "2024-03-18T16:47:00Z",
  "phase": 2,
  "plan": "02-01",
  "status": "plan_complete_ready_to_execute",
  "blocking_issues": ["Resend API key not configured"],
  "immediate_next_step": "Run /gsd:execute-phase 2",
  "context_summary": "Phase 2 planning done. 3 plans ready. Plans 01+02 parallel, Plan 03 depends on both."
}
```

**Seeds** — 带触发条件的前瞻想法：

```markdown
# SEED-003: 实时协作功能

## 想法
当多个用户同时编辑同一个项目时，支持实时看到对方的变更。

## 触发条件
当 WebSocket/Realtime 基础设施就绪，且用户数超过 1000 时考虑实现。

## 当前阻塞原因
v1 仅支持 solo 使用，基础设施尚未就绪。

## 参考
Liveblocks 和 PartyKit 是可选的实现方案。
```

`/gsd:new-milestone` 时自动扫描所有 Seeds，匹配触发条件则弹出提示。

---

## 四、文件加载策略：按需注入的上下文矩阵

GSD 不同命令加载不同的文件子集：

| 命令 | PROJECT | REQUIREMENTS | ROADMAP | STATE | CONTEXT | RESEARCH | PLAN |
|------|---------|-------------|---------|-------|---------|----------|------|
| new-project | - | 生成 | 生成 | 生成 | - | - | - |
| discuss-phase | ✅ | ✅ | ✅ | ✅ | 生成 | - | - |
| plan-phase | ✅ | ✅ | ✅ | - | ✅ | 生成 | 生成 |
| execute-phase（子智能体） | ✅ | - | - | - | - | - | ✅（仅当前） |
| verify-work | ✅ | ✅ | - | - | ✅ | - | - |
| resume-work | ✅ | - | ✅ | ✅ | - | - | - |

执行子智能体是最严格的——**它只拿到 PROJECT.md 和当前 PLAN.md**，其余所有"背景信息"已经被蒸馏进了 PLAN 的 `<action>` 字段里。

---

## 五、棕地项目的特殊处理：codebase/ 目录

对于已有代码的项目，`/gsd:map-codebase` 会并行 spawn 4 个代码库分析子智能体：

```
gsd-stack-mapper      → codebase/STACK.md（技术栈清单）
gsd-arch-mapper       → codebase/ARCHITECTURE.md（架构模式）
gsd-convention-mapper → codebase/CONVENTIONS.md（命名/结构约定）
gsd-concern-mapper    → codebase/CONCERNS.md（技术债务/风险点）
```

之后运行 `new-project` 时，GSD 读取这 4 个文件，将提问聚焦在"你想**新增**什么"而不是"整个项目是什么"，规划也自动继承现有约定。

---

## 小结

`.planning/` 目录的设计哲学是：**外部化项目记忆，结构化信息流，按需注入上下文**。

每个文件都有精确的职责边界：
- PROJECT.md 是永恒的锚点
- REQUIREMENTS.md 是版本护栏
- STATE.md 是跨会话记忆
- CONTEXT.md 是阶段决策捕获
- PLAN.md 是执行最小单元
- VALIDATION.md 是质量合约

这套文件系统让 GSD 能做到：任何时候从任何状态恢复，每次执行都在干净的上下文中进行，整个项目生命周期质量保持一致。

下一篇，我们将深入工作流的每一步，看这些文件如何在 `new-project → discuss → plan → execute → verify` 链路中被生成和消费。

---

*参考：[GSD GitHub](https://github.com/gsd-build/get-shit-done) · [USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)*
