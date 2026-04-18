---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["claude-code", "skill", "frontend", "design-system", "工具与框架"]
aliases: ["frontend-design", "frontend-design Skill"]
relates_to:
  - target: "[[AI Slop]]"
    type: contradicts
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[Anthropic]]"
    type: created_by
---

# frontend-design Skill

## 概述
[[Anthropic]] 官方 Skill，指导创建独特、生产级前端界面，避免通用的"[[AI Slop]]"美学，强制在编码前进行设计决策（Purpose → Tone → Constraints → Differentiation）。

## 关键内容

1. **安装方式**：
   ```bash
   /plugin marketplace add anthropics/skills
   /plugin install frontend-design@anthropics/skills
   ```

2. **核心定位**：
   - **distinctive**（独特的）：每次生成的设计都应该不同
   - **production-grade**（生产级）：真实可用的代码
   - **real working code**（真实可运行代码）：不允许伪代码或占位符

3. **设计前思考框架**：
   - **Purpose**：界面解决什么问题？谁使用它？
   - **Tone**：美学方向（必须选一个极端彻底执行）
   - **Constraints**：技术要求（框架、性能、无障碍）
   - **Differentiation**：什么让这令人难忘？

4. **美学方向选项**：
   - brutally minimal（极简暴力）
   - maximalist chaos（最大化混乱）
   - retro-futuristic（复古未来）
   - organic/natural（有机自然）
   - luxury/refined（奢华精致）
   - playful/toy-like（玩具感）
   - editorial/magazine（杂志感）
   - brutalist/raw（野兽派）
   - art deco/geometric（装饰艺术）
   - soft/pastel（柔和粉彩）

5. **五大设计维度**：
   - **Typography**：禁止 Inter/Roboto，选择独特有个性字体
   - **Color & Theme**：主色调 + 锐利对比色，避免紫色渐变
   - **Motion**：staggered reveal、物理反馈微交互
   - **Spatial Composition**：打破居中容器，尝试不对称布局
   - **Backgrounds**：渐变网格、噪点纹理、几何图案

6. **实现底线**：
   - ✅ 完整实现所有交互逻辑
   - ✅ 处理 loading/error/empty 状态
   - ✅ 正确的语义 HTML
   - ✅ 基本无障碍（ARIA labels）
   - ❌ 不允许 `// TODO` 或占位符

## 来源
- [[02_anthropic_frontend_design_skill]] — frontend-design Skill 解析
- GitHub: anthropics/skills

## 相关
- [[AI Slop]] — contradicts
- [[Claude Code]] — uses
- [[Anthropic]] — created_by
- [[Design Thinking]] — implements
