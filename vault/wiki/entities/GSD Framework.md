---
type: project
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, project-management, automation, AI工程]
aliases: ["GSD", "Get Shit Done", "GSD Framework"]
relates_to:
  - target: "[[Context File System]]"
    type: implements
  - target: "[[Agent Skills 三层渐进式加载]]"
    type: uses
  - target: "[[Claude Code]]"
    type: extends
supersedes: null
---

# GSD Framework

## 概述
一个AI驱动的项目管理系统，通过结构化的[[GSD Planning Directory|.planning/]]目录实现持久化项目记忆，提供从需求讨论到执行验证的完整工作流。

## 关键内容

1. **核心哲学**：
   - 外部化项目记忆，结构化信息流，按需注入上下文
   - 解决LLM缺乏持久化记忆的问题
   - 提供跨会话连续工作的能力

2. **主要组件**：
   - [[GSD Planning Directory|.planning/]]目录系统：包含PROJECT.md、REQUIREMENTS.md、ROADMAP.md等多个结构化文件
   - 阶段化工作流：new-project → discuss → plan → execute → verify
   - [[Nyquist Validation Layer|Nyquist验证层]]：将需求映射到可运行测试的[[Nyquist Validation Layer|验证合约]]

3. **工作流机制**：
   - 棕地项目支持：通过codebase/分析器自动识别现有代码库
   - 阶段化执行：每个阶段独立管理，支持并行和依赖关系
   - 会话恢复：通过STATE.md和HANDOFF.json实现精确的会话快照恢复

## 来源
- [[raw/articles/ai-tools/claude-skills/02-context-file-system.md]] — 主要设计理念和功能介绍

## 相关
- [[Context File System]] — implements
- [[Agent Skills 三层渐进式加载]] — uses
- [[Claude Code]] — extends