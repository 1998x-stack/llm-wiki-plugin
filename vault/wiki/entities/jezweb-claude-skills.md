---
type: project
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [claude-skills, frontend, react, tailwind, AI工程]
aliases: ["jezweb/claude-skills", "jezweb Skills"]
relates_to:
  - target: "[[Claude Code]]"
    type: extends
  - target: "[[shadcn/ui]]"
    type: uses
  - target: "[[Tailwind CSS v4]]"
    type: uses
  - target: "[[React]]"
    type: uses
  - target: "[[Agent Skills]]"
    type: extends
  - target: "[[Context Window]]"
    type: implements
  - target: "[[Frontend Plugin]]"
    type: includes
  - target: "[[ERRATA mechanism]]"
    type: implements
  - target: "[[Design Review]]"
    type: includes
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# jezweb/claude-skills

## 概述
社区最活跃的 [[Claude Code Skills]] [[仓库]]之一，由 Jeremy Dawes (Jez) 开发，专注于前端 [[React]] 风格的[[Skills|技能]]实现，强调工程实现和错误预防。项目核心理念是"[[上下文窗口]]是公共资源"，只包含 [[Claude_Code|Claude]] 不知道的信息。

## 关键内容
1. **设计理念**：与 [[Anthropic]] 官方 [[Skills]] 不同，jezweb [[Skills]] 注重工程实现和错误预防，每个 [[Skills|Skill]] 必须产出可见成果。项目有明确的 documented errors 数量统计和版本锁定机制。

2. **插件结构**：包含 10 个插件，63 个[[Skills|技能]]，其中 [[Frontend Plugin]] 包含 10 个前端相关[[Skills|技能]]，涵盖了从 [[Tailwind CSS v4|Tailwind v4]] 主题[[Configuration|配置]]到完整落地页生成的完整工作流。

3. **[[Frontend Plugin]]**：前端插件包含多个核心[[Skills|技能]]，如 tailwind-theme-builder（[[Tailwind CSS v4|Tailwind v4]] 主题基础设施）、shadcn-ui（组件安装[[Configuration|配置]]）、react-patterns（[[React 19]] 性能模式）、design-review（[[Design Review|设计质量审查]]）等。

4. **错误预防机制**：通过 [[ERRATA 机制|ERRATA.md]] 管理版本变更，避免频繁修改核心[[Skills|技能]]内容，确保[[Skills|技能]]内容的稳定性。ERRATA状态生命周期包括active→absorbed→outdated。

5. **全栈集成**：设计考虑了完整的 [[Cloudflare]] 全栈部署链路，从前端到 [[Cloudflare]] [[Worker Agent|Worker]]s 的完整流程。

6. **核心原则**：
   - "The context window is a public good" — 只包含 [[Claude_Code|Claude]] 不知道的内容
   - "Teach patterns, not ship scripts" — [[Skills|技能]]描述做什么，由 [[Claude_Code|Claude]] 生成适应环境的脚本
   - 每个[[Skills|技能]]必须产生可见输出（文件、[[Configuration|配置]]、可部署项目）

## 来源
- [[04_jezweb_claude_skills_frontend]] — jezweb/claude-skills Frontend Plugin 深度解析

## 相关
- [[Claude Code]] — 扩展平台
- [[shadcn/ui]] — 使用的技术
- [[Tailwind CSS v4]] — 使用的技术
- [[React]] — 使用的技术
- [[Agent Skills]] — 技能类型扩展