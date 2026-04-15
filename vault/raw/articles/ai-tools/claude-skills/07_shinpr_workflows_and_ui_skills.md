# shinpr/claude-code-workflows 前端工作流 + ui-skills 工具链深度解析

> **系列**：Claude Code 前端 React 风格 SKILL/Plugin 深度调查  
> **文章编号**：07 / 09  
> **涵盖内容**：shinpr/claude-code-workflows（前端工作流）+ blamsa0mine/ui-skills（UI 工具链）  

---

## Part A：shinpr/claude-code-workflows

### A-1. 基本信息

| 属性 | 值 |
|------|---|
| **仓库** | `shinpr/claude-code-workflows` |
| **最后更新** | 2026年4月（17小时前） |
| **设计思想** | 生产就绪的多 Agent 工作流 |
| **Frontend Plugin** | `dev-workflows-frontend` |
| **技术栈** | React + TypeScript（专用规则内置） |

---

### A-2. 核心概念：Plugins vs Dev-Skills

这个仓库的独特设计是提供**两种不同深度的前端支持**：

**`dev-skills`（技能模式）**：
```
只包含最佳实践知识，不包含工作流 Recipe
- coding-principles：编码原则（实现时激活）
- testing-principles：测试原则（写测试时激活）
- design-guidelines：设计指南
最小 Context 占用，无 Agent 调用
```

**`dev-workflows-frontend`（工作流模式）**：
```
包含 Skills + Agents + Recipes 的完整系统
- 每个开发阶段由专用 Agent 执行
- 多个 Recipe 覆盖前端开发全生命周期
- 每个 Agent 在新鲜上下文中运行（质量不退化）
```

> **重要警告**：不要同时安装 `dev-skills` 和 `dev-workflows-frontend`——它们共享相同 Skills，重复安装会使 description 出现两次，可能触发 Claude Code 的 2% 上下文限制而被静默忽略。

---

### A-3. 安装前端工作流

```bash
# 1. 启动 Claude Code
claude

# 2. 添加 Marketplace 源
/plugin marketplace add shinpr/claude-code-workflows

# 3. 安装前端专用插件
/plugin install dev-workflows-frontend@claude-code-workflows

# 4. 重新加载插件
/reload-plugins

# 5. 开始构建
/recipe-front-design "Add user authentication with login form"
```

---

### A-4. Frontend Plugin 专用 Recipes

#### `/recipe-front-design` — 前端功能设计 Recipe

```
入口：/recipe-front-design <feature description>
          ↓
  requirement-analyzer Agent
  分析功能规模（小/中/大）
  确定是否需要多 Agent 协作
          ↓
  design-architect Agent（大型功能）
  创建前端 Design Doc
  定义组件结构、状态管理方案
  规划 API 集成点
          ↓
  frontend-executor Agent
  使用 React + TypeScript 特定规则执行
  遵循 coding-principles Skill
          ↓
  code-reviewer Agent
  代码质量审查
  检查 TypeScript 类型、组件设计
  验证测试覆盖
```

#### `/recipe-front-review` — 前端代码审查

```
/recipe-front-review
→ 分析当前 Git diff 或指定文件
→ 检查 React 最佳实践
→ 检查 TypeScript 类型安全
→ 输出带优先级的改进建议
```

#### `/recipe-front-test` — 前端测试生成

```
/recipe-front-test <component or feature>
→ 分析组件结构
→ 识别测试边界
→ 生成 Vitest + React Testing Library 测试
→ 包含 happy path, edge cases, error states
```

#### `/recipe-fullstack-implement`（全栈 Recipe）— 跨层级功能

```bash
/recipe-fullstack-implement "Add user authentication with JWT + login form"
```

这个 Recipe 特别有趣：它同时调用**后端 Agent** 和**前端 Agent**，并通过 `design-sync` Agent 验证接口一致性：

```
/recipe-fullstack-implement
        ↓
  后端 Design Doc 创建（API 接口定义）
  前端 Design Doc 创建（组件和状态设计）
        ↓
  design-sync Agent
  验证前后端接口一致性
  检查 TypeScript 类型匹配
        ↓
  根据文件模式（.tsx/.ts）路由到对应 executor
  .tsx → frontend-executor Agent
  .ts（API） → backend-executor Agent
```

---

### A-5. 内置 React/TypeScript 专用规则

Frontend Plugin 在 Skills 中内置了 React/TypeScript 特定的编码规则：

**组件设计规则**：
```typescript
// ✅ 强制：小组件（< 100 行）
// ✅ 强制：明确的 Props interface 定义
// ✅ 强制：显式返回类型（不依赖推断）
// ✅ 强制：组件文件与组件同名

interface UserCardProps {
  userId: string
  onSelect?: (id: string) => void
}

export function UserCard({ userId, onSelect }: UserCardProps): JSX.Element {
  // ...
}
```

**状态管理规则**：
```typescript
// 原则：状态在最近的共同祖先
// 禁止：在叶子组件中管理全局状态
// 推荐：zustand for global state, react-query for server state
// 警告：避免 useEffect 驱动的状态同步（Vercel react-best-practices 同款规则）
```

**文件组织规则**：
```
src/
├── components/         # 共享 UI 组件
│   └── ComponentName/
│       ├── index.tsx   # 组件主文件
│       ├── index.test.tsx
│       └── types.ts    # 组件专属类型
├── features/           # 功能域组件（Colocation 模式）
│   └── auth/
│       ├── LoginForm.tsx
│       ├── LoginForm.test.tsx
│       └── use-auth.ts  # feature-scoped hook
└── hooks/              # 跨功能的共享 hooks
```

---

### A-6. 每个 Agent 运行在新鲜上下文中

这是 shinpr 工作流的核心设计理念：

> Each phase runs in a **fresh agent context**, so quality doesn't degrade as the task grows.

**为什么这重要？**

Claude Code 的上下文窗口有限。当在一个长对话中执行多步骤任务时，早期的信息会被"压缩"，导致后期 Claude 忘记早期决策，产生不一致的输出。

通过让每个 Agent（requirement-analyzer → design-architect → frontend-executor → code-reviewer）在新的上下文窗口中启动，并将必要信息通过**文件系统**传递（而不是对话历史），每个阶段都保持最高质量。

**传递机制**：
```
Agent A 完成 → 写入 design-doc.md
Agent B 启动 → 读取 design-doc.md → 基于文档执行，不依赖对话历史
```

---

## Part B：ui-skills 工具链

### B-1. 基本信息

| 属性 | 值 |
|------|---|
| **来源** | DEV Community 文章（blamsa0mine，2026年1月） |
| **工具** | `npx ui-skills add <skill-name>` |
| **定位** | "打磨 AI 生成的界面"——不是生成，是改善 |

这不是一个单一的仓库，而是一套**专门用于修复 AI 生成前端问题**的 Skills 工具链。

### B-2. 四个核心 Skills

```bash
npx ui-skills add baseline-ui
npx ui-skills add fixing-accessibility
npx ui-skills add fixing-motion-performance
npx ui-skills add fixing-metadata
```

#### `baseline-ui` — 清除 AI UI 糟粕

这个 Skill 处理 AI 生成代码中最常见的"agent UI slop"问题：

**检查并修复的项目**：

```markdown
间距问题：
  - 不一致的 padding/margin（有时 16px，有时 20px，有时 24px）
  - 修复：统一使用 4px 网格系统（4, 8, 12, 16, 24, 32, 48, 64）

排版问题：
  - 字体大小混乱（没有清晰的层级）
  - 行高未设置（导致文字拥挤）
  - 修复：建立清晰的 type scale

视觉层次问题：
  - 每个元素都 bold（没有视觉重量差异）
  - 颜色使用混乱
  - 修复：建立主次关系

状态问题：
  - 缺少 hover state
  - 缺少 focus state  
  - 缺少 disabled state
  - 修复：为所有交互元素添加完整状态
```

#### `fixing-accessibility` — 无障碍修复

```markdown
专注于 AI 最容易遗漏的无障碍问题：

1. focus-visible 替代 focus
   button:focus { outline: none; }              ← ❌
   button:focus-visible { outline: 2px solid; } ← ✅

2. 交互元素的 role 和 label
   <div onClick={...}>                          ← ❌（不是真正的按钮）
   <button onClick={...}>                       ← ✅

3. aria-live 区域（动态内容）
   AI 通常忘记为 toast、alert、status 更新添加 aria-live

4. 图片 alt 文字（AI 经常生成无意义的 alt）
   alt="image"    ← ❌
   alt="User avatar for John Doe"  ← ✅
```

#### `fixing-motion-performance` — 动效性能修复

```markdown
AI 生成的动效常见性能问题：

1. 触发 Layout 重排的属性（性能杀手）
   transition: width, height, margin, padding  ← ❌ 触发 reflow
   transition: transform, opacity              ← ✅ 仅 composite

2. 未遵循 prefers-reduced-motion
   @media (prefers-reduced-motion: reduce) 缺失 ← ❌

3. 过度使用 will-change
   will-change: transform（滥用）              ← ❌ 会增加内存

4. 动效时机问题
   所有元素同时动画（不是 staggered）           ← 效果差
   使用 animation-delay 实现 staggered reveal  ← ✅
```

#### `fixing-metadata` — SEO 和元数据

```markdown
AI 生成的页面通常缺少：

1. <title> 和 <meta description>
2. Open Graph 标签（og:title, og:description, og:image）
3. Twitter Card 标签
4. 规范 URL（<link rel="canonical">）
5. 结构化数据（JSON-LD）

fixing-metadata Skill 检查并补全这些项目。
```

---

### B-3. 推荐的 4 Skill 工作流

DEV Community 文章提出的完整前端开发流程：

```
Step 1: /frontend-design "Build a full-page Habit Tracker + Focus Timer"
        ↓（生成初始设计和代码）

Step 2: /baseline-ui
        ↓（清除间距/排版/状态问题，建立基础规范）

Step 3: /fixing-accessibility
        ↓（添加 ARIA、焦点、键盘导航）

Step 4: /fixing-motion-performance
        ↓（优化动效，添加 prefers-reduced-motion）
```

**作者比喻**：
> Design → Craft → A11y → Perf.

这是一个**渐进质量提升**的流程，而不是一次性生成完美代码。

---

### B-4. 实战示例

**用户请求**：
```
/frontend-design Build a full-page "Habit Tracker + Focus Timer" screen.
```

**技术规范**（用户提供的详细约束，体现了优秀 Prompt 工程）：
```
Stack:
- Vue 3 SFC + <script setup lang="ts">
- TailwindCSS + dark mode
- No external UI libs

UX requirements:
- Full viewport layout: w-screen h-screen
- Sticky top bar with: title, date, "Add habit" button
- Main layout (desktop): Left: Habit list | Right: Focus timer card + session history
- Mobile: single column, timer above list

States: loading / empty / error (mock states ok)

A11y:
- Keyboard navigation (tab order makes sense)
- Visible focus rings
- aria-live for "X habits completed"

Motion:
- Subtle transitions only
- Respect prefers-reduced-motion (motion-reduce:transition-none)
```

生成后依次运行 `/baseline-ui` → `/fixing-accessibility` → `/fixing-motion-performance`，每步解决一类问题。

---

## Part C：两者的对比与选择

| 维度 | shinpr workflows | ui-skills |
|------|-----------------|-----------|
| **复杂度** | 高（多 Agent，全生命周期） | 低（4 个独立 Skill） |
| **适用阶段** | 从 0 开始构建新功能 | 改善/修复已有代码 |
| **Context 使用** | 较高（Agent 调用） | 低（逐步激活） |
| **Team 适用性** | 高（Design Doc 文件传递） | 中（个人工作流） |
| **学习曲线** | 较陡（理解 Recipe/Agent 系统） | 平缓（直接使用） |

**推荐策略**：
- 新项目 / 新功能：`shinpr workflows` → 结构化多 Agent 设计开发
- 迭代改善 / 代码审查：`ui-skills` → 快速逐项修复
- 两者不冲突，可以组合使用

---

## 小结

**shinpr/claude-code-workflows** 的贡献：
1. 证明了 Skills + Agents + Recipes 的组合可以处理真实的中大型前端功能
2. 每个 Agent 运行在新鲜 Context 的设计解决了长上下文质量退化问题
3. React/TypeScript 特定规则内置，不需要开发者配置

**ui-skills 工具链**的贡献：
1. 提供了一个实用的"AI 界面打磨"工作流
2. 明确分离了四类常见问题（基线、无障碍、动效、元数据）
3. 进化方向：从"一次生成好代码"到"迭代改善代码"

---

**下一篇** → `08_shadcn_official_skill_and_ui_pro_max.md`  
shadcn/ui 官方 Skill + UI/UX Pro Max 深度解析：项目感知型 Skill、50 种设计风格数据库、21 调色板

---

*调查时间：2025年4月 | 数据来源：github.com/shinpr/claude-code-workflows, dev.to/blamsa0mine*
