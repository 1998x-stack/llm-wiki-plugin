# Skill 03：writing-plans — 把设计文档拆解为原子级任务清单

> **系列位置**：Superpowers 深度解析 · 第 3 篇  
> **SKILL.md 位置**：`skills/writing-plans/SKILL.md`（116 行，3.19 KB）  
> **触发描述**：`Use when you have a spec or requirements for a multi-step task, before touching code`  
> **前置依赖**：`brainstorming` 完成、设计文档已批准

---

## 一句话定位

`writing-plans` 将已批准的规格文档分解成"充满热情但经验不足、品味糟糕、不了解项目上下文、讨厌写测试的初级工程师也能执行"的原子级任务清单——每个步骤 2-5 分钟、包含完整代码、精确文件路径、可复现的验证命令。

---

## 核心设定：假设执行者是谁？

技能文档开头就明确了"写作对象"的画像：

> 假设执行工程师**技术能力合格，但几乎不了解我们的工具链或问题域**。  
> 假设他们**不擅长设计测试**。

这个设定非常关键：它要求计划的编写者（主 Agent）不能偷懒，必须把每个细节——包括测试设计、精确命令、预期输出——都写清楚。

---

## 开始前的首要动作：文件映射

在定义任何任务之前，技能要求先完成**文件映射（File Mapping）**：

> 在定义任务之前，先列出哪些文件将被创建或修改，以及每个文件的职责。这是锁定分解决策的地方。设计具有清晰边界和良好定义接口的单元。每个文件应该有一个明确的职责。

这个步骤强制主 Agent 在写第一行代码之前，先把模块边界和文件职责想清楚，而不是边写边拆。

**偏好小文件原则**：
- 你更能对小文件推理清晰
- 小文件的编辑更可靠
- 一起修改的文件应该住在一起（Cohesion）

---

## 计划文档的强制 Header

每份计划文档必须以固定格式开头（这个 Header 不是建议，是强制）：

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [一句话描述构建什么]

**Architecture:** [2-3 句话描述整体方法]

**Tech Stack:** [关键技术/库]

---
```

Header 里的 `> **For agentic workers:**` 这段话至关重要——它是给下一个读取此计划的 Agent 看的强制指令，确保执行阶段也用正确的技能。

---

## 任务粒度：2-5 分钟原则

每个 Step 是一个独立的可执行动作，耗时约 2-5 分钟：

```markdown
### Task N: [组件名称]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: 写失败测试**
- [ ] 动作描述

```python
def test_specific_behavior():
    result = function(input_val)
    assert result == expected_val
```

**Step 2: 运行确认失败**
- [ ] Run: `pytest tests/path/test.py::test_name -v`
- [ ] Expected output: `FAILED - AssertionError: ...`

**Step 3: 写最少实现代码**
- [ ] 动作描述

```python
def function(input_val):
    return expected_val
```

**Step 4: 运行确认通过**
- [ ] Run: `pytest tests/path/test.py::test_name -v`
- [ ] Expected: `PASSED`

**Step 5: Commit**
- [ ] ```bash
      git add tests/path/test.py src/path/file.py
      git commit -m "feat: add specific feature"
      ```
```

注意 Steps 使用 `- [ ]` 复选框语法，供执行子 Agent 用 `TodoWrite` 跟踪。

---

## 什么不能出现在计划里

| 禁止写法 | 正确写法 |
|---------|---------|
| "加一个验证函数" | 提供完整函数代码 |
| "运行测试" | `pytest tests/specific.py::test_name -v` + 预期输出 |
| "类似地……" | 每个重复的结构都完整写出 |
| "参考 X 实现" | 直接写出实现代码 |
| "测试应该覆盖边界条件" | 写出具体的边界条件测试代码 |

**计划里不能有任何需要执行者自行判断的内容。**

---

## 计划评审子循环（Plan Review Loop）

写完计划后，技能会触发一个**计划文档评审子 Agent**（`plan-document-reviewer-prompt.md`）：

```
写完计划文档
       ↓
派遣 plan-document-reviewer 子 Agent 评审
       ↓
发现问题？
  是 → 同一个 Agent（写计划的）修复（保持上下文），再次评审
  否 → 评审通过
       ↓
最多 5 次迭代，超出 → 升级给人类
```

**关键设计**：与其他技能中评审由不同子 Agent 做不同，这里修复仍由**写计划的同一 Agent**来做，原因是"需要保留编写上下文"。

大型计划的评审按 Chunk 分段进行（每段 ≤1000 行，以 `## Chunk N:` 为分隔符），防止单次评审窗口溢出。

---

## 存储路径

```
docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md
```

（用户自定义优先于此默认路径）

每个子系统独立一份计划。如果 brainstorming 阶段没有正确分拆子系统，writing-plans 发现后要提醒重新分拆，**不能把多个子系统合并进一份计划**。

---

## 执行移交：两条路径的选择

计划写完并通过评审后，主 Agent 询问执行方式：

```
计划已保存到 docs/superpowers/plans/<filename>.md

两种执行方式：

1. 子 Agent 驱动（当前会话）
   - 每个任务派一个新子 Agent
   - 任务间有双阶段代码评审
   - 快速迭代，适合实时监控

2. 并行会话（独立会话）
   - 在新会话中使用 executing-plans
   - 批量执行，有人工检查点
   - 适合无人值守执行

选择哪种？
```

**有子 Agent 的平台（Claude Code、Codex）**：必须（REQUIRED）使用 `subagent-driven-development`

**无子 Agent 的平台（Gemini CLI）**：使用 `executing-plans`

---

## 与 brainstorming 的衔接细节

writing-plans 收到的设计文档来自 brainstorming，但有一个重要的衔接检查：

> 如果规格文档覆盖多个独立子系统，它本应在 brainstorming 阶段被拆分。如果没有被拆分，建议将其拆分为独立计划——每个子系统一份。每份计划应该独立产出可工作、可测试的软件。

这个检查防止了"大计划陷阱"——一份计划试图覆盖整个大型项目，导致任务依赖关系混乱。

---

## 核心原则汇总

| 原则 | 具体要求 |
|------|---------|
| **DRY** | 计划文档本身也要 DRY；重复的步骤用引用，不要复制 |
| **YAGNI** | 严格按规格实现，不加"将来可能用到的"内容 |
| **TDD** | 每个 Task 都以写测试开始（Red → Green → Refactor） |
| **频繁 Commit** | 每个 Task 完成后立即 Commit，不积累 |
| **精确路径** | 所有文件路径必须是精确的相对路径，不允许模糊描述 |
| **完整代码** | 代码必须在计划文档里完整写出，不允许"参考 X 实现" |

---

## 宣告语

技能要求 Agent 在开始时显式宣告：

```
"I'm using the writing-plans skill to create the implementation plan."
```

宣告的意义不是仪式，而是让人类合作伙伴知道"Agent 当前处于计划写作阶段，而不是实现阶段"。

---

*上一篇：[Skill 02：brainstorming] | 下一篇：[Skill 04：using-git-worktrees]*
