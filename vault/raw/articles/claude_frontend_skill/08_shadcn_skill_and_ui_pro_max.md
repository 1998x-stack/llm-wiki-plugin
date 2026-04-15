# shadcn/ui 官方 Skill + UI/UX Pro Max + Shadcnblocks 深度解析

> **系列**：Claude Code 前端 React 风格 SKILL/Plugin 深度调查  
> **文章编号**：08 / 09  
> **涵盖内容**：shadcn/ui 官方 Skill、UI/UX Pro Max、Shadcnblocks-Skill  

---

## Part A：shadcn/ui 官方项目感知 Skill

### A-1. 背景：为什么需要官方 Skill？

shadcn/ui 本身就是"复制代码到项目"的设计——没有 npm 包，组件源码直接生成到 `src/components/ui/`。这导致 AI 工具面临一个特殊挑战：**AI 不知道你当前项目安装了哪些组件、用的什么框架版本、路径别名是什么。**

官方 shadcn/ui Skill 通过**运行时项目检测**解决了这个问题。

### A-2. 工作原理：项目感知的三步机制

```
步骤 1：项目检测
  ├─ 检测到 components.json → Skill 激活
  └─ 未检测到 → Skill 保持沉默（不干扰）

步骤 2：上下文注入
  运行 `shadcn info --json`
  ↓
  输出注入到 Claude 的上下文：
  {
    "framework": "Next.js",
    "tailwind": "4.0",
    "aliases": { "components": "@/components", "ui": "@/components/ui" },
    "baseLibrary": "radix",
    "iconLibrary": "lucide",
    "installedComponents": ["button", "card", "form", "input", "dialog"],
    "resolvedPaths": {
      "components": "/Users/xm/project/src/components",
      "ui": "/Users/xm/project/src/components/ui"
    }
  }

步骤 3：模式强制执行
  Claude 根据注入的配置生成代码：
  - 使用正确的 import 路径（@/components/ui/button）
  - 使用已安装的组件（不建议未安装的）
  - 使用正确的 base library API（radix vs base）
  - 遵循 shadcn/ui 组合规则
```

**安装**：

```bash
# 方式 1：npx skills（推荐）
npx skills add shadcn/ui

# 方式 2：手动（shadcn 官方文档）
mkdir -p .claude/skills
npx shadcn skill add   # shadcn CLI 集成
```

### A-3. 四大核心知识模块

#### 模块一：CSS 主题系统

```markdown
涵盖：
- CSS 变量架构（:root + .dark）
- OKLCH 颜色空间（shadcn/ui 新版本偏好）
- 自定义颜色和 border-radius
- Tailwind v3 vs v4 的不同配置方式
- ThemeProvider 实现深色模式
- 组件 variants 的颜色继承
```

**OKLCH 颜色示例**（shadcn/ui 新方向）：
```css
:root {
  --background: oklch(100% 0 0);         /* 纯白 */
  --foreground: oklch(9% 0 0);           /* 近黑 */
  --primary: oklch(45.2% 0.31 264.1);    /* 深蓝 */
  --primary-foreground: oklch(98% 0 0);  /* 近白 */
}
```

#### 模块二：组合规则（Composition Rules）

这是 Skill 的核心价值——shadcn/ui 有特定的最佳组合模式，AI 如果不了解会生成错误代码：

```tsx
// ❌ 错误：直接在 Input 外层包 div 处理错误信息
<div>
  <Input />
  {error && <p className="text-red-500">{error}</p>}
</div>

// ✅ 正确：使用 FormItem + FormMessage（shadcn/ui 表单组合）
<FormItem>
  <FormLabel>Email</FormLabel>
  <FormControl>
    <Input {...field} />
  </FormControl>
  <FormMessage />   {/* 自动显示验证错误 */}
</FormItem>

// ❌ 错误：用多个 Checkbox 没有语义组织
<Checkbox /> Option A
<Checkbox /> Option B

// ✅ 正确：使用 ToggleGroup 表示互斥选项
<ToggleGroup type="single" value={value} onValueChange={setValue}>
  <ToggleGroupItem value="a">Option A</ToggleGroupItem>
  <ToggleGroupItem value="b">Option B</ToggleGroupItem>
</ToggleGroup>
```

#### 模块三：自定义组件注册表

```markdown
涵盖：
- registry.json 格式（item types, file objects, dependencies）
- CSS 变量在注册表中的定义方式
- 构建和托管自定义注册表
- 用户如何配置使用自定义注册表
```

这对需要构建内部组件库（Design System）的团队特别有价值。

#### 模块四：shadcn MCP Server 集成

shadcn 官方提供了 MCP Server，Skill 知道如何使用它：

```markdown
功能：
- 搜索组件（按关键词）
- 浏览组件文档
- 安装组件到项目
- 查看组件代码示例

Claude 使用 MCP Server 而不是依靠训练数据中可能过时的知识
→ 始终获取最新的组件 API 和用法
```

---

## Part B：UI/UX Pro Max Skill

### B-1. 基本信息

| 属性 | 值 |
|------|---|
| **仓库** | `nextlevelbuilder/ui-ux-pro-max-skill` |
| **Stars** | 10,800 ⭐（最新版本）|
| **设计数据规模** | 50+ styles, 161 color palettes, 57 font pairings, 99 UX guidelines, 25 chart types |
| **技术栈支持** | 10 stacks（React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, HTML/CSS） |
| **核心机制** | Python CLI 脚本（`scripts/search.py`）+ 数据驱动推荐 |

这是当前 Claude Code Skills 生态中**规模最大**的设计情报 Skill，与其他 Skill 的本质区别在于：它不是"指导原则"，而是**可搜索的设计数据库**。

### B-2. 核心数据库内容

#### 50+ 设计风格（Styles）

```
视觉风格：
glassmorphism（玻璃态），claymorphism（粘土态），
neumorphism（新拟态），skeuomorphism（拟物），
flat design（扁平），brutalism（野兽派）

布局风格：
bento grid（本托格），editorial（杂志），
dashboard（仪表盘），landing page（落地页）

特殊风格：
dark mode（暗色），responsive（响应式），
minimalism（极简），maximalism（最大化）
```

#### 161 个调色板

每个调色板包含：
- 主色调（Primary）
- 次色调（Secondary）  
- Accent 强调色
- 中性色（背景、文字、边框）
- 适用场景标注（fintech, healthcare, gaming, etc.）

#### 57 个字体配对

每个配对包含：
- 标题字体（Display/Heading）
- 正文字体（Body）
- 特殊字体（Mono/Accent，可选）
- 场景适用性（professional, playful, luxury, etc.）

#### 99 个 UX 规则

按类别：
```
accessibility（无障碍）- 最高优先级
animation（动效）
z-index management（层级管理）
form design（表单设计）
navigation patterns（导航模式）
...
```

### B-3. Python CLI 工作流

UI/UX Pro Max 的独特之处：它捆绑了一个 **Python 脚本**，Claude 在设计任务时会运行该脚本查询数据库：

```bash
# 基础用法：生成完整设计系统
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "saas productivity dashboard" \
  --design-system \
  -p "TaskFlow"

# 输出示例（ASCII 格式）
╔══════════════════════════════════════════════╗
║        DESIGN SYSTEM: TaskFlow               ║
╠══════════════════════════════════════════════╣
║ PATTERN:     Professional Dashboard          ║
║ STYLE:       Minimalist + Dark Mode          ║
║ TYPOGRAPHY:  IBM Plex Sans / JetBrains Mono  ║
╠══════════════════════════════════════════════╣
║ COLORS:                                      ║
║   Background: #0a0e17                        ║
║   Surface:    #131929                        ║
║   Primary:    #4361ee                        ║
║   Accent:     #7209b7                        ║
╠══════════════════════════════════════════════╣
║ EFFECTS:     subtle gradients, glass cards   ║
║ ANTI-PATTERNS: avoid neon, avoid cartoonish  ║
╚══════════════════════════════════════════════╝
```

```bash
# 按领域搜索
python3 scripts/search.py "animation accessibility" --domain ux
python3 scripts/search.py "elegant luxury serif" --domain typography
python3 scripts/search.py "layout responsive form" --stack html-tailwind
python3 scripts/search.py "fintech crypto dark" --design-system -f markdown
```

### B-4. 四步设计工作流

```
Step 1: 分析需求
  提取：product type, style keywords, industry, stack

Step 2: 生成设计系统（必须，使用 --design-system）
  并行搜索 5 个领域：product, style, color, landing, typography
  应用数据集中的推理规则（CSV 格式）
  输出：pattern + style + colors + typography + effects + anti-patterns

Step 3: 细化查询（可选）
  对 ux, animation, accessibility, typography 等领域进行深入查询

Step 4: 获取技术栈规范
  针对目标 stack（react, nextjs, shadcn 等）获取实现最佳实践

Step 5: 实现
  综合设计系统 + 细化查询结果 → 生成代码
```

### B-5. 持久化设计系统（Persistent Design System）

这是 UI/UX Pro Max 的高级功能，专为大型项目设计：

```bash
python3 scripts/search.py "enterprise saas" --design-system --persist -p "MyApp"
```

**输出目录结构**：
```
design-system/
├── MASTER.md           # 全局设计系统（字体、颜色、间距、图标）
└── pages/
    ├── landing.md      # 落地页专属规则（可覆盖 MASTER）
    ├── dashboard.md    # 仪表盘专属规则（不同密度）
    └── onboarding.md   # 引导页专属规则
```

**Master + Overrides 模式**：
- `MASTER.md`：全局不变的设计决策（调色板、字体、圆角）
- `pages/*.md`：页面级覆盖（密度、特殊组件规则）

这让大型项目中 Claude 在处理不同页面时保持设计一致性，同时允许页面级调整。

### B-6. 无障碍分类排名最高

UI/UX Pro Max 的 99 条 UX 规则中，**无障碍（accessibility）被列为最高优先级**：

```
accessibility 规则（部分）：
- minimum-contrast: 4.5:1 for normal text, 3:1 for large text
- visible-focus-rings: All interactive elements must have focus indicators
- descriptive-alt: Alt text must describe content, not just "image"
- aria-labels: Buttons/icons without text must have aria-label
- keyboard-navigation: All actions must be keyboard-accessible
- proper-form-labels: Every input must have an associated label
- safe-area-awareness: Keep touch targets away from notch, gesture bar
- no-precision-required: Avoid requiring pixel-perfect taps
```

---

## Part C：Shadcnblocks-Skill

### C-1. 基本信息

| 属性 | 值 |
|------|---|
| **仓库** | `masonjames/Shadcnblocks-Skill` |
| **定位** | 给 Claude 2,500+ shadcn/ui blocks 的专家知识 |
| **参考文档** | block-catalog.md (71 categories) + component-catalog.md (60+ groups) |

### C-2. 核心概念：Blocks vs Components

```
shadcn/ui Components（基础组件）：
  button, card, input, form, dialog...
  → 单个 UI 元素，高度可定制
  → 通过 `npx shadcn add button` 安装

shadcn/ui Blocks（完整 UI 段落）：
  hero section, feature grid, pricing table, checkout flow...
  → 多个组件组合的完整页面段落
  → 通过 Shadcnblocks API 获取
```

### C-3. 71 个 Block 类别

```
落地页类：
hero, feature, pricing, testimonial, FAQ, navbar, footer, CTA, team, about

内容类：
blog post list, gallery, article, contact form

电商类：
product cards, shopping cart, checkout flow, order history

应用/仪表盘类：
charts, data tables, sidebars, stats overview, user settings

认证类：
login form, signup form, password reset, two-factor auth
```

### C-4. 工作流程

```bash
# 1. 用户描述需求
"Build a SaaS landing page with a hero, features grid, and pricing table"

# 2. Skill 激活，Claude 匹配 Block 类别
hero → 推荐：hero-split（hero with image/illustration）
features → 推荐：feature-3col（3 columns with icons）
pricing → 推荐：pricing-tier（tiered pricing cards）

# 3. Claude 运行设置脚本
bash scripts/setup-shadcnblocks.sh

# 4. 按 Block 类别安装并组合
npx shadcnblocks add hero-split
npx shadcnblocks add feature-3col
npx shadcnblocks add pricing-tier

# 5. 在页面中组合使用
import { HeroSplit } from "@/components/blocks/hero-split"
import { FeatureGrid } from "@/components/blocks/feature-3col"
import { PricingTier } from "@/components/blocks/pricing-tier"
```

---

## 三者组合使用建议

```
场景：构建新的 SaaS 产品落地页

Step 1: UI/UX Pro Max
python3 search.py "saas landing page professional" --design-system
→ 获取设计系统（颜色、字体、风格）

Step 2: Shadcnblocks-Skill
→ 识别所需 Blocks（hero, features, pricing）
→ 安装对应 Blocks

Step 3: shadcn/ui 官方 Skill
→ 为交互细节选择正确的基础组件
→ 保证组合规则正确

Step 4: Vercel react-best-practices Skill
→ 优化数据获取、Bundle 大小

Step 5: AccessLint
→ WCAG 合规检查
```

---

## 小结

| Skill | 核心定位 | 独特价值 |
|-------|---------|---------|
| shadcn/ui 官方 | 项目感知的 API 正确性 | 运行时读取 components.json，第一次生成正确代码 |
| UI/UX Pro Max | 设计情报数据库 | 161 调色板 + 57 字体配对 + 99 UX 规则的可搜索数据库 |
| Shadcnblocks | 2,500+ Block 知识 | 快速组装完整页面段落（不是单组件） |

---

**下一篇** → `09_comprehensive_guide_and_skill_selection.md`  
综合指南：前端 React Skill 选择矩阵、组合策略、创建自定义 Skill 的实践指南

---

*调查时间：2025年4月 | 数据来源：ui.shadcn.com/docs/skills, claudeskills.club, nextlevelbuilder/ui-ux-pro-max-skill, masonjames/Shadcnblocks-Skill*
