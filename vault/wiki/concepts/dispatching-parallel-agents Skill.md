---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [skill, multi-agent, parallel, superpowers, workflow, isolation, AI工程]
aliases: ["dispatching-parallel-agents", "Parallel Agents Skill", "并行代理调度技能", "dispatching-parallel-agents Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[Git Worktree]]"
    type: uses
  - target: "[[subagent-driven-development Skill]]"
    type: relates_to
  - target: "[[using-git-worktrees Skill]]"
    type: follows_after
---
# dispatching-parallel-agents Skill

## 概述
[[Superpowers]] 框架中的一个关键[[Skills|技能]]，负责调度多个并行[[子 Agent & 多 Agent 系统|子 Agent]] 同时处理不同任务。该[[Skills|技能]]依赖 [[Git Worktree]] 为每个[[子 Agent & 多 Agent 系统|子 Agent]] 提供独立的工作目录，确保各 Agent 之间的工作不会相互干扰或覆盖。

## 关键内容

1. **核心机制**：
   - **并行调度**：同时启动多个[[子 Agent & 多 Agent 系统|子 Agent]] 处理独立任务
   - **工作隔离**：通过 [[Git Worktree]] 为每个[[子 Agent & 多 Agent 系统|子 Agent]] 创建独立工作目录
   - **资源分配**：合理分配[[计算]]资源给不同[[子 Agent & 多 Agent 系统|子 Agent]]

2. **与 [[Git Worktree]] 的关系**：
   - 在执行并行任务前，为每个[[子 Agent & 多 Agent 系统|子 Agent]] 预先创建独立的 worktree
   - 每个 worktree 对应一个分支和独立工作目录
   - 防止多个 Agent 同时修改相同文件时的冲突

3. **工作流程**：
   ```
   主 Agent 分析任务
   ↓
   识别可并行的任务单元
   ↓
   通过 [[using-git-worktrees Skill]] 为每个任务创建 worktree
   ↓
   启动并行子 Agent（每个在独立 worktree 中）
   ↓
   监控各子 Agent 进度
   ↓
   汇总并行工作的结果
   ```

4. **应用场景**：
   - **功能模块并行开发**：不同 Agent 开发不同功能模块
   - **测试并行执行**：多个 Agent 并行运行不同类型测试
   - **[[重构]]并行处理**：不同 Agent 负责不同组件的[[重构]]
   - **文档并行生成**：多个 Agent 并行生成不同类型文档

5. **优势**：
   - **提高效率**：充分利用多核 CPU 和并发能力
   - **降低风险**：每个 Agent 在隔离环境中工作，减少冲突
   - **可扩展性**：支持根据任务复杂度调整并行度

6. **限制与注意事项**：
   - 需要足够硬件资源支撑多个并行进程
   - 依赖 [[using-git-worktrees Skill]] 确保环境隔离
   - 某些任务无法并行化，需顺序执行

7. **与 [[Superpowers]] 流水线的关系**：
   - 通常在 [[using-git-worktrees Skill]] 之后执行
   - 为 [[subagent-driven-development Skill]] 提供并行基础设施
   - 最终结果汇总到主分支通过 finishing-a-development-branch

## 来源
- [[04-using-git-worktrees]] — Git Worktree 并行场景说明

## 相关
- [[Superpowers]] — part_of
- [[Git Worktree]] — uses for isolation
- [[using-git-worktrees Skill]] — prerequisite
- [[subagent-driven-development Skill]] — complementary skill
- [[writing-plans Skill]] — receives task breakdown