---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, specification, anthropic]
aliases: ["Agent Skills", "Skills"]
entity_type: project
relates_to:
  - target: "[[Claude Code]]"
    type: extends
  - target: "[[Custom Slash Commands]]"
    type: supersedes
  - target: "[[OpenAI Codex]]"
    type: compares_to
  - target: "[[Cursor]]"
    type: compares_to
  - target: "[[web-artifacts-builder Skill]]"
    type: implements
  - target: "[[frontend-design Skill]]"
    type: implements
supersedes: null
---

# Agent Skills

## 概述
由[[Anthropic]]与社区共同制定的AI编码工具扩展规范([[agentskills.io]]/specification)，用于替代[[Custom Slash Commands]]，成为[[Claude Code]]、[[OpenAI Codex]]、[[Cursor]]、[[Gemini CLI]]等主流AI编码工具的统一扩展机制。

## 关键内容

1. **设计目的**：
   - 提供比单文件Prompt模板更完整的可复用能力包
   - 包含说明文档、辅助脚本、参考资料的完整目录结构

2. **核心特点**：
   - 不再是简单的单文件Prompt模板
   - 包含完整的目录结构，支持文档、脚本和参考资料

3. **三层[[渐进式加载]]机制**：
   - 第1层：启动时加载skill的name + description（约100 tokens/skill）
   - 第2层：任务匹配后[[渐进式披露（Progressive Disclosure）|按需加载]]完整[[SKILL.md]]内容（<5,000 tokens）
   - 第3层：执行过程中明确需要时加载references/中的内容

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文

## 相关
- [[Claude Code]] — extends
- [[Custom Slash Commands]] — supersedes
- [[SKILL.md]] — implements
- [[OpenAI Codex]] — compares_to
- [[Cursor]] — compares_to