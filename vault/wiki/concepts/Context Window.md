---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-tools, resource-management, efficiency]
aliases: ["Context Window", "Context Limit", "上下文窗口"]
relates_to:
  - target: "[[Claude Code]]"
    type: constrained_by
  - target: "[[Agent Skills 三层渐进式加载]]"
    type: optimized_by
  - target: "[[jezweb/claude-skills]]"
    type: principle_for
supersedes: null
---

# Context Window

## 概述
AI模型能够处理的最大上下文长度限制，是影响AI编码工具性能和功能设计的关键因素，需要通过各种优化策略进行管理。

## 关键内容

1. **基本概念**：
   - AI模型能够处理的最大上下文长度
   - 限制了可同时加载的信息量
   - 影响AI编码工具的性能表现

2. **对[[Skills]]系统的影响**：
   - [[Claude Code]]将[[Skills|Skill]] description字段总量限制在约[[上下文窗口]]的2%
   - 超出部分会被静默忽略
   - 需要通过[[渐进式加载]]等机制优化利用

3. **最佳实践**：
   - 不要安装太多Plugin，避免description重复占用过多上下文
   - description要精确，使用明确的触发短语
   - 合理分层使用[[Skills]]（个人通用放在~/.claude/skills/，项目专属放在.claude/skills/）

4. **项目设计原则**：
   - [[jezweb-claude-skills|jezweb/claude-skills]]项目强调"The context window is a public good"，只包含[[Claude_Code|Claude]]不知道的信息
   - "Teach patterns, not ship scripts"，[[Skills|技能]]描述做什么，由[[Claude_Code|Claude]]生成适应环境的脚本

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文
- [[04_jezweb_claude_skills_frontend]] — jezweb/claude-skills Context Window 哲学

## 相关
- [[Claude Code]] — constrained_by
- [[Agent Skills 三层渐进式加载]] — optimized_by