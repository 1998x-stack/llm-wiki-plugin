# Skill 04：using-git-worktrees — 为每个功能开辟隔离工作岛

> **系列位置**：Superpowers 深度解析 · 第 4 篇  
> **SKILL.md 位置**：`skills/using-git-worktrees/SKILL.md`  
> **触发时机**：设计批准后、实现开始之前（brainstorming → **using-git-worktrees** → writing-plans）

---

## 一句话定位

`using-git-worktrees` 在设计批准后、代码开始写之前，为当前功能创建一个独立的 Git Worktree——一个与主仓库共享 `.git` 历史、却拥有独立工作目录和分支的"工作岛"——确保所有实现工作在隔离空间进行，不污染主分支，且天然支持并行子 Agent。

---

## 什么是 Git Worktree？先搞清楚概念

大多数开发者熟悉 Git 分支（Branch），但不了解 Git Worktree。

```
普通分支切换（Branch checkout）：
  一个工作目录 + 多个分支
  切换分支会改变工作目录的内容
  → 无法同时在两个分支上工作

Git Worktree：
  一个 .git 仓库 + 多个独立工作目录
  每个工作目录对应一个分支
  → 可以同时在多个分支上工作，互不干扰
```

```bash
# 查看当前所有 worktrees
git worktree list
# 输出：
# /home/user/myproject          abc1234 [main]
# /home/user/myproject-feature  def5678 [feature/login]
```

---

## 为什么 Superpowers 流水线需要 Worktree？

### 原因 1：保护主分支

没有 worktree 隔离，Agent 可能直接在 `main` 分支上写代码：

```
❌ 不隔离的风险：
main 分支 ← Agent 直接在这里工作
  ├── 实验性代码混入稳定代码
  ├── 半完成的功能影响其他开发者
  └── 难以回滚到之前的稳定状态
```

### 原因 2：支持并行子 Agent

`dispatching-parallel-agents` 需要同时运行多个子 Agent，每个处理不同的独立任务。没有独立工作目录，多个 Agent 会互相覆盖文件修改：

```
主仓库 (.git)
├── ../myproject-feature-login/     ← 子 Agent A 独立工作
├── ../myproject-feature-search/    ← 子 Agent B 独立工作  
└── ../myproject-feature-analytics/ ← 子 Agent C 独立工作
```

三个 Agent 同时运行，各自的文件修改完全隔离，最终由主 Agent 汇总。

### 原因 3：建立干净的测试基线

在实现工作开始之前，必须知道"起点状态"是什么：哪些测试是已经通过的，哪些是已经失败的。这样才能在实现完成后，清晰地区分"我的修改引入的失败"和"本来就有的失败"。

---

## 完整执行步骤

```
Step 1: 确定基础分支（通常是 main 或 master）
        git branch -v

Step 2: 创建 worktree（新分支）
        git worktree add ../myproject-feature-login -b feature/login

Step 3: 进入 worktree 目录
        cd ../myproject-feature-login

Step 4: 运行项目设置
        npm install          # Node.js 项目
        pip install -r requirements.txt  # Python 项目
        bundle install       # Ruby 项目
        # 等等，根据项目类型

Step 5: 验证测试基线
        pytest               # 运行完整测试套件
        # 记录：通过 N 个，失败 M 个（M 是预先存在的，不是我引入的）

Step 6: 宣告工作区就绪，移交给下一个技能
        "Worktree ready at ../myproject-feature-login"
        "Baseline: 47 passed, 2 pre-existing failures (tracked in TODO)"
```

**如果测试基线不干净（有预先存在的失败）**：记录下来，但不要在这里修复。专注于建立基线，实现工作继续。

---

## 命令速查

### 创建 Worktree

```bash
# 创建新 worktree + 新分支（最常用）
git worktree add ../project-feature-name -b feature/name

# 创建新 worktree + 已有分支
git worktree add ../project-hotfix hotfix/critical-bug

# 创建新 worktree + detached HEAD（用于只读探索）
git worktree add --detach ../project-explore abc1234
```

### 查看和管理

```bash
# 列出所有 worktrees
git worktree list

# 详细列出（带 porcelain 格式）
git worktree list --porcelain

# 清理失效的 worktree 记录（worktree 目录被手动删除后）
git worktree prune
```

### 删除 Worktree

```bash
# 正常删除（无未提交修改时）
git worktree remove ../project-feature-name

# 强制删除（有未提交修改时，慎用）
git worktree remove --force ../project-feature-name

# 删除 worktree 后还可以选择删除对应分支
git branch -d feature/name        # 安全删除（已合并时）
git branch -D feature/name        # 强制删除（未合并也删）
```

---

## 命名约定

Superpowers 推荐 worktree 目录名遵循：

```
../<project-name>-<feature-name>/
```

例如：
```
../superpowers-feature-login/
../superpowers-hotfix-auth-bug/
../superpowers-refactor-database-layer/
```

放在父目录（`../`），而不是子目录，防止 worktree 的文件被主仓库的 `.gitignore` 或工具意外处理。

---

## Worktree 生命周期：从创建到清理

```
brainstorming 设计批准
        ↓
using-git-worktrees（创建 worktree）← 你在这里
        ↓
writing-plans（在 worktree 环境下规划）
        ↓
subagent-driven-development（在 worktree 中实现）
        ↓
verification-before-completion（在 worktree 中验证）
        ↓
finishing-a-development-branch（清理 worktree）
```

`finishing-a-development-branch` 技能负责收尾：根据用户选择（合并/PR/放弃），执行 `git worktree remove` 并清理分支。

---

## 并行场景：多 Worktree 协作

当 `dispatching-parallel-agents` 处理并行任务时，主 Agent 需要提前为每个并行任务组创建独立的 worktree：

```bash
# 主 Agent 为并行任务创建多个 worktrees
git worktree add ../project-task-1 -b feature/task-1
git worktree add ../project-task-2 -b feature/task-2  
git worktree add ../project-task-3 -b feature/task-3

# 各子 Agent 在各自的 worktree 中工作
# 子 Agent A: cd ../project-task-1 && 实现 Task 1
# 子 Agent B: cd ../project-task-2 && 实现 Task 2
# 子 Agent C: cd ../project-task-3 && 实现 Task 3
```

---

## 平台差异

| 平台 | Worktree 支持 | 注意事项 |
|------|-------------|---------|
| Claude Code | ✅ 完整 | 原生支持，自动处理 |
| Codex | ✅ 完整 | 需配置 `multi_agent = true` |
| Cursor | ✅ 完整 | 通过 terminal 操作 |
| Gemini CLI | ⚠️ 部分 | 没有子 Agent 但 worktree 本身可用 |

---

## 常见问题

**Q：worktree 里的文件修改会影响主仓库吗？**
A：不会，文件系统完全隔离。但 commits 是共享到同一个 `.git` 历史的，所以 worktree 里的 commit 在主仓库也可以看到（通过 `git log --all`）。

**Q：能在 worktree 里 `git stash` 吗？**
A：可以，但 stash 是全局的（对整个 `.git` 仓库），不是 worktree 独有的。建议用 commit 代替 stash 在 worktree 间保存状态。

**Q：worktree 有数量限制吗？**
A：没有硬性限制，但过多的 worktree 会让 `git worktree list` 混乱。Superpowers 推荐任务完成后立即清理。

---

*上一篇：[Skill 03：writing-plans] | 下一篇：[Skill 05：subagent-driven-development]*
