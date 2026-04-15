# jezweb/claude-skills Frontend Plugin 深度解析

> **系列**：Claude Code 前端 React 风格 SKILL/Plugin 深度调查  
> **文章编号**：04 / 09  
> **来源仓库**：[github.com/jezweb/claude-skills](https://github.com/jezweb/claude-skills)  
> **Stars**：615 ⭐ | **Forks**：47  
> **设计者**：Jeremy Dawes (Jez)  
> **Plugin 总数**：10 plugins，63 skills  
> **Frontend Plugin Skills 数量**：10 skills  

---

## 一、项目定位与设计哲学

jezweb/claude-skills 是社区最活跃的 Claude Code Skills 仓库之一，其设计哲学与 Anthropic 官方 Skills 存在根本性差异：

### 官方 Anthropic Skills vs jezweb Skills

| 维度 | Anthropic 官方 | jezweb |
|------|--------------|--------|
| **设计目标** | 设计哲学 + 美学指导 | 工程实现 + 错误预防 |
| **核心承诺** | "避免 AI Slop" | "每个 Skill 必须产出可见成果" |
| **Skill 内容** | 原则和方向 | 具体命令、代码片段、Recipes |
| **错误处理** | 不涉及 | 明确列出 documented errors 数量 |
| **版本锁定** | 无 | 明确标注兼容版本 |
| **ERRATA 机制** | 无 | 有 ERRATA.md 管理版本变更 |

**项目最核心的原则**（来自 CLAUDE.md）：

> **"The context window is a public good"** — only include what Claude doesn't already know.

> **"Teach patterns, not ship scripts"** — skills describe what to do; Claude generates scripts adapted to your environment.

> Every skill must produce **visible output** (files, configurations, deployable projects).

---

## 二、Frontend Plugin 完整结构

```
plugins/frontend/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── tailwind-theme-builder/    # Tailwind v4 主题基础设施
    ├── shadcn-ui/                 # shadcn/ui 组件安装与配置
    ├── landing-page/              # 落地页生成
    ├── product-showcase/          # 产品展示页
    ├── react-patterns/            # React 19 性能与组合模式
    ├── design-review/             # 设计质量审查
    ├── react-native/              # React Native + Expo
    ├── design-loop/               # 迭代设计循环工作流
    ├── design-system/             # 完整设计系统构建
    └── walkthrough-video/         # 网页功能演示视频录制
```

**安装方式**：
```bash
/plugin marketplace add jezweb/claude-skills
/plugin install frontend@jezweb-skills
```

---

## 三、核心 Skill 深度解析

### 3.1 `tailwind-theme-builder` — Tailwind v4 主题工程

这是 Frontend Plugin 中**最重要**的基础 Skill，其他 Skills 几乎都依赖它。

**触发条件**：
```
tailwind v4, shadcn/ui 初始化, 主题配置, dark mode, 
@theme inline, @plugin directive, CSS 变量不工作
```

**解决的核心问题：Tailwind v4 的破坏性变更**

Tailwind CSS v4 相比 v3 有重大变化，这是 AI 工具最容易出错的领域之一：

| 变更项 | v3 方式 | v4 方式 |
|-------|---------|---------|
| 配置文件 | `tailwind.config.ts` | 删除！在 CSS 中配置 |
| Vite 插件 | `tailwindcss()` (PostCSS) | `@tailwindcss/vite` 插件 |
| 动画库 | `tailwindcss-animate` | `tw-animate-css`（v4 专用） |
| 主题扩展 | `extend: { colors: {...} }` | `@theme inline { --color-*: }` |
| CSS 导入 | `@tailwind base; @tailwind components` | `@import "tailwindcss"` |

**强制四步架构模式（Mandatory Pattern）**：

```css
/* src/index.css — 严格按此顺序 */

/* Step 1: 导入基础 */
@import "tailwindcss";
@import "tw-animate-css";   /* shadcn/ui 动画依赖 */

/* Step 2: 定义 CSS 变量（在 :root，NOT 在 @layer base）*/
:root {
  --background: hsl(0 0% 100%);     /* ⚠️ 必须有 hsl() wrapper */
  --foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(221.2 83.2% 53.3%);
  --primary-foreground: hsl(210 40% 98%);
  --secondary: hsl(210 40% 96.1%);
  --border: hsl(214.3 31.8% 91.4%);
  --radius: 0.5rem;
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
}

/* Step 3: 映射到 Tailwind utility 类 */
@theme inline {
  --color-background: var(--background);   /* → bg-background 类 */
  --color-foreground: var(--foreground);   /* → text-foreground 类 */
  --color-primary: var(--primary);         /* → bg-primary 类 */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: var(--radius);
  --radius-lg: calc(var(--radius) + 4px);
}

/* Step 4: 应用基础样式 */
@layer base {
  body {
    background-color: var(--background);   /* ⚠️ 不加 hsl() wrapper */
    color: var(--foreground);
  }
}
```

**预防的 8 个 documented errors**：

1. `tw-animate-css` 缺失导致 shadcn 动画失效
2. CSS 变量未加 `hsl()` wrapper 导致颜色不渲染
3. `@theme inline` 的 dark mode 切换失效（已知 Bug）
4. 残留 `tailwind.config.ts` 与 v4 冲突
5. `@apply` 在 v4 中的使用限制
6. 多个 `@layer base` 块的级联问题
7. `@plugin directive` 语法错误
8. v3 → v4 迁移后路径别名配置失效

**vite.config.ts 正确配置**：
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'  // v4 专用导入
import path from 'path'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),  // v4 插件，不再是 postcss
  ],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') }
  }
})
```

---

### 3.2 `shadcn-ui` — shadcn/ui 组件工程 Skill

**定位**：在 `tailwind-theme-builder` 建立好主题基础设施后，用于安装、配置、组合 shadcn/ui 组件。

**核心规则（shadcn/ui 最重要的使用原则）**：

```tsx
// ❌ 错误：直接使用原始 Tailwind 颜色
<Button className="bg-blue-500 text-white">Submit</Button>

// ✅ 正确：使用语义化 token
<Button className="bg-primary text-primary-foreground">Submit</Button>
<Card className="bg-card text-card-foreground border-border">...</Card>
```

**组件安装顺序规范**（依赖关系驱动）：

```bash
# Foundation 层（必须先装）
pnpm dlx shadcn@latest add button
pnpm dlx shadcn@latest add input label
pnpm dlx shadcn@latest add card

# Overlay 层（依赖 Foundation）
pnpm dlx shadcn@latest add dialog sheet popover

# Form 层（依赖 Foundation + Input）
pnpm dlx shadcn@latest add form  # 自动安装 react-hook-form + zod

# Data 层
pnpm dlx shadcn@latest add table
pnpm dlx shadcn@latest add select dropdown-menu
```

**Recipes（来自 `references/recipes.md`）**：

| Recipe | 使用的组件 |
|--------|-----------|
| 联系表单 | Form + Input + Textarea + Button + Toast |
| 数据表格 | Table + Pagination + Select + Badge |
| 导航菜单 | NavigationMenu + Sheet (mobile) |
| 确认对话框 | AlertDialog + Button |
| 命令面板 | Command + Dialog + Badge |

**自定义 Variant 示例**：
```typescript
// components/ui/button.tsx — 添加 brand variant
const buttonVariants = cva("...", {
  variants: {
    variant: {
      default: "bg-primary text-primary-foreground hover:bg-primary/90",
      brand: "bg-brand text-brand-foreground hover:bg-brand/90",  // 新增
      // ... 其他 variants
    },
  },
})
```

---

### 3.3 `react-patterns` — React 19 性能与组合模式

**定位**：专注于 React 19 引入的新 API 和现代化的组合设计模式。

**核心内容领域**：

#### React 19 新特性模式
```tsx
// ✅ React 19 use() API — 简化异步数据读取
import { use, Suspense } from 'react'

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise)  // 直接读取 Promise，Suspense 自动处理加载
  return <div>{user.name}</div>
}

// ✅ React 19 Actions — 简化表单提交
function SubmitForm() {
  async function submitAction(formData: FormData) {
    'use server'  // or client-side async action
    await saveData(formData.get('title'))
  }
  
  return (
    <form action={submitAction}>
      <input name="title" />
      <button type="submit">Save</button>
    </form>
  )
}
```

#### 组合模式（Composition Patterns）
```tsx
// ✅ Compound Components 模式
function DataTable({ children }: { children: React.ReactNode }) {
  return <table className="w-full">{children}</table>
}
DataTable.Header = function Header({ children }) { ... }
DataTable.Body = function Body({ children }) { ... }
DataTable.Row = function Row({ children }) { ... }

// 使用
<DataTable>
  <DataTable.Header>...</DataTable.Header>
  <DataTable.Body>
    {data.map(row => <DataTable.Row key={row.id}>...</DataTable.Row>)}
  </DataTable.Body>
</DataTable>
```

#### 性能优化模式
```tsx
// ✅ useMemo / useCallback 的正确使用时机
// 只在以下情况使用：
// 1. 计算开销大（>1ms）
// 2. 作为 useEffect 依赖
// 3. 传给被 React.memo 包裹的子组件

const sortedItems = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]  // 仅在 items 引用变化时重算
)

// ✅ React 19 自动 memoization（compiler 模式）
// 如果启用了 React Compiler，大部分 useMemo/useCallback 可以省略
```

---

### 3.4 `design-review` — 设计质量审查 Skill

**定位**：建成后对界面进行系统性的质量检查，输出带优先级的改进建议报告。

**审查维度**：

```
检查清单（按优先级排序）：

🔴 Critical（必须修复）：
  - 对比度不足（< WCAG AA 标准 4.5:1）
  - 交互元素缺少 focus 状态
  - 移动端点击目标 < 44px

🟡 High（强烈建议）：
  - 字体选择是否有个性（避免 Inter/Roboto）
  - 颜色是否使用语义 token（避免硬编码 #3b82f6）
  - 空状态、加载状态、错误状态是否完整
  - 动效是否尊重 prefers-reduced-motion

🟢 Medium（建议改善）：
  - 间距系统是否一致（type scale + spacing scale）
  - 组件是否可复用（避免重复样式）
  - 是否有记忆锚点（unforgettable design element）
```

**输出格式**：
```markdown
## Design Review Report

### Critical Issues (2)
1. **低对比度**: `text-gray-400 on bg-gray-100` = 2.3:1 (需要 ≥ 4.5:1)
   Fix: 改为 `text-gray-600` (4.6:1)

2. **缺少 Focus Ring**: Button 组件缺少可见的键盘焦点样式
   Fix: 添加 `focus-visible:ring-2 focus-visible:ring-primary`

### High Priority (3)
...
```

---

### 3.5 `landing-page` 和 `product-showcase` Skills

这两个 Skills 是**输出驱动型**（Output-Oriented）的高阶 Skill，直接生成完整页面。

**`landing-page` 的典型调用**：
```
/landing-page "SaaS project management tool for remote teams, 
emphasizing async collaboration, B2B, tech-savvy audience"
```

**`landing-page` 的结构规范**（来自 references）：

```
Section 1: Hero
  - 主标题：<= 8 个词，说清楚 value prop
  - 副标题：解释 HOW，不重复 WHAT
  - CTA：明确的行动按钮（避免 "Learn More"）
  - 视觉：能支撑文案的 hero image / illustration

Section 2: Social Proof
  - Logo wall 或 Testimonials（建立可信度）

Section 3: Features/Benefits
  - 3 列 或 Z 字形布局
  - 每个功能聚焦用户收益，不是技术特性

Section 4: Pricing（可选）

Section 5: CTA 重申 + Footer
```

---

### 3.6 ERRATA 机制——版本变更的优雅处理

jezweb Skills 的独特设计：当库更新导致 Skill 内容过时时，**不立即修改 SKILL.md**，而是创建 `ERRATA.md`：

```
skill-name/
├── SKILL.md          # 核心内容（稳定，少改）
├── ERRATA.md         # 版本变更记录（活跃更新）
└── references/
    └── REFERENCE.md
```

**ERRATA.md 状态生命周期**：
```
active（当前有效的纠正）
  → absorbed（已折叠进 SKILL.md）
  → outdated（库又变了，本条记录已过期）
```

这种设计让 Skill 内容保持稳定，同时提供即时的错误修正能力。

---

## 四、项目完整 Plugin 结构（63 Skills）

```
plugins/
├── cloudflare/        8 skills  # Workers, Hono, D1, Vite, TanStack Start
├── frontend/         10 skills  # ⭐ 本文重点
├── design-assets/     5 skills  # 色彩、图标、图片、AI 图像
├── dev-tools/         9 skills  # Git, PR, 测试, 文档, 安全
├── writing/           5 skills  # 技术写作, 邮件, 博客
├── ai-integrations/   6 skills  # OpenAI, Gemini, ElevenLabs
├── web-design/        1 skill   # 本地 SEO
├── development/       7 skills  # 通用开发工具
├── mcp/               6 skills  # MCP Server 构建
└── administration/    6 skills  # 团队协作, 知识管理
```

---

## 五、与其他工具链的集成

jezweb Frontend Plugin 的设计考虑了完整的 Cloudflare 全栈部署链路：

```
前端 (Frontend Plugin)
tailwind-theme-builder → shadcn-ui → react-patterns → landing-page
          ↓
全栈集成 (Cloudflare Plugin)
vite-flare-starter (React 19 + Hono + D1)
          ↓
部署 (cloudflare-worker-builder)
```

这意味着你可以用一套 Skills 完成从"空白项目"到"Cloudflare 生产部署"的完整流程。

---

## 六、小结

jezweb/claude-skills 的 Frontend Plugin 代表了社区 Skills 工程化的最高水平：

| 优势 | 说明 |
|------|------|
| **错误预防导向** | 每个 Skill 明确列出预防的 documented errors 数量 |
| **版本感知** | 标注兼容版本，ERRATA.md 管理变更 |
| **输出承诺** | 每个 Skill 必须产出可见的文件或部署结果 |
| **依赖链清晰** | tailwind-theme-builder → shadcn-ui → react-patterns 的明确顺序 |
| **Context 效率** | 严格遵循"只包含 Claude 不知道的内容"原则 |

---

**下一篇** → `05_vercel_agent_skills_react.md`  
Vercel Agent Skills React 系列深度解析：官方 React 最佳实践、组合模式、React Native Skills 完整调研

---

*调查时间：2025年4月 | 数据来源：github.com/jezweb/claude-skills, agentskills.so, claudeskills.club, skillsmp.com*
