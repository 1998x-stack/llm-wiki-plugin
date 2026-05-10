---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: [claude-code, skills, workflow, plugin]
aliases: ["Superpowers", "Superpowers Skills"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[Agent Skills]]"
    type: implements
---

# Superpowers

## 概述
一套为 [[Claude Code]] 设计的 [[Agent Skills]] 集合，通过专业化分工的[[Agent Skills|技能系统]]（brainstorming、[[writing-plans Skill|writing-plans]]、[[using-git-worktrees Skill|using-git-worktrees]] 等）实现高质量软件开发的完整工作流。

## 关键内容

1. **核心[[Skills|技能]]列表**：
   - **brainstorming**：创意探索与需求澄清
   - **[[writing-plans Skill|writing-plans]]**：将设计文档拆解为原子任务清单
   - **[[using-git-worktrees Skill|using-git-worktrees]]**：创建隔离工作区
   - **[[subagent-driven-development Skill|subagent-driven-development]]**：[[子 Agent & 多 Agent 系统|子 Agent]] 驱动开发
   - **[[executing-plans Skill]]**：计划执行（无[[子 Agent & 多 Agent 系统|子 Agent]] 平台）
   - **[[dispatching-parallel-agents Skill|dispatching-parallel-agents]]**：并行[[子 Agent & 多 Agent 系统|子 Agent]] 调度
   - **finishing-a-development-branch**：开发分支收尾
   - **verification-before-completion**：完成前验证

2. **工作流链路**：
   ```
   brainstorming（设计批准）
   → using-git-worktrees（创建 worktree）
   → writing-plans（原子任务清单）
   → subagent-driven-development / executing-plans（实现）
   → verification-before-completion（验证）
   → finishing-a-development-branch（收尾）
   ```

3. **核心原则**：
   - **专业化分工**：每个 [[Skills|Skill]] 负责特定阶段
   - **文件系统通信**：通过文件而非上下文传递信息
   - **隔离与并行**：[[Git Worktree]] 支持并行开发
   - **TDD**：每个任务以测试开始

4. **与 GSD 的区别**：
   - **Superpowers**：通用软件开发[[Skills|技能]]集
   - **GSD**：完整项目管理框架（含 [[GSD Planning Directory|.planning/]] 目录系统）

## 来源
- [[03-writing-plans]] — writing-plans Skill
- [[04-using-git-worktrees]] — using-git-worktrees Skill
- [[01_claude_code_skill_system_overview]] — 系统架构全景

## 相关
- [[Claude Code]] — uses
- [[Agent Skills]] — implements
- [[GSD]] — compares_to
- [[writing-plans Skill]] — part_of
- [[using-git-worktrees Skill]] — part_of
