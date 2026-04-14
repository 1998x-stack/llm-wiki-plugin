# GSD 深度解析 · 第五篇
# XML 结构化计划系统：从需求到可执行任务的精确转化

> **上一篇**：[第四篇——多智能体编排架构](./04-multi-agent-orchestration.md)

---

## 一、"告诉 Claude 做什么"的两种方式

**方式 A：自然语言描述**

```
请实现用户登录功能。需要验证用户的邮箱和密码，
登录成功后设置 session，登录失败返回错误。
```

**方式 B：XML 结构化任务**

```xml
<task type="auto">
  <n>创建登录 API 端点</n>
  <files>src/app/api/auth/login/route.ts</files>
  <action>
    POST /api/auth/login 接收 {email: string, password: string}。
    用 Zod 验证输入格式（email 必须是有效邮箱，password 最少 8 位）。
    从 Prisma users 表查询用户（使用 findUnique by email）。
    用 bcryptjs.compare 验证密码哈希（禁止使用 bcrypt，Serverless 兼容问题）。
    成功：用 jose SignJWT 生成 token，设置 httpOnly + Secure cookie，name="auth-token"，
          maxAge=604800（7天），SameSite=Lax。响应 200 + {user: {id, email, name}}。
    密码错误：响应 401 + {error: "Invalid credentials"}（不区分用户不存在还是密码错误）。
    格式错误：响应 400 + {error: "Validation failed", details: ZodError.flatten()}。
  </action>
  <verify>
    pnpm exec ts-node -e "
    const res = await fetch('http://localhost:3000/api/auth/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: 'test@test.com', password: 'correct_password'})
    });
    console.log(res.status, res.headers.get('set-cookie'));
    "
  </verify>
  <done>
    ✅ POST /api/auth/login 存在并可接收请求
    ✅ 有效凭证：200 响应 + Set-Cookie 头包含 auth-token
    ✅ 无效密码：401 响应 + {error: "Invalid credentials"}
    ✅ 格式错误：400 响应 + Zod 错误详情
    ✅ 无 httpOnly 以外的 cookie 泄露
  </done>
</task>
```

两种方式生成的代码质量，在实验中差距显著。GSD 全面采用方式 B，这篇文章解释为什么以及如何设计这个系统。

---

## 二、为什么 XML 比自然语言更适合 AI 任务指令？

### 2.1 语义边界的清晰度

自然语言中，段落边界是软性的。Claude 可能将验证条件理解为实现建议，将错误处理描述理解为可选项。

XML 标签创造了硬性语义边界：
- `<action>` 里的内容 = 必须实现的精确指令
- `<verify>` 里的内容 = 必须运行的验证命令
- `<done>` 里的内容 = 完成的语义定义（Claude 用来判断自己是否真正完成了）

这种硬边界消除了 Claude 在"应该实现什么"上的猜测空间。

### 2.2 Claude 的训练数据中大量存在 XML

Claude 在训练时见过大量结构化 XML 文档（API 文档、配置文件、数据格式）。它对 XML 标签的语义理解比对自然语言段落更一致、更准确。

### 2.3 可机器处理性

GSD 的 plan-checker 需要解析计划文件来提取任务列表、依赖关系、验证命令等信息。XML 使这个解析过程完全可靠——`<depends_on>` 标签的内容就是依赖列表，不需要自然语言理解。

---

## 三、PLAN.md 完整 XML Schema

### 3.1 完整格式

```xml
<!-- 文件：02-01-PLAN.md -->
<!-- 命名规范：{phase}-{plan}-PLAN.md -->

## Phase 2, Plan 1: 项目数据模型与迁移

### 目标
建立项目（Project）实体的数据层，为后续 API 和 UI 奠定基础。

### 依赖
本计划无外部依赖，可作为 Wave 1 与 Plan 02 并行执行。

### 需求覆盖
- REQ-002: 用户可以创建项目 (Model)
- REQ-002: 用户可以编辑项目 (Schema 支持)
- REQ-002: 用户可以删除项目 (Schema 支持，软删除字段)

---

<tasks>

<task type="auto">
  <n>创建 Project Prisma Schema</n>
  <files>prisma/schema.prisma</files>
  <action>
    在 schema.prisma 中添加 Project 模型：

    model Project {
      id          String    @id @default(cuid())
      name        String    @db.VarChar(100)
      description String?   @db.Text
      status      ProjectStatus @default(ACTIVE)
      deletedAt   DateTime?          // 软删除字段
      createdAt   DateTime  @default(now())
      updatedAt   DateTime  @updatedAt
      userId      String
      user        User      @relation(fields: [userId], references: [id], onDelete: Cascade)
      phases      Phase[]
    }

    enum ProjectStatus {
      ACTIVE
      ARCHIVED
      COMPLETED
    }

    注意：
    - 使用软删除（deletedAt）而非硬删除（CONTEXT.md 决策）
    - userId 外键关联到现有 User 模型（已在 Phase 01 实现）
    - 不添加全文搜索索引（out-of-scope，REQUIREMENTS.md 明确）
  </action>
  <verify>npx prisma validate</verify>
  <done>
    ✅ prisma validate 无错误
    ✅ Project 模型包含 id, name, description, status, deletedAt, userId 字段
    ✅ ProjectStatus enum 存在且包含三个值
  </done>
</task>

<task type="auto">
  <n>生成并运行数据库迁移</n>
  <files>prisma/migrations/</files>
  <depends_on>创建 Project Prisma Schema</depends_on>
  <action>
    运行：npx prisma migrate dev --name add-project-model
    
    迁移文件应创建：
    - projects 表（所有字段）
    - projects.user_id 外键到 users.id（CASCADE DELETE）
    - projects.deleted_at 列（可空，索引以优化软删除查询）
    
    运行后验证迁移成功：npx prisma db pull 确认 schema 与数据库一致。
  </action>
  <verify>npx prisma migrate status</verify>
  <done>
    ✅ migrate status 显示所有迁移已应用
    ✅ migrations/ 目录包含新的迁移文件
    ✅ 迁移文件名包含 "add-project-model"
  </done>
</task>

<task type="auto">
  <n>添加 Project 数据访问层（DAL）</n>
  <files>src/lib/dal/projects.ts</files>
  <depends_on>生成并运行数据库迁移</depends_on>
  <action>
    创建 src/lib/dal/projects.ts，遵循现有 DAL 模式（参考 src/lib/dal/users.ts）：

    导出以下函数（全部接受 userId 参数，确保数据隔离）：
    
    getProjects(userId: string): 返回用户的所有未删除项目
      - WHERE userId = ? AND deletedAt IS NULL
      - ORDER BY updatedAt DESC
    
    getProject(userId: string, projectId: string): 返回单个项目
      - 验证 userId 所有权（防止越权访问）
    
    createProject(userId: string, data: CreateProjectInput): 创建项目
      - 使用 Zod schema 验证输入（在 src/lib/validations/project.ts 中定义）
    
    updateProject(userId: string, projectId: string, data: UpdateProjectInput): 更新
      - 验证所有权后更新
    
    softDeleteProject(userId: string, projectId: string): 软删除
      - 设置 deletedAt = new Date()，不实际删除记录
    
    类型定义：
    - CreateProjectInput: { name: string; description?: string }
    - UpdateProjectInput: Partial&lt;CreateProjectInput&gt; &amp; { status?: ProjectStatus }
    
    错误处理：
    - 项目不存在或无权限：throw new NotFoundError("Project not found")
    - 使用项目中现有的 error 类（src/lib/errors.ts）
  </action>
  <verify>pnpm tsc --noEmit</verify>
  <done>
    ✅ tsc 无类型错误
    ✅ src/lib/dal/projects.ts 存在
    ✅ 所有 5 个函数都有正确的 TypeScript 签名
    ✅ 每个函数都包含 userId 验证
  </done>
</task>

</tasks>

### 波次分配
- Wave 1: Task 1（创建 Schema）
- Wave 2: Task 2（依赖 Task 1）, 与 Plan 02 的无依赖任务并行
- Wave 3: Task 3（依赖 Task 2）
```

### 3.2 每个字段的深层设计

**`<n>` — 任务名称**

不仅是标识符，也是 git commit message 的素材来源：
```bash
git commit -m "feat(02-01): 创建 Project Prisma Schema"
git commit -m "feat(02-01): 生成并运行数据库迁移"
```

GSD 要求任务名简洁、动词开头、能独立描述完成的工作。

**`<files>` — 文件路径**

消除 Claude 猜测"应该写到哪里"的歧义。这个字段看起来简单，但在实践中非常重要：

```xml
<!-- ❌ 不好：只说功能不说位置 -->
<files>DAL 层</files>

<!-- ✅ 好：精确到文件路径 -->
<files>src/lib/dal/projects.ts, src/lib/validations/project.ts</files>
```

**`<action>` — 实现指令**

这是 PLAN.md 中信息密度最高的字段，包含：
- **库选型决策**（不是"实现认证"，而是"使用 jose，不用 jsonwebtoken"）
- **边界情况处理**（密码错误和用户不存在都返回同样的错误信息，防止用户枚举）
- **代码级别的规范**（cookie 的 name, maxAge, flags 都明确指定）
- **禁止事项**（明确说明不能做什么，比可以做什么更重要）

**`<verify>` — 可执行验证命令**

这是 XML Schema 中最关键的创新。`<verify>` 中的命令会被 gsd-executor 在任务完成后**真正运行**：

```xml
<!-- 数据库层验证 -->
<verify>npx prisma validate && npx prisma migrate status</verify>

<!-- API 层验证 -->
<verify>curl -s -X POST http://localhost:3000/api/projects \
  -H "Content-Type: application/json" \
  -H "Cookie: auth-token=test_token" \
  -d '{"name":"Test Project"}' | jq '.id'</verify>

<!-- TypeScript 验证 -->
<verify>pnpm tsc --noEmit</verify>

<!-- 单元测试验证 -->
<verify>pnpm test src/lib/dal/projects.test.ts</verify>
```

如果 `<verify>` 命令失败，gsd-executor 会尝试修复（最多 3 次），然后才标记任务完成。这是 GSD 的质量自动闭环机制。

**`<depends_on>` — 任务内依赖**

用于同一 PLAN 内的任务排序（不同 PLAN 之间的依赖用文件头部的元数据声明）：

```xml
<task>
  <n>任务A</n>
  <!-- 无 depends_on：可以立即执行 -->
</task>

<task>
  <n>任务B</n>
  <depends_on>任务A</depends_on>  <!-- 必须在任务A之后 -->
</task>
```

**`<done>` — 完成语义**

这个字段解决了一个微妙但重要的问题：Claude 怎么知道它真的完成了？

没有 `<done>` 时，Claude 倾向于"写完代码就算完成"。但"完成"应该是：
- 代码存在 ✅
- TypeScript 编译无错误 ✅
- 功能按预期工作 ✅
- 边界情况被覆盖 ✅

`<done>` 用清单形式定义了这些完成标准，Claude 逐项检查后才能结束任务。

---

## 四、plan-checker 的 8 维验证体系

gsd-plan-checker 在 gsd-planner 生成计划后立即验证，8 个维度全部通过才允许进入执行阶段。

### 维度一：需求覆盖完整性（Requirement Coverage）

```
检查：本阶段的所有 v1 需求是否都有对应的任务？

验证方法：
  读取 REQUIREMENTS.md 中本阶段的 v1 需求列表（REQ-XXX）
  遍历所有 PLAN.md 文件，提取 <action> 中涉及的功能
  对比两个集合，识别未被覆盖的需求

失败示例：
  REQUIREMENTS.md 包含 REQ-005: 软删除
  但所有 PLAN 文件中都没有软删除的实现任务
  → 计划被拒绝，要求补充
```

### 维度二：技术一致性（Technical Consistency）

```
检查：计划中的技术选型是否与 PROJECT.md 的约束一致？

常见冲突：
  PROJECT.md: "禁止使用 any 类型"
  PLAN.md 中某任务：<action>暂时用 any 类型，后续再改</action>
  → 冲突，要求修改

  PROJECT.md: "数据库使用 PostgreSQL via Prisma"
  PLAN.md 中某任务：<action>使用 raw SQL 查询</action>
  → 冲突，要求修改（除非 PROJECT.md 明确允许部分场景使用 raw SQL）
```

### 维度三：计划原子性（Plan Atomicity）

```
检查：每个 PLAN 文件是否可以在单个 200k 上下文窗口内完成？

评估指标：
  - 涉及的文件数量（超过 20 个文件的计划通常需要拆分）
  - 任务数量（超过 5 个任务的计划通常太大）
  - 任务复杂度（"实现整个认证系统"是一个任务，过于庞大）

失败示例：
  一个 PLAN 文件包含 8 个任务，涉及 35 个文件
  → 要求拆分为 2-3 个更小的计划
```

### 维度四：依赖关系正确性（Dependency Correctness）

```
检查：
  1. 任务间的 <depends_on> 是否正确（没有循环依赖）
  2. 跨 PLAN 的依赖是否合理（依赖的 PLAN 确实会更早执行）
  3. 是否有隐性依赖被遗漏（A 任务使用了 B 任务创建的类型，但没有声明依赖）

DAG 验证：
  构建依赖有向图 → 检测循环 → 验证拓扑排序可行
```

### 维度五：并行安全性（Parallel Safety）

```
检查：同一波次中并行执行的计划是否会产生文件冲突？

文件冲突定义：
  两个同波次的计划都声明了对同一文件的写操作

处理方式：
  检测到冲突 → 建议将冲突任务移到不同波次，或合并为同一计划
  允许并行读同一文件（读操作不冲突）
```

### 维度六：可验证性（Verifiability）

```
检查：每个任务的 <verify> 字段是否包含可执行的验证命令？

不可验证的示例（被拒绝）：
  <verify>确认登录功能正常工作</verify>
  （这是人类描述，不是可运行的命令）

可验证的示例（通过）：
  <verify>curl -s -X POST http://localhost:3000/api/auth/login -d '...' | jq '.status'</verify>
  <verify>pnpm test src/tests/auth.test.ts</verify>
  <verify>pnpm tsc --noEmit && pnpm lint</verify>
```

### 维度七：上下文一致性（Context Consistency）

```
检查：计划的技术决策是否与 CONTEXT.md 中记录的用户偏好一致？

示例：
  CONTEXT.md 记录：用户明确要求使用无限滚动，不用分页按钮
  某 PLAN 的 <action> 中仍然实现了分页按钮
  → 冲突，要求按 CONTEXT.md 修改
```

### 维度八：Nyquist 验证覆盖（Nyquist Validation）

```
检查：VALIDATION.md 是否存在？
      其中每个 v1 需求是否都有对应的自动化测试命令？

如果 VALIDATION.md 不存在：
  要求 gsd-planner 先生成测试覆盖合约

如果存在但覆盖不完整：
  列出缺失覆盖的需求，要求补充
  或者标记为"手动验证"（人工 UAT 覆盖）

可以通过 /gsd:settings 关闭 nyquist_validation
（适用于快速原型阶段，不需要完整测试覆盖）
```

### 验证循环机制

```
gsd-planner 生成计划
       │
       ▼
gsd-plan-checker 验证
       │
    通过？
   ╱      ╲
 Yes        No
  │          │
  │     生成修订意见（具体指出哪个维度不通过、原因、建议修改方向）
  │          │
  ▼          ▼
计划批准   gsd-planner 修订
          │
        通过？
       ╱      ╲
     Yes        No（第 2 次）
      │          │
      ▼          ▼
   批准         再次修订
             │
           通过？
          ╱      ╲
        Yes        No（第 3 次，上报）
         │          │
         ▼          ▼
      批准     报告用户，请求人工干预
```

---

## 五、计划粒度控制（Granularity）

GSD 通过 `granularity` 配置控制整体阶段拆分的细粒度：

| 粒度 | 阶段数（里程碑） | 每阶段 PLAN 数 | 适合场景 |
|------|---------|-------|---------|
| `coarse` | 3-5 个阶段 | 1-2 个 PLAN | 快速原型，概念验证 |
| `standard` | 5-8 个阶段 | 2-3 个 PLAN | 日常开发（默认） |
| `fine` | 8-12 个阶段 | 3-5 个 PLAN | 生产级开发，高质量要求 |

粒度越细，每个 PLAN 越小，执行质量越高，但规划开销也越大。`fine` 模式适合需要最高代码质量的场景（如金融应用、医疗应用）。

---

## 六、SUMMARY.md：执行存档格式

每个 PLAN 执行完成后，gsd-executor 生成对应的 SUMMARY.md：

```markdown
## 执行摘要：02-01（项目数据模型与迁移）

### 执行状态
✅ 全部成功

### 时间轴
2024-03-19 14:32 开始执行
2024-03-19 15:47 执行完成（1小时15分钟）

### Git Commits
- a1b2c3d feat(02-01): 创建 Project Prisma Schema
- d4e5f6g feat(02-01): 生成并运行数据库迁移  
- h7i8j9k feat(02-01): 添加 Project DAL

### 实际完成的工作
- [x] prisma/schema.prisma 添加 Project 模型和 ProjectStatus enum
- [x] 迁移文件 20240319143832_add_project_model.sql 已生成并运行
- [x] src/lib/dal/projects.ts 包含 5 个函数（getProjects, getProject, createProject, updateProject, softDeleteProject）
- [x] src/lib/validations/project.ts 包含 Zod schema

### 关键决策记录
- 确认使用软删除（设置 deletedAt）而非硬删除，与 CONTEXT.md 决策一致
- DAL 函数全部包含 userId 参数，确保数据隔离

### 偏差说明
- 无偏差，完全按照 PLAN 执行

### 影响的文件
- prisma/schema.prisma（修改）
- prisma/migrations/20240319xxx/（新增）
- src/lib/dal/projects.ts（新增）
- src/lib/validations/project.ts（新增）
```

SUMMARY.md 是 GSD 的"工程日志"，记录了 AI 真正做了什么，而不仅仅是计划要做什么。gsd-verifier 和未来会话的 `/gsd:resume-work` 都会读取这些文件。

---

## 七、实践建议：如何写出好的 PLAN

（GSD 会自动生成，但理解原则有助于审查和修改）

**原则一：action 字段写"不能做什么"和"为什么"**

```xml
<!-- ❌ 弱：只说能做什么 -->
<action>实现密码验证功能，使用加密库</action>

<!-- ✅ 强：包含禁止事项和理由 -->
<action>
使用 bcryptjs（不用 bcrypt——bcrypt 有 Node.js Serverless 兼容问题）。
轮数 rounds=12（平衡安全性和响应时间：bcrypt 在 rounds=12 时约 100-300ms）。
禁止在日志中输出密码或密码哈希（即使是 debug 日志）。
</action>
```

**原则二：verify 要真正运行，不能只是描述**

```xml
<!-- ❌ 不可执行 -->
<verify>确认密码验证正常工作</verify>

<!-- ✅ 可执行 -->
<verify>
pnpm test src/__tests__/auth/password.test.ts
</verify>
```

**原则三：done 用清单而不是叙述**

```xml
<!-- ❌ 叙述式（模糊） -->
<done>登录功能已完整实现，包含验证和错误处理</done>

<!-- ✅ 清单式（明确） -->
<done>
✅ POST /api/auth/login 返回 200 + cookie（有效凭证）
✅ POST /api/auth/login 返回 401（无效凭证）
✅ POST /api/auth/login 返回 400（格式错误）
✅ cookie 包含 httpOnly + Secure 标志
✅ pnpm tsc --noEmit 无错误
</done>
```

---

## 小结

GSD 的 XML 计划系统本质上是将软件工程的最佳实践编码化：
- 精确的任务定义（`<action>`）= 减少实现歧义
- 可执行的验证（`<verify>`）= 自动化质量闭环
- 明确的完成定义（`<done>`）= 消除"完成"的主观判断
- 8 维 plan-checker = 多层质量过滤

这套系统让 AI 从"随意发挥"变为"在精确约束下执行"，是 GSD 能够一致产出高质量代码的核心机制之一。

下一篇，我们看 GSD 的 UI 设计契约系统——如何解决 AI 生成前端代码视觉不一致的问题。

---

*参考：[GSD GitHub](https://github.com/gsd-build/get-shit-done) · [USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)*
