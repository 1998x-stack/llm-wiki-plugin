# bencium UX Designer Skill + AccessLint 无障碍插件深度解析

> **系列**：Claude Code 前端 React 风格 SKILL/Plugin 深度调查  
> **文章编号**：06 / 09  
> **涵盖内容**：bencium/bencium-claude-code-design-skill + accesslint/claude-marketplace  

---

## Part A：bencium UX Designer Skill

### A-1. 基本信息

| 属性 | 值 |
|------|---|
| **仓库** | `bencium/bencium-claude-code-design-skill` |
| **Stars** | 126 ⭐（2026年4月） |
| **SKILL.md 大小** | 27.5KB（**28,000+ 字符**） |
| **Skill 数量** | 2 个（`bencium-innovative-ux-designer` + `bencium-controlled-ux-designer`） |
| **参考文档** | 4 个（ACCESSIBILITY.md, MOTION-SPEC.md, RESPONSIVE-DESIGN.md, DESIGN-SYSTEM-TEMPLATE.md） |
| **版本** | v2.0.0（2025年11月22日，"Creative Liberation" 更新） |

**安装方式**：

```bash
# 通过 bencium-marketplace 安装（推荐）
/plugin marketplace add bencium/bencium-marketplace
/plugin install bencium-controlled-ux-designer@bencium-marketplace
/plugin install bencium-innovative-ux-designer@bencium-marketplace

# 通过 npx skills
npx skills add bencium/bencium-marketplace -g --skill bencium-controlled-ux-designer
npx skills add bencium/bencium-marketplace -g --skill bencium-innovative-ux-designer

# 手动安装
git clone https://github.com/bencium/bencium-claude-code-design-skill.git
cp -r bencium-claude-code-design-skill/bencium-innovative-ux-designer ~/.claude/skills/
```

---

### A-2. 双模式架构：Innovative vs Controlled

bencium 的最大特点是为**同一 UX 设计领域**提供了**两种完全不同的 AI 行为模式**，对应两种项目需求：

| 维度 | `bencium-innovative-ux-designer` | `bencium-controlled-ux-designer` |
|------|----------------------------------|----------------------------------|
| **核心哲学** | 大胆、独特、出人意料 | 系统化、可控、符合规范 |
| **设计决策** | 主动选择美学方向，大胆执行 | 始终先询问，再实施 |
| **对比度对待** | 允许艺术性低对比度（有意识地） | 严格 WCAG AA 4.5:1 |
| **阴影/渐变** | ✅ 允许（v2.0 "创意解放"后） | 谨慎使用 |
| **字体选择** | 意外的、有个性的配对 | 品牌规范优先 |
| **适合项目** | 创意机构、作品集、新产品 | 企业应用、受监管行业、设计系统 |

**v2.0.0 "Creative Liberation" 更新的核心变化**：
- Innovative 变体解禁了阴影和渐变（v1.0 过于保守）
- 加入了 Design Thinking Protocol（设计前强制四步思考）
- 将无障碍定位为"创意的使能者，而非限制者"

---

### A-3. Innovative Variant 核心指令解析

**SKILL.md 禁止清单（❌ NEVER）**：
```
- 默认 AI 外观（Inter 字体、紫色渐变）
- 没有设计个性的通用布局
- 让用户感到困惑的过度动效
- 互相竞争的元素堆砌成的混乱界面
```

**SKILL.md 强制清单（✅ ALWAYS）**：
```
- 先问清楚：purpose, tone, constraints, differentiation
- 然后大胆选择一个独特美学方向并彻底执行
- 出人意料的字体选择（有个性的）
- 有意识地创造氛围：阴影、渐变、纹理、噪点
- 主色调 + 锐利对比色（不是温吞的均衡配色）
- 为交互提供即时反馈
- 用真实设备测试
- 验证无障碍（无障碍使创意成为可能，而非限制）
```

**Design Thinking Protocol（v2.0 新增）**：
```markdown
在实现任何组件之前，Claude 必须问：

1. 这个界面要解决什么问题？
2. 主要用户是谁？
3. 这个设计应该传达什么情感？
   (urgent/urgent / calm / playful / professional)
4. 什么应该让人难忘（unforgettable）？
```

---

### A-4. Controlled Variant 核心指令解析

**"Design Decision Protocol" — 强制先问后做**：

```markdown
Before implementing ANYTHING involving visual decisions (colors, typography, 
sizes, layout), Claude MUST ask:

1. What's the primary action you want to emphasize?
2. Do you have brand colors in mind, or should I suggest options?
3. What emotion should this button convey? (urgent, calm, playful, professional)
```

这与 Innovative 变体"主动做出大胆选择"形成鲜明对比。Controlled 的理念是：**AI 不应该代替用户做设计决策，而应该通过问题引导用户表达自己的意图**。

**数学化的设计系统**：

Controlled 变体强调**数学比例关系**：

```css
/* Type Scale（模块化比例）*/
:root {
  --type-ratio: 1.25;          /* Major Third */
  --text-base: 1rem;           /* 16px */
  --text-sm: calc(var(--text-base) / var(--type-ratio));    /* ~12.8px */
  --text-md: var(--text-base);                               /* 16px */
  --text-lg: calc(var(--text-base) * var(--type-ratio));     /* ~20px */
  --text-xl: calc(var(--text-lg) * var(--type-ratio));       /* ~25px */
  --text-2xl: calc(var(--text-xl) * var(--type-ratio));      /* ~31px */
  --text-3xl: calc(var(--text-2xl) * var(--type-ratio));     /* ~39px */
}

/* Spacing Scale（基于 4px 基准的 8 点网格）*/
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

---

### A-5. 四个参考文档的内容

#### `ACCESSIBILITY.md`（2.7KB）
WCAG AA 基线要求的精简版：

```markdown
## 核心检查清单

颜色对比度：
  - 正常文字（< 18pt）≥ 4.5:1
  - 大文字（≥ 18pt 或 14pt bold）≥ 3:1
  - 非文字 UI 元素（图标、边框）≥ 3:1

焦点状态：
  - 所有交互元素必须有可见的 focus ring
  - focus ring 对比度 ≥ 3:1
  - 避免 outline: none（除非有替代方案）

表单：
  - 每个 input 必须有关联的 <label>（不能只用 placeholder）
  - 错误信息必须通过 aria-describedby 关联
  - 必填字段通过 aria-required="true" 标注

键盘导航：
  - 所有功能可纯键盘完成
  - Tab 顺序符合视觉顺序
  - 模态框打开时焦点必须进入模态框
  - 模态框关闭时焦点必须返回触发元素
```

#### `MOTION-SPEC.md`（2.0KB）
动效规范（easing curves 和 duration 表格）：

```markdown
## Duration（持续时间）

| 类型 | 时长 |
|------|------|
| 微交互（hover, focus） | 150-200ms |
| 简单进出（fade, scale） | 200-300ms |
| 复杂动画（slide, morph） | 300-400ms |
| 页面转场 | 400-500ms |

## Easing

| 用途 | Curve |
|------|-------|
| 元素进入 | ease-out（0.0, 0.0, 0.2, 1.0）快入慢出 |
| 元素离开 | ease-in（0.4, 0.0, 1.0, 1.0）慢入快出 |
| 状态变化 | ease-in-out（0.4, 0.0, 0.2, 1.0） |
| 有趣的弹性 | cubic-bezier(0.68, -0.55, 0.265, 1.55) |

## Reduced Motion

所有动画必须 respect prefers-reduced-motion：
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

#### `RESPONSIVE-DESIGN.md`（2.3KB）
移动优先断点规范：

```markdown
## Breakpoints（Tailwind 对齐）

| 名称 | 宽度 | 典型设备 |
|------|------|---------|
| xs | < 480px | 小屏手机 |
| sm | ≥ 640px | 大屏手机 / 小平板 |
| md | ≥ 768px | 平板 |
| lg | ≥ 1024px | 小桌面 |
| xl | ≥ 1280px | 大桌面 |
| 2xl | ≥ 1536px | 超宽屏 |

## 字体响应式规则

- 移动端比桌面端小 20-30%
- 移动端减少字体层级数量
- 使用 CSS clamp() 实现流体字体：
  h1 { font-size: clamp(2rem, 5vw, 4rem); }

## 触摸目标最小尺寸

- iOS：44×44px（Apple HIG 标准）
- Android：48×48dp（Material Design 标准）
- 相邻触摸目标间距 ≥ 8px
```

#### `DESIGN-SYSTEM-TEMPLATE.md`（14.8KB）
设计系统的元框架——这是四个文档中**最重量级**的一个：

```markdown
## 三类设计决策

固定（Universal Rules）：
  - WCAG AA 对比度要求
  - 最小触摸目标尺寸
  - 焦点状态可见性

项目特定（Brand Personality）：
  - 主色调和 accent 颜色
  - 字体组合
  - 圆角半径
  - 动效风格

可调（Context-Dependent）：
  - 密度（紧凑 vs 宽松）
  - 内容长度
  - 可选组件展示

## 决策树

当需要选择颜色时：
1. 是否有品牌颜色？
   ├─ 是 → 使用品牌颜色，调整为语义 token
   └─ 否 → 询问用户：行业、受众、情感 → 生成选项

当需要选择字体时：
1. 是否有品牌字体规范？
   ├─ 是 → 使用规定字体
   └─ 否 → 询问用户：行业、风格偏好 → 推荐 3 个选项
```

---

### A-6. 与 Anthropic frontend-design 的对比

| 维度 | Anthropic frontend-design | bencium-innovative | bencium-controlled |
|------|--------------------------|--------------------|--------------------|
| **SKILL.md 大小** | ~3KB | **27.5KB** | **27.5KB** |
| **参考文档** | 无 | 4 个 | 4 个 |
| **决策协议** | 自主选择 | 先问后做（v2 简化） | **严格先问** |
| **字体规范** | 避免通用字体 | 有个性 + 意外感 | 遵循品牌规范 |
| **无障碍深度** | 基础提及 | ACCESSIBILITY.md | **WCAG 完整覆盖** |
| **动效规范** | 方向性指导 | **MOTION-SPEC.md** | **MOTION-SPEC.md** |
| **响应式规范** | 无 | **RESPONSIVE-DESIGN.md** | **RESPONSIVE-DESIGN.md** |

bencium 的核心价值在于**深度**——28,000 字的 SKILL.md 加上 4 个参考文档，是官方 Skill 的约 10 倍内容量。

---

## Part B：AccessLint 无障碍插件

### B-1. 基本信息

| 属性 | 值 |
|------|---|
| **仓库** | `accesslint/claude-marketplace` |
| **Stars** | 8 ⭐ |
| **License** | MIT |
| **最后更新** | 2025年11月 |
| **Plugin 结构** | Skills + Agent + MCP Server |

### B-2. Skills 列表

```
plugins/accesslint/skills/
├── contrast-checker/     # 颜色对比度检查
├── refactor/             # 无障碍代码重构
├── use-of-color/         # 颜色使用规范审查
└── link-purpose/         # 链接文字可理解性检查
```

### B-3. `contrast-checker` Skill

**功能**：自动检测 CSS/Tailwind 中的颜色对比度问题

**工作流程**：

```
1. 扫描组件中的前景色和背景色组合
2. 调用 MCP Server 计算实际对比度比值
3. 对照 WCAG 2.1 标准分类：
   - Pass AA（≥ 4.5:1 正文 / ≥ 3:1 大文字）
   - Fail（需要修复）
4. 输出修复建议（具体的颜色替代值）
```

**MCP Server 集成**（programmatic color contrast analysis）：

AccessLint 捆绑了一个专门的 MCP Server，用于精确的颜色对比度计算：

```json
// MCP Server 能力
{
  "tools": [
    "calculate_contrast_ratio",     // 计算两色对比度
    "find_accessible_alternative",  // 找到满足对比度要求的替代色
    "audit_color_combinations"      // 批量审查颜色组合
  ]
}
```

### B-4. `link-purpose` Skill

**目标**：修复"点击这里"、"了解更多"等无障碍不友好的链接文字

```tsx
// ❌ 问题：脱离上下文无法理解
<a href="/docs">Click here</a>
<a href="/product">Learn more</a>

// ✅ 修复：链接文字本身描述目的
<a href="/docs">Read the documentation</a>
<a href="/product">Learn more about Premium Plan</a>

// ✅ 或使用 aria-label（当视觉上需要保持简短时）
<a href="/docs" aria-label="Read the full documentation">Click here</a>
```

### B-5. `refactor` Skill

**功能**：系统性地重构代码以提升无障碍性

**审查维度**：
1. 语义 HTML（`<button>` 替代 `<div onClick>`）
2. ARIA 角色和属性（`role`, `aria-label`, `aria-expanded`）
3. 键盘事件处理（`onKeyDown` 配合 `onClick`）
4. 图片 alt 属性
5. 表单 `<label>` 关联
6. 动态内容的 `aria-live` 区域

**典型重构示例**：

```tsx
// ❌ Before（多个无障碍问题）
<div className="dropdown" onClick={toggleMenu}>
  <div>Menu</div>
  {isOpen && (
    <div className="menu-items">
      <div onClick={() => navigate('/home')}>Home</div>
      <div onClick={() => navigate('/about')}>About</div>
    </div>
  )}
</div>

// ✅ After（AccessLint 重构后）
<div className="relative">
  <button
    onClick={toggleMenu}
    aria-expanded={isOpen}
    aria-haspopup="true"
    aria-controls="navigation-menu"
    className="..."
  >
    Menu
    <ChevronIcon aria-hidden="true" />
  </button>
  {isOpen && (
    <ul
      id="navigation-menu"
      role="menu"
      className="..."
    >
      <li role="none">
        <a href="/home" role="menuitem">Home</a>
      </li>
      <li role="none">
        <a href="/about" role="menuitem">About</a>
      </li>
    </ul>
  )}
</div>
```

### B-6. `accesslint:reviewer` Agent

AccessLint 还包含一个专用 Agent（`AGENT.md` 定义），执行**综合多步骤无障碍代码审查**：

```markdown
# accesslint:reviewer Agent

## 任务
执行完整的 WCAG 2.1 Level A 和 AA 一致性审查

## 步骤
1. 导航到项目的组件目录
2. 识别所有 UI 组件
3. 对每个组件运行 4 个 Skills（对比度、颜色使用、链接文字、重构候选）
4. 汇总发现，按严重程度排序
5. 生成结构化审查报告

## 输出格式
Level A 问题（必须修复）
Level AA 问题（强烈建议）
WCAG 引用（每个问题附引用条款）
优先级排序（按用户影响从高到低）
```

---

### B-7. bencium + AccessLint 组合策略

```
bencium-innovative-ux-designer    ← 创意设计方向
        +
bencium 的 ACCESSIBILITY.md       ← WCAG 基线规范（开发时）
        +
AccessLint contrast-checker       ← 实现后的颜色对比度验证
        +
AccessLint accesslint:reviewer    ← 发布前的全面无障碍审查
```

**工作时间线**：
1. **设计阶段**：`bencium-innovative` → 确定美学方向
2. **开发阶段**：参考 `ACCESSIBILITY.md` 和 `MOTION-SPEC.md`
3. **组件完成后**：`contrast-checker` + `link-purpose` 即时检查
4. **发布前**：`accesslint:reviewer` 执行完整 WCAG 审查

---

## 小结

| Skill | 核心价值 | 适用场景 |
|-------|---------|---------|
| `bencium-innovative` | 大胆美学方向 + 深度 UX 知识 | 创意项目、作品集、新产品 |
| `bencium-controlled` | 系统化设计决策 + 数学比例 | 企业应用、设计系统、受监管行业 |
| `AccessLint` | WCAG 2.1 AA 自动化检查 + 重构 | 所有面向公众的 Web 应用 |

bencium 的独特贡献是**认真程度**——28,000 字的 SKILL.md 不是堆砌，而是真正将专业 UX 设计师的知识体系系统化。AccessLint 则是将无障碍合规从"发布后的检查项"变成"开发中的实时反馈"。

---

**下一篇** → `07_shinpr_claude_code_workflows_frontend.md`  
shinpr/claude-code-workflows 前端工作流插件深度解析：多 Agent 协作、frontend recipe 系统、设计→开发→验证全链路

---

*调查时间：2025年4月 | 数据来源：github.com/bencium, agentskills.so, playbooks.com, snyk.io*
