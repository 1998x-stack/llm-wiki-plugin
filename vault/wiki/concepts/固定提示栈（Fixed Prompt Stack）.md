---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["ai-engineering", "prompt-design", "agent-pattern", "LLM能力"]
aliases: ["Fixed Prompt Stack", "固定提示栈", "确定性上下文分配", "完整规范重复分配"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: used_by
  - target: "[[上下文窗口]]"
    type: relates_to
  - target: "[[Agent 迭代循环]]"
    type: enables
  - target: "[[AGENTS.md 项目约定文件]]"
    type: uses
supersedes: null
---

# 固定提示栈（Fixed Prompt Stack）

## 概述
固定提示栈是一种 Agent 上下文分配模式，每次迭代向 Agent 注入完全相同的完整规范内容（CLAUDE.md），以"浪费性重复"为代价换取零 [[上下文压缩]] 风险和确定性良态起点。

## 关键内容

1. **固定结构**：每次迭代都向 Agent 分配完全相同的 CLAUDE.md 内容：
   - **项目背景** — 每次都分配（"浪费"但必要）
   - **核心约束** — 每次都分配
   - **强制启动序列** — 每次都分配
   - **参考文件引用** — @prd.json @progress.txt @AGENTS.md

2. **为什么"浪费性重复"是必要的**：
   - **替代方案的问题**：每次只分配"差异"部分 → Agent 可能不知道它不知道什么 → 遗漏关键约束 → [[上下文腐烂]] 的变体
   - **固定提示栈的收益**：零[[上下文压缩]]风险，每次迭代都从已知良态开始
   - **代价分析**：N tokens × M 迭代 = 重复分配，但代价值得

3. **与 [[上下文窗口]] 的关系**：固定提示栈占用固定的[[上下文预算管理|上下文预算]]，每次迭代开始时这部分 token 被"预扣"。剩余窗口用于 Agent 的实际工作输出。这种可预测的分配模式使得上下文使用量可以精确估算。

4. **与 [[Agent 迭代循环]] 的关系**：固定提示栈是迭代循环的基础设施——每个新 Agent 实例启动时获得相同的规范上下文，确保行为的一致性和可预测性。

5. **确定性上下文分配的核心原则**：
   - 完整规范 > 差异增量（Agent 无法知道自己不知道什么）
   - 可预测性 > token 效率（每次迭代消耗相同 token 量）
   - 良态起点 > 上下文连续性（从干净状态开始优于从腐化状态继续）

6. **在 [[Ralph Loop]] 中的应用**：`ralph.sh` 每次迭代执行 `cat CLAUDE.md | claude --dangerously-skip-permissions`，将完整的固定提示栈注入全新的 Agent 实例。

## 来源
- [[raw/articles/ai-tools/ralph-loop/how-the-loop-works.md]] — Ralph Loop 核心原理深度解析

## 相关
- [[Ralph Loop]] — used_by（Ralph Loop 的核心上下文分配模式）
- [[上下文窗口]] — relates_to（固定提示栈占用固定的上下文预算）
- [[Agent 迭代循环]] — enables（为每次迭代提供确定性的规范起点）
- [[AGENTS.md 项目约定文件]] — uses（固定提示栈中引用的核心文件之一）
