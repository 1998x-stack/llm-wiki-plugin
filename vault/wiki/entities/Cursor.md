---
type: tool
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["ai-tools", "coding-assistant", "ide", "git", "workflow", "工具与框架"]
aliases: ["Cursor", "Cursor IDE", "Cursor.sh"]
relates_to:
  - target: "[[Claude Code]]"
    type: compares_to
  - target: "[[OpenAI Codex]]"
    type: compares_to
  - target: "[[Agent Skills]]"
    type: uses
  - target: "[[Git Worktree]]"
    type: supports
  - target: "[[Write-Tools]]"
    type: compares_to
  - target: "[[AST-based diff]]"
    type: implements
---

# Cursor

## 概述
AI 原生代码编辑器，基于 [[VS Code]] 构建，支持 [[Agent Skills]] 规范，与 [[Claude Code]]、[[OpenAI Codex]]、[[Gemini CLI]] 共同采用 [[agentskills.io]] 扩展标准。在 [[Write-Tools]] 实现中采用了先进的 [[AST-based diff]] 技术，提供了精确的代码修改能力。

## 关键内容

1. **定位**：基于 [[VS Code]] 的 AI 编程 IDE
2. **[[Agent Skills]] 支持**：支持 [[Agent Skills]] 规范
3. **跨工具兼容**：与 [[Claude Code]]、[[OpenAI Codex]]、[[Gemini CLI]] 共享 [[Skills|Skill]] 生态
4. **[[Write-Tools|Write Tools]] 实现**：
   - 采用 [[AST-based diff]] 技术，这是目前最精确的方案——不依赖行号，直接在语法树层面做 diff，彻底解决了 unified patch 的行号漂移问题
   - 无传统意义上的[[Claude Code 沙箱机制|沙箱]]（在 IDE 内运行），信任环境中的代码修改操作
   - 采用 inline accept/reject 模式，用户可以直接在编辑器中接受或拒绝 AI 建议的修改
   - 采用 AST 感知的大文件处理策略，能够理解代码结构而非简单的行号定位
   - 部分支持多文件事务（通过 Composer 功能）

## 来源
- [[01_claude_code_skill_system_overview]] — 系统架构全景
- [[04-using-git-worktrees]] — Git Worktree 支持情况
- [[write-tools.md]] — 八、横向对比

## 相关
- [[Claude Code]] — compares_to
- [[OpenAI Codex]] — compares_to
- [[Gemini CLI]] — compares_to
- [[Agent Skills]] — uses
- [[Git Worktree]] — supports
- [[Write-Tools]] — compares_to
- [[AST-based diff]] — implements
