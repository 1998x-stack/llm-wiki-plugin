# GSD 深度解析 · 第六篇：UI 设计契约系统

> **上一篇**：[第五篇——XML 结构化计划系统](./05-xml-plan-system.md)

---

## 一、为什么 AI 生成的前端视觉不一致？

这是一个让很多人困惑的现象：Claude Code 单独写一个组件时做得很好，但当你让它写第五个、第十个组件时，整个 UI 看起来像是出自多个不同的设计师之手——间距比例各异、颜色使用不统一、按钮文案风格迥然不同。

问题不在于 Claude 不会写 UI。**问题在于：执行前没有设计契约。**

五个组件在没有共享规范的情况下构建：

```
组件 1（早期会话）:  padding: 16px,  按钮文案:"Submit"
组件 2（中期会话）:  padding: 12px,  按钮文案:"Save Changes"
组件 3（子智能体A）: padding: 20px,  按钮文案:"Confirm"
组件 4（子智能体B）: padding: 16px,  按钮文案:"Done"
组件 5（后期会话）:  padding: 8px,   按钮文案:"Update"
```

每个单独看都合理，合在一起就是视觉噪声。

GSD v1.x 引入了 **UI 设计契约系统**，在执行前锁定设计规范，在执行后量化审计结果。核心是两个命令：`/gsd:ui-phase` 和 `/gsd:ui-review`。

---

## 二、`/gsd:ui-phase`：执行前生成设计契约

### 2.1 何时运行

```
标准工作流位置：

discuss-phase N     ← 捕获功能实现偏好（业务逻辑层面）
    ↓
ui-phase N          ← 生成 UI 设计契约（视觉规范层面）  ← 这里
    ↓
plan-phase N        ← 基于 CONTEXT.md + UI-SPEC.md 生成计划
    ↓
execute-phase N     ← 执行器读取 UI-SPEC.md，保持设计一致性
```

只有包含前端/UI 工作的阶段才需要运行。纯 API、数据库迁移、CLI 工具等阶段可以跳过。

### 2.2 内部流程

```
/gsd:ui-phase N
       │
       ├── 读取 CONTEXT.md（功能偏好决策）
       ├── 读取 RESEARCH.md（技术栈信息）
       ├── 读取 REQUIREMENTS.md（本阶段需求）
       │
       ├── 检测现有设计系统状态
       │     ├── shadcn components.json 是否存在？
       │     ├── Tailwind config 中有哪些自定义 token？
       │     └── 现有组件使用了哪些设计模式？
       │
       ├── [条件] shadcn 初始化门控（见 2.3）
       │
       ├── 只询问尚未决定的设计问题（避免重复已有决策）
       │     ├── 间距系统（4px / 8px / 自定义基数？）
       │     ├── 字体层级（几级标题？正文 line-height？）
       │     ├── 颜色策略（强调色数量？60/30/10 分配？）
       │     ├── 文案风格（动词优先？第几人称？语气？）
       │     └── 空状态/加载状态/错误状态的处理规范
       │
       ├── 生成 {N}-UI-SPEC.md
       │
       ├── 6 维度验证（见 2.4）
       │     └── 不通过则迭代修改，最多 2 次
       │
       └── 输出：{padded_phase}-UI-SPEC.md
```

### 2.3 shadcn 初始化门控

对于 React/Next.js/Vite 项目，如果检测到没有 `components.json`，GSD 会提供 shadcn 初始化指引：

```bash
# 步骤 1：访问 shadcn 预设配置器
open https://ui.shadcn.com/create

# 步骤 2：配置你的设计系统（颜色、圆角、字体）并复制 preset 字符串
# 例如: --preset zinc --radius 0.5 --base-color zinc

# 步骤 3：使用 preset 初始化
npx shadcn init --preset zinc
```

**为什么 preset 是一等公民？**

Preset 字符串编码了整个设计系统——颜色、border-radius、字体。它成为 GSD 规划产物的一部分，确保每个阶段、每个执行器都在同一套设计系统上工作，跨里程碑保持一致性。

### 2.4 6 维度验证（生成阶段）

`ui-phase` 生成 UI-SPEC.md 后，会从 6 个维度自我验证：

| 维度 | 验证内容 |
|------|----------|
| Copywriting | CTA 文案规范是否定义？空状态/错误状态文案策略是否明确？ |
| Visuals | 视觉焦点层级是否有设计原则？图标使用规范是否统一？ |
| Color | 颜色 token 是否定义完整？强调色使用限制是否明确？ |
| Typography | 字体层级数量是否合理？字重使用约束是否有规范？ |
| Spacing | 间距基数系统是否确立？栅格规范是否定义？ |
| Registry Safety | 第三方 shadcn 组件是否通过安全审查流程？（见 2.5）|

验证不通过则迭代修改，最多循环 2 次。若仍有 BLOCKED 维度，会将问题呈现给开发者手动处理。

### 2.5 Registry 安全门控

第三方 shadcn registry（如社区组件库）可以注入任意代码。GSD 在 `ui_safety_gate` 启用时（默认启用）要求：

```bash
# 安装任何第三方 shadcn 组件前，必须先检查
npx shadcn view <component-name>     # 查看完整源代码

# 与官方版本对比
npx shadcn diff <component-name>     # 检查与官方的差异
```

这个门控可以通过 `workflow.ui_safety_gate: false` 关闭（不建议在生产项目中关闭）。

---

## 三、`/gsd:ui-review`：执行后量化视觉审计

### 3.1 何时运行

```
execute-phase N 完成之后，或 verify-work N 之后运行：

execute-phase N     ← 代码写完了
    ↓
verify-work N       ← 功能验证通过
    ↓
ui-review N         ← 视觉质量量化审计  ← 这里
```

**独立性**：`ui-review` 也可以在任何没有使用 GSD 的前端项目上运行。如果没有 `UI-SPEC.md`，它会基于抽象的 6 柱标准进行审计。

### 3.2 6 柱评分体系（1-4 分制）

每个柱次 1-4 分，总分 24 分：

**柱 1：Copywriting（文案质量）**

```
1分：CTA 使用通用文案（"Submit", "Click here"）
2分：CTA 有动词，但空状态/错误状态文案缺失
3分：主要场景文案清晰，边缘情况有覆盖
4分：所有文案动词化、场景化，错误消息有指引性
```

检查项：
- CTA 按钮文案是否使用动词（"Save Draft" vs "OK"）
- 空状态是否有操作引导（不是简单的"暂无数据"）
- 错误状态文案是否告诉用户下一步该怎么办
- 加载状态是否有进度或预期时间提示

**柱 2：Visuals（视觉质量）**

```
1分：页面没有明显视觉焦点，信息密度混乱
2分：有主要视觉焦点，但层级不够清晰
3分：视觉层级明确，主/次操作有差异化处理
4分：视觉叙事完整，眼动路径符合设计意图
```

检查项：
- 页面上最重要的操作/信息是否最突出
- 图标是否可访问（有 aria-label 或 tooltip）
- 高密度区域是否有足够的呼吸空间
- 图片/图标的一致性（风格统一）

**柱 3：Color（颜色系统）**

```
1分：颜色使用随意，无系统可言
2分：主色调一致，但强调色过多或分散
3分：60/30/10 基本合规，强调色克制
4分：颜色使用高度克制，强调色精准指向主操作
```

60/30/10 原则：
- 60% 中性色（背景、容器、分割线）
- 30% 辅助色（次要内容、图标、次要按钮）
- 10% 强调色（CTA、重要信息、关键状态）

检查项：
- 强调色是否被稀释（如果到处都是强调色，就没有强调色）
- 颜色是否有语义一致性（红色=危险，绿色=成功，不要混用）
- 暗色/亮色模式切换时颜色对比度是否达标

**柱 4：Typography（字体排版）**

```
1分：字号和字重随意，无系统
2分：有字号层级，但字重不够克制（全部加粗）
3分：字号层级 ≤4 级，字重使用有约束
4分：字号层级 ≤3 级，只在必要时使用粗体，行高一致
```

检查项：
- 字号层级数量（超过 5 种通常是过度设计）
- 正文行高（1.5-1.7 是舒适阅读范围）
- 字重层级数量（一个页面超过 3 种字重通常显得混乱）
- 长文本是否有合适的 max-width（65-75 字符是理想阅读宽度）

**柱 5：Spacing（间距系统）**

```
1分：间距随意，无规律可循
2分：有大致的间距感，但不规律
3分：间距遵循 8px 或 4px 基数系统
4分：间距高度一致，栅格对齐精确，边距统一
```

检查项：
- 间距是否遵循基数系统（4px, 8px, 16px, 24px, 32px...）
- 相似元素之间的间距是否一致
- 页面边距是否统一
- 列表/表格的行间距是否规律

**柱 6：Experience Design（体验设计）**

```
1分：仅处理 happy path，loading/error/empty 状态缺失
2分：有 loading 状态，但 error/empty 状态缺失
3分：三种状态基本覆盖，但没有操作引导
4分：三种状态完整，且每种状态都有明确的下一步引导
```

检查项：
- 数据加载期间是否有 skeleton 或 spinner
- 网络错误是否有重试选项
- 空数据集是否有"添加第一条数据"的引导
- 提交中状态是否禁用按钮防止重复提交

### 3.3 输出产物

`ui-review` 生成 `{N}-UI-REVIEW.md`，包含：

```markdown
## UI Review — Phase 03 (Authentication UI)

### Scores
| Pillar | Score | Notes |
|--------|-------|-------|
| Copywriting | 3/4 | CTA 清晰，但密码重置的错误提示可改进 |
| Visuals | 4/4 | 视觉焦点明确，登录按钮突出度合适 |
| Color | 3/4 | 颜色克制，但错误状态红色与禁用灰色对比不足 |
| Typography | 4/4 | 字号层级 3 级，行高一致 |
| Spacing | 3/4 | 基本遵循 8px 系统，表单内间距略不一致 |
| Experience | 2/4 | 加载状态已实现，空状态缺失 |

**Total: 19/24**

### Top 3 Priority Fixes
1. **[Experience]** 添加密码重置后的成功状态页（目前没有确认反馈）
2. **[Color]** 错误状态文字（#ff4444）与输入框禁用背景（#f5f5f5）对比度不达标
3. **[Copywriting]** 登录失败提示从 "Invalid credentials" 改为 "邮箱或密码不正确，请重试"
```

### 3.4 截图存档

`ui-review` 通过 Playwright CLI 自动截图：

```
.planning/ui-reviews/
  phase-03-desktop-1440.png
  phase-03-mobile-375.png
  phase-03-dark-mode.png
  .gitignore           ← 自动创建，截图不进 git
```

里程碑完成（`/gsd:complete-milestone`）时，截图目录自动清理。

---

## 四、workflow 配置

```json
{
  "workflow": {
    "ui_phase": true,         // 是否为前端阶段生成设计契约
    "ui_safety_gate": true    // 是否启用 Registry 安全门控
  }
}
```

两个配置都遵循"absent=enabled"原则——配置项不存在时默认启用。

在 `plan-phase` 运行时，如果检测到是前端阶段且没有 `UI-SPEC.md`，GSD 会提示你先运行 `ui-phase`（由 `ui_safety_gate` 控制这个提示行为）。

---

## 五、实际使用建议

### 何时运行 `ui-phase`

```
✅ 新功能阶段，有明显的 UI 组件需要创建
✅ 跨多个子页面的阶段（如完整的用户设置页）
✅ 需要统一视觉语言的阶段（如 Dashboard 类页面）

⏭️ 可跳过：
- 纯 API/后端阶段
- 小范围文案修改
- CSS 微调（不涉及设计决策）
```

### 如何用好 `ui-review`

`ui-review` 的最大价值不在于总分高低，而在于 **Top 3 Priority Fixes**——它告诉你投入最小代价、获得最大视觉改善的三个修改点。

建议工作流：
1. 运行 `ui-review` 获取报告
2. 把 Top 3 作为 `/gsd:quick` 任务立即修复（无需完整规划流程）
3. 重新运行 `ui-review` 验证改进

### 与 Figma 设计稿的关系

GSD 的 `ui-phase` 是**代码优先**的设计契约，不依赖 Figma。它适合以下场景：
- 独立开发者，没有专业设计师参与
- 快速原型验证，设计和开发同步进行
- 已有设计系统（如 shadcn），只需约束使用规范

如果你有 Figma 设计稿，可以将设计决策作为 `ui-phase` 的输入（在对话中直接提供设计规范），GSD 会将其编码进 `UI-SPEC.md`。

---

## 六、小结

UI 设计契约系统解决了 AI 生成前端代码的最顽固问题：**不是 Claude 不会写 UI，而是每次执行都从零开始，缺乏跨组件、跨阶段的视觉一致性约束**。

`ui-phase` 在执行前建立契约，`ui-review` 在执行后量化审计，形成闭环。

---

> **下一篇**：[第七篇——配置、安全与高级功能](./07-config-security-advanced.md)

*参考来源：[GSD USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)*
