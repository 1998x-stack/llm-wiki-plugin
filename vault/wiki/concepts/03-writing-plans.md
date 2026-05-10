---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [source, claude-skills, planning, documentation]
aliases: ["Skill 03: writing-plans", "writing-plans source"]
relates_to:
  - target: "[[writing-plans Skill]]"
    type: source_for
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[Plan Document Reviewer]]"
    type: mentions
  - target: "[[File Mapping]]"
    type: mentions
  - target: "[[executing-plans Skill]]"
    type: mentions
---

# Skill 03: writing-plans — 把设计文档拆解为原子级任务清单

## 概述
Source document describing the [[writing-plans Skill|writing-plans]] skill for breaking down specifications into atomic task lists. Part of the [[Superpowers]] series - detailed analysis of [[Claude_Code|Claude]] AI skills for software development.

## 关键内容

1. **核心目的**：
   - 将已批准的规格文档分解成"初级工程师也能执行"的原子级任务清单
   - 每个步骤 2-5 分钟、包含完整代码、精确文件路径、可复现的验证命令

2. **执行者画像假设**：
   - 技术能力合格，但几乎不了解工具链或问题域
   - 不擅长设计测试
   - 假设执行者为"充满热情但经验不足、品味糟糕、讨厌写测试的初级工程师"

3. **[[File Mapping|文件映射]]优先原则**：
   - 在定义任何任务之前，先完成[[File Mapping|文件映射]]（[[File Mapping]]）
   - 明确哪些文件将被创建或修改及各自的职责
   - 遵循小文件原则（更易推理、编辑可靠、高内聚）

4. **强制文档结构**：
   - 包含固定的 Header 结构
   - 任务粒度遵循 2-5 分钟原则
   - 每个任务包含完整的测试-实现-验证-提交流程

5. **计划评审子循环**：
   - 通过 [[plan-document-reviewer]] [[子 Agent & 多 Agent 系统|子 Agent]] 进行评审
   - 发现问题由同一 Agent 修复以保持上下文
   - 最多 5 次迭代后升级给人类

6. **执行路径选择**：
   - 有[[子 Agent & 多 Agent 系统|子 Agent]] 平台（[[Claude Code]]）：使用 [[subagent-driven-development Skill|subagent-driven-development]]
   - 无[[子 Agent & 多 Agent 系统|子 Agent]] 平台（如 [[Gemini CLI]]）：使用 [[executing-plans Skill|executing-plans]]

## 来源
- [[raw/articles/ai-tools/claude-skills/03-writing-plans.md]] — Source file location

## 相关
- [[writing-plans Skill]] — source_for
- [[Superpowers]] — part_of
- [[Plan Document Reviewer]] — mentions
- [[File Mapping]] — mentions
- [[executing-plans Skill]] — mentions