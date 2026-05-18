---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [git, workflow, isolation, superpowers, multi-agent, Agent系统]
aliases: ["Git Worktree", "Git Worktrees", "工作树", "Git Subtree"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[using-git-worktrees Skill]]"
    type: implements
  - target: "[[dispatching-parallel-agents Skill]]"
    type: enables
  - target: "[[Claude Code]]"
    type: supported_by
  - target: "[[Codex CLI|Codex]]"
    type: supported_by
---

# Git Worktree

## 概述
Git 功能，允许一个[[仓库]]拥有多个独立工作目录，每个目录对应不同分支，支持同时在多个分支上工作互不干扰，是 [[Superpowers]] 实现并行[[子 Agent & 多 Agent 系统|子 Agent]] 隔离的核心机制。

## 关键内容

1. **与普通分支的区别**：
   - **普通分支**：一个工作目录 + 多个分支（切换改变内容）
   - **Git Worktree**：一个 `.git` + 多个独立工作目录（同时工作）

2. **为什么需要 Worktree**：
   - **保护主分支**：防止实验性代码混入稳定代码
   - **支持并行[[子 Agent & 多 Agent 系统|子 Agent]]**：每个 Agent 独立工作目录，互不覆盖
   - **建立测试基线**：清晰[[区分]]"修改引入的失败"和"预先存在的失败"

3. **常用命令**：
   ```bash
   # 创建 worktree + 新分支
   git worktree add ../project-feature-name -b feature/name
   
   # 列出所有 worktrees
   git worktree list
   
   # 删除 worktree
   git worktree remove ../project-feature-name
   
   # 清理失效记录
   git worktree prune
   ```

4. **命名约定**：
   - `../<project-name>-<feature-name>/`
   - 例：`../superpowers-feature-login/`
   - 放父目录（`../`）防止被主仓库 `.gitignore` 处理

5. **Worktree 生命周期**：
   ```
   brainstorming（设计批准）
   → using-git-worktrees（创建 worktree）
   → writing-plans（在 worktree 中规划）
   → subagent-driven-development（在 worktree 中实现）
   → verification-before-completion（在 worktree 中验证）
   → finishing-a-development-branch（清理 worktree）
   ```

6. **并行场景**：
   ```bash
   # 主 Agent 为并行任务创建多个 worktrees
   git worktree add ../project-task-1 -b feature/task-1
   git worktree add ../project-task-2 -b feature/task-2
   git worktree add ../project-task-3 -b feature/task-3
   ```

7. **平台支持**：
   | 平台 | 支持 |
   |------|------|
   | [[Claude Code]] | ✅ 完整 |
   | [[Codex CLI|Codex]] | ✅ 完整 |
   | [[Cursor]] | ✅ 完整 |
   | [[Gemini CLI]] | ⚠️ 部分 |

## 来源
- [[04-using-git-worktrees]] — using-git-worktrees Skill 解析

## 相关
- [[Superpowers]] — part_of
- [[using-git-worktrees Skill]] — implements
- [[dispatching-parallel-agents Skill]] — uses
