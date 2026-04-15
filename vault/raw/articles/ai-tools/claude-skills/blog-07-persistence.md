# UI UX Pro Max 深度解析⑦：Master + Overrides——解决 AI 跨会话设计一致性的持久化模式

> **系列第 7 篇（终章）**：AI 编程助手最大的痛点之一是「每次对话从零开始」。UUPM 的 Design System Persistence 功能通过 Master + Overrides 文件模式，让设计决策跨越会话边界持续存在。

---

## 一、问题的本质：AI 的"设计失忆症"

想象这样一个场景：

```
第 1 次对话:
  你: "帮我做首页，使用靛蓝 + Inter 字体"
  AI: ✅ 生成了完美的首页

第 2 次对话（新会话）:
  你: "帮我做仪表板"
  AI: 生成了... 使用紫色 + Roboto 字体
  你: 😤 "等等，不是说好靛蓝 + Inter 吗？"
```

这是 AI 无状态（Stateless）本质导致的。每次新对话，AI 对你的项目一无所知。

传统解法是在每次提示词里重复粘贴设计规范——但这低效、易遗漏，且随项目增长变得不可维护。

**UUPM 的解法**：把设计系统写进项目文件，AI 读文件，不读记忆。

---

## 二、Master + Overrides 文件架构

```
design-system/
├── MASTER.md              # 全局设计规范（全项目唯一真相来源）
└── pages/
    ├── dashboard.md       # 仪表板页面专属覆盖规则
    ├── checkout.md        # 结账页面专属覆盖规则
    ├── landing.md         # 落地页专属覆盖规则
    └── marketing.md       # 营销页面专属覆盖规则
```

### 核心原则

```
层级检索规则:

1. 构建特定页面时，先检查 design-system/pages/<page-name>.md
2. 如果页面文件存在，其规则「覆盖」MASTER.md 中的对应规则
3. 如果页面文件不存在，完全使用 MASTER.md
4. 页面文件只记录「与 MASTER 不同的地方」，不重复 MASTER 内容
```

---

## 三、MASTER.md 的标准结构

通过 `--persist` 参数生成的 MASTER.md 遵循以下结构：

```markdown
# Design System: [Project Name]
> Generated: [timestamp] | Stack: [技术栈] | Version: [版本]

---

## 1. Identity
- **Project Name**: MyApp
- **Product Type**: SaaS Dashboard
- **Target Audience**: B2B Enterprise Users
- **Brand Voice**: Professional, Efficient, Trustworthy

---

## 2. Color System

### Primary Palette
| Role       | Light Mode   | Dark Mode    | Usage |
|------------|-------------|-------------|-------|
| Primary    | #4F46E5     | #6366F1     | CTA, Links, Active states |
| Secondary  | #7C3AED     | #8B5CF6     | Secondary actions |
| Success    | #10B981     | #34D399     | Confirmations |
| Warning    | #F59E0B     | #FBBF24     | Alerts |
| Error      | #EF4444     | #F87171     | Validation |
| Background | #F8FAFC     | #0F172A     | Page background |
| Surface    | #FFFFFF     | #1E293B     | Card backgrounds |
| Text-1     | #1E293B     | #F1F5F9     | Primary text |
| Text-2     | #64748B     | #94A3B8     | Secondary text |

### Color Rules
- CTA buttons: always use Primary color
- Destructive actions: always use Error color
- Never use more than 3 colors in a single component

---

## 3. Typography System

### Font Stack
```css
--font-heading: 'Inter', -apple-system, sans-serif;
--font-body: 'Plus Jakarta Sans', -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### Type Scale
| Token      | Size  | Weight | Line Height | Usage |
|------------|-------|--------|-------------|-------|
| display-2xl| 4.5rem| 700    | 1.1         | Hero headings |
| display-xl | 3.75rem| 700  | 1.1         | Section titles |
| display-lg | 3rem  | 600    | 1.2         | Page titles |
| heading-xl | 2rem  | 600    | 1.3         | H1 |
| heading-lg | 1.5rem| 600    | 1.4         | H2 |
| heading-md | 1.25rem| 500   | 1.5         | H3 |
| body-lg    | 1.125rem| 400  | 1.7         | Lead text |
| body-md    | 1rem  | 400    | 1.6         | Default body |
| body-sm    | 0.875rem| 400  | 1.5         | Captions |
| caption    | 0.75rem | 400  | 1.4         | Labels, badges |

---

## 4. Spacing System

Base unit: 4px (0.25rem)

| Token | Value | Usage |
|-------|-------|-------|
| space-1  | 4px  | Micro spacing (icon gap) |
| space-2  | 8px  | Tight spacing (button padding) |
| space-3  | 12px | Small (form gap) |
| space-4  | 16px | Base unit |
| space-6  | 24px | Section inner padding |
| space-8  | 32px | Component gap |
| space-12 | 48px | Section gap |
| space-16 | 64px | Major section separation |

---

## 5. Component Specifications

### Buttons
- Border-radius: 8px (rounded-lg)
- Height: 40px (default), 32px (sm), 48px (lg)
- Padding: 16px horizontal
- Transition: all 150ms ease
- Focus ring: 2px offset + Primary color

### Cards
- Border-radius: 12px
- Shadow: 0 1px 3px rgba(0,0,0,0.1)
- Padding: 24px
- Hover shadow: 0 4px 12px rgba(0,0,0,0.15)

### Forms
- Input height: 40px
- Border: 1px solid #E2E8F0
- Border-radius: 6px
- Focus border: Primary color + 1px box-shadow

---

## 6. UI Style
- **Primary Style**: Glassmorphism
- **Secondary Style**: Soft UI Evolution
- **Dark Mode**: Required (class-based toggle)
- **Animation**: Subtle (150-300ms, ease-in-out)
- **Icon Set**: Lucide React

---

## 7. Anti-Patterns (NEVER DO)
- ✗ Emoji as icons
- ✗ Color-only error indicators (no text)
- ✗ Animations > 500ms
- ✗ AI purple/pink gradients
- ✗ Z-index values > 9999
- ✗ Neon colors on financial data

---

## 8. Tech Stack Specifics
- Framework: Next.js 14 (App Router)
- Styling: Tailwind CSS v3
- UI Library: shadcn/ui
- Animation: Framer Motion
- Icons: Lucide React
- State: Zustand
```

---

## 四、pages/ 覆盖文件：只写差异

覆盖文件的黄金法则：**只记录与 MASTER 不同的地方**。

### 示例：仪表板页面覆盖

```markdown
# Page Override: Dashboard
> Overrides MASTER.md for the /dashboard route

## Color Overrides
- Background: #0F172A (dark default, regardless of theme toggle)
- Surface: #1E293B
- Note: Dashboard is ALWAYS dark mode for data readability

## Typography Overrides
- body-md → 0.875rem (compact for dense data)
- All numbers: font-variant-numeric: tabular-nums (alignment)

## Component Overrides
### Cards
- Padding: 16px (compact, was 24px)
- Border: 1px solid #1E293B (visible in dark mode)

## Additional Components (Not in MASTER)
- Data cells: min-height 48px, tabular layout
- Status badges: 20px height, uppercase 0.75rem
- Chart containers: min-height 200px, overflow-hidden
```

### 示例：结账页面覆盖

```markdown
# Page Override: Checkout
> Overrides MASTER.md for /checkout route

## Color Overrides
- Error color: #DC2626 + red-50 background (critical, must be obvious)
- Trust indicators: add #10B981 + shield icon for security badges

## Anti-Patterns (Page-specific additions)
- ✗ NO dark mode on checkout (user trust issue)
- ✗ NO animations on form submission feedback
- ✗ NO auto-close on payment confirmation (explicit user action required)

## UX Rules (Page-specific)
- Payment button: full-width, min-height 52px
- Error messages: immediate inline, never toast
- Back button: prominent but secondary styled
```

---

## 五、上下文感知的提示词模板

有了持久化文件，你的提示词也应该相应调整：

```
情景：构建结账页面

提示词模板:
"我正在构建 [Checkout] 页面。
请先阅读 design-system/MASTER.md。
再检查 design-system/pages/checkout.md 是否存在。
如果页面文件存在，优先使用其规则；如不存在，完全遵照 MASTER。
现在，请生成结账页面的完整代码..."
```

---

## 六、UUPM CLI 生成持久化文件

```bash
# 步骤 1: 生成 MASTER.md（全局设计系统）
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "SaaS dashboard analytics B2B" \
  --design-system --persist \
  -p "MyAnalytics App"

# 输出: design-system/MASTER.md

# 步骤 2: 生成页面专属覆盖（可选）
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "data visualization dark analytics dashboard" \
  --design-system --persist \
  -p "MyAnalytics App" \
  --page "dashboard"

# 输出: design-system/pages/dashboard.md

# 步骤 3: 按需为各页面生成覆盖
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "checkout payment trust security" \
  --design-system --persist \
  -p "MyAnalytics App" \
  --page "checkout"
# 输出: design-system/pages/checkout.md
```

---

## 七、在大型项目中的完整工作流

### 项目初始化阶段

```bash
# 1. 安装 UUPM
npm install -g uipro-cli
uipro init --ai claude

# 2. 生成项目 MASTER.md
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "e-commerce luxury fashion marketplace" \
  --design-system --persist -p "LuxeShop"

# 3. 生成各主要页面覆盖
for page in landing product-detail checkout user-profile; do
  python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
    "$page e-commerce luxury" \
    --design-system --persist -p "LuxeShop" --page "$page"
done
```

### 开发阶段的 AI 提示词标准模板

```
我正在为 LuxeShop 构建 [页面名] 页面。

上下文读取规则:
1. 阅读 design-system/MASTER.md
2. 检查 design-system/pages/[页面名].md
3. 若页面文件存在: 其规则 > MASTER.md（覆盖关系）
4. 若页面文件不存在: 仅使用 MASTER.md

技术栈: Next.js 14 + Tailwind CSS + shadcn/ui

任务: [具体实现需求]

约束:
- 严格遵循 MASTER 中的 color tokens
- 使用 MASTER 中定义的 spacing scale
- 遵守 Anti-Patterns 列表
```

### 设计系统迭代

```bash
# 当需要更新全局规范时（如换色调）
# 只更新 MASTER.md，所有页面自动继承新规则

# 当某个页面需要专属处理时
# 创建/更新对应的 pages/xxx.md，不影响其他页面
```

---

## 八、与 CI/CD 集成：设计规范的自动验证

进阶用法：在 CI 流程中加入设计规范检查：

```yaml
# .github/workflows/design-lint.yml
name: Design System Lint

on: [pull_request]

jobs:
  design-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Design System Files
        run: |
          # 检查 MASTER.md 是否存在
          test -f design-system/MASTER.md || exit 1
          
          # 使用 UUPM 检查颜色对比度（如果集成了 checker）
          python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
            "contrast check" --domain ux -n 3
            
      - name: Remind design-system update
        if: github.event.pull_request.changed_files > 20
        run: |
          echo "大型 PR 提醒: 请检查 design-system/ 是否需要更新"
```

---

## 九、系列总结：UUPM 的设计哲学

经过 7 篇深度解析，可以提炼出 UUPM 的核心设计哲学：

### 哲学一：知识的结构化优先于知识的丰富性

UUPM 不是「把设计书转成 PDF 给 AI 读」，而是把设计知识**编码成机器可处理的结构**（CSV + 优先级 + 条件判断）。这使得 AI 可以推理，而非仅仅检索。

### 哲学二：反模式比正模式更有价值

UUPM 的 161 条推理规则中，最有差异化价值的不是「推荐用什么」，而是「明确禁止什么」。金融行业禁止 AI 紫、医疗行业禁止刺激色、儿童应用禁止暗黑模式——这些负样本约束才是真正的行业经验结晶。

### 哲学三：工具链感知的设计系统

设计不能脱离实现谈，UUPM 的 15 个技术栈指南把「如何在这个框架里正确实现这个设计」也纳入了知识库，让设计决策和实现路径合一。

### 哲学四：持久化解决 AI 无状态问题

AI 本质上是无状态的，但项目是有状态的。UUPM 的 Master + Overrides 模式把「有状态的设计决策」写入文件系统，让无状态的 AI 通过读文件获得「记忆」。

### 哲学五：零依赖的实用主义

选择 BM25 + Regex 而非向量搜索，选择 CSV 而非数据库，选择 Python 标准库——这些都是「在 AI Skill 场景下，可用性比精确性更重要」的实用主义选择。

---

## 十、本系列文章索引

| 篇章 | 核心主题 | 文件 |
|------|---------|------|
| ① 总览篇 | 架构全貌、工作流、项目背景 | blog-01-overview.md |
| ② 风格引擎篇 | 67 种 UI 风格体系详解 | blog-02-styles.md |
| ③ 设计系统生成器篇 | 161 条推理规则内部逻辑 | blog-03-design-system-generator.md |
| ④ 色彩与排版篇 | 161 色板 + 57 字体配对系统 | blog-04-colors-typography.md |
| ⑤ UX 准则与图表篇 | 99 条 UX 规范 + 25 种图表 | blog-05-ux-charts.md |
| ⑥ 技术栈与搜索引擎篇 | 15 栈适配 + BM25 架构 | blog-06-stacks-search.md |
| ⑦ 持久化模式篇（本篇）| Master + Overrides 设计系统 | blog-07-persistence.md |

---

> **GitHub**: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill  
> **官网**: https://uupm.cc  
> **npm**: `npm install -g uipro-cli`  
> **版本**: v2.5.0 | MIT License  
> **Star**: 53k+ ⭐
