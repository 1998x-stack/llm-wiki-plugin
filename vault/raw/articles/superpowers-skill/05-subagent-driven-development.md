# Skill 05：subagent-driven-development — 多 Agent 协作的执行主引擎

> **系列位置**：Superpowers 深度解析 · 第 5 篇  
> **SKILL.md 位置**：`skills/subagent-driven-development/SKILL.md`（276 行）  
> **触发描述**：`Use when executing implementation plans with independent tasks in the current session`  
> **子 Agent 支持要求**：Claude Code、Codex（需开启 `multi_agent = true`）

---

## 一句话定位

对计划中的每个任务派遣一个**全新的子 Agent** 来实现，完成后经历**两阶段评审**（规格合规性 → 代码质量），双双通过后标记任务完成并继续下一个。这是 Superpowers 在有子 Agent 支持的平台上的**首选执行引擎**。

> **核心公式**：Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

---

## 为什么不让主 Agent 直接做？

理解这个问题是理解整个技能设计的钥匙。

### 上下文窗口污染（Context Window Pollution）

当主 Agent 完成 brainstorming + writing-plans 之后，它的上下文已经积累了：
- 大量的需求讨论
- 设计方案的权衡辩论  
- 被否定的替代方案
- 用户的偏好说明

如果主 Agent 继续做实现，这些历史会：

1. **占用宝贵的上下文空间**，压缩实现任务能"看到"的代码量
2. **污染推理路径**，实现可能被"应该用方案 B 但被否定了"这样的历史干扰
3. **降低执行精度**，注意力分散在协调和执行两种完全不同的认知模式之间

### 子 Agent 的解法

```
主 Agent（Orchestrator）
  职责：读计划、维护状态、构建子 Agent 上下文、协调评审
  上下文：完整的计划 + 项目背景
  
子 Agent（Implementer，每任务一个）
  职责：只做当前任务
  上下文：仅当前任务所需的最小信息
  生命周期：任务完成即销毁
```

子 Agent 的上下文由主 Agent **精确构造**，不继承主 Agent 的对话历史。

> **官方原则**：They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

---

## 完整执行流程图

```
主 Agent 宣告：
"I'm using Subagent-Driven Development to execute this plan."
        ↓
读取计划文件（只读一次）
提取所有任务的完整文本和上下文
创建 TodoWrite 任务列表
        ↓
┌────────────── 每个任务循环 ──────────────────────────────┐
│                                                         │
│  派遣实现子 Agent（implementer-prompt.md）               │
│    ├── 子 Agent 有问题？                                 │
│    │     是 → 主 Agent 回答（NEEDS_CONTEXT）             │
│    │         再次派遣（同模型）                           │
│    │     否 → 子 Agent 完成任务                          │
│                                                         │
│  子 Agent 返回状态：                                     │
│    DONE → 继续下一步                                     │
│    DONE_WITH_CONCERNS → 读取关切，评估，必要时处理        │
│    NEEDS_CONTEXT → 提供信息，重新派遣                     │
│    BLOCKED → 升级模型 / 拆分任务 / 升级给人类             │
│                                                         │
│  ──────── Phase A：规格合规性评审 ────────────────────── │
│  派遣 spec-reviewer 子 Agent（spec-reviewer-prompt.md） │
│    ├── ✅ 合规 → 进入 Phase B                            │
│    └── ❌ 问题 → 实现子 Agent 修复 → 重新评审             │
│                                                         │
│  ──────── Phase B：代码质量评审 ──────────────────────── │
│  派遣 code-quality-reviewer 子 Agent                    │
│  （code-quality-reviewer-prompt.md）                    │
│    ├── ✅ 批准 → 在 TodoWrite 中标记任务完成              │
│    └── ❌ 问题 → 实现子 Agent 修复 → 重新评审             │
│                                                         │
│  还有更多任务？                                          │
│    是 → 回到循环开始                                     │
│    否 → 退出循环                                         │
└─────────────────────────────────────────────────────────┘
        ↓
派遣最终代码评审子 Agent（整体实现评审）
        ↓
调用 finishing-a-development-branch 技能
```

---

## 两阶段评审：为什么要分开？

### Phase A：规格合规性评审（Spec Compliance Review）

**评审员角色**：怀疑论者（Skeptic），不相信实现子 Agent 的自述。

评审的问题：
```
✅ 规格要求的每一个功能点都实现了吗？
✅ 有没有实现规格没有要求的额外功能（违反 YAGNI）？
✅ 读的是真实代码，而不是相信实现者说"完成了"？
```

> **设计逻辑**：No point reviewing code quality if the implementation doesn't match requirements.

先确认"做了正确的事"，再审"做得对不对"。顺序不能颠倒。

### Phase B：代码质量评审（Code Quality Review）

只在 Phase A 通过后才触发。评审内容：

```
- 代码是否遵循项目已有的约定和模式？
- 错误处理是否完整？类型安全？防御性编程？
- 代码组织、命名规范、可维护性
- 新创建的文件或修改的文件是否已经过大？
  （大文件往往意味着职责不清，需要拆分）
```

---

## 子 Agent 状态协议

实现子 Agent 完成任务后，必须返回以下四种状态之一：

| 状态 | 含义 | 主 Agent 处理 |
|------|------|-------------|
| `DONE` | 任务完成，测试全过，自检通过 | 进入 Phase A 评审 |
| `DONE_WITH_CONCERNS` | 完成但有值得注意的问题 | 读取关切评估严重性，必要时处理后再评审 |
| `NEEDS_CONTEXT` | 缺少信息，无法决策 | 提供信息，重新派遣同级模型 |
| `BLOCKED` | 遇到无法解决的阻碍 | 升级到更强模型 / 拆分任务 / 升级给人类 |

**自检要求**：实现子 Agent 在返回 `DONE` 之前，必须对自己的工作做自我评审：
- 所有测试通过了吗？
- 有没有遗漏的边界条件？
- 代码质量是否可以接受？

---

## 模型选择策略：用合适的模型做合适的事

技能内置了基于任务类型的模型选择指南（成本优化原则）：

| 任务类型 | 描述 | 推荐模型 |
|---------|------|---------|
| 机械性实现 | 独立函数、清晰规格、1-2 个文件 | **Cheap（快速廉价模型）** |
| 集成任务 | 多文件协调、模式匹配、调试 | **Standard（标准模型）** |
| 架构/设计/评审 | 全局视角、判断调用 | **Capable（最强模型）** |

> Most implementation tasks are mechanical when the plan is well-specified.

计划写得好，大多数实现任务其实只需要廉价快速模型，把昂贵模型留给真正需要判断力的评审工作。

---

## Prompt 模板系统

子 Agent 的派遣通过预定义的 Prompt 模板进行，模板文件存储在技能目录下：

```
skills/subagent-driven-development/
├── SKILL.md                         ← 主技能文档
├── implementer-prompt.md            ← 实现子 Agent 的 Prompt 模板
├── spec-reviewer-prompt.md          ← 规格评审子 Agent 的 Prompt 模板
└── code-quality-reviewer-prompt.md  ← 质量评审子 Agent 的 Prompt 模板
```

主 Agent 在派遣子 Agent 时，会将模板中的占位符替换为当前任务的具体内容：

```
Task tool（通用型）:
  description: "Implement Task N: [task name]"
  prompt: |
    [模板内容，包含占位符]
    [FULL TEXT of task] ← 替换为当前任务的完整文本
    [Scene-setting context] ← 替换为项目背景信息
```

---

## 实战对话完整示例

```
主 Agent: I'm using Subagent-Driven Development to execute this plan.
         [读取计划文件: docs/superpowers/plans/feature-plan.md]
         [提取所有 5 个任务]
         [创建 TodoWrite 任务列表]

─── Task 1: Hook 安装脚本 ───

         [提取 Task 1 的完整文本]
         [派遣实现子 Agent]

实现子 Agent: "开始之前——hook 应该安装在用户级别还是系统级别？"
             [状态：NEEDS_CONTEXT]

主 Agent:    "用户级别（~/.config/superpowers/hooks/）"

实现子 Agent: "明白了，开始实现..."
             [实现完成]
             "已完成：
              - 实现了 install-hook 命令
              - 加了测试，5/5 通过
              - 自检：发现遗漏了 --force 参数，已补充
              - 已 Commit: abc123f"
             [状态：DONE]

         [派遣 spec-reviewer 子 Agent]

spec-reviewer: ✅ 规格合规
               - 所有需求满足
               - 没有实现规格外的功能

         [获取 git SHA，派遣 code-quality-reviewer 子 Agent]

quality-reviewer: 优点：测试覆盖好，代码简洁
                  建议：错误消息可以更具体（Minor，不阻断）
                  结论：✅ 批准

         [标记 Task 1 完成]

─── Task 2: Recovery 模式 ───
...（依此类推）

─── 所有任务完成 ───

         [派遣最终代码评审子 Agent]
         [调用 finishing-a-development-branch]
```

---

## 评审中发现问题的处理示例

```
─── Task 2 的规格合规评审 ───

spec-reviewer: ❌ 问题发现：
               - 遗漏：进度报告（规格说"每 100 个条目报告一次"）
               - 超出范围：添加了 --json 标志（未在规格中要求）

         [重新派遣实现子 Agent，附上评审反馈]

实现子 Agent: - 删除了 --json 标志
             - 添加了每 100 个条目的进度报告
             - 重新测试，7/7 通过
             - 已 Commit: ghi789b
             [状态：DONE]

         [重新派遣 spec-reviewer]

spec-reviewer: ✅ 规格合规——所有问题已修复

         [派遣 code-quality-reviewer]
...
```

---

## 与 executing-plans 的根本区别

| 维度 | subagent-driven-development | executing-plans |
|------|----------------------------|----------------|
| 执行主体 | 子 Agent（每任务独立） | 主 Agent 自己 |
| 上下文隔离 | ✅ 完全隔离 | ❌ 共享累积上下文 |
| 规格合规评审 | ✅ 独立子 Agent 评审 | ❌ 主 Agent 自检 |
| 代码质量评审 | ✅ 独立子 Agent 评审 | ❌ 无独立视角 |
| 人工检查点 | 可选（任务间评审结果可见） | 必要（每批任务后暂停） |
| 质量上限 | 高 | 中 |
| 速度 | 快（并发潜力） | 较慢（顺序执行） |

---

*上一篇：[Skill 04：using-git-worktrees] | 下一篇：[Skill 06：executing-plans]*
