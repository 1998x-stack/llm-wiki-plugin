---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [skill, git, worktree, superpowers, workflow, isolation]
aliases: ["using-git-worktrees", "Git Worktree Skill", "工作树技能"]
relates_to:
  - target: "[[Git Worktree]]"
    type: implements
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[brainstorming Skill]]"
    type: follows
  - target: "[[writing-plans Skill]]"
    type: precedes
---
# using-git-worktrees Skill

## 概述
[[Superpowers]] 深度解析系列中的第4个[[Skills|技能]]，设计批准后、代码实现开始前，为当前功能创建独立的 [[Git Worktree]]——一个与主[[仓库]]共享 .git 历史却拥有独立工作目录和分支的"工作岛"，确保所有实现工作在隔离空间进行，不污染主分支，且天然支持并行[[子 Agent & 多 Agent 系统|子 Agent]]。

## 关键内容

1. **核心目的**：
   - **保护主分支**：避免实验性代码混入稳定代码，防止半完成功能影响其他开发者
   - **支持并行[[子 Agent & 多 Agent 系统|子 Agent]]**：为 [[dispatching-parallel-agents Skill|dispatching-parallel-agents]] 提供独立工作目录，防止多个 Agent 互相覆盖文件修改
   - **建立测试基线**：明确[[区分]]"修改引入的失败"和"预先存在的失败"

2. **执行时机**：
   - 触发时机：设计批准后、实现开始之前
   - 执行顺序：brainstorming → using-git-worktrees → [[writing-plans Skill|writing-plans]]
   - 作为 [[Superpowers]] 流水线的关键隔离步骤

3. **完整执行步骤**：
   ```
   Step 1: 确定基础分支（通常是 main 或 master）
   Step 2: 创建 worktree（新分支）：git worktree add ../project-feature-name -b feature/name
   Step 3: 进入 worktree 目录
   Step 4: 运行项目设置（npm install, pip install 等）
   Step 5: 验证测试基线
   Step 6: 宣告工作区就绪，移交给下一个技能
   ```

4. **命名约定**：
   - 格式：`../<project-name>-<feature-name>/`
   - 例如：`../superpowers-feature-login/`、`../superpowers-hotfix-auth-bug/`
   - 放在父目录（`../`），防止被主仓库的 `.gitignore` 处理

5. **常用命令**：
   ```bash
   # 创建新 worktree + 新分支（最常用）
   git worktree add ../project-feature-name -b feature/name
   
   # 列出所有 worktrees
   git worktree list
   
   # 删除 worktree
   git worktree remove ../project-feature-name
   
   # 清理失效的 worktree 记录
   git worktree prune
   ```

6. **生命周期管理**：
   - 创建于：brainstorming 设计批准后
   - 使用于：writing-plans、subagent-driven-development 等阶段
   - 清理于：finishing-a-development-branch 技能负责收尾

7. **并行场景应用**：
   ```bash
   # 主 Agent 为并行任务创建多个 worktrees
   git worktree add ../project-task-1 -b feature/task-1
   git worktree add ../project-task-2 -b feature/task-2
   git worktree add ../project-task-3 -b feature/task-3
   # 各子 Agent 在各自 worktree 中工作
   ```

## 来源
- [[04-using-git-worktrees]] — Skill 04：using-git-worktrees 解析

## 相关
- [[Git Worktree]] — implements
- [[Superpowers]] — part_of
- [[brainstorming Skill]] — follows
- [[writing-plans Skill]] — precedes
- [[dispatching-parallel-agents Skill]] — enables
- [[subagent-driven-development Skill]] — prepares environment for