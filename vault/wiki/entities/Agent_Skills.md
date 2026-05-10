---
type: entity
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-tools, extension-system, specification]
aliases: ["Agent Skills", "Skills System", "agentskills.io"]
relates_to: []
supersedes: null
---

# Agent Skills

## 概述
[[Agent Skills]] 是 [[Anthropic]] 与社区共同制定的 AI 扩展规范，被 [[Claude Code]]、[[OpenAI Codex]]、[[Cursor]]、[[Gemini CLI]] 等工具采用。

## 关键内容

1. **发展历史**：
   - 作为 [[Custom Slash Commands]] 的超集，全面替代后者
   - 不再是简单的单文件 Prompt 模板，而是完整的目录结构

2. **文件结构**：
   - 每个 [[Skills|Skill]] 是一个目录，包含 [[SKILL.md]] 核心文件
   - 可选包含 scripts、references、assets 等子目录
   - [[SKILL.md]] 包含 YAML frontmatter 和 Markdown 指令

3. **三层加载机制**：
   - 第1层：启动时加载 name + description（约100 tokens/skill）
   - 第2层：任务匹配后[[渐进式披露（Progressive Disclosure）|按需加载]]完整 [[SKILL.md]] 内容（<5,000 tokens）
   - 第3层：执行过程中明确需要时加载参考资料

## 来源
- [[01_claude_code_skill_system_overview.md]] — 详细说明
- [[]] —

## 相关
- [[Claude Code]] — implements
- [[Custom Slash Commands]] — supersedes
- [[SKILL.md]] — implements