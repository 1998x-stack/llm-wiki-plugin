# Skill 06：executing-plans — 无子 Agent 时的批量顺序执行模式

> **系列位置**：Superpowers 深度解析 · 第 6 篇  
> **SKILL.md 位置**：`skills/executing-plans/SKILL.md`  
> **触发描述**：`Use when executing implementation plans in batches without subagent support`  
> **适用平台**：Gemini CLI 及其他不支持子 Agent 的平台

---

## 一句话定位

`executing-plans` 是 `subagent-driven-development` 的**降级版本**。当运行平台不支持子 Agent 时，由主 Agent 自己批量顺序执行计划任务，每完成一批后暂停并等待人工确认，用人工检查点替代自动化评审。

---

## 明确的降级声明

技能在开始时会主动提醒用户：

```
注意：告诉你的人类合作伙伴，Superpowers 在有子 Agent 支持的平台上
      效果好得多。如果可以，考虑切换到 Claude Code 或 Codex。

      如果子 Agent 可用，请改用 superpowers:subagent-driven-development。
```

这不是谦虚的免责声明，而是真实的能力边界告知。技能本身知道自己是降级方案。

---

## 核心执行逻辑

没有子 Agent 分担，主 Agent 自己按顺序处理每个任务：

```
读取计划文件
创建 TodoWrite 跟踪列表
        ↓
┌─── 批量执行循环 ───────────────────────────┐
│                                           │
│  执行 Task N                              │
│  （主 Agent 自己写代码、运行测试、Commit）  │
│                                           │
│  执行 Task N+1                            │
│  ...                                      │
│                                           │
│  完成一批（3-5 个任务，或主要节点）        │
│        ↓                                  │
│  暂停，汇报摘要：                          │
│  "完成了任务 1-3：                         │
│   ✅ Task 1: Hook 安装脚本               │
│   ✅ Task 2: Recovery 模式               │
│   ✅ Task 3: 错误处理                     │
│   是否继续执行任务 4-5？"                  │
│        ↓                                  │
│  等待人类确认                             │
│        ↓                                  │
│  继续下一批...                             │
└────────────────────────────────────────────┘
        ↓
所有任务完成
调用 finishing-a-development-branch
```

---

## 人工检查点：代替自动化评审

`subagent-driven-development` 用两个独立的评审子 Agent 做质量保证，而 `executing-plans` 用**人工检查点**替代：

| 质量保证机制 | subagent-driven-development | executing-plans |
|------------|---------------------------|----------------|
| 规格合规检查 | 独立 spec-reviewer 子 Agent | 主 Agent 自检 + 人工确认 |
| 代码质量检查 | 独立 code-reviewer 子 Agent | 人工确认 |
| 检查时机 | 每个任务完成后 | 每批任务完成后 |
| 是否阻断 | 是（评审不过不继续） | 依赖人工判断 |

---

## 遇到不确定时的处理原则

技能有一条简单但关键的规则：

> **Ask for clarification rather than guessing.**

主 Agent 在没有子 Agent 可以问的情况下，遇到任何不确定的情况，宁可停下来问用户，也不要假设一个答案继续执行。这防止了"静默地做错事"的问题。

---

## 批次划分建议

批次的划分不是固定的，建议按以下原则：

```
✅ 好的批次边界：
  - 一个逻辑功能组（例如：认证相关的 3 个任务）
  - 一个"检查点"（可以独立测试的里程碑）
  - 计划中明确标注的分段

❌ 避免的批次：
  - 太大（超过 5-6 个任务，确认时人工难以全面检查）
  - 太小（每个任务都停下来汇报，效率太低）
```

---

## 上下文窗口管理

由于主 Agent 需要持续执行，上下文窗口会随着任务进行逐渐填满。技能建议：

```
计划前期（任务 1-5）：正常执行
计划中期（任务 6-15）：注意上下文使用，适当精简汇报内容
计划后期（任务 16+）：
  - 如果上下文接近上限，在检查点提醒人类
  - 可能需要开新的会话，从当前进度继续
```

这也是为什么 `writing-plans` 要求频繁 Commit——每个任务完成后都有 Commit，即使会话中断，进度也不会丢失。

---

## 与 subagent-driven-development 的切换

如果在执行过程中，平台突然支持了子 Agent（比如用户切换了平台），可以中途切换：

```
已完成：Task 1, 2, 3（已 Commit）
当前进度：Task 4 未开始

→ 停止 executing-plans
→ 告知当前进度
→ 建议用户在 Claude Code 中开新会话
→ 新会话从 Task 4 开始，使用 subagent-driven-development
```

---

---

# Skill 07：dispatching-parallel-agents — 相互独立任务的并发编排

> **系列位置**：Superpowers 深度解析 · 第 7 篇  
> **SKILL.md 位置**：`skills/dispatching-parallel-agents/SKILL.md`  
> **触发时机**：存在多个相互独立、无依赖关系的任务，且平台支持子 Agent

---

## 一句话定位

当计划中包含多个**完全独立、互不依赖**的任务时，`dispatching-parallel-agents` 让主 Agent 同时派遣多个子 Agent 并发执行，从而将总耗时从"任务数 × 单任务时间"压缩到接近"1 × 单任务时间"。

---

## 与 subagent-driven-development 的核心差异

| 维度 | subagent-driven-development | dispatching-parallel-agents |
|------|----------------------------|-----------------------------|
| **任务顺序** | 串行（一个接一个） | 并行（同时执行） |
| **任务依赖** | 允许有依赖（Task B 依赖 Task A 的输出） | 必须完全独立 |
| **评审机制** | 每任务后双阶段评审 | 各子 Agent 完成后汇总评审 |
| **适用场景** | 功能实现（有依赖关系） | 批量生成（无依赖关系） |

---

## 什么任务适合并行？

```
✅ 适合并行化（完全独立）：
  - 为 5 个独立 API 端点各写测试
  - 同时更新 4 个不相关模块的文档
  - 并行处理 3 个独立的数据迁移脚本
  - 同时为 6 个独立组件生成类型定义

❌ 不适合并行化（有依赖/共享状态）：
  - Task B 需要 Task A 创建的数据库表
  - 两个任务都要修改 config.py 的同一区域
  - Task C 需要 Task A 和 B 都完成才能知道接口格式
  - 需要在共享内存/全局状态上做原子操作
```

---

## 前提条件：独立的 Worktree

并行子 Agent **必须**在独立的 worktree 中工作，否则文件修改会互相覆盖：

```bash
# 主 Agent 为每个并行任务组创建独立 worktree
git worktree add ../project-batch-1 -b feature/parallel-1
git worktree add ../project-batch-2 -b feature/parallel-2
git worktree add ../project-batch-3 -b feature/parallel-3
```

这也是为什么 `using-git-worktrees` 是 Superpowers 流水线的前置步骤——并行执行需要多个 worktree 已经就位。

---

## 上下文隔离原则

与 `subagent-driven-development` 相同，每个并行子 Agent 只接收**当前任务所需的最小上下文**，由主 Agent 精确构造：

```
主 Agent 为每个子 Agent 准备独立的 context 包：

子 Agent 1 的 context：
  - 任务 1 的完整文本
  - 任务 1 涉及的文件范围
  - 相关的项目背景（仅任务 1 需要的部分）

子 Agent 2 的 context：
  - 任务 2 的完整文本
  - 任务 2 涉及的文件范围
  - 相关的项目背景（仅任务 2 需要的部分）
```

子 Agent 之间**互不知道对方的存在**，也不共享状态。

---

## 并行执行流程

```
主 Agent 识别出独立的并行任务组
        ↓
为每个任务组创建独立 worktree
        ↓
同时派遣所有子 Agent（并发）：
  子 Agent 1 → worktree-1 → 实现 Task A
  子 Agent 2 → worktree-2 → 实现 Task B
  子 Agent 3 → worktree-3 → 实现 Task C
        ↓
等待所有子 Agent 完成
（任何一个 BLOCKED 或 NEEDS_CONTEXT → 主 Agent 处理）
        ↓
汇总所有子 Agent 的结果
评审（可以是顺序评审，也可以并发评审）
        ↓
将各 worktree 的变更合并回主分支
        ↓
调用 finishing-a-development-branch
```

---

## 实战效益计算

假设有 8 个独立的 API 端点测试需要编写，每个约 15 分钟：

```
串行执行（subagent-driven-development）：
  Task 1 → Task 2 → ... → Task 8
  总时间 ≈ 8 × 15 = 120 分钟

并行执行（dispatching-parallel-agents，假设并发上限 4）：
  第一批（Task 1-4 同时）→ 等待 → 第二批（Task 5-8 同时）
  总时间 ≈ 2 × 15 = 30 分钟

速度提升：4 倍
```

在实际中，并发上限受平台约束（Claude Code 当前有子 Agent 数量限制），但即使只能同时运行 2-3 个，速度提升也非常显著。

---

## 合并冲突的处理

并行执行后，各 worktree 的变更需要合并。如果不同子 Agent 恰好修改了同一个文件（这不应该发生，但可能出现于共享的测试 helper 文件等），主 Agent 需要处理合并冲突。

技能的建议：
- **设计阶段避免**：在 brainstorming 和 writing-plans 时，确保并行任务触碰的文件集合不重叠
- **发现冲突后**：由主 Agent（而不是子 Agent）处理合并，因为主 Agent 有全局视角

---

## 平台支持情况

| 平台 | 并行子 Agent | 并发上限 | 备注 |
|------|------------|---------|------|
| Claude Code | ✅ | 取决于平台设置 | 推荐平台 |
| Codex | ✅ | 需开启 `multi_agent = true` | 需要配置 |
| Cursor | ⚠️ 有限 | 通常 1-2 | 依赖版本 |
| Gemini CLI | ❌ | 0 | 降级到 executing-plans |

---

## 何时选择 dispatching-parallel-agents vs subagent-driven-development

```
任务有依赖关系？
  是 → subagent-driven-development（串行）
  否 → 继续判断

任务数量 ≥ 3 且平台支持并发？
  是 → dispatching-parallel-agents（并行）
  否 → subagent-driven-development（串行，但无依赖时效率较低）
```

实际使用中，两者也可以**混合**：计划的前半段有依赖，用 subagent-driven-development；后半段无依赖，切换到 dispatching-parallel-agents。

---

*上一篇：[Skill 06：executing-plans] | 下一篇：[Skill 08：test-driven-development]*
