---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [claude, documentation, ai-agent, project-setup]
aliases: ["CLAUDE.MD", "Claude Markdown", "Project Context File"]
relates_to:
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[Skills]]"
    type: related_to
  - target: "[[AGENTS.MD 项目约定文件]]"
    type: related_to
supersedes: null
---

# CLAUDE.MD

## 概述
CLAUDE.MD 是为 AI agent 提供最优项目入门上下文的特殊文件，在每次 [[Claude Code]] 对话中自动包含，是让 AI agent 了解代码库的主要入门文档。

## 关键内容

1. **核心原则**：
   - LLM 是无状态的：CLAUDE.MD 是每次对话中唯一会自动包含的文件
   - 少即是多：前沿 LLM 大约能遵循 150-200 条指令，[[Claude Code]] 的系统提示词本身已占约 50 条，因此 CLAUDE.MD 必须聚焦且简洁
   - 只放通用信息：只包含每次会话都适用的内容
   - 不要把 [[Claude_Code|Claude]] 当成 lint 工具：风格指南会膨胀上下文并降低指令遵循效果

2. **内容策略 (WHAT, WHY, HOW)**：
   - **WHAT** - 技术与结构：技术栈概览、项目组织方式、关键目录及其用途
   - **WHY** - 目的与背景：项目功能、架构决策原因、各组件职责
   - **HOW** - 工作流与约定：开发流程、测试命令、构建方法、关键"坑点"

3. **渐进式披露策略**：
   - 对较大项目建议创建 `agent_docs/` 文件夹
   - 例如 `agent_docs/building_the_project.md`、`agent_docs/running_tests.md`
   - 在 CLAUDE.MD 中引用这些文件，避免内容过多

4. **必备章节结构**：
   - 技术栈（主语言、关键框架、数据库）
   - 项目结构（对 monorepo 尤其重要）
   - 开发命令（安装、测试、构建）
   - 关键约定（只保留非显而易见、高影响的约定）
   - 已知问题/坑点（常让开发者踩坑的内容）

## 来源
- [[raw/assets/claude-howto/03-skills/claude-md/SKILL.md]] — 官方技能文档
- [[Claude How To Slash Commands Reference]] — 配置指南

## 相关
- [[Claude Code]] — part_of
- [[Skills]] — relates_to
- [[AGENTS.MD 项目约定文件]] — relates_to
- [[Context Engineering]] — relates_to