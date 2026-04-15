# web-artifacts-builder Skill 深度解析

> **系列**：Claude Code 前端 React 风格 SKILL/Plugin 深度调查  
> **文章编号**：03 / 09  
> **来源仓库**：`anthropics/skills`（examples/web-artifacts-builder）  
> **技术栈**：React 18 + TypeScript + Vite + Parcel + Tailwind CSS 3.4.1 + shadcn/ui  

---

## 一、定位：什么时候用这个 Skill？

`frontend-design` Skill 负责**设计哲学**，`web-artifacts-builder` Skill 负责**工程实现**——两者是互补关系。

### 使用场景判断表

| 场景 | 用哪个 |
|------|--------|
| 单文件 React JSX Artifact（无需构建） | `frontend-design` Skill + Artifacts 功能 |
| 单文件 HTML Artifact | `frontend-design` Skill + Artifacts 功能 |
| **多组件 + 状态管理 + 路由 + shadcn/ui** | ✅ `web-artifacts-builder` Skill |
| 需要复杂 TypeScript 类型系统 | ✅ `web-artifacts-builder` Skill |
| 需要 40+ shadcn/ui 组件 | ✅ `web-artifacts-builder` Skill |
| 最终输出需要是单个可分享的 HTML 文件 | ✅ `web-artifacts-builder` Skill |

官方 description 明确说明：
> Use for complex artifacts requiring **state management, routing, or shadcn/ui components** — not for simple single-file HTML/JSX artifacts.

---

## 二、技术栈全景

```
React 18                    ← UI 框架
TypeScript (strict)         ← 类型安全
Vite                        ← 开发服务器 + 热更新
Parcel                      ← 最终打包（替代 Vite build，更适合 bundle-to-single-HTML）
Tailwind CSS 3.4.1          ← 样式框架（含 shadcn/ui theming system）
shadcn/ui (40+ components)  ← UI 组件库（Radix UI primitives）
html-inline                 ← 将所有资源内联到单个 HTML
```

**为什么用 Parcel 而不是 Vite build？**

Vite 构建输出多个文件（JS chunks + CSS），需要服务器静态托管。Parcel + html-inline 的组合可以将整个 React 应用——包括所有 JS、CSS、字体、图片——**内联到单个 HTML 文件**，直接在 Claude.ai Artifacts 环境中展示，无需服务器。

---

## 三、五步工作流详解

### Step 1：初始化项目

```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

初始化脚本（`scripts/init-artifact.sh`）做了以下事情：

**1. 创建 Vite + React + TypeScript 项目**
```bash
npx create-vite@latest . --template react-ts
```

**2. 安装 Tailwind CSS 3.4.1**
```bash
npm install -D tailwindcss@3.4.1 postcss autoprefixer
npx tailwindcss init -p
```

**3. 配置 shadcn/ui theming**
在 `src/index.css` 中注入完整的 shadcn/ui CSS 变量体系：
```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
  .dark { /* ... dark mode variables ... */ }
}
```

**4. 配置 Path Alias `@/`**
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

```typescript
// vite.config.ts
import path from 'path'
export default defineConfig({
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') }
  }
})
```

**5. 预安装 40+ shadcn/ui 组件**

包括（非完整列表）：
```
accordion, alert, alert-dialog, aspect-ratio, avatar, badge, button,
calendar, card, checkbox, collapsible, command, context-menu, dialog,
dropdown-menu, form, hover-card, input, label, menubar, navigation-menu,
popover, progress, radio-group, scroll-area, select, separator, sheet,
skeleton, slider, switch, table, tabs, textarea, toast, toggle, tooltip
```

所有 Radix UI 基础依赖（`@radix-ui/react-*`）一并安装。

**6. 自动检测 Node 版本并锁定 Vite 版本**

脚本检测 Node.js 版本，如果是 Node 18，自动使用兼容的 Vite 版本（避免 Node 18 与最新 Vite 的兼容问题）：
```bash
NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -eq 18 ]; then
  npm install -D vite@4.5.0   # Node 18 兼容版本
fi
```

---

### Step 2：开发 Artifact

初始化完成后，开始编写实际业务代码。

**典型文件结构**：
```
project-name/
├── index.html              # Parcel 的打包入口
├── src/
│   ├── App.tsx             # 根组件
│   ├── main.tsx            # React DOM 挂载
│   ├── index.css           # Tailwind + shadcn/ui CSS 变量
│   ├── components/
│   │   ├── ui/             # shadcn/ui 生成的组件（自动）
│   │   └── custom/         # 业务组件（手写）
│   ├── pages/              # 路由页面（如使用 React Router）
│   ├── hooks/              # 自定义 React Hooks
│   ├── types/              # TypeScript 类型定义
│   └── lib/
│       └── utils.ts        # cn() 等工具函数
└── package.json
```

**shadcn/ui 组件使用示例**：
```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function ProductCard({ product }: { product: Product }) {
  return (
    <Card className="overflow-hidden">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{product.name}</CardTitle>
          <Badge variant="secondary">{product.category}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground text-sm">{product.description}</p>
        <Button className="mt-4 w-full">View Details</Button>
      </CardContent>
    </Card>
  )
}
```

**`cn()` 工具函数**（shadcn/ui 标准配置）：
```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

### Step 3：Bundle 到单个 HTML 文件

```bash
bash scripts/bundle-artifact.sh
```

该脚本执行以下步骤：

**1. 安装打包依赖**
```bash
npm install -D parcel @parcel/config-default parcel-resolver-tspaths html-inline
```

**2. 创建 `.parcelrc` 配置**
```json
{
  "extends": "@parcel/config-default",
  "resolvers": ["parcel-resolver-tspaths", "..."]
}
```

**3. Parcel 构建（禁用 source map）**
```bash
npx parcel build index.html --no-source-maps --dist-dir dist
```

**4. 使用 html-inline 内联所有资源**
```bash
npx html-inline dist/index.html -o bundle.html
```

**输出**：`bundle.html`——一个包含所有 JavaScript、CSS、字体、图片的自包含 HTML 文件，大小通常在 500KB ~ 3MB 之间。

---

### Step 4：分享给用户

通过 `present_files` 工具将 `bundle.html` 展示给用户，Claude.ai 会自动渲染为交互式 Artifact。

---

### Step 5：可选——测试 Artifact

使用 Playwright 对 `bundle.html` 进行截图验证：

```bash
# 可结合 webapp-testing Skill
npx playwright screenshot bundle.html screenshot.png
```

Skill 文档明确说明这是可选步骤：
> Avoid testing upfront as it adds latency between the request and when the finished artifact can be seen.

---

## 四、Anti-AI-Slop 在此 Skill 中的体现

即使是在工程化的 Skill 中，Anthropic 也保留了反 AI Slop 的警告：

```
VERY IMPORTANT: To avoid what is often referred to as "AI slop", avoid using:
- Excessive centered layouts
- Purple gradients  
- Uniform rounded corners
- Inter font
```

这意味着即使在多组件、TypeScript 的正式项目中，也需要配合 `frontend-design` Skill 的设计哲学。

---

## 五、实战示例：使用此 Skill 构建任务管理应用

**用户请求**：
> Build a Kanban task management app with drag-and-drop, priority labels, and team member assignment using React and shadcn/ui

**Claude 的执行流程**：

```
1. bash scripts/init-artifact.sh kanban-app
2. 设计美学方向：选择"editorial/magazine"风格，深色基调，
   DM Mono + Syne 字体组合
3. 核心组件：
   - KanbanBoard.tsx（使用 @dnd-kit/core 拖拽）
   - TaskCard.tsx（使用 shadcn/ui Card + Badge + Avatar）
   - ColumnHeader.tsx（自定义设计）
   - AddTaskDialog.tsx（使用 shadcn/ui Dialog + Form）
4. 状态管理：React useState + useReducer（避免引入 Zustand 等外部库）
5. bash scripts/bundle-artifact.sh
6. present_files bundle.html
```

**关键代码片段**（TaskCard.tsx）：
```tsx
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { cn } from "@/lib/utils"

interface TaskCardProps {
  task: Task
  isDragging?: boolean
}

const priorityConfig = {
  high: { label: 'P1', className: 'bg-red-500/20 text-red-300 border-red-500/30' },
  medium: { label: 'P2', className: 'bg-amber-500/20 text-amber-300 border-amber-500/30' },
  low: { label: 'P3', className: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' },
}

export function TaskCard({ task, isDragging }: TaskCardProps) {
  const priority = priorityConfig[task.priority]
  
  return (
    <Card className={cn(
      "group cursor-grab active:cursor-grabbing",
      "bg-[#0f0f0f] border-[#252525] hover:border-[#3a3a3a]",
      "transition-all duration-200",
      isDragging && "shadow-2xl shadow-black/60 rotate-2 scale-105"
    )}>
      {/* ... */}
    </Card>
  )
}
```

---

## 六、已知限制

| 限制 | 说明 |
|------|------|
| Node 版本依赖 | Node 18 需要降级 Vite，Node 20+ 更稳定 |
| Bundle 文件较大 | shadcn/ui + React 内联后通常 1-3MB |
| 无 SSR 支持 | 仅 SPA，不支持 Next.js / Remix |
| 字体内联 | Google Fonts 字体在内联时可能失效，需改用本地字体或 data URI |
| 外部 API 调用 | 打包后的 HTML 如需调用 API，需配合 Anthropic API（见 Claude.ai Artifacts API 能力） |

---

## 七、与其他 Skill 的组合使用

```
web-artifacts-builder   ← 工程基础设施
        +
frontend-design         ← 设计哲学与美学指导
        +
theme-factory           ← 主题颜色与字体选择辅助
        =
高质量、有设计感的复杂 React Artifact
```

---

## 八、小结

`web-artifacts-builder` 是一个**工程级别的 Skill**，解决的是"如何把复杂 React 应用打包成 Claude.ai 可渲染的单文件 Artifact"的纯工程问题。

核心价值：
1. **完整预配置**：React 18 + TypeScript + Tailwind + shadcn/ui 的最佳实践配置，零调试
2. **40+ 组件开箱即用**：所有 shadcn/ui 组件预安装，跳过重复的脚手架工作
3. **单文件输出**：Parcel + html-inline 的组合将复杂应用变成可分享的单文件
4. **Node 兼容性处理**：自动检测 Node 版本，避免踩坑

---

**下一篇** → `04_jezweb_claude_skills_react_collection.md`  
jezweb/claude-skills React 前端技能集深度解析：Tailwind v4、shadcn/ui、React 19 性能优化模式、设计评审工作流

---

*调查时间：2025年4月 | 数据来源：anthropics/skills GitHub（examples/web-artifacts-builder）*
