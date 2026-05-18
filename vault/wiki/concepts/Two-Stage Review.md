---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["quality assurance", multi-agent, "review process", "software engineering", validation, AI工程]
aliases: ["Two-Stage Review", "两阶段评审", "双阶段审查", "Two Phase Review"]
relates_to:
  - target: "[[subagent-driven-development Skill]]"
    type: part_of
    confidence: 1.0
  - target: "[[Quality Assurance]]"
    type: implements
    confidence: 0.9
  - target: "[[Specification Compliance]]"
    type: relates_to
    confidence: 0.95
  - target: "[[Code Quality Review]]"
    type: extends
    confidence: 0.9
---

# Two-Stage Review

## 概述
Two-Stage Review 是一种质量保证流程，在 Subagent-Driven Development 中使用两个独立的评审阶段来确保任务完成质量：第一阶段评审规格合规性，第二阶段评审代码质量。这种分离确保了"做正确的事"先于"做得对不对"。

## 关键内容
1. **第一阶段：规格合规性评审（Spec Compliance Review）**：
   - **评审员角色**：怀疑论者（Skeptic），不相信实现[[子 Agent & 多 Agent 系统|子 Agent]] 的自述
   - **检查内容**：
     - 规格要求的每一个功能点都实现了吗？
     - 有没有实现规格没有要求的额外功能（违反 YAGNI）？
     - 读的是真实代码，而不是相信实现者说"完成了"
   - **设计理念**：No point reviewing code quality if the implementation doesn't match requirements

2. **第二阶段：代码质量评审（Code Quality Review）**：
   - **触发条件**：仅在 Phase A 通过后才触发
   - **检查内容**：
     - 代码是否遵循项目已有的约定和模式？
     - [[错误处理]]是否完整？类型安全？防御性编程？
     - 代码组织、命名规范、[[可维护性]]
     - 新创建的文件或修改的文件是否已经过大？（大文件往往意味着职责不清，需要拆分）

3. **评审顺序的重要性**：
   - 先确认"做了正确的事"，再审"做得对不对"
   - 顺序不能颠倒，因为如果实现不符合规格，高质量的代码也没有意义

4. **评审流程**：
   - 派遣 spec-reviewer [[子 Agent & 多 Agent 系统|子 Agent]] 进行规格合规性评审
   - 通过后派遣 code-quality-reviewer [[子 Agent & 多 Agent 系统|子 Agent]] 进行代码质量评审
   - 任何阶段发现问题都会回到实现[[子 Agent & 多 Agent 系统|子 Agent]] 进行修复，然后重新评审

5. **优势**：
   - **职责分离**：不同评审关注不同方面，避免混淆
   - **质量保证**：双重保障确保实现既符合规格又具备高质量
   - **清晰反馈**：明确[[区分]]规格问题和质量问题，便于修复

## 来源
- [[05-subagent-driven-development]] — Two-Stage Review 流程的详细说明

## 相关
- [[subagent-driven-development Skill]] — part_of
- [[Quality Assurance]] — implements
- [[Specification Compliance]] — relates_to
- [[Code Quality Review]] — extends
- [[Multi-Agent Orchestration]] — relates_to